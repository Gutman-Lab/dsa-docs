# Troubleshooting and FAQ

This page is organized by symptom. Find the section that matches what you see,
then follow **Likely cause** and **Fix**. Each entry ends with a page or
upstream source where the deeper detail lives.

## Install and startup {#install-and-startup}

These commands run from the deployment directory: `devops/dsa` for the Girder
3 reference stack, or `devops/ver5` for the Girder 5 stack. See
[Install on one machine](get-started/install.md) for the full walkthrough.

### Compose exits with "Set the DSA_USER before starting" {#dsa-user-missing}

- **Symptom:** `docker compose up` exits immediately. The Girder or worker log
  says `Set the DSA_USER before starting` or `DSA_USER must be in UID:GID
  format.`
- **Likely cause:** `DSA_USER` is unset, not in `UID:GID` form, or set to root
  (`0:0`). The startup scripts reject all three.
- **Fix:** start with your own account:
  `DSA_USER=$(id -u):$(id -g) docker compose up -d`. In `devops/ver5`,
  `./start.sh` does this for you.
- **Where to look next:** [Install on one machine](get-started/install.md#3-start-the-stack),
  or the upstream
  [`start_girder.sh`](https://github.com/DigitalSlideArchive/digital_slide_archive/blob/master/devops/dsa/start_girder.sh).

### Port 8080 is already allocated {#port-conflict}

- **Symptom:** Docker reports
  `Bind for 0.0.0.0:8080 failed: port is already allocated`.
- **Likely cause:** Another process, often a second DSA stack, already owns port
  8080.
- **Fix:** stop the other stack with `docker compose down`, or start this one on
  another host port:
  `DSA_PORT=8081 DSA_USER=$(id -u):$(id -g) docker compose up -d`. Then open
  <http://localhost:8081>.
- **Where to look next:** [Install settings you are likely to change](get-started/install.md#install-settings-you-are-likely-to-change).

### "permission denied while trying to connect to the Docker daemon socket" {#docker-socket-permission}

- **Symptom:** Compose or a container cannot reach `/var/run/docker.sock`.
- **Likely cause:** Your user is not in the `docker` group, or Docker uses a
  different socket path (for example, rootless Docker).
- **Fix (host command):** add your user to the group, then log out and back in:
  `sudo usermod -aG docker "$USER"`. Confirm with `docker info`. Rootless
  Docker is not covered by the reference compose file.
- **Where to look next:** [Install prerequisites](get-started/install.md#prerequisites).

### Containers start but Girder never becomes ready {#girder-never-ready}

- **Symptom:** `docker compose ps` shows `girder` restarting or unhealthy, and
  `curl --silent http://localhost:8080/api/v1/system/version` never returns a
  `release` field.
- **Likely cause:** A dependency such as MongoDB, RabbitMQ, or Redis failed to
  start, or provisioning failed. The first start can take a minute or two.
- **Fix:** run `docker compose ps`, then
  `docker compose logs girder mongodb`. On `devops/ver5`, also check
  `docker compose logs redis rabbitmq`. Fix the first dependency that reports an
  error, then restart with `docker compose restart girder`.
- **Where to look next:** [Install troubleshooting](get-started/install.md#troubleshooting)
  and [Logs and status](#logs-and-status).

### GPU analysis fails or runs only on CPU {#missing-gpu}

- **Symptom:** A GPU-oriented task fails with a Docker device error, or runs far
  slower than expected.
- **Likely cause:** The reference compose files do not request GPU devices. The
  host needs the NVIDIA container toolkit, the container needs a GPU device
  reservation, and the task image itself must support GPU execution.
- **Fix:** confirm the host exposes a GPU runtime with `docker info` (host
  command). Add a `deploy.resources.reservations.devices` entry or the
  equivalent `--gpus` setting in a `docker-compose.override.yml`. If you cannot
  provide a GPU, use a CPU-capable task.
- **Where to look next:** [Run an analysis](tutorials/run-an-analysis.md) and
  the upstream
  [GPU task discussion](https://github.com/DigitalSlideArchive/digital_slide_archive/issues/186).

### Default admin login does not work {#first-admin-login}

- **Symptom:** `admin` / `password` is rejected on a new installation.
- **Likely cause:** Provisioning creates that account **only when the database
  has no administrator**. An existing database keeps its old password. A
  different `DSA_PROVISION_YAML` can also define different credentials.
- **Fix:** use the credentials for the existing instance. If this really is a
  fresh stack, check the provisioning output with
  `docker compose logs girder | grep -i provision`. Change the default password
  as soon as you can sign in.
- **Where to look next:** [Upload and view your first slide](get-started/first-slide.md#1-sign-in)
  and the upstream
  [`provision.yaml`](https://github.com/DigitalSlideArchive/digital_slide_archive/blob/master/devops/dsa/provision.yaml).

### Assetstore, database, or log files are owned by root {#root-owned-files}

- **Symptom:** Girder cannot write files, or `assetstore/`, `db/`, and `logs/`
  are owned by `root`.
- **Likely cause:** The stack was started without `DSA_USER`, or as root.
- **Fix:** from the deployment directory, repair ownership with
  `sudo chown -R $(id -u):$(id -g) assetstore db logs`, then restart with
  `DSA_USER` set.
- **Where to look next:** [Install troubleshooting](get-started/install.md#troubleshooting).

## Authentication and sessions {#authentication}

For the sign-in walkthrough, see [Connect to a DSA server](tutorials/connect.md).

### "Login failed." with the correct password {#login-failed}

- **Symptom:** The login dialog returns `Login failed.`
- **Likely cause:** The login name or email is wrong, the account does not
  exist, or the password changed. Girder also returns distinct errors when the
  account is disabled, needs email verification, or needs administrator
  approval.
- **Fix:** confirm the exact login name or email with the account owner. An
  administrator can check the account status in the Admin console. Look for
  `Account is disabled.`, `Email verification required.`, or
  `Account approval required.` in the response or server log.
- **Where to look next:** [Connect troubleshooting](tutorials/connect.md#troubleshooting)
  and [Logs and status](#logs-and-status).

### Two-factor code is rejected {#two-factor-rejected}

- **Symptom:** Login fails with `One-time password validation failed: Token did
  not match` or `Token has already been used, please wait for another.`
- **Likely cause:** The authenticator clock is skewed, the code was already
  used, or the code belongs to another account.
- **Fix:** enable automatic time sync on the device, wait for the next code,
  and enter the current six-digit value in **Two-factor code**. Do not reuse a
  code. If the device is lost, an administrator can remove the second factor
  after verifying your identity, with `DELETE /api/v1/user/{id}/otp`. You can
  then sign in and enroll a new device; do not create a duplicate account.
- **Where to look next:** [Connect: sign in](tutorials/connect.md#2-sign-in) and
  the upstream
  [Girder user model](https://github.com/girder/girder/blob/3.x-maintenance/girder/models/user.py).

### API key request returns "Invalid API key." {#invalid-api-key}

- **Symptom:** `POST /api/v1/api_key/token` returns `Invalid API key.`
- **Likely cause:** The key was copied incorrectly, deleted, or deactivated.
- **Fix:** create a new key under **My account** → **API keys** and copy the
  whole value. Keys can also have a maximum token duration.
- **Where to look next:** [Connect from a script](tutorials/connect.md#connect-from-a-script-optional).

### "API key functionality is disabled on this instance." {#api-keys-disabled}

- **Symptom:** The **API keys** tab or create button is missing, or the token
  request returns `API key functionality is disabled on this instance.`
- **Likely cause:** An administrator turned off `core.api_keys`.
- **Fix:** an administrator can enable **Enable API keys** in the Admin console
  under **System configuration**. Otherwise, authenticate with your username
  and password.
- **Where to look next:** [Connect: API keys may be disabled](tutorials/connect.md#connect-from-a-script-optional).

### You are signed out sooner than expected {#session-expiry}

- **Symptom:** The session ends after minutes or hours instead of lasting.
- **Likely cause:** The instance sets
  `histomicsui.login_session_expiry_minutes`, which shortens the token lifetime.
  Clearing cookies or using a private window also ends the session.
- **Fix:** sign in again. An administrator can change or clear that HistomicsUI
  setting in the plugin settings. When it is unset, Girder uses
  `core.cookie_lifetime`, whose default is 180 days.
- **Where to look next:** [Connect: confirm that you are connected](tutorials/connect.md#3-confirm-that-you-are-connected).

### An administrator-created account cannot sign in {#admin-created-account}

- **Symptom:** A user created in the Admin console cannot log in.
- **Likely cause:** The user is typing the email where the login name is
  required (or the reverse), the account is disabled, or the instance requires
  email verification or administrator approval.
- **Fix:** confirm the exact login and email, check the account status, and
  reset the password if needed. The user must complete email verification or
  approval before the first successful login.
- **Where to look next:** [Connect: if you do not have an account](tutorials/connect.md#if-you-do-not-have-an-account).

## Viewing and tiles {#viewing}

The viewer reads an image through `large_image`. If the item page has no
**Open in HistomicsUI** button, treat it as a format or tile-source problem
first, not a browser problem.

### Blank viewer or a spinner that never finishes {#blank-viewer}

- **Symptom:** HistomicsUI opens but the image area stays blank or keeps
  loading.
- **Likely cause:** Tile requests are failing, the file is not a readable large
  image, the assetstore is unavailable, or the browser is holding stale assets
  after an upgrade.
- **Fix:** hard-refresh the tab (Ctrl+Shift+R or Cmd+Shift+R). Open the item
  page and confirm **Open in HistomicsUI** is present. In the browser developer
  tools, check whether tile requests return 200 rather than 403 or 500. Then
  check the server log for tile-source errors.
- **Where to look next:** [Logs and status](#logs-and-status), [Unsupported
  formats](#unsupported-format), and the
  [`large_image` format table](https://github.com/girder/large_image/blob/master/docs/formats.rst).

### Tiles are missing, checkered, or return 404 {#tiles-missing}

- **Symptom:** The viewer loads partially, some zoom levels are blank, or tile
  requests return 404.
- **Likely cause:** The underlying file was moved or deleted, the assetstore
  path is not available inside the container, anonymous access is restricted,
  or a reverse proxy is not forwarding tile routes.
- **Fix:** sign in and retry. Confirm the file still exists in its item. If you
  operate the server, check `docker compose logs girder` and the Girder error
  log. `devops/dsa` sets `restrict_downloads = 100000`, which limits anonymous
  downloads to small files.
- **Where to look next:** [Install troubleshooting](get-started/install.md#troubleshooting)
  and [Logs and status](#logs-and-status).

### Pan and zoom are slow {#slow-viewer}

- **Symptom:** The first tile load is slow, or panning and zooming stutter.
- **Likely cause:** The file is not stored as a pyramidal/tiled image, the tile
  cache is cold or unavailable, the host has too little memory, or a non-tiled
  format is being decoded on every request.
- **Fix:** convert the slide to a pyramidal TIFF or OME-TIFF with
  `large_image_converter`, then upload the converted file. Give the host more
  memory, and check that the cache backend is healthy: `devops/dsa` uses
  memcached, while `devops/ver5` uses Redis.
- **Where to look next:** [`large_image` image conversion](https://github.com/girder/large_image/blob/master/docs/image_conversion.rst)
  and [Install prerequisites](get-started/install.md#prerequisites).

### The item is not recognized as a large image {#unsupported-format}

- **Symptom:** There is no **Open in HistomicsUI** button, or the server reports
  `No available tilesource` / an unsupported image.
- **Likely cause:** No installed `large_image` tile source can read that format,
  or the file is corrupt or misnamed.
- **Fix:** check the format against the `large_image` format table. Convert the
  file to a pyramidal TIFF or OME-TIFF, then upload it again. Check
  `docker compose logs girder` for the tile-source error.
- **Where to look next:** [`large_image` supported formats](https://github.com/girder/large_image/blob/master/docs/formats.rst)
  and the upstream
  [`No available tilesource` issue](https://github.com/girder/large_image/issues/446).

### The viewer still looks wrong after an upgrade {#browser-cache}

- **Symptom:** Menus or controls are missing after the server was updated, but
  another browser works.
- **Likely cause:** The tab is using cached JavaScript, CSS, or HTML.
- **Fix:** hard-refresh the page, or open it in a private window. HistomicsUI
  appends a build timestamp to its main scripts and styles, but an already-open
  tab can keep the old page.
- **Where to look next:** the upstream
  [HistomicsUI cache handling](https://github.com/DigitalSlideArchive/HistomicsUI/blob/master/histomicsui/__init__.py).

## Upload {#upload}

DSA stores data as **collection → folder → item → file**. Uploading a file into
a folder creates an item; uploading into an item attaches another file to that
item.

### Upload fails with "file too large" or HTTP 413 {#file-too-large}

- **Symptom:** The upload dialog stops with a size error, or a proxy returns 413.
- **Likely cause:** A reverse proxy body limit, an optional quota plugin, or a
  full assetstore. The reference `devops/dsa` configuration sets
  `server.max_request_body_size = 1073741824` (1 GiB) and Girder uploads in
  chunks, so a single monolithic request is usually not the limit.
- **Fix:** raise the proxy limit if you use one, confirm free disk space with
  `df -h`, and check the Girder error log. Do not raise `DSA_WORKER_CONCURRENCY`
  to work around an upload problem.
- **Where to look next:** [Disk full](#disk-full) and [Install settings](get-started/install.md#install-settings-you-are-likely-to-change).

### Upload is interrupted and offers "Click to resume upload" {#interrupted-upload}

- **Symptom:** The dialog shows an error with **Click to resume upload** or
  **Click to restart upload**.
- **Likely cause:** A network or proxy timeout, the browser sleeping, or the
  server restarting mid-upload.
- **Fix:** leave the dialog open and select **Click to resume upload**. If the
  server lost the upload record, use **Click to restart upload**. Closing the
  dialog aborts the partial upload, so you must start over.
- **Where to look next:** the upstream
  [Girder upload widget](https://github.com/girder/girder/blob/3.x-maintenance/girder/web_client/src/views/widgets/UploadWidget.js).

### The file went into the wrong folder or item {#wrong-folder}

- **Symptom:** The slide appears in the wrong place, or an item now has an extra
  file.
- **Likely cause:** The upload target was the folder or item that was open at
  the time.
- **Fix:** use the folder action menu to move the item to the correct folder. If
  the file was attached to an existing item instead of creating its own item,
  re-upload it into the intended folder.
- **Where to look next:** [Create a folder](tutorials/create-a-folder.md) and
  [Copy an item](tutorials/copy-an-item.md).

### Duplicate items appear after a retry {#duplicate-items}

- **Symptom:** The same slide appears twice, often as `slide.svs` and
  `slide (1).svs`.
- **Likely cause:** The file was uploaded twice, or an interrupted upload was
  restarted after the first attempt actually completed. Girder keeps sibling
  names unique by appending `(1)`, `(2)`, and so on; it does not overwrite.
- **Fix:** compare the item sizes and metadata, then delete the extra item. Do
  not retry an upload that already finished. Use
  [Copy an item](tutorials/copy-an-item.md) when you intentionally want a
  duplicate.
- **Where to look next:** the upstream
  [Girder item name validation](https://github.com/girder/girder/blob/3.x-maintenance/girder/models/item.py).

### The assetstore is full or read-only {#assetstore-full}

- **Symptom:** Uploads fail while the UI still responds, or the log reports a
  write error.
- **Likely cause:** The disk or volume holding `assetstore/` is full, the mount
  disappeared, or files are not writable by `DSA_USER`.
- **Fix:** check `df -h` and `du -sh assetstore db logs`, confirm the assetstore
  path exists on the host, and repair ownership with
  `sudo chown -R $(id -u):$(id -g) assetstore db logs`. Back up before moving
  an assetstore to a larger volume.
- **Where to look next:** [Disk full](#disk-full) and [Logs and status](#logs-and-status).

## Permissions and sharing {#permissions}

Collections and folders carry access control. Items inherit access from their
folder; items do not have their own ACL. Annotations are the exception: each
annotation has its own ACL. See [Share a collection or folder](tutorials/share-a-collection.md)
for the task walkthrough, [Permissions and access control](user-guide/permissions.md)
for the model, [Create a collection](tutorials/create-a-collection.md) for the
private-by-default behavior, and [Annotation basics](user-guide/annotations.md)
for annotation access.

### You cannot see a collection {#cannot-see-collection}

- **Symptom:** A colleague sent a link, but the collection is missing or returns
  access denied.
- **Likely cause:** Your account has no read access, you are signed in as a
  different user, or the collection is private.
- **Fix:** ask the owner to check the collection's **Access control** and grant
  your user or group **Can view**. Confirm you are signed in as the expected
  account and check **My folders** to verify the session.
- **Where to look next:** [Create a collection](tutorials/create-a-collection.md)
  and [Connect: find your workspace](tutorials/connect.md#4-find-your-workspace).

### You can view but not edit or upload {#cannot-edit}

- **Symptom:** The folder is visible, but upload, edit, or delete controls are
  missing.
- **Likely cause:** Your role is **Can view** (READ), not **Can edit** (WRITE)
  or owner. Access is inherited from the collection or a parent folder.
- **Fix:** ask an owner to grant **Can edit** on the collection or folder. If
  the share was applied only to one folder, check whether the item is in a
  subfolder that received different permissions.
- **Where to look next:** [Create a collection](tutorials/create-a-collection.md)
  and [Create a folder](tutorials/create-a-folder.md).

### You cannot create annotations {#cannot-annotate}

- **Symptom:** The **New** button is missing, or the API returns
  `Write access and annotation creation access were denied for the item.`
- **Likely cause:** Creating annotations requires write access to the item's
  folder, or the folder's **Create annotations** access flag.
- **Fix:** ask an owner to grant **Can edit** on the folder, or enable the
  **Create annotations** flag. Viewing an image does not by itself allow
  drawing.
- **Where to look next:** [Annotation basics](user-guide/annotations.md) and
  [`large_image` annotation access](https://github.com/girder/large_image/blob/master/docs/girder_annotation_access.rst).

### Annotations are invisible after sharing a folder {#annotations-after-sharing}

- **Symptom:** A user can see the image but not annotations that existed before
  the share.
- **Likely cause:** An annotation copies the folder's ACL **when it is
  created**. Later changes to the folder ACL, and moving an item, do not update
  existing annotations.
- **Fix:** from the folder action menu, open **Annotation access control** and
  add the user or group. For a single annotation, use its access dialog. Saving
  replaces the annotation ACL rather than merging it; choose the subfolder
  option deliberately.
- **Where to look next:** [`large_image` annotation access control](https://github.com/girder/large_image/blob/master/docs/girder_annotation_access.rst)
  and the upstream
  [folder-wide annotation access request](https://github.com/DigitalSlideArchive/HistomicsUI/issues/27).

### A public image is still hidden by its collection {#public-image-private-collection}

- **Symptom:** A slide or folder is marked public, but anonymous users still
  cannot see it.
- **Likely cause:** Items inherit access from their folder and collection. The
  surrounding collection or an ancestor folder is still private, or the link
  points at a private parent.
- **Fix:** make the containing collection or folder public, or share it with the
  intended group. Do not rely on a public flag on a single item.
- **Where to look next:** the upstream
  [public image in a private collection discussion](https://github.com/DigitalSlideArchive/HistomicsUI/issues/55).

## Annotation {#annotation}

For the annotation model, panels, shortcuts, and save behavior, see
[Annotation basics](user-guide/annotations.md) and
[Annotate a slide](tutorials/annotate-a-slide.md).

### The Draw panel is missing or nothing can be drawn {#cannot-draw}

- **Symptom:** The **Draw** panel is absent, or drawing tools do nothing.
- **Likely cause:** No annotation is selected, the **New** button is hidden by
  permissions, or the panel layout hides the Draw panel.
- **Fix:** create or select an annotation first. Confirm you have write or
  **Create annotations** access on the folder. If the panel is hidden, reopen it
  from the viewer controls or check the folder's panel layout configuration.
- **Where to look next:** [Annotation basics: the two panels you need](user-guide/annotations.md#the-two-panels-you-need).

### A style group is missing or the wrong one is selected {#missing-style-group}

- **Symptom:** The Draw panel does not list the expected style group, or the
  group changes when you select an annotation.
- **Likely cause:** Style groups are configured per folder in
  `.histomicsui_config.yaml`. An annotation can also restrict its groups with
  `allowed_groups`; groups named there are created from the default style the
  first time they are needed.
- **Fix:** check the folder's configuration and the annotation's
  `allowed_groups` metadata. Use the Draw panel's gear button to edit groups.
  Remember that group hotkeys only apply where the config file is active.
- **Where to look next:** [Annotation style groups](user-guide/annotation-groups.md)
  and the upstream
  [`config_options.rst`](https://github.com/DigitalSlideArchive/HistomicsUI/blob/master/docs/config_options.rst).

### Autosave fails or the annotation spinner never stops {#annotation-autosave}

- **Symptom:** Edits are not persisted, the spinner stays beside the
  **Annotations** panel, or the browser reports a failed request.
- **Likely cause:** The session expired, write access was removed, the server is
  unavailable, or a validation error rejected the annotation.
- **Fix:** keep the tab open and check the browser network response for 401,
  403, or 500. Sign in again if the session expired. Check the Girder error log
  for validation errors. If the page is closed before a retry succeeds, unsaved
  edits are lost.
- **Where to look next:** [Annotation basics: annotation documents](user-guide/annotations.md#annotation-documents)
  and the upstream
  [annotation save retry logic](https://github.com/DigitalSlideArchive/HistomicsUI/blob/master/histomicsui/web_client/panels/AnnotationSelector.js).

### Annotation export or download does not produce what you need {#annotation-export}

- **Symptom:** The downloaded annotation is JSON, but a downstream tool wants
  GeoJSON, or the download control is missing.
- **Likely cause:** The **Annotations** panel downloads the stored annotation
  document as JSON. GeoJSON is a separate representation.
- **Fix:** use the panel's download control for the JSON document, or request
  `GET /api/v1/annotation/{id}/geojson` for GeoJSON. You need read access to the
  annotation.
- **Where to look next:** [Annotation basics: coordinate lists](user-guide/annotations.md#coordinate-lists).

### Annotations from an analysis job never appear {#job-annotations-missing}

- **Symptom:** The job succeeds, but the **Annotations** panel does not show the
  result.
- **Likely cause:** The output name, reference, or ingestion step is wrong. See
  [Job succeeds but produces no output](#job-no-output).
- **Fix:** inspect the job outputs and the task XML, then check the server log
  for annotation-ingestion errors.
- **Where to look next:** [Run an analysis](tutorials/run-an-analysis.md#5-find-the-result).

## Analysis jobs {#analysis-jobs}

Analysis tasks are containerized Slicer CLI Web jobs. The Girder worker starts
sibling Docker containers, so the worker needs access to the Docker socket. See
[Run an analysis](tutorials/run-an-analysis.md) for the task walkthrough.

### The Analyses menu is missing {#analyses-menu-missing}

- **Symptom:** There is no **Analyses** menu in the viewer.
- **Likely cause:** No Slicer CLI Web task is registered, the image is not open,
  or the plugin is disabled.
- **Fix:** an administrator must register at least one Docker image, for example
  `dsarchive/histomicstk:latest`, in the Slicer CLI Web settings. Open the image
  item itself, not a folder. Test the image with
  `docker run --rm dsarchive/histomicstk:latest --list_cli`.
- **Where to look next:** [Run an analysis: before you start](tutorials/run-an-analysis.md#before-you-start)
  and [For task authors](tutorials/run-an-analysis.md#for-task-authors).

### The job stays queued forever {#job-queued-forever}

- **Symptom:** The job status stays **Queued** and never changes to **Running**.
- **Likely cause:** The worker is stopped or unhealthy, RabbitMQ is unavailable,
  no worker is consuming the queue, or the queue is backed up.
- **Fix:** run `docker compose ps` and confirm `worker` and `rabbitmq` are
  healthy. Inspect `docker compose logs worker` and
  `docker compose logs rabbitmq`, then restart the worker with
  `docker compose restart worker`. The worker health check uses
  `celery inspect ping`.
- **Where to look next:** [Run an analysis troubleshooting](tutorials/run-an-analysis.md#troubleshooting)
  and [Logs and status](#logs-and-status).

### The job fails or its container exits immediately {#job-failed}

- **Symptom:** The job status becomes **Error**, or the task container exits
  before producing output.
- **Likely cause:** The task image is missing, the worker cannot reach the
  Docker socket, the container ran out of memory, a GPU is required, or the
  task's XML does not match its command line.
- **Fix:** open the job in the jobs panel and read its log. Run
  `docker compose logs worker`, then `docker ps -a` to find the exited task
  container and `docker logs <container>` for its output. Test the image with
  `--list_cli` and `<algorithm> --xml`.
- **Where to look next:** [For task authors](tutorials/run-an-analysis.md#for-task-authors)
  and the upstream
  [job submission discussion](https://github.com/DigitalSlideArchive/digital_slide_archive/issues/132).

### The job succeeds but produces no output {#job-no-output}

- **Symptom:** The job status is **Success**, but no annotation or metadata
  appears on the item.
- **Likely cause:** An output name must end in `AnnotationFile` or
  `ItemMetadata` **and** reference the input item or image. If ingestion fails,
  the job can still succeed.
- **Fix:** inspect the job outputs and the task XML. Check the Girder error log
  (`logs/error.log` on `devops/dsa`; `logs/info.log` on `devops/ver5`) for
  `Could not parse annotation file` or
  `Could not create annotation object from data`. Confirm the output is attached
  to the item you are viewing.
- **Where to look next:** [Run an analysis: find the result](tutorials/run-an-analysis.md#5-find-the-result)
  and [Annotation basics: annotations and metadata from jobs](user-guide/annotations.md#annotations-and-metadata-from-jobs).

### The worker is not configured, or an external worker never connects {#worker-not-configured}

- **Symptom:** Jobs stay queued even though the Girder server is healthy, or an
  external worker does not appear to consume work.
- **Likely cause:** The worker service is absent from the compose stack, or an
  external worker cannot reach the broker with the configured
  `CELERY_BROKER_URL`.
- **Fix:** confirm the `worker` service is running with `docker compose ps`.
  Check that the worker and Girder use the same RabbitMQ URL. For a separate
  worker machine, follow the external-worker deployment instead of adding a
  second broker.
- **Where to look next:** the upstream
  [`external-worker` README](https://github.com/DigitalSlideArchive/digital_slide_archive/blob/master/devops/external-worker/README.rst)
  and [Run an analysis](tutorials/run-an-analysis.md).

## Data, disk, and upgrades {#data-admin}

Back up before any upgrade, storage move, or MongoDB version change.

### Back up and restore the Girder database {#database-backup}

- **Symptom:** You need a copy of the database before maintenance, or you need
  to restore one.
- **Likely cause:** Routine operations or recovery.
- **Fix:** from the deployment directory, back up with
  `docker compose exec mongodb /usr/bin/mongodump --db girder --archive --gzip > dsa_girder.dump.gz`.
  Restore with
  `docker compose exec -T mongodb /usr/bin/mongorestore --db girder --archive --gzip < dsa_girder.dump.gz`.
  Add `--drop` to the restore only when you intend to replace the current
  database. Back up `assetstore/` separately; the dump does not contain file
  bytes.
- **Where to look next:** the upstream
  [`devops/dsa` README](https://github.com/DigitalSlideArchive/digital_slide_archive/blob/master/devops/dsa/README.rst#database-backup).

### Disk is full {#disk-full}

- **Symptom:** Uploads, jobs, or Girder itself start failing, and the log
  reports write errors or `No space left on device`.
- **Likely cause:** The database, assetstore, logs, or Docker images consumed
  the volume.
- **Fix:** check `df -h`, `docker system df`, and
  `du -sh assetstore db logs`. Free space by rotating or removing old logs and
  unused images (host command; review before deleting). Do not delete `db/` or
  `assetstore/` to reclaim space without a backup.
- **Where to look next:** [The assetstore is full or read-only](#assetstore-full)
  and [Back up and restore the Girder database](#database-backup).

### An upgrade failed and you need to roll back {#upgrade-rollback}

- **Symptom:** A new image or MongoDB version breaks the instance.
- **Likely cause:** Moving image tags such as `latest`, or upgrading MongoDB
  across more than one major version. MongoDB does not automatically downgrade
  database files.
- **Fix:** restore the database dump, restore the assetstore if it changed, and
  start the previous image digests. Before the next attempt, pin image digests in
  `docker-compose.override.yml` and read the migration guide.
- **Where to look next:** [Migration guide](migration.md) and
  [Database backup](#database-backup).

### MongoDB compatibility version changed {#mongo-compatibility}

- **Symptom:** MongoDB refuses to start after an image change, or the migration
  guide warns about version steps.
- **Likely cause:** The database files were created by a different MongoDB major
  version.
- **Fix:** follow the migration guide one major version at a time. Take a
  database dump first.
- **Where to look next:** [Migration guide: MongoDB version compatibility](migration.md#mongodb-version-compatibility).

## FAQ {#faq}

### Where are these docs published? {#where-are-docs}

This is the consolidated preview at <https://gutman-lab.github.io/dsa-docs/>.
It is separate from the official public deployment while the content is under
review. The source is
[`Gutman-Lab/dsa-docs`](https://github.com/Gutman-Lab/dsa-docs).

### How do I get an account? {#get-an-account}

If the server shows **Register** next to **Log In**, self-registration is open.
If it does not, registration is closed and an administrator must create the
account. See [Connect to a DSA server](tutorials/connect.md#if-you-do-not-have-an-account).

### What is the default administrator password? {#default-password}

A fresh reference install creates `admin` with password `password`. Change it
immediately. An existing database keeps its existing password; provisioning
does not reset it.

### Why is there no "Open in HistomicsUI" button? {#no-open-button}

`large_image` did not recognize the file as a large image. Check the format,
convert to a pyramidal TIFF or OME-TIFF, and upload again. See
[Unsupported formats](#unsupported-format).

### Why can my colleague see the image but not my annotations? {#colleague-cannot-see-annotations}

Annotations have their own ACL, copied from the folder when each annotation was
created. Sharing the folder later does not update existing annotations. Use
**Annotation access control** on the folder. See
[Annotations are invisible after sharing a folder](#annotations-after-sharing).

### Why is the Analyses menu empty? {#empty-analyses-menu}

No Slicer CLI Web task is registered, or the image is not open. An administrator
must register a Docker image such as `dsarchive/histomicstk:latest`. See
[The Analyses menu is missing](#analyses-menu-missing).

### How do I restart or stop the stack? {#restart-stack}

Restart one service with `docker compose restart girder` or
`docker compose restart worker`. Stop everything with `docker compose down`.
`docker compose down -v` also removes temporary Docker volumes; the bind-mounted
`assetstore/`, `db/`, and `logs/` directories remain on disk.

### Where are the logs? {#logs-and-status}

Run `docker compose ps` for service health and `docker compose logs <service>`
for container output. On `devops/dsa`, Girder also writes `logs/info.log` and
`logs/error.log` inside the deployment directory. On `devops/ver5`, the logging
service writes `logs/info.log` for Girder and separate `logs/<service>.log`
files for the worker, MongoDB, RabbitMQ, and Redis.

### How do I report a bug? {#report-a-bug}

Open an issue in the repository that owns the failing part:

- [digital_slide_archive](https://github.com/DigitalSlideArchive/digital_slide_archive/issues)
  for installation, deployment, and jobs.
- [HistomicsUI](https://github.com/DigitalSlideArchive/HistomicsUI/issues)
  for the viewer, annotations, and analysis menus.
- [HistomicsTK](https://github.com/DigitalSlideArchive/HistomicsTK/issues)
  for analysis algorithms.
- [large_image](https://github.com/girder/large_image/issues) for image formats
  and tile sources.

Include the DSA release, the browser or client, the exact error text, and the
relevant log lines. Do not paste passwords, API keys, internal hostnames, or
patient data.

??? note "Source and version"

    Written on 2026-11-02 against the `devops/dsa` and `devops/ver5`
    deployments at
    [`2e16b9a`](https://github.com/DigitalSlideArchive/digital_slide_archive/commit/2e16b9a),
    HistomicsUI at
    [`75a9be6`](https://github.com/DigitalSlideArchive/HistomicsUI/commit/75a9be6),
    `large_image` at
    [`f4ad903`](https://github.com/girder/large_image/commit/f4ad903), and
    Girder `3.x-maintenance` at
    [`71e5fba`](https://github.com/girder/girder/commit/71e5fba).

    Commands and paths below were read from those checked-in files and upstream
    documentation. They were **not executed against a running DSA instance** in
    this documentation slice. Commands marked **host command** or **operational
    guidance** are standard system operations, not DSA-specific source.
