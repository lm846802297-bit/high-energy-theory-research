# 项目注册表

语言：简体中文。英文原版：[README.md](README.md)。

本目录是 **High-Energy Theory Research** 平台的导航层，用于区分父研究项目、项目内工作流、Scientific Diff 研究变更记录、单次计算运行以及物理主张。

## 已登记项目

当前注册表只包含一个已确认的顶层项目及其已知 UV–EFT 工作流。只有在确认其他研究主题在仓库中的实际存在及其父项目关系后，才会将其登记为顶层项目，以避免臆测项目边界。

注册表位于 [registry.yaml](registry.yaml)。它是导航元数据，**不是**规范的 Schema v1.4.3.7 记录，因此与结构化项目记录校验器分开。可使用[注册表校验脚本](../skills/high-energy-theory-research/scripts/validate_project_registry.py)检查层级和声明路径。完整操作流程参见[中文用户手册](../docs/USER_GUIDE.zh-CN.md)。

### 轴矢量模型构建

顶层研究项目是 **axial-vector-model-building**。**vll-higgs-singlet-uv-eft** 工作流属于该项目内部的研究分支，不是独立的顶层项目。

建立注册表期间，该工作流的现有记录继续保留在原路径：

- 主研究记录：[research/RC-001-vll-higgs-singlet-uv-eft.md](../research/RC-001-vll-higgs-singlet-uv-eft.md)
- 规范子图工作流记录：[research/RC-001-gauge-subgraph-change-record.md](../research/RC-001-gauge-subgraph-change-record.md)
- 主张—证据矩阵：[research/RC-001-claim-evidence-matrix.md](../research/RC-001-claim-evidence-matrix.md)
- 当前活跃记录的共享索引：[research/README.zh-CN.md](../research/README.zh-CN.md)

引入注册表没有移动、重命名或重新归类任何文件。尤其要注意，RC-001 是研究变更/记录 ID，不是父项目 ID。

参见[第一阶段注册表与迁移预审](../docs/PROJECT_REGISTRY_AUDIT.md)，了解已执行的检查和仍需满足的迁移门槛。

## 身份与层级规则

1. **项目（Project）** — 具有自身研究范围和顶层状态的持续研究计划，例如 `axial-vector-model-building`。
2. **工作流（Workstream）** — 项目内部范围明确的一条研究分支，例如 `vll-higgs-singlet-uv-eft`。
3. **研究变更（Research change）** — 有基线、证据和下游影响记录的可追溯科学变更，例如 `RC-001`。
4. **运行（Run）** — 一次具有明确源码版本、输入、环境和输出的实际执行。不能仅因为存在脚本或验证日志，就推断某次运行已发生。
5. **主张（Claim）** — 独立追踪范围与证据的物理陈述，例如 `CL-015`。

不要仅仅因为某个工作流有自己的目录、论文小节、计算类别或 Git 分支，就新建顶层项目。只有当它具有独立且有意义的研究范围及所有权/生命周期时，才应单独建项。

## 添加项目或工作流

1. 从[项目记录模板](../templates/project-record.md)开始。
2. 将项目/工作流加入 `registry.yaml`，使用稳定标识符，并链接到其规范记录。
3. 注册表应保持描述性和保守性：没有证据时使用 `unknown` 或省略可选元数据，不要编造仓库 URL、基线或状态证据。
4. 登记项目时不要移动已有研究产物。
5. 未来迁移文件前，应审计 Markdown 链接、Schema 路径规则、校验器假设、测试、脚本和 CI 引用；每次只迁移一条工作流。
6. 将软件验证状态与科学验证状态分开记录。

## 当前实现边界

第一阶段仅登记项目层级，并提供可复用的项目记录模板。它不会引入新的规范 Schema，不会修改候选 Schema 包，不会自动迁移文件，也不会认证任何物理结果。

注册表校验命令：

~~~bash
python skills/high-energy-theory-research/scripts/validate_project_registry.py --registry projects/registry.yaml --repo-root .
~~~
