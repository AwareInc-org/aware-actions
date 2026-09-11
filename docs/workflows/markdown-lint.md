# Markdown Lint

[← Back to README](../../README.md)

Lints Markdown files with
[markdownlint-cli](https://github.com/igorshubovych/markdownlint-cli):
multiple H1s, trailing heading punctuation, hard tabs, and similar. Defaults
to a relaxed config rather than markdownlint's own default ruleset: MD013
(line-length) is constant noise on prose-heavy READMEs, and MD031/MD032
(blank lines required around fenced code blocks/lists) fire on the common
"Label:\n\`\`\`" and "Label:\n- item" doc style used throughout this repo's
own docs. Pass `config_path` for full control instead.

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/markdown-lint.reusable.yml@v1
```

**Inputs:**
- `working_directory`: Directory to search recursively for Markdown files (default: `.`)
- `markdownlint_version`: Version of markdownlint-cli to install (default: `latest`)
- `config_path`: Path to a markdownlint config file (default: none — the relaxed default described above)
