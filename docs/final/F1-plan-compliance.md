# F1 计划合规审计报告

- **仓库**：`/home/xieningke/课程/计算化学/泛函详解`
- **HEAD**：`edcc416`（`fix: move pgfplots out of texmf and wire TEXINPUTS`）
- **审计日期**：2026-10-20（B1 修复后复审）
- **审计对象**：`.omo/plans/chem-methods-lecture.md` 的 Must have / Must NOT have / IS-1…IS-10
- **审计方式**：只读。读取计划、`CONTRACT.md`、`docs/build-check.md`、`docs/audit-fixes.md`、`docs/final/F1-remediation.md`、三份审计报告、`sections/*.tex`、`appendix/*.tex`、`data/*.csv`、`refs.bib`、`runs/`、`preamble.tex`、`main.tex`；运行 `pdfinfo`、`pdftotext`、`grep`、`stat`、`kpsewhich`、`find`、Python CSV 解析。未改产品文件，未重编译，未 commit。

## 0. 结论摘要

| 类别 | PASS | FAIL | 判定 |
|---|---:|---:|---|
| Must have | 14 | 0 | 全部满足 |
| Must NOT have | 7 | 0 | 全部满足（B1 已修复） |
| IS-1 … IS-10 | 10 | 0 | 全部 PASS |

**关键结论**：书稿内容、数据、引用、图表、页数和 LaTeX 工程均达到计划要求；此前唯一阻断项 B1（`~/texmf` 中被加入 `pgfplots`）已由 commit `edcc416` 修复：`~/texmf` 下已无任何 `pgfplots` 路径，完整 pgfplots 树移至 `~/texmf-disabled/pgfplots-4.42/`，构建通过 `TEXINPUTS` 引用新位置。N2 复验 PASS，无剩余阻断缺口。

---

## 1. Must have 逐项核验

