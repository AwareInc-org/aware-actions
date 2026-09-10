#!/usr/bin/env python3
"""
Update GitHub Actions to their latest versions.

Scans all workflow files in .github/workflows, queries the GitHub API for the
latest release of each action, and updates workflow files to use the latest
versions. Supports dry-run mode for previewing changes before applying them.

Also updates pinned third-party install scripts referenced directly in `run:`
steps (e.g. a CLI tool's official download script fetched from
raw.githubusercontent.com), not just `uses:` Actions. A script reference is
recognized as a tracked pin when it looks like:

    https://raw.githubusercontent.com/<owner>/<repo>/<40-char-sha>/<path> ... # v<version>

with the version comment trailing on the same line. Any workflow following
that convention gets picked up automatically -- no per-tool changes needed
here.

Example:
    python3 update-actions.py --dry-run
    python3 update-actions.py
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple, NamedTuple
from urllib.request import urlopen, Request
from urllib.error import HTTPError

# Workflow YAML files are always a few KB; reject anything past this before
# scanning it for action references, bounding the match loop below.
MAX_WORKFLOW_FILE_SIZE = 1_048_576  # 1 MiB

class ActionVersion(NamedTuple):
    """Version info for a GitHub Action."""
    version: str  # e.g., "7.0.0" (without v)
    sha: str      # e.g., "11bd71901bbe5b1630ceea73d27597364c9af683"

# Matches a pinned raw.githubusercontent.com script reference with its version
# comment trailing on the same line, e.g.:
#   https://raw.githubusercontent.com/rhysd/actionlint/914e7df.../scripts/x.bash) "..." # v1.7.12
RAW_SCRIPT_PIN_RE = re.compile(
    r"raw\.githubusercontent\.com/([a-zA-Z0-9\-._]+)/([a-zA-Z0-9\-._]+)/([0-9a-fA-F]{40})/\S+"
    r".*?#\s*v([0-9]+(?:\.[0-9]+)*)\s*$",
    re.MULTILINE,
)

def fetch_latest_release(owner: str, repo: str) -> Optional[ActionVersion]:
    """
    Fetch the latest release version and commit SHA from GitHub API.

    Args:
        owner (str): GitHub organization or username.
        repo (str): Repository name.

    Returns:
        ActionVersion or None: Named tuple with version (without v) and full
                               commit SHA, or None if fetch fails.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    try:
        req = Request(url)
        req.add_header("Accept", "application/vnd.github.v3+json")
        with urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            tag = data.get("tag_name", "")
            version = tag.lstrip("v") if tag else None
            if not version:
                return None

            # Fetch the actual commit SHA for this tag
            sha_url = f"https://api.github.com/repos/{owner}/{repo}/git/refs/tags/{tag}"
            sha_req = Request(sha_url)
            sha_req.add_header("Accept", "application/vnd.github.v3+json")
            with urlopen(sha_req, timeout=10) as sha_response:
                sha_data = json.loads(sha_response.read().decode())
                sha = sha_data.get("object", {}).get("sha", "")
                if sha:
                    return ActionVersion(version=version, sha=sha)
            return None
    except HTTPError as e:
        if e.code == 404:
            print(f"Warning: Release not found for {owner}/{repo}", file=sys.stderr)
        else:
            print(f"Error fetching {owner}/{repo}: {e.code}", file=sys.stderr)
    except Exception as e:
        print(f"Error fetching {owner}/{repo}: {e}", file=sys.stderr)
    return None

def parse_action(action_ref: str) -> Tuple[str, str, str]:
    """
    Parse a GitHub action reference into components.

    Args:
        action_ref (str): Action reference like "actions/checkout@v4" or
                          "docker/build-push-action@v6".

    Returns:
        tuple: (owner, repo, version) tuple, with all None if parse fails.
    """
    match = re.match(r"^([^/]+)/([^@]+)@(.+)$", action_ref)
    if not match:
        return None, None, None
    return match.groups()

