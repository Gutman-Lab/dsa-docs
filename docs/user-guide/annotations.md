# Annotation basics

HistomicsUI stores annotations as structured documents attached to an image
item. The model is small, but the vocabulary matters when you use the API or
share annotations between users.

## Annotation documents

An annotation document belongs to one item. It contains:

- A name and optional attributes.
- A list of **elements**.
- Optional metadata used by the interface, such as allowed style groups.

Each element is one shape: a point, rectangle, ellipse, circle, polygon, line,
or brush stroke. Elements also carry a style group name and their coordinates.

## Style groups

A style group defines how elements look: fill color, line color, line width,
and an optional pattern. Groups are configured per folder in a
`.histomicsui_config.yaml` file. The default group is named `default`.

Keeping style groups consistent across a study makes annotations easier to
review and compare. The draw panel and the annotation context menu both offer
the configured groups.

## Coordinate lists

DSA stores polygon and line geometry as coordinate lists. That format is easy
to exchange over the API, but analysis code often wants a mask image instead.
HistomicsTK includes helpers for converting between coordinate lists and mask
images, and for merging annotations produced by tiled analysis.

## Learn the controls

The viewer shortcuts for creating, selecting, editing, and combining
annotations are in [Mouse and keyboard controls](controls.md).

## Planned

A task-based annotation tutorial — create a project, define style groups, draw
and review annotations, and export the result — is planned for a later slice.
It will be verified against a running instance before it is published.
