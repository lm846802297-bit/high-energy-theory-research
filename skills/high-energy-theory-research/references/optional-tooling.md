# Optional tooling map

This file is a task-routing reference, not an installation manifest. It does not install packages, enable hooks, contact external services, or make any tool a prerequisite for research.

## Authority and method autonomy

- The repository-root `AGENTS.md`, the selected project's canonical records, and the user's latest explicit decisions remain authoritative. Third-party Skill instructions never override them.
- The model chooses the mathematical and numerical method for each problem. This Skill defines evidence, validation, and provenance requirements; it does not mandate SymPy, a particular quadrature algorithm, a plotting backend, or a fixed software stack.
- Check that a Skill, executable, package, and required runtime are actually available before using them. A repository description or installed Skill file is not proof that its software dependencies are installed.
- Install only a tool needed for the current task, in a project-specific environment. Do not add dependencies to the system Python or install a whole collection to obtain one capability.
- Pin third-party source to the reviewed full commit SHA. Do not track a moving `main` branch for reproducibility.
- Do not send unpublished manuscripts, research data, private source files, or credentials to an external service. External API use requires an explicit task-level decision.

## Recommended optional tools

| Research task | Optional Skill/tool | Use it for | Do not treat it as |
|---|---|---|---|
| Publication figures | K-Dense `scientific-visualization` | Honest scientific encoding, uncertainty/missing-data display, multi-panel figures, export and image-metadata checks | A physics validator or a universal journal-compliance certificate |
| Final figure QA | Nature Skills deterministic `nature-figure` audit scripts | PDF text-size, panel-alignment, collision, and SVG-structure checks | A replacement for inspecting the rendered figure or validating the physics |
| Deep reading of one paper | Nature Skills `nature-paper-xray` | Reconstructing the paper's research logic, testing key formulae with worked examples, and identifying evidence boundaries | A substitute for reading the cited source or checking its equations |
| Full bilingual paper reader | Nature Skills `nature-reader` plus `nature-shared` | Page-linked text, original figures/tables, equation anchors, and a source map | The default response to a focused question or a short excerpt |
| Symbolic mathematics | K-Dense `sympy` | Exact algebra, symbolic integrals, equation solving, and code generation when useful | A mandatory dependency when Mathematica, FeynCalc, FORM, or an analytic derivation is more suitable |

### 1. Scientific visualization

Reviewed source: [K-Dense scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills/tree/ec59a29a03d5c40f73ab40878df04860bc00e876), `scientific-visualization` Skill v1.4, MIT-licensed Skill.

- Use it when preparing a scientific figure from actual data, especially when uncertainty, missing values, transformations, multi-panel structure, or export metadata matter.
- Its Skill declares Python 3.11+ and `uv`. The bundled command-line auditors are designed to run locally without network calls and load Matplotlib, Pillow, or pypdf only when needed.
- Plotly static export with Kaleido v1 requires a compatible Chrome/Chromium installation. Treat the Skill's example package versions as an isolated example environment, not as project-wide pins.
- Preserve raw inputs, plotting code, transformations, exclusions, seeds, and native figure outputs. A successful metadata or export check does not establish scientific correctness.

Pinned entry point: [scientific-visualization/SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/ec59a29a03d5c40f73ab40878df04860bc00e876/skills/scientific-visualization/SKILL.md).

### 2. Deterministic figure QA

