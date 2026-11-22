# No-Skill arm run records

Store one immutable run directory per run ID. Do not place the shared Skill or evaluator keys in this workspace.

Each run must include:
- `run-record.json` conforming to [run-record.schema.json](../../protocol/run-record.schema.json);
- original prompt and its SHA-256;
- transcript or approved transcript reference;
- tool/command log;
- native outputs and their SHA-256;
- evaluation record.

The no-skill arm must have `skill.available=false`, null Skill commit/manifest, and an explicit record that the Skill was not accessible in the workspace.
