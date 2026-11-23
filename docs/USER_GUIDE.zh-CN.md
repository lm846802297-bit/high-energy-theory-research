# 用户手册——高能理论物理研究平台

语言：简体中文。英文原版：[USER_GUIDE.md](USER_GUIDE.md)。

本手册介绍如何将本仓库作为一个**多项目研究平台**使用。首先阅读[中央科研规范索引](governance/CENTRAL_STANDARDS_INDEX.md)，了解已采用的共享规范和下游采用契约。[科研治理规范](RESEARCH_GOVERNANCE_STANDARD.md)、[任务交接规范](RESEARCH_TASK_HANDOFF_STANDARD.md)和[科研质量门](governance/RESEARCH_QUALITY_GATE.md)定义通用最低要求；项目专属物理规则仍由对应研究仓库维护。

本仓库是研究流程与可追溯性框架，并非完全自主的研究智能体。软件检查通过不等于物理结果正确。

## 1. 从这里开始

1. 阅读[中央科研规范索引](governance/CENTRAL_STANDARDS_INDEX.md)和[科研治理规范](RESEARCH_GOVERNANCE_STANDARD.md)。
2. 阅读本手册，了解整体工作方式。
3. 实质性研究任务开始前，填写[研究任务单模板](../templates/research-task-brief.md)，遵循[任务交接规范](RESEARCH_TASK_HANDOFF_STANDARD.md)，并选择适用的[科研质量门](governance/RESEARCH_QUALITY_GATE.md)任务类型。
4. 打开[项目注册表说明](../projects/README.zh-CN.md)和[注册表文件](../projects/registry.yaml)，确定研究所属的项目与工作流。
5. 阅读[Scientific Diff 工作流规范](scientific-diff-workflow.md)。
6. 开始计算前，阅读[研究 Skill](../skills/high-energy-theory-research/SKILL.md)。
7. 打开所选项目的规范研究记录及 Claim–Evidence Matrix（主张—证据矩阵）。
8. 在修改候选 Schema 或迁移规则前，检查[仓库状态](REPOSITORY_STATUS.md)和[未解决问题](OPEN_ISSUES.md)。

根目录的[中文 README](../README.zh-CN.md)是简明入口；本文件是完整操作手册。

## 2. 理解五个层级

不要把每个目录或每项计算都称为一个“项目”。本仓库区分以下五个层级：

| 层级 | 含义 | 本仓库中的示例 |
|---|---|---|
| 项目（Project） | 具有独立研究范围和生命周期的持续研究计划 | `axial-vector-model-building` |
| 工作流（Workstream） | 项目内部范围明确的一条研究分支 | `vll-higgs-singlet-uv-eft` |
| 研究变更（Research change） | 有基线、理由、证据和影响评估的具体科学变更 | `RC-001` |
| 运行（Run） | 一次真实执行，具有明确的源码版本、输入、环境和输出 | 只有实际执行后才能建立运行记录 |
| 主张（Claim） | 有明确适用范围、可以评估证据支持程度的物理陈述 | `CL-015` |

一个项目可以包含多个工作流；一个工作流可以包含多项研究变更；一次变更可能需要多次运行，也可能影响多个物理主张。这些标识符不能互换。

**当前层级关系：** `vll-higgs-singlet-uv-eft` 是 `axial-vector-model-building` 项目内部的工作流，并非独立的顶层项目。`RC-001-GAUGE-SUBGRAPHS` 是 UV–EFT 研究关联的子记录，不是独立顶层项目。

## 3. 新工作应该放在哪里？

创建文件之前，按以下规则判断：

- **新建顶层项目：** 研究计划具有独立且有意义的研究范围、问题、生命周期和证据体系。将其登记到 `projects/registry.yaml`。
- **新建工作流：** 工作属于已有项目，但需要单独管理范围、进度或计算流程。将其添加到父项目的 `workstreams` 下。
- **新建研究变更：** 一项明确的推导、修正、计算、交叉核查或论文影响分析会改变当前研究状态。使用[研究变更模板](../templates/research-change.md)。
- **新建物理主张：** 某项物理陈述需要独立管理证据和适用范围。将其添加到相应项目的 Claim–Evidence Matrix。
- **新建运行记录：** 只有在计算或测试真实执行后，才记录确切代码版本、输入/配置、环境、命令、输出和状态。不得为计划中的检查虚构运行记录。
- **新增通用方法或工具：** 如果可供多个项目复用，应放在共享的 `skills/`、`schema/`、`templates/`、`docs/`、`tests/` 或 `tools/` 目录，而不是复制到单一项目中。

