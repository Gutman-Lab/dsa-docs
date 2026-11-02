# Annotate a slide

This tutorial takes you from an open slide to a saved annotation you can find,
edit, and download. It uses the **Annotations** and **Draw** panels in
HistomicsUI.

!!! info "Verified status"

    The control labels, dialog fields, and shortcuts were checked against the
    HistomicsUI web client at commit
    [`75a9be6`](https://github.com/DigitalSlideArchive/HistomicsUI/commit/75a9be6)
    on 2026-11-01. They were **not click-tested on a writable slide** because
    this documentation slice had no writable test account. If your deployment
    differs, the source is authoritative. See
    [Annotation basics](../user-guide/annotations.md) for the underlying model.

## Before you start

- You can open a slide in the viewer. If not, start with
  [Upload and view your first slide](../get-started/first-slide.md).
- You have **write** access to the image item. Without it, the **New** button
  and the **Draw** panel are hidden.
- You know which style group you should use. If your study defines groups, ask
  the study owner. Otherwise use the default group.

## 1. Open the slide

Open the image item. HistomicsUI loads the image in the viewer with the
**Annotations** panel on the right. The **Draw** panel appears when you have
annotation access.

## 2. Create an annotation

1. In the **Annotations** panel, select **New** (the button with the plus icon).
   The keyboard shortcut is the space bar.
2. In the **Create annotation** dialog, enter a **Name**. The default is
   `Annotation <date and time>`; replace it with something meaningful, such as
   `Tumor region 1`.
3. Optionally add a **Description**.
4. Leave **Show on first load** off unless the annotation should be visible to
   everyone when the image opens.
5. Select **Save**.

The new annotation appears in the **Annotations** panel and becomes the active
annotation. The **Draw** panel title shows its name.

## 3. Choose a style group

In the **Draw** panel, open the style-group dropdown and select a group. The
colors and line width come from that group.

To create or change groups, select the gear button beside the dropdown. The
style-group editor lets you create, rename, restyle, import, export, and set the
default group. See [Annotation style groups](../user-guide/annotation-groups.md).

## 4. Draw an element

Select a tool and draw on the image:

| Tool | Shortcut | What to do |
| --- | --- | --- |
| **Rectangle** | `r` | Drag from one corner to the opposite corner |
| **Polygon** | `p` | Click each vertex; close the shape to finish |
| **Ellipse** | `i` | Drag to set the ellipse extent |
| **Circle** | `c` | Drag from the center outward |
| **Line** | `l` | Drag from start to end |
| **Point** | `o` | Click once |
| **Brush** | `b` | Paint a freehand stroke; set square or circle and a size in the brush dropdown |

For rectangles and ellipses, the small dropdown beside the tool offers
**Unconstrained**, **Fixed Aspect Ratio**, and **Fixed Size** with width and
height fields.

The element is added to the active annotation and saved automatically. The
spinner beside the **Annotations** title means a save is in progress.

## 5. Verify the result

- The element appears in the image with the group's colors.
- The annotation is listed in the **Annotations** panel under its style group.
- The panel's element count includes the new element.
- The eye icon toggles the annotation's visibility.

If the panel is collapsed, expand it. If the annotation is hidden, select the
eye icon or press `a` to show all annotations.

## 6. Edit or delete the element

Right-click the element. The context menu offers:

- **Remove group** — clears the element's group.
- The available style groups — move the element to another group.
- **Edit Shape** — adjust the geometry (`e`).
- **Edit Properties** — edit element-level values such as the label.
- **Delete** — remove the element.

To edit the annotation document itself, use the gear icon in the **Annotations**
panel. The **Edit annotation** dialog has **Name**, **Description**, **Show on
first load**, and a style section for point, line, and polygon elements.

## 7. Download a copy

In the **Annotations** panel, select the download icon beside the annotation.
The browser downloads the annotation's JSON document. Use this for a backup, for
an analysis script, or to attach the annotation to a paper trail.

## Troubleshooting

The symptom-first index covers style groups, autosave failures, export, and
annotations that are invisible after sharing:
[Troubleshooting and FAQ: annotation](../troubleshooting.md#annotation).

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| There is no **New** button | You do not have write access to the item, or you are not signed in | Sign in. Ask the item owner for write access if it is still missing. |
| There is no **Draw** panel | The image is not open in the viewer, or you lack annotation access | Open the image item itself, not a folder listing. Check your access. |
| The annotation does not appear in the list | The panel is collapsed or the annotation is hidden | Expand **Annotations**; press `a` to show all. |
| The element uses the wrong color | The active style group is different from the one you expected | Select the group in the **Draw** dropdown and redraw, or right-click the element and choose the correct group. |
| The **Draw** panel offers only a few groups | The annotation has an `allowed_groups` restriction | Use one of the listed groups, or edit the annotation metadata if you own it. See [Annotation style groups](../user-guide/annotation-groups.md). |
| Changes do not stick | The save failed or your session expired | Check the save spinner and the browser console; sign in again and retry. |

## Next

- [Annotation basics](../user-guide/annotations.md)
- [Annotation style groups](../user-guide/annotation-groups.md)
- [Run an analysis](run-an-analysis.md)
- [Mouse and keyboard controls](../user-guide/controls.md)
