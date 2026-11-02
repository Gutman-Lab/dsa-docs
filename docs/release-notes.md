# Release and upgrade notes

This page is the release and upgrade feed for the Digital Slide Archive (DSA).
It records what changed in each release, what operators must do before and after
upgrading, and how to roll back.

!!! info "Preview and proposed process"

    This page is part of the consolidated documentation preview at
    <https://gutman-lab.github.io/dsa-docs/>. It is not part of the official
    DSA documentation site yet. The source-of-truth choice and process below are
    **proposed** and await confirmation from the Chief of Staff and DevOps. No
    release or deployment automation has been added.

## What counts as a release

DSA does not publish GitHub Releases, and the repository has no maintained
`CHANGELOG.md`. The GitHub tags are old: `v1.0.0` is from 2020-02-18 and
`v1.1.0` is from 2020-11-04. They do not describe current releases.

In practice, a DSA release is a **date-stamped container image** built from
`master` by CircleCI:

| Image | Deployment | Tags |
| --- | --- | --- |
| `dsarchive/dsa_common` | Girder 3 reference stack in `devops/dsa` | `latest`, `YYYYMMDD`, and `v*` when a git tag exists |
| `dsarchive/dsa_common_5` | Girder 5 reference stack in `devops/ver5` | `latest`, `YYYYMMDD`, and `v*` when a git tag exists |

