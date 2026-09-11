# Go Test

[← Back to README](../../README.md)

Runs `go test` (with race detector and coverage summary by default). Supports resolving
private AwareInc-org Go modules imported directly from source.

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/go-test.reusable.yml@v1
  with:
    working_directory: .
```

**Usage (with a private module dependency):**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/go-test.reusable.yml@v1
  with:
    private_modules: github.com/AwareInc-org/*
  secrets:
    PRIVATE_MODULES_TOKEN: ${{ secrets.DEVKIT_ACCESS_TOKEN }}
```

**Inputs:**
- `go_version`: Go version to set up, e.g. `1.22` or `stable` (default: `stable`)
- `working_directory`: Directory containing `go.mod` (default: `.`)
- `test_path`: Package path(s) to pass to `go test` (default: `./...`)
- `race`: Run tests with the race detector (default: `true`)
- `coverage`: Collect and print a coverage summary (default: `true`)
- `test_args`: Additional arguments passed through to `go test` (default: none)
- `private_modules`: Comma-separated `GOPRIVATE` patterns, e.g. `github.com/AwareInc-org/*` (default: none). Requires `PRIVATE_MODULES_TOKEN`.
