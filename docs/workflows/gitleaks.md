# Gitleaks

[← Back to README](../../README.md)

Scans for committed secrets (API keys, tokens, credentials) with
[gitleaks](https://github.com/gitleaks/gitleaks). Scans the full git history
by default — a secret introduced in an old commit and later removed is still
a leak — set `scan_git_history` to `false` to scan only the current working
tree instead.

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/gitleaks.reusable.yml@v1
```

**Usage (suppressing known findings with a baseline):**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/gitleaks.reusable.yml@v1
  with:
    baseline_path: .gitleaks-baseline.json
```

**Inputs:**
- `scan_git_history`: Scan the full git history, not just the current working tree (default: `true`)
- `gitleaks_version`: Version of gitleaks to install (default: `latest`)
- `config_path`: Path to a gitleaks config file (`.gitleaks.toml`) (default: none — gitleaks' own default rules/discovery)
- `baseline_path`: Path to a baseline report (from a prior gitleaks `--report-path` run) whose findings should be suppressed (default: none)
