# 高能理论物理研究

语言：简体中文。英文原版：[README.md](README.md)。

本仓库是高能理论物理研究的共享基础设施仓库，维护可复用工作流、Skills、科研规范、Schema、模板、测试和导航元数据。具体项目的研究记录、源码、计算、验证输出和研究产物保存在各自的项目仓库中。

## 共享科研规范

[中央科研规范索引](docs/governance/CENTRAL_STANDARDS_INDEX.zh-CN.md)是共享科研治理、任务交接、质量门、计算、溯源、归档、结构化结果、审查和 Git 集成规范的统一入口。下游项目通过 PR 固定采用中央仓库的完整 commit SHA；项目专属物理规则仍保留在各自研究仓库。

## Scientific Diff 工作流

**Scientific Diff（科学变更追踪）** 不只是文本或代码比较。它记录研究状态发生了什么变化、变化的原因、支持变化的证据、执行过哪些检查，以及哪些下游结果或主张可能受到影响。

该工作流适用于理论粒子物理、UV–EFT 匹配、微扰计算、数值唯象学以及论文/审稿回复工作。它用于组织证据，**不能**替代科学判断，也不能因为工作流执行完成就证明结果正确。

### 从这里开始

0. 每次开始任务前，先阅读根目录的强制规范 [AGENTS.md](AGENTS.md) 和[中央科研规范索引](docs/governance/CENTRAL_STANDARDS_INDEX.zh-CN.md)。
1. 阅读[详细中文用户手册](docs/USER_GUIDE.zh-CN.md)，了解项目设置、工作流、研究变更、证据、验证和审查。
2. 阅读[Scientific Diff 工作流规范](docs/scientific-diff-workflow.md)。
3. 每项实质性研究变更都应从[研究变更模板](templates/research-change.md)开始。
4. 使用[主张—证据矩阵模板](templates/claim-evidence-matrix.md)追踪重要物理陈述的证据支持程度。
5. 在标记变更完成或将结果同步到论文之前，执行[审查清单](docs/review-checklist.md)。
6. 使用[项目注册表](projects/README.zh-CN.md)查找各项目的规范研究仓库。RC-001 的规范归档位于 [axial-vector-review-response](https://github.com/lm846802297-bit/axial-vector-review-response/tree/main/research/rc001-vll-higgs-singlet-uv-eft)。
7. 使用[项目注册表说明](projects/README.zh-CN.md)区分顶层研究项目、工作流和研究变更记录。VLL–Higgs–Singlet UV–EFT 工作流属于父项目 `axial-vector-model-building`，不是独立的顶层项目。
8. 可复用的研究 Skill 从 [SKILL.md](skills/high-energy-theory-research/SKILL.md) 开始，再阅读其参考指南。
9. 修改候选 Schema 前，先检查[仓库状态](docs/REPOSITORY_STATUS.md)、[未解决问题](docs/OPEN_ISSUES.md)和[规范决策登记表](docs/governance/DECISION_REGISTER.md)。
10. 阅读 [v1.6.5 设计基线](docs/design/high-energy-theory-research-Skill-v1.6.5.md)、[v1.6.7 设计与实现整合报告](docs/design/high-energy-theory-research-Skill-v1.6.7.md)，以及 [v1.6.6 Artifact 身份候选澄清](schema/v1.4.3.7/audit/高能理论物理研究-Skill-详细设计文档-v1.6.6-Artifact身份语义候选修订.md)。
11. 提交数值结果、运行清单和验证证据时，必须遵守[计算结果归档规范](docs/CALCULATION_RESULT_ARCHIVAL_POLICY.zh-CN.md)。
12. 必须遵守[科研计算执行规范](RESEARCH_COMPUTE_POLICY.md)：普通 GPT 聊天模式使用 ChatGPT Linux；Codex/Work 可使用 Windows 本地环境或 GPT 管理的云端计算机；GitHub 负责长期归档，Actions 只负责独立验证。
13. 每项实质性研究任务开始前，填写[研究任务单模板](templates/research-task-brief.zh-CN.md)，遵循[任务交接规范](docs/RESEARCH_TASK_HANDOFF_STANDARD.zh-CN.md)，并选择适用的[科研质量门](docs/governance/RESEARCH_QUALITY_GATE.zh-CN.md)。
14. 实质性科研 PR 默认使用 [Merge Commit 合并策略](docs/governance/GIT_MERGE_POLICY.md)，保留有科研追溯价值的独立提交。
15. 已完成且验收通过的科研成果必须及时合并到 `main`，并在专题 README、项目注册表或研究索引中建立稳定入口；PR 负责审查与集成，不作为长期归档位置。未完成工作保留在专题分支或 Draft PR。详见 [科研成果归档与 PR 生命周期规范](docs/governance/GIT_MERGE_POLICY.md#6-main-is-the-canonical-research-archive)。

### 核心链条

科学问题 → 基线与假设 → 推导 → 计算 → 验证 → 物理主张 → 论文。

链条中的每一步都应可追溯。上游假设或公式发生变化时，必须评估其对依赖计算、图、约束和论文陈述的影响。

### 仓库目录结构

- **`docs/scientific-diff-workflow.md`** — 工作流、术语定义、状态模型和物理研究专项指引。
- **`projects/`** — 顶层项目注册表及项目/工作流层级；目前只承担导航元数据功能。
- **`docs/USER_GUIDE.md`** — 项目设置、研究变更、计算证据、验证和迁移纪律的详细操作手册；另有[中文版本](docs/USER_GUIDE.zh-CN.md)。
- **`RESEARCH_COMPUTE_POLICY.md`** — 主计算、GitHub 归档和 Actions 独立验证三者职责分离的强制规范。
- **`docs/CALCULATION_RESULT_ARCHIVAL_POLICY.zh-CN.md`** — 数值结果原生文件归档、运行来源、校验和、大文件存储及远端核对的强制规范；另有[英文版](docs/CALCULATION_RESULT_ARCHIVAL_POLICY.md)。
- **`docs/GENERATED_FIGURE_AND_REPORT_POLICY.zh-CN.md`** — 归档图件源数据和绘图程序、日常 PDF/PNG/SVG 按需生成的共享规范；另有[英文版](docs/GENERATED_FIGURE_AND_REPORT_POLICY.md)。
- **`docs/PROJECT_REGISTRY_AUDIT.md`** — 第一阶段注册表/路径预审的范围与证据，明确记录尚未执行的测试和未来文件迁移的限制。
- **`docs/review-checklist.md`** — 科学变更及其与论文同步时的审查项目。
- **`docs/design/`** — 保留的设计基线与整合实现报告；目录说明见[中文版本](docs/design/README.zh-CN.md)。
- **`docs/governance/`** — 规范决策及指纹契约审查。
- **`templates/research-change.md`** — 单项研究变更的记录模板。
- **`templates/project-record.md`** — 顶层研究项目或嵌套工作流的登记模板。
- **`templates/claim-evidence-matrix.md`** — 新建主张—证据台账的通用模板。
- **项目专属研究仓库** — 规范研究记录、计算源码、原生输出、验证记录和研究产物保存在各自项目仓库；本仓库只保留导航元数据。
- **`schema/v1.4.3.7/`** — 候选 JSON Schema、测试夹具、校验器、迁移原型、审计报告和需求/测试可追溯性数据；目录说明见[中文版本](schema/v1.4.3.7/README.zh-CN.md)。
- **`skills/high-energy-theory-research/`** — 可复用的 Skill 入口、参考指南、指纹计算、结构化记录校验和项目注册表校验工具。
- **`tests/eval-cases/`** — 有明确范围的解析矩阵与 UV–EFT 硬核导数试点；相关说明见[解析质量矩阵试点中文说明](tests/eval-cases/analytic-mass-matrix-pilot/README.zh-CN.md)和 [UV–EFT 硬核导数试点中文说明](tests/eval-cases/uv-eFT-hard-derivative-pilot/README.zh-CN.md)。
- **`tests/unit/`** — 对 Skill 框架、记录校验器、指纹、迁移引用解析和试点案例的回归测试。

## 研究 Skill 与候选 Schema

**状态：开发/候选阶段，尚未宣布正式 Schema 发布。**

- 研究设计基线：v1.6.5。
- Artifact 身份澄清：v1.6.6 候选版本；相关规范决策仍待批准。
- 整合设计/实现报告：v1.6.7。
- Schema 包：`schema/v1.4.3.7/`，以候选版本包形式引入。
- 候选包包含 25 个 JSON Schema 入口、83 个已索引测试夹具、跨记录校验、保守的迁移原型、目录清单辅助工具、审计报告和可追溯性数据。
- 项目记录校验器位于 `skills/high-energy-theory-research/scripts/validate_project_records.py`。它支持 JSON/YAML 解析、候选 Schema 检查、有限范围的引用与 ID 校验、状态/原因一致性检查，以及本地来源/产物路径检查。
- 端到端 UV–EFT 试点将有限范围内的硬核导数及小 `r` 展开与独立的 Feynman 参数数值积分进行比较。该试点不能证明完整 UV 图集合完备、完整的 dimension-six 算符基底约化已完成，或最终 Wilson 系数已通过科学验收。

## 工作原则

- 保留基线，不得悄然覆盖既有结果。
- 分开记录假设、推导、代码、数值输出、证据和主张。
- 明确记录结果成立的具体范围与条件。
- 区分计算完成、独立验证和主张确认。
- 只有给出理由时才可将检查标记为不适用；证据缺失应标记为未解决，而不是通过。
- 论文表述不得强于已验证证据所能支持的程度。
- 使用 Git diff 比较有版本控制的文本/代码；对于普通文本 diff 无法有效比较的 notebook、数据集、生成图和其他产物，应记录哈希或元数据。

## 本地验证

PR HEAD `5c5b10b6889c2e4146d0a696fde16f2b3ca847bf` 的最新一次集成前 CI 于 2026-10-21 通过候选验证工作流（[GitHub Actions 运行记录](https://github.com/lm846802297-bit/high-energy-theory-research/actions/runs/39542332657)）：

- 候选 Schema 包检查：60/60。
- Schema 入口与清单哈希：25/25。
- 当前候选测试夹具预期：83/83。
- 语义测试案例：16/16。
- 候选集成测试：29/29。
- 仓库单元测试：36/36。
- Python 编译：通过。
- 真实物理审计案例：8/8。
- 研究记录图：22 条记录，0 个错误，0 条警告。
- 指纹重算与来源感知迁移测试：通过；有歧义的引用仍保持未解决。
- 小 `r` 二阶残差回归：最大缩放残差为 63.86，低于 70 的测试阈值。

以上均为范围有限、绑定到特定 SHA 的软件验证结果。它们**不能**证明 Schema 完整、历史迁移兼容，或完整物理结果正确。来源追溯包中包含独立的 Mathematica 验证脚本，但该脚本**没有在 CI 中运行**，因此不得标记为通过。

上述成功运行针对集成前 HEAD `5c5b10b6889c2e4146d0a696fde16f2b3ca847bf`。之后针对 `879996ce13929afdf63e463dced6668df0b691b1` 的一次集成尝试，在任何工作流步骤被记录之前便失败：作业没有分配 runner 名称，日志也不可用。这不能证明代码测试失败，但同样不能作为集成后代码通过的证据。当前候选树新增的输出目录安全回归检查尚未经过 CI 验证。待 runner 可用时，应对最终 HEAD 重新运行完整工作流。

### 验证命令

~~~bash
python -m pip install -r requirements-dev.txt
python schema/v1.4.3.7/tools/schema-v1.4.3.6-validate.py schema/v1.4.3.7
python schema/v1.4.3.7/tests/integration/test_v1_4_3_7.py
python -m unittest discover -s tests/unit -v
python skills/high-energy-theory-research/scripts/validate_project_registry.py --registry projects/registry.yaml --repo-root .
python skills/high-energy-theory-research/scripts/validate_project_records.py path/to/project/records --project-root path/to/project
~~~

## 治理与发布限制

在所有发布门槛处理完毕前，不得将候选版本视为已批准发布：

1. DD-ART-007 至 DD-ART-010 目前只是建议，不是批准；需要明确的规范决策。
2. 解决测试夹具索引的版本字段不一致：继承的索引标记为 `1.4.3.6-candidate`，而包清单标记为 `1.4.3.7-candidate`。用于逐字节验证来源关系的原始归档当前不可用。
3. 在不猜测目标记录类型的前提下，解决旧版 `validation_ids` 的映射歧义。迁移仍仅限暂存阶段，`commit_allowed=false`；不允许覆盖源记录或提交迁移结果。
4. 扩展语义/状态机覆盖，并验证目录清单与实际文件系统内容一致。
5. 定义并审查 `FingerprintInputs` 字段与哈希契约，再补齐完整可复现性验收所需的结构化记录覆盖。
6. 在宣称端到端科学可复现之前，先为真实研究任务建立科学验收测试。

## 科学诚信边界

软件测试通过并不能证明物理推导正确。即使推导正确，也不自动证明数值实现或实验约束应用正确。具体需要哪些检查，取决于模型、近似、重整化方案、数据和可观测量。

本工作流的作用是明确记录这些依赖，而不是自动认证物理正确性。不得将候选 Schema 或一次合并描述为对 UV–EFT 匹配、Wilson 系数或实验允许性主张的科学批准。
