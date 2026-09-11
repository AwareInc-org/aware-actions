# Docker Lint

[← Back to README](../../README.md)

Lints every Dockerfile under `working_directory` with
[hadolint](https://github.com/hadolint/hadolint): unpinned base images,
unpinned/uncleaned apt packages, `ADD` vs `COPY`, shell-form
`CMD`/`ENTRYPOINT`, missing `USER`, and similar. Runs no build, so it needs
no Docker daemon or registry access.

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/docker-lint.reusable.yml@v1
  with:
    working_directory: docker
```

**Usage (ignoring specific rules):**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/docker-lint.reusable.yml@v1
  with:
    ignore_rules: |
      DL3008
      DL3009
```

**Inputs:**
- `working_directory`: Directory to search recursively for Dockerfiles (default: `.`)
- `hadolint_version`: Version of hadolint to install, e.g. `v2.15.1` (default: `latest`)
- `failure_threshold`: Minimum rule severity that fails the job — `error`, `warning`, `info`, `style`, `ignore`, or `none` (default: `warning`)
- `ignore_rules`: Newline-separated hadolint rule codes to ignore (default: none)
- `config_path`: Path to a hadolint config file (default: none — relies on hadolint's own `.hadolint.yaml` discovery)
