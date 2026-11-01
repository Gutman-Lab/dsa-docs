# Migration guide

This page helps you move between major versions of the Digital Slide Archive.
It is consolidated from the upstream `docs/migration.rst` on 2026-11-01.

!!! note "Which deployment does this cover?"

    The current installation method is `docker compose`. The `devops/dsa`
    reference deployment is based on Girder 3.x; a Girder 5 reference
    deployment is available in `devops/ver5`. This guide covers migrations for
    the `devops/dsa` stack unless a section says otherwise.

## From `deploy_docker.py` to Docker Compose

Before 2021, DSA used the `deploy_docker.py` script. If you deployed the
software another way, these instructions need adjustment.

`deploy_docker.py` predates Docker Compose handling all of the desired
features. If you passed command-line options to `deploy_docker.py`, translate
each one into the Compose notation. For the default deployment with no
options, switch as follows.

First, take ownership of the existing data directory:

```bash
chown -R $(id -u):$(id -g) ~/.dsa
```

Then add `docker-compose.override.yml` to the `devops/dsa` directory,
replacing `/home/ubuntu` with the resolution of `~`:

```yaml
---
services:
  girder:
    volumes:
      - /home/ubuntu/.dsa/assetstore:/opt/digital_slide_archive/assetstore
      - /home/ubuntu/.dsa/logs:/logs
  mongodb:
    volumes:
      - /home/ubuntu/.dsa/db:/data/db
```

From the `devops/dsa` directory, `docker compose` now uses the existing data.

## From Girder 2.x and the HistomicsTK repository

The DSA deployment was originally part of the HistomicsTK repository and used
Girder 2.x as the server. To migrate from a Girder 2.x instance to the version
in this repository, no special changes are needed: use the current
`deploy_docker.py` script from this repository.

## MongoDB version compatibility

By default the latest major version of MongoDB is used. MongoDB does not
automatically upgrade database files across more than one major version beyond
the last update. For example, a database created in MongoDB 3.4 works with 3.6
but not 4.0.

On a running instance, find the version the database is compatible with:

```bash
docker exec histomicstk_mongodb mongo girder --eval \
  'db.adminCommand({getParameter: 1, featureCompatibilityVersion: 1})'
```

If that is not the version you need, upgrade the compatibility version. For
example, to move to MongoDB 4.2:

```bash
docker exec histomicstk_mongodb mongo girder --eval \
  'db.adminCommand({setFeatureCompatibilityVersion: "4.2"})'
```

To start DSA with an older MongoDB, set the version in the `mongo` container's
image name in `docker-compose.override.yml`. If the database is old enough, move
one major version at a time and adjust the compatibility version at each step.

!!! warning "These commands were not executed for this page"

    The commands above are transcribed from the upstream migration guide. They
    are not a substitute for a backup. Back up the database and assetstore
    before changing the MongoDB version or compatibility setting.
