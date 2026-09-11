# Kube Lint

[← Back to README](../../README.md)

Checks Kubernetes best practices with
[kube-linter](https://github.com/stackrox/kube-linter): missing resource
requests/limits, containers running as root, missing/mismatched probes,
`:latest` image tags, and similar. Complements [Helm Lint](helm-lint.md),
which only confirms a chart renders — it doesn't check what's inside the
rendered manifests. Accepts either a directory of raw Kubernetes YAML or a
Helm chart directory directly (kube-linter renders it internally with its
own `values.yaml`); a path containing multiple charts or manifest trees is
walked recursively in one pass. Runs no build/render/apply against a real
cluster.

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/kube-lint.reusable.yml@v1
  with:
    path: charts
```

**Usage (ignoring specific checks):**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/kube-lint.reusable.yml@v1
  with:
    exclude_checks: |
      unset-cpu-requirements
```

**Inputs:**
- `path`: Directory to lint — raw Kubernetes YAML, a Helm chart, or a tree containing several of either (default: `.`)
- `kube_linter_version`: Version of kube-linter to install (default: `latest`)
- `exclude_checks`: Newline-separated kube-linter check names to exclude (default: none)
