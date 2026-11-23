# RCRPS v1.0.1 Formal Adoption Record

**Decision:** Adopt the Structured Research Result Data Standard v1.0.1  
**Decision owner:** Project owner  
**Adoption date / effective date:** 2026-11-23  
**Canonical repository:** `lm846802297-bit/high-energy-theory-research`  
**Implementation PR:** [#32](https://github.com/lm846802297-bit/high-energy-theory-research/pull/32)  
**Integrated commit:** `cd65712c54b4b298e6131f1045d89b795d3d7084`

## 1. Decision

RCRPS v1.0.1 is formally adopted as the current central structured-result standard. It supersedes v1.0.0 for new substantial numerical, simulation, parameter-scan, and computational-validation runs beginning on the effective date.

The normative implementation consists of:

- `docs/STRUCTURED_RESULT_DATA_STANDARD_v1.0.1.md` and its Chinese counterpart;
- `docs/schemas/research-result-record-v1.0.1.schema.json`;
- `docs/schemas/validate_result_records.py`, whose default schema is v1.0.1.

The v1.0.1 schema is a compatibility superset: it validates existing v1.0.0 records under their original requirements and requires `execution.source_control` only for v1.0.1 `run_manifest` records.

## 2. Effective requirements

1. Every new v1.0.1 `run_manifest` must contain all 14 required `execution.source_control` fields.
2. PR executions must distinguish the actual checkout from PR head, base, and tested merge revisions.
3. Non-PR executions must explicitly set all seven PR-only fields to `null`.
4. Workflow run ID and attempt must be recorded together, or both be `null`.
5. Working-tree state and dirty-path metadata must follow the adopted schema and semantic validator.
6. The exact checked-out commit remains `source.commit_sha`; no duplicate checkout SHA is introduced.

## 3. Compatibility and historical records

- The v1.0.0 schema remains byte-for-byte unchanged (blob SHA-1 `8c072cf088e1cab39b0a18411d81682c0cc8ab44`).
- Existing v1.0.0 manifests, summaries, reports, inputs, calculations, and native outputs remain unchanged and valid.
- The default v1.0.1 validator accepts both v1.0.0 and v1.0.1 records. Use `--schema docs/schemas/research-result-record-v1.0.0.schema.json` when an explicitly v1.0.0-only validation run is required.
- No bulk backfill or retroactive rewriting is authorized. Downstream projects migrate producers and documentation for new runs; historical records remain under their recorded schema version.

## 4. Implementation and verification evidence

The merged implementation is PR #32 at `cd65712c54b4b298e6131f1045d89b795d3d7084`. The tested code-bearing commit was `db9e98c40232ad7ada1a7bf278bb31483e2306cd`; the later PR HEAD `18e7e847e2778c42e6c47bbb5d96cd0c9a4f81cc` changed only the implementation-plan verification ledger.

- [Structured-result validation run #48](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/45096940614): 69/69 tests passed; `python -m compileall -q docs/schemas` passed.
- [Candidate schema validation run #1212](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/45096940598): candidate schema/fixture/traceability validation, integration checks, Skill scaffold tests, compilation, and UV-EFT bundle validation passed.
- These checks validate the schema, validator, and repository software behavior. They do not certify scientific correctness of any calculation.

## 5. Downstream migration

The central repository remains the normative source. Downstream repositories must use a focused PR and preserve their existing domain-specific extensions.

| Repository | Migration target | Historical-data policy |
|---|---|---|
| `LZ-3-body-for-hdm` | Local v1.0.1 schema/validator, run-manifest producer, archive tests, and LZ-specific documentation | Keep all existing v1.0.0 records byte-for-byte |
| `ColliderAgent` | Update the existing structured-result adoption PR to v1.0.1, retain collider-MC extensions, and document final JSON run-manifest provenance | Keep existing progress YAML and historical event outputs unchanged |

No unrelated repositories are included in this adoption decision. Project-specific physics fields and acceptance criteria remain local to their owning projects.

## 6. Supersession

The unified implementation in PR #32 is the adopted resolution of the earlier overlapping v1.0.1 provenance proposals PR #28 and PR #29. Their alternative designs are not separate normative authorities.

---

## 中文采用决定

**决定：** 正式采用结构化科研结果数据规范 RCRPS v1.0.1。  
**决策负责人：** 项目负责人。  
**采用及生效日期：** 2026-11-23。  
**中央仓库：** `lm846802297-bit/high-energy-theory-research`。  
**实施 PR：** [#32](https://github.com/lm846802297-bit/high-energy-theory-research/pull/32)。  
**集成提交：** `cd65712c54b4b298e6131f1045d89b795d3d7084`。

自生效日起，新的重要数值计算、模拟、参数扫描和计算验证运行采用 v1.0.1。每个新的 v1.0.1 `run_manifest` 必须包含完整的 14 个 `execution.source_control` 字段，并满足 PR checkout、非 PR 显式 null、workflow ID/attempt 配对和 working-tree 语义约束。

v1.0.0 Schema 保持原样，历史 v1.0.0 运行清单、结果、输入和原生数据不回填、不改写。v1.0.1 默认校验器同时接受 v1.0.0 与 v1.0.1 记录；需要仅按旧版校验时，显式指定 v1.0.0 Schema。

69/69 项回归测试和 Python 编译已在 PR #32 的精确代码提交上通过。该软件验证不替代具体科研计算所需的数值收敛和物理验证。下游项目分别通过独立 PR 迁移新运行清单生成器、校验器和项目文档，保留各自的领域扩展及全部历史结果。
