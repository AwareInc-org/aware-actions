# Verify Installer

[← Back to README](../../README.md)

Ensures `install-<product>.sh` matches its `installer.config.yaml`.

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/verify-installer.reusable.yml@v1
  with:
    config_path: installer.config.yaml
```

**Inputs:**
- `config_path`: Path to config (default: `installer.config.yaml`)
- `devkit_ref`: aware-devkit ref (default: `main`)

Accesses `aware-devkit` — see [Setup](../setup.md) for the required token.
