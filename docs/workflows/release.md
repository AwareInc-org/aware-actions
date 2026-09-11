# Release

[← Back to README](../../README.md)

Two-phase release: prepare (SemVer validation, version bump, release PR) → finalize (tag, GitHub release).

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/release.reusable.yml@v1
  with:
    bump_docker_version: true
    regenerate_installer: true
```

**Inputs:**
- `version`: SemVer (e.g., `1.2.3` or `1.2.3-rc1`)
- `bump_docker_version`: Stamp `docker_version` in version.json (default: `false`)
- `regenerate_installer`: Regenerate installer from config (default: `false`)
- `installer_config_path`: Path to config (default: `installer.config.yaml`)
- `devkit_ref`: aware-devkit ref for generation (default: `main`)

Accesses `aware-devkit` — see [Setup](../setup.md) for the required token.
