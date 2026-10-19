# T18 LaTeX/数据对账审计报告

- 仓库：`/home/xieningke/课程/计算化学/泛函详解`
- 审计日期：2026-10-20
- 审计基线：`5252f1d`
- 数据源：`data/ch4_results.csv`、`data/h2m_pes.csv`、`data/h2m_occupations.csv`、`refs.bib`
- 审计方式：Python 3（csv/re）+ grep + 既有 `.aux`/`main.log`；未重新编译、未修改任何章节文件。

## 1. 总结

| # | 检查项 | 断言数 | PASS | FAIL |
|---|--------|-------:|-----:|-----:|
| 1 | ch4box 总能 vs CSV（6 位小数） | 33 | 33 | 0 |
| 2 | ch4box ΔE vs 精确值重算（2 位小数） | 20 | 20 | 0 |
| 3 | ch4box 内部算式中间量（差值/相关能） | 8 | 8 | 0 |
| 4 | 图/表 label 均被正文 `\ref` 引用 | 23 | 23 | 0 |
| 5 | 公式 label 均有 `\eqref` | 163 | 163 | 0 |
| 6 | `\cite` key 均存在于 `refs.bib` | 60 | 60 | 0 |
| 7 | 术语一致性 | 5 | 5 | 0 |
| 8 | 全书 label 无重复 | 1（304 个 label） | 1 | 0 |
| 9 | 第 16 章 CH4/H2- 汇总表 | 2 | 2 | 0 |
| 10 | 图表编号连续（spot-check `.aux`） | 1 | 1 | 0 |
| **合计** | | **316** | **316** | **0** |

**规定检查项：0 FAIL。**

另有 1 个超出上述数值对账清单的正文计数错误（不影响任何 ch4box、图表、公式或引用），见第 11 节：

- `sections/ch01-overview.tex:145`：“20 个方法中有 18 个在 def2-TZVPP 下计算”与 CSV 基组列不符（实际 16 个）。

## 2. ch4box 总能审计

规则：box 中的 6 位小数若等于 CSV `energy` 的 6 位舍入值，或等于 CSV 精确值（允许“精确值 + 舍入值”成对出现），即 PASS。全部 13 个 `ch4box`（第 3–15 章；第 16 章无 `ch4box`）均通过。