| # | 计划要求 | 证据 | 判定 |
|---|----------|------|:----:|
| M1 | ctexart + XeLaTeX + fandol | `main.tex:6`：`\documentclass[UTF8,11pt,a4paper,fontset=fandol]{ctexart}`；`docs/final/F3-build-qa.md` §1：`latexmk -xelatex` exit 0；`main.log:2347`：`Output written on main.xdv (102 pages...)` | **PASS** |
| M2 | 16 章正文 + 附录 | `ls sections/*.tex \| wc -l` = **16**；`main.tex:34-49` 逐个 `\include` 16 章；`appendix/*.tex` = **4**（A–D），`main.tex:52-57` 全部 `\include` | **PASS** |
| M3 | 总页数 95–105 | `pdfinfo main.pdf \| grep Pages` = **102**；`main.log:2347` = 102 pages | **PASS** |
| M4 | 16 章页数配额 ±1 | 由 `main.toc` 章节起始页计算（见 §4）：Ch1 +1、Ch2 −1、Ch3 −1、Ch4 −1、Ch5 −1、Ch6 −1、Ch7 0、Ch8 0、Ch9 −1、Ch10 −1、Ch11 −1、Ch12 −1、Ch13 −1、Ch14 0、Ch15 0、Ch16 +1；**16/16 在 ±1 内** | **PASS** |
| M5 | 4 个自定义环境 | `preamble.tex:81` `problemchain`、`:88` `methodcard`、`:95` `ch4box`、`:102` `pitfall`；使用计数：problemchain **16**、methodcard **13**、ch4box **13**、pitfall **16**（Ch1/2/16 按 `CONTRACT.md §4` 豁免 methodcard/ch4box） | **PASS** |
| M6 | CH₄ 16 个基础方法 + 4 个 MR 补充 | `data/ch4_results.csv` 20 数据行：HF、MP2、CISD、CCSD(T)、SVWN5、PBE、B97-3c、TPSS、r2SCAN、r2SCAN-3c、B3LYP、wB97M-V、B2PLYP、PWPB95、GFN2-xTB、GFN-FF、CASSCF(8,8)、CASPT2、NEVPT2、MRCI；`runs/ch4/` 20 目录、20 个 `.out` 全部 `ORCA TERMINATED NORMALLY` 且含 `FINAL SINGLE POINT ENERGY` | **PASS** |
| M7 | CH₄ 统一 def2-TZVPP 策略 | CSV `basis`：**16 × def2-TZVPP**、1 × def2-mTZVP（B97-3c）、1 × def2-mTZVPP（r2SCAN-3c）、2 × `none`（GFN2-xTB/GFN-FF）；`runs/ch4/*/*.inp` 第一行逐项一致；`grep -m1 def2-mTZVP runs/ch4/b973c/*.out` 与 `grep -m1 def2-mTZVPP runs/ch4/r2scan3c/*.out` 均有输出 | **PASS** |
| M8 | H₂⁻ 6 方法 × 8 R；CAS(3,2)、nroots=1 | `data/h2m_pes.csv` **48** 数据行；`Counter` 显示 UHF/MP2/CCSD(T)/CASSCF/NEVPT2/MRCI 各 **8**；`runs/h2m/*/R*/` 共 **48** 个 R 目录；输入含 `nel 3`、`norb 2`、`mult 2`、`nroots 1`、`* xyz -1 2` | **PASS** |
| M9 | UHF ⟨S²⟩ 数据；NEVPT2<CASSCF；MRCI<NEVPT2 | CSV UHF ⟨S²⟩：0.754473（R=0.6）→ 0.821141（R=3.0），增量 **0.066668**；逐 R 计算：`NEVPT2−CASSCF` 最大 **−0.033149 Eh**（全 R <0），`MRCI−NEVPT2` 最大 **−0.012927 Eh**（全 R <0） | **PASS** |
| M10 | CH₄ MR 补充 CASSCF(8,8)/CASPT2/NEVPT2/MRCI | `runs/ch4/{casscf,caspt2,nevpt2,mrci}/*.inp` 均含 `nel 8`、`norb 8`、`mult 1`、`nroots 1`；CSV 第 17–20 行为这四个方法，能量见 `data/ch4_notes.md` 与 `docs/data-audit.md` §2 | **PASS** |
| M11 | natbib + bibtex，~40+ 文献 | `preamble.tex:46` 加载 `natbib`；`main.tex:60-61` 使用 `plainnat` + `\bibliography{refs}`；`refs.bib` 有 **63** 个 `@...` entry；`main.bbl` **60** 个 `\bibitem`；`main.blg` 0 条 `Warning--/error`；60 个 cite key 全部存在 | **PASS** |
| M12 | 5 张图 | 5 个指定主题全部存在：Ch1 方法地图（`ch:01:fig:map`，`ch01-overview.tex:33-82`）、Ch7 H₂⁻ 势能曲线（`figures/ch07/h2m_pes.pdf`，`ch07-casscf.tex:157`）、Ch9 DFT 阶梯（`ch:09:fig:ladder`，`ch09-dft.tex:157-185`）、Ch16 CH₄ 偏差条形图（`figures/ch16/ch4_deviations.pdf`，`ch16-summary.tex:72`）、Ch16 决策树（`ch:16:fig:tree`，`ch16-summary.tex:156-193`）。另有 Ch8 H₂⁻ MR 图，属超集，不是缺口 | **PASS** |
| M13 | 8 张表 | 8 个主题均有落点：① 方法总览 = `ch:01:tab:methods`（17 行）；② DFT 泛函阶梯 = `ch:16:tab:cost` 的 LDA/GGA/meta-GGA/杂化/范围分离/双杂化行；③ CH₄ 总表 = `ch:16:tab:ch4-summary`（20 行）；④ H₂⁻ 结果 = `ch:16:tab:h2m-summary`（6 方法 + UHF ⟨S²⟩）与 `ch:07:tab:h2m`；⑤ xTB/FF 对比 = Ch1 表最后一行 + `ch:16:tab:cost` 的 GFN-FF/GFN2-xTB 独立行；⑥ ORCA 关键词 = Ch1 表关键词列 + 附录 A 模板；⑦ 误差指标 = `ch:16:tab:ch4-summary` 的 ΔE 列（18 个 QM 方法）；⑧ 术语表 = `app:tab:glossary`（57 行）。全书共 **17** 个表 label，为超集 | **PASS** |
| M14 | 附录 A–D 内容 | A `appendix/app-orca.tex`：A.1–A.6 只给正文未完整展示的 ORCA 输入模板（CH₄、H₂⁻、CASSCF/MR、双杂化 AuxC、3c、xTB/FF）；B `appendix/app-data.tex`：目录结构、CSV 列定义、parse/plot 脚本用法，明确“CSV 本身不在这里全文打印”；C `appendix/app-exercises.tex`：**10** 个 `\item` 习题并附解答；D `appendix/app-glossary.tex`：**57** 个数据行的术语中英表 | **PASS** |

