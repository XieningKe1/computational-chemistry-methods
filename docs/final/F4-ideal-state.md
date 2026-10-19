# F4 理想状态忠实度终验报告

- **仓库**：`/home/xieningke/课程/计算化学/泛函详解`
- **HEAD**：`b720d76`（`fix: resolve all audit findings`）
- **验证日期**：2026-10-20
- **验证方式**：只读。读取 `.omo/plans/chem-methods-lecture.md`、`CONTRACT.md`、`docs/build-check.md`、`docs/audit-fixes.md`、三份审计报告、章节/附录/数据/脚本/ORCA 输出；运行只读计数与对账命令，未改任何产品文件，未重编译，未 commit。
- **结论**：IS-1 至 IS-10 全部 PASS，无阻断性缺口。

---

## 1. IS 逐行判定

| IS | 判定 | 核心证据 |
|----|------|----------|
| IS-1 | **PASS** | `pdfinfo main.pdf` → `Pages: 102`；`main.log:2324` → `Output written on main.xdv (102 pages)`；`grep -c '^!' main.log` → `0`；`main.tex:6` 为 `ctexart[UTF8,11pt,a4paper,fontset=fandol]` |
| IS-2 | **PASS** | `grep -c '\begin{problemchain}' sections/*.tex` → 每章 1 个，合计 **16**；脚本检查 16/16 个 block 均含“上一章留下的问题 / 本章为什么存在 / 本章留下的新问题”三问 |
| IS-3 | **PASS** | Ch3–15 共 **13 个 `methodcard`**、**13 个 `ch4box`**；每张卡片含方法/文献（定位）、核心近似、带 `\eqref` 的关键方程、ORCA 关键词、成本/变分/尺寸一致、典型失效；`docs/data-audit.md` 记录 33/33 个方法—box 数值组合 PASS |
| IS-4 | **PASS** | `data/h2m_pes.csv` **48** 数据行（6 方法 × 8 个 R）；`figures/ch07/h2m_pes.pdf` 存在并被 `sections/ch07-casscf.tex:157` 引用；UHF ⟨S²⟩ 0.754473（R=0.6）→ 0.821141（R=3.0），Ch7/Ch16 正文一致 |
| IS-5 | **PASS** | `data/ch4_results.csv` 含 SVWN5、PBE、B97-3c、TPSS、r2SCAN、r2SCAN-3c、B3LYP、wB97M-V、B2PLYP、PWPB95 全部 10 个 DFT 代表；Ch10–13 分章覆盖，Ch16 总表 40–49 行逐行列全 |
| IS-6 | **PASS** | CSV `basis` 列：**16** × def2-TZVPP、1 × def2-mTZVP（B97-3c）、1 × def2-mTZVPP（r2SCAN-3c）、2 × `none`（GFN2-xTB/GFN-FF）；20 个 `runs/ch4/*/*.inp` 与 CSV 一致；参考值 CCSD(T)/def2-TZVPP `-40.438597868462` Eh |
| IS-7 | **PASS** | Python CSV 解析：`ch4_results.csv` **20** 数据行、`h2m_pes.csv` **48** 数据行；`scripts/parse_orca.py --batch runs/ch4` 解析 **20/20 converged**，20 个能量/基组与 CSV 逐项一致；48 个 H₂⁻ 原始输出能量与 ⟨S²⟩ 与 CSV 逐项一致（0 不符） |
| IS-8 | **PASS** | `pdftotext main.pdf - \| grep -c '??'` → **0**；`main.log` 的 undefined reference/citation、multiply-defined、missing character 均为 **0**；**23/23** 图/表 label 被引用，**163/163** 公式 label 被 `\eqref` 引用，304 个 label 无重复 |
| IS-9 | **PASS** | `sections/ch01-overview.tex:98–145` 的 17 行方法存在意义表（17 个数据行，最后一行合并 GFN2-xTB/GFN-FF）；`:33–82` 的方法地图 TikZ；`sections/ch16-summary.tex:156–193` 的决策树 TikZ |
| IS-10 | **PASS** | `CONTRACT.md` 含符号、单位、公式宏、章节模板、16 章问题链、标签、文献、数据、页数配额、术语等章节；`preamble.tex:81–108` 定义 `problemchain`/`methodcard`/`ch4box`/`pitfall` 四个环境；`refs.bib` 共 **63** 个 entry |

