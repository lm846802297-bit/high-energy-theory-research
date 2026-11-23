# 下游科研规范采用契约

**状态：** 已采用的中央契约  
**生效日期：** 2026-11-23  
**适用范围：** 从 high-energy-theory-research 采用共享规范的项目仓库

## 1. 目的

本契约使下游采用过程明确且可复现。每个下游项目必须标明采用了哪些中央规范，以及提供这些规范的精确、不可变中央版本。

该契约避免项目依赖不断变化的 main、混用不兼容的规范版本，或仅凭仓库中存在某个规范副本就声称已经采用。

## 2. 必需的规范锁记录

每个采用规范的项目都应保存 YAML 锁文件，通常位于 research/standards-lock.yaml，也可以使用 README 明确声明的其他路径。使用[规范锁模板](../../templates/research-standards-lock.yaml)。

必需字段：

- lock_version：锁文件格式版本。
- central_repository：规范的 owner/repository。
- standards_release：中央 release/tag（如已发布）；否则为 null。
- source_commit：经过审查并采用的完整 40 位中央 commit SHA。
- adopted_at：下游采用决策日期。
- adoption_pr：集成锁文件和本地引用的下游 PR。
- adopted_profiles：本项目实际采用的共享规范配置 ID。
- local_extensions：项目专属规范路径及其范围。
- deviations：对中央要求的明确例外，包括理由和批准依据；没有时使用空列表。

Release tag 不能替代 source_commit；如果两者都有，应同时记录。不得编造 release 标识。在中央项目发布正式规范版本之前，standards_release 必须为 null，并固定完整 commit SHA。

## 3. 采用配置

初始配置 ID：

- core-governance
- research-compute
- task-handoff
- scientific-diff
- research-quality-gate
- calculation-result-archive
- rcrps-v1.0.1
- git-review-and-merge
- document-review
- referee-response-and-manuscript-synchronization

项目可以根据实际情况选择子集，但锁文件必须明确列出每项实际采用的配置。采用 rcrps-v1.0.1 的数值项目仍须保留自己的领域扩展字段和验证流程。

## 3A. 机器验证

中央仓库提供 `docs/schemas/standards-adoption-v1.0.0.schema.json` 和 `docs/schemas/validate_standards_adoption.py`。应使用该验证器检查项目规范锁文件；存在任务溯源记录或规范验收报告时，也应一并检查。验证器检查记录契约、已知 Profile 与中央规范文件的映射、本地扩展路径/指纹，以及任务记录与锁文件/任务单之间的指纹关系。如果本地 Git 对象库中包含精确中央 commit，还可以检查该 commit 是否真实存在。

结构验证通过只说明声明的采用记录和证据记录在内部一致。它不能证明推理过程中遵守了每一项要求，也不能证明物理结果正确。任务级规范执行仍须结合实际工作和科学证据进行审查。

## 4. 本地扩展与偏离

- 项目专属物理规则继续由所属项目仓库维护。
- 项目可以强化中央要求。
- 不得暗中削弱或重新定义已采用的中央最低要求。
- 偏离必须注明中央配置/要求、原因、项目负责人决策/PR，以及复核日期或重新考虑的条件。
- 任务类型中的 N/A 不自动构成项目级偏离。

## 5. 迁移与更新

1. 阅读中央规范索引，并检查 source_commit 对应的精确规范文件。
2. 与项目现有指令和规范比较。
3. 保留领域专属规则；只有在检查入站链接和运行依赖后，才删除或重定向重复的通用文字。
4. 添加/更新规范锁文件，并从项目 README/AGENTS 链接。
5. 创建聚焦的下游 PR。中央规范更新不会自动修改项目 main。
6. 审查精确 diff，验证链接和工具，并记录下游验收决策。
7. 只有在明确决定采用新中央版本时才更新锁文件。

中央仓库是共享最低规范的权威来源；下游项目仓库仍然是其科学内容、实际运行、输入、原生结果和项目专属验收标准的权威来源。

## 6. 当前发布状态

RCRPS v1.0.1 已正式采用。更广泛的中央科研规范集合尚未发布语义化版本。在该版本发布前，下游项目必须固定完整 commit SHA，并将 standards_release 设为 null。

参见[中央科研规范索引](CENTRAL_STANDARDS_INDEX.zh-CN.md)。