---

## 2. Must NOT have 逐项核验

| # | 禁止项 | 证据 | 判定 |
|---|--------|------|:----:|
| N1 | 不安装/不使用 biblatex + biber | `grep -rniE 'biblatex\|biber' preamble.tex main.tex sections appendix refs.bib` 仅 **1** 处命中，且是 `refs.bib:2` 的注释“Do NOT use biblatex”；无 `\usepackage{biblatex}`、无 `biber` 构建步骤；实际使用 natbib + bibtex（`main.bbl` 60 条） | **PASS** |
| N2 | 不修改 `~/texmf` 中除 tcolorbox 外的任何内容 | **PASS（B1 修复后）**。`find ~/texmf -path '*pgfplots*' \| wc -l` = **0**；`~/texmf/tex/latex/` 仅含 chemfig、everysel、makecell、multirow、tcolorbox；完整 pgfplots 树（`tex/latex`、`tex/generic`、`tex/context`、`tex/plain`、`doc`、`scripts`、`source`）位于 `~/texmf-disabled/pgfplots-4.42/`。无 `TEXINPUTS` 时 `kpsewhich pgfplots.sty` 无输出；带项目 `TEXINPUTS` 时解析到 `~/texmf-disabled/pgfplots-4.42/tex/latex/pgfplots/pgfplots.sty`。tcolorbox 4.42 仍为唯一活动版本，2026 版仍在 `~/texmf-disabled/tcolorbox-2026/`（未改动） | **PASS** |
| N3 | 不在子 agent 中各自运行 ORCA | `find runs -type f -printf '%TY-%Tm-%Td %TH:%TM'`：全部 run 文件时间为 **22:33–22:37**；数据 commit `0d240f2` 在 **22:56**，早于第一章 commit `79959c0`（23:15）和后续章节（23:43）；`runs/` 下只有 `runs/h2m/run_all.sh`，无按章生成脚本；`runs/ch4/` 20 个输出同批生成 | **PASS** |
| N4 | 不引入 CONTRACT 未冻结的新符号/宏 | `grep -rE '\\(newcommand\|renewcommand\|def\|DeclareMathOperator\|newenvironment\|newtcolorbox)' sections appendix` = **0**；`preamble.tex` 的宏 `\dd,\ee,\ii,\HF,\xc,\ket,\bra,\op,\braket,\bracket` 全部列于 `CONTRACT.md §3`；4 个环境亦在 §4 冻结 | **PASS** |
| N5 | 不超过 105 页 | `pdfinfo main.pdf` = **102** | **PASS** |
| N6 | 不使用 `~/texmf` 中的 2026 版 tcolorbox | `kpsewhich tcolorbox.sty` → `/home/xieningke/texmf/tex/latex/tcolorbox/tcolorbox.sty`；首行 `\ProvidesPackage{tcolorbox}[2020/10/09 version 4.42 ...]`；2026 版在 `~/texmf-disabled/tcolorbox-2026/tcolorbox.sty`，不在 kpathsea 搜索树内 | **PASS** |
| N7 | 不调用 `/usr/bin/orca` | `grep -rn '/usr/bin/orca' runs scripts sections appendix *.tex` = **0**；`runs/h2m/run_all.sh:8` 使用 `ORCA="/home/xieningke/orca611/orca"`；CH₄ 输入只含 ORCA 关键词，未调用外部 Python 程序 | **PASS** |