---

## 2. 逐项证据

### IS-1 — 约 100 页中文 LaTeX PDF，编译零错误

- **页数**：`pdfinfo main.pdf` 输出 `Pages: 102`，在计划的 95–105 页区间内。
- **编译**：`main.log:2324` 为 `Output written on main.xdv (102 pages, 2276700 bytes).`；`grep -c '^!' main.log` = `0`，即无 LaTeX 错误行。
- **文档类/字体**：`main.tex:6`：
  `\documentclass[UTF8,11pt,a4paper,fontset=fandol]{ctexart}`。
  `main.log` 加载 `ctex-fontset-fandol.def`，并实际使用 `FandolSong-Regular` 等字体。
- **交叉引用**：`main.log` 中 `LaTeX Warning: Reference` = 0、`LaTeX Warning: Citation` = 0、`multiply defined` = 0、`Missing character` = 0。
- **排版**：Overfull hbox 共 5 处，最大 3.56561pt（`sections/ch01-overview.tex` 2.82448pt、`ch02` 1.23936pt、`ch16` 0.38074/1.10976pt、`appendix/app-data.tex` 3.56561pt），符合“≤5 且每处 <10pt”的门槛。
- **报告基线说明**：`docs/build-check.md` 记录的是 `5252f1d` 的全量构建（5 条命令 exit 0、102 页、0 引用/0 `??`/5 处 overfull）。`docs/audit-fixes.md` §2.2 明确记录 T19 修复后再次执行 `latexmk -C → latexmk -xelatex → bibtex → latexmk ×2`，结果仍为 102 页、0 错误、0 undefined、0 multiply；当前 `main.log`（102 页、0 错误行）与之一致。

### IS-2 — 16 章问题链结构

- `grep -c '\begin{problemchain}' sections/*.tex` 的结果为：
  Ch1–Ch16 每章各 1 个，合计 **16**。
- 每个 block 均含三个必需字段：
  - `上一章留下的问题：`
  - `本章为什么存在：`
  - `本章留下的新问题：`
  脚本逐块检查 16/16 通过。
- 示例：`sections/ch03-hf.tex:10–14` 从 Ch2 的“多体方程不可解”接到 HF 的平均场，再留下“HF 缺少动态相关能”；`sections/ch07-casscf.tex:10–14` 从 CC 的强静态相关失效接到 CASSCF，再留下“CASSCF 缺动态相关”；`sections/ch16-summary.tex:10–14` 收束全书并说明“本章留下的新问题”为全书收束。
- 16 个 block 的交接内容与 `CONTRACT.md §5` 的 16 章问题链交接表一致（逻辑审计 `docs/logic-audit.md` 16/16 章 PASS）。

### IS-3 — 每方法有定位、核心近似、关键编号方程、ORCA 关键词、CH₄ 结果框、失效模式

- **方法卡片数量**：Ch3–Ch15 每章 `\begin{methodcard}` 各 1 个，共 **13** 个（Ch1/Ch2/Ch16 按 `CONTRACT.md §4` 明确豁免）。
- **字段完整性**：以 `sections/ch03-hf.tex:17–25` 为例，卡片依次给出：
  - `方法：哈特里--福克（Hartree--Fock，HF）` + `文献：\citep{...}`（方法身份/定位）
  - `核心近似：单个斯莱特行列式 + 平均场...`
  - `关键方程：式~\eqref{ch:03:eq:hf-energy}（HF 能量）`
  - `ORCA 关键词：! HF def2-TZVPP TightSCF`
  - `成本标度：O(N^4)`；`能否变分 / 尺寸一致：是/是`
  - `典型失效：键解离、色散作用、带隙（以及开壳层的自旋污染）`
