# aware-actions

Reusable GitHub Actions for CI/CD workflows.

## Workflows

- [Docker Publish](docs/workflows/docker-publish.md) — Multi-architecture Docker image build and push to DockerHub
- [Release](docs/workflows/release.md) — Two-phase release: prepare (SemVer validation, version bump, release PR) → finalize (tag, GitHub release)
- [Verify Installer](docs/workflows/verify-installer.md) — Ensures `install-<product>.sh` matches its `installer.config.yaml`
- [Shell Lint](docs/workflows/shell-lint.md) — Lints shell scripts, PowerShell, bash 3.2 compatibility, and optional Windows batch files
- [Actionlint](docs/workflows/actionlint.md) — Lints GitHub Actions workflow YAML with actionlint
- [Check Requirements](docs/workflows/check-requirements.md) — Ensures `requirements*.txt` files are up to date with `pyproject.toml`
- [Python Test](docs/workflows/pytest.md) — Installs a Python repo (editable) and runs its pytest suite
- [Bats Test](docs/workflows/bats-test.md) — Runs a repo's bats suite, unit tests for bash functions
- [Go Test](docs/workflows/go-test.md) — Runs `go test` with race detector and coverage summary
- [OpenTofu Test](docs/workflows/tofu-test.md) — Runs OpenTofu unit tests against mocked providers
- [Terraform Lint](docs/workflows/terraform-lint.md) — Checks Terraform/OpenTofu formatting and static analysis
- [Terragrunt Lint](docs/workflows/terragrunt-lint.md) — Checks Terragrunt HCL formatting
- [Terragrunt Render](docs/workflows/terragrunt-render.md) — Confirms Terragrunt units render and flags dependency blocks missing mock_outputs
- [Helm Lint](docs/workflows/helm-lint.md) — Lints Helm charts and confirms they render with their own defaults, optionally validating output against the Kubernetes API schema

## Setup

See [docs/setup.md](docs/setup.md) for `aware-devkit` authentication, required by the Release and Verify Installer workflows.

## Utilities

**update-actions.py** — Updates all GitHub Actions to latest versions.

```bash
python3 update-actions.py --dry-run
python3 update-actions.py
```