| 章 | box 位置 | 方法 | box 引用值 | CSV 6 dp | CSV 精确值 | 结论 |
|---|----------|------|-----------:|---------:|-----------:|:----:|
| 3 | `sections/ch03-hf.tex:231` | HF | −40.214415 | −40.214415 | −40.214414724759 | PASS |
| 3 | `sections/ch03-hf.tex:231` | CCSD(T) | −40.438598 | −40.438598 | −40.438597868462 | PASS |
| 4 | `sections/ch04-mp2.tex:203` | MP2 | −40.412099 | −40.412099 | −40.412098578202 | PASS |
| 4 | `sections/ch04-mp2.tex:203` | HF（参考） | −40.214415 | −40.214415 | −40.214414724759 | PASS |
| 5 | `sections/ch05-ci.tex:206` | CISD | −40.422685 | −40.422685 | −40.422684814182 | PASS |
| 5 | `sections/ch05-ci.tex:206` | CCSD(T)（参考） | −40.438598 | −40.438598 | −40.438597868462 | PASS |
| 6 | `sections/ch06-cc.tex:229` | CCSD(T) | −40.438598（并给出 −40.438597868462） | −40.438598 | −40.438597868462 | PASS |
| 6 | `sections/ch06-cc.tex:229` | CISD | −40.422685 | −40.422685 | −40.422684814182 | PASS |
| 7 | `sections/ch07-casscf.tex:203` | CASSCF(8,8) | −40.297163（并给出 −40.297162861153） | −40.297163 | −40.297162861153 | PASS |
| 8 | `sections/ch08-mrpt-mrci.tex:163` | CASPT2 | −40.420721（并给出 −40.420720703026） | −40.420721 | −40.420720703026 | PASS |
| 8 | `sections/ch08-mrpt-mrci.tex:163` | NEVPT2 | −40.405834（并给出 −40.405833810464） | −40.405834 | −40.405833810464 | PASS |
| 8 | `sections/ch08-mrpt-mrci.tex:163` | MRCI | −40.428596（并给出 −40.428596004396） | −40.428596 | −40.428596004396 | PASS |
| 8 | `sections/ch08-mrpt-mrci.tex:163` | CCSD(T)（参考） | −40.438598 | −40.438598 | −40.438597868462 | PASS |
| 9 | `sections/ch09-dft.tex:189` | PBE | −40.464324（并给出 −40.464323928376） | −40.464324 | −40.464323928376 | PASS |
| 9 | `sections/ch09-dft.tex:189` | CCSD(T) | −40.438598（并给出 −40.438597868462） | −40.438598 | −40.438597868462 | PASS |
| 10 | `sections/ch10-lda-gga.tex:178` | SVWN5（LDA） | −40.117774 | −40.117774 | −40.117773578800 | PASS |
| 10 | `sections/ch10-lda-gga.tex:178` | PBE（GGA） | −40.464324 | −40.464324 | −40.464323928376 | PASS |
| 10 | `sections/ch10-lda-gga.tex:178` | B97-3c | −40.497380 | −40.497380 | −40.497379885896 | PASS |
| 10 | `sections/ch10-lda-gga.tex:178` | CCSD(T)（参考） | −40.438598 | −40.438598 | −40.438597868462 | PASS |
| 11 | `sections/ch11-meta-gga.tex:143` | TPSS | −40.541484 | −40.541484 | −40.541483557685 | PASS |
| 11 | `sections/ch11-meta-gga.tex:143` | r$^2$SCAN | −40.500987 | −40.500987 | −40.500987222276 | PASS |
| 11 | `sections/ch11-meta-gga.tex:143` | r$^2$SCAN-3c | −40.494868 | −40.494868 | −40.494867680722 | PASS |
| 11 | `sections/ch11-meta-gga.tex:143` | CCSD(T)（参考） | −40.438598 | −40.438598 | −40.438597868462 | PASS |
| 12 | `sections/ch12-hybrid.tex:143` | B3LYP | −40.503278 | −40.503278 | −40.503277669626 | PASS |
| 12 | `sections/ch12-hybrid.tex:143` | ωB97M-V | −40.492948 | −40.492948 | −40.492948404733 | PASS |
| 12 | `sections/ch12-hybrid.tex:143` | CCSD(T)（参考） | −40.438598 | −40.438598 | −40.438597868462 | PASS |
| 13 | `sections/ch13-double-hybrid.tex:135` | B2PLYP | −40.487287 | −40.487287 | −40.487286977330 | PASS |
| 13 | `sections/ch13-double-hybrid.tex:135` | PWPB95 | −40.489598 | −40.489598 | −40.489597965231 | PASS |
| 13 | `sections/ch13-double-hybrid.tex:135` | CCSD(T)（参考） | −40.438598 | −40.438598 | −40.438597868462 | PASS |
| 14 | `sections/ch14-xtb.tex:150` | GFN2-xTB | −4.175157（并给出 −4.175157467990） | −4.175157 | −4.175157467990 | PASS |
| 14 | `sections/ch14-xtb.tex:150` | CCSD(T)（参考） | −40.438598 | −40.438598 | −40.438597868462 | PASS |
| 15 | `sections/ch15-force-field.tex:171` | GFN-FF | −0.630874（并给出 −0.630873896930） | −0.630874 | −0.630873896930 | PASS |
| 15 | `sections/ch15-force-field.tex:171` | CCSD(T)（参考） | −40.438598 | −40.438598 | −40.438597868462 | PASS |

合计 33 个方法—box 组合，33 PASS，0 FAIL。第 14/15 章未报告 GFN2-xTB/GFN-FF 相对 CCSD(T) 的 ΔE，并用“与量子化学方法不可直接比较”说明，符合 CSV 的能量零点事实。

## 3. ch4box ΔE 审计

规则：`ΔE = (E_method − E_CCSD(T)) × 627.509474`，用 CSV 未舍入值重算，检查 box 引用的 2 位小数。全部 PASS，无符号或 627.509474 因子错误。