- Ch10 的卡片把 LDA（SVWN5）、GGA（PBE）与 B97-3c 合并为一个方法族卡片，并在 `ch4box` 中逐方法给出 ORCA 关键词与数值；Ch11（TPSS/r²SCAN/r²SCAN-3c）、Ch12（B3LYP/ωB97M-V）、Ch13（B2PLYP/PWPB95）、Ch8（CASPT2/NEVPT2/MRCI）同样在卡片与结果框中逐方法覆盖。
- **CH₄ 结果框**：Ch3–Ch15 的 `\begin{ch4box}` 各 1 个，共 **13** 个（行号：Ch3 231、Ch4 203、Ch5 206、Ch6 229、Ch7 203、Ch8 163、Ch9 189、Ch10 176、Ch11 143、Ch12 143、Ch13 135、Ch14 150、Ch15 171）。
- **数值对账**：`docs/data-audit.md` 第 2 节记录 33 个方法—box 组合（含同一 box 内多个方法）全部与 CSV 6 位小数或精确值一致；第 3 节记录 20 个 ΔE 全部按 `(E−E_CCSD(T))×627.509474` 重算通过。
- **关于“定位”字段的说明**：`CONTRACT.md §4` 的冻结模板使用 `方法`/`文献` 字段表达方法身份与定位，没有独立的“定位”字段；章节正文另有方法定位段落（如 `sections/ch14-xtb.tex:129` 的“xTB 的定位”、`sections/ch15-force-field.tex:153` 的 GFN-FF 定位）。因此以模板字段 + 正文定位为准，判 PASS。

### IS-4 — H₂⁻ CAS(3,2) 势能曲线 + UHF 自旋污染

- **数据规模**：`data/h2m_pes.csv` 共 **48** 个数据行，方法集合为 UHF、MP2、CCSD(T)、CASSCF、NEVPT2、MRCI，每种 8 个 R（0.6、0.8、1.0、1.2、1.5、2.0、2.5、3.0）。
- **图**：`figures/ch07/h2m_pes.pdf` 存在（26,943 bytes），由 `sections/ch07-casscf.tex:157` 的 `\includegraphics[...]{figures/ch07/h2m_pes.pdf}` 引入；同处 `:158–160` 的 caption 明确写“六条曲线分别是 UHF、MP2、CCSD(T)、CASSCF(3,2)、NEVPT2 与 MRCI”，下半部分为 UHF 的 ⟨S²⟩。另有 `figures/ch08/h2m_mr.pdf` 用于第 8 章多参考对比。
- **UHF 自旋污染**：CSV 中 R=0.6 为 `0.754473`，R=3.0 为 `0.821141`；`sections/ch07-casscf.tex:177/184` 的表格与 `:196` 的完整序列一致；`sections/ch16-summary.tex:136` 的汇总表引用 0.754473 / 0.764251 / 0.821141。
- **诚实叙事**：Ch7 `:164` 与 `:189` 明确说明 CASSCF(3,2) 在每个 R 上都高于 UHF，活性空间自然占据数为 2.0000/1.0000 而非 1.5/1.5；多参考必要性由 ⟨S²⟩ 增长、NEVPT2/MRCI 的大修正支撑，而不是 CASSCF–UHF 的能量排序。这与计划“由实际数据决定叙述方向”的验收口径一致，不构成失败。
- **CASPT2 H₂⁻ 缺失**：Ch16 `:148` 用脚注说明 ORCA 6.1.1 在 H₂⁻/CAS(3,2) 的 CASPT2 清理阶段存在已知段错误，因此未做 H₂⁻ 的 CASPT2 扫描；这是实现问题，不是理论失效，且 CH₄ 的 CASPT2 行仍保留。

### IS-5 — DFT 每级代表泛函清单

`data/ch4_results.csv` 中 10 个 DFT 代表逐项存在：

