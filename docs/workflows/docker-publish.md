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

**Recipe: auto-publish when a Release workflow (see [release.md](release.md))
merges.** The `release.reusable.yml` `finalize` job creates the GitHub
Release with a PAT, so its `release: published` event does reach a caller's
`release:`-triggered `docker-publish.yml` — but `tag`/`update_latest` must be
derived from the release event yourself; they aren't populated for you.
A caller wired for both `workflow_dispatch` (ad-hoc/scratch builds) and
`release: published` (real releases, including prereleases) typically looks
like:

```yaml
on:
  release:
    types: [published]
  workflow_dispatch:
    inputs:
      tag:
        default: 'test-build'
      update_latest:
        type: boolean
        default: false

jobs:
  publish:
    uses: AwareInc-org/aware-actions/.github/workflows/docker-publish.reusable.yml@v2
    with:
      image: examplehub/example-cli
      tag: ${{ github.event_name == 'workflow_dispatch' && inputs.tag || github.event.release.tag_name }}
      update_latest: ${{ github.event_name == 'workflow_dispatch' && inputs.update_latest || (github.event_name == 'release' && !github.event.release.prerelease) }}
    secrets: inherit
```

The `!github.event.release.prerelease` clause is what keeps an RC
(`1.5.0-rc1`, published as a GitHub prerelease per [release.md](release.md))
from ever updating `:latest` — it still gets its own correctly-tagged image,
just without touching the tag other consumers pull by default.
