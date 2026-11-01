# DSA documentation site

Source for a consolidated Digital Slide Archive documentation site, built with
MkDocs Material. This repository is a **staging area**: it pulls guides and
tutorials from across the DSA ecosystem into one place while the documentation
is rebuilt.

**Preview:** <https://gutman-lab.github.io/dsa-docs/> (built from `main` by
GitHub Actions and published with GitHub Pages).

- `docs/` is the site source.
- `SOURCES.md` records where each page came from and what is still queued.
- The canonical upstream code lives in
  [`DigitalSlideArchive/digital_slide_archive`](https://github.com/DigitalSlideArchive/digital_slide_archive).

## Publishing

The site is a static MkDocs build. `.github/workflows/docs.yml` builds it with
`mkdocs build --strict`, runs the link checker, and deploys the result to
GitHub Pages on every push to `main`. Pull requests run the same build and
check but do not deploy.

- `site_url` in `mkdocs.yml` must match the Pages URL: for this repository that
  is `https://gutman-lab.github.io/dsa-docs/`.
- The link checker defaults to the matching URL prefix (`/dsa-docs`). Change
  both values together if the site moves to another path or domain.
- Pages is enabled for this repository with **GitHub Actions** as the source.
  There is no `gh-pages` branch and no deploy from a local machine.

To force a rebuild without a content change, run the `docs` workflow manually
from the Actions tab.

## Requirements

- Python 3.9 or newer.
- The versions pinned in `requirements.txt`: MkDocs 1.6.1, MkDocs Material
  9.8.0, and pymdown-extensions 12.3.

## Build locally

From the repository root:

```bash
python3 -m venv .venv-docs
. .venv-docs/bin/activate
pip install -r requirements.txt
mkdocs build --strict
```

The built site is written to `site/`. `--strict` turns MkDocs warnings into
errors, which catches broken navigation entries and malformed links during the
build.

To preview with live reload:

```bash
mkdocs serve
```

Then open <http://127.0.0.1:8000/>.

## Check links

`scripts/check_links.py` checks internal page links, anchors, and assets in the
built site:

```bash
python3 scripts/check_links.py site
```

Use `--external` to also request every external `http`/`https` link. External
checks depend on the network and on third-party sites, so they are not part of
the baseline command.

The full baseline is:

```bash
mkdocs build --strict && python3 scripts/check_links.py site
```

Exit code 0 means the build had no warnings and every internal link resolved.
If the site moves to a different URL path, pass the new prefix explicitly:

```bash
python3 scripts/check_links.py site --base-path /new-prefix
```

## Add a page

1. Add the Markdown file under `docs/`.
2. Add it to `nav` in `mkdocs.yml`; `--strict` fails if a nav entry has no file.
3. Add a row to `SOURCES.md` naming the upstream source and its commit or date.
4. Run the baseline command.

## Content policy

- Consolidation over originality: replicating an existing page here is fine
  while we converge on one canonical copy. Always record the source.
- Mark commands as verified or unverified. Never call an untested command
  "tested".
- Preserve attribution and license notices when adapting upstream material.
- Do not change hosting, publishing, or release settings from this repository
  without a separate approval.
