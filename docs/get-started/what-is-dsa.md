# What is DSA?

The Digital Slide Archive (DSA) is an open-source platform for storing,
managing, visualizing, and annotating large microscopy images. It is designed
for whole-slide digital pathology, but the same machinery works for other
large, tiled image formats.

DSA is not a single application. It is a set of services and plugins that run
together:

| Piece | What it does |
| --- | --- |
| [Girder](https://girder.readthedocs.io/) | Asset and user management, permissions, and the HTTP API. |
| [large_image](https://github.com/girder/large_image) | Reads many slide formats as multi-resolution tiles. |
| [HistomicsUI](https://github.com/DigitalSlideArchive/HistomicsUI) | The slide viewer, annotation tools, and analysis panels. |
| [Slicer CLI Web](https://github.com/girder/slicer_cli_web) | Runs containerized analysis tasks from the UI and the API. |
| [HistomicsTK](https://github.com/DigitalSlideArchive/HistomicsTK) | A collection of pathology image-analysis algorithms. |
| MongoDB | Stores users, items, metadata, and annotations. |
| Girder Worker and RabbitMQ | Queue and run analysis jobs. |
| Memcached | Caches tile data for faster viewing. |

## What you can do with it

- Organize images in collections, folders, and items, with per-user and
  per-group access control.
- Store files on a local filesystem or in external assetstores such as Amazon
  S3.
- View and navigate whole-slide images in a browser.
- Draw, edit, and review annotations, including multi-user annotation studies.
- Run analysis tasks on whole images or selected regions, on one machine or
  across worker machines.
- Drive all of the above through the REST API and the Python client.

## How the pieces are deployed

The common deployment is a single computer running five containers: Girder,
MongoDB, Girder Worker, RabbitMQ, and Memcached. Analysis tasks start additional
short-lived containers. For more computing power, you can run workers on other
machines while the main server keeps the database and assetstore.

See [System Overview](../system-overview.md) for diagrams of both layouts.

## Ways to run DSA

- **Use the public demo** to explore the interface: [Try the demo](try-the-demo.md).
- **Install on one machine** with Docker Compose: [Install on one machine](install.md).
- **Scale out** with external workers, Kubernetes, or Apptainer. The repository
  contains reference deployments under
  [`devops/`](https://github.com/DigitalSlideArchive/digital_slide_archive/tree/master/devops);
  this slice documents the single-machine Docker Compose path only.

## Next

- [Try the demo](try-the-demo.md)
- [Install on one machine](install.md)