不要仅仅因为某个名称出现在论文、笔记或未来研究构想中，就将其登记为无关的新项目。只有在项目身份和归属关系已确认时才进行登记。

## 4. 登记项目或工作流

### 4.1 编辑注册表

导航注册表位于[`projects/registry.yaml`](../projects/registry.yaml)。它描述项目层级，**不是**候选 Schema v1.4.3.7 中的记录类型，因此不会传入结构化研究记录校验器。

新建顶层项目时，在 `projects` 下添加条目，并填写稳定的 `project_id`、标题、状态、范围以及可选的工作流列表。新增工作流时，将其添加到父项目的 `workstreams` 下，并将 `parent_project_id` 设为该父项目的 `project_id`。

使用稳定的小写连字符 ID。项目改名时不要回收或替换原 ID；应保留 ID，仅更新标题。人类工作流状态包括 `planned`、`active`、`blocked`、`paused`、`complete` 和 `archived`。这些状态描述工作进度，而非科学正确性。

以下仅为结构示例，不要将示例 ID 直接复制到正式注册表：

~~~yaml
projects:
  - project_id: example-research-programme
    title: 示例研究计划
    status: planned
    scope: 一个具有独立意义的研究计划。
    workstreams:
      - workstream_id: example-loop-matching
        title: 圈图匹配
        kind: research_branch
        status: planned
        parent_project_id: example-research-programme
        scope: 匹配计算及其验证。
        canonical_records: []
~~~

不要编造仓库 URL、基线 SHA、已完成的检查或科学状态。信息未知时，使用 `unknown`、省略可选字段，或明确标注尚未解决。

### 4.2 使用项目记录模板

从[项目记录模板](../templates/project-record.md)开始，填写：

- 项目身份及父项目；
- 研究范围、包含/排除的问题、模型约定和基线；
- 工作流及关联的研究变更 ID；
- 计算入口、运行记录、验证证据和 Claim Matrix；
- 已建立、有条件支持和尚未解决的结论；
- 一项明确的下一步行动，以及关闭该任务所需的证据。

该模板是供人阅读和维护的规划文档，不会自动创建结构化记录、运行计算或批准项目。

### 4.3 校验注册表

运行专用的注册表/路径检查器：

~~~bash
python skills/high-energy-theory-research/scripts/validate_project_registry.py --registry projects/registry.yaml --repo-root .
~~~

该检查器验证注册表结构、稳定 ID、父项目与工作流的关系，以及声明的规范路径是否存在且位于仓库内部。这只是有限范围的导航检查，不是 Schema v1.4.3.7 校验，也不是科学验证。

## 5. 开始一项研究变更

对于每一项实质性的科学变更：

1. **固定基线。** 记录 commit SHA、文档版本、notebook 版本或其他不可变来源。
2. **明确一个问题。** 指明要研究的公式、模型假设、可观测量、实验解释或论文主张。
3. **定义范围和控制条件。** 记录纳入/排除的贡献、微扰阶数、参数范围、重整化方案、红外处方、近似条件和比较基准。
4. **绘制依赖关系。** 找出可能受影响的上游假设，以及下游方程、代码、图、主张和论文段落。
5. **创建记录。** 复制 `templates/research-change.md`，分配稳定的研究变更 ID，并关联父项目和工作流。
6. **计算前先规划证据。** 决定需要哪些解析检查、数值检查、独立推导、软件包级计算和实验来源。
7. **计算并留档。** 确保代码、输入参数、输出、环境和局限均可追溯。
8. **评估主张。** 将证据与主张本身及其适用范围比较后，再更新相应的 Claim–Evidence Matrix。
9. **审查下游影响。** 只有在验证结果支持的范围内，才更新相关图、论文文字和审稿回复。
10. **关闭或继续推进。** 明确标记未解决事项，并指出下一项能够产生证据的行动。

完整流程参见 [Scientific Diff 工作流](scientific-diff-workflow.md)和[审查清单](review-checklist.md)。

## 6. 使用研究 Skill

可复用的研究指令位于[研究 Skill 文件](../skills/high-energy-theory-research/SKILL.md)。它适用于文献分析、解析推导、圈图计算、参数扫描、实验约束和论文核查等任务。

开始任务前，提供或确认：

