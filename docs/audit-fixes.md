# T19 审计修复记录

- 基线提交：`5252f1d`
- 修复范围：仅 `sections/ch01-overview.tex`、`ch02-foundations.tex`、`ch05-ci.tex`、`ch09-dft.tex`、`ch10-lda-gga.tex`、`ch16-summary.tex` 与三份审计报告；未改 `preamble.tex`、`main.tex`、`CONTRACT.md`、`refs.bib`、`data/`、`scripts/`、`runs/`。
- 验证方式：`latexmk -C` → `latexmk -xelatex` → `bibtex main` → 两次 `latexmk -xelatex`，全量重编译。

## 1. 修改前后对照

| # | 文件:行（修复后） | 修复前 | 修复后 | 审计来源 |
|---|---|---|---|---|
| F1 | `sections/ch02-foundations.tex:122-131` | `ΔE_BSSE=(E_A^AB+E_B^AB)-(E_A^A+E_B^B)`，右端 ≤0，与“扣除 BSSE”矛盾 | 两式对齐：`ΔE_BSSE=(E_A^A+E_B^B)-(E_A^AB+E_B^AB)≥0`；`ΔE_int^CP=E_AB^AB-E_A^AB-E_B^AB`；正文说明第一/第二式含义 | equation-audit F1 |
| F2 | `sections/ch05-ci.tex:157-164` | Davidson 因子 `1-Σ_{I≠0}|c_I|²`，实为参考态权重 `|c_0|²` | 因子改为 `1-|c_0|²`（激发组态权重）；正文同步改为“当 `1-|c_0|²` 较小……” | equation-audit F2 |
| F3 | `sections/ch05-ci.tex:195-201` | 右端 `-Σ_{p<q}Δ_pq`，符号与“误差为正、二次增长”相反 | 右端改为 `+Σ_{p<q}Δ_pq`；正文明确 `Δ_pq>0` 是被截掉的负相关贡献的绝对值 | equation-audit F3 |
| F4 | `sections/ch10-lda-gga.tex:159-166` | `Σ_i w_i f(r_i)`，`w_{Ai}` 只是无量纲划分权重，量纲不一致 | `Σ_A Σ_{i∈A} [P_A(r_i)/Σ_B P_B(r_i)] ω_i^(A) f(r_i)`；正文说明 `ω_i^(A)` 含径向 Jacobian | equation-audit F4 |
| F5a | `sections/ch01-overview.tex:145` | “20 个方法中有 18 个在 def2-TZVPP 下计算” | “20 个方法中，16 个用 def2-TZVPP；B97-3c 与 r$^2$SCAN-3c 使用各自内置基组（def2-mTZVP / def2-mTZVPP）；GFN2-xTB 与 GFN-FF 不含外部基组” | data-audit ch01:145；logic F1 |
| F5b | `sections/ch01-overview.tex:147` | “$0.6$–$1.5$ 步长 0.2，其后步长 0.5” | “$0.6$–$1.2$ 步长 0.2，随后 $1.5$，之后 $2.0$–$3.0$ 步长 0.5”（恰为 CSV 的 8 个点） | logic F2 |
| F5c | `sections/ch01-overview.tex:106` | caption“17 个方法的存在意义……” | caption“17 行（18 个方法；GFN2-xTB/GFN-FF 合并一行）的存在意义……” | logic §3.4 / data §11.3 |
| F6 | `sections/ch10-lda-gga.tex:2,6` | “LDA/GGA：密度泛函的**前两级阶梯**够用吗？” | “LDA/GGA：密度泛函前两级够用吗？”（与 Ch9 过渡句、`CONTRACT.md:207` 逐字一致） | logic F3 |
| F7a | `sections/ch16-summary.tex:207` | “省略 AuxC 会退回 AutoAux 或直接失败” | “省略 AuxC 会直接报错（不会自动退回四指数 MP2）” | logic F4 |
| F7b | `sections/ch16-summary.tex:205` | “先看 `⟨S²⟩` 与 `⟨S²⟩` 的增长” | “先看 `⟨S²⟩` 是否偏离纯自旋值” | T19 指定 |
| F7c | `sections/ch16-summary.tex:64` | “波函数方法的 ΔE 则为正” | “波函数方法的 ΔE 则为正或零”（CCSD(T) 为 0） | T19 指定 |
| F7d | `sections/ch16-summary.tex:61` | “是复合方法，不应把其基组……” | “是复合方法（不是雅各布天梯的新梯级），不应把其基组……” | logic N1 |
| F7e | `sections/ch16-summary.tex:153,176` | “$\omega$B97M-V（+D4）”“$\omega$B97M-V (+D4)” | “$\omega$B97M-V（已含 VV10）”（正文与 TikZ 叶） | logic N2 |
| F7f | `sections/ch16-summary.tex:174` | “双杂化\\大分子热化学 / 非共价” | “双杂化（非共价 +D3(BJ)）\\大分子热化学 / 非共价” | logic N3 |
| F7g | `sections/ch16-summary.tex:189-192` | 底部水平“成本 ↑（向右）”箭头，图注“成本向右递增” | 叶子右侧竖直箭头（`(5.55,-6.45) -- (5.55,-1.65)`），图注“成本向上递增” | logic N5 |
| F8 | `sections/ch01-overview.tex:129,138,145`；`sections/ch09-dft.tex:148,153` | `r\textsuperscript{2}SCAN`（6 处） | `r$^2$SCAN`（ORCA 关键词 `\texttt{! R2SCAN ...}` 未动） | T19 指定 |

