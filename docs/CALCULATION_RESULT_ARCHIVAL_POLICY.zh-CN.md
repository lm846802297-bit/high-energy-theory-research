# 计算结果归档规范

**状态：** 已采用的共享规范，适用于明确采用中央科研规范体系的研究仓库。

本规范适用于采用该规范的项目仓库中的解析/数值计算、模拟、参数扫描、数据处理、唯象学及计算验证。它补充[用户手册](USER_GUIDE.zh-CN.md)和[Scientific Diff 工作流](scientific-diff-workflow.md)。每个项目仓库自行维护产物索引或 `artifacts/README.md`，用于导航不可变产物包。本规范只规定结果如何保存和追溯，不自动证明物理结论正确。

## 1. 使用项目专属的规范研究目录

- 项目专属研究仓库：保存规范项目/工作流记录、专题代码、输入、结果、图像和审计记录。计算结果应与其规范研究变更记录放在一起；共享基础设施仓库只保留导航元数据。
- 在每个项目仓库内部，`calculations/` 用于保存可复用、可复现的符号或代数计算源码。
- 在每个项目仓库内部，`validation/` 用于保存实际运行产生的输出、数值检查和验证日志。必须区分已完成检查与计划中或尚未执行的检查。
- 在每个项目仓库内部，`artifacts/<bundle-id>/` 保存大型或二进制源码及计算产物的不可变、带哈希快照。遵守该仓库自己的产物索引或 `artifacts/README.md`；新版本应新建 bundle，不得覆盖既有快照。

遵循现有项目/工作流目录和记录约定。不要为了满足本规范而制造多个相互竞争的权威副本，也不要仅为目录整齐而迁移历史记录。

## 2. 提交可直接使用的原生结果文件，不要重新打包

- 在文件大小、许可和仓库规则允许时，直接提交计算实际产生或使用的原生数据文件，例如 CSV、JSON/JSONL、TXT、ROOT、HDF5、Parquet、notebook、源码、图像等。
- **不得新建 ZIP/TAR 压缩包来代替提交解压后的计算结果文件。** 审查者应能直接查看和使用实际数据文件，而不必先解压一个不透明的总包。
- 如果上游输入以压缩包形式提供，应提取计算所需文件，并在允许再分发时提交提取后的文件。来源记录中必须保留原压缩包文件名、来源/版本、字节数、SHA-256、解压命令及提取文件各自的校验和。不得悄然改变精度、单位、列顺序、换行符或原始数据。
- 原始输入、转换后的输入和派生结果必须明确区分。如果转换或后处理改变了数据，应在允许的范围内保留原始来源，并记录转换步骤及输出校验和。
- 如果工具本身产生的压缩格式就是原始数据产品，且确有必要，可以保留该原生格式，但必须记录格式和生成命令。这一例外不允许把普通结果重新封装为 ZIP/TAR。


## 2A. 生成图件与报告 PDF

对于渲染图、多面板图、带注释 PDF 和合并图件报告，遵循单独的[生成图件与报告产物规范](GENERATED_FIGURE_AND_REPORT_POLICY.zh-CN.md)。默认做法是归档科研数据、参考曲线、绘图/汇编源码、配置、依赖、溯源和哈希，需要查看时再生成 PDF/PNG/SVG。不要提交每一次预览或中间渲染。只有当精确渲染文件属于冻结的论文/报告交付物、正式批准的里程碑、外部流程要求的文件，或无法忠实重建时，才归档该快照；同时保留源数据和生成溯源。本规则细化可复现展示派生产物的处理方式，不放宽上述原生数据和运行溯源要求。

## 3. 大文件与受限数据

- 在文件大小、许可和仓库策略允许时，优先直接提交 Git。
- 对于不适合普通 GitHub Git 存储的大文件，使用 Git LFS 或仓库批准的、持久且有版本标识的存储位置。不得悄然省略文件，也不得用无法追溯的压缩包替代。
- 对外部存储文件，必须在仓库中提交清单，记录准确文件名、不可变下载 URI 或 Release 标识、版本、字节数、格式、来源和 SHA-256。优先保存独立的原生文件，而不是新生成的压缩包。
- 即将过期的 GitHub Actions artifact、临时工作区、聊天附件或仅存在于本地的文件，不得成为研究主张所依赖结果的唯一永久副本。
- 不得提交凭据、访问令牌、私钥、个人数据或项目无权再分发的输入。对受限输入应记录获取说明和校验和。

## 4. 必需的运行来源记录

每次重要计算都必须提供 `run_manifest.json`、YAML 或内容等价的完整运行记录。按适用情况至少记录：

- 精确的源码 commit，以及计算脚本/notebook 路径；
- 输入文件名、来源/版本、参数或配置文件及 SHA-256；
- 运行时、操作系统、编译器和相关软件包版本；
- 精确命令或执行流程；
- 影响结果解释的物理约定和数值设置：单位、参数、近似、网格、求积、精度、容差、边界条件和随机种子；
- 输出路径、格式、字节数、必要时的记录/行数及 SHA-256；
- 警告、失败或舍弃的运行、后处理、收敛检查和未解决的限制。

保留审查或恢复长时间计算所需的日志和 checkpoint。不要提交可丢弃的缓存、临时构建产物、虚拟环境或无关草稿。

## 4A. Reuse accepted calculation results; do not recompute without cause

**A result that has passed predeclared numerical and scientific acceptance criteria and has complete source/input provenance is reusable scientific evidence. A new PR, CI restart, documentation edit, archival-path change, or workflow adjustment alone is not a reason to recompute it.**

