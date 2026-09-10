# Docker Publish

[← Back to README](../../README.md)

Multi-architecture Docker image build and push to DockerHub.

**Usage:**
```yaml
- uses: AwareInc-org/aware-actions/.github/workflows/docker-publish.reusable.yml@v1
  with:
    image: examplehub/example-cli
  secrets:
    DOCKERHUB_USERNAME: ${{ secrets.DOCKERHUB_USERNAME }}
    DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
```

**Inputs:**
- `image` (required): DockerHub repo (e.g., `examplehub/example-cli`)
- `dockerfile`: Path to Dockerfile (default: `docker/Dockerfile`)
- `context`: Build context (default: `.`)
- `platforms`: Comma-separated platforms (default: `linux/amd64,linux/arm64`)
- `tag`: Tag for manual dispatch (default: `test-build`)
- `update_latest`: Also tag `:latest` (default: `false`)
- `version_build_arg`: Name of a build-arg to receive the resolved version/tag, e.g. `VERSION` (default: none)
- `build_args`: Additional newline-separated `NAME=value` build args for the Dockerfile (default: none)
