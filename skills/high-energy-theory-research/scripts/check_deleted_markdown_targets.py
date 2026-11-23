#!/usr/bin/env python3
"""Report retained Markdown references to repository paths removed between two commits."""
from __future__ import annotations

import argparse
import json
import posixpath
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit


def git(repo: Path, *args: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True
    ).stdout


def revision(repo: Path, ref: str) -> str:
    return git(repo, "rev-parse", "--verify", "--end-of-options",
               f"{ref}^{{commit}}").decode("ascii").strip()


def tree(repo: Path, sha: str) -> dict[str, str]:
    files = {}
    for entry in git(repo, "ls-tree", "-rzt", sha).split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        mode = metadata.split(b" ", 1)[0].decode("ascii")
        files[name.decode("utf-8", errors="surrogateescape")] = mode
    return files


def local_target(source: str, href: str) -> str | None:
    try:
        parsed = urlsplit(href)
        path = unquote(parsed.path, errors="strict")
    except (UnicodeError, ValueError):
        return None
    if parsed.scheme or parsed.netloc or not path or path.startswith("/"):
        return None
    target = posixpath.normpath(posixpath.join(posixpath.dirname(source), path))
    if target in {".", ".."} or target.startswith("../"):
        return None
    return target


def destinations(tokens, block_line=None):
    for token in tokens:
        line = token.map[0] + 1 if token.map else block_line
        if token.type in {"link_open", "image"}:
            attr = "href" if token.type == "link_open" else "src"
            href = token.attrGet(attr)
            if href is not None:
                yield line, href
        if token.children:
            yield from destinations(token.children, line)


def check(repo: Path, base: str, head: str) -> dict:
    from markdown_it import MarkdownIt

    base, head = revision(repo, base), revision(repo, head)
    base_tree, head_tree = tree(repo, base), tree(repo, head)
    deleted = base_tree.keys() - head_tree.keys()
    parser = MarkdownIt("commonmark").enable("table")
    findings = []
    if deleted:
        for source, mode in sorted(head_tree.items()):
            if mode not in {"100644", "100755"} or not source.lower().endswith(".md"):
                continue
            raw = git(repo, "show", f"{head}:{source}")
            for line, href in destinations(parser.parse(raw.decode("utf-8-sig"))):
                target = local_target(source, href)
                if target in deleted:
                    findings.append({"source": source, "block_line": line,
                                     "destination": href, "deleted_path": target})
    return {"base": base, "head": head, "findings": findings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=Path.cwd(), type=Path)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", default="HEAD")
    args = parser.parse_args()
    try:
        report = check(args.repo, args.base, args.head)
    except ModuleNotFoundError as exc:
        if exc.name != "markdown_it":
            raise
        print(json.dumps({"error": "Install the optional markdown-it-py dependency."}))
        return 2
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        detail = exc.stderr.decode("utf-8", errors="replace").strip() if (
            isinstance(exc, subprocess.CalledProcessError) and exc.stderr
        ) else str(exc)
        print(json.dumps({"error": detail}))
        return 2
    print(json.dumps(report, indent=2))
    return 1 if report["findings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
