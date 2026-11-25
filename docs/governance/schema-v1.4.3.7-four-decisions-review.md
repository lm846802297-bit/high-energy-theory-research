# v1.6.6 四项规范决策审阅

## 基线与边界
- 设计文档 SHA-256：`49b113fe790b413851dbafafc0728426d6de74af05503a728dd687ebcbde2269`
- v1.4.3.6 bundle SHA-256：`aefb34e68af65daf8277b9553d232cab29ffb5df9c4f18c1cfe126474a06adf1`
- 本审阅以实际读取的 v1.6.6 文档候选段、§52.4、§56.2–§56.4、§58.2、§69.4、§73.1–§73.3 为依据。
- 以下全部为**推荐、待批准**；未将其写成正式规范，也未覆盖 v1.4.3.6。

## 决策 1：`artifact_storage_kind` 必需显式字段（DD-ART-007）
**推荐 A：** 必需 enum `file|directory`。理由是 §56.4 对 file/directory 的内容哈希规则不同。不能依赖 `artifact_type`、文件扩展名或 URI 猜测存储类型。

**兼容性：** 旧记录只能在来源证据足够时映射。不能确定时写入 `migration_review_items`，不得根据扩展名自动定值。

## 决策 2：目录清单规范化/哈希算法（DD-ART-008）
**推荐 A：** 采用 RFC 8785 JCS 序列化规范化后的 manifest 对象，再对 UTF-8 字节执行 SHA-256，输出 64 位小写十六进制摘要。

规范化步骤建议：
1. 对每个 `relative_path` 进行 Unicode NFC；将分隔符统一为 `/`。
2. 拒绝绝对路径、空路径、`.`/`..` 路径段、根目录外路径；默认拒绝符号链接。
3. 检查 NFC 后路径唯一，碰撞即硬错误，不得覆盖。
4. 按 NFC 后 POSIX 相对路径排序；清单的数组顺序由此固定。
5. `FileEntry` 使用固定结构；对 manifest 数组按 RFC 8785 JCS 生成 UTF-8 字节，不加 BOM、前后空白或尾部换行。
6. 对上述字节计算 SHA-256，保存小写十六进制值。
7. 文件 entry 的 `size_bytes` 与 `content_sha256` 由实际文件字节计算；目录 entry 仅在空目录语义重要或契约要求时登记；默认不跟随符号链接。

**边界：** §58.2 明确要求 NFC POSIX 路径排序及对规范化 manifest JSON 求哈希，但未明确点名 JCS 是目录 manifest 的最终序列化算法。因此 JCS 是强推荐，不是已批准规范。正式批准前，不应重算并覆盖历史哈希。

## 决策 3：`needs_review` 的状态语义（DD-ART-009）
**推荐 A：** 外部导入的普通文件没有原始字节 `content_sha256` 时，即使替代身份方法为 `verified`，`artifact_integrity_status` 仍为 `needs_review`。替代身份可证明 DOI/版本/来源标识在声明范围内匹配，但不证明本地字节与源字节相同。

这与 §52.4 的状态机相容：`needs_review → passed|failed|blocked` 必须由新检查/审查事件支持。`needs_review` 不是永远不可解除；它表示当前证据不足以给出字节级完整性结论。

## 决策 4：契约哈希与替代身份方法登记（DD-ART-010）
**推荐 A：** 将 `alternative_identity_methods` 的完整规范化内容纳入 TEC 的哈希载荷。方法登记是验收契约的一部分，变更它会改变契约语义。

- 对象键顺序由 JCS 处理；方法数组按稳定 `method_id` 排序后再规范化。
- 新增/修改方法必须产生新契约版本/ID 或明确 supersession；重新计算 `contract_sha256`。
- Artifact 必须引用精确的 `contract_id`、`contract_version`、`contract_sha256`、`method_id` 和方法版本。
- 迁移时若原始 TEC 哈希载荷不可恢复，不得声称已验证新哈希；保留旧哈希和源证据，将项目标记为待复核。

**待批准项：** 是否允许缺失登记表在迁移中显式转换为 `[]`。建议只有在迁移规则中声明并留下审计记录后才允许，不能静默补默认值。

## 配套兼容性与测试矩阵
四项决策的兼容性影响、正反测试及未验证门禁汇总于 [Schema v1.4.3.7 决策兼容性与测试矩阵](schema-v1.4.3.7-decision-compatibility-test-matrix.md)。该矩阵仅用于审查和实施规划，不构成任何决策批准。

## 本轮代码范围
本轮实现迁移器原型与跨记录校验器。目录 JCS 重算、真实文件系统遍历、状态事件哈希重算和科学验收仍按未实现/未运行报告。


## DD-ART-008 implementation comparison (non-normative)

A separate comparison of serialization/numeric-domain, normalized-path ordering, digest preimage scope, and symlink-policy alternatives is recorded in [DD-ART-008 decision options](schema-v1.4.3.7-dd-art-008-decision-options-2026-10-24.md). It is an implementation/review aid only; DD-ART-008 remains pending owner approval, and no Schema semantics or historical hashes have been changed.