def get_latest_versions(workflow_dir: Path) -> Dict[str, ActionVersion]:
    """
    Scan workflow files and fetch latest versions for all actions.

    Scans all .yml files in the workflow directory, extracts all GitHub action
    references, and fetches the latest release version and SHA for each unique action.

    Args:
        workflow_dir (Path): Path to .github/workflows directory.

    Returns:
        dict: Mapping of action references (e.g. "actions/checkout@v4") to
              ActionVersion tuples with version and commit SHA.
    """
    actions = set()
    for workflow_file in workflow_dir.glob("*.yml"):
        with open(workflow_file, "r") as f:
            content = f.read()
            if len(content) > MAX_WORKFLOW_FILE_SIZE:
                print(f"Skipping {workflow_file.name}: exceeds {MAX_WORKFLOW_FILE_SIZE} byte limit")
                continue
            for match in re.finditer(
                r"uses:\s+([a-zA-Z0-9\-._]+/[a-zA-Z0-9\-._]+@[a-zA-Z0-9\-._#]+)", content
            ):
                actions.add(match.group(1))
    latest_versions = {}
    for action in sorted(actions):
        owner, repo, current_version = parse_action(action)
        if owner and repo:
            latest = fetch_latest_release(owner, repo)
            if latest:
                latest_versions[action] = latest
                print(f"✓ {owner}/{repo}: {current_version} → {latest.version} ({latest.sha[:7]}...)")
            else:
                print(f"✗ {owner}/{repo}: could not fetch latest version")
    return latest_versions

def get_latest_raw_script_versions(workflow_dir: Path) -> Dict[Tuple[str, str, str], ActionVersion]:
    """
    Scan workflow files for pinned raw.githubusercontent.com script references
    and fetch latest versions for each.

    A pin is recognized by RAW_SCRIPT_PIN_RE: a raw.githubusercontent.com URL
    with a 40-char commit SHA, followed later on the same line by a `# vX.Y.Z`
    comment recording the currently-pinned version. This mirrors the `uses:`
    convention but for third-party install scripts run directly in a `run:`
    step rather than invoked as an Action.

    Args:
        workflow_dir (Path): Path to .github/workflows directory.

    Returns:
        dict: Mapping of (owner, repo, current_sha) to ActionVersion tuples
              with the latest version and commit SHA.
    """
    pins: Dict[Tuple[str, str, str], str] = {}
    for workflow_file in workflow_dir.glob("*.yml"):
        with open(workflow_file, "r") as f:
            content = f.read()
        if len(content) > MAX_WORKFLOW_FILE_SIZE:
            continue
        for match in RAW_SCRIPT_PIN_RE.finditer(content):
            owner, repo, sha, version = match.groups()
            pins[(owner, repo, sha)] = version

    latest_versions = {}
    for (owner, repo, sha), current_version in sorted(pins.items()):
        latest = fetch_latest_release(owner, repo)
        if latest:
            latest_versions[(owner, repo, sha)] = latest
            print(f"✓ {owner}/{repo} (script pin): {current_version} → {latest.version} ({latest.sha[:7]}...)")
        else:
            print(f"✗ {owner}/{repo} (script pin): could not fetch latest version")
    return latest_versions

def update_raw_script_pins(workflow_dir: Path, latest_versions: Dict[Tuple[str, str, str], ActionVersion], dry_run: bool = False) -> int:
    """
    Update all workflow files with latest SHAs/versions for pinned raw script references.

    Args:
        workflow_dir (Path): Path to .github/workflows directory.
        latest_versions (dict): Mapping of (owner, repo, current_sha) to ActionVersion tuples.
        dry_run (bool): If True, print changes without modifying files.

    Returns:
        int: Number of files with changes (or would have changes in dry-run mode).
    """
    files_updated = 0
    for workflow_file in workflow_dir.glob("*.yml"):
        with open(workflow_file, "r") as f:
            original_content = f.read()
        if len(original_content) > MAX_WORKFLOW_FILE_SIZE:
            continue
        updated_content = original_content

        for (owner, repo, old_sha), latest in latest_versions.items():
            if old_sha == latest.sha or old_sha not in updated_content:
                continue
            updated_content = updated_content.replace(old_sha, latest.sha)
            updated_content = re.sub(
                rf"(raw\.githubusercontent\.com/{re.escape(owner)}/{re.escape(repo)}/{re.escape(latest.sha)}/\S+.*?#\s*v)[0-9]+(?:\.[0-9]+)*",
                rf"\g<1>{latest.version}",
                updated_content,
            )

        # Only count/report files whose content actually changed -- matching
        # a pattern doesn't imply the substitution altered anything (e.g. the
        # pin is already at latest).
        if updated_content == original_content:
            continue

        files_updated += 1
        if dry_run:
            print(f"\n[DRY RUN] Would update {workflow_file.name} (script pin)")
            for line_num, (old, new) in enumerate(
                zip(original_content.split("\n"), updated_content.split("\n")), 1
            ):
                if old != new:
                    print(f"  Line {line_num}: {old}")
                    print(f"           → {new}")
        else:
            with open(workflow_file, "w") as f:
                f.write(updated_content)
            print(f"\n✓ Updated {workflow_file.name} (script pin)")
    return files_updated