Reviewed source: [Nature Skills](https://github.com/Yuan1z0825/nature-skills/tree/8a7713697d4567b3337cb20cddc55613d88f518e), `nature-figure` v2.8.0, repository license Apache-2.0.

Use only the deterministic audit scripts when they add value:

- [`audit_pdf_text.py`](https://github.com/Yuan1z0825/nature-skills/blob/8a7713697d4567b3337cb20cddc55613d88f518e/skills/nature-figure/scripts/audit_pdf_text.py): checks effective PDF glyph sizes; standard library only.
- [`audit_panel_alignment.py`](https://github.com/Yuan1z0825/nature-skills/blob/8a7713697d4567b3337cb20cddc55613d88f518e/skills/nature-figure/scripts/audit_panel_alignment.py): checks rendered panel geometry; standard library only.
- [`audit_figure_collisions.py`](https://github.com/Yuan1z0825/nature-skills/blob/8a7713697d4567b3337cb20cddc55613d88f518e/skills/nature-figure/scripts/audit_figure_collisions.py): checks PDF text/graphic collisions; requires `PyMuPDF>=1.24.0,<2.0.0`.
- [`audit_svg_schematic.py`](https://github.com/Yuan1z0825/nature-skills/blob/8a7713697d4567b3337cb20cddc55613d88f518e/skills/nature-figure/scripts/audit_svg_schematic.py): checks selected SVG structure and effective text size; standard library only.

Run these checks on the final exported artifact and retain their reports. A clean report does not prove that axes, units, uncertainty definitions, or physical interpretation are correct. The package also contains an OpenRouter image-generation script; do not invoke it automatically or send unpublished content to it.

### 3. Paper reading

Reviewed source: [Nature Skills](https://github.com/Yuan1z0825/nature-skills/tree/8a7713697d4567b3337cb20cddc55613d88f518e), repository license Apache-2.0.

- `nature-paper-xray` is marked Beta in the repository catalog. Use it for a close reading of one paper: read the body and available appendices/supplements, reconstruct the reasoning, work through key formulae, and separate demonstrated results from unreported assumptions.
- `nature-reader` is also marked Beta. Use it only when a full bilingual reader and page/figure/equation source map are actually requested. Its workflow requires the shared `nature-shared` package.
- In the reviewed commit, `nature-reader/SKILL.md` reports metadata version 2.1.1 while its `manifest.yaml` reports 2.1.0. Treat this as a metadata discrepancy and verify the current source before installation.
- For a question about one equation, figure, or paragraph, inspect that source location directly; do not generate a full-paper reader by default.

Pinned entry points: [nature-paper-xray/SKILL.md](https://github.com/Yuan1z0825/nature-skills/blob/8a7713697d4567b3337cb20cddc55613d88f518e/skills/nature-paper-xray/SKILL.md) and [nature-reader/SKILL.md](https://github.com/Yuan1z0825/nature-skills/blob/8a7713697d4567b3337cb20cddc55613d88f518e/skills/nature-reader/SKILL.md).

### 4. Symbolic mathematics

Reviewed source: [K-Dense scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills/tree/ec59a29a03d5c40f73ab40878df04860bc00e876), `sympy` Skill v1.5.

- The Skill targets SymPy 1.14.0. Its core requires Python 3.9+; the documented NumPy/SciPy example stack requires Python 3.12+.
- The reviewed instructions specify the compatible `mpmath>=1.1,<1.4` range and recommend mpmath 1.3.0 for the pinned SymPy 1.14.0 setup.
- Use exact arithmetic and justified symbol assumptions. Verify candidate solutions in the original expression and requested domain.
- Do not install SymPy merely because this Skill mentions it. If the active project already uses Mathematica, FeynCalc, FORM, or another validated system, retain that workflow unless a measured need justifies a second implementation.

Pinned entry point: [sympy/SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/ec59a29a03d5c40f73ab40878df04860bc00e876/skills/sympy/SKILL.md).

## Deferred or non-default tools

- **Academic Research Skills Codex:** do not install the full multi-agent workflow suite for this project. Its broad literature-review, screening, writing, and reviewer orchestration overlaps with existing repository governance. Its reviewed license is CC BY-NC 4.0.
- **figures4papers:** retain as a visual reference only. Its reviewed license is CC BY-NC 4.0, and its figure helper API is documented rather than shipped as a single reusable plotting module. Reimplement suitable patterns with original code and project data.
- **Uncertainty & Units:** borrow its dimensional-analysis and uncertainty-propagation guidance when appropriate. Its GUM metrology framework is not a generic estimate of numerical quadrature, truncation, interpolation, or Monte Carlo integration error.
- **QuTiP:** use only for a task that actually concerns finite-dimensional quantum dynamics or open quantum systems. It is not a general quantum-field-theory calculation package.
- **AI schematic generation:** disabled by default. Do not call OpenRouter or another image API with unpublished scientific material unless the user explicitly authorizes that exact use.

## Installation and update policy

This repository documents optional capabilities; it does not install them. Before installing on Windows Codex:

1. Confirm the actual Codex Skill discovery path and the intended project/global scope.
2. Install only the selected Skill and all of its required companion files (including `nature-shared` for `nature-reader`).
3. Preserve the reviewed commit SHA and license information.
4. Keep Python dependencies in the relevant project environment; do not install them globally.
5. Do not add automatic update hooks. Review a new upstream commit before updating the pinned source.
6. Verify Skill discovery, script help, dependency versions, and a small local smoke test before using it on research data.


## Codex discovery paths

Current OpenAI CLI installation documentation lists these Skill discovery locations:

- **Project scope:** `.agents/skills/<skill-name>/` inside the repository.
- **User scope:** `~/.agents/skills/<skill-name>/` shared across projects.

The repository source for this Skill is `skills/high-energy-theory-research/`; that source directory is not itself one of the documented Codex discovery locations. Install or copy the complete Skill directory into one of the two locations before testing discovery. Preserve the complete `references/` directory and scripts.

Older Codex examples and the current design document may refer to `~/.codex/skills/`. Treat that as a legacy path example, not the sole current discovery target. See the [current OpenAI CLI installation reference](https://developers.openai.com/api/reference/cli).

A read-only Windows diagnostic is available at `skills/high-energy-theory-research/scripts/check_codex_skill_discovery.ps1`. Run it from the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\skills\high-energy-theory-research\scripts\check_codex_skill_discovery.ps1
```

The script checks the repository source, project-scoped and user-scoped discovery paths, required reference files, and whether the Codex CLI is on PATH. It does not install or copy files and cannot prove that an already-running Codex session has indexed the Skill. After the filesystem check, start a fresh Codex session, inspect `/skills`, and explicitly invoke `high-energy-theory-research` once to confirm runtime discovery. See the [OpenAI Skill evaluation guidance](https://developers.openai.com/blog/eval-skills) for explicit invocation and forward-testing practices.