---

## 3. IS-1 … IS-10 逐行判定

| IS | 计划判据 | 证据 | 判定 |
|----|----------|------|:----:|
| IS-1 | ~100 页中文 PDF，编译零错误 | `pdfinfo main.pdf` → `Pages: 102`；`main.log:2347` → `Output written on main.xdv (102 pages)`；`grep -c '^!' main.log` = **0**；`LaTeX Warning: Citation` = 0、`Reference` = 0、`multiply defined` = 0、`Missing character` = 0；F3 全量重建 5 步 exit 0 | **PASS** |
| IS-2 | 16 章问题链，每章 problemchain 回答三问 | `grep -c '\begin{problemchain}' sections/*.tex`：16 章每章 **1**，合计 **16**；逐块含“上一章留下的问题 / 本章为什么存在 / 本章留下的新问题”；`docs/logic-audit.md` 16/16 章 PASS | **PASS** |
| IS-3 | 每方法：定位、核心近似、关键编号方程、ORCA 关键词、CH₄ 结果框、失效模式 | Ch3–15 共 **13** 个 `methodcard` + **13** 个 `ch4box`；卡片字段含方法/文献、核心近似、`\eqref` 关键方程、ORCA 关键词、成本/变分/尺寸、典型失效；`docs/data-audit.md` 33/33 方法—box 数值组合 PASS；`docs/equation-audit.md` 163/163 PASS | **PASS** |
| IS-4 | H₂⁻ CAS(3,2) 势能曲线 + UHF 自旋污染 | `figures/ch07/h2m_pes.pdf` 存在并被 `ch07-casscf.tex:157` 引用；CSV **48** 行（6×8）；UHF ⟨S²⟩ 0.754473→0.821141；Ch7/Ch16 均如实写 CASSCF(3,2) 高于 UHF、占据数 2.0/1.0，多参考证据来自 ⟨S²⟩ 与 NEVPT2/MRCI 修正 | **PASS** |
| IS-5 | DFT 每级代表泛函 | CSV 与 Ch10–13/Ch16 均含 SVWN5、PBE、B97-3c、TPSS、r2SCAN、r2SCAN-3c、B3LYP、wB97M-V、B2PLYP、PWPB95 共 **10** 个；Ch10=LDA/GGA/B97-3c、Ch11=TPSS/r²SCAN/r²SCAN-3c、Ch12=B3LYP/ωB97M-V、Ch13=B2PLYP/PWPB95 | **PASS** |
| IS-6 | 波函数/DFT 统一 def2-TZVPP；3c 内置；xTB/FF 无基组 | CSV `basis` 16 + 1 + 1 + 2；20 个 `runs/ch4/*/*.inp` 第一行逐项一致；CCSD(T) 参考 `-40.438597868462 Eh` 为 def2-TZVPP | **PASS** |
| IS-7 | `ch4_results.csv` 20 行 + `h2m_pes.csv` 48 行 | Python `csv.DictReader`：**20** / **48** 数据行；`h2m_occupations.csv` **8** 行；`scripts/parse_orca.py --batch` 解析 20/20 converged；F4 复核 48 个 H₂⁻ 输出能量与 ⟨S²⟩ 逐项一致 | **PASS** |
| IS-8 | 全书无 `??`，图表全部被引用 | `pdftotext main.pdf - \| grep -c '??'` = **0**；`main.log` 0 undefined reference/citation、0 multiply、0 missing；6 个图 label + 17 个表 label 全部被 `\ref`，163/163 公式 label 被 `\eqref`；304 个 label 无重复 | **PASS** |
| IS-9 | 17 行方法存在意义表 + 方法地图 + 决策树 | `ch01-overview.tex` 表体 **17** 个数据行（HF…GFN2-xTB/GFN-FF 合并行），caption 明写“17 行”；方法地图 `ch:01:fig:map`；决策树 `ch:16:fig:tree`（三步：是否需要电子结构→是否强静态相关→按目标精度分派） | **PASS** |
| IS-10 | CONTRACT.md + methodcard/problemchain 环境 + refs.bib | `CONTRACT.md` 含符号、单位、公式宏、章节模板、16 章问题链、标签、文献、数据、页数配额、术语等 14 节；`preamble.tex` 定义 4 个环境；`refs.bib` **63** 个 entry | **PASS** |

