# Terragrunt Lint

[← Back to README](../../README.md)

Checks Terragrunt HCL formatting (`terragrunt hcl format --check`). Deliberately does not run
`terragrunt hcl validate` -- it was found to hang indefinitely against real live/ configs,
apparently while resolving backend/provider state.

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/terragrunt-lint.reusable.yml@v1
  with:
    working_directory: live
```

**Inputs:**
- `working_directory`: Directory to check, checked recursively (default: `.`)
- `terragrunt_version`: Terragrunt version to install, e.g. `v1.1.3`, or `latest` (default: `latest`)
