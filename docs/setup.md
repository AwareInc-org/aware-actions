# Setup

[← Back to README](../README.md)

## aware-devkit access

[Release](workflows/release.md) and [Verify Installer](workflows/verify-installer.md) access `aware-devkit`. Set up authentication:

1. Create a [GitHub Personal Access Token](https://github.com/settings/tokens/new) with `repo` scope
2. Add it as a secret in your calling repo: `DEVKIT_ACCESS_TOKEN`
3. Pass it when calling the workflows:

```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/release.reusable.yml@v1
  with:
    regenerate_installer: true
  secrets:
    DEVKIT_ACCESS_TOKEN: ${{ secrets.DEVKIT_ACCESS_TOKEN }}
```
