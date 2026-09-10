# OpenTofu Test

[← Back to README](../../README.md)

Runs OpenTofu unit tests (`tofu test -recursive`) on modules using mocked providers. Tests
are self-contained with no cloud credentials or real resources needed.

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/tofu-test.reusable.yml@v1
  with:
    working_directory: modules
```

**Inputs:**
- `tofu_version`: Version of OpenTofu to install (default: `latest`)
- `working_directory`: Directory to test, searched recursively for `.tftest.hcl` files (default: `.`)
- `test_filter`: Filter tests by name, passed to `tofu test -filter` (default: none)
