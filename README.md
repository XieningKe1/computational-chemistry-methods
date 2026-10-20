# 计算化学方法讲义

> 从 Hartree–Fock 到分子力场：每个方法为什么存在

![LaTeX](https://img.shields.io/badge/LaTeX-XeLaTeX-008080)
![Pages](https://img.shields.io/badge/pages-102-blue)
![ORCA](https://img.shields.io/badge/ORCA-6.1.1-orange)

一本 102 页的中文讲义，用一条"问题链"串起电子结构方法：从多体薛定谔方程出发，
依次回答 Hartree–Fock 为什么必须做平均场、MP2 补的是什么、截断 CI 为什么尺寸不一致、
耦合簇如何修复它、静态相关何时要求 CASSCF、DFT 的五个梯级各自解决了什么，
最后落到 xTB 与分子力场。每一章都从上一章留下的问题开始，以该方法的失效模式结束。

全书使用同一套算例：**CH₄ 与 H₂⁻，ORCA 6.1.1 / def2-TZVPP**。CH₄ 上并排比较 20 种方法
（HF → CCSD(T)、LDA → 双杂化、xTB、力场），H₂⁻ 上给出 6 种方法 × 8 个键长的势能曲线与
自旋污染诊断。正文中的每张表、每幅图都能追溯到仓库内的原始 ORCA 输入/输出、CSV 与绘图脚本。

## 目录

| 章 | 本章回答的问题 | 源文件 |
|---|---|---|
| 1 | 计算化学到底在解什么问题？ | `sections/ch01-overview.tex` |
| 2 | 为什么多电子方程不能直接解？ | `sections/ch02-foundations.tex` |
| 3 | HF：平均场能走多远？ | `sections/ch03-hf.tex` |
| 4 | MP2：HF 缺失的相关能怎么补？ | `sections/ch04-mp2.tex` |
| 5 | CI：能不能系统地加激发组态？ | `sections/ch05-ci.tex` |
| 6 | CC：如何修复截断 CI 的尺寸一致性？ | `sections/ch06-cc.tex` |
| 7 | CASSCF：当一个行列式不够时怎么办？ | `sections/ch07-casscf.tex` |
| 8 | CASPT2/NEVPT2/MRCI：如何给多参考态补动态相关？ | `sections/ch08-mrpt-mrci.tex` |
| 9 | DFT：能不能不写波函数？ | `sections/ch09-dft.tex` |
| 10 | LDA/GGA：密度泛函前两级够用吗？ | `sections/ch10-lda-gga.tex` |
| 11 | meta-GGA：加入动能密度能解决什么？ | `sections/ch11-meta-gga.tex` |
| 12 | 杂化：精确交换能修正什么？ | `sections/ch12-hybrid.tex` |
| 13 | 双杂化：把 MP2 装进 DFT 值不值？ | `sections/ch13-double-hybrid.tex` |
| 14 | xTB：如何把成本降到大规模筛选？ | `sections/ch14-xtb.tex` |
| 15 | 力场：能不能彻底去掉电子？ | `sections/ch15-force-field.tex` |
| 16 | CH₄/H₂⁻：同一分子、不同方法，如何选？ | `sections/ch16-summary.tex` |

附录：

| 附录 | 内容 | 源文件 |
|---|---|---|
| A | ORCA 环境与输入模板（HF/MP2/CCSD(T)、CASSCF/CASPT2/NEVPT2/MRCI、双杂化、3c、xTB/GFN-FF） | `appendix/app-orca.tex` |
| B | 数据获取方式说明（`runs/` 结构、CSV 列定义、解析与绘图脚本） | `appendix/app-data.tex` |
| C | 习题与解答 | `appendix/app-exercises.tex` |
| D | 术语中英对照表 | `appendix/app-glossary.tex` |

## 快速开始

### 依赖

- **TeX Live 2020 或更新版本**，使用 XeLaTeX 编译。需要 `ctex`（含 fandol 字体）、
  `pgfplots`、`tcolorbox`、`natbib`、`booktabs`、`longtable`、`listings`、`fancyhdr`、`microtype` 等宏包。
- **Python 3.9+**（可选）：仅重绘插图时需要 `numpy`、`pandas`、`matplotlib`。
- **ORCA 6.1.1**（可选）：复现计算时需要，需自行向 ORCA 团队申请授权；本仓库不包含 ORCA 二进制。

### 编译全书

```bash
git clone https://github.com/XieningKe1/computational-chemistry-methods.git
cd computational-chemistry-methods

./build-chapter.sh          # 等价于 latexmk -xelatex main.tex
```

产物为 `main.pdf`（A4，102 页）。仓库内已附编译好的 `main.pdf`，可直接阅读。

### 只编译一章（快速迭代）

```bash
./build-chapter.sh sections/ch03-hf                       # 一章
./build-chapter.sh sections/ch03-hf sections/ch04-mp2     # 多章
```

脚本通过 `\includeonly` 只排版指定章节，产物为 `chapter-build.pdf`。
清理中间文件用 `latexmk -C`。

构建注意：

- 直接调用 latexmk 时请显式给出 `main.tex`。裸跑 `latexmk` 会把同目录的 `preamble.tex`
  当作独立文档，报 `\usepackage before \documentclass`。
- `latexmkrc` 设置 `$pdf_mode = 5`（XeLaTeX → XDV → PDF），不要改成 pdflatex。
- `build-chapter.sh` 会把 `$HOME/texmf-disabled/pgfplots-4.42` 前置到 `TEXINPUTS`，
  用于覆盖本机 pgfplots 版本；该目录不存在时无影响，可按需删除这一行。

## 数据与复现

| 数据 | 内容 |
|---|---|
| `data/ch4_results.csv` | CH₄/def2-TZVPP 的 20 个方法：`method,basis,energy,s2,converged,runtime,inp_path`。参考值 CCSD(T) = −40.438598 Eh。 |
| `data/h2m_pes.csv` | H₂⁻ 势能扫描：6 种方法（UHF、MP2、CCSD(T)、CASSCF、NEVPT2、MRCI）× 8 个键长（0.6–3.0 Å），含 `s2` 列。 |
| `data/h2m_occupations.csv` | CASSCF(3,2) 的自然轨道占据数及其偏离 0/2 的程度。 |
| `data/h2m_report.md`、`data/ch4_notes.md` | 批量作业状态、能量表与偏差诊断。 |
| `runs/ch4/<method>/` | CH₄ 各方法的 ORCA 输入与输出。 |
| `runs/h2m/<method>/R<value>/` | H₂⁻ 各方法、各键长的 ORCA 输入与输出（48 个作业全部正常结束）。 |

重新汇总与绘图：

```bash
# 解析单份 ORCA 输出
python3 scripts/parse_orca.py runs/ch4/hf/hf.out

# 批量解析目录或 glob，写出 CSV
python3 scripts/parse_orca.py --batch runs/ch4 --csv /tmp/ch4.csv
python3 scripts/parse_orca.py --batch 'runs/h2m/*.out' --csv /tmp/h2m.csv

# 重绘插图（--csv / --out 可覆盖默认路径）
python3 scripts/plot_ch4.py --out figures/ch16/ch4_deviations.pdf
python3 scripts/plot_h2m.py
```

提示：总能量对 ORCA 版本、基组与网格敏感，复现正文数值时请固定 ORCA 6.1.1 与
def2-TZVPP（3c 方法除外，它们自带基组）。`ch4_results.csv` 的 `inp_path` 列保留了
作者本机的绝对路径，仅作溯源用。

## 仓库结构

```
.
├── main.tex              # 主文件：封面、目录、16 章 + 4 附录
├── preamble.tex          # 宏包、Okabe–Ito 配色、数学宏
├── latexmkrc             # XeLaTeX 构建配置
├── build-chapter.sh      # 全书 / 单章 / 多章构建脚本
├── sections/             # 16 章正文
├── appendix/             # 附录 A–D
├── figures/              # 正文插图（PDF，由 scripts/ 生成）
├── data/                 # 汇总 CSV 与数据报告
├── runs/                 # ORCA 原始输入/输出（CH₄ 与 H₂⁻）
├── scripts/              # parse_orca.py、plot_ch4.py、plot_h2m.py
├── docs/                 # 构建检查与公式/数据/逻辑审计报告
├── refs.bib              # 参考文献（63 条，正文引用 60 条）
├── CONTRACT.md           # 全书写作契约：符号、单位、宏、标签、图表规范
└── main.pdf              # 编译产物（102 页）
```

## 写作规范

`CONTRACT.md` 是全书的"宪法"，修改 `sections/`、`appendix/` 或新增图表前请先读它。
其中冻结了：

- **指标字母**：`i,j,k` 占据轨道，`a,b,c` 虚轨道，`p,q,r` 一般轨道，`μ,ν,λ` 基函数，
  `A,B` 原子核，`I,J` 行列式，`α,β` 自旋分量。
- **单位与精度**：公式用原子单位；绝对能量用 Eh 并保留 6 位小数，与 CSV `energy` 列一致。
- **数学宏**：`\ket`、`\bra`、`\op`、`\HF`、`\xc`、`\dd` 等一律用 `preamble.tex` 中的定义
  （项目未使用 `braket` 宏包）。
- **标签与文献**：标签按 `ch:NN:...` 命名；文献 key 与 `refs.bib` 保持一致。
- **图表风格**：统一使用色盲友好的 Okabe–Ito 配色，矢量图输出为 PDF。

## 质量检查

`docs/` 记录了构建与内容审计结果：

| 文件 | 内容 |
|---|---|
| `docs/build-check.md` | 全量构建记录：102 页，0 个未解析引用/交叉引用，5 个 overfull box（均 < 4 pt） |
| `docs/equation-audit.md` | 公式推导审计 |
| `docs/data-audit.md` | CSV 与正文数值对账 |
| `docs/logic-audit.md` | 章节逻辑与问题链审计 |
| `docs/audit-fixes.md` | 审计发现的问题及修复记录 |
| `docs/final/` | 终检报告（F1–F4）：计划符合性、代码质量、构建 QA、理想状态检查 |

## 引用

如果这份讲义对你的教学或研究有帮助，请注明出处：

```bibtex
@misc{ke2026chemmethods,
  author = {柯谐宁},
  title  = {计算化学方法讲义：从 Hartree--Fock 到分子力场},
  year   = {2026},
  url    = {https://github.com/XieningKe1/computational-chemistry-methods}
}
```

## 许可

本仓库尚未添加开源许可证（默认保留所有权利）。如需转载、改编或商业使用，
请先通过 GitHub Issues 联系作者。

## 反馈

勘误、算例复现问题或方法解释上的疑问，欢迎提交
[Issue](https://github.com/XieningKe1/computational-chemistry-methods/issues)。
