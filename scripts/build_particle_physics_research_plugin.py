#!/usr/bin/env python3
"""Build a deterministic Plugin Creator update archive for Particle Physics Research."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_PREFIX = "skills/high-energy-theory-research"
PLUGIN_SOURCE = ROOT / "packaging" / "particle-physics-research"
VERSION = "0.2.0"
REPOSITORY = "https://github.com/lm846802297-bit/high-energy-theory-research"
SOURCE_PR = REPOSITORY + "/pull/27"
REQUIRED_REFERENCES = (
    "task-router.md",
    "evidence-and-claim-gates.md",
    "source-and-version-audit.md",
    "symbolic-calculation.md",
    "numerical-scans-and-uncertainty.md",
    "scientific-figure-audit.md",
    "paper-reading.md",
    "optional-tooling.md",
    "central-repository-governance.md",
)


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def git_blob_sha1(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def build(output: Path) -> dict[str, object]:
    commit = git("rev-parse", "HEAD")
    tracked = git("ls-tree", "-r", "--name-only", commit, "--", SKILL_PREFIX).splitlines()
    if not tracked:
        raise SystemExit("No tracked Skill files found.")

    skill_files: dict[str, bytes] = {}
    source_records = []
    for relative_path in sorted(tracked):
        data = (ROOT / relative_path).read_bytes()
        skill_files[relative_path] = data
        source_records.append({
            "path": relative_path,
            "bytes": len(data),
            "git_blob": git_blob_sha1(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        })

    skill_text = skill_files[f"{SKILL_PREFIX}/SKILL.md"].decode("utf-8")
    if not skill_text.startswith("---\n"):
        raise SystemExit("Skill front matter is missing.")
    for reference in REQUIRED_REFERENCES:
        if f"{SKILL_PREFIX}/references/{reference}" not in skill_files:
            raise SystemExit(f"Missing required Skill reference: {reference}")

    plugin_manifest_path = PLUGIN_SOURCE / "plugin.json"
    overlay_path = PLUGIN_SOURCE / ".codex-plugin" / "plugin.json"
    plugin_manifest = json.loads(plugin_manifest_path.read_text(encoding="utf-8"))
    overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
    if plugin_manifest.get("name") != "particle-physics-research":
        raise SystemExit("Unexpected plugin name.")
    if plugin_manifest.get("version") != VERSION or overlay.get("version") != VERSION:
        raise SystemExit("Root and compatibility plugin manifests must both be version 0.2.0.")
    if overlay.get("name") != plugin_manifest.get("name"):
        raise SystemExit("Plugin compatibility overlay identity mismatch.")

    install_manifest = {
        "source_repository": REPOSITORY,
        "source_commit": commit,
        "source_pr": SOURCE_PR,
        "plugin_version": VERSION,
        "source_files": source_records,
    }
    skill_files[f"{SKILL_PREFIX}/skill-install-manifest.json"] = (
        json.dumps(install_manifest, ensure_ascii=False, indent=2) + "\n"
    ).encode("utf-8")

    package_files = {
        "plugin.json": plugin_manifest_path.read_bytes(),
        ".codex-plugin/plugin.json": overlay_path.read_bytes(),
        **skill_files,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path, data in sorted(package_files.items()):
            info = zipfile.ZipInfo(path, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)

    with zipfile.ZipFile(output, "r") as archive:
        names = sorted(archive.namelist())
        if names != sorted(package_files):
            raise SystemExit("Archive member inventory does not match the intended package.")
        for path, expected in package_files.items():
            if archive.read(path) != expected:
                raise SystemExit(f"Archive read-back mismatch: {path}")

    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    sidecar = output.with_suffix(output.suffix + ".sha256")
    sidecar.write_text(f"{digest}  {output.name}\n", encoding="ascii")
    return {
        "plugin": "particle-physics-research",
        "version": VERSION,
        "source_commit": commit,
        "source_file_count": len(source_records),
        "archive": str(output),
        "archive_bytes": output.stat().st_size,
        "archive_sha256": digest,
        "install_manifest": install_manifest,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
