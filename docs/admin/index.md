# Administration

This section is for the person who runs a Digital Slide Archive instance: the
operator who owns the server, the accounts, the storage, and the upgrades. It is
not a guide to using DSA as a researcher. If you are looking for the viewer,
annotations, sharing, or analysis, start with the [User Guide](../user-guide/index.md)
and the [tutorials](../tutorials/index.md) instead.

The pages here assume DSA is already installed and running. The verified
[Ubuntu 24.04 install walkthrough](../get-started/install-ubuntu-24-04.md)
brings up the `devops/ver5` stack and ends with a working instance at
`http://localhost:8080`; this section starts where that guide stops.

## Three control surfaces

Almost every administrative task happens in one of three places. Knowing which
one owns a setting prevents the most common mistake: changing something in the
web console and expecting it to survive a redeploy, or editing a Compose file and
expecting a running container to notice.

| Surface | What it controls | Use it for |
| --- | --- | --- |
| Web admin console | Users, groups, collections, plugin settings, server configuration, assetstores, and jobs | Day-to-day account, policy, storage, and job work |
| Provision and Compose files | First-boot bootstrap, admin account, default collections, seeded plugin settings, service definitions, ports, environment, and volume mounts | Repeatable setup and changes that must survive container recreation |
| Container runtime | The running Girder, worker, MongoDB, RabbitMQ, Redis, and log collector processes | Start, stop, restart, inspect logs, and apply image or Compose changes |

### The web admin console

Sign in as a user with the site-admin flag and choose **Admin console** in the
left navigation, or open `http://localhost:8080/#admin`. The console itself has
four sections: **Server configuration**, **Plugins**, **Assetstores**, and
**Jobs**. **Users**, **Groups**, and **Collections** are top-level navigation
items that are visible to administrators and are covered in the console tour.

The console writes to the Girder database. Settings saved there take effect for
the application at runtime unless the setting defines a route, a mount point, or
a container environment variable. The [settings page](settings.md) spells out
which is which.

### The provision and Compose files

The `devops/ver5` directory contains the service definitions and the bootstrap
script:

| File | Role |
| --- | --- |
| `docker-compose.yml` | Services, images, ports, environment, and bind mounts |
| `provision.py` | Bootstrap and settings script run by the container entry points |
| `provision.yaml` | Inputs to `provision.py`: admin user, default assetstore, collections, and initial settings |
| `start_girder.sh`, `start_worker.sh` | Container entry points that call `provision.py` and start the processes |

`provision.py` is not a general-purpose settings editor. It creates an admin
only if no admin exists, creates the default filesystem assetstore only if no
assetstore exists, and with `force: False` writes a setting only when it is
missing or still has its default value. Editing `provision.yaml` is therefore
useful for a new instance or for values you have not already changed; it is not
a reliable way to overwrite settings that are already stored in the database.

The Compose file is the source of truth for anything that must exist before
Girder starts: the image version, published port, MongoDB and Redis addresses,
RabbitMQ credentials, the worker concurrency, and the `assetstore/`, `db/`, and
`logs/` bind mounts. Change these in the file and recreate the affected
containers; a running container does not read a changed environment variable
from the file.

### The container runtime

The running stack is the third surface. Use it to start and stop the stack,
watch logs, open a shell, and apply changes:

```bash
cd ~/devel/digital-slide-archive/devops/ver5
docker compose ps
docker compose logs --tail=100 girder
docker compose restart girder
docker compose up -d
```

`docker compose restart` restarts a container with its existing configuration.
It does not pick up a changed image, environment variable, or volume mount. Use
`docker compose up -d` after editing `docker-compose.yml`; Compose recreates the
affected containers and leaves the bind-mounted data in place.

## Which task lives where

| Task | Where |
| --- | --- |
| Create a user, reset a password, disable an account | Web console → **Users** |
| Grant or remove the site-admin flag | Web console → **Users** → user → **Actions** → **Edit user** |
| Create a group or change group roles | Web console → **Groups** |
| Change registration, collection-creation, or download policy | Web console → **Admin console** → **Server configuration** |
| Change large_image, HistomicsUI, Slicer CLI Web, or worker settings | Web console → **Admin console** → **Plugins** |
| Register an assetstore or import existing files | Web console → **Admin console** → **Assetstores** |
| Diagnose a failed analysis or import | Web console → **Admin console** → **Jobs** |
| Read container logs | Host shell → `docker compose logs` or the `logs/` directory |
| Change the published port, bind mounts, database address, or worker concurrency | `docker-compose.yml`, then `docker compose up -d` |
| Change the DSA image version | Pull the new image, update the Compose image reference if needed, then `docker compose up -d`; see [release notes](../release-notes.md) |
| Back up the instance | Host shell → MongoDB dump plus a copy of every assetstore |
| Change the HistomicsUI URL path | Web console → **Plugins** → **HistomicsUI**, then restart Girder |

## Before you make changes

- **Use a real admin account.** The stock provisioning creates `admin` with the
  password `password`. Change that password before the instance is reachable by
  anyone else, as the install guide warns.
- **Know where the data is.** Uploaded files live in the assetstore bind mount,
  metadata and accounts live in MongoDB, and the two must be backed up together.
  [Assetstores and storage](assetstores-and-storage.md) covers the layout and a
  backup procedure.
- **Change one thing at a time.** Most console changes are immediate. If a
  change has no effect, check whether it is a route or environment setting
  before restarting anything.
- **Do not edit files inside the assetstore by hand.** The filesystem assetstore
  is content-addressed; the database holds the references.

## In this section

- [Admin console tour](admin-console.md) — the screens for users, groups,
  collections, plugins, system configuration, assetstores, and jobs.
- [Users, groups, and roles for operators](users-and-roles.md) — creating and
  disabling accounts, the site-admin flag, and group roles.
- [Assetstores and storage](assetstores-and-storage.md) — the `assetstore/`
  bind mount, registering storage, permission pitfalls, and backups.
- [Plugin and system settings that matter for DSA](settings.md) — the settings
  an operator actually touches, and which changes need a restart.

??? note "Source and version"

    This page was written against the live local DSA 5 instance used for the
    verified install walkthrough and re-checked on 2026-11-13. It describes the
    stock `devops/ver5` files at commit `2e16b9a`; local site-specific mounts are
    called out where they appear in screenshots.

    | Item | Value |
    | --- | --- |
    | DSA / Girder | `5.0.23.dev5+g70eb94dcd` |
    | HistomicsUI | `1.8.1.dev208+gee5f4c0da.d20261030` |
    | large_image | `1.35.7.dev217+g09c6d7801` |
    | Slicer CLI Web | `5.0.23.dev5+g70eb94dcd` |
    | Deployment files | `devops/ver5` at `2e16b9a` |
    | Web address | `http://localhost:8080` |