### 4A.1 Identify a reusable result

A reusable accepted result must be bound, as applicable, to:

- repository and full source commit SHA, plus hashes of the calculation scripts/notebooks actually used;
- paths, versions, and SHA-256 checksums of all input data, reference data, parameter files, and configurations;
- physical definitions and conventions: units, normalization, model assumptions, approximations, boundary conditions, and other result-affecting choices;
- numerical methods and settings: grids, integration/quadrature order, precision, tolerances, random seeds, and parallel settings;
- execution environment: operating system, runtime, compiler, and relevant dependency versions;
- native output files and their SHA-256 checksums;
- predeclared acceptance criteria, actual validation methods/results, and locatable logs/reports.

Together these fields form the result's *calculation fingerprint*. A filename, PR number, green CI status, or verbal statement alone does not establish equivalence between calculation versions.

### 4A.2 When to reuse directly

When the calculation fingerprint relevant to the current task matches the accepted record, and the supported scientific claim and scope are unchanged:

1. cite the native result and its exact version;
2. cite the existing convergence, error-analysis, and independent-validation evidence;
3. perform necessary integrity/hash checks on the existing files and verify their archival location;
4. record this task as “reuse of an accepted result,” identifying the reused run ID, commit, input/output hashes, and validation record;
5. do not rerun expensive physics calculations or duplicate a calculation merely to obtain a new CI record.

Hash verification, metadata checks, result-table comparisons, and archival checks are lightweight verification; they are not reruns of the original calculation. If the result files, source, and inputs are unchanged, the existing independent validation remains valid; do not repeat it merely to “prove it again.”

### 4A.3 When recalculation or targeted revalidation is justified

Recompute only the affected part when there is a concrete, relevant change or new evidence, for example:

- a source-code or algorithm change that may alter numerical results;
- a change in the content/version of input data, parameters, configuration, data transformation, or reference data;
- a change in physical definitions, sign conventions, normalization, approximations, model assumptions, or the target scientific claim;
- a change in numerical method, precision, grid, quadrature, tolerance, random seed, or execution environment that may affect the result;
- discovery of an actual error, numerical instability, failed convergence, checksum mismatch, or new independent evidence contradicting the old result;
- evidence that the previous validation scope is insufficient for a stronger claim now being made.

Scope revalidation along the dependency graph: check the downstream components affected by the changed input, code module, result, or claim. Do not treat unrelated documentation edits, plot-style changes, file moves, README additions, PR reopenings, or CI configuration changes as automatic reasons to recompute all physics results. If a change affects only presentation, regenerate the figure without recomputing its upstream numerical data.

### 4A.4 Keep calculation, validation, and archival status distinct

Record these separately:

- **Calculation status:** result produced, or not yet executed;
- **Scientific-validation status:** which predeclared checks passed, were not run, or are not applicable;
- **Archival status:** whether native results, source, inputs, and provenance are durably stored and verified;
- **Reuse status:** whether this task reuses an accepted result or performs targeted recalculation because of a specified change.

A historical calculation passing does not automatically validate new modifications; equally, not rerunning a calculation in a new PR does not invalidate the existing result. Do not report “not recomputed this round” as “validation failed,” and do not report a matching checksum as a new independent physics validation.

### 4A.5 CI and automation requirements

- CI should select checks according to changed paths and dependency relationships. Documentation-only, presentation-only, or non-calculation workflow changes should not automatically trigger every expensive numerical calculation.
- When a task reuses an accepted result, CI may verify source/input/output hashes, manifest completeness, and consistency of result summaries with frozen references. A full physics rerun is not required unless one of the recalculation triggers above applies.
- Multiple workflows must not concurrently recompute the same result or overwrite each other merely because an automated archive commit changed a result directory. Archival should be idempotent and keyed to an explicit result identity, with deliberate commit-conflict handling.
- Independent replay is valuable, but should be performed for initial acceptance, a relevant dependency change, or a concrete discrepancy—not as a default full recomputation for every PR.

This section applies together with the [minimum-sufficient-acceptance and historical-validation-reuse principles in the Research Quality Gate](governance/RESEARCH_QUALITY_GATE.md). Preserve the stricter provenance requirements, but do not expand the recalculation scope without evidence.

## 5. 验证并核对远端提交

1. 提交前检查文件完整性、预期文件/行数、单位、数值有限性和该计算专属的验收标准。失败、部分完成或尚未运行的检查必须如实记录。
2. 将结果、源码或精确源码版本、来源记录及清单放在独立工作分支和聚焦的 Pull Request 中。
3. 推送后检查实际 PR diff，并从 GitHub 重新读取已提交文件。将远端路径、文件数量、大小和 SHA-256 与本地提交逐项核对。
4. 分开报告仓库归档状态和科学验证状态。成功 commit、校验和一致、CI 通过或计算程序正常结束，都不能单独证明物理结果正确或研究主张已经成立。

## 6. 结构化 JSON/CSV 结果记录

新产生的重要数值计算应遵循已正式采用的[结构化科研结果数据规范 v1.0.1](STRUCTURED_RESULT_DATA_STANDARD_v1.0.1.zh-CN.md)，并使用 `schemas/research-result-record-v1.0.1.schema.json` 校验 `run_manifest`、`result_summary` 和 `validation_report`。运行来源、科学结果和验证报告分开记录；逐点数组保存为带明确单位的原生表格。该归档数据规范独立于尚未发布的研究记录 Schema v1.4.3.7 候选包。

本规范适用于本仓库今后的所有项目和工作流。
