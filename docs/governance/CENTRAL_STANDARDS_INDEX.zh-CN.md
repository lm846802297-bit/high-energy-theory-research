# 中央科研规范索引

**状态：** 规范导航索引  
**所有者：** 共享科研基础设施仓库  
**适用范围：** 明确采用本中央规范体系的研究仓库

本索引为每项共享要求指定唯一的中央权威来源。索引负责导航和规范优先级，具体要求以所链接的正式规范为准。

## 1. 共享规范

| 领域 | 规范权威来源 | 主要内容 |
|---|---|---|
| 仓库入口与 Agent 指令 | [AGENTS.md](../../AGENTS.md) | 任务预检、仓库边界、任务路由和强制入口指令 |
| 科研治理与来源层级 | [科研治理规范](../RESEARCH_GOVERNANCE_STANDARD.zh-CN.md) | 来源权威、冲突处理、科学状态以及中央/项目边界 |
| 计算执行 | [科研计算执行规范](../../RESEARCH_COMPUTE_POLICY.md) | 主计算环境、GitHub 归档、Actions 独立验证和运行溯源 |
| 任务交接 | [科研任务交接规范](../RESEARCH_TASK_HANDOFF_STANDARD.zh-CN.md) 与[任务单模板](../../templates/research-task-brief.zh-CN.md) | 实质性任务的执行前定义和交付记录 |
| 科学变更生命周期 | [Scientific Diff 工作流](../scientific-diff-workflow.md) | 项目/工作流/变更/运行/主张层级和证据追踪 |
| 科研质量门 | [科研质量门](RESEARCH_QUALITY_GATE.zh-CN.md) | 十项共享验收要求、任务类型及 PASS/FAIL/BLOCKED/NOT RUN/N/A 状态 |
| 科研沟通 | [Scientific Diff 第 11 节](../scientific-diff-workflow.md#11-research-reporting-and-communication-standard) | 结论、依据、结果、剩余工作及与证据相称的表述 |
| 计算结果归档 | [计算结果归档规范](../CALCULATION_RESULT_ARCHIVAL_POLICY.zh-CN.md) | 原生输出、解压后提交、溯源、哈希和 CI 边界 |
| 结构化数值记录 | [RCRPS v1.0.1](../STRUCTURED_RESULT_DATA_STANDARD_v1.0.1.zh-CN.md) 与[采用记录](RCRPS_V1.0.1_ADOPTION_RECORD.md) | 运行清单、结果摘要、验证报告、源码控制溯源和 CSV 约定 |
| 科学审查 | [科学变更审查清单](../review-checklist.md) | 基线、推导、计算、物理主张、依赖和决策 |
| 文档审查与迁移 | [科研文档审查规范](../DOCUMENT_REVIEW_STANDARD.zh-CN.md) | 文档身份、权威性、科学内容、引用、一致性、可复现性、链接、处置及安全迁移 |
| 审稿回复与论文同步 | [审稿回复与论文正文同步规范](../REFEREE_RESPONSE_AND_MANUSCRIPT_SYNCHRONIZATION_STANDARD.zh-CN.md) | 面向审稿人的论证完整性、与内部正文跟踪的分离、独立科学论证的保留及审查记录 |
| Git 集成 | [Git 合并规范](GIT_MERGE_POLICY.md) | PR 生命周期、审查、合并策略、main 可发现性和合并后验证 |
| 高能理论方法 | [研究 Skill](../../skills/high-energy-theory-research/SKILL.md) | 文献、推导、UV–EFT、圈图和唯象学等领域专属流程 |
| 项目/工作流导航 | [项目注册表](../../projects/README.zh-CN.md) | 项目身份、父子层级和规范研究仓库入口 |

## 2. 规范状态与版本规则

- **已采用：** 已批准的中央规范。下游仓库通过审查 PR 固定采用完整 commit SHA 或正式 release。
- **历史兼容：** 文件或 Schema 保留用于解释、校验历史记录，不再作为新工作的默认版本。
- **候选/草案：** 尚未成为规范要求。不能仅因文件存在或工作流通过就提升其状态。
- **已实现但非规范：** 软件已经存在，但其接口或验收含义尚未正式批准。

自 2026-11-23 起，RCRPS v1.0.1 是新产生的重要数值计算所采用的中央结构化结果规范。RCRPS v1.0.0 保留为历史兼容版本，其 Schema 和历史记录不变。研究记录 Schema v1.4.3.7 是独立的候选项目，不是结果数据 Schema。

## 3. 采用与优先级

1. 中央仓库负责共享最低科研标准、可复用 Skills、模板、Schema、校验器和通用自动化。
2. 每个项目仓库负责自己的模型、假设、领域约定、计算、输入、原生输出、科学主张和领域验收标准。
3. 项目可以增加兼容的严格要求，不得暗中削弱已采用的中央最低要求。
4. 下游仓库在规范锁文件中记录中央仓库完整 commit、可选 release、采用的规范配置、本地扩展和批准的偏离。参见[下游规范采用契约](DOWNSTREAM_STANDARDS_ADOPTION.zh-CN.md)和[锁文件模板](../../templates/research-standards-lock.yaml)。
5. 中央规范更新不会自动修改下游仓库；必须通过独立审查 PR 采用。

## 4. 推荐阅读顺序

开始一项实质性研究任务时：

1. 阅读下游仓库的 AGENTS.md 和项目 README。
2. 阅读本索引及[科研治理规范](../RESEARCH_GOVERNANCE_STANDARD.zh-CN.md)。
3. 按照[任务交接规范](../RESEARCH_TASK_HANDOFF_STANDARD.zh-CN.md)填写[科研任务单](../../templates/research-task-brief.zh-CN.md)。
4. 根据任务类型选择[科研质量门](RESEARCH_QUALITY_GATE.zh-CN.md)。
5. 遵循适用的计算、归档、结构化记录、Scientific Diff 和 Git 规范。
6. 阅读项目专属规范及相关原始科学文献。

## 5. 明确保留在项目内部的内容

不能仅因为某个项目已经写成文档，就将以下内容提升为共享最低标准：

- LZ 三体运动学、AFH 响应约定、同位素选择、晕模型、探测器响应和似然假设；
- UV–EFT 图完整性、重整化处方、Ward 恒等式、反项记录以及特定模型的算符基底约定；
- 对撞机专属 UFO、MadGraph、Pythia8、Delphes、事件样本、cutflow 和探测器卡片规则；
- 热场论、降维、弱电相变可观测量和项目基准；
- 特定模型的场内容、物理假设、输入数据集、冻结基准和数值验收阈值。

只有在范围、所有权、接口和独立验证均明确后，真正可复用的领域规范才可以提升为中央规范。
