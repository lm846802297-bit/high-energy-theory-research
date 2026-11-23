#!/usr/bin/env python3
"""Check new Git paths against the central archive boundary.

This path check is not a scientific-content classifier. See
docs/governance/CENTRAL_ARCHIVE_BOUNDARY_CHECK.md for its scope.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


GUARDED_ROOTS = ("artifacts", "calculations", "research", "validation")
INFRASTRUCTURE_PREFIXES = (
    "validation/infrastructure-tests/",
    "validation/research-skill-benchmark/",
    "validation/skill-benchmark/",
    "validation/skill-module-evaluation-2026-11-22/",
    "validation/workflow-tests/",
)


def git(repo_root: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo_root), *args], capture_output=True, check=False,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(f"git {' '.join(args)} failed: {detail or 'no matching commit history'}")
    return result.stdout


def report_boundary(repo_root: Path, base_ref: str, head_ref: str) -> dict:
    base = git(repo_root, "rev-parse", "--verify", "--end-of-options",
               f"{base_ref}^{{commit}}").decode("ascii").strip()
    head = git(repo_root, "rev-parse", "--verify", "--end-of-options",
               f"{head_ref}^{{commit}}").decode("ascii").strip()
    bases = git(repo_root, "merge-base", "--all", base, head).decode("ascii").splitlines()
    if len(bases) != 1:
        raise ValueError("Expected a unique merge base; select a specific ancestor for --base.")
    merge_base = bases[0]

    # Don't let similarity detection hide a new path behind a rename or copy.
    # NUL termination also preserves non-ASCII, tabs, and newlines in filenames.
    raw = git(repo_root, "diff", "--no-renames", "--diff-filter=A",
              "--name-only", "-z", merge_base, head, "--")
    new_paths = [part.decode("utf-8", errors="surrogateescape")
                 for part in raw.split(b"\0") if part]
    blocked = sorted(
        path for path in new_paths
        if any(path == root or path.startswith(root + "/") for root in GUARDED_ROOTS)
        and not path.startswith(INFRASTRUCTURE_PREFIXES)
    )
    return {
        "base": base,
        "head": head,
        "merge_base": merge_base,
        "new_paths_checked": len(new_paths),
        "blocked_new_paths": blocked,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--base", required=True, help="Target branch or base commit")
    parser.add_argument("--head", default="HEAD", help="Topic branch or tested commit")
    args = parser.parse_args(argv)
    try:
        report = report_boundary(args.repo_root, args.base, args.head)
    except (OSError, ValueError) as error:
        print(f"Central archive boundary: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return int(bool(report["blocked_new_paths"]))


if __name__ == "__main__":
    raise SystemExit(main())
