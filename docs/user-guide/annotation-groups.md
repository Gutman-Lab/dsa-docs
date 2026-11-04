# Annotation style groups

Style groups give annotations a consistent visual language. A group is a named
set of fill color, line color, line width, and pattern. Reviewers can then read
"pink outline" or "green fill" as a label instead of inspecting each element.

## Where groups are configured

Groups are defined in a `.histomicsui_config.yaml` file in a folder. DSA applies
the file to that folder, so different studies can use different palettes. If a
folder has no file, the instance's existing groups remain in effect.

A minimal file looks like this:

```yaml
---
annotationGroups:
  replaceGroups: false
  defaultGroup: default
  groups:
    - id: default
      fillColor: rgba(0,0,0,0)
      lineColor: rgb(0,0,0)
      lineWidth: 2
    - id: tumor
      label: Tumor
      fillColor: rgba(255, 0, 0, 0.25)
      lineColor: rgb(255, 0, 0)
      lineWidth: 2
    - id: stroma
      label: Stroma
      fillColor: rgba(0, 128, 0, 0.25)
      lineColor: rgb(0, 128, 0)
      lineWidth: 2
      hotkey: s
```

Key rules:

- `id` is required and is the value stored on each element.
- `replaceGroups: false` or omitting it merges the listed groups with existing
  groups and updates groups with the same name. `true` removes all existing
  groups first.
- `defaultGroup` names the group assigned to annotations that have no group.
- Colors are `rgb(r, g, b)` or `rgba(r, g, b, a)`, with channels from 0 to 255
  and alpha from 0 to 1.
- `lineWidth` is in pixels.
- `pattern` can be `none`, `circle`, `triangle`, `diamond`, `flower(number)`,
  `star(number)`, or `jack(number)`, where `number` is 1 to 16. Omitting it is
  the same as `none`.
- `hotkey` applies only while the folder's config file is in effect.

Hotkeys with modifiers use a separate block:

```yaml
---
hotkeys:
  - key: r
    ctrl: true
    alt: false
    action: group
    param: tumor
```

## Edit groups in the viewer

In the **Draw** panel, the style-group dropdown selects the group for new
elements. The gear button opens the style-group editor, where you can create,
rename, restyle, delete, import, export, reset, and set the default group.

Changing a group's style updates the legend used by the **Annotations** panel.
Existing elements keep the group name; their rendered colors follow the group
definition.

## Restrict an annotation to allowed groups

An annotation document can limit which groups its elements may use. Put an
`allowed_groups` key in the annotation's `attributes`:

```json
{
  "name": "restricted annotation",
  "attributes": {
    "allowed_groups": ["tumor", "stroma"]
  },
  "elements": []
}
```

For convenience when editing through the UI metadata editor, the value may also
be a JSON-stringified array:

```json
{
  "attributes": {
    "allowed_groups": "[\"tumor\", \"stroma\"]"
  }
}
```

When the restriction is present, the **Draw** panel and the annotation context
menu offer only the listed groups.

### Validation

`allowed_groups` is honored only when it is a non-empty array of non-empty
strings, or a string that parses as JSON into such an array. Any other value is
treated as **unrestricted**:

- a missing key,
- a non-array or non-JSON-array value,
- an unparseable string,
- an empty array, or
- an array with no valid strings.

Duplicate entries are ignored.

### Missing groups are created

If `allowed_groups` names a group that does not exist yet, HistomicsUI creates
it the first time the restriction is encountered. The new group copies the
default group's fill color, line color, line width, and pattern, and is
persisted immediately. This can happen from either the **Draw** panel or the
annotation context menu, whichever sees the restricted annotation first.

### Effect on the current selection

If the active style group is not allowed for the selected annotation, the
**Draw** panel switches to the first allowed group that exists. This prevents a
new element from silently using a group the annotation forbids.

## Verify a restriction

1. Create or select an annotation.
2. Add the `allowed_groups` attribute through the annotation metadata editor, or
   through the API.
3. Reopen the annotation. The **Draw** panel should list only the allowed groups.
4. Draw a new element and confirm its group is one of the allowed values.

If every group is still offered, check the value: an empty array, a malformed
JSON string, or a non-string entry makes the annotation unrestricted.

??? note "Source and version"

    This page is based on HistomicsUI's
    [`docs/config_options.rst`](https://github.com/DigitalSlideArchive/HistomicsUI/blob/master/docs/config_options.rst)
    and
    [`docs/annotation_group_restrictions.rst`](https://github.com/DigitalSlideArchive/HistomicsUI/blob/master/docs/annotation_group_restrictions.rst)
    at commit
    [`75a9be6`](https://github.com/DigitalSlideArchive/HistomicsUI/commit/75a9be6),
    plus the web client's `allowedGroups` utility. It is **source-verified, not
    live-tested** on a configured DSA instance in this documentation slice.