| 章 | 方法 | box 引用 ΔE | 精确重算 | 2 dp 舍入 | 结论 |
|---|------|------------:|---------:|----------:|:----:|
| 3 | HF | +140.68 | 140.677047 | +140.68 | PASS |
| 4 | MP2 | +16.63 | 16.628556 | +16.63 | PASS |
| 5 | CISD | +9.99 | 9.985592 | +9.99 | PASS |
| 6 | CCSD(T) | 0.00 | 0.000000 | 0.00 | PASS |
| 6 | CISD | +9.99 | 9.985592 | +9.99 | PASS |
| 7 | CASSCF(8,8) | +88.75 | 88.751807 | +88.75 | PASS |
| 8 | CASPT2 | +11.22 | 11.218091 | +11.22 | PASS |
| 8 | NEVPT2 | +20.56 | 20.559757 | +20.56 | PASS |
| 8 | MRCI | +6.28 | 6.276264 | +6.28 | PASS |
| 9 | PBE | −16.14 | −16.143346 | −16.14 | PASS |
| 10 | SVWN5 | +201.32 | 201.320281 | +201.32 | PASS |
| 10 | PBE | −16.14 | −16.143346 | −16.14 | PASS |
| 10 | B97-3c | −36.89 | −36.886273 | −36.89 | PASS |
| 11 | TPSS | −64.56 | −64.561745 | −64.56 | PASS |
| 11 | r$^2$SCAN | −39.15 | −39.149911 | −39.15 | PASS |
| 11 | r$^2$SCAN-3c | −35.31 | −35.309840 | −35.31 | PASS |
| 12 | B3LYP | −40.59 | −40.587188 | −40.59 | PASS |
| 12 | ωB97M-V | −34.11 | −34.105476 | −34.11 | PASS |
| 13 | B2PLYP | −30.55 | −30.552877 | −30.55 | PASS |
| 13 | PWPB95 | −32.00 | −32.003044 | −32.00 | PASS |

第 14/15 章按设计不报告 ΔE（N/A，不计入 FAIL）。

### 3.1 box 内部算式中间量

| 章 | 中间量 | box 引用值 | 由 CSV 精确值重算 | 结论 |
|---|--------|-----------:|------------------:|:----:|
| 3 | E_HF − E_CCSD(T) | 0.224183 | 0.224183143703 | PASS |
| 4 | E_MP2 − E_HF（相关能） | −0.197684 | −0.197683853443 | PASS |
| 4 | E_MP2 − E_CCSD(T) | 0.026499 | 0.026499290260 | PASS |
| 9 | E_PBE − E_CCSD(T) | −0.025726 | −0.025726059914 | PASS |
| 12 | E_B3LYP − E_CCSD(T) | −0.064680 | −0.064679801164 | PASS |
| 12 | E_ωB97M-V − E_CCSD(T) | −0.054350 | −0.054350536271 | PASS |
| 13 | E_B2PLYP − E_CCSD(T) | −0.048689 | −0.048689108868 | PASS |
| 13 | E_PWPB95 − E_CCSD(T) | −0.051000 | −0.051000096769 | PASS |

第 12 章“ωB97M-V 的偏差比 B3LYP 小约 6.5 kcal·mol⁻¹”经重算为 6.4817，PASS；第 13 章“B2PLYP 比 PWPB95 高约 1.45 kcal·mol⁻¹”经重算为 1.4502，PASS。

## 4. 图/表引用审计

全书共 6 个图和 17 个表（含第 10/11 章的 `\captionof{table}`、第 16 章的 `\captionof{figure}`，以及附录 2 个表）：章级浮动体 21 个（6 图 + 15 表），附录表 2 个。每个 `\label{ch:XX:fig:...}` / `\label{ch:XX:tab:...}` 都在同一章正文中至少被 `\ref` 一次；附录 `app:tab:csv` / `app:tab:glossary` 也均被引用。无孤立图/表。所有编号图/表（含 `longtable` 与 `\captionof`）均带 label；未发现无 label 的图/表。

