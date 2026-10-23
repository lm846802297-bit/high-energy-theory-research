# Schema v1.4.3.7 候选版本

语言：简体中文。英文原版：[README.md](README.md)。

本目录包含尚未批准的候选 Schema 包，不是已发布的规范版本。

## 按版本区分的测试夹具集合

- `tests/fixture-index.json` 是继承自 `1.4.3.6-candidate` 的测试夹具索引。其字节内容和版本标签作为来源信息保留，不会被悄然改标。
- `tests/fixture-index-v1.4.3.7.json` 是针对当前 Schema 进行验收时使用的候选版本专属索引。Run Plan/Run Manifest 的四条有效/条件有效夹具记录已在 `tests/v1.4.3.7/` 中重新生成，并包含符合候选契约的非空结构化载荷。
- 校验器会将继承夹具预期与当前候选 Schema 之间的不匹配单独报告为兼容性漂移。这些不匹配不会替代或削弱与候选版本匹配的测试套件。

## FingerprintInputs（指纹输入）

`run_plan.fingerprint_inputs` 使用候选版本专属的 `fingerprint-inputs-v1` 契约，具体见 `docs/governance/fingerprint-inputs-contract-review.md`。RFC 8785 确定性哈希实现、黄金测试向量和负向测试位于研究 Skill 脚本及 `tests/unit/test_fingerprint_inputs.py` 中。

## 验证报告的来源追溯

工作流会在 runner 中重新生成 `audit/validation-report.json`，并将其作为 GitHub Actions 工件 `candidate-schema-validation-report` 上传。仓库中提交的报告文件是导入的仓库快照，不能单独作为最新 CI 运行的证据。审计当前计数和测试夹具结果时，应使用具体工作流运行所附的报告工件。

## 迁移原型与 validation_ids 边界

迁移工具当前规则版本为 `v1.4.3.7-migration-rules-6`。规则 v5 在代码/测试 HEAD `0799dada7eaa8dcd08b8db2f2311a844335d7198` 上的本地验证由仓库所有者报告为通过：目录清单测试 7/7、迁移回归 33/33、集成测试 30/30、完整单元测试 83/83、Python 编译通过，以及 Schema 验证 68/68 项、候选 Fixture 83/83、语义用例 16/16、追踪记录 125 条。该报告在仓库外的临时目录生成，未覆盖仓库中的历史验证报告。这些结果不是 GitHub Actions 通过证据。

后续静态审查发现 DD-ART-010 的迁移门禁缺口：旧版 Task Execution Contract 的 `contract_hash` 可能被直接映射为 `contract_sha256` 而未按目标载荷重新验证；缺失的 `alternative_identity_methods` 也可能因为候选 Schema 将其设为可选字段而通过迁移。规则 v6 新增 MIG-015，缺失登记表或无法重新验证的契约哈希将产生未解决项，目标记录不会写入 staging。相关代码和两项回归测试已添加，但**尚未在本地执行验证**；不能把规则 v5 的测试结果当作规则 v6 的通过证据。

- 工具先加载只读源快照，并且只在同一项目内按唯一主键解析引用。
- 唯一解析到 `validation_plan` 类型的记录时，映射到 `validation_plan_ids`。
- 只有当目标是 `validation_activity`，且其状态有明确的目标枚举映射、`started_at` 是带时区的有效 ISO 日期时间时，才映射到 `validation_activity_ids`；不会自动推断 `in_progress → running`。
- 目标缺失、跨类型 ID 重复、记录类型不受支持、项目不匹配或启动证据不足的情况，均保持未解决。
- 空的旧版 `validation_ids` 列表会映射为空的 `validation_activity_ids` 和 `validation_plan_ids` 数组。
- Dry-run 和 staging 阶段都不会提交更改。报告始终设置 `commit_allowed=false`；事务式提交、活动指针切换、回滚和完整跨记录验证均尚未实现。
- 回归测试位于 `tests/unit/test_migration_reference_resolution.py`。现有 `audit/migration-dry-run-summary.json` 是按照规则版本 1 生成的历史报告。
- Artifact Schema 允许 `FileEntry.entry_type: "symlink"`，而目录清单辅助程序拒绝符号链接条目。这是尚未解决的 DD-ART-008 规范与实现契约差异，需在批准符号链接策略后处理。

只有在来源证据完整时，该解析器才能减少可避免的歧义。历史 v1.3 源包仍不可用，兼容性尚未验证；DD-ART-007 至 DD-ART-010 仍待批准。

## 发布约束

- DD-ART-007 至 DD-ART-010 尚未批准。
- `validation_ids` 迁移仍仅限暂存阶段；在歧义解决前不得继续。
- Schema/CI 通过不构成物理正确性证明。任何真实研究任务在作出发布决定前，都必须独立验证以下链条：来源追溯 → 配置 → 运行 → 产物 → 验证 → 证据 → Claim。
