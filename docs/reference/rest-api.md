# REST API

DSA exposes the Girder REST API under `/api/v1` on the Girder server. A local
installation therefore serves its API at:

```text
http://localhost:8080/api/v1
```

The public demo serves the same API shape at:

```text
https://demo.kitware.com/histomicstk/api/v1
```

## What the API covers

The API manages the same resources as the web interface: users, groups,
collections, folders, items, files, metadata, annotations, jobs, and plugin
settings. HistomicsUI and Slicer CLI Web add their own routes on top of Girder's
core routes.

## Reference

Use the Girder API reference for route parameters, request bodies, and
authentication details:

- [Girder REST API documentation](https://girder.readthedocs.io/en/stable/api.html)
- [Girder Python client](https://girder.readthedocs.io/en/stable/python-client.html)

## Status

This page is a foundation entry, not a complete DSA-specific route reference.
A curated reference — listing the routes DSA users actually need, with verified
request and response examples — is planned for a later slice. Until then, the
Girder documentation is the authoritative source.
