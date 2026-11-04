# Annotation basics

An annotation is a structured drawing attached to one image item: a region of
interest, a set of nuclei, a review comment, or the output of an analysis. This
page explains the model and the controls you use every day. For a step-by-step
walkthrough, see [Annotate a slide](../tutorials/annotate-a-slide.md).

## Annotation documents

An annotation document belongs to one item. It contains:

- A **name** and optional **description**.
- A **visibility** flag used when the image first loads.
- A list of **elements**.
- Optional attributes, including a `allowed_groups` style restriction.

Each element is one shape: a point, rectangle, ellipse, circle, polygon, line,
or brush stroke. Elements carry a style group name and their coordinates.

Annotations are saved to the server as you edit them. The small spinner beside
the **Annotations** panel title means a save is in progress; you do not need a
page-level Save button after drawing. If saves fail or an annotation is not
visible to a collaborator, see
[Troubleshooting and FAQ](../troubleshooting.md#annotation).

## The two panels you need

### Annotations

The **Annotations** panel lists the documents on the current image, grouped by
style group. Use it to:

- show or hide all annotations (`a`),
- show or hide one annotation or one group with the eye icons,
- change the annotation and fill opacity with the two sliders,
- select annotations by region,
- create a new annotation with **New**,
- edit annotation metadata with the gear icon,
- delete an annotation with the **×** icon, and
- download an annotation as JSON.

**New** opens the **Create annotation** dialog. Give the annotation a **Name**
and optional **Description**, choose whether it is shown on first load, and
select **Save**.

### Draw

The **Draw** panel is where you add elements to the selected annotation. The
style-group dropdown at the top selects which group new elements belong to; the
gear button opens the style-group editor. The tools are:

| Tool | Shortcut | What it draws |
| --- | --- | --- |
| **Point** | `o` | A single point |
| **Rectangle** | `r` | A rectangle; the dropdown can fix the aspect ratio or size |
| **Ellipse** | `i` | An ellipse; the same fixed-shape options apply |
| **Circle** | `c` | A circle |
| **Polygon** | `p` | A closed polygon, point by point |
| **Line** | `l` | A line |
| **Brush** | `b` | A freehand stroke; square or circle, with a pixel size |

The **Sort By** control orders elements by **Label**, **Group**, **Shape**, or
**Count**. The panel footer shows the element count for the selected annotation.

## Draw and edit elements

1. Select an annotation in the **Annotations** panel, or create one with
   **New**.
2. Choose a style group and a drawing tool in the **Draw** panel.
3. Draw on the image. The new element is added to the selected annotation and
   saved automatically.
4. To change an existing element, right-click it. The context menu offers
   **Remove group**, the available style groups, **Edit Shape**, **Edit
   Properties**, and **Delete**.
5. To change an annotation's name, description, visibility, or style, use the
   gear icon in the **Annotations** panel. The **Edit annotation** dialog has
   the same fields as **Create annotation**, plus a style section for point,
   line, and polygon elements.

Use **Edit Properties** for element-level metadata such as a label. Use the
annotation dialog for document-level metadata.

## Style groups

A style group defines how elements look: fill color, line color, line width,
and an optional pattern. Groups are configured per folder, and the default group
is named `default`. The draw panel and the annotation context menu both offer
the configured groups.

Keeping groups consistent across a study makes annotations easier to review and
compare. An annotation can also restrict which groups its elements may use; see
[Annotation style groups](annotation-groups.md) for the configuration format and
the `allowed_groups` rule.

## Coordinate lists

DSA stores polygon and line geometry as coordinate lists. That format is easy
to exchange over the API, but analysis code often wants a mask image instead.
HistomicsTK includes helpers for converting between coordinate lists and mask
images, and for merging annotations produced by tiled analysis.

Downloading an annotation from the **Annotations** panel produces the same JSON
document that the API returns.

## Annotations and metadata from jobs

Analysis tasks can add annotations and metadata to an existing image. HistomicsUI
ingests an uploaded file that carries a `reference` record when the reference
contains an `identifier` and at least one of `fileId` or `itemId`:

- An identifier ending in `ItemMetadata` sets metadata on the associated item.
- An identifier ending in `AnnotationFile` loads the file as annotations on the
  associated item.

This is how a HistomicTK task returns nuclei boundaries or other results. The
job output naming convention is described in
[Run an analysis](../tutorials/run-an-analysis.md).

## Learn the controls

The viewer shortcuts for creating, selecting, editing, and combining
annotations are in [Mouse and keyboard controls](controls.md).

## Next

- [Annotate a slide](../tutorials/annotate-a-slide.md)
- [Annotation style groups](annotation-groups.md)
- [Run an analysis](../tutorials/run-an-analysis.md)

??? note "Source and version"

    The labels, shortcuts, and behavior on this page were checked against the
    HistomicsUI web client at commit
    [`75a9be6`](https://github.com/DigitalSlideArchive/HistomicsUI/commit/75a9be6)
    on 2026-11-01. This page was **not** click-tested on a writable slide in
    this documentation slice, so treat the source as authoritative if your
    deployment differs. The coverage of the underlying controls is also on
    [Mouse and keyboard controls](controls.md).
