# Central-repository project, schema, and migration governance

Load this reference only when the active repository is `high-energy-theory-research` or a downstream project explicitly adopts its central project registry and candidate-schema contract. These rules do not apply to unrelated repositories.

## Project and workstream selection

In the central source repository, consult `projects/README.md` and `projects/registry.yaml` before creating a research record. Identify the parent project and workstream rather than treating every calculation family as a top-level project. The current UV–EFT matching workstream belongs to axial-vector-model-building; do not register it as a separate top-level project.

The registry is navigation metadata, not a record in candidate Schema v1.4.3.7. To validate project/workstream IDs and declared local canonical paths, run:

~~~bash
python skills/high-energy-theory-research/scripts/validate_project_registry.py --registry projects/registry.yaml --repo-root .
~~~

Do not pass the navigation registry to `validate_project_records.py`. Use the structured-record validator only for a directory containing JSON/YAML records that follow the candidate record schemas. Neither validator establishes scientific correctness.

## Project record validation

**Central-repository-only tooling:** `validate_project_records.py` and `validate_project_registry.py` are maintained for the central `high-energy-theory-research` source checkout. The user-level Skill export contains these script files but does not contain the central candidate schema bundle or its `cross_record_validate.py` helper. Therefore, do not invoke these validators from the standalone user-level installation or assume they are available in another repository. For a downstream project that explicitly adopts the central candidate schema/registry contract, use a pinned, compatible central source checkout and pass the downstream project's record/registry paths and project root explicitly. Otherwise, follow that project's own validation tooling and schemas.

When a project stores structured research records as JSON or YAML **and explicitly adopts the central candidate schema bundle**, run the validator from the central source checkout against the project record directory:

~~~bash
python skills/high-energy-theory-research/scripts/validate_project_records.py path/to/project/records --project-root path/to/project
~~~

The record directory should contain only project record JSON/YAML files. The default schema directory is this repository's Schema v1.4.3.7 candidate bundle. The report checks declared schemas, mapped cross-record references, ID uniqueness, status/reason consistency, and local source/artifact paths. A clean report is a bounded software check; it does not certify a physics derivation, full state-machine coverage, or scientific acceptance.

## Migration safety

Treat schema migration as a separate, review-gated workflow. The bundled v1.3-to-v1.4 migration prototype is dry-run by default; even staging mode never commits or overwrites source records, and its report must keep `commit_allowed=false`.

For legacy `validation_ids`, resolve references only from the read-only source snapshot, using a unique primary ID within the same project. Map to `validation_plan_ids` only when the target record is a Validation Plan. Map to `validation_activity_ids` only when the target is a uniquely identified Validation Activity with `execution_status` in `in_progress`, `succeeded`, or `failed` and a non-empty `started_at`. Missing targets, duplicate IDs, project mismatches, unstarted activities, and unclear states remain unresolved; do not guess from the field name alone. An empty legacy list may be represented as two empty typed lists because it contains no references to classify.

The migration resolver does not implement transactional commit or rollback and does not recover a missing source-schema archive. Keep unresolved items visible, preserve source hashes, and do not treat a successful dry run as migration approval. Candidate Artifact decisions DD-ART-007 through DD-ART-010 remain pending until explicitly approved.
