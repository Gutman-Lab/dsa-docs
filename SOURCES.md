# Content sources and consolidation status

This repository deliberately replicates material that also lives elsewhere. The
goal of this first version is one browsable place for DSA information and
tutorials; each page records its origin so we can converge later instead of
forking silently.

## Pages in this repository

| Page | Source | Adaptation notes |
| --- | --- | --- |
| `docs/index.md` | New | Landing page and navigation for the consolidated site. |
| `docs/get-started/what-is-dsa.md` | New, from upstream `README.rst` and `docs/index.md` at `2e16b9a` | Short orientation; links to upstream components. |
| `docs/get-started/try-the-demo.md` | Upstream demo links | Demo URLs and expectations only. |
| `docs/get-started/install.md` | `devops/dsa/README.rst` and `devops/dsa/docker-compose.yml` at `2e16b9a` | Commands transcribed, not executed here (no Docker). Corrects the stale Girder 3 claim. |
| `docs/get-started/install-ubuntu-24.04.md` | GUT-25 install walkthrough, `devops/ver5` at `2e16b9a`; package from GUT-30 | New 2026-11-02. **Verified** end to end on Ubuntu 24.04.5, Docker 29.9.2, Compose v5.6.1, DSA `5.0.23.dev5+g70eb94dcd`. 12 screenshots in story order; print-ready PDF and full bundle under `docs/assets/downloads/`. Internal DICOM planning section excluded from the public page. |
| `docs/get-started/first-slide.md` | Upstream workflow docs | Upload, viewer, and sample-data steps. CLI steps unexecuted. |
| `docs/get-started/next-steps.md` | New | Points at tutorials, reference, and community channels. |
| `docs/user-guide/index.md` | New | Section landing page. |
| `docs/user-guide/controls.md` | HistomicsUI `docs/controls.rst` at `2e9a298` (2025-12-03) | Adapted 2026-11-01 under Apache-2.0; attribution on the page. Controls not re-tested live. |
| `docs/user-guide/annotations.md` | HistomicsUI README, `web_client` panels and dialogs at `75a9be6`; `docs/config_options.rst` | Expanded 2026-11-01: annotation documents, panels, draw tools, autosave, element editing, job ingestion. Source-verified; not click-tested on a writable slide. |
| `docs/user-guide/annotation-groups.md` | HistomicsUI `docs/config_options.rst` and `docs/annotation_group_restrictions.rst` at `75a9be6`, plus `web_client/utilities/allowedGroups.js` | New 2026-11-01: style-group YAML, hotkeys, `allowed_groups` validation, auto-creation, and selection behavior. Source-verified, not live-tested. |
| `docs/user-guide/permissions.md` | Girder `docs/user-guide.rst` and web client access templates at `70eb94d`; `girder/large_image` `docs/girder_annotation_access.rst` at `f4ad903` | New 2026-11-02: roles, groups, private/public, inheritance, access flags, and annotation access rules. Role and inheritance behavior live-checked on a local DSA 5 stack; annotation ACL rules source-verified. |
| `docs/system-overview.md` | Upstream `docs/system-overview/index.md` | Moved and lightly edited; diagrams copied. |
| `docs/tutorials/index.md` | New | Tutorial index; lists the task walkthroughs and the remaining plan. |
| `docs/tutorials/connect.md` | New, from Girder `3.x-maintenance` UI source at `71e5fba` | Sign-in, registration, workspace, and API-key connection. Live-tested with a signed-in test account on `pub-data.bdsa.io` on 2026-11-01; screenshots captured. Two-factor login was not exercised. |
| `docs/tutorials/create-a-collection.md` | New, from the live instance's served web client on 2026-11-01 | Collection creation and the private-by-default access rule. Live-tested end to end on `pub-data.bdsa.io` on 2026-11-01 with an administrator account, including creation and deletion of the test collection and its first folder. Collection creation is administrator-only there; a non-admin attempt is recorded in the page. |
| `docs/tutorials/create-a-folder.md` | New, from Girder `3.x-maintenance` UI source at `71e5fba` | Folder creation flow. Live-tested on `pub-data.bdsa.io` on 2026-11-01; screenshots captured. |
| `docs/tutorials/copy-an-item.md` | New, from Girder `3.x-maintenance` UI source at `71e5fba` | Pick-and-copy flow and the `copyItem` model behavior. Live-tested on `pub-data.bdsa.io` on 2026-11-01; screenshots captured. |
| `docs/tutorials/edit-metadata.md` | New, from Girder `3.x-maintenance` UI source at `71e5fba` | Simple and JSON metadata editing plus key validation rules. Simple values live-tested on `pub-data.bdsa.io` on 2026-11-01; JSON editor and key validation remain source-verified. |
| `docs/tutorials/share-a-collection.md` | Girder `AccessWidget.js` and `accessEditor` templates at `70eb94d`; `girder/large_image` annotation access docs at `f4ad903` | New 2026-11-02: Access control dialog, roles, private/public, subfolder propagation, access flags, and annotation ACL caveats. Live-tested end to end on a local DSA 5 stack with an owner and a non-admin user; screenshots captured. The bulk **Annotation access control** dialog was not exercised and its rules remain source-verified. |
| `docs/tutorials/annotate-a-slide.md` | New, from HistomicsUI `web_client` at `75a9be6` | Create annotation dialog, style group, draw tools and shortcuts, element context menu, download. Source-verified; not click-tested (no writable account in this slice). |
| `docs/tutorials/run-an-analysis.md` | New, from HistomicsUI `web_client` and `docs/slicer_cli_plugins.rst` at `75a9be6` | Analyses menu, generated input panel, region selection, job submission, result ingestion. Source-verified; not live-tested. |
| `docs/assets/tutorials/*.png` | Live capture | Real screenshots of the signed-in user menu, API keys tab, folder actions, create-folder dialog, checked actions and copy flow, metadata rows, and upload. Captured on `pub-data.bdsa.io` on 2026-11-01. |
| `docs/assets/tutorials/collections-list.png`, `create-collection-dialog.png`, `collection-created.png`, `collection-first-folder.png` | Live capture | Collections list, Create collection dialog, new collection page, and the collection with its first folder. Captured on `pub-data.bdsa.io` on 2026-11-01 with an administrator account; the temporary collection was deleted afterward. |
| `docs/assets/tutorials/connect-login.png`, `connect-register.png` | Live capture | Real screenshots of the Log in and Sign up dialogs from `pub-data.bdsa.io` on 2026-11-01. |
| `docs/assets/tutorials/share-*.png` | Live capture | Collection **Actions** menu, access control dialogs, the public option, the **Create annotations** access flag, the recursive subfolder option, and a non-admin user's view. Captured on a local DSA 5 stack on 2026-11-02 with an owner account and a non-admin collaborator; the test collection and users were created for the run. |
| `docs/reference/rest-api.md` | Girder `girder/api/v1/{user,api_key,collection,folder,item,file,resource}.py` at `70eb94dcd`; large_image `girder/girder_large_image/rest/tiles.py` and `girder_annotation/girder_large_image_annotation/rest/annotation.py` at `09c6d7801`; `slicer_cli_web/rest_slicer_cli.py` at `70eb94dcd`; live local DSA 5 instance | Reworked 2026-11-02 from a generic skeleton into a verified cookbook. Every recipe was executed against the local DSA 5 stack (Girder `5.0.23.dev5+g70eb94dcd`, `large_image`/`large_image_annotation` `1.35.7.dev217+g09c6d7801`, HistomicsUI `1.8.1.dev208+gee5f4c0da.d20261030`). Read-only list, lookup, tile, and annotation-list recipes were also checked against the public demo (Girder `3.2.18.dev2+g339bcdfe6`). API-key exchange was re-tested and corrected to a form-encoded `POST /api_key/token`. See the page's **Verified status** and **Route sources** sections. |
| `docs/reference/python-client.md` | `girder-client` `5.0.22` (PyPI) and `5.0.23.dev5+g70eb94dcd` (DSA 5 image); live local DSA 5 instance | Reworked 2026-11-02 with a complete runnable script. Executed end to end locally with both clients and with API-key and username/password authentication: path lookup, collection tree walk, metadata read/write, annotation list/create, item creation and upload, file download with SHA-512 comparison, tile fetch, and analysis job submission/polling. Read-only checks were also made against the public demo. See the page's **Verified status** section. |
| `docs/reference/bdsa-react-components.md` | Published package `bdsa-react-components` 0.2.5 type declarations and repo `Gutman-Lab/bdsa-react-components` at `399c2b3` | Expanded 2026-11-01: install, peer dependencies, auth store/hooks, FolderBrowser, SlideViewer, annotation/thumbnail/protocol components, and version notes. Source-verified against types; not rendered in a live app. The repo's README/API.md are stale where they mention removed exports. |
| `docs/release-notes.md` | DSA merged PRs #532–#538, CircleCI config at `2e16b9a`, Docker Hub tags/digests, and `build-tracking` at `85ae552` | Rewritten 2026-11-02: release model, first date-stamped-image entry, upgrade/rollback, process, and template. No release or deploy automation added. |
| `docs/contributing.md` | Upstream repo conventions | Contributor entry point for DSA and this docs repository. |
| `docs/troubleshooting.md` | New 2026-11-02, from `devops/dsa` and `devops/ver5` at `2e16b9a`, HistomicsUI `75a9be6`, `large_image` `f4ad903`, and Girder `3.x-maintenance` `71e5fba`; public issues in DSA, HistomicsUI, and large_image | Symptom-first guide covering install, authentication, viewing, upload, permissions, annotation, analysis jobs, and data recovery, plus an FAQ. Commands and paths are **source-verified** from checked-in compose files, startup scripts, and upstream docs; **none were executed against a running instance** in this slice. Host-level commands are labelled. Links to upstream issues rather than restating their detail. |
| `docs/migration.md` | Upstream `docs/migration.rst` at `2e16b9a` | RST converted to Markdown; commands transcribed, not executed. |
| `docs/about.md` | Upstream `README.rst`, `docs/index.md`, and the HPC/community links at `2e16b9a` | New synthesis: history, license, funding, community, collaborators, citation. The upstream `docs/about/index.md` is untouched Jekyll boilerplate and was not reused. |
| `docs/success-stories.md` | Upstream `docs/_success_stories/*.md` at `2e16b9a` | Both stories converted from Jekyll HTML to Markdown; references kept. |
| `docs/papers-publications.md` | Upstream `docs/papers-publications/index.md` front matter at `2e16b9a` | 24 entries generated from the YAML list; not independently checked against a citation database. |