The publish jobs tag each successful build with the build date. See
[`publish-docker-common` and `publish-docker-common-5`](https://github.com/DigitalSlideArchive/digital_slide_archive/blob/2e16b9a/.circleci/config.yml)
and the [Docker Hub tags for `dsa_common_5`](https://hub.docker.com/r/dsarchive/dsa_common_5/tags).

For these notes, the **release identifier is the date tag** (for example
`20261030`), and every entry records the `master` commit it was built from.
`/api/v1/system/version` reports the Girder server version (for example
`5.0.23.dev5+g70eb94dcd`), not the DSA release identifier.

## Current release: 20261030

**Published:** 2026-10-30 (image build)
**Source:** `master` at [`2e16b9a`](https://github.com/DigitalSlideArchive/digital_slide_archive/commit/2e16b9a), the merge of PR #538 on 2026-10-29
**Images:** `dsarchive/dsa_common:20261030` and `dsarchive/dsa_common_5:20261030`
**Coverage:** PRs #532–#538, merged 2026-10-02 through 2026-10-29

!!! note "First entry"

    This is the first real entry. It is a baseline for the October 2026 build,
    not a delta from an earlier notes page. September and earlier history is not
    backfilled.

### Added

- **Local Kubernetes test harness and sample Helm charts.** `devops/k8s-local`
  adds a `kind`-based local cluster, helper scripts, and two sample charts:
  `dsa3` 0.1.0 for the Girder 3 stack and `dsa5` 0.1.0 for the Girder 5 stack.
  The charts are explicitly for local development and chart validation, not for
  production. ([#534](https://github.com/DigitalSlideArchive/digital_slide_archive/pull/534),
  [b75c48f](https://github.com/DigitalSlideArchive/digital_slide_archive/commit/b75c48f))

### Changed

- **Pre-commit hook versions updated.** The repository's pre-commit
  configuration moved to newer hook revisions. ([#535](https://github.com/DigitalSlideArchive/digital_slide_archive/pull/535),
  [2d71d6f](https://github.com/DigitalSlideArchive/digital_slide_archive/commit/2d71d6f))

### Fixed

- **Documentation typo.** "replacable" was corrected to "replaceable" in
  `devops/slurm/HPC.md`. ([#535](https://github.com/DigitalSlideArchive/digital_slide_archive/pull/535),
  [2d71d6f](https://github.com/DigitalSlideArchive/digital_slide_archive/commit/2d71d6f))

### Security

- **No DSA runtime security changes in this window.** PRs
  [#532](https://github.com/DigitalSlideArchive/digital_slide_archive/pull/532),
  [#533](https://github.com/DigitalSlideArchive/digital_slide_archive/pull/533),
  [#536](https://github.com/DigitalSlideArchive/digital_slide_archive/pull/536),
  [#537](https://github.com/DigitalSlideArchive/digital_slide_archive/pull/537),
  and [#538](https://github.com/DigitalSlideArchive/digital_slide_archive/pull/538)
  changed only `.trivyignore`, the list of vulnerabilities the image scanner is
  told to ignore. They did not change runtime package versions. The Trivy scan
  itself is still part of the CircleCI pipeline.

### Upgrade notes

- **Breaking changes:** none.
- **Database:** no migration. No changes to either reference compose file in
  this window.
- **Assetstore:** no migration.
- **Configuration:** no new required settings.
- **Action required:** none for existing deployments. If you want the new local
  Kubernetes harness, see `devops/k8s-local/README.rst`; do not treat those
  charts as a production deployment.

### Known issues

- The new `devops/k8s-local` charts are local-development only. They use
  single-replica in-cluster MongoDB, RabbitMQ, Redis (for `dsa5`), and Memcached
  (for `dsa3`), with `ReadWriteOnce` volumes and no backup or high-availability
  story. See the [chart README](https://github.com/DigitalSlideArchive/digital_slide_archive/blob/b75c48f/devops/k8s-local/README.rst).
- The reference compose files still use moving tags such as `mongo:latest`,
  `rabbitmq:latest`, `memcached`, and `redis`. That is existing behaviour, not
  new in this release; pin image digests in `docker-compose.override.yml` when
  you need a reproducible deployment.
- No other known issues were recorded for this window. Check
  [open issues](https://github.com/DigitalSlideArchive/digital_slide_archive/issues)
  for current reports.

### Components in the 20261030 image

The image is built from `master` plus the upstream branches recorded in the
`build-tracking` file written after the build. The key commits are:

| Component | Branch | Commit |
| --- | --- | --- |
| Girder (Girder 5 stack) | `master` | [`70eb94d`](https://github.com/girder/girder/commit/70eb94dcdcf9f92d6e5252c83bbadc6d8c98db6b) |
| Girder (Girder 3 stack) | `3.x-maintenance` | [`71e5fba`](https://github.com/girder/girder/commit/71e5fbabb740f77df7c66e04768e5e40a701452e) |
| HistomicsUI (Girder 5 stack) | `girder-5` | [`ee5f4c0`](https://github.com/DigitalSlideArchive/HistomicsUI/commit/ee5f4c0da27b6692ba33edd716ec8b96517c16d3) |
| HistomicsUI (Girder 3 stack) | `girder-3` | [`75a9be6`](https://github.com/DigitalSlideArchive/HistomicsUI/commit/75a9be6234adf22491092deea99c9ac50b40bead) |
| large_image (Girder 5 stack) | `girder-5` | [`09c6d78`](https://github.com/girder/large_image/commit/09c6d78019c0381402cd814a0060cf4af1bb569e) |
| large_image (Girder 3 stack) | `girder-3` | [`b2c8c21`](https://github.com/girder/large_image/commit/b2c8c216b65ef68df6164a5f1080e2d9da867c5d) |
| girder_assetstore (Girder 5 stack) | `girder-5` | [`f860fef`](https://github.com/DigitalSlideArchive/girder_assetstore/commit/f860fef09e0530965e03f0d43fd3d87651628755) |
| slicer_cli_web | `master` | [`9da9ba6`](https://github.com/girder/slicer_cli_web/commit/9da9ba6b2d9936a01e7f529ca0d51e4ce6e53566) |

Source: [`last_build_commits.json` at 85ae552](https://github.com/DigitalSlideArchive/digital_slide_archive/blob/85ae552/last_build_commits.json).
The full file records the remaining branches, including `girder_worker`,
`geojs`, and `import-tracker`.

## Upgrade and rollback

These steps apply to both reference stacks. Replace `dsa_common_5` with
`dsa_common` and `devops/ver5` with `devops/dsa` for the Girder 3 stack.

### Before upgrading

1. Read the entry's **Upgrade notes** section. If it names a migration, plan it
   before pulling.
2. Record the image you are running and its digest:

   ```bash
   docker compose images
   docker inspect --format '{{index .RepoDigests 0}}' dsarchive/dsa_common_5:latest
   ```

3. Back up the data and configuration. In the reference deployments, the
   database and assetstore are bind-mounted under `devops/dsa/` or
   `devops/ver5/`:

   ```bash
   tar -czf dsa-backup-$(date +%Y%m%d).tar.gz db assetstore docker-compose.override.yml
   ```

4. If the entry involves MongoDB, read
   [MongoDB version compatibility](migration.md#mongodb-version-compatibility)
   and check the current feature compatibility version before changing images.

### Pin and upgrade

Pin both the Girder and worker services in `docker-compose.override.yml` when
you need a reproducible deployment. For the Girder 5 stack:

```yaml
services:
  girder:
    image: dsarchive/dsa_common_5@sha256:7f8515756e8e35802c0707d8245baa41ac0e2b2866bf2501e31a50586941d33a
  worker:
    image: dsarchive/dsa_common_5@sha256:7f8515756e8e35802c0707d8245baa41ac0e2b2866bf2501e31a50586941d33a
```

Then pull and restart:

```bash
docker compose pull
DSA_USER=$(id -u):$(id -g) docker compose up -d
curl --silent http://localhost:8080/api/v1/system/version
```

Open the site, sign in, open a slide, and run one small analysis task if your
deployment uses them. These are the same smoke checks used for a new install;
see [Install on one machine](get-started/install.md).

### Rollback

The previous date tags are still on Docker Hub:

| Release | `dsa_common` digest | `dsa_common_5` digest |
| --- | --- | --- |
| `20261030` (this entry) | `sha256:4f24f2efd1195b7a69244f22761782f5bd6f508502e1fa6dc374f30d92e48071` | `sha256:7f8515756e8e35802c0707d8245baa41ac0e2b2866bf2501e31a50586941d33a` |
| `20261029` | `sha256:7e4d3582d40915601df597e910ae426005c589a40c6c9eb316c568e2044eb9b3` | `sha256:907d9e15bc7988f40187bba183327a482bc76bdd2d1172b2f24874e0d10a2b4d` |
| `20261027` | `sha256:114b938949ed5287c8201ff7dfbd3c83a403fb70932831ab32475379f1009350` | `sha256:f50d98c7c7228773a1c7996cbefaa15793b2b117ab30575aca7cf1980ecdc021` |

`20261030` made no database or assetstore changes, so rolling back to
`20261029` only requires pinning the older digest and restarting. For any entry
that does name a migration, restore the matching `db/` and `assetstore/` backup
after stopping the stack; do not run an older image against a database that was
already migrated.

```bash
docker compose down
# set the older digest in docker-compose.override.yml, then:
DSA_USER=$(id -u):$(id -g) docker compose up -d
```

## Release-notes process (proposed)

### Source of truth

**Proposed: this page.** `docs/release-notes.md` in
[`Gutman-Lab/dsa-docs`](https://github.com/Gutman-Lab/dsa-docs) is the canonical
release and upgrade feed.

Why this is the lightest option:

| Option | What it needs | Why it is not the first choice |
| --- | --- | --- |
| GitHub Releases | A tag and a written release for every entry | The project's last tags are from 2020; adopting releases would change the release process |
| `CHANGELOG.md` in `digital_slide_archive` | Every contributor to update another file in the code repository | Adds a second source and a new upstream convention; the repository has never had one |
| This docs page | A monthly pass over merged PRs and `build-tracking` | No upstream process change; the raw material already exists |

If the project later adopts GitHub Releases or a changelog, this page should
become the human-readable summary that links to it. Do not maintain two full
copies.

### Who writes entries

- **Draft author:** CMO.
- **Technical check:** DevOps for image tags, compose files, database,
  assetstore, and rollback; Frontend for HistomicsUI and
  `bdsa-react-components` changes.
- **Process owner:** Chief of Staff.
- **Breaking changes:** the maintainer who made the change must supply the
  upgrade and rollback text before the entry is published.

### Cadence

- At least once a month.
- Immediately when a release contains a breaking change, a security fix, a
  database or assetstore migration, or a change that affects rollback.
- Do not backfill entries that cannot be tied to a merged PR or commit.

### Where entries are published

- On the documentation preview at <https://gutman-lab.github.io/dsa-docs/>.
- The official upstream documentation site is not changed until the user
  reviews and approves the consolidated site.
- The entry may be reused as the body of a GitHub Release if the project adopts
  releases later.

### Entry rules

- Every version, date, and change cites a merged PR, commit, or tag.
- Use the date stamped on the image as the release date. Do not infer a release
  date from a commit date.
- Record the image digest for both stacks when the entry is published.
- Mark commands as verified or unverified. Never call an untested command
  "tested".
- Append a dated correction instead of silently rewriting a published entry.

### Automation

None. The existing CircleCI image build and Trivy scan are unchanged. This
process does not add a release job, a tag, or a deploy step.

## Entry template

Copy this when adding a release. Keep the section order stable.

```markdown
## <YYYYMMDD>

**Published:** <YYYY-MM-DD> (image build)
**Source:** `master` at [`<short-sha>`](<commit-url>), the merge of PR #<n> on <YYYY-MM-DD>
**Images:** `dsarchive/dsa_common:<tag>` and `dsarchive/dsa_common_5:<tag>`
**Coverage:** PRs #<first>–#<last>, merged <YYYY-MM-DD> through <YYYY-MM-DD>

### Added

- **<Change>.** <What changed and who it affects>. ([#<n>](<pr-url>), [<sha>](<commit-url>))

### Changed

- **<Change>.** <What changed and who it affects>. ([#<n>](<pr-url>), [<sha>](<commit-url>))

### Fixed

- **<Fix>.** <What was broken and what is fixed>. ([#<n>](<pr-url>), [<sha>](<commit-url>))

### Security

- **<Fix or "No changes">.** <CVE, affected component, or why there is no runtime change>.

### Upgrade notes

- **Breaking changes:** <none, or the exact change and the new setting>.
- **Database:** <migration, or "none">.
- **Assetstore:** <migration, or "none">.
- **Configuration:** <new or removed settings>.
- **Action required:** <steps, or "none">.

### Known issues

- <Issue and workaround, or "None recorded">.
```

## Sources checked

Checked on 2026-11-02:

- `git log --merges --since=2026-09-29 --until=2026-10-31` on
  [`digital_slide_archive`](https://github.com/DigitalSlideArchive/digital_slide_archive)
  for PR merge commits and dates.
- [`.circleci/config.yml` at `2e16b9a`](https://github.com/DigitalSlideArchive/digital_slide_archive/blob/2e16b9a/.circleci/config.yml)
  for the image-publish and tag logic.
- [Docker Hub tags for `dsa_common_5`](https://hub.docker.com/r/dsarchive/dsa_common_5/tags)
  and `dsa_common` for the `20261030`, `20261029`, and `20261027` tags and
  digests.
- [`last_build_commits.json` at `85ae552`](https://github.com/DigitalSlideArchive/digital_slide_archive/blob/85ae552/last_build_commits.json)
  for the component commits recorded after the 2026-10-30 build.
- The [`v1.0.0`](https://github.com/DigitalSlideArchive/digital_slide_archive/tree/v1.0.0)
  and [`v1.1.0`](https://github.com/DigitalSlideArchive/digital_slide_archive/tree/v1.1.0)
  tags for the historical tag dates.