---

## 4. 章页配额证据（`main.toc`）

| 章 | 起始印刷页 | 实际页数 | 配额 | 差 | 判定 |
|---|---:|---:|---:|---:|:----:|
| Ch1 | 5 | 5 | 4 | +1 | PASS |
| Ch2 | 10 | 6 | 7 | −1 | PASS |
| Ch3 | 16 | 5 | 6 | −1 | PASS |
| Ch4 | 21 | 5 | 6 | −1 | PASS |
| Ch5 | 26 | 5 | 6 | −1 | PASS |
| Ch6 | 31 | 5 | 6 | −1 | PASS |
| Ch7 | 36 | 6 | 6 | 0 | PASS |
| Ch8 | 42 | 5 | 5 | 0 | PASS |
| Ch9 | 47 | 5 | 6 | −1 | PASS |
| Ch10 | 52 | 5 | 6 | −1 | PASS |
| Ch11 | 57 | 4 | 5 | −1 | PASS |
| Ch12 | 61 | 4 | 5 | −1 | PASS |
| Ch13 | 65 | 4 | 5 | −1 | PASS |
| Ch14 | 69 | 5 | 5 | 0 | PASS |
| Ch15 | 74 | 5 | 5 | 0 | PASS |
| Ch16 | 79 | 6 | 5 | +1 | PASS |

- 正文合计 80 印刷页；附录 A 从第 85 页开始；参考文献第 96–101 页；PDF 物理页 **102**（含封面偏移）。16/16 章均在配额 ±1 内。

---

## 5. B1 修复后复核（post-fix）

- **修复提交**：`edcc416 fix: move pgfplots out of texmf and wire TEXINPUTS`（改动 `latexmkrc`、`build-chapter.sh`、`appendix/app-orca.tex`、`docs/final/F1-remediation.md`）。
- **目录迁移**：
  - `find ~/texmf -path '*pgfplots*' | wc -l` = **0**；
  - `~/texmf/tex/latex/` = `chemfig`、`everysel`、`makecell`、`multirow`、`tcolorbox`（无 pgfplots）；
  - `~/texmf-disabled/pgfplots-4.42/` 含完整树：`tex/latex/pgfplots`、`tex/generic/pgfplots`、`tex/context/third/pgfplots`、`tex/plain/pgfplots`、`doc/*/pgfplots`、`scripts/pgfplots`、`source/*/pgfplots`；
  - `~/texmf-disabled/tcolorbox-2026/tcolorbox.sty` 的 birth time 仍为 `2026-07-03 00:10:07`，未被改动。
- **TEXINPUTS 接入**：
  - `latexmkrc` 首行：`$ENV{'TEXINPUTS'} = "$ENV{HOME}/texmf-disabled/pgfplots-4.42//:" . ($ENV{'TEXINPUTS'} // '');`
  - `build-chapter.sh` 在调用 xelatex/latexmk 前：`export TEXINPUTS="$HOME/texmf-disabled/pgfplots-4.42//:${TEXINPUTS:-}"`。
