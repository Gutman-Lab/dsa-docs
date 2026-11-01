# Contributing

Contributions to DSA, HistomicsUI, and the documentation are welcome. This page
covers the repository-level basics. Component repositories have their own
guides.

## Before you start

- Read [`README.rst`](https://github.com/DigitalSlideArchive/digital_slide_archive/blob/master/README.rst)
  for what the project is and where the deployment examples live.
- Read [`devops/dsa/README.rst`](https://github.com/DigitalSlideArchive/digital_slide_archive/blob/master/devops/dsa/README.rst)
  if your change affects the reference Docker Compose deployment.
- Search [existing issues](https://github.com/DigitalSlideArchive/digital_slide_archive/issues)
  and [discussions](https://github.com/DigitalSlideArchive/digital_slide_archive/discussions)
  before opening a new one.

## Set up pre-commit

The repository uses [pre-commit](https://pre-commit.com/) for whitespace, YAML,
Python, and spelling checks:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

Run `pre-commit run --all-files` before you push. CI and local hooks use the
same configuration in
[`.pre-commit-config.yaml`](https://github.com/DigitalSlideArchive/digital_slide_archive/blob/master/.pre-commit-config.yaml).

## Test changes to the deployment

Integration tests run against the Docker Compose stacks. The CircleCI
configuration starts `devops/dsa` or `devops/ver5`, waits for
`/api/v1/system/version`, and then runs the CLI test inside the Girder
container:

```bash
docker exec dsa-girder-1 bash -c \
  "python /opt/digital_slide_archive/devops/dsa/utils/cli_test.py dsarchive/histomicstk:latest --test --username=admin --password=password"
```

See
[`.circleci/config.yml`](https://github.com/DigitalSlideArchive/digital_slide_archive/blob/master/.circleci/config.yml)
for the complete matrix. Those commands were not executed in the documentation
environment because Docker was unavailable.

## Contribute documentation

The consolidated MkDocs source lives in
[`Gutman-Lab/dsa-docs`](https://github.com/Gutman-Lab/dsa-docs), under `docs/`.
Build and link-check it locally before opening a pull request:

```bash
python3 -m venv .venv-docs
. .venv-docs/bin/activate
pip install -r requirements.txt
mkdocs build --strict
python3 scripts/check_links.py site
```

Full instructions, including the pinned versions and output path, are in the
repository
[`README.md`](https://github.com/Gutman-Lab/dsa-docs/blob/main/README.md).
Record new pages in
[`SOURCES.md`](https://github.com/Gutman-Lab/dsa-docs/blob/main/SOURCES.md).

Guidelines:

- Prefer a task-based page over a feature list.
- Mark commands as verified or unverified. Never call an untested command
  "tested".
- Link to the upstream source when a fact comes from a README, compose file, or
  code path.
- Leave the upstream Jekyll site in the DSA repository untouched; it is still
  the live site. This repository is a separate build.

## Pull requests

- Keep a pull request focused. Separate documentation moves from behaviour
  changes.
- Describe what you ran and what you could not run.
- Do not include secrets, credentials, or private data.
- Do not change hosting, publishing, or release settings as part of a
  documentation change.
