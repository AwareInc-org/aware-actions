# Python Test

[← Back to README](../../README.md)

Installs a Python repo (editable) and runs its pytest suite. Has no built-in knowledge of any
specific repo -- callers whose code depends on another repo's source tree (rather than a
published package) supply that via `sibling_repos`.

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/pytest.reusable.yml@v1
  with:
    extras: dev
```

**Usage (with a sibling repo dependency):**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/pytest.reusable.yml@v1
  with:
    extras: dev
    sibling_repos: |
      AwareInc-org/aware-common-lib@main aware-common-lib AWARE_COMMON_LIB_DIR
  secrets:
    SIBLING_REPO_TOKEN: ${{ secrets.DEVKIT_ACCESS_TOKEN }}
```

**Inputs:**
- `python_version`: Python version to set up (default: `3.x`)
- `extras`: Optional-dependencies extras to install from this repo's own `pyproject.toml`, comma-separated (default: `dev`)
- `test_path`: Path(s) to pass to pytest (default: `tests/`)
- `pytest_args`: Additional arguments passed through to pytest (default: none)
- `sibling_repos`: Newline-separated `owner/repo@ref path [ENV_VAR_NAME]` entries to checkout and `pip install -e` before this repo's own install/tests (default: none)
