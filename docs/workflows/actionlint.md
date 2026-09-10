# Actionlint

[← Back to README](../../README.md)

Lints GitHub Actions workflow YAML (`.github/workflows/*.yml`) with
[actionlint](https://github.com/rhysd/actionlint): syntax errors, expression
errors, and (via its shellcheck integration) shell issues inside `run:` steps.
Useful for this repo's own reusable workflows and for other repos' custom
actions, which typically still have workflows exercising/releasing them. Note:
actionlint only checks workflow files, not standalone `action.yml`/`action.yaml`
metadata.

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/actionlint.reusable.yml@v1
```

**Inputs:**
- `working_directory`: Directory to lint, i.e. where `.github/workflows` is discovered from (default: `.`)
- `actionlint_version`: Version of actionlint to install (default: `latest`)
- `ignore_patterns`: Newline-separated regex patterns for error messages to ignore (default: none)
