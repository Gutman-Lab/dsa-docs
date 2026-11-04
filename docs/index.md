# Digital Slide Archive documentation

The Digital Slide Archive (DSA) stores, manages, visualizes, and annotates large
whole-slide microscopy images. It combines a Girder-based data server, the
HistomicsUI viewer and annotation interface, and containerized analysis tasks
from HistomicsTK and other Slicer CLI Web tools.

This documentation site is being rebuilt in focused slices. The **Get Started**
path, the **task tutorials**, and the **controls reference** are ready to use.
Some reference sections are still skeletons that point at the source material
they will replace.

## Start here

<div class="grid cards" markdown>

-   **New to DSA?**

    Understand what the platform is and how its pieces fit together.

    [:material-arrow-right: What is DSA?](get-started/what-is-dsa.md)

-   **Want to look around first?**

    Open the public demo and explore a slide without installing anything.

    [:material-arrow-right: Try the demo](get-started/try-the-demo.md)

-   **Ready to install?**

    Run DSA on one machine with Docker Compose. The verified Ubuntu 24.04
    walkthrough covers the DSA 5 stack with screenshots.

    [:material-arrow-right: Install on one machine](get-started/install.md)

    [:material-arrow-right: Ubuntu 24.04 walkthrough](get-started/install-ubuntu-24-04.md)

-   **Already installed?**

    Upload a slide and open it in the viewer.

    [:material-arrow-right: Upload and view your first slide](get-started/first-slide.md)

</div>

## Everyday tutorials

Short, task-based walkthroughs for the actions people need first:

- [Connect to a DSA server](tutorials/connect.md)
- [Create a collection](tutorials/create-a-collection.md)
- [Create a folder](tutorials/create-a-folder.md)
- [Copy an item](tutorials/copy-an-item.md)
- [Edit metadata](tutorials/edit-metadata.md)
- [Annotate a slide](tutorials/annotate-a-slide.md)
- [Run an analysis](tutorials/run-an-analysis.md)

## Reference and help

- [User guide](user-guide/index.md) — viewer controls, annotations, style
  groups, and permissions.
- [System overview](system-overview.md) — single-computer and
  distributed-worker layouts.
- [REST API cookbook](reference/rest-api.md) and
  [Python client](reference/python-client.md) — drive DSA from scripts.
- [Troubleshooting and FAQ](troubleshooting.md) — fixes for install, sign-in,
  viewing, upload, permissions, annotations, and analysis jobs.

## BDSA-specific documentation

GutmanLab/BDSA additions to DSA stay on this site for now, so everything remains
linkable from this landing page. More BDSA-specific guides will be added here as
they are written.

- [UI components (bdsa-react-components)](reference/bdsa-react-components.md) —
  the shared React component library used by BDSA front ends.

## Project background

- [About the project](about.md) — history, license, funding, and community.
- [Release and upgrade notes](release-notes.md) — what changed in the current
  date-stamped image, how to upgrade, and how to roll back.
- [Success stories](success-stories.md) — collaborative annotation and TCGA.
- [Papers and publications](papers-publications.md) — work that uses DSA and
  its components.
- [Migration guide](migration.md) — moving from `deploy_docker.py` or Girder 2.

## About this site

- This repository is a staging area for consolidating DSA information and
  tutorials in one place. Some pages replicate material that still lives
  upstream; each page records its source and version in a collapsible note at
  the bottom.
- The documentation source lives in
  [`Gutman-Lab/dsa-docs`](https://github.com/Gutman-Lab/dsa-docs). Build and
  link-check instructions are in the repository
  [`README.md`](https://github.com/Gutman-Lab/dsa-docs/blob/main/README.md), and
  [`SOURCES.md`](https://github.com/Gutman-Lab/dsa-docs/blob/main/SOURCES.md)
  tracks where each page came from and what is still queued.
- The site is built with MkDocs Material and published from `main` at
  <https://gutman-lab.github.io/dsa-docs/>. The upstream project website
  remains the Jekyll site under `DigitalSlideArchive/digital_slide_archive`;
  this preview is the consolidation area, not a replacement for it.
