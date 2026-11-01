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
| `docs/get-started/first-slide.md` | Upstream workflow docs | Upload, viewer, and sample-data steps. CLI steps unexecuted. |
| `docs/get-started/next-steps.md` | New | Points at tutorials, reference, and community channels. |
| `docs/user-guide/index.md` | New | Section landing page. |
| `docs/user-guide/controls.md` | HistomicsUI `docs/controls.rst` at `2e9a298` (2025-12-03) | Adapted 2026-11-01 under Apache-2.0; attribution on the page. Controls not re-tested live. |
| `docs/user-guide/annotations.md` | New skeleton | To be filled from HistomicsUI and Girder annotation docs. |
| `docs/system-overview.md` | Upstream `docs/system-overview/index.md` | Moved and lightly edited; diagrams copied. |
| `docs/tutorials/index.md` | New | Tutorial index; lists the four task walkthroughs and the remaining plan. |
| `docs/tutorials/connect.md` | New, from Girder `3.x-maintenance` UI source at `71e5fba` | Sign-in, registration, workspace, and API-key connection. Logged-out home page and the Log in / Sign up dialogs checked in a headless browser against `pub-data.bdsa.io` on 2026-11-01; signed-in steps remain source-verified, not live-tested. |
| `docs/tutorials/create-a-collection.md` | New, from the live instance's served web client on 2026-11-01 | Collection creation and the private-by-default access rule. Flow not click-tested. |
| `docs/tutorials/create-a-folder.md` | New, from Girder `3.x-maintenance` UI source at `71e5fba` | Folder creation flow. Labels checked against the live instance's served web client on 2026-11-01; flow not click-tested. |
| `docs/tutorials/copy-an-item.md` | New, from Girder `3.x-maintenance` UI source at `71e5fba` | Pick-and-copy flow and the `copyItem` model behavior. Labels checked against the live instance's served web client on 2026-11-01; flow not click-tested. |
| `docs/tutorials/edit-metadata.md` | New, from Girder `3.x-maintenance` UI source at `71e5fba` | Simple and JSON metadata editing plus key validation rules. Labels checked against the live instance's served web client on 2026-11-01; flow not click-tested. |
| `docs/assets/tutorials/*.svg` | New | Schematics of the action bar, checked actions menu, and metadata panel. Not screenshots. |
| `docs/reference/rest-api.md` | New skeleton | Points at the Girder API reference. |
| `docs/reference/python-client.md` | New skeleton | Points at `girder-client` and the DSA CLI test. |
| `docs/reference/bdsa-react-components.md` | New skeleton | Deliberately does not invent props or APIs; the package location is unconfirmed. |
| `docs/release-notes.md` | New skeleton | Will aggregate release notes from DSA and companion repos. |
| `docs/contributing.md` | Upstream repo conventions | Contributor entry point for DSA and this docs repository. |

## Still to consolidate

These are known sources that are not yet represented here. Each should become a
page or merge into an existing page in a later slice.

- Upstream Jekyll pages: `docs/documentation/index.md` (the long tutorial and
  example list), `docs/migration.rst`, `docs/about/index.md`,
  `docs/demos-examples/index.md`, `docs/papers-publications/index.md`, and the
  success stories.
- HistomicsUI user and developer documentation, including the annotation and
  analysis task workflows.
- Girder user, administrator, and API documentation that DSA relies on.
- `bdsa-react-components` usage, once its repository and package are confirmed.
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
