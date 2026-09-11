# Trivy Config

[← Back to README](../../README.md)

Scans Terraform/OpenTofu configuration for security misconfigurations with
[`trivy config`](https://github.com/aquasecurity/trivy): public storage
buckets, open security groups, missing encryption, and similar. Complements
[Terraform Lint](terraform-lint.md), which only checks formatting and style
(tflint) — not security posture. Static HCL analysis only, so it needs no
cloud credentials, backend init, or real plan/apply. tfsec
(aquasecurity/tfsec) covered this same ground but is deprecated in favor of
Trivy.

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/trivy-config.reusable.yml@v1
  with:
    working_directory: modules
```

**Usage (ignoring specific checks):**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/trivy-config.reusable.yml@v1
  with:
    skip_checks: |
      AWS-0132
```

**Inputs:**
- `working_directory`: Directory to scan, checked recursively (default: `.`)
- `trivy_version`: Version of Trivy to install (default: `latest`)
- `severity`: Comma-separated severities that fail the job — `UNKNOWN`, `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` (default: `HIGH,CRITICAL`)
- `skip_checks`: Newline-separated check IDs to ignore (default: none)
