# Python client

The `girder-client` package is the supported Python client for the Girder API
that DSA exposes. DSA's own CLI test script uses it, so the pattern below
matches the one in
[`devops/dsa/utils/cli_test.py`](https://github.com/DigitalSlideArchive/digital_slide_archive/blob/master/devops/dsa/utils/cli_test.py)
at commit `2e16b9a`.

## Install

```bash
pip install girder-client
```

## Connect and authenticate

```python
import girder_client

gc = girder_client.GirderClient(apiUrl="http://127.0.0.1:8080/api/v1")
gc.authenticate("admin", "password")
```

The `apiUrl` includes the `/api/v1` suffix. This is the default used by the
reference CLI test.

## Use it

Once authenticated, the client can list and create resources, upload files,
read annotations, and submit jobs. The Girder Python client documentation
covers the available methods:

- [Girder Python client](https://girder.readthedocs.io/en/stable/python-client.html)

## Status

This page covers installation and authentication only. A DSA-specific client
cookbook — upload a slide, find an item, run a task, and download a result —
is planned for a later slice.
