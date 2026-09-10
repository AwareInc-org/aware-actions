# Shell Lint

[← Back to README](../../README.md)

Lints shell scripts (shellcheck), PowerShell, bash 3.2 compatibility, and optional Windows batch files.

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/shell-lint.reusable.yml@v1
  with:
    check_batch_files: true
```

**Inputs:**
- `check_batch_files`: Run batch file check (default: `false`)
