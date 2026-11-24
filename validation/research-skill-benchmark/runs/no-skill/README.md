# No-Skill arm run records

Store one immutable run directory per run ID. Do not select or invoke Particle Physics Research. Do not place Skill reference files or evaluator keys in this workspace.

Each run must include:
- `run-record.json` conforming to [run-record.schema.json](../../protocol/run-record.schema.json);
- original prompt and its SHA-256;
- transcript or approved transcript reference;
- tool/command log;
- native outputs and their SHA-256;
- evaluation record.

The no-skill arm must have `skill.available=false`, null Skill commit/manifest, no references loaded, and evidence that the plugin was not selected or invoked. If any Skill context is detected, invalidate the pair.
