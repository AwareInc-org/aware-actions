# Terragrunt Render

[← Back to README](../../README.md)

Confirms every Terragrunt unit (a `terragrunt.hcl` with a `terraform` block)
under `working_directory` actually renders (`terragrunt render --all`), and
flags `dependency` blocks with no `mock_outputs` — the Terragrunt equivalent
of a chart shipping with no usable defaults, since a unit shaped that way
can't be planned before its dependency has ever been applied, or in CI with
no cloud credentials.

Pass/fail is decided by scanning Terragrunt's `ERROR` log lines, not the
process exit code: once a `dependency` block falls back to mock outputs
(expected in CI, where there's no real state to read), Terragrunt exits `0`
even when that fallback cascades into a genuine error elsewhere in the same
unit.

Unlike `terragrunt hcl validate` (deliberately avoided by
[Terragrunt Lint](terragrunt-lint.md) — see that file for why), reading a
dependency's outputs against an unreachable backend fails fast locally
instead of making a live network call. `timeout_minutes` still caps the step
as a backstop.

Needs outbound network access to fetch any unit whose `terraform.source` is a
remote (git/registry) module, the same as any `terraform init`-adjacent
command would.

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/terragrunt-render.reusable.yml@v1
  with:
    working_directory: live
```

**Inputs:**
- `working_directory`: Directory to search recursively for Terragrunt units (default: `.`)
- `terragrunt_version`: Terragrunt version to install (default: `latest`)
- `tf_binary`: Binary for terragrunt to drive, `tofu` or `terraform` (default: `tofu`)
- `tf_version`: Version of `tf_binary` to install (default: `latest`)
- `require_mock_outputs`: Fail (instead of warn) when a dependency block has no `mock_outputs` (default: `false`)
- `timeout_minutes`: Hard cap on the render step, as a backstop against an unexpected hang (default: `10`)
