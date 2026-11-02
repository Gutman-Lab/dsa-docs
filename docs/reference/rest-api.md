# REST API cookbook

The Digital Slide Archive exposes the Girder REST API under `/api/v1`. These
recipes cover the routes DSA users and integrations need most: signing in,
finding data, uploading slides, reading and writing metadata, downloading tiles,
working with annotations, and running analysis jobs.

Every snippet was executed against a local DSA 5 installation on 2026-11-02.
The read-only recipes were also checked against the public demo. See
[Verified status](#verified-status) for exact versions and for what was not
tested.

!!! info "Set the base URL first"

    All examples use one environment variable, so they work against a local
    server, the demo, or a production instance without edits:

    ```bash
    export DSA_URL="http://localhost:8080/api/v1"
    ```

    The public demo is `https://demo.kitware.com/histomicstk/api/v1`. It runs an
    older Girder release than a current DSA 5 install, so use it for read-only
    checks and follow the version notes in [Verified status](#verified-status).

## Before you start

You need `curl` and [`jq`](https://jqlang.github.io/jq/). The examples also use
GNU `stat`, `sha512sum`, and `split`; on macOS, use `stat -f%z` and
`shasum -a 512`.

The API returns JSON. Most write routes accept form fields, not a JSON body.
The exceptions are metadata, annotations, and access updates, which are called
out below. If you send a JSON body to a form route, Girder reports that the form
parameter is missing.

!!! warning "Credentials are secrets"

    A token is a bearer credential: anyone who has it can act as you until it
    expires. Do not commit tokens, paste them into issues, or put them in a URL
    that will be logged. Use environment variables as shown, serve DSA over
    HTTPS, and revoke keys you no longer need.

## Authenticate

### Username and password

DSA 5 uses `GET /user/authentication` with HTTP Basic authentication. The
older `POST` form of this route is not registered; sending a form body returns
`No matching route for "POST authentication"`.

```bash
export DSA_USER="<your login>"
read -rsp "DSA password: " DSA_PASSWORD; echo
export DSA_TOKEN=$(curl -s -u "$DSA_USER:$DSA_PASSWORD" \
  "$DSA_URL/user/authentication" | jq -r '.authToken.token')
test -n "$DSA_TOKEN" && echo "signed in"
curl -s -H "Girder-Token: $DSA_TOKEN" "$DSA_URL/user/me" \
  | jq '{login, admin}'
```

The response contains the user and an `authToken`:

```json
{
  "authToken": {
    "expires": "2027-05-01T14:22:32.599463+00:00",
    "scope": ["core.user_auth"],
    "token": "<token>"
  },
  "message": "Login succeeded.",
  "user": {"login": "admin", "admin": true}
}
```

Send the token in the `Girder-Token` header on later calls. HTTP Basic is only
base64 encoding, not encryption, so use HTTPS for anything other than a local
test. `read` keeps the password out of shell history, but `-u` still places it
in the `curl` process arguments. On a shared host, use `curl -u "$DSA_USER"` and
let `curl` prompt, or keep the credentials in a mode-600 `--netrc-file`.

### API key

Create a key in the web UI under **My account** → **API keys**, or with the API:

```bash
curl -s -X POST -H "Girder-Token: $DSA_TOKEN" "$DSA_URL/api_key" \
  --data-urlencode "name=my-script" | jq '{name, key, _id}'
```

Exchange the key for a short-lived token:

```bash
export DSA_API_KEY="<key from the previous step>"
export DSA_TOKEN=$(curl -s -X POST "$DSA_URL/api_key/token" \
  --data-urlencode "key=$DSA_API_KEY" | jq -r '.authToken.token')
```

Send the key as a form field. `POST /api_key/token` is the only accepted method,
and a `POST` with no body fails with `411 Length Required`. This also keeps the
key out of the URL, where proxies and access logs may record it.

On DSA 5, passing an API key directly as `Girder-Token` does not authenticate
the request: Girder ignores the unknown token and treats the call as anonymous,
so protected routes return `401`. Exchange it first, as above.
(`girder-client` does this exchange for you when you call
`authenticate(apiKey=...)`; see the [Python client](python-client.md).)

**Security trade-off.** Passwords are sent on every sign-in and are only as safe
as the connection. API keys are longer-lived bearer secrets, but they can be
listed, deactivated, and scoped without changing the account password. For
automation, use an API key with the narrowest scope that works, keep it in a
secret manager, and exchange it for a short-lived token at the start of a run.
Never commit either credential.

### Confirm the token

```bash
curl -s -H "Girder-Token: $DSA_TOKEN" "$DSA_URL/user/me" | jq '{login, admin}'
```

## List collections, folders, and items

Listing uses the core Girder routes. Every list is paginated with `limit` and
`offset`; the default limit is 50, and `limit=0` asks for no limit.

```bash
curl -s -H "Girder-Token: $DSA_TOKEN" "$DSA_URL/collection" \
  | jq -r '.[] | [._id, .name] | @tsv'
```

Pick a collection id, then list its folders and their items:

```bash
export COLLECTION_ID="<collection id>"
curl -s -H "Girder-Token: $DSA_TOKEN" \
  --get "$DSA_URL/folder" \
  --data-urlencode "parentType=collection" \
  --data-urlencode "parentId=$COLLECTION_ID" \
  | jq -r '.[] | [._id, .name] | @tsv'

export FOLDER_ID="<folder id>"
curl -s -H "Girder-Token: $DSA_TOKEN" \
  --get "$DSA_URL/item" \
  --data-urlencode "folderId=$FOLDER_ID" \
  | jq -r '.[] | [._id, .name, .size] | @tsv'
```

### Resolve a path to an item id

`GET /resource/lookup` accepts an absolute Girder path. This is usually safer
than copying ids into a script:

```bash
curl -s -H "Girder-Token: $DSA_TOKEN" \
  --get "$DSA_URL/resource/lookup" \
  --data-urlencode "path=/collection/My Collection/My Folder/my-slide.svs" \
  | jq '{_id, _modelType, name, folderId}'
```

The path must start with `/collection/<collection name>` or
`/user/<login>`. Names are case-sensitive and must match exactly.

## Upload a slide or file

DSA stores a slide as an **item** with an image file attached. Creating the item
and uploading the file are two calls:

```bash
export ITEM_ID=$(curl -s -X POST -H "Girder-Token: $DSA_TOKEN" \
  "$DSA_URL/item" \
  --data-urlencode "folderId=$FOLDER_ID" \
  --data-urlencode "name=my-slide.svs" \
  | jq -r '._id')
```

### One request, small files

If the file fits comfortably in one request, send the bytes as the request body
and the upload metadata in the query string:

```bash
export FILE_SIZE=$(stat -c%s my-slide.svs)
curl -s -X POST \
  "$DSA_URL/file?parentType=item&parentId=$ITEM_ID&name=my-slide.svs&size=$FILE_SIZE&mimeType=image%2Fvnd.slide" \
  -H "Girder-Token: $DSA_TOKEN" \
  -H "Content-Type: application/octet-stream" \
  --data-binary @my-slide.svs \
  | jq '{_id, name, size, sha512}'
```

The response is the final file record. The `size` must equal the number of
bytes actually sent.

### Multiple chunks, large files

For large files, initialize an upload with an empty body, then send chunks.
Girder's default minimum chunk size is 5 MiB (`core.upload_minimum_chunk_size`);
the final chunk may be smaller. `girder-client` uses 64 MiB chunks.

```bash
export UPLOAD_ID=$(curl -s -X POST \
  "$DSA_URL/file?parentType=item&parentId=$ITEM_ID&name=my-slide.svs&size=$FILE_SIZE&mimeType=image%2Fvnd.slide" \
  -H "Girder-Token: $DSA_TOKEN" \
  -H "Content-Length: 0" | jq -r '._id')

split -b 64m -d my-slide.svs chunk-
offset=0
for chunk in chunk-*; do
  curl -s -X POST \
    "$DSA_URL/file/chunk?uploadId=$UPLOAD_ID&offset=$offset" \
    -H "Girder-Token: $DSA_TOKEN" \
    -H "Content-Type: application/octet-stream" \
    --data-binary @"$chunk" > /dev/null
  offset=$((offset + $(stat -c%s "$chunk")))
done
```

The chunk response is an upload record until the last byte arrives, then it is
the final file record. Do not send a chunk smaller than the configured minimum
unless it is the last one; the server rejects it with
`Chunk is smaller than the minimum size.`

### Checksum expectations

DSA does not accept a client-supplied checksum in the upload call. It computes
SHA-512 while the file is written and stores the result in the file document:

```bash
export FILE_ID="<file id from the upload response>"
LOCAL_SHA=$(sha512sum my-slide.svs | awk '{print $1}')
SERVER_SHA=$(curl -s -H "Girder-Token: $DSA_TOKEN" \
  "$DSA_URL/file/$FILE_ID" | jq -r '.sha512')
test "$LOCAL_SHA" = "$SERVER_SHA" && echo "checksum matches"
```

Because the check happens after the upload, compare the two values before you
delete the local copy or start a long analysis. SHA-256 is available only when
the optional `hashsum_download` plugin is enabled; do not assume it exists.

## Read and write metadata

There is no `GET /item/<id>/metadata` route in DSA 5; reading the item returns
its metadata in the `meta` field.

```bash
curl -s -H "Girder-Token: $DSA_TOKEN" "$DSA_URL/item/$ITEM_ID" | jq '.meta'
```

`PUT /item/<id>/metadata` **merges** the supplied keys. It does not replace the
whole metadata object:

```bash
curl -s -X PUT -H "Girder-Token: $DSA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"Organ": "Prostate", "Stain": "H&E", "Case ID": "TEST-001"}' \
  "$DSA_URL/item/$ITEM_ID/metadata" | jq '.meta'

curl -s -X PUT -H "Girder-Token: $DSA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"Scanner": "Synthetic"}' \
  "$DSA_URL/item/$ITEM_ID/metadata" | jq '.meta'
```

Delete specific keys with `DELETE` and a JSON array of field names:

```bash
curl -s -X DELETE -H "Girder-Token: $DSA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '["Case ID"]' \
  "$DSA_URL/item/$ITEM_ID/metadata" | jq '.meta'
```

Metadata keys and values must be JSON-serializable. The simple metadata editor
in the web UI enforces the same rules; see
[Edit metadata](../tutorials/edit-metadata.md).

## Download a file or a tile

### Whole file

```bash
curl -s -H "Girder-Token: $DSA_TOKEN" \
  -o my-slide.svs \
  "$DSA_URL/file/$FILE_ID/download"
```

The route supports HTTP `Range` requests for resumable or partial downloads:

```bash
curl -s -H "Girder-Token: $DSA_TOKEN" \
  -H "Range: bytes=0-1023" \
  -o first-1k.bin \
  "$DSA_URL/file/$FILE_ID/download"
```

### Tile

Read the tile metadata first. It tells you the number of levels and the tile
size:

```bash
curl -s -H "Girder-Token: $DSA_TOKEN" \
  "$DSA_URL/item/$ITEM_ID/tiles" \
  | jq '{levels, tileWidth, tileHeight, sizeX, sizeY, frames}'
```

Then request a tile by level, column, and row. The server returns JPEG bytes:

```bash
curl -s -H "Girder-Token: $DSA_TOKEN" \
  -o tile-0-0-0.jpg \
  "$DSA_URL/item/$ITEM_ID/tiles/zxy/0/0/0"
```

For a multi-frame image, use the frame route and include the frame index:

```bash
curl -s -H "Girder-Token: $DSA_TOKEN" \
  -o frame-0.jpg \
  "$DSA_URL/item/$ITEM_ID/tiles/fzxy/0/0/0/0"
```

Private items need the token on every tile request. Tile responses are cached
by the server, so repeated requests are cheap; do not add cache-busting
parameters.

## List and create annotations

HistomicsUI stores annotations through the `annotation` resource. List them for
an item with:

```bash
curl -s -H "Girder-Token: $DSA_TOKEN" \
  "$DSA_URL/annotation/item/$ITEM_ID" | jq 'length'
```

Create an annotation by posting a JSON object (or a list of objects) with an
`annotation` key. The minimum useful shape is a name and an `elements` array.
The element schema is available at `GET /annotation/schema`:

```bash
cat > annotation.json <<'JSON'
[
  {
    "annotation": {
      "name": "API cookbook example",
      "description": "Created with the REST API",
      "elements": [
        {
          "type": "rectangle",
          "center": [512, 512, 0],
          "width": 256,
          "height": 256,
          "rotation": 0,
          "lineColor": "#00ff00",
          "lineWidth": 2,
          "fillColor": "#00ff0033",
          "label": {"value": "Tumor"}
        }
      ]
    }
  }
]
JSON

curl -s -X POST -H "Girder-Token: $DSA_TOKEN" \
  -H "Content-Type: application/json" \
  --data-binary @annotation.json \
  "$DSA_URL/annotation/item/$ITEM_ID"
```

The response is the number of annotations created (`1` above), not the new
annotation record. Re-read the list to get the annotation ids and element ids.

Coordinates are in base-layer pixels, with the origin at the upper left. A
rectangle is defined by `center`, `width`, and `height`; `rotation` is in
radians. `fillColor` accepts `#rgb`, `#rrggbb`, and eight-digit variants.
Creating annotations requires write access to the item; a user with read-only
access receives `403`.

## Submit an analysis job

Slicer CLI Web exposes one REST resource per installed CLI. List the tasks and
their ids:

```bash
curl -s -H "Girder-Token: $DSA_TOKEN" \
  "$DSA_URL/slicer_cli_web/cli" \
  | jq -r '.[] | [._id, .name, .image] | @tsv'
```

Fetch the task's Slicer Execution Model XML to see its inputs, outputs, and
defaults:

```bash
export CLI_ID="<id of the task you want>"
curl -s -H "Girder-Token: $DSA_TOKEN" \
  "$DSA_URL/slicer_cli_web/cli/$CLI_ID/xml"
```

Submit the job with `POST /slicer_cli_web/cli/<cli id>/run`. Image and file
inputs take **Girder file ids**, not item ids. Output parameters need a
`<name>_folder` value with the destination folder id and a `<name>` value with
the output filename:

```bash
export JOB_ID=$(curl -s -X POST -H "Girder-Token: $DSA_TOKEN" \
  "$DSA_URL/slicer_cli_web/cli/$CLI_ID/run" \
  --data-urlencode "slide_path=$FILE_ID" \
  --data-urlencode "sample_fraction=0.1" \
  --data-urlencode "magnification=1.25" \
  --data-urlencode "tissue_seg_mag=1.25" \
  --data-urlencode "min_coverage=0.1" \
  --data-urlencode "sample_approximate_total=-1" \
  --data-urlencode "tile_grouping=256" \
  --data-urlencode "scheduler=" \
  --data-urlencode "outputAnnotationFile_folder=$FOLDER_ID" \
  --data-urlencode "outputAnnotationFile=background.anot" \
  | jq -r '._id')

echo "job $JOB_ID"
```

The example uses `BackgroundIntensity` from
`dsarchive/histomicstk:latest`. Its XML has five indexed parameters; send all of
them explicitly, plus the two output values. Omitting an indexed parameter is
not filled in from the XML default by the REST route and produces a server
error. The folder parameter suffix is `_folder`, lowercase.

Poll the job until it reaches a terminal status:

```bash
while :; do
  JOB=$(curl -s -H "Girder-Token: $DSA_TOKEN" "$DSA_URL/job/$JOB_ID")
  STATUS=$(echo "$JOB" | jq -r '.status')
  case "$STATUS" in
    0|1|2) sleep 2 ;;
    3) echo "succeeded"; echo "$JOB" | jq -r '.log[-1]'; break ;;
    4|5) echo "failed or canceled"; echo "$JOB" | jq -r '.log[-1]'; break ;;
    *) echo "unknown status $STATUS"; break ;;
  esac
done
```

| Status | Meaning |
| --- | --- |
| `0` | Inactive, not queued yet |
| `1` | Queued |
| `2` | Running |
| `3` | Succeeded |
| `4` | Failed |
| `5` | Canceled |

Results are attached to the source item according to the output names. An
output whose name ends in `AnnotationFile` becomes an annotation on the image;
one ending in `ItemMetadata` becomes item metadata. HistomicsUI deletes the
staging output file after ingesting it, so check the annotations or metadata
rather than looking for the `.anot` file in the folder:

```bash
curl -s -H "Girder-Token: $DSA_TOKEN" \
  "$DSA_URL/annotation/item/$ITEM_ID" \
  | jq -r '.[] | .annotation.name'
```

A job can be queued while no worker is available. If it stays at status `1`,
ask an administrator to check the worker; see
[Run an analysis](../tutorials/run-an-analysis.md).

## Common error responses

API errors are usually JSON with `message` and `type`. Route errors are the
exception: a `404` for an unregistered route returns an HTML body. Example JSON
error:

```json
{"message": "Read access denied for folder 6ae89b2ead9f85a8521df8f6 (user None).", "type": "access"}
```

| Status | When it happens | What to do |
| --- | --- | --- |
| `400` | A parameter is missing or invalid, an id does not resolve, a path lookup fails, or a chunk is too small. | Read `message`; fix the request. A missing object id is **not** a permission problem. |
| `401` | No token, an expired token, or a token that no longer resolves. The message names the user as `None`. | Sign in again or exchange the API key. |
| `403` | The token is valid but the user lacks read or write access to the resource. | Ask the owner or administrator for access; retrying will not help. |
| `404` | The URL is not a registered route. The body is HTML, not JSON. | Check the `/api/v1` prefix and the route path. |
| `500` | An unexpected server error. The body includes a `uid`. | Capture the `uid` and server log; do not retry blindly. |

How to tell permission from a missing resource on these routes:

- A `401` or `403` with `"type": "access"` means the request reached an
  access-controlled resource. A `403` is an authenticated user without
  permission; a `401` means the identity was not established.
- A `400` with `Invalid item id` (or `Invalid folder id`, `Invalid file id`,
  `Collection not found`) means the id or path did not resolve. A malformed id
  returns `Invalid ObjectId: <value>` instead. On a Girder route, a nonexistent
  object id is a `400`, not a `404`.
- A `404` with `Nothing matches the given URI` means the route itself is wrong,
  not that the object is private. This often means the base URL is missing
  `/api/v1` or a reverse proxy is rewriting the path.

If a load balancer or reverse proxy in front of DSA returns its own `404`, the
JSON body will not look like Girder's. Check the proxy configuration before
changing client credentials.

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

    The read-only recipes — collection/folder/item listing, path lookup, item
    metadata read, tile metadata and tile download, and annotation listing —
    were also checked against the public demo at
    `https://demo.kitware.com/histomicstk/api/v1`, which reported Girder
    `3.2.18.dev2+g339bcdfe6`. The demo is older than a current DSA 5 install;
    use it for read-only examples only.

    Write recipes (upload, metadata updates, annotation creation, analysis)
    were tested on the local install with an administrator account. The
    `403` case was tested with a separate non-admin account. Not tested:
    two-factor login, non-admin write permissions, S3 or other external
    assetstores, the `hashsum_download` plugin, and third-party analysis images
    other than `dsarchive/histomicstk:latest`.

## Route sources

The routes above are not guesses. They come from the running server and these
source files:

- Sign-in: `girder/api/v1/user.py` (`GET user/authentication`, `GET user/me`).
- API keys: `girder/api/v1/api_key.py` (`POST api_key`,
  `POST api_key/token`).
- Collections, folders, items, uploads, metadata: `girder/api/v1/collection.py`,
  `folder.py`, `item.py`, and `file.py` at Girder `70eb94dcd`.
- Path lookup: `girder/api/v1/resource.py` (`GET resource/lookup`).
- Tiles: `large_image/girder/girder_large_image/rest/tiles.py` at
  `09c6d78019c0381402cd814a0060cf4af1bb569e`.
- Annotations: `large_image/girder_annotation/girder_large_image_annotation/rest/annotation.py`
  at the same commit.
- Analysis tasks: the generated `POST /slicer_cli_web/cli/<id>/run` route in
  `girder/plugins/slicer_cli_web/slicer_cli_web/rest_slicer_cli.py`.

## Next

- [Python client](python-client.md): the same workflow with `girder-client`.
- [Connect to a server](../tutorials/connect.md): creating an account and an
  API key in the browser.
- [Run an analysis](../tutorials/run-an-analysis.md): the HistomicsUI version
  of the analysis workflow.