- 父项目 ID 和工作流 ID；
- 研究问题与不可变基线；
- 来源论文/数据及其版本；
- 模型、场内容、电荷指派、符号和约定；
- 目标微扰阶数与近似；
- 预期产物和独立验证方法；
- 当前主张状态与未解决依赖。

Skill 目前由指令、参考文档和脚本构成，尚不是能够自动完成所有研究阶段的完整执行智能体。应明确区分实际执行的步骤和仅计划执行的步骤。

## 7. 计算与独立验证

必须区分以下证据类别：

1. **解析推导：** 在明确假设下给出方程和中间步骤。
2. **符号/代数检查：** 例如使用 SymPy 或 Mathematica 化简。准确说明检查了哪些恒等式或系数。
3. **数值检查：** 记录输入、精度、收敛性、稳定性和输出。
4. **独立计算：** 使用真正独立的推导路径、实现或方法。
5. **图级验证：** 例如给出可运行的 FeynCalc/FeynArts 计算、软件包版本假设及输出。
6. **实验验证/重解释：** 记录来源版本、数据/似然、选择假设、重解释代码和适用范围。
7. **软件/CI 验证：** 检查代码和工作流的行为。

某一类别通过不代表其他类别也通过。符号检查不是图级验证；CI 通过不是 Wilson 系数正确的证明；引用文献不等于复现。如果工具或环境不可用，应记录缺失的证据及其影响。

每次重要数值计算都必须遵守[计算结果归档规范](CALCULATION_RESULT_ARCHIVAL_POLICY.zh-CN.md)：将必要的原生结果文件直接归档，不得新建 ZIP/TAR 来代替解压后的结果；记录运行来源和校验和，并在推送后从 GitHub 重新读取核对。超出普通 Git 存储能力的结果应使用 Git LFS 或带清单的持久版本化存储。

对于圈图匹配，应记录外部动量及其流向、费曼规则和符号、UV/IR 调节方式、重整化约定、EFT 减法处方、反项、算符基底、EOM/Fierz 约定，以及保留项的阶数。

## 8. Claim–Evidence Matrix（主张—证据矩阵）

新项目可从[主张—证据矩阵模板](../templates/claim-evidence-matrix.md)开始创建矩阵，并将实际使用的矩阵与该项目的规范记录放在一起维护。

每一行应对应一项可评估的物理陈述，并记录其假设和适用范围、推导证据、计算证据、独立检查状态、论文位置及下一步行动。

建议采用以下保守状态：

- **Proposed（待评估）：** 已提出主张，但证据评估尚未完成。
- **Supported（有证据支持）：** 指定证据在所声明范围内支持该主张。
- **Conditionally supported（有条件支持）：** 支持程度依赖明确的假设、基准点或限制条件。
- **Unresolved（未解决）：** 证据缺失、不完整或相互冲突。
- **Contradicted（被反驳）：** 已核查证据与主张冲突。
- **Superseded（已被替代）：** 后续评估结果取代了早期陈述。

不要把任务完成等同于主张成立。例如，一项任务可以因为已查明差异来源而完成，但对应的物理主张仍可能处于未解决状态。

## 9. 结构化记录校验器与项目注册表校验器

本仓库有两个用途不同的工具，必须按对象选择。

### 项目导航注册表

~~~bash
python skills/high-energy-theory-research/scripts/validate_project_registry.py --registry projects/registry.yaml --repo-root .
~~~

该命令仅检查项目层级元数据和声明路径。

### 结构化研究记录

~~~bash
python skills/high-energy-theory-research/scripts/validate_project_records.py path/to/project/records --project-root path/to/project
~~~

第二条命令要求输入目录只包含符合当前候选 Schema v1.4.3.7 约定的 JSON/YAML 记录。**不要**将 [`projects/registry.yaml`](../projects/registry.yaml) 或含 Markdown 笔记的目录传给它。候选 Schema 仍处于开发阶段；校验通过不代表 Schema 已正式批准，也不代表物理结论正确。

对于两种命令，都应检查完整报告，而不只是退出码。应依据来源证据修复错误，不要通过削弱 Schema 或虚构引用来消除失败。结构化记录校验器仍存在已记录的局限，包括状态机覆盖不完整，且不负责科学正确性认证。

## 10. Git、审查与发布纪律

