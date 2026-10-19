# CONTRACT.md — 并行写作契约（v1.0，冻结）

> **谁必须读这份文件**：所有章节写作 agent（Wave 0–3）、公式/逻辑/对账审计 agent（Wave 4）、以及任何要改动 `sections/`、`figures/` 的人。
> 本文件是全书的"宪法"。与本文冲突的写作习惯一律以本文为准。发现本文有错，报集成者修订，不要自行偏离。
> 最后更新：2026-10-19（T3）。

---

## 目录

1. [符号约定](#1-符号约定)
2. [单位约定](#2-单位约定)
3. [公式宏列表](#3-公式宏列表)
4. [章节模板](#4-章节模板)
5. [16 章问题链交接表](#5-16-章问题链交接表)
6. [标签约定](#6-标签约定)
7. [文献约定](#7-文献约定)
8. [数据约定](#8-数据约定)
9. [文件所有权](#9-文件所有权)
10. [页数配额](#10-页数配额)
11. [术语中英对照表](#11-术语中英对照表)
12. [图表风格](#12-图表风格)
13. [术语与记号禁令](#13-术语与记号禁令)
14. [文献 key 清单](#14-文献-key-清单)

---

## 1. 符号约定

### 1.1 指标（指标字母冻结，禁止挪用）

| 记号 | 含义 |
|------|------|
| $i,\ j,\ k$ | 占据（occupied）自旋轨道 |
| $a,\ b,\ c$ | 虚（virtual）自旋轨道 |
| $p,\ q,\ r$ | 一般（任意）自旋轨道 |
| $\mu,\ \nu,\ \lambda$ | 基函数（AO）指标 |
| $A,\ B$ | 原子核指标 |
| $I,\ J$ | 行列式 / 组态指标 |
| $\alpha,\ \beta$ | 自旋分量 |

### 1.2 常用对象（已冻结）

| 记号 | 含义 |
|------|------|
| $\chi_\mu(\mathbf{r})$ | 基函数 |
| $\psi_p(\mathbf{x})$ | 自旋轨道（$\mathbf{x}$ 含空间与自旋） |
| $\phi_p(\mathbf{r})$ | 空间轨道 |
| $\Psi$ | 精确（多电子）波函数 |
| $\Phi_0$ | HF 基态 Slater 行列式 |
| $\varepsilon_p$ | 轨道能 |
| $h_{pq}$ | 单电子积分 |
| $(pq\vert rs)$ | 双电子积分，化学家记号 |
| $J_{pq},\ K_{pq}$ | Coulomb 积分、交换积分 |
| $E_{\mathrm{corr}}$ | 相关能（$E_{\mathrm{corr}}=E_{\mathrm{exact}}-E_{\HF}$，Löwdin 定义） |
| $\rho(\mathbf{r})$ | 电子密度 |
| $\tau(\mathbf{r})$ | 动能密度 |
| $s$ | 约化密度梯度 |
| $\alpha$ | iso-orbital 指示器（$0\le\alpha$；单轨道区 $\alpha=0$，均匀区 $\alpha=1$） |
| $\op{T}_1,\ \op{T}_2$ | 耦合簇单/双激发簇算符 |
| $t_i^a,\ t_{ij}^{ab}$ | CC 振幅 |
| $E^{(2)}$ | 微扰二阶能量修正（MP2） |
| $\langle S^2\rangle$ | 自旋平方期望值（自旋污染指标） |

方法下标一律用 §3 的宏：$E_{\HF}$、$E_{\mathrm{MP2}}$、$E_{\xc}$ 等，不手写 `\mathrm{HF}`。

### 1.3 Dirac 记号宏（重要）

`\ket`、`\bra`、`\braket` **不是** braket 宏包提供的——braket 宏包**未安装**。它们是本项目在 `preamble.tex` 中自定义的宏。因此：

- 禁止 `\usepackage{braket}`；
- 禁止在章节文件中 `\newcommand` 任何与 §3 重名的宏；
- 用法完全按 §3 的签名来。

---

## 2. 单位约定

1. **公式与推导**：一律原子单位（$m_e = e = \hbar = 1$），方程中不出现单位。
2. **绝对能量**：Hartree（Eh），保留 **6 位小数**（与 CSV 中 `energy` 列一致）。
3. **能量差 ΔE**：kcal·mol⁻¹，保留 2 位小数。换算因子全书唯一：
   $$1\ \mathrm{Eh} = 627.509474\ \mathrm{kcal\cdot mol^{-1}}$$
4. **键长 / 坐标**：Å（势能曲线横坐标 R 用 Å，取 1 位小数网格 0.6–3.0）。
5. **角度**：度（°）。
6. **⟨S²⟩**：无量纲，随 CSV 精度（6 位小数）引用。
7. 全书**不使用** kJ·mol⁻¹ 作能量单位；如确需提及，写"1 kcal·mol⁻¹ = 4.184 kJ·mol⁻¹"一次即可。
8. ΔE 的定义冻结为：
   $$\Delta E_{\mathrm{method}} = \left(E_{\mathrm{method}} - E_{\mathrm{CCSD(T)}}\right)\times 627.509474 \quad (\mathrm{kcal\cdot mol^{-1}})$$
   正值 = 高于参考。参考值 = CCSD(T)/def2-TZVPP（CH₄ 行）。见 §8 关于 xTB/GFN-FF 的禁令。

---

## 3. 公式宏列表

以下宏由 `preamble.tex`（T2）定义。章节作者**只使用，不定义**。任何章节不得出现 `\newcommand` / `\renewcommand` / `\DeclareMathOperator`（确有需要走 §13 流程）。

| 宏（用法） | 展开 | 典型用途 |
|------------|------|----------|
| `\dd x` | `\mathrm{d}x` | 微分：`\int f(r)\,\dd r` |
| `\ee` | `\mathrm{e}` | 自然常数 / 指数算符：`\ee^{\op{T}}` |
| `\ii` | `\mathrm{i}` | 虚数单位 |
| `\HF` | `\mathrm{HF}` | 方法下标：`E_\HF` |
| `\xc` | `\mathrm{xc}` | 交换相关下标：`E_\xc`、`v_\xc` |
| `\braket{a\|b}` | `\langle a \mid b \rangle` | 内积 |
| `\bracket{a\|O\|b}` | `\langle a \mid O \mid b \rangle` | 矩阵元 / 期望值 |
| `\ket{ψ}` | `\lvert \psi \rangle` | 右矢 |
| `\bra{ψ}` | `\langle \psi \rvert` | 左矢 |
| `\op{A}` | `\hat{A}` | 算符帽子：`\op{F}`、`\op{H}`、`\op{T}_2` |

说明：

- `\braket` / `\bracket` 的参数中竖线直接写 `|`（T2 负责将其按 `\mid` 间距排版）；
- 算符一律套 `\op{}`，不用 `\hat` 裸写；
- 方法名做下标时，双字符以上用宏或 `\mathrm{}`：`E_{\mathrm{MP2}}`、`E_{\mathrm{CCSD(T)}}`、`E_{\mathrm{CASPT2}}`；
- 泛函名直接作名词时用正体普通文本：B3LYP、PBE0、ωB97M-V（写作 `$\omega$B97M-V`）、r²SCAN（写作 `r$^2$SCAN`）。

---

## 4. 章节模板

> **集成说明（T2）**: 章节文件写 `\section{<标题>}`，不要写 '第 X 章：' 前缀；`preamble.tex` 自动生成 '第 N 章' 编号，写前缀会重复。

每个章节文件（`sections/chXX-slug.tex`）**必须**按以下顺序组织。文件以 `\section` 开头（`main.tex` 用 `\include` 负责换页；章节文件内不出现 `\chapter`、`\documentclass`、导言区）。

**顺序（不可调换）**：
1. `\begin{problemchain}` —— 章首问题链（三问齐全）；
2. `\begin{methodcard}` —— 方法卡片（仅"方法章"需要；第 1、2、16 章可省略）；
3. 正文小节（`\subsection`）；
4. `\begin{ch4box}` —— CH₄ 数值框（数值只来自 CSV，见 §8）；
5. `\begin{pitfall}` —— 常见陷阱框；
6. 小结（`\subsection*{小结}`）+ **明确的过渡句**指向下一章。

**可直接复制的骨架**：

```latex
% ============================================================
% sections/chXX-slug.tex —— 第 X 章：<中文标题>
% 页数配额：N 页（±1）。数值只取自 data/*.csv。
% ============================================================

\section{第 X 章：<中文标题>}
\label{ch:XX:sec:title}

% ---- 1. 问题链（三问齐全，措辞与 §5 交接表一致） ----
\begin{problemchain}
\textbf{上一章留下的问题：}……（承接第 X--1 章“本章留下的新问题”）\\
\textbf{本章为什么存在：}……\\
\textbf{本章留下的新问题：}……（原文取自 §5 交接表）
\end{problemchain}

% ---- 2. 方法卡片（方法章必有） ----
\begin{methodcard}
\textbf{方法}：<中文名>（<英文缩写>）\quad \textbf{文献}：\citep{key}\\
\textbf{核心近似}：……\\
\textbf{关键方程}：式~\eqref{ch:XX:eq:core}\\
\textbf{ORCA 关键词}：\texttt{! <KEYWORDS>}\\
\textbf{成本标度}：$\mathcal{O}(N^n)$\quad
\textbf{能否变分 / 尺寸一致}：……\\
\textbf{典型失效}：……
\end{methodcard}

% ---- 3. 正文 ----
\subsection{……}
\label{ch:XX:sec:slug}
……（编号方程带 \label{ch:XX:eq:slug}，引用用 \eqref）

% ---- 4. CH4 结果框 ----
\begin{ch4box}
CH$_4$/def2-TZVPP：$E_{\mathrm{XX}} = -40.xxxxxx$\,Eh；
$\Delta E = x.xx$\,kcal·mol$^{-1}$（相对 CCSD(T)）。
\end{ch4box}

% ---- 5. 常见陷阱 ----
\begin{pitfall}
……（本章方法最常被误用的 1--3 个点）
\end{pitfall}

% ---- 6. 小结 + 过渡 ----
\subsection*{小结}
……（3--5 句总结）。……。带着这个问题，我们进入第 X+1 章：<下一章标题>。
```

硬性要求：

- problemchain 三问的措辞必须与 §5 交接表对应单元格一致（可加连接词，不得改问题实质）；
- 过渡句必须出现在小结末尾，点名下一章标题；
- 第 14/15 章的 ch4box **必须**含一句"该总能量与量子化学方法不可直接比较"；
- 每个编号方程都要被正文 `\eqref` 引用或后文使用；每个图/表都要被 `\ref` 引用。

---

## 5. 16 章问题链交接表

**本表是全书逻辑骨架，逐字冻结，不允许偏离、不允许发明替代问题。** 三列分别填入 problemchain 的第一、三问及章节动机。

| 章 | 章标题 | 上一章留下的问题 | 本章为什么存在 | 本章留下的新问题 |
|----|--------|------------------|----------------|------------------|
| 1 | 计算化学到底在解什么问题？ | ——（起点） | 建立方法地图 | 多体薛定谔方程不能直接解 |
| 2 | 为什么多电子方程不能直接解？ | 多体方程不可解 | BO 近似、基组、相关能语言 | 平均场能否近似？ |
| 3 | HF：平均场能走多远？ | 需要可计算近似 | 独立电子 + 反对称波函数 | 缺动态相关能 |
| 4 | MP2：HF 缺失的相关能怎么补？ | HF 缺相关能 | 微扰论二阶修正 | 参考态差时发散、非变分 |
| 5 | CI：能不能系统地加激发组态？ | MP2 依赖单参考 | 变分组态展开 | 截断 CI 不尺寸一致 |
| 6 | CC：如何修复截断 CI 的尺寸一致性？ | CISD 不尺寸一致 | 指数拟设 + 相连簇 | 强静态相关下失效 |
| 7 | CASSCF：当一个行列式不够时怎么办？ | CC 在强静态相关失效 | 活性空间 + 轨道/CI 联合优化 | 缺动态相关 |
| 8 | CASPT2/NEVPT2/MRCI：如何给多参考态补动态相关？ | CASSCF 缺动态相关 | 多参考微扰与 MRCI | 成本高、活性空间选择难 |
| 9 | DFT：能不能不写波函数？ | 多参考路线成本高 | HK 定理 + KS 方程 | $E_\xc$ 泛函未知 |
| 10 | LDA/GGA：密度泛函前两级够用吗？ | $E_\xc$ 未知 | 均匀电子气 + 梯度修正 | 半局域、自相互作用误差 |
| 11 | meta-GGA：加入动能密度能解决什么？ | GGA 仍半局域 | 加入 $\tau$ 与 $\alpha$ | 仍有 SIE、缺非局域相关 |
| 12 | 杂化：精确交换能修正什么？ | meta-GGA 有 SIE | 混入精确交换 | 仍缺动态相关 |
| 13 | 双杂化：把 MP2 装进 DFT 值不值？ | 杂化缺动态相关 | DFT + MP2 微扰项 | $N^5$ 成本、强相关失效 |
| 14 | xTB：如何把成本降到大规模筛选？ | 双杂化仍太贵 | 紧束缚 + SCC | 精度与转移性有限 |
| 15 | 力场：能不能彻底去掉电子？ | xTB 精度/转移性有限 | 经典势能面 | 不能断键、电子转移、激发态 |
| 16 | CH4/H2-：同一分子、不同方法，如何选？ | 方法很多 | 成本-精度-问题类型决策 | ——（结束，决策树收束全书） |

---

## 6. 标签约定

- 格式：`\label{ch:XX:TYPE:slug}`
  - `XX` = 两位章号（`01`–`16`，**补零**）；
  - `TYPE` ∈ `eq` / `fig` / `tab` / `sec`；
  - `slug` = 小写 ASCII 短横线串（如 `hf-energy`, `mp2-denominator`）。
- 示例：`\label{ch:03:eq:hf-energy}`、`\label{ch:07:fig:h2m-pes}`、`\label{ch:16:tab:ch4-summary}`、`\label{ch:02:sec:basis}`。
- 引用：本区内 `式~\eqref{ch:XX:eq:...}`；**跨章引用**用完整标签 `\ref{ch:YY:...}`（如"见第 3 章式~\eqref{ch:03:eq:hf-energy}"）。
- **同一 label 全书只能出现一次**（Wave 门禁：`grep -c 'multiply defined' main.log` = 0）。
- 图表引用一律 `\ref`；公式引用一律 `\eqref`。

---

## 7. 文献约定

- 引擎：**natbib（numeric）+ bibtex**。全书不使用 biblatex/biber。
- 正文命令：
  - `\citep{key}` —— 括号引用（默认）；
  - `\citet{key}` —— 作者入句时（如"Grimme 提出 B2PLYP\citep{grimme2006b2plyp}"用 `\citep`；"Grimme 等人提出了……\citep{grimme2006b2plyp}"亦用 `\citep`；仅当确实要写"文献 [n] 的作者指出……"时用 `\citet`）。
- **只能引用 `refs.bib` 中已存在的 key**（完整清单见 §14）。写入前先查 §14。
- 需要新文献时：
  1. 追加到 **`refs-pending.bib`**（append only），条目上方加一行 `% PENDING: <章节> <为什么需要>`；
  2. 正文中先照常 `\citep{newkey}`；
  3. 由集成者在 Wave 门禁统一审核合并进 `refs.bib`；
  4. **绝不**直接改 `refs.bib`，**绝不**在正文用脚注/手写文献。
- 参考文献表由 `main.tex` 的 `\bibliography{refs}` 生成；章节文件不含 `\bibliography` 命令。
- 每章至少给出方法原始文献（methodcard 的"文献"行）；教科书引用用于推导出处。

---

## 8. 数据约定

**所有数值结果只来自两个 CSV**：

- `data/ch4_results.csv`（20 行：CH₄ 全部方法）
- `data/h2m_pes.csv`（48 行：H₂⁻ 势能扫描，6 方法 × 8 个 R）

规则：

1. **禁止自行运行 ORCA、禁止编造或心算任何数值**。CSV 里没有的数不写。
2. 能量引用精确到**小数点后 6 位**（与 CSV `energy` 列逐位一致）。
3. ΔE 一律按 §2 公式从 CSV 能量换算（保留 2 位小数），参考行 = CCSD(T)/def2-TZVPP。
4. **xTB 与 GFN-FF 的总能量不进入任何 ΔE 表格或偏差条形图**。第 16 章总表中这两行的 ΔE 列填"—"，并加脚注："xTB/GFN-FF 总能量不含完整电子结构意义，与 QM 方法不可直接比较"。
5. 第 14/15 章的 ch4box 引用 xTB/GFN-FF 能量时，**必须**附"与 QM 总能不可直接比较"说明。
6. B97-3c、r2SCAN-3c 使用内置基组（def2-mTZVP / def2-mTZVPP），表格与正文注明"内置基组"，不写 def2-TZVPP。
7. ⟨S²⟩ 数据（h2m_pes.csv 的 S2 列）用于第 7 章自旋污染讨论；引用值与 CSV 一致。
8. CSV 尚未生成（T5/T6 产出）时，章节文件中数值位置写 `\TODO{ch4:MP2}` 式占位注释 `% TODO(data): E_MP2 from ch4_results.csv`，不得先填估计值。

---

## 9. 文件所有权

| 文件 / 目录 | 归属 | 你能做 |
|-------------|------|--------|
| `sections/chXX-*.tex` | 对应章节 agent | 写/改（仅自己的章） |
| `figures/chXX/` | 对应章节 agent | 写/改（仅自己的目录） |
| `refs-pending.bib` | 所有 agent | **追加**（append only，带 `% PENDING` 注释） |
| `sections/` 其他章、`appendix/` | 其他 agent / T14 | 禁止触碰 |
| `preamble.tex`、`main.tex` | T2 | 禁止触碰 |
| `refs.bib`、`CONTRACT.md` | T3 / 集成者 | 禁止触碰 |
| `data/*.csv`、`runs/`、`scripts/` | T4–T6 | 禁止触碰 |

并行写作冲突由本表裁决：越界改动一律回滚。

---

## 10. 页数配额

| 部分 | 配额（页） | 容差 |
|------|-----------|------|
| 第 1 章 | 4 | ±1 |
| 第 2 章 | 7 | ±1 |
| 第 3 章 | 6 | ±1 |
| 第 4 章 | 6 | ±1 |
| 第 5 章 | 6 | ±1 |
| 第 6 章 | 6 | ±1 |
| 第 7 章 | 6 | ±1 |
| 第 8 章 | 5 | ±1 |
| 第 9 章 | 6 | ±1 |
| 第 10 章 | 6 | ±1 |
| 第 11 章 | 5 | ±1 |
| 第 12 章 | 5 | ±1 |
| 第 13 章 | 5 | ±1 |
| 第 14 章 | 5 | ±1 |
| 第 15 章 | 5 | ±1 |
| 第 16 章 | 5 | ±1 |
| 附录 A–D | ~9 | 合计 8–10 |
| 封面/目录/参考文献 | ~6 | —— |
| **全书** | **95–105** | 硬上限 105 |

- 正文小计 ~88 页。单章超配额 +1 页以上必须删推导细节或表格，不得挤占他章。
- 超页时删减优先级：重复性对比表 > 次要推导步骤 > 习题 > 附录 A 重复输入。

---

## 11. 术语中英对照表

同一概念全书用同一中文词（以本表为准）。首次出现时给"中文（English, 缩写）"。

| 中文 | English |
|------|---------|
| 波函数 | wavefunction |
| 多体薛定谔方程 | many-body Schrödinger equation |
| 玻恩-奥本海默近似 | Born-Oppenheimer approximation |
| 电子哈密顿算符 | electronic Hamiltonian |
| 基组 | basis set |
| 原子轨道 | atomic orbital |
| 分子轨道 | molecular orbital |
| 高斯型轨道 | Gaussian-type orbital |
| 斯莱特行列式 | Slater determinant |
| 反对称性 | antisymmetry |
| 变分原理 | variational principle |
| 变分性 | variationality |
| 自洽场 | self-consistent field (SCF) |
| 平均场 | mean field |
| 福克算符 | Fock operator |
| 库仑积分 | Coulomb integral |
| 交换积分 | exchange integral |
| 库普曼斯定理 | Koopmans' theorem |
| 自旋污染 | spin contamination |
| 电子相关 | electron correlation |
| 相关能 | correlation energy |
| 动态相关 | dynamic correlation |
| 静态相关 | static (nondynamic) correlation |
| 尺寸一致性 | size consistency |
| 尺寸广延性 | size extensivity |
| 微扰论 | perturbation theory |
| 二阶修正 | second-order correction |
| 非变分 | non-variational |
| 发散 | divergence |
| 组态相互作用 | configuration interaction (CI) |
| 激发组态 | excited configuration |
| 完全组态相互作用 | full configuration interaction (FCI) |
| 戴维森对角化 | Davidson diagonalization |
| 戴维森校正 | Davidson correction |
| 耦合簇 | coupled cluster (CC) |
| 指数拟设 | exponential ansatz |
| 簇算符 | cluster operator |
| 相连簇 / 连通簇 | connected cluster |
| 非连通簇 | disconnected cluster |
| 振幅方程 | amplitude equation |
| 相似变换 | similarity transformation |
| 活性空间 | active space |
| 活性轨道 | active orbital |
| 完全活性空间自洽场 | complete active space SCF (CASSCF) |
| 态平均 | state averaging |
| 自然轨道 | natural orbital |
| 自然占据数 | natural occupation number |
| 单参考 | single reference |
| 多参考 | multireference |
| 入侵态 | intruder state |
| 零阶哈密顿算符 | zeroth-order Hamiltonian |
| 密度泛函理论 | density-functional theory (DFT) |
| 霍恩贝格-科恩定理 | Hohenberg-Kohn theorem |
| 科恩-沙姆方程 | Kohn-Sham equations |
| 交换相关 | exchange-correlation |
| 交换相关泛函 | exchange-correlation functional |
| 交换相关穴 | exchange-correlation hole |
| 绝热连接 | adiabatic connection |
| 雅各布天梯 | Jacob's ladder |
| 局域密度近似 | local density approximation (LDA) |
| 均匀电子气 | uniform electron gas |
| 广义梯度近似 | generalized gradient approximation (GGA) |
| meta-GGA（动能密度泛函） | meta-generalized gradient approximation |
| 动能密度 | kinetic energy density |
| 等轨道指示器 | iso-orbital indicator |
| 增强因子 | enhancement factor |
| 半局域 | semilocal |
| 自相互作用误差 | self-interaction error (SIE) |
| 杂化泛函 | hybrid functional |
| 全局杂化 | global hybrid |
| 范围分离杂化 | range-separated hybrid |
| 非局域相关 | nonlocal correlation |
| 色散校正 | dispersion correction |
| 双杂化泛函 | double hybrid |
| 自旋分量缩放 | spin-component scaling (SCS) |
| 自旋反对称缩放 | spin-opposite scaling (SOS) |
| 复合方法 | composite method |
| 紧束缚 | tight-binding |
| 自洽电荷 | self-consistent charge (SCC) |
| 半经验方法 | semiempirical method |
| 参数化 | parametrization |
| 力场 | force field |
| 键合项 | bonded term |
| 非键合项 | nonbonded term |
| 键伸缩 | bond stretching |
| 角弯曲 | angle bending |
| 二面角 | dihedral angle |
| 伦纳德-琼斯势 | Lennard-Jones potential |
| 埃瓦尔德求和 | Ewald summation |
| 极化 | polarization |
| 基组叠加误差 | basis set superposition error (BSSE) |
| 辅助基组 | auxiliary basis set |
| 分辨率恒等式近似 | resolution-of-the-identity (RI) approximation |
| 几何抗叠加校正 | geometrical counterpoise correction (gCP) |
| 势能面 | potential energy surface |
| 势能曲线 | potential energy curve |
| 参考值 | reference value |
| 决策树 | decision tree |

（≥40 行要求已满足：本表 90+ 行。）

---

## 12. 图表风格

1. **配色**：色盲友好（Okabe-Ito 调色板为默认）：
   `#000000` 黑、`#E69F00` 橙、`#56B4E9` 天蓝、`#009E73` 青绿、`#F0E442` 黄、`#0072B2` 蓝、`#D55E00` 朱红、`#CC79A7` 粉紫。
2. **灰度可辨**：任何图在黑白打印下必须可读——不同曲线同时用**不同线型**（实线/虚线/点线）与**不同 marker**（`o s ^ D v`）区分，不单靠颜色。
3. **matplotlib 统一设置**（所有脚本）：
   ```python
   import matplotlib
   matplotlib.use("Agg")
   import matplotlib.pyplot as plt
   plt.rcParams["font.sans-serif"] = ["Noto Sans CJK JP", "Droid Sans Fallback"]
   plt.rcParams["axes.unicode_minus"] = False
   ```
   （若 'Noto Sans CJK JP' 中文观感不佳，可整体切换为 'Droid Sans Fallback'，但必须全书一致。）
4. **输出**：一律矢量 PDF，存 `figures/chXX/`；DPI 类设置仅影响栅格元素。
5. **图表必须被正文引用**：每个 `\begin{figure}` / `\begin{table}` 都有 `\label{ch:XX:fig|tab:slug}`，正文有对应 `\ref`。孤立图表按审计 FAIL 处理。
6. 表格用 `booktabs`（`\toprule/\midrule/\bottomrule`），不用竖线。
7. 图注、表头字号不小于正文脚注字号；图内文字避免小于 `\footnotesize` 等价物。
8. TikZ 图（方法地图、决策树）与 matplotlib 图风格保持一致（同一调色板）。

---

## 13. 术语与记号禁令

1. **不引入本契约未冻结的符号、指标用法或宏**（§1、§3 之外的一切数学记号都算"新"）。
2. 确实不可避免时（例如某推导需要新中间量）：
   - 在**同一个 commit** 内把该记号补进 CONTRACT.md §1 或 §3；
   - 在 `.omo/notepads/chem-methods-lecture/learnings.md` 追加一行"新增记号 X：用途，出现章"；
   - 不走此流程的"悄悄新符号"按审计 FAIL 处理。
3. 禁止在同一章内混用同义记号（如 $g(r)$ 与 $\rho(r)$ 混指密度）；禁止将已冻结指标挪作他用（如用 $a$ 表示基函数）。
4. 术语用词以 §11 为准：例如全书用"尺寸一致性"，不用"大小一致性"；用"活性空间"，不用"活化空间"。
5. 不使用未定义的缩写；首次出现给全称（中文或英文均可，按 §11 格式）。

---

## 14. 文献 key 清单

以下 63 个 key 是 `refs.bib` 的全部条目，也是章节可引用的全部范围（`grep -c '@' refs.bib` = 63）。

**教科书（6）**
`szabo1996` `helgaker2000` `jensen2017` `cramer2004` `parr1989` `shavitt2009`

**基础理论（7）**
`hohenberg1964` `kohn1965` `moller1934` `lowdin1955` `lowdin1959corr` `koopmans1934` `burke2012`

**波函数方法（10）**
`cizek1966` `purvis1982` `raghavachari1989` `knowles1988` `werner1988` `roos1980` `andersson1990` `angeli2001` `langhoff1974` `grimme2003scsmp2`

**密度泛函与色散（21）**
`vosko1980` `ceperley1980` `perdew1981sie` `becke1988` `lee1988` `becke1993b3lyp` `perdew1996pbe` `adamo1999pbe0` `ernzerhof1999` `tao2003` `sun2015scan` `furness2020r2scan` `mardirossian2016wb97mv` `grimme2006b2plyp` `goerigk2011pwpb95` `brandenburg2018b973c` `grimme2021r2scan3c` `grimme2010d3` `grimme2011d3bj` `caldeweyher2019d4` `kruse2012gcp`

**基组（4）**
`weigend2005def2` `weigend2006aux` `hellweg2007aux` `dunning1989ccpvdz`

**半经验与力场（11）**
`bannwarth2019gfn2` `spicher2020gfnff` `stewart2007pm6` `dewar1985am1` `dewar1977mndo` `rappe1992uff` `cornell1995amber` `mackerell1998charmm` `jorgensen1996oplsaa` `ewald1921` `lennardjones1931`

**软件与综述（4）**
`neese2012orca` `neese2020orca` `bartlett2007cc` `lischka2018mr`

> 各章 methodcard "文献"行的推荐选择：
> HF→`szabo1996`；MP2→`moller1934`+`grimme2003scsmp2`；CI→`knowles1988`；CC→`cizek1966`+`raghavachari1989`+`bartlett2007cc`；CASSCF→`roos1980`；CASPT2→`andersson1990`；NEVPT2→`angeli2001`；MRCI→`werner1988`+`lischka2018mr`；DFT→`hohenberg1964`+`kohn1965`+`parr1989`；LDA→`vosko1980`+`ceperley1980`；GGA/PBE→`perdew1996pbe`；B97-3c→`brandenburg2018b973c`；TPSS→`tao2003`；r2SCAN→`furness2020r2scan`；r2SCAN-3c→`grimme2021r2scan3c`；B3LYP→`becke1993b3lyp`+`lee1988`+`vosko1980`；ωB97M-V→`mardirossian2016wb97mv`；B2PLYP→`grimme2006b2plyp`；PWPB95→`goerigk2011pwpb95`；xTB→`bannwarth2019gfn2`；GFN-FF→`spicher2020gfnff`。

---

*CONTRACT.md 结束。执行中发现的任何矛盾，以"数据约定 > 标签/宏约定 > 页数配额 > 其他"的优先级暂时裁决，并立即报告集成者。*