## 2. 修复后验证

### 2.1 公式与计数

- 4 个 FAIL 公式按上表逐条复核，符号、因子、量纲均与标准约定一致。
- 第 1 章基组计数：16（def2-TZVPP）+ 2（B97-3c / r²SCAN-3c 内置）+ 2（GFN2-xTB / GFN-FF 无基组）= 20。
- H₂⁻ R 网格：0.6、0.8、1.0、1.2、1.5、2.0、2.5、3.0，共 8 点。
- 第 10 章标题 == `sections/ch09-dft.tex:216` 过渡句 == `CONTRACT.md:207`：“LDA/GGA：密度泛函前两级够用吗？”
- 第 16 章 AuxC 句与 `sections/ch13-double-hybrid.tex:123,172` 的“直接报错、不会自动退回四指数 MP2”一致（ORCA 6.1.1 实测）。

### 2.2 编译指标

| 指标 | 结果 |
|---|---|
| 编译退出码 | 0（pass1、bibtex、pass2、pass3 均为 0） |
| 页数 | 102（要求 95–105） |
| undefined reference | 0 |
| undefined citation | 0 |
| multiply-defined label | 0 |
| Missing character | 0 |
| PDF 中 `??` | 0 |
| Overfull `\hbox` | 5 处，最大 3.57pt（要求 ≤5 且每处 <10pt） |
| 编号公式 | 163，全部有 `\eqref`，无未引用 |
| 全书 label | 304，无重复 |
| `\cite` key | 60，全部存在于 `refs.bib` |

### 2.3 审计统计更新

| 报告 | 修复前 | 修复后 |
|---|---|---|
| `docs/equation-audit.md` | 159/163 PASS，4 FAIL | **163/163 PASS，0 FAIL** |
| `docs/logic-audit.md` | 12/16 章 PASS，4 FAIL | **16/16 章 PASS，0 FAIL** |
| `docs/data-audit.md` | 316/316 规定项 PASS；ch01:145 额外计数错误 | **316/316 PASS；ch01:145 已修复，额外检查 0 FAIL** |

### 2.4 未触碰的文件

`preamble.tex`、`main.tex`、`CONTRACT.md`、`refs.bib`、`data/`、`scripts/`、`runs/`，以及 `sections/ch03,04,06,07,08,11,12,13,14,15` 均未修改。未新增 label 或 bib key。CASSCF 2.0/1.0 叙事与 CH₄/H₂⁻ 数值未变。

## 3. 提交

```
fix: resolve all audit findings
```

仅暂存上述 6 个章节文件与 `docs/equation-audit.md`、`docs/logic-audit.md`、`docs/data-audit.md`、`docs/audit-fixes.md`；不包含 `main.pdf`、`.omo/`、`build-*`、`docs/build-check.md`。