def update_workflow_files(workflow_dir: Path, latest_versions: Dict[str, ActionVersion], dry_run: bool = False) -> int:
    """
    Update all workflow files with latest action SHAs and versions.

    Replaces all action version/SHA references in workflow files with their
    latest commit SHAs (with version comments for readability). If dry_run is
    True, shows what would be changed without modifying files.

    Args:
        workflow_dir (Path): Path to .github/workflows directory.
        latest_versions (dict): Mapping of action references to ActionVersion tuples.
        dry_run (bool): If True, print changes without modifying files.
                        Defaults to False.

    Returns:
        int: Number of files with changes (or would have changes in dry-run mode).
    """
    files_updated = 0
    for workflow_file in workflow_dir.glob("*.yml"):
        with open(workflow_file, "r") as f:
            original_content = f.read()
        if len(original_content) > MAX_WORKFLOW_FILE_SIZE:
            print(f"Skipping {workflow_file.name}: exceeds {MAX_WORKFLOW_FILE_SIZE} byte limit")
            continue
        updated_content = original_content

        # Replace the old version with the new SHA-based pin
        for action_ref, latest_version_info in latest_versions.items():
            owner, repo, current_version = parse_action(action_ref)
            # Skip if already pinned to the latest commit SHA
            if current_version == latest_version_info.sha:
                continue
            old_pattern = re.compile(
                rf"{re.escape(owner)}/{re.escape(repo)}@{re.escape(current_version)}(?:\s*#[^\n]*)?"
            )
            new_pattern = f"{owner}/{repo}@{latest_version_info.sha} # v{latest_version_info.version}"
            updated_content = old_pattern.sub(new_pattern, updated_content)

        # Only count/report files whose content actually changed -- matching
        # a pattern doesn't imply the substitution altered anything (e.g. the
        # pin is already at latest).
        if updated_content == original_content:
            continue

        files_updated += 1
        if dry_run:
            print(f"\n[DRY RUN] Would update {workflow_file.name}")
            for line_num, (old, new) in enumerate(
                zip(original_content.split("\n"), updated_content.split("\n")), 1
            ):
                if old != new:
                    print(f"  Line {line_num}: {old}")
                    print(f"           → {new}")
        else:
            with open(workflow_file, "w") as f:
                f.write(updated_content)
            print(f"\n✓ Updated {workflow_file.name}")
    return files_updated

def main():
    """
    Parse arguments and orchestrate the update process.

    Returns:
        int: Exit code (0 on success, 1 on error).
    """
    parser = argparse.ArgumentParser(
        description="Update GitHub Actions to their latest versions"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without modifying files",
    )
    parser.add_argument(
        "--workflows-dir",
        type=Path,
        default=Path(".github/workflows"),
        help="Path to workflows directory (default: .github/workflows)",
    )
    args = parser.parse_args()

    # Validate workflows directory exists
    if not args.workflows_dir.exists():
        print(f"Error: Workflows directory not found: {args.workflows_dir}", file=sys.stderr)
        return 1

    # Fetch latest versions
    print("Fetching latest versions from GitHub API...\n")
    latest_versions = get_latest_versions(args.workflows_dir)
    latest_script_versions = get_latest_raw_script_versions(args.workflows_dir)
    if not latest_versions and not latest_script_versions:
        print("No actions found to update")
        return 0

    # Update workflows
    print(f"\nUpdating workflows in {args.workflows_dir}...")
    files_updated = 0
    if latest_versions:
        files_updated += update_workflow_files(args.workflows_dir, latest_versions, args.dry_run)
    if latest_script_versions:
        files_updated += update_raw_script_pins(args.workflows_dir, latest_script_versions, args.dry_run)
    if args.dry_run:
        print(f"\n[DRY RUN] Would update {files_updated} file(s)")
    else:
        print(f"\n✓ Updated {files_updated} file(s)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
