# Run an analysis

HistomicsUI can run containerized analysis tasks on a whole slide or on a
selected region. The tasks appear in the **Analyses** menu when a DSA
administrator has registered Slicer CLI Web Docker images. This tutorial covers
starting a task and finding its result.

!!! info "Verified status"

    This page is based on the HistomicsUI web client at commit
    [`75a9be6`](https://github.com/DigitalSlideArchive/HistomicsUI/commit/75a9be6)
    and its
    [`docs/slicer_cli_plugins.rst`](https://github.com/DigitalSlideArchive/HistomicsUI/blob/master/docs/slicer_cli_plugins.rst).
    It is **source-verified, not live-tested** in this documentation slice. The
    available tasks, their parameters, and their output names come from the
    installed images, so your menus will differ from the examples here.

## Before you start

- You can open a slide in the viewer.
- Your account can create jobs. If you cannot, ask an administrator.
- The instance has at least one Slicer CLI Web task registered. Without one,
  the **Analyses** menu is hidden.

The tasks are packaged as Docker images. A typical installation registers
`dsarchive/histomicstk:latest`, which provides nuclei detection, stain
separation, positive pixel counting, and related algorithms.

## 1. Open the slide

Open the image item in HistomicsUI. The analysis tools apply to the image that
is currently open.

## 2. Choose a task

Open the **Analyses** menu in the viewer header. The menu is organized by image
name, then image version, then algorithm. Select the algorithm you want.

The menu is built from the tasks the server reports. If a task is missing, it is
not installed or not visible to your account.

## 3. Fill in the task panel

Selecting an algorithm opens its input panel. The controls are generated from
the task's Slicer Execution Model XML, so each task has its own fields. Common
inputs include:

- the input image (usually filled in from the open slide),
- an analysis region, and
- algorithm-specific thresholds, channels, or output options.

If the task accepts a region, use the region selector to draw a rectangle or
polygon on the image, or choose the whole image where the task offers that
option.

## 4. Submit the job

Use the panel's submit control to queue the job. HistomicsUI reports
**Analysis job submitted.** and expands the jobs panel.

Jobs run on the server or on a worker. The browser does not need to stay open
for the job to finish, but you do need to return to the image to see results
that are attached to it.

## 5. Find the result

When the job finishes, its output is attached according to the task's output
names:

- An output whose name ends in `AnnotationFile` becomes an annotation document
  on the image, usually visible in the **Annotations** panel.
- An output whose name ends in `ItemMetadata` becomes metadata on the item.

Open the **Annotations** panel or the item's **Metadata** section to check. Job
status and logs are in the jobs panel.

## Troubleshooting

For worker configuration, queued jobs, failed containers, and missing outputs in
one place, see
[Troubleshooting and FAQ: analysis jobs](../troubleshooting.md#analysis-jobs).

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| The **Analyses** menu is missing | No Slicer CLI Web task is registered, or the image is not open | Ask an administrator to register a Docker image; open the image item itself. |
| The task panel has no submit control | You lack job permission, or a required input is missing | Fill the required fields; ask the administrator about job creation permission. |
| The job stays queued | No worker is available, or the queue is backed up | Check the jobs panel and ask the administrator to inspect the worker. |
| The job finishes but no annotation appears | The output name does not end in `AnnotationFile`, or the result was written elsewhere | Read the job outputs and the task documentation; check the item's metadata and files. |
| The task fails immediately | The Docker image is missing, or its XML does not match its command line | Ask the administrator to test the image with `--list_cli` and `--xml`. |

## For task authors

A task image must support:

```bash
docker run {image/name} --list_cli
docker run {image/name} {algorithm} --xml
```

The first command returns the available algorithms as JSON; the second returns
the Slicer Execution Model XML. The XML describes the inputs and outputs that
the panel renders. Output names ending in `AnnotationFile` or `ItemMetadata`
receive the automatic ingestion described above. The full schema is in
[HistomicsUI's Slicer CLI Web documentation](https://github.com/DigitalSlideArchive/HistomicsUI/blob/master/docs/slicer_cli_plugins.rst).

## Next

- [Annotate a slide](annotate-a-slide.md)
- [Annotation basics](../user-guide/annotations.md)
- [Mouse and keyboard controls](../user-guide/controls.md)
