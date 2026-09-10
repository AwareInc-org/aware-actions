# Terraform Lint

[← Back to README](../../README.md)

Checks Terraform/OpenTofu formatting (`fmt -check`) and static analysis (`tflint`). Runs no
init/plan/apply, so it needs no cloud credentials.

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/terraform-lint.reusable.yml@v1
  with:
    working_directory: modules
```

**Inputs:**
- `working_directory`: Directory to lint, checked recursively (default: `.`)
- `tf_binary`: Binary to use for the fmt check, `tofu` or `terraform` (default: `tofu`)
- `tf_version`: Version of `tf_binary` to install (default: `latest`)
- `tflint_version`: Version of tflint to install (default: `latest`)
- `minimum_failure_severity`: Minimum tflint issue severity that fails the job — `error`, `warning`, or `notice` (default: `warning`)
