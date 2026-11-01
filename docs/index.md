# Digital Slide Archive documentation

The Digital Slide Archive (DSA) stores, manages, visualizes, and annotates large
whole-slide microscopy images. It combines a Girder-based data server, the
HistomicsUI viewer and annotation interface, and containerized analysis tasks
from HistomicsTK and other Slicer CLI Web tools.

This documentation site is being rebuilt in focused slices. The **Get Started**
path and the **controls reference** are ready to use. Other sections are
skeletons that point at the source material they will replace.

## Start here

<div class="grid cards" markdown>

-   **New to DSA?**

    Understand what the platform is and how its pieces fit together.

    [:material-arrow-right: What is DSA?](get-started/what-is-dsa.md)

-   **Want to look around first?**

    Open the public demo and explore a slide without installing anything.

    [:material-arrow-right: Try the demo](get-started/try-the-demo.md)

-   **Ready to install?**

    Run DSA on one machine with Docker Compose.

    [:material-arrow-right: Install on one machine](get-started/install.md)

-   **Already installed?**

    Upload a slide and open it in the viewer.

    [:material-arrow-right: Upload and view your first slide](get-started/first-slide.md)

</div>

## About this site

- This repository is a staging area for consolidating DSA information and
  tutorials in one place. Some pages replicate material that still lives
  upstream; each page records its source.
- The documentation source lives in
  [`Gutman-Lab/dsa-docs`](https://github.com/Gutman-Lab/dsa-docs). Build and
  link-check instructions are in the repository
  [`README.md`](https://github.com/Gutman-Lab/dsa-docs/blob/main/README.md), and
  [`SOURCES.md`](https://github.com/Gutman-Lab/dsa-docs/blob/main/SOURCES.md)
  tracks where each page came from and what is still queued.
- The site is built with MkDocs Material. Nothing here is published yet: the
  live marketing site remains the upstream Jekyll site.
