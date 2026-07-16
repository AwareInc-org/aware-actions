#!/usr/bin/env python3
"""
Update GitHub Actions to their latest versions.

Scans all workflow files in .github/workflows, queries the GitHub API for the
latest release of each action, and updates workflow files to use the latest
versions. Supports dry-run mode for previewing changes before applying them.

Example:
    python3 update-actions.py --dry-run
    python3 update-actions.py
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple
from urllib.request import urlopen, Request
from urllib.error import HTTPError

def fetch_latest_release(owner: str, repo: str) -> Optional[str]:
    """
    Fetch the latest release version from GitHub API.

    Args:
        owner (str): GitHub organization or username.
        repo (str): Repository name.

    Returns:
        str or None: Latest version tag with leading 'v' removed, or None if
                     the fetch fails or release is not found.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    try:
        req = Request(url)
        req.add_header("Accept", "application/vnd.github.v3+json")
        with urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            tag = data.get("tag_name", "")
            version = tag.lstrip("v") if tag else None
            return version
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

def get_latest_versions(workflow_dir: Path) -> Dict[str, str]:
    """
    Scan workflow files and fetch latest versions for all actions.

    Scans all .yml files in the workflow directory, extracts all GitHub action
    references, and fetches the latest release version for each unique action.

    Args:
        workflow_dir (Path): Path to .github/workflows directory.

    Returns:
        dict: Mapping of action references (e.g. "actions/checkout@v4") to
              their latest version numbers (e.g. "7.0.0").
    """
    actions = set()
    for workflow_file in workflow_dir.glob("*.yml"):
        with open(workflow_file, "r") as f:
            content = f.read()
            for match in re.finditer(
                r"uses:\s+([a-zA-Z0-9\-._]+/[a-zA-Z0-9\-._]+@[a-zA-Z0-9\-._]+)", content
            ):
                actions.add(match.group(1))
    latest_versions = {}
    for action in sorted(actions):
        owner, repo, current_version = parse_action(action)
        if owner and repo:
            latest = fetch_latest_release(owner, repo)
            if latest:
                latest_versions[action] = latest
                print(f"✓ {owner}/{repo}: {current_version} → {latest}")
            else:
                print(f"✗ {owner}/{repo}: could not fetch latest version")
    return latest_versions

def update_workflow_files(workflow_dir: Path, latest_versions: Dict[str, str], dry_run: bool = False) -> int:
    """
    Update all workflow files with latest action versions.

    Replaces all action version references in workflow files with their latest
    versions. If dry_run is True, shows what would be changed without modifying
    files. Otherwise, writes changes directly to files.

    Args:
        workflow_dir (Path): Path to .github/workflows directory.
        latest_versions (dict): Mapping of action references to latest versions.
        dry_run (bool): If True, print changes without modifying files.
                        Defaults to False.

    Returns:
        int: Number of files with changes (or would have changes in dry-run mode).
    """
    files_updated = 0
    for workflow_file in workflow_dir.glob("*.yml"):
        with open(workflow_file, "r") as f:
            original_content = f.read()
        updated_content = original_content
        made_changes = False

        # Replace the old version with the new one
        for action_ref, latest_version in latest_versions.items():
            owner, repo, current_version = parse_action(action_ref)
            if current_version == latest_version:
                continue
            old_pattern = f"{owner}/{repo}@{current_version}"
            new_pattern = f"{owner}/{repo}@{latest_version}"
            if old_pattern in updated_content:
                updated_content = updated_content.replace(old_pattern, new_pattern)
                made_changes = True

        # Either apply or show the diff
        if made_changes:
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
    if not latest_versions:
        print("No actions found to update")
        return 0

    # Update workflows
    print(f"\nUpdating workflows in {args.workflows_dir}...")
    files_updated = update_workflow_files(args.workflows_dir, latest_versions, args.dry_run)
    if args.dry_run:
        print(f"\n[DRY RUN] Would update {files_updated} file(s)")
    else:
        print(f"\n✓ Updated {files_updated} file(s)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