| 章 | label | label 行 | 引用行（同章） | 结论 |
|---|-------|---------:|----------------|:----:|
| 1 | `ch:01:fig:map` | 82 | 31 | PASS |
| 1 | `ch:01:tab:methods` | 106 | 101, 111, 157, 173 | PASS |
| 2 | `ch:02:tab:basis` | 105 | 96 | PASS |
| 2 | `ch:02:tab:properties` | 203 | 198 | PASS |
| 2 | `ch:02:tab:symbols` | 222 | 51 | PASS |
| 3 | `ch:03:tab:variants` | 184 | 179 | PASS |
| 4 | `ch:04:tab:variants` | 172 | 167 | PASS |
| 5 | `ch:05:tab:hierarchy` | 86 | 81 | PASS |
| 6 | `ch:06:tab:compare` | 214 | 209 | PASS |
| 7 | `ch:07:fig:h2m` | 161 | 153, 196 | PASS |
| 7 | `ch:07:tab:h2m` | 172 | 164, 189, 196 | PASS |
| 8 | `ch:08:tab:compare` | 124 | 118, 137 | PASS |
| 8 | `ch:08:fig:h2m-mr` | 150 | 142, 153 | PASS |
| 9 | `ch:09:fig:ladder` | 185 | 143 | PASS |
| 10 | `ch:10:tab:ch4` | 195 | 179 | PASS |
| 11 | `ch:11:tab:ch4` | 160 | 144 | PASS |
| 16 | `ch:16:tab:ch4-summary` | 30 | 19, 64, 69, 82, 87, 113, 148, 209, 214 | PASS |
| 16 | `ch:16:fig:deviations` | 74 | 61, 69, 77, 214 | PASS |
| 16 | `ch:16:tab:cost` | 88 | 82, 214 | PASS |
| 16 | `ch:16:tab:h2m-summary` | 124 | 118, 142, 205, 214 | PASS |
| 16 | `ch:16:fig:tree` | 193 | 153, 214 | PASS |
| 附录 | `app:tab:csv` | `appendix/app-data.tex:31` | 同文件 25 | PASS |
| 附录 | `app:tab:glossary` | `appendix/app-glossary.tex:13` | 同文件 9, 18 | PASS |

合计 23 个图/表 label（6 图 + 17 表），23 PASS，0 未引用。

## 5. 公式引用审计

共 163 个 `\label{ch:XX:eq:...}`，全部在对应章内有至少一个 `\eqref{...}`，无孤立公式 label。

| 章 | 公式 label 数 | 被 `\eqref` 数 | 结论 |
|---|-------------:|---------------:|:----:|
| 1 | 0 | 0 | N/A |
| 2 | 16 | 16 | PASS |
| 3 | 17 | 17 | PASS |
| 4 | 13 | 13 | PASS |
| 5 | 13 | 13 | PASS |
| 6 | 16 | 16 | PASS |
| 7 | 10 | 10 | PASS |
| 8 | 8 | 8 | PASS |
| 9 | 12 | 12 | PASS |
| 10 | 12 | 12 | PASS |
| 11 | 10 | 10 | PASS |
| 12 | 9 | 9 | PASS |
| 13 | 8 | 8 | PASS |
| 14 | 8 | 8 | PASS |
| 15 | 10 | 10 | PASS |
| 16 | 1 | 1 | PASS |
| **合计** | **163** | **163** | **PASS** |

## 6. 引文审计

- 全书的 `\cite` / `\citep` / `\citet`（含可选参数与多 key）共收集到 60 个唯一 key。
- `refs.bib` 有 63 个唯一 entry；60 个被引用 key 全部存在，**0 个缺失 / 0 个未定义**。
- `main.log` 中无 “Citation ... undefined” 或 “There were undefined references” 警告。
- 未被引用的 bib entry（仅提示，不是 FAIL）：`cramer2004`、`ernzerhof1999`、`neese2012orca`。

## 7. 术语一致性审计

| 术语/检查 | 结果 | 位置与计数 | 结论 |
|-----------|------|------------|:----:|
| 尺寸一致性（禁用“大小一致性”） | “大小一致性” 0 次；“尺寸一致性” 24 次 | ch01:5、ch02:7、ch04:2、ch05:4、ch06:3、ch08:1、ch13:2 | PASS |
| 活性空间（禁用“活化空间”） | “活化空间” 0 次；“活性空间” 75 次 | ch01:8、ch02:1、ch07:34、ch08:29、ch16:3 | PASS |
| r$^2$SCAN 拼写 | 正文 38 次 `r$^2$SCAN`、6 次 `r\textsuperscript{2}SCAN`；`R2SCAN` 仅 3 次、裸 `r2SCAN` 仅 1 次，且全部位于 `\texttt{! ...}` ORCA 关键词内 | ch01:129、ch09:148/153 用 `\textsuperscript`；ch01:129、ch11:22/144 为 ORCA 关键词 | PASS（渲染一致；可选统一为 `r$^2$SCAN`） |
| 复合方法 | Ch10 6 次、Ch11 7 次、Ch16 5 次；另有 Ch9 1 次 | `sections/ch10-lda-gga.tex`, `ch11-meta-gga.tex`, `ch16-summary.tex` | PASS |
| 不可直接比较 | Ch14 2 次、Ch15 2 次、Ch16 2 次；另有 Ch1 1 次 | `sections/ch14-xtb.tex:156/162`、`ch15-force-field.tex:177/183`、`ch16-summary.tex:61/209` | PASS |