- 尽量让每个分支或 Pull Request 只包含一项范围明确的研究变更。
- 确保基线和工作版本可识别。
- 审查实际 diff，而不只看提交说明或绿色状态。
- 针对最新的确切提交运行可用测试，并明确记录跳过、不可用或过期的检查。
- 避免将候选 Schema、迁移和物理研究内容混在一个无法独立审查的变更中。
- 不要因为文档整洁就合并研究变更；应单独检查其科学验收标准。
- 集成后检查默认分支的实际状态，并在研究记录中写入确切的集成版本。
- 不要仅为格式美观而重写历史或大规模移动文件。
- 结果推送后，必须从 GitHub 重新读取已提交文件，核对路径、大小和哈希；仅仅推送成功不等于归档验证完成。详见[计算结果归档规范](CALCULATION_RESULT_ARCHIVAL_POLICY.zh-CN.md)。

## 11. 文件组织与迁移

共享平台层用于存放可复用的方法、Schema、模板、文档、测试和工具。项目专属的物理研究记录与产物最终应能按项目/工作流清晰定位。

注册表用于导航各项目的规范研究仓库。RC-001 归档迁移已于 2026-11-23 完成：480 个文件的冻结源版本保存在 [axial-vector-review-response](https://github.com/lm846802297-bit/axial-vector-review-response/tree/main/research/rc001-vll-higgs-singlet-uv-eft)，中央基础设施仓库只保留导航元数据。请参阅[第一阶段注册表与迁移审计](PROJECT_REGISTRY_AUDIT.md)，了解迁移前审查和已完成的迁移记录。未来迁移其他工作流前必须：

1. 枚举所有待移动文件；
2. 审查 Markdown 链接、脚本导入、测试、CI 路径、Schema 路径规则和校验器假设；
3. 建立旧路径到新规范路径的一一映射；
4. 在一个可审查的变更中更新全部引用；
5. 在新提交上运行链接/路径检查及相关测试；
6. 保留 Git 历史并记录迁移映射；
7. 保持旧基线可识别；如果只改变路径，不得声称发生了科学内容变更。

除非单独完成设计、审查、版本管理和批准，不要将导航注册表纳入候选 Schema。

## 12. 当前项目示例

当前已登记的层级如下：

- **父项目：** `axial-vector-model-building`
- **工作流：** `vll-higgs-singlet-uv-eft`
- **归档入口：** [RC-001 归档 README](https://github.com/lm846802297-bit/axial-vector-review-response/blob/main/research/rc001-vll-higgs-singlet-uv-eft/README.md)
- **主研究记录：** [RC-001-vll-higgs-singlet-uv-eft.md](https://github.com/lm846802297-bit/axial-vector-review-response/blob/main/research/rc001-vll-higgs-singlet-uv-eft/upstream/research/RC-001-vll-higgs-singlet-uv-eft.md)
- **规范子图记录：** [RC-001-gauge-subgraph-change-record.md](https://github.com/lm846802297-bit/axial-vector-review-response/blob/main/research/rc001-vll-higgs-singlet-uv-eft/upstream/research/RC-001-gauge-subgraph-change-record.md)
- **主张矩阵：** [RC-001-claim-evidence-matrix.md](https://github.com/lm846802297-bit/axial-vector-review-response/blob/main/research/rc001-vll-higgs-singlet-uv-eft/upstream/research/RC-001-claim-evidence-matrix.md)

该工作目前处于验证进行中。部分解析积分与符号/代数子模块已有记录，但完整 Wilson 系数向量、所有相关规范/箱图贡献、统一算符基底约化以及独立图级验证仍未完成。该示例展示的是可追溯性和状态管理，不应被解读为完整匹配计算已经完成。

## 13. 常见问题

- **这应该是项目还是工作流？** 只有具有独立研究意义的计划才应成为顶层项目。如果属于轴矢量模型研究计划，就应登记为其内部工作流。
- **可以把结构化记录校验器用于注册表吗？** 不可以。`projects/registry.yaml` 应使用项目注册表校验器。
- **代数检查通过后，可以把物理主张标记为有证据支持吗？** 只有当该检查足以支撑这项具体主张及其适用范围时才可以，否则应记录缺失的独立证据。
- **CI 不可用怎么办？** 标记为未运行或受阻，不得标记为通过，也不要把软件验证限制与科学证据混为一谈。
- **RC-001 文件现在在哪里？** 480 个文件的冻结归档已迁移并合并至 [axial-vector-review-response](https://github.com/lm846802297-bit/axial-vector-review-response/tree/main/research/rc001-vll-higgs-singlet-uv-eft)。迁移其他工作流前，仍须完成路径、Schema、测试和工作流依赖审计。
- **可以登记其他研究主题吗？** 可以，但必须先确认其父项目关系；不要仅凭文件名推断归属。
