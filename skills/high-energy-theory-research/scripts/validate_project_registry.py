#!/usr/bin/env python3
"""Validate the navigation-only multi-project registry.

This is intentionally separate from validate_project_records.py: the project
registry is not a record type in the current candidate Schema v1.4.3.7 bundle.
The checker validates metadata structure, repository-local canonical paths, and
optional related_workstreams ID references. Relations may point across projects
and need not be reciprocated. It does not validate scientific content.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml
from yaml.constructor import ConstructorError


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_unique_mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ConstructorError(
                "while constructing a mapping", node.start_mark,
                f"duplicate key {key!r}", key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)

ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PROJECT_STATUSES = {"planned", "active", "blocked", "paused", "complete", "archived"}


def _inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
        return True
    except ValueError:
        return False


def validate_registry(registry_path: str | Path, repo_root: str | Path) -> dict:
    root = Path(repo_root).resolve()
    source = Path(registry_path)
    if not source.is_absolute():
        source = root / source
    source = source.resolve()
    errors: list[dict] = []
    warnings: list[dict] = []

    if not _inside(root, source):
        return {
            "validator": "project registry validator",
            "summary": {"projects": 0, "workstreams": 0, "errors": 1, "warnings": 0},
            "errors": [{"code": "REGISTRY_PATH_OUTSIDE_ROOT", "path": str(source)}],
            "warnings": [],
            "scope": ["registry metadata and canonical repository paths only"],
        }
    if not source.is_file():
        return {
            "validator": "project registry validator",
            "summary": {"projects": 0, "workstreams": 0, "errors": 1, "warnings": 0},
            "errors": [{"code": "REGISTRY_NOT_FOUND", "path": str(source)}],
            "warnings": [],
            "scope": ["registry metadata and canonical repository paths only"],
        }

    try:
        data = yaml.load(source.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except (OSError, yaml.YAMLError) as exc:
        return {
            "validator": "project registry validator",
            "summary": {"projects": 0, "workstreams": 0, "errors": 1, "warnings": 0},
            "errors": [{"code": "REGISTRY_PARSE_ERROR", "message": str(exc), "path": str(source)}],
            "warnings": [],
            "scope": ["registry metadata and canonical repository paths only"],
        }

    if not isinstance(data, dict):
        data = {}
        errors.append({"code": "REGISTRY_ROOT_NOT_MAPPING"})
    if data.get("registry_version") != 1:
        errors.append({"code": "REGISTRY_VERSION_INVALID", "value": data.get("registry_version")})
    projects = data.get("projects")
    if not isinstance(projects, list):
        errors.append({"code": "PROJECTS_NOT_LIST"})
        projects = []

    seen_projects: set[str] = set()
    seen_workstreams: set[str] = set()
    related_edges: list[tuple[str, str]] = []
    project_count = 0
    workstream_count = 0

    def check_id(value, code, path):
        if not isinstance(value, str) or not ID_PATTERN.fullmatch(value):
            errors.append({"code": code, "path": path, "value": value})
            return False
        return True

    def check_local_path(value, code, owner_path):
        if not isinstance(value, str) or not value.strip():
            errors.append({"code": code + "_INVALID", "owner": owner_path, "value": value})
            return
        candidate = (root / value).resolve()
        if not _inside(root, candidate):
            errors.append({"code": code + "_OUTSIDE_ROOT", "owner": owner_path, "value": value})
        elif not candidate.exists():
            errors.append({"code": code + "_MISSING", "owner": owner_path, "value": value})

    for index, project in enumerate(projects):
        ppath = f"projects[{index}]"
        if not isinstance(project, dict):
            errors.append({"code": "PROJECT_NOT_MAPPING", "path": ppath})
            continue
        project_count += 1
        pid = project.get("project_id")
        if check_id(pid, "PROJECT_ID_INVALID", ppath):
            if pid in seen_projects:
                errors.append({"code": "PROJECT_ID_DUPLICATE", "path": ppath, "project_id": pid})
            seen_projects.add(pid)
        if not isinstance(project.get("status"), str) or project.get("status") not in PROJECT_STATUSES:
            errors.append({"code": "PROJECT_STATUS_INVALID", "path": ppath, "status": project.get("status")})
        if not isinstance(project.get("title"), str) or not project["title"].strip():
            errors.append({"code": "PROJECT_TITLE_MISSING", "path": ppath})
        if not isinstance(project.get("scope"), str) or not project["scope"].strip():
            errors.append({"code": "PROJECT_SCOPE_MISSING", "path": ppath})

        workstreams = project.get("workstreams", [])
        if not isinstance(workstreams, list):
            errors.append({"code": "WORKSTREAMS_NOT_LIST", "path": ppath})
            workstreams = []
        for wi, workstream in enumerate(workstreams):
            wpath = f"{ppath}.workstreams[{wi}]"
            if not isinstance(workstream, dict):
                errors.append({"code": "WORKSTREAM_NOT_MAPPING", "path": wpath})
                continue
            workstream_count += 1
            wid = workstream.get("workstream_id")
            if check_id(wid, "WORKSTREAM_ID_INVALID", wpath):
                if wid in seen_workstreams or wid in seen_projects:
                    errors.append({"code": "WORKSTREAM_ID_DUPLICATE", "path": wpath, "workstream_id": wid})
                seen_workstreams.add(wid)
            if workstream.get("parent_project_id") != pid:
                errors.append({
                    "code": "WORKSTREAM_PARENT_MISMATCH",
                    "path": wpath,
                    "expected_parent_project_id": pid,
                    "actual_parent_project_id": workstream.get("parent_project_id"),
                })
            if not isinstance(workstream.get("status"), str) or workstream.get("status") not in PROJECT_STATUSES:
                errors.append({"code": "WORKSTREAM_STATUS_INVALID", "path": wpath, "status": workstream.get("status")})
            if not isinstance(workstream.get("title"), str) or not workstream["title"].strip():
                errors.append({"code": "WORKSTREAM_TITLE_MISSING", "path": wpath})
            if not isinstance(workstream.get("scope"), str) or not workstream["scope"].strip():
                errors.append({"code": "WORKSTREAM_SCOPE_MISSING", "path": wpath})
            canonical = workstream.get("canonical_records", [])
            if not isinstance(canonical, list):
                errors.append({"code": "CANONICAL_RECORDS_NOT_LIST", "path": wpath})
                canonical = []
            for ci, item in enumerate(canonical):
                check_local_path(item, "CANONICAL_RECORD", f"{wpath}.canonical_records[{ci}]")
            for key in ("claim_evidence_matrix", "index"):
                if key in workstream and workstream[key] is not None:
                    check_local_path(workstream[key], key.upper(), wpath)

            related = workstream.get("related_workstreams", [])
            relation_path = f"{wpath}.related_workstreams"
            if not isinstance(related, list):
                errors.append({"code": "RELATED_WORKSTREAMS_NOT_LIST", "path": relation_path})
                continue
            seen_targets: set[str] = set()
            for ri, target in enumerate(related):
                path = f"{relation_path}[{ri}]"
                if not check_id(target, "RELATED_WORKSTREAM_ID_INVALID", path):
                    continue
                if target in seen_targets:
                    errors.append({"code": "RELATED_WORKSTREAM_DUPLICATE", "path": path, "value": target})
                    continue
                seen_targets.add(target)
                if target == wid:
                    errors.append({"code": "RELATED_WORKSTREAM_SELF", "path": path, "value": target})
                    continue
                related_edges.append((path, target))

    # Resolve after reading every workstream so order and parent do not affect links.
    for path, target in related_edges:
        if target not in seen_workstreams:
            errors.append({"code": "RELATED_WORKSTREAM_UNKNOWN", "path": path, "value": target})

    collisions = seen_projects.intersection(seen_workstreams)
    for collision in sorted(collisions):
        errors.append({"code": "PROJECT_WORKSTREAM_ID_COLLISION", "id": collision})

    return {
        "validator": "project registry validator",
        "registry": str(source.relative_to(root)),
        "registry_status": data.get("registry_status"),
        "summary": {
            "projects": project_count,
            "workstreams": workstream_count,
            "errors": len(errors),
            "warnings": len(warnings),
        },
        "scope": [
            "YAML parsing and basic registry structure",
            "stable project/workstream ID format and uniqueness",
            "status/title/scope and parent-child consistency",
            "optional related_workstreams ID references",
            "existence and repository-root containment of declared canonical paths",
        ],
        "not_implemented": [
            "candidate JSON Schema validation",
            "automated migration of existing research files",
            "complete Markdown link checking or CI/script dependency analysis",
            "scientific correctness, independent physics validation, or claim acceptance",
        ],
        "errors": errors,
        "warnings": warnings,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate projects/registry.yaml navigation metadata and declared local paths."
    )
    parser.add_argument("--registry", default="projects/registry.yaml")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default=None, help="Optional JSON report path")
    args = parser.parse_args(argv)
    report = validate_registry(args.registry, args.repo_root)
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        output = Path(args.output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 1 if report["summary"]["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