## 8. label 重复审计

- 全书（`sections/*.tex` + `appendix/*.tex`）共 304 个 `\label`，唯一 label 304 个，**重复 0 个**。
- 无 `\ref` 指向不存在的 label（`UNDEFINED REFS: none`）。
- 说明：约 116 个 `sec:` 级 label 未被 `\ref` 引用，这是章节结构的正常情况；T18 的孤立 label 检查范围为 fig/tab/eq，三者均为 0 孤立。

## 9. 第 16 章汇总表审计

### 9.1 CH4 20 方法表（`ch:16:tab:ch4-summary`，`sections/ch16-summary.tex:30`）

- 数据行：第 36–55 行，恰好 **20 行**。
- 方法集合与 `data/ch4_results.csv` 的 20 个方法 **完全一致**（无多、无缺）。
- 20 个总能：全部等于 CSV `energy` 的 6 位舍入值，PASS。
- 18 个可比较方法的 ΔE：全部等于 `(E−E_CCSD(T))×627.509474` 的 2 位舍入值，PASS。
- GFN2-xTB 与 GFN-FF 的 ΔE 列为“—”，与“不可直接比较”的正文/表注一致，PASS。

### 9.2 H2- 表（`ch:16:tab:h2m-summary`，`sections/ch16-summary.tex:124`）

- 方法行：UHF、MP2、CCSD(T)、CASSCF、NEVPT2、MRCI，共 **6 个方法**。
- 每个方法取 R = 0.6、1.5、3.0 Å，共 18 个能量，全部与 `data/h2m_pes.csv` 的 `energy` 6 位舍入值一致，PASS。
- 另有 UHF ⟨S²⟩ 行：0.754473 / 0.764251 / 0.821141，与 CSV `s2` 列完全一致，PASS。
- 正文引用的派生量复核：CASSCF 高于 UHF 0.0012–0.0131 Eh；NEVPT2 低于 CASSCF 0.0331–0.0391 Eh；MRCI 低于 NEVPT2 0.0129–0.0137 Eh；⟨S²⟩ 增量 0.066668；均 PASS。

### 9.3 成本表（`ch:16:tab:cost`）

非必审项，顺带核对：表中 ΔE 与 20 方法总表一致（+201.32、−16.14、−64.56/−39.15、−40.59、−34.11、−30.55/−32.00、+140.68、+16.63、0.00、+88.75、+20.56/+6.28），PASS。

## 10. 图表编号连续性

用既有 per-chapter `.aux` 与 `main.log` spot-check（未重编译）：

- 图：1.1；7.1；8.1；9.1；16.1–16.2。无跳号。
- 表：1.1；2.1–2.3；3.1；4.1；5.1；6.1；7.1；8.1；10.1；11.1；16.1–16.3。无跳号。
- 第 12–15 章没有浮动图表，计数器无空洞。
- `main.log` 有 102 页输出，无 undefined reference/citation 警告；唯一 LaTeX Warning 是 `h` float specifier 被改为 `ht`，不影响编号。

## 11. FAIL 清单

### 11.1 规定检查项

**无。** 316/316 PASS。

### 11.2 额外发现（超出规定数值对账清单，但属于全书数据一致性）

| 严重度 | 位置 | 问题 | 建议修正 |
|--------|------|------|----------|
| 低（正文计数） | `sections/ch01-overview.tex:145` | 原文“20 个方法中有 18 个在 def2-TZVPP 下计算，B97-3c 与 r²SCAN-3c 使用各自内置基组”。按 `data/ch4_results.csv` 的 `basis` 列：def2-TZVPP 16 个、def2-mTZVP/def2-mTZVPP 2 个、无基组 2 个（GFN2-xTB、GFN-FF）。18 是“量子化学方法数”，不是“def2-TZVPP 方法数”。 | 改为：“20 个方法中有 18 个是量子化学方法：16 个在 def2-TZVPP 下计算，B97-3c 与 r²SCAN-3c 使用各自内置基组；GFN2-xTB 与 GFN-FF 无基组。” |

### 11.3 观察项（不判 FAIL）