## Still to consolidate

These are known sources that are not yet represented here. Each should become a
page or merge into an existing page in a later slice.

- Upstream marketing homepage callouts. The demos page
  (`docs/demos-examples/index.md`) has one Kitware demo link that is already
  covered by [Try the demo](docs/get-started/try-the-demo.md).
  `docs/documentation/index.md` was reviewed on 2026-11-01: it is only a redirect
  to the upstream MkDocs site, with no tutorial list to copy.
- Remaining HistomicsUI user and developer documentation: installation,
  plugin configuration beyond style groups, permissions, and the full Slicer CLI
  schema. The annotation and analysis workflows are now represented here.
- Girder user and administrator documentation that DSA relies on. The
  DSA-specific API routes are now covered by the cookbook pages; Girder's
  administrative settings, assetstores, and plugin management are still
  upstream-only.
- Analysis task documentation beyond the verified `BackgroundIntensity` example:
  the full Slicer CLI schema, batch inputs, and task-image authoring.
- Deployment material under `devops/` (external workers, version 5 stack,
  Apptainer and Docker image builds).
- Existing Gutman-Lab documentation repositories: `bdsa-docs`,
  `bdsa-readthedocs`, and `DSA-LLM-Docs`.

## Replication policy

1. Copy first, edit second. Keep the upstream wording unless it is wrong or
   unclear, so diffs against the source stay small.
2. Record the source path and, where possible, the commit hash in this file and
   in the page's front matter or a note.
3. Mark verification status explicitly: `Verified` only for commands actually
   executed, `Transcribed` for commands read from source, `Unverified` for
   anything else.
4. When a page becomes canonical, update the source to link here and mark the
   old copy as deprecated rather than deleting it.
