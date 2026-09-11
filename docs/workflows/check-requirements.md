# Check Requirements

[← Back to README](../../README.md)

Ensures `requirements*.txt` files are up to date with `pyproject.toml`.

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/check-requirements.reusable.yml@v1
  with:
    gen_script_path: scripts/gen-requirements.py
    requirements_files: |
      requirements.txt
      requirements-dev.txt
      requirements-docker.txt
```

**Inputs:**
- `gen_script_path`: Path to the requirements generation script (default: `scripts/gen-requirements.py`)
- `pyproject_path`: Path to `pyproject.toml` (default: `pyproject.toml`)
- `requirements_files`: Newline-separated list of requirements files to check (default: `requirements.txt`)
- `python_version`: Python version to use for generation (default: `3.x`)