| 泛函 | CSV 能量 / Eh | 出现章节 |
|------|---------------|----------|
| SVWN5 | −40.1177735788 | Ch10、Ch16 |
| PBE | −40.464323928376 | Ch10、Ch16 |
| B97-3c | −40.497379885896 | Ch10、Ch16 |
| TPSS | −40.541483557685 | Ch11、Ch16 |
| r2SCAN | −40.500987222276 | Ch11、Ch16 |
| r2SCAN-3c | −40.494867680722 | Ch11、Ch16 |
| B3LYP | −40.503277669626 | Ch12、Ch16 |
| wB97M-V | −40.492948404733 | Ch12、Ch16 |
| B2PLYP | −40.48728697733 | Ch13、Ch16 |
| PWPB95 | −40.489597965231 | Ch13、Ch16 |

- 分章覆盖检查：Ch10 含 SVWN5/PBE/B97-3c；Ch11 含 TPSS/r2SCAN/r2SCAN-3c；Ch12 含 B3LYP/wB97M-V；Ch13 含 B2PLYP/PWPB95。
- Ch16 总表 `sections/ch16-summary.tex:40–49` 逐行列出上述 10 行，并各带基组与备注。
- 3c 复合方法在 Ch16 表注 `:61` 明确标注“不是雅各布天梯的新梯级”，且基组写为 def2-mTZVP/def2-mTZVPP。

### IS-6 — 基组策略

Python 按 CSV 正确解析（处理了 `"CASSCF(8,8)"` 的引号逗号）后的 `basis` 计数：

- `def2-TZVPP`：**16** 个（HF、MP2、CISD、CCSD(T)、SVWN5、PBE、TPSS、r2SCAN、B3LYP、wB97M-V、B2PLYP、PWPB95、CASSCF(8,8)、CASPT2、NEVPT2、MRCI）
- `def2-mTZVP`：1 个（B97-3c，内置）
- `def2-mTZVPP`：1 个（r2SCAN-3c，内置）
- `none`：2 个（GFN2-xTB、GFN-FF）

输入文件逐项核对（`runs/ch4/*/*.inp` 第 1 行）：

- `runs/ch4/ccsdt/ccsdt.inp:1` → `! CCSD(T) def2-TZVPP TightSCF`
- `runs/ch4/b973c/b973c.inp:1` → `! B97-3c TightSCF`（无外部基组，使用内置）
- `runs/ch4/r2scan3c/r2scan3c.inp:1` → `! r2SCAN-3c TightSCF`（无外部基组，使用内置）
- `runs/ch4/xtb/xtb.inp:1` → `! XTB`
- `runs/ch4/gfnff/gfnff.inp:1` → `! GFN-FF`

参考值：`data/ch4_results.csv` 的 CCSD(T) 行 `energy = -40.438597868462`，基组 `def2-TZVPP`；Ch16 `:19` 与 Ch1 `:145` 均写 `E = -40.438598` Eh。

### IS-7 — 数据规模与可追溯性

**行数（Python `csv.reader`，非 `wc -l`）**：

- `data/ch4_results.csv`：20 个数据行（表头 7 列：`method,basis,energy,s2,converged,runtime,inp_path`）。
- `data/h2m_pes.csv`：48 个数据行（表头 4 列：`method,R,energy,s2`）。
- `data/h2m_occupations.csv`：8 个数据行，与 H₂⁻ 的 8 个 R 对应。

**CH₄ 复现**：

- `python3 scripts/parse_orca.py --batch runs/ch4 --csv /tmp/opencode/f4_ch4.csv`
  → `parsed 20 file(s) ... (20 converged, 0 failed)`。
- 与 `data/ch4_results.csv` 对账：20/20 行存在；`energy`、`basis`、`converged` 全部一致；`inp_path` 指向的 20 个文件全部存在。
- 说明：解析器直接从 ORCA 输入行取方法名，因此对 4 行输出 ORCA 关键词名（`LDA`、`XTB`、`CASSCF`、`R2SCAN`），而 CSV 使用教学名（`SVWN5`、`GFN2-xTB`、`CASSCF(8,8)`、`r2SCAN`）；逐项映射后能量与基组完全一致。这是标签规范化，不是数值差异，列为非阻断观察。

**H₂⁻ 复现**：

