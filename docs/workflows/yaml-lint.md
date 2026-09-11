# YAML Lint

[← Back to README](../../README.md)

Lints YAML files with [yamllint](https://github.com/adrienverge/yamllint):
trailing whitespace, bad indentation, duplicate keys, and similar. Defaults
to a relaxed config rather than yamllint's own default ruleset, which is
noisy on real GitHub Actions workflow YAML: it warns on every file missing a
leading `---`, on the `on:` key (read as a YAML 1.1 boolean), and on
trailing `# comments` with only one space before them; an 80-column
line-length limit also flags most `description:` and pinned-`uses:` lines.
This workflow's own default disables `document-start`, `truthy`, and
`line-length`, and relaxes comment spacing to 1. Pass `config_path` for full
control instead.

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/yaml-lint.reusable.yml@v1
```

**Inputs:**
- `working_directory`: Directory to search recursively for YAML files (default: `.`)
- `yamllint_version`: Version of yamllint to install (default: `latest`)
- `config_path`: Path to a yamllint config file (default: none — the relaxed default described above)
