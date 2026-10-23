# Project Registry

简体中文版本：[README.zh-CN.md](README.zh-CN.md)。

This directory is the navigation layer for the **High-Energy Theory Research** platform. It distinguishes a parent research project from its workstreams, Scientific Diff change records, individual computation runs, and physical claims.

## Registered projects

At present, this registry contains one confirmed top-level project and its known UV–EFT workstream. Other research topics are not added as top-level projects until their repository presence and parent-project relationship are established; this avoids guessing project boundaries.

The registry is maintained in [registry.yaml](registry.yaml). It is navigation metadata, **not** a normative Schema v1.4.3.7 record and is intentionally separate from the structured project-record validator. Validate its hierarchy and declared paths with [validate_project_registry.py](../skills/high-energy-theory-research/scripts/validate_project_registry.py). For the complete operating procedure, see the [User Guide](../docs/USER_GUIDE.md).

### Axial-vector model building

The top-level research project is **axial-vector-model-building**. The **vll-higgs-singlet-uv-eft** workstream is a branch/workstream *inside that project*, not an independent top-level project.

The workstream's existing records remain at their current paths while this registry is introduced:

- Main research record: [research/RC-001-vll-higgs-singlet-uv-eft.md](../research/RC-001-vll-higgs-singlet-uv-eft.md)
- Gauge-subgraph workstream record: [research/RC-001-gauge-subgraph-change-record.md](../research/RC-001-gauge-subgraph-change-record.md)
- Claim–evidence matrix: [research/RC-001-claim-evidence-matrix.md](../research/RC-001-claim-evidence-matrix.md)
- Shared project index for the currently active records: [research/README.md](../research/README.md)

No files have been moved, renamed, or reclassified by introducing this registry. In particular, the RC-001 identifier remains a research-change/record identifier; it is not the parent project ID.

See the [Phase A registry and migration pre-audit](../docs/PROJECT_REGISTRY_AUDIT.md) for the checks performed and the remaining migration gates.

## Identity and nesting rules

1. **Project** — a sustained research programme with its own scope and top-level status, e.g. axial-vector-model-building.
2. **Workstream** — a coherent branch of work inside a project, e.g. vll-higgs-singlet-uv-eft.
3. **Research change** — a traceable scientific change with a baseline, evidence, and downstream impact, e.g. RC-001.
4. **Run** — one execution with identified source revision, inputs, environment, and outputs. A run must not be inferred merely because a script or validation log exists.
5. **Claim** — a physical statement whose scope and evidence are tracked independently of project/work status, e.g. CL-015.

Do not create a new top-level project solely because a workstream has its own directory, manuscript section, calculation family, or Git branch. Create a separate project only when it has an independently meaningful research scope and ownership/lifecycle.

## Adding a project or workstream

1. Start from [templates/project-record.md](../templates/project-record.md).
2. Add the project/workstream to registry.yaml with a stable identifier and links to its canonical records.
3. Keep the registry descriptive and conservative: use unknown or omit optional metadata rather than inventing repository URLs, baselines, or status evidence.
4. Do not move existing research artifacts as part of registration.
5. Before any future file migration, audit Markdown links, schema path rules, validator assumptions, tests, scripts, and CI references; migrate one workstream at a time.
6. Keep software validation status separate from scientific validation status.

## Current implementation boundary

Phase A registers project hierarchy and provides a reusable project-record template only. It does not introduce a new normative schema, modify the candidate schema bundle, run an automatic migration, or certify any physics result.