- `runs/h2m/` 下共 **48** 个 `*.out`（6 方法 × 8 R）。
- 逐文件读取最后一个 `FINAL SINGLE POINT ENERGY` 与 `Expectation value of <S**2>`，与 `data/h2m_pes.csv` 的 48 行逐项比较：能量 48/48 一致，有 S² 的行也逐项一致，**0 个不符**。
- `data/h2m_report.md` 记录 48 个作业全部 `ORCA TERMINATED NORMALLY`，并给出 6×8 能量表；`data/ch4_notes.md` 记录 CH₄ 几何、基组与 HF 能隙/CASSCF 占据数的原始输出出处。

### IS-8 — 交叉引用与图表引用

- **PDF 中 `??`**：`pdftotext main.pdf - | grep -c '??'` → **0**。
- **main.log**：`LaTeX Warning: Reference` = 0；`LaTeX Warning: Citation` = 0；`multiply defined` = 0；`Missing character` = 0；`undefined` = 0。
- **图/表**：全书共 **23** 个图/表 label（6 图 + 17 表，含附录 2 个表）；23 个均至少被正文 `\ref` 一次；无孤立图/表。
- **公式**：编号公式 **163** 个，`\label{ch:XX:eq:...}` **163** 个，被 `\eqref` 引用 **163** 个，未引用 0 个。
- **重复 label**：全书 304 个 `\label`，重复 0 个。
- 与审计报告一致：`docs/data-audit.md` 23/23 图表、163/163 公式、316/316 规定项 PASS；`docs/equation-audit.md` 163/163 PASS；`docs/logic-audit.md` 16/16 章 PASS。

### IS-9 — 17 行方法存在意义表 + 方法地图 + 决策树

- **17 行表**：`sections/ch01-overview.tex:98` 小节标题为“方法存在意义表（17 行）”；`:106` caption 为“17 行（18 个方法；GFN2-xTB/GFN-FF 合并一行）……”；表体 `:112–144` 共 17 个数据行：
  HF、MP2、CISD、CCSD(T)、CASSCF、CASPT2、NEVPT2、MRCI、SVWN5（LDA）、PBE（GGA）、TPSS（meta-GGA）、r²SCAN（meta-GGA）、B3LYP（全局杂化）、ωB97M-V（范围分离杂化 + VV10）、B2PLYP（双杂化）、PWPB95（双杂化）、GFN2-xTB/GFN-FF（合并一行）。
- **方法地图**：`sections/ch01-overview.tex:33–82` 为 TikZ 图，label 为 `ch:01:fig:map`；caption `:81` 说明左侧波函数路线、右侧 DFT 天梯、两端收敛到 xTB/力场。
- **决策树**：`sections/ch16-summary.tex:156–191` 为 TikZ 决策树，label `ch:16:fig:tree`（`:193`），正文 `:153` 与 `:214` 说明“是否需要电子结构 → 是否有强静态相关 → 按目标精度分派”的三步逻辑。
- 三者在当前 `main.pdf` 中均编译呈现（`pdftotext` 可检索到“方法地图”“决策树”等文本）。

### IS-10 — LaTeX 工程

- **CONTRACT.md**：`CONTRACT.md` 含 14 个一级章节：符号约定、单位约定、公式宏列表、章节模板、16 章问题链交接表、标签约定、文献约定、数据约定、文件所有权、页数配额、术语中英对照、图表风格、术语与记号禁令、文献 key 清单。
- **自定义环境**：`preamble.tex:81–108` 用 `\newtcolorbox` 定义：
  - `problemchain`（问题链）
  - `methodcard`（方法卡片）
  - `ch4box`（CH₄ 算例，def2-TZVPP）
  - `pitfall`（常见陷阱）
- **文献库**：`refs.bib` 共 **63** 个 `@...` entry；`main.bbl` 有 60 个 `\bibitem`，正文 60 个 cite key 全部存在，0 undefined citation。未使用的 3 个 entry（`cramer2004`、`ernzerhof1999`、`neese2012orca`）不影响引文完整性。
- **文档类**：`main.tex:6` 使用 ctexart + XeLaTeX + fandol，符合 IS-1/IS-10 的工程约定。

