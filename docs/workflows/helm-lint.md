# Helm Lint

[← Back to README](../../README.md)

Lints Helm charts (`helm lint`) and confirms they render (`helm template`) using
their own default `values.yaml` plus any additional values files supplied.
Rendering with no overrides at all is the point: a chart that only works once
you pass `--set` or a values file doesn't ship usable defaults, which is one
of the most common mistakes in charts. Optionally validates the rendered
manifests against the Kubernetes API schema with
[kubeconform](https://github.com/yannh/kubeconform), catching malformed
resources that both `helm lint` and a successful render can miss (custom
resources without a known schema are skipped rather than failed). Every
directory under `chart_path` containing a `Chart.yaml` is discovered and
linted/rendered independently. Runs no install/upgrade against a real
cluster.

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/helm-lint.reusable.yml@v1
  with:
    chart_path: charts
```

**Usage (with additional values files per chart):**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/helm-lint.reusable.yml@v1
  with:
    chart_path: charts
    values_files: |
      ci/values-staging.yaml
      ci/values-prod.yaml
```

**Inputs:**
- `chart_path`: Directory to search recursively for Helm charts (default: `.`)
- `values_files`: Newline-separated additional values file(s) to render each chart against, relative to the chart's own directory (default: none — every chart is always rendered once with no overrides first)
- `helm_version`: Version of Helm to install (default: `latest`)
- `strict`: Run `helm lint` with `--strict` (default: `true`)
- `kubeconform`: Also validate rendered manifests against the Kubernetes API schema (default: `true`)
- `kubeconform_version`: Version of kubeconform to install (default: `latest`)
- `kubernetes_version`: Kubernetes version schema for kubeconform to validate against, e.g. `1.30.0` (default: kubeconform's own default, the `master` schema)
