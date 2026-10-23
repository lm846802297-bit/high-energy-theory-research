# 端到端研究 Skill 试点：\(2\times2\) 质量平方矩阵

语言：简体中文。英文原版：[README.md](README.md)。

## 目的与适用边界

这是一个规模较小、确定性的可复现工作流试点，用于测试可复用研究 Skill 的基本流程。它覆盖任务接收、明确单位与假设、解析计算、独立检查、结果产物生成，以及合成的候选记录链。

本试点**不**被宣称为真实物理模型的结果。它不测试规范不变性、标量势、微扰性、UV/EFT 匹配或实验约束。

## 输入与推导

输入为实对称矩阵

\[
M^2 = \begin{pmatrix}5&2\\2&8\end{pmatrix}\;\mathrm{TeV}^2.
\]

对于对称矩阵 \(\begin{pmatrix}a&b\\b&d\end{pmatrix}\)，其特征方程给出

\[
\lambda_{\pm}=\frac{a+d\pm\sqrt{(a-d)^2+4b^2}}{2}.
\]

本例中 \(a+d=13\)、\(ad-b^2=36\)，判别式为 \(5\)，因此本征值为 \(4\) 和 \(9\;\mathrm{TeV}^2\)，对应质量为 \(2\) 和 \(3\;\mathrm{TeV}\)。

## 独立检查

测试框架会验证：

- 根据本征值重建的迹与行列式；
- 本征向量的归一化和正交性；
- 本征对残差；
- 使用顺序主子式和行列式检查正定性。

运行命令：

~~~bash
python tests/eval-cases/analytic-mass-matrix-pilot/run_pilot.py
~~~

脚本仅使用 Python 标准库。独立验收值记录在 `expected-results.json` 中。

## 候选记录链与当前局限

单元测试会构造一条合成的记录链：

Task → 已批准的测试契约 → Run Plan → Run → Run Manifest → Artifact → Validation Plan/Activity/Report → Evidence Fragment → Claim。

随后使用候选 Schema 对其进行验证。生成的结果文件会执行哈希检查，本地来源/产物路径也会受到检查。

当前候选版本将 FingerprintInputs 定义为带版本的输入声明。源文件字节和输入产物必须显式提供 SHA-256 摘要；配置、代码和环境组件必须提供记录 ID 与组件摘要，或提供 null 并附带明确的不适用理由。执行规格和指纹载荷使用 RFC 8785 规范化。用于哈希的来源/产物条目按 ID 排序，重复 ID 会被拒绝，Run Manifest 绑定包会根据声明输入重新计算。

位于 `tests/fixtures/fingerprint-inputs-v1/golden-vector.json` 的黄金测试向量固定了规范 JSON 字节及预期 SHA-256 值。单元测试检查顺序无关性、重复 ID 拒绝、执行规格篡改、组件语义和跨记录一致性。候选契约仍待审查批准；真实物理任务试点是单独的验收门槛。
