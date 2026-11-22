# With-Skill arm run records

Store one immutable run directory per run ID. Install or mount the exact Skill commit from the frozen environment lock.

Each run must include:
- `run-record.json` conforming to [run-record.schema.json](../../protocol/run-record.schema.json);
- original prompt and its SHA-256;
- transcript or approved transcript reference;
- Skill source commit, installation-manifest SHA-256, and loaded reference names;
- tool/command log;
- native outputs and their SHA-256;
- evaluation record.

The with-skill arm must record explicit Skill invocation. Do not silently use a moving `main` version.
