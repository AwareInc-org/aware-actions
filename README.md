# aware-actions

Reusable GitHub Actions for CI/CD workflows.

## Workflows

### Docker Publish

Multi-architecture Docker image build and push to DockerHub.

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/docker-publish.reusable.yml@v1
  with:
    image: examplehub/example-cli
  secrets:
    DOCKERHUB_USERNAME: ${{ secrets.DOCKERHUB_USERNAME }}
    DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
```

**Inputs:**
- `image` (required): DockerHub repo (e.g., `examplehub/example-cli`)
- `dockerfile`: Path to Dockerfile (default: `docker/Dockerfile`)
- `context`: Build context (default: `.`)
- `platforms`: Comma-separated platforms (default: `linux/amd64,linux/arm64`)
- `tag`: Tag for manual dispatch (default: `test-build`)
- `update_latest`: Also tag `:latest` (default: `false`)

### Release

Two-phase release: prepare (SemVer validation, version bump, release PR) → finalize (tag, GitHub release).

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/release.reusable.yml@v1
  with:
    bump_docker_version: true
    regenerate_installer: true
```

**Inputs:**
- `version`: SemVer (e.g., `1.2.3` or `1.2.3-rc1`)
- `bump_docker_version`: Stamp `docker_version` in version.json (default: `false`)
- `regenerate_installer`: Regenerate installer from config (default: `false`)
- `installer_config_path`: Path to config (default: `installer.config.yaml`)
- `devkit_ref`: aware-devkit ref for generation (default: `main`)

### Verify Installer

Ensures `install-<product>.sh` matches its `installer.config.yaml`.

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/verify-installer.reusable.yml@v1
  with:
    config_path: installer.config.yaml
```

**Inputs:**
- `config_path`: Path to config (default: `installer.config.yaml`)
- `devkit_ref`: aware-devkit ref (default: `main`)

### Shell Lint

Lints shell scripts (shellcheck), PowerShell, bash 3.2 compatibility, and optional Windows batch files.

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/shell-lint.reusable.yml@v1
  with:
    check_batch_files: true
```

**Inputs:**
- `check_batch_files`: Run batch file check (default: `false`)

## Setup

Release and Verify Installer workflows access `aware-devkit`. Set up authentication:

1. Create a [GitHub Personal Access Token](https://github.com/settings/tokens/new) with `repo` scope
2. Add it as a secret in your calling repo: `DEVKIT_ACCESS_TOKEN`
3. Pass it when calling the workflows:

```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/release.reusable.yml@v1
  with:
    regenerate_installer: true
  secrets:
    DEVKIT_ACCESS_TOKEN: ${{ secrets.DEVKIT_ACCESS_TOKEN }}
```

## Utilities

**update-actions.py** — Updates all GitHub Actions to latest versions.

```bash
python3 update-actions.py --dry-run
python3 update-actions.py
```
