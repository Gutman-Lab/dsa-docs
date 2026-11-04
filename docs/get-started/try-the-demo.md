# Try the demo

The quickest way to see DSA is the public demo instance hosted by Kitware:

<https://demo.kitware.com/histomicstk/>

The link above opens a sample collection. From there you can:

- Browse the collection and folder tree.
- Open a slide in HistomicsUI.
- Pan, zoom, and rotate the image.
- Open the analysis panel to see the tasks that are available.
- Try the annotation tools, if your account has permission to edit the demo
  data.

!!! warning "The demo is a shared public instance"

    Do not upload private, regulated, or otherwise sensitive data to the demo.
    Other users can see what is stored there, and the instance may be reset.

## What you are looking at

The demo runs the same components as a local installation: Girder serves the
API and the data, HistomicsUI provides the viewer and annotation tools, and
Slicer CLI Web exposes analysis tasks. It is a full DSA instance, not a static
screenshot.

## Next

- Want your own instance? [Install on one machine](install.md).
- Want to understand the parts? [What is DSA?](what-is-dsa.md).

## Verified status

On 2026-11-01 the demo homepage returned HTTP 200, and its version endpoint
reported:

```json
{"release": "3.2.18.dev2+g339bcdfe6"}
```

That tells you the demo is reachable, not that every feature is available to
anonymous users. Some actions require an account or edit permission.
