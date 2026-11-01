#!/usr/bin/env python3
"""Check links, anchors, and assets in a built MkDocs site.

Internal checks are self-contained and deterministic. External checks are
opt-in because they depend on the network and on third-party availability.

Usage:
    python3 scripts/check_links.py site
    python3 scripts/check_links.py site --external
"""

import argparse
import os
import posixpath
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

SKIP_SCHEMES = {"mailto", "tel", "javascript", "data", "ftp", "file"}
EXTERNAL_SCHEMES = {"http", "https"}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self._in_anchor = False
        self._anchor_href = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        for attr in ("href", "src"):
            value = attrs.get(attr)
            if value:
                self.links.append((tag, attr, value.strip()))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def iter_html_files(site_dir):
    for root, dirs, files in os.walk(site_dir):
        dirs.sort()
        for name in sorted(files):
            if name.endswith(".html"):
                yield os.path.join(root, name)


def page_url(site_dir, path):
    return "/" + os.path.relpath(path, site_dir).replace(os.sep, "/")


def resolve_target(site_dir, source, url_path, base_path):
    """Return the filesystem path a URL path points to, or None."""
    if url_path.startswith("/"):
        if base_path and (url_path == base_path or url_path.startswith(base_path + "/")):
            url_path = url_path[len(base_path):]
        url_path = url_path.lstrip("/")
        candidate = os.path.join(site_dir, *url_path.split("/"))
    else:
        candidate = os.path.join(os.path.dirname(source), *url_path.split("/"))

    candidate = posixpath.normpath(candidate.replace(os.sep, "/"))
    site_root = os.path.abspath(site_dir)
    if os.path.commonpath([site_root, os.path.abspath(candidate)]) != site_root:
        return None

    if os.path.isdir(candidate):
        candidate = os.path.join(candidate, "index.html")
    if os.path.isfile(candidate):
        return candidate
    if not os.path.splitext(candidate)[1]:
        for suffix in ("/index.html", ".html"):
            if os.path.isfile(candidate + suffix):
                return candidate + suffix
    return None


def load_anchors(cache, site_dir, path):
    if path not in cache:
        parser = PageParser()
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            parser.feed(handle.read())
        cache[path] = parser.ids
    return cache[path]


def check_external(url, timeout):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "dsa-docs-link-check/1.0"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return None
    except urllib.error.HTTPError as exc:
        if exc.code in (403, 405, 429):
            return f"HTTP {exc.code} (treated as reachable but restricted)"
        return f"HTTP {exc.code}"
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return str(exc)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site_dir", help="Path to the built site directory")
    parser.add_argument(
        "--base-path",
        default="/digital_slide_archive/docs",
        help="URL path prefix used by site_url (default: /digital_slide_archive/docs)",
    )
    parser.add_argument(
        "--external",
        action="store_true",
        help="Also request external http/https links",
    )
    parser.add_argument("--timeout", type=float, default=15.0, help="External request timeout")
    args = parser.parse_args()

    site_dir = os.path.abspath(args.site_dir)
    if not os.path.isdir(site_dir):
        print(f"error: site directory not found: {site_dir}", file=sys.stderr)
        return 2

    base_path = "/" + args.base_path.strip("/")
    anchor_cache = {}
    broken = []
    checked_internal = 0
    checked_external = 0
    skipped_external = 0

    external_results = {}

    for source in iter_html_files(site_dir):
        with open(source, "r", encoding="utf-8", errors="replace") as handle:
            page = PageParser()
            page.feed(handle.read())

        source_url = page_url(site_dir, source)
        for tag, attr, raw_url in page.links:
            if raw_url.startswith("#"):
                parts = urllib.parse.urlsplit(raw_url)
                target = source
                fragment = urllib.parse.unquote(parts.fragment)
            else:
                parts = urllib.parse.urlsplit(raw_url)
                scheme = parts.scheme.lower()
                if scheme in EXTERNAL_SCHEMES or parts.netloc:
                    if not args.external:
                        skipped_external += 1
                        continue
                    if raw_url not in external_results:
                        external_results[raw_url] = check_external(raw_url, args.timeout)
                        checked_external += 1
                    problem = external_results[raw_url]
                    if problem and "treated as reachable" not in problem:
                        broken.append((source_url, raw_url, problem))
                    continue
                if scheme and scheme not in SKIP_SCHEMES:
                    continue
                if scheme in SKIP_SCHEMES:
                    continue

                url_path = urllib.parse.unquote(parts.path)
                if not url_path:
                    target = source
                else:
                    target = resolve_target(site_dir, source, url_path, base_path)
                    if target is None:
                        broken.append((source_url, raw_url, "target not found"))
                        continue
                fragment = urllib.parse.unquote(parts.fragment)

            checked_internal += 1
            if fragment:
                anchors = load_anchors(anchor_cache, site_dir, target)
                if fragment not in anchors:
                    broken.append(
                        (source_url, raw_url, f"anchor #{fragment} not found in {page_url(site_dir, target)}")
                    )

    for source_url, raw_url, reason in sorted(set(broken)):
        print(f"BROKEN {source_url} -> {raw_url}: {reason}")

    print(
        f"Checked {checked_internal} internal link(s) across "
        f"{sum(1 for _ in iter_html_files(site_dir))} page(s)."
    )
    if args.external:
        print(f"Checked {checked_external} external link(s).")
    else:
        print(f"Skipped {skipped_external} external link(s); pass --external to check them.")

    if broken:
        print(f"FAILED: {len(set(broken))} broken link(s).")
        return 1
    print("OK: no broken links found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
