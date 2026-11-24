# With-Skill arm run records

Store one immutable run directory per run ID. Select the installed Particle Physics Research plugin, version 0.1.0, pinned to the exact Skill commit from the frozen environment lock. Explicitly invoke `@Particle Physics Research` and load only the task-specific reference.

Each run must include:
- `run-record.json` conforming to [run-record.schema.json](../../protocol/run-record.schema.json);
- original prompt and its SHA-256;
- transcript or approved transcript reference;
- Skill source commit, installation-manifest SHA-256, and loaded reference names;
- tool/command log;
- native outputs and their SHA-256;
- evaluation record.

The with-skill arm must record explicit Skill invocation. Do not silently use a moving `main` version.
