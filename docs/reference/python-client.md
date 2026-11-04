# Python client

`girder-client` is the supported Python client for the Girder API that DSA
exposes. It handles authentication, chunked uploads, and the small differences
between Girder routes, so scripts stay short and do not reimplement HTTP
plumbing.

The script below was run end to end against a local DSA 5 install on
2026-11-02. It signs in, resolves a path, walks the collection tree, reads and
writes metadata, creates and lists annotations, uploads a file, downloads and
checks a file, fetches a tile, and submits and polls an analysis job. See
[Verified status](#verified-status).

## Install

```bash
python3 -m pip install girder-client
```

The examples were tested with `girder-client` 5.0.22 from PyPI and with the
5.0.23.dev5 build bundled in the DSA 5 image. Both work. Use the version that
matches your server's Girder major release. If you pin a version, pin it with
the rest of your environment, not in a shared system Python.

## Authenticate

`girder-client` takes the API base URL including `/api/v1`:

```python
import os
import girder_client

gc = girder_client.GirderClient(
    apiUrl=os.environ.get("DSA_API_URL", "http://127.0.0.1:8080/api/v1")
)

# Preferred for automation: an API key. girder-client exchanges it for a token.
gc.authenticate(apiKey=os.environ["DSA_API_KEY"])

# Or username and password. Use only over HTTPS and keep the password in the
# environment, not in the source file.
# gc.authenticate(os.environ["DSA_USERNAME"], os.environ["DSA_PASSWORD"])
```

`authenticate(apiKey=...)` calls `POST /api_key/token` for you. Passing the key
directly as a `Girder-Token` header does not work on DSA 5; let the client do
the exchange.

The token is stored on the client and sent on later calls. Do not print
`gc.token` or put it in logs.

## The script

Save this as `dsa_client.py`, set the environment variables, and run it:

```bash
export DSA_API_URL="http://127.0.0.1:8080/api/v1"
export DSA_API_KEY="<key>"
export DSA_ITEM_PATH="/collection/My Collection/My Folder/my-slide.svs"
export DSA_UPLOAD_FILE="/path/to/another-slide.svs"   # optional
python3 dsa_client.py
```

```python
#!/usr/bin/env python3
"""Minimal Digital Slide Archive client for the DSA API cookbook.

Environment:
  DSA_API_URL    e.g. http://127.0.0.1:8080/api/v1
  DSA_API_KEY    preferred, or DSA_USERNAME / DSA_PASSWORD
  DSA_ITEM_PATH  Girder path to an existing item, e.g.
                 /collection/API Cookbook Test/Slides/test-slide.tif
  DSA_DOWNLOAD   local path for the downloaded file (optional)
  DSA_UPLOAD_FILE  local file to upload into the item's folder (optional)
  DSA_CLI_NAME   Slicer CLI task to run (default BackgroundIntensity)
"""
import hashlib
import os
import time

import girder_client

API_URL = os.environ.get("DSA_API_URL", "http://127.0.0.1:8080/api/v1")
ITEM_PATH = os.environ["DSA_ITEM_PATH"]
DOWNLOAD = os.environ.get("DSA_DOWNLOAD", "/tmp/dsa-cookbook-download.tif")
CLI_NAME = os.environ.get("DSA_CLI_NAME", "BackgroundIntensity")


def connect():
    gc = girder_client.GirderClient(apiUrl=API_URL)
    if os.environ.get("DSA_API_KEY"):
        gc.authenticate(apiKey=os.environ["DSA_API_KEY"])
    else:
        gc.authenticate(os.environ["DSA_USERNAME"], os.environ["DSA_PASSWORD"])
    return gc


def main():
    gc = connect()
    item = gc.get("resource/lookup", parameters={"path": ITEM_PATH})
    item_id = item["_id"]
    folder = gc.getFolder(item["folderId"])
    print("item:", item_id, item["name"])
    print("folder:", folder["_id"], folder["name"])

    for coll in gc.listCollection():
        for fold in gc.listFolder(coll["_id"], parentFolderType="collection"):
            for it in gc.listItem(fold["_id"]):
                print("tree:", coll["name"], "/", fold["name"], "/", it["name"])

    print("metadata before:", item.get("meta", {}))
    gc.put(f"item/{item_id}/metadata", json={"Cookbook": "girder-client"})
    print("metadata after:", gc.getItem(item_id).get("meta", {}))

    annotations = gc.get(f"annotation/item/{item_id}")
    print("annotations before:", len(annotations))
    gc.post(f"annotation/item/{item_id}", json=[{"annotation": {
        "name": "girder-client example",
        "elements": [{
            "type": "rectangle",
            "center": [512, 512, 0],
            "width": 128,
            "height": 128,
            "lineColor": "#ff0000",
        }],
    }}])
    print("annotations after:", len(gc.get(f"annotation/item/{item_id}")))

    upload_path = os.environ.get("DSA_UPLOAD_FILE")
    if upload_path:
        new_item = gc.post("item", parameters={
            "folderId": folder["_id"],
            "name": os.path.basename(upload_path),
        })
        gc.uploadFileToItem(new_item["_id"], upload_path, mimeType="image/tiff")
        print("uploaded:", new_item["_id"])

    files = gc.get(f"item/{item_id}/files")
    file_id = files[0]["_id"]
    gc.downloadFile(file_id, DOWNLOAD)
    with open(DOWNLOAD, "rb") as fp:
        digest = hashlib.sha512(fp.read()).hexdigest()
    print("download sha512 matches:", digest == files[0]["sha512"])

    tile = gc.get(f"item/{item_id}/tiles/zxy/0/0/0", jsonResp=False)
    print("tile:", tile.status_code, tile.headers.get("content-type"), len(tile.content), "bytes")

    cli = next((c for c in gc.get("slicer_cli_web/cli") if c["name"] == CLI_NAME), None)
    if cli:
        job = gc.post(f"slicer_cli_web/cli/{cli['_id']}/run", parameters={
            "slide_path": file_id,
            "sample_fraction": "0.1",
            "magnification": "1.25",
            "tissue_seg_mag": "1.25",
            "min_coverage": "0.1",
            "sample_approximate_total": "-1",
            "tile_grouping": "256",
            "scheduler": "",
            "outputAnnotationFile_folder": folder["_id"],
            "outputAnnotationFile": "girder-client-background.anot",
        })
        print("job:", job["_id"], job["status"])
        while job["status"] not in (3, 4, 5):
            time.sleep(2)
            job = gc.get(f"job/{job['_id']}")
        print("job finished:", job["status"], job.get("log", [""])[-1].strip())


if __name__ == "__main__":
    main()
```

Expected output is a line per step, ending with the job status. The exact item
and job ids differ on every run. On the local test instance the last lines were:

```text
download sha512 matches: True
tile: 200 image/jpeg 15994 bytes
job: 6ae89d0cad9f85a8521df92d 0
job finished: 3 >> Writing annotation file ...
```

## What the calls do

| Call | Route | Notes |
| --- | --- | --- |
| `gc.get("resource/lookup", parameters={"path": ...})` | `GET /resource/lookup` | Absolute path under `/collection/<name>` or `/user/<login>`. |
| `gc.listCollection()` | `GET /collection` | Paginated; pass `limit` and `offset` for large instances. |
| `gc.listFolder(id, parentFolderType="collection")` | `GET /folder` | Use `parentFolderType="folder"` for nested folders. |
| `gc.listItem(id)` | `GET /item` | Lists items in a folder. |
| `gc.post("item", parameters=...)` | `POST /item` | Creates the item that will hold the slide file. |
| `gc.uploadFileToItem(item_id, path)` | `POST /file`, `POST /file/chunk` | Chooses chunks automatically and returns the final file record. |
| `gc.put(f"item/{id}/metadata", json=...)` | `PUT /item/<id>/metadata` | Merges keys; it does not replace the metadata object. |
| `gc.get(f"annotation/item/{id}")` | `GET /annotation/item/<id>` | Returns annotation records, including elements. |
| `gc.post(f"annotation/item/{id}", json=[...])` | `POST /annotation/item/<id>` | Returns the number created, not the records. |
| `gc.downloadFile(file_id, path)` | `GET /file/<id>/download` | The local file is written to `path`. |
| `gc.get(..., jsonResp=False)` | `GET /item/<id>/tiles/zxy/...` | Returns the raw `requests` response so you can write `.content`. |
| `gc.post(f"slicer_cli_web/cli/{id}/run", parameters=...)` | `POST /slicer_cli_web/cli/<id>/run` | Form fields only; image inputs are file ids. |
| `gc.get(f"job/{id}")` | `GET /job/<id>` | Poll until status is `3`, `4`, or `5`. |

`uploadFileToItem` computes the file size, sends chunks of up to 64 MiB, and
returns the file document with `size` and `sha512`. The server computes the
SHA-512; the client does not supply one. See
[REST API: Upload a slide or file](rest-api.md#upload-a-slide-or-file) for the
raw HTTP version and the chunk-size rules.

## Errors

`girder-client` raises `girder_client.HttpError` for non-2xx responses. The
exception exposes `status` and `responseText`:

```python
try:
    item = gc.get("resource/lookup", parameters={"path": path})
except girder_client.HttpError as exc:
    print(exc.status, exc.responseText)
    raise
```

The status meanings are the same as the HTTP API:

- `401`: no token, an expired token, or an invalid token.
- `403`: signed in, but the account lacks access to the collection, folder, or
  item.
- `404`: the route does not exist; check `apiUrl` includes `/api/v1`.
- `400`: a missing or invalid parameter, an id that does not resolve, or a bad
  path.

A valid token with no permission returns `403`, not `404`. A nonexistent object
id usually returns `400` (`Invalid item id`) rather than `404`. See
[REST API: Common error responses](rest-api.md#common-error-responses) for the
full table.

## Next

- [REST API cookbook](rest-api.md): the same routes with `curl`.
- [Connect to a server](../tutorials/connect.md): create an account and an API
  key in the browser.
- [Run an analysis](../tutorials/run-an-analysis.md): the HistomicsUI analysis
  workflow.

## Verified status

!!! info "Verified status"

    Verified on **2026-11-02** against a local DSA 5 stack built from
    `DigitalSlideArchive/digital_slide_archive` at `2e16b9a` using the
    `dsarchive/dsa_common_5` image:

    - Girder `5.0.23.dev5+g70eb94dcd` (`GET /api/v1/system/version`)
    - `large_image` and `large_image_annotation` `1.35.7.dev217+g09c6d7801`
    - HistomicsUI `1.8.1.dev208+gee5f4c0da.d20261030`
    - `girder-client` `5.0.22` (PyPI) and `5.0.23.dev5+g70eb94dcd`
      (bundled in the DSA 5 image)

    The script was executed with API-key authentication and with
    username/password authentication. The upload, metadata, annotation,
    download, tile, and analysis steps all completed; the downloaded SHA-512
    matched the server's `sha512`. The public demo runs an older Girder
    (`3.2.18.dev2+g339bcdfe6`), so it was used only for read-only HTTP checks,
    not for this script.

    Not tested: two-factor login, non-admin write permissions, external
    assetstores, the `hashsum_download` plugin, and analysis images other than
    `dsarchive/histomicstk:latest`.
