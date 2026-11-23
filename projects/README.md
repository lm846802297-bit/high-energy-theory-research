# Project Registry

简体中文版本：[README.zh-CN.md](README.zh-CN.md)。

This directory is the navigation layer for the **High-Energy Theory Research** platform. It distinguishes a parent research project from its workstreams, Scientific Diff change records, individual computation runs, and physical claims.

## Registered projects

At present, this registry contains one confirmed top-level project and its registered workstreams. Other research topics are not added as top-level projects until their repository presence and parent-project relationship are established; this avoids guessing project boundaries.

The registry is maintained in [registry.yaml](registry.yaml). It is navigation metadata, **not** a normative Schema v1.4.3.7 record and is intentionally separate from the structured project-record validator. Validate its hierarchy and declared local paths with [validate_project_registry.py](../skills/high-energy-theory-research/scripts/validate_project_registry.py). External repository URLs are navigation references, not local canonical paths. For the complete operating procedure, see the [User Guide](../docs/USER_GUIDE.md).

### Axial-vector model building

The top-level research project is **axial-vector-model-building**. It currently contains two registered workstreams:

- **vll-higgs-singlet-uv-eft** — UV–EFT matching and associated dimension-six gauge corrections.
- **manuscript-review-response** — referee-comment analysis, response-letter development, manuscript diffs, and coordination of the supporting physics checks.

The **vll-higgs-singlet-uv-eft** workstream is part of the parent project, not an independent top-level project. Its migration destination is [axial-vector-review-response](https://github.com/lm846802297-bit/axial-vector-review-response), with a [commit-pinned Phase 1 archive](https://github.com/lm846802297-bit/axial-vector-review-response/tree/e1f8a557daec93864f8ba2ed14e9946516e158ed/research/vll-higgs-singlet-uv-eft) verified on the destination migration branch. It is not integrated into the destination's `main`, and the historical v66 archive is inventoried rather than transferred. This notice does not authorize source retirement.

Until that verification, the existing RC-001 records and links stay in place:

- Main research record: [research/RC-001-vll-higgs-singlet-uv-eft.md](../research/RC-001-vll-higgs-singlet-uv-eft.md)
- Gauge-subgraph workstream record: [research/RC-001-gauge-subgraph-change-record.md](../research/RC-001-gauge-subgraph-change-record.md)
- Claim–evidence matrix: [research/RC-001-claim-evidence-matrix.md](../research/RC-001-claim-evidence-matrix.md)
- Shared project index for the currently active records: [research/README.md](../research/README.md)

#### Manuscript review and revision

The **manuscript-review-response** workstream is maintained in its own repository: [axial-vector-review-response](https://github.com/lm846802297-bit/axial-vector-review-response). Start with its [reading guide](https://github.com/lm846802297-bit/axial-vector-review-response/blob/main/README-%E5%85%88%E8%AF%BB%E8%BF%99%E9%87%8C.md).

That repository retains the submitted manuscript, referee report, consolidated review analyses, neutrino-sector charge analysis, one-loop mixing review, and manuscript-revision materials. It remains the source of those files; this registration does not copy or move them into the workbench.

The workstream is related to **vll-higgs-singlet-uv-eft**, but it does not duplicate RC-001 or replace its calculation and claim–evidence records. The registry's status summary preserves unresolved research questions; pending checks must not be described as completed until their evidence is recorded.

No files have been moved, renamed, or reclassified by this registration. In particular, the RC-001 identifier remains a research-change/record identifier; it is not the parent project ID.

See the [Phase A registry and migration pre-audit](../docs/PROJECT_REGISTRY_AUDIT.md) for the checks performed and the remaining migration gates.

## Identity and nesting rules

1. **Project** — a sustained research programme with its own scope and top-level status, e.g. axial-vector-model-building.
2. **Workstream** — a coherent branch of work inside a project, e.g. vll-higgs-singlet-uv-eft or manuscript-review-response.
3. **Research change** — a traceable scientific change with a baseline, evidence, and downstream impact, e.g. RC-001.
4. **Run** — one execution with identified source revision, inputs, environment, and outputs. A run must not be inferred merely because a script or validation log exists.
5. **Claim** — a physical statement whose scope and evidence are tracked independently of project/work status, e.g. CL-015.

Do not create a new top-level project solely because a workstream has its own directory, manuscript section, calculation family, or Git branch. Create a separate project only when it has an independently meaningful research scope and ownership/lifecycle.

## Adding a project or workstream

1. Start from [templates/project-record.md](../templates/project-record.md).
2. Add the project/workstream to registry.yaml with a stable identifier and links to its canonical records or external repository entry point.
3. Keep the registry descriptive and conservative: use unknown or omit optional metadata rather than inventing repository URLs, baselines, or status evidence.
4. Do not move existing research artifacts as part of registration.
5. Before any future file migration, audit Markdown links, schema path rules, validator assumptions, tests, scripts, and CI references; migrate one workstream at a time.
6. Keep software validation status separate from scientific validation status.

## Current implementation boundary

The registry is navigation metadata. It does not introduce a new normative schema, modify the candidate schema bundle, automatically migrate files, or certify any physics result. Cross-repository links identify where work is maintained; they do not imply that external artifacts have been copied, validated, or accepted scientifically.