---

## 3. 计划 Success criteria 证据列复核

| IS | 计划证据 | 实际核验 |
|----|----------|----------|
| IS-1 | `main.pdf` | 存在，1,208,499 bytes，102 页 |
| IS-2 | `grep problemchain = 16` | 16 个 `\begin{problemchain}`，16/16 三问齐全 |
| IS-3 | 审计报告 | `docs/data-audit.md` 33/33 box 数值 PASS；`docs/equation-audit.md` 163/163；`docs/logic-audit.md` 16/16 |
| IS-4 | `figures/` 曲线 PDF | `figures/ch07/h2m_pes.pdf`、`figures/ch08/h2m_mr.pdf`、`figures/ch16/ch4_deviations.pdf` |
| IS-5 | `ch4_results.csv` | 10 个 DFT 代表全部在 CSV、Ch10–13、Ch16 总表 |
| IS-6 | `runs/ch4/` 输入文件 | 20 个 `.inp`；16 def2-TZVPP + 2 内置 3c + 2 无基组 |
| IS-7 | `data/*.csv` | 20 + 48 行；parse_orca 20/20；48 个 H₂⁻ 输出逐项匹配 |
| IS-8 | `main.log` | 0 undefined、0 multiply、0 missing；PDF 0 `??` |
| IS-9 | `sections/ch01`, `ch16` | 17 行表 + 方法地图 + 决策树 |
| IS-10 | `preamble.tex`, `CONTRACT.md` | 四个环境 + 14 节契约 + 63 条 bib |

---

## 4. 非阻断观察（不改变 PASS/APPROVE）

1. **build-check 基线早于 T19**：`docs/build-check.md` 标注 HEAD `5252f1d`，当前 HEAD 为 `b720d76`。T19 的 `docs/audit-fixes.md` §2.2 已记录修复后全量重编译（102 页、0 错误、0 undefined、0 multiply），当前 `main.log` 也显示 102 页、0 错误行。因此 IS-1 以当前构建日志为准，判 PASS。
2. **parse_orca 方法标签**：`scripts/parse_orca.py` 输出的 4 个方法名是 ORCA 关键词名（LDA/XTB/CASSCF/R2SCAN），CSV 用教学名（SVWN5/GFN2-xTB/CASSCF(8,8)/r2SCAN）；能量、基组、收敛标志逐项一致。属标签规范化，不影响数值可追溯性。
3. **Ch1/Ch2/Ch16 无 methodcard/ch4box**：符合 `CONTRACT.md §4` 的“仅方法章需要；第 1、2、16 章可省略”，不是缺口。
4. **3c 复合方法**：B97-3c 与 r²SCAN-3c 使用内置基组（def2-mTZVP/def2-mTZVPP），Ch16 表注明确“不是雅各布天梯的新梯级”；与 IS-6 一致。
5. **H₂⁻ CASPT2 未运行**：Ch16 `:148` 脚注说明 ORCA 6.1.1 的已知段错误；CH₄ 的 CASPT2 行仍存在。属实现限制，不是理论或数据缺口。
6. **H₂⁻ 占据数 2.0/1.0**：`nroots 1` 的 CASSCF(3,2) 在本活性空间呈单组态，书中如实报告，并用 ⟨S²⟩ 与 NEVPT2/MRCI 修正支撑多参考必要性；符合“数据驱动叙事”的验收口径。
7. **Overfull box 5 处**：最大 3.56561pt，均在 <4pt 的非阻断范围内。
8. **refs.bib 63 条 vs 引用 60 条**：3 条未使用 entry 为正常冗余，不构成引用错误。

---

## 5. 最终判定

IS-1 至 IS-10 全部 PASS；计划 Success criteria 的 10 项证据列全部落实；三份审计报告（公式 163/163、逻辑 16/16、数据 316/316）与当前构建日志一致。无阻断性缺口。

**VERDICT: APPROVE**
