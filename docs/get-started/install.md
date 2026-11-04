# Install on one machine

!!! tip "Looking for the DSA 5 walkthrough?"

    [Install on Ubuntu 24.04 (DSA 5)](install-ubuntu-24-04.md) is a verified,
    screenshot-by-screenshot local install using the `devops/ver5` stack. This
    page covers the older Girder 3 reference deployment in `devops/dsa`. Use
    the page that matches the stack you intend to run.

This guide runs DSA on a single Linux computer with Docker Compose. It follows
the reference deployment in
[`devops/dsa`](https://github.com/DigitalSlideArchive/digital_slide_archive/tree/master/devops/dsa)

!!! note "Which Girder version is this?"

    The `devops/dsa` stack is the long-standing **Girder 3** reference
    deployment. The repository also contains a **Girder 5** reference
    deployment in
    [`devops/ver5`](https://github.com/DigitalSlideArchive/digital_slide_archive/tree/master/devops/ver5).
    This guide covers `devops/dsa` only. Do not assume that the commands below
    apply unchanged to `devops/ver5`.

## Prerequisites

- A 64-bit Linux machine. The upstream README says the stack was tested on
  Ubuntu 20.04; this slice checked the source and commands on Ubuntu 24.04.5.
- Docker Engine with the Compose v2 plugin, so the command is `docker compose`
  (not the old `docker-compose`).
- Git.
- Permission to use the Docker daemon. In practice, your user must be able to
  access `/var/run/docker.sock`, usually by being in the `docker` group.
- At least 2 CPU cores and 8 GB of RAM for a small instance. More memory and
  cores make analysis and tiled viewing much more comfortable.

DSA starts analysis tasks as sibling containers, so the Girder container mounts
the host Docker socket. Without that access, uploading and viewing may work but
analysis tasks will not.

## Start DSA

### 1. Get the repository

```bash
git clone https://github.com/DigitalSlideArchive/digital_slide_archive
cd digital_slide_archive/devops/dsa
```

### 2. Pull the prebuilt images

```bash
docker compose pull
```

If you skip this step, Docker Compose builds the main `dsarchive/dsa_common`
image locally instead of pulling it. Pulling is faster for a first run.

!!! warning "The compose file uses moving image tags"

    The reference stack uses tags such as `dsarchive/dsa_common`,
    `mongo:latest`, and `rabbitmq:latest`. Those tags can change between runs.
    For a reproducible deployment, pin image digests in a
    `docker-compose.override.yml`.

### 3. Start the stack

On Linux:

```bash
DSA_USER=$(id -u):$(id -g) docker compose up
```

`DSA_USER` tells the containers which host user and group should own the
assetstore, database files, logs, and temporary files. Use `UID:GID` format.
The startup script rejects `0:0`: DSA will not start as root.

The command stays in the foreground. Add `-d` if you prefer to run it in the
background:

```bash
DSA_USER=$(id -u):$(id -g) docker compose up -d
```

On Windows, the upstream README uses:

```bat
set DSA_USER=1000:1000
docker compose up
```

### 4. Wait for Girder

The Girder container has a health check. You can also poll the API from the
host:

```bash
curl --silent http://localhost:8080/api/v1/system/version
```

When Girder is ready, the response contains a `"release"` field. Then open:

<http://localhost:8080>

The default administrator account is `admin` with password `password`. Change
that password before exposing the instance to anyone else.

The default provisioning does not add sample data or analysis tasks. You will
create your own collection and upload a slide in
[Upload and view your first slide](first-slide.md).

## Stop DSA

```bash
docker compose down -v
```

The `-v` flag removes temporary Docker volumes. The bind-mounted `assetstore/`,
`db/`, and `logs/` directories in `devops/dsa` remain on disk.

## Install settings you are likely to change

| Variable | Default | Effect |
| --- | --- | --- |
| `DSA_USER` | none; startup fails | Host `UID:GID` that owns files and can access Docker. |
| `DSA_PORT` | `8080` | Host port mapped to Girder's port 8080. |
| `DSA_WORKER_CONCURRENCY` | `2` | Number of jobs a worker process runs at once. |
| `DSA_PROVISION_YAML` | `/opt/digital_slide_archive/devops/dsa/provision.yaml` | Provisioning file used at startup. |
| `TMPDIR` | `/tmp` | Host temporary directory shared with the worker for task data. |

These names come from
[`devops/dsa/docker-compose.yml`](https://github.com/DigitalSlideArchive/digital_slide_archive/blob/master/devops/dsa/docker-compose.yml).

## Troubleshooting

For a symptom-first index that also covers authentication, viewing, upload,
permissions, annotations, analysis jobs, and recovery, see
[Troubleshooting and FAQ](../troubleshooting.md#install-and-startup).

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `Bind for 0.0.0.0:8080 failed: port is already allocated` | Another process, often another DSA instance, owns port 8080. | Stop the other process, or start with `DSA_PORT=8081 DSA_USER=$(id -u):$(id -g) docker compose up` and open `http://localhost:8081`. |
| Files in `assetstore/`, `db/`, or `logs/` are owned by `root`; Girder cannot write. | `DSA_USER` was omitted or set to `0:0`. | Restart with `DSA_USER=$(id -u):$(id -g)`. To repair files created by an earlier root run: `sudo chown -R $(id -u):$(id -g) assetstore db logs` from `devops/dsa`. |
| `permission denied while trying to connect to the Docker daemon socket` | Your user cannot access `/var/run/docker.sock`. | Add your user to the `docker` group, log out and back in, and confirm with `docker info`. Rootless Docker uses a different socket path and is not covered by this compose file. |
| The machine becomes unresponsive, the Mongo container is killed, or analysis jobs die. | Out of memory. A small host running several tasks can exhaust RAM. | Give the VM or host more memory, reduce `DSA_WORKER_CONCURRENCY`, and check `dmesg` for the OOM killer. |
| An uploaded file never shows an "Open in HistomicsUI" button, or the viewer reports an unsupported image. | `large_image` has no tile source for that format. | Check the format against [large_image's supported sources](https://github.com/girder/large_image#tile-sources). Convert the slide to a pyramidal TIFF or OME-TIFF, then upload it again. Check `docker compose logs girder` for tile-source errors. |
| Analysis tasks stay queued, or the UI reports that no worker is connected. | The worker container is stopped, unhealthy, or cannot reach RabbitMQ. | Run `docker compose ps` and check that `rabbitmq` and `worker` are healthy. Inspect `docker compose logs worker` and `docker compose logs rabbitmq`, then restart with `docker compose restart worker`. |
| Girder never becomes ready. | A dependency failed to start, or provisioning failed. | Run `docker compose ps`, then `docker compose logs girder mongodb`. The health check polls `/api/v1/system/version` every five minutes; the first start can take a minute or two. |

## What was verified in this slice

Docker is not installed in the documentation build environment and
`/var/run/docker.sock` does not exist there, so the container commands below
were **not executed**. They are transcribed from the upstream README and
compose file, not labelled "tested".

| Step | Environment | Result |
| --- | --- | --- |
| `git clone https://github.com/DigitalSlideArchive/digital_slide_archive` | Ubuntu 24.04.5, Git 2.43.0 | Succeeded; cloned HEAD `2e16b9a`. |
| `cd digital_slide_archive/devops/dsa` | Ubuntu 24.04.5 | Succeeded; `docker-compose.yml` is present. |
| `docker compose pull` | Ubuntu 24.04.5 | Not run: `docker` is not installed. |
| `DSA_USER=$(id -u):$(id -g) docker compose up` | Ubuntu 24.04.5 | Not run: no Docker daemon or socket. |
| `curl http://localhost:8080/api/v1/system/version` | Ubuntu 24.04.5 | Not run against a local instance; the public demo endpoint was reachable. |
| Reading `docker-compose.yml` for `DSA_USER`, `DSA_PORT`, socket mount, and health checks | Source at `2e16b9a` | Confirmed in the checked-in file. |

For the record, this environment reports `UID:GID` as `1000:1000`, which is the
value `$(id -u):$(id -g)` would substitute.

## Next

- [Upload and view your first slide](first-slide.md)
- [Mouse and keyboard controls](../user-guide/controls.md)
- [Troubleshooting](#troubleshooting)

??? note "Source and version"

    This guide follows the reference deployment in
    [`devops/dsa`](https://github.com/DigitalSlideArchive/digital_slide_archive/tree/master/devops/dsa)
    and was written against commit
    [`2e16b9a`](https://github.com/DigitalSlideArchive/digital_slide_archive/commit/2e16b9a).
