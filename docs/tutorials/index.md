# Tutorials

Tutorials are task-based walkthroughs. Each one starts from a working
installation or a reachable server, states what you need, and ends with a
result you can check.

## Everyday tasks

These tutorials cover the actions people need first. Connect, create a folder,
copy an item, and edit metadata were **click-tested with a signed-in account**
on <https://pub-data.bdsa.io/> on 2026-11-01, and the screenshots come from
that run. Create a collection is source-verified only: that instance restricts
self-service collection creation to administrators.

- [Connect to a DSA server](connect.md) — sign in through the browser, find your
  workspace, and optionally connect from a script with an API key.
- [Create a collection](create-a-collection.md) — start a shared data tree and
  set who can see it.
- [Create a folder](create-a-folder.md) — add a folder in your personal space,
  a collection, or another folder.
- [Share a collection or folder](share-a-collection.md) — grant a user or group
  the right role, make a folder public, and handle annotation access.
- [Copy an item](copy-an-item.md) — duplicate a slide and its metadata into
  another folder.
- [Edit metadata](edit-metadata.md) — add, change, and delete key/value metadata
  on items, folders, and collections.

## Viewer and annotation

- [Upload and view your first slide](../get-started/first-slide.md)
- [Annotate a slide](annotate-a-slide.md) — create an annotation, choose a style
  group, draw, edit, and download it.
- [Run an analysis](run-an-analysis.md) — start a containerized task on a slide
  or region and find its output.
- [Mouse and keyboard controls](../user-guide/controls.md)
- [Annotation basics](../user-guide/annotations.md)
- [Annotation style groups](../user-guide/annotation-groups.md)

`Annotate a slide` and `Run an analysis` are **source-verified** against
HistomicsUI at commit `75a9be6`, not click-tested on a writable slide. Their
pages state the limits.

## When something goes wrong

- [Troubleshooting and FAQ](../troubleshooting.md) — symptom-first fixes for
  installation, sign-in, viewing, upload, permissions, annotations, and analysis
  jobs.

## Planned tutorials

These will be written once they can be run against a current release and a
dedicated test instance.

- Set up a multi-user annotation review with a shared style-group palette.
- Convert annotations to masks and back with HistomicsTK.
- Back up and restore the Girder database and assetstore.

## Existing examples

The upstream site's
[Documentation & Examples](https://digitalslidearchive.github.io/digital_slide_archive/documentation/)
URL is now a redirect to the upstream MkDocs documentation. Its one linked demo
is already covered by [Try the demo](../get-started/try-the-demo.md). There is no
separate tutorial list there to copy.