- `sections/ch01-overview.tex:106` 表 caption 写“17 个方法”，但该表为 17 行、其中最后一行合并 GFN2-xTB 与 GFN-FF，实际代表 18 个方法；小节标题“方法存在意义表（17 行）”是准确的行数。建议将 caption 改为“17 行（18 个方法；GFN2-xTB/GFN-FF 合并一行）”，避免与第 16 章的“20 个方法”混淆。
- `refs.bib` 有 3 个未使用 entry：`cramer2004`、`ernzerhof1999`、`neese2012orca`。不影响引文完整性。
- 正文中 `r$^2$SCAN` 与 `r\textsuperscript{2}SCAN` 两种 LaTeX 写法混用；两者渲染相同，不影响 PDF，但可在后续统一为 `r$^2$SCAN`。

## 12. 复现命令（只读）

```bash
# CSV → 方法能量映射与 ΔE
python3 - <<'PY'
import csv
rows=list(csv.DictReader(open('data/ch4_results.csv')))
ref=float(next(r['energy'] for r in rows if r['method']=='CCSD(T)'))
for r in rows:
    e=float(r['energy'])
    print(f"{r['method']:12s} {e: .12f} {e: .6f} {(e-ref)*627.509474: .6f} {(e-ref)*627.509474: .2f}")
PY

# ch4box 提取
for f in sections/ch0*-*.tex sections/ch1*-*.tex; do
  awk '/begin\{ch4box\}/,/end\{ch4box\}/' "$f"
done

# 图/表/公式引用与重复 label
grep -o '\\label{[^}]*}' sections/*.tex appendix/*.tex | sort | uniq -d
grep -o '\\(eq\)\?ref{[^}]*}' sections/*.tex | sort -u

# 引文 key 对账
grep -ohE '\\cite[a-zA-Z]*(\[[^]]*\])*\{[^}]*\}' sections/*.tex appendix/*.tex \
  | sed 's/.*{//;s/}//' | tr ',' '\n' | sed 's/^ *//;s/ *$//' | sort -u
grep -oE '^@[a-zA-Z]+\{[^,]+' refs.bib | sed 's/.*{//' | sort -u
```

**结论：所有规定数值/引用/术语检查 0 FAIL；仅 `sections/ch01-overview.tex:145` 有 1 处正文计数值与 CSV 基组列不符，建议在 T19 修复。**

---

## T19 修复后复审

> 复审对象：T19 修改后的全书（全量重编译），重点复核原报告第 11.2 节唯一额外发现 `sections/ch01-overview.tex:145`。

| 原发现 | 位置（修复后） | 修复内容 | 结论 |
|---|---|---|---|
| ch01:145 基组计数 | `sections/ch01-overview.tex:145` | 改为“20 个方法中，16 个用 def2-TZVPP；B97-3c 与 r$^2$SCAN-3c 使用各自内置基组（def2-mTZVP / def2-mTZVPP）；GFN2-xTB 与 GFN-FF 不含外部基组”，与 `data/ch4_results.csv` 的 `basis` 列逐一对应（16 + 2 + 2 = 20） | **PASS** |

### 更新后统计

| # | 检查项 | 断言数 | PASS | FAIL |
|---|--------|-------:|-----:|-----:|
| 1 | ch4box 总能 vs CSV（6 位小数） | 33 | 33 | 0 |
| 2 | ch4box ΔE vs 精确值重算（2 位小数） | 20 | 20 | 0 |
| 3 | ch4box 内部算式中间量 | 8 | 8 | 0 |
| 4 | 图/表 label 均被正文 `\ref` 引用 | 23 | 23 | 0 |
| 5 | 公式 label 均有 `\eqref` | 163 | 163 | 0 |
| 6 | `\cite` key 均存在于 `refs.bib` | 60 | 60 | 0 |
| 7 | 术语一致性 | 5 | 5 | 0 |
| 8 | 全书 label 无重复（304 个 label） | 1 | 1 | 0 |
| 9 | 第 16 章 CH4/H2- 汇总表 | 2 | 2 | 0 |
| 10 | 图表编号连续 | 1 | 1 | 0 |
| **合计** | | **316** | **316** | **0** |

- 316/316 规定检查项仍全部 PASS；额外的 `ch01:145` 正文计数错误已修复，故全书数据一致性额外检查也为 0 FAIL。
- 全量重编译后 `main.log`：0 undefined reference、0 undefined citation、0 multiply-defined、0 Missing character；PDF 中 0 处 `??`；overfull 5 处，最大 3.57pt。
