# Bats Test

[← Back to README](../../README.md)

Runs a repo's [bats](https://github.com/bats-core/bats-core) suite -- unit tests for bash
functions, as opposed to [Shell Lint](shell-lint.md)'s static analysis. Best suited to pure(ish)
functions in sourced lib files: no network, filesystem side effects kept to `$BATS_TEST_TMPDIR`,
external commands faked rather than actually run.

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/bats-test.reusable.yml@v2
```

**Inputs:**
- `test_path`: Path/glob passed to `bats` (default: `tests/*.bats`)