- **kpsewhich 验证**：
  - `env -u TEXINPUTS kpsewhich pgfplots.sty` → **无输出**（默认路径不再命中 `~/texmf`）；
  - `TEXINPUTS="$HOME/texmf-disabled/pgfplots-4.42//:" kpsewhich pgfplots.sty` → `/home/xieningke/texmf-disabled/pgfplots-4.42/tex/latex/pgfplots/pgfplots.sty`；
  - `kpsewhich tcolorbox.sty` → `/home/xieningke/texmf/tex/latex/tcolorbox/tcolorbox.sty`，版本 **4.42（2020/10/09）**。
- **构建日志**：`main.log` 实际加载 `/home/xieningke/texmf-disabled/pgfplots-4.42/tex/latex/pgfplots/pgfplots.sty`；日志中对 `~/texmf/tex/latex/pgfplots` 与 `~/texmf/tex/generic/pgfplots` 的引用计数 = **0**。
- **全量重建结果**：`pdfinfo` = **102 页**，A4；`main.log:2347` = `Output written on main.xdv (102 pages)`；`grep -c '^!'` = **0**；Citation/Reference/multiply-defined/Missing character 均为 **0**；`pdftotext main.pdf - | grep -c '??'` = **0**；Overfull = **5**，最大 **3.56561pt**（全部 <4pt）。
- **附录 A 对齐**：`appendix/app-orca.tex:87` 已改为“只写 `def2-TZVPP` 会直接报错（不会自动退回四指数 MP2），能量不可复现”，与 Ch13/Ch16 一致。
- **计划记录**：`.omo/plans/chem-methods-lecture.md:391` 的 Task 7 已为 `[x]`。

**B1 复验结论**：N2 已由 FAIL 转为 **PASS**；无剩余阻断缺口。

---

## 6. 非阻断观察

1. **附录 A AuxC 措辞（已关闭）**：`appendix/app-orca.tex:87` 已在 `edcc416` 中改为“直接报错（不会自动退回四指数 MP2）”，与 Ch13/Ch16 一致。
2. **表 8 主题的落点较合并**：xTB/FF 对比与误差指标没有独立浮动表，分别落在 Ch1 表最后一行、Ch16 成本表/CH₄ 总表的 ΔE 列中；内容齐全，但若要求“8 张独立表”，可拆分为独立表。当前按“主题覆盖 + 全书 17 表超集”判 PASS。
3. **计划 Task 7 复选框（已关闭）**：`.omo/plans/chem-methods-lecture.md:391` 已改为 `[x] 7.`；第 1、2、9 章已写入并由 `79959c0` 提交，逻辑审计 16/16 PASS。
4. **`kpsewhich tcolorbox.sty` 不是系统路径**：解析到 `~/texmf/tex/latex/tcolorbox/tcolorbox.sty`（4.42），而非计划 Task 1 验收写的 `/usr/share/texlive/...`。硬性 Must NOT（2026 版不激活）通过；该项仅为 Task 1 验收偏差记录。
5. **`refs.bib` 3 条未引用 entry**：`cramer2004`、`ernzerhof1999`、`neese2012orca`；不影响 60 个 cite key 的完整性。
6. **`parse_orca.py` 方法标签规范化**：输出用 ORCA 关键词名（LDA/XTB/CASSCF/R2SCAN），CSV 用教学名（SVWN5/GFN2-xTB/CASSCF(8,8)/r2SCAN）；能量、基组、收敛标志逐项一致，不影响 IS-7。

---

## 7. 最终判定

- Must have：**14/14 PASS**。
- Must NOT have：**7/7 PASS**（N2 在 `edcc416` 后复验通过）。
- IS-1…IS-10：**10/10 PASS**。
- 阻断缺口：**无**。B1 已修复；`~/texmf` 下无 pgfplots，兼容版 pgfplots 4.42 位于 `~/texmf-disabled/pgfplots-4.42/` 并由 `TEXINPUTS` 接入；tcolorbox 4.42 仍活动，2026 版未激活。
- 构建指标：102 页，0 error，0 citation/reference/multiply/missing/`??`，Overfull 5 处最大 3.56561pt。

所有 Must have、Must NOT have 与 IS-1…IS-10 均已验证通过，可以交付。

**VERDICT: APPROVE**
