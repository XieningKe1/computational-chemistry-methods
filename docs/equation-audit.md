# 全书公式审计报告（T16）

> **审计对象**：`sections/ch01-overview.tex` – `sections/ch16-summary.tex`，共 **163 个编号公式**（Ch1 无编号公式；另有 3 个 `align*` 数值代入式在 Ch3/Ch4/Ch9 的 `ch4box` 内，不单独编号，已一并核对）。
> **审计依据**：`CONTRACT.md` §1–§3（冻结符号、单位、宏）与 §14（文献 key）；标准约定参照 Szabo & Ostlund、Helgaker 等。
> **审计方式**：逐条读取 `\begin{equation}` 环境及其上下文，检查因子、符号、归一化、指标/自旋约定与量纲一致性。
> **只读声明**：本次审计**未修改** `sections/`、`appendix/`、`preamble.tex`、`main.tex`、`CONTRACT.md`、`refs.bib`、`data/`、`scripts/`、`runs/`；**未执行 git commit**。

---

## 0. 结论摘要

| 项目 | 数量 |
|---|---:|
| 编号公式总数 | 163 |
| PASS | **159** |
| FAIL | **4** |

**FAIL 清单（4 项）**

| 编号 | 章节 | 公式 label | 文件:行 | 问题摘要 |
|---|---|---|---|---|
| F1 | Ch2 | `ch:02:eq:bsse` | `sections/ch02-foundations.tex:123-125` | BSSE 定义符号与标准约定相反 |
| F2 | Ch5 | `ch:05:eq:davidson-correction` | `sections/ch05-ci.tex:157-162` | Davidson 校正因子应为激发组态权重，写成参考态权重 |
| F3 | Ch5 | `ch:05:eq:pair-error` | `sections/ch05-ci.tex:195-199` | CISD 尺寸一致性误差的符号写反 |
| F4 | Ch10 | `ch:10:eq:grid-quadrature` | `sections/ch10-lda-gga.tex:159-166` | Becke 网格求积权重缺少径向-角向积分权重（量纲不一致） |

> 说明：Ch7/Ch16 的“CASSCF 占据数 2.0/1.0、CASSCF 能量高于 UHF”是 CSV 数据与 `nroots 1` 设定的结果，**不是公式错误**，本报告不将其判为 FAIL。

---

## 1. FAIL 详情

### F1 — Ch2：BSSE 定义符号相反

- **文件:行**：`sections/ch02-foundations.tex:123-125`（`\label{ch:02:eq:bsse}` 在第 125 行；表达式在第 124 行）
- **当前表达式**：
  \[
  \Delta E_{\mathrm{BSSE}}
  = \big(E_A^{AB}+E_B^{AB}\big)-\big(E_A^{A}+E_B^{B}\big).
  \]
- **为什么错**：在二聚体基组中，片段能量只会因额外基函数而降低，即 \(E_A^{AB}\le E_A^{A}\)、\(E_B^{AB}\le E_B^{B}\)，所以当前右端 \(\le 0\)。标准 BSSE 是“片段在二聚体基组中被人为稳定”的正能量：
  \[
  \mathrm{BSSE}=(E_A^{A}+E_B^{B})-(E_A^{AB}+E_B^{AB})\ge 0.
  \]
  原文紧接着说“可把 BSSE 扣除”，这要求 BSSE 为正；当前表达式实际上是标准 BSSE 的相反数（或 counterpoise 校正的负值）。若作者想定义“片段能量因 BSSE 的降低量”，应把符号写成 \(-\Delta E_{\mathrm{BSSE}}\) 或改名为 \(\Delta E_{\mathrm{CP}}\)，不能沿用 \(\Delta E_{\mathrm{BSSE}}\)。
- **修正表达式**：
  \[
  \Delta E_{\mathrm{BSSE}}
  = \big(E_A^{A}+E_B^{B}\big)-\big(E_A^{AB}+E_B^{AB}\big)\ge 0,
  \]
  并以
  \[
  \Delta E_{\mathrm{int}}^{\mathrm{CP}}
  = E_{AB}^{AB}-E_A^{AB}-E_B^{AB}
  \]
  作为 counterpoise 校正后的相互作用能。

### F2 — Ch5：Davidson 校正的因子写成了参考态权重

- **文件:行**：`sections/ch05-ci.tex:157-162`（`\label{ch:05:eq:davidson-correction}` 在第 162 行；错误因子在第 160 行）
- **当前表达式**：
  \[
  E_{\mathrm{CISD}+Q}
  = E_{\mathrm{CISD}}
  + \Big(1-\sum_{I\ne 0}|c_I|^2\Big)
    \big(E_{\mathrm{CISD}}-E_{\mathrm{HF}}\big).
  \]
- **为什么错**：对归一化 CI 波函数，
  \[
  \sum_{I\ne0}|c_I|^2=1-|c_0|^2,
  \]
  因此当前括号等于 \(|c_0|^2\)，即**参考态权重**。标准 Davidson（\(+Q\)）校正的因子是**激发组态权重** \(1-|c_0|^2=\sum_{I\ne0}|c_I|^2\)：波函数越接近单参考（激发权重越小），校正应越小；当前公式恰好相反，单参考时给出接近 1 的大校正，强多参考时反而给出小校正。原文第 164 行“当 \(\sum_{I\ne0}|c_I|^2\) 较小、波函数接近单参考时，它给出合理的改进”也只有在因子取 \(\sum_{I\ne0}|c_I|^2\) 时才成立。
- **修正表达式（归一化波函数）**：
  \[
  E_{\mathrm{CISD}+Q}
  = E_{\mathrm{CISD}}
  + \Big(\sum_{I\ne 0}|c_I|^2\Big)
    \big(E_{\mathrm{CISD}}-E_{\mathrm{HF}}\big),
  \]
  等价地
  \[
  E_{\mathrm{CISD}+Q}
  = E_{\mathrm{CISD}}
  + \big(1-|c_0|^2\big)
    \big(E_{\mathrm{CISD}}-E_{\mathrm{HF}}\big).
  \]
  若采用中间归一化 \(c_0=1\)，因子应写成
  \[
  \frac{\sum_{I\ne0}|c_I|^2}{1+\sum_{I\ne0}|c_I|^2}.
  \]

### F3 — Ch5：CISD 尺寸一致性误差的符号写反

- **文件:行**：`sections/ch05-ci.tex:195-199`（`\label{ch:05:eq:pair-error}` 在第 199 行；错误符号在第 198 行）
- **当前表达式**：
  \[
  E_{\mathrm{CISD}}(A_1\cdots A_n)
  - \sum_{p=1}^{n}E_{\mathrm{CISD}}(A_p)
  = -\sum_{p<q}\Delta_{pq}+\cdots,
  \qquad \Delta_{pq}>0.
  \]
- **为什么错**：CISD 是变分的；在无穷分离极限，超体系 CISD 缺少“两个片段同时发生双激发”的断开四激发。把片段 CISD 波函数相乘会得到这些项，而超体系 CISD 的线性截断把它们丢掉了。丢失的是负的相关贡献，因此超体系 CISD 能量**高于**片段 CISD 能量之和：
  \[
  E_{\mathrm{CISD}}(A_1\cdots A_n)-\sum_p E_{\mathrm{CISD}}(A_p)>0.
  \]
  当前右端在 \(\Delta_{pq}>0\) 时为负，方向相反。原文说“误差随片段数二次增长”，若误差定义为左端，则应为正号。
- **修正表达式**：
  \[
  E_{\mathrm{CISD}}(A_1\cdots A_n)
  - \sum_{p=1}^{n}E_{\mathrm{CISD}}(A_p)
  = +\sum_{p<q}\Delta_{pq}+\cdots,
  \qquad \Delta_{pq}>0,
  \]
  其中 \(\Delta_{pq}\) 是片段对 \((p,q)\) 上被截掉的负相关贡献的绝对值。

### F4 — Ch10：Becke 网格求积权重缺少径向-角向积分权重

- **文件:行**：`sections/ch10-lda-gga.tex:159-166`（`\label{ch:10:eq:grid-quadrature}` 在第 166 行；错误定义在第 163–165 行）
- **当前表达式**：
  \[
  \int f(\mathbf r)\,\dd\mathbf r
  \approx \sum_i w_i\,f(\mathbf r_i),
  \qquad
  w_i=\sum_A w_{Ai},
  \qquad
  w_{Ai}=\frac{P_A(\mathbf r_i)}{\sum_B P_B(\mathbf r_i)}.
  \]
- **为什么错**：\(P_A(\mathbf r_i)/\sum_B P_B(\mathbf r_i)\) 是 Becke fuzzy-cell 的**空间划分权重**，无量纲，且对每个网格点满足 \(\sum_A w_{Ai}=1\)。它不是三维求积权重。真正的求积权重还必须乘上以原子 \(A\) 为中心的径向-角向网格权重（含径向 Jacobian）\(\omega_i^{(A)}\)。按当前写法，\(\sum_i w_i f(\mathbf r_i)\) 只是网格点上的加权平均，不是体积积分；即使 \(f\equiv1\)，也不会得到盒子体积。这是量纲不一致。
- **修正表达式**：
  \[
  \int f(\mathbf r)\,\dd\mathbf r
  \approx \sum_A\sum_{i\in A}
  \frac{P_A(\mathbf r_i)}{\sum_B P_B(\mathbf r_i)}\,
  \omega_i^{(A)}\,f(\mathbf r_i),
  \]
  其中 \(\omega_i^{(A)}\) 是原子 \(A\) 的径向-角向求积权重（含 Jacobian）。等价地，
  \[
  w_i=\sum_A w_{Ai}\,\omega_i^{(A)}.
  \]

---

## 2. 分章审计

> 表中“行号”指该 `\label{ch:XX:eq:...}` 所在行；公式内容可能从上一行开始。PASS 行给出关键核对点；FAIL 行指向第 1 节对应编号。

### 第 1 章（`ch01-overview.tex`）

- 本章无编号公式；只有 TikZ 方法地图与表格。**PASS（0 个公式，无公式级审计项）**。

### 第 2 章（`ch02-foundations.tex`，16 个编号公式）

| 审计项 | 编号公式 | 行号 | 结论 |
|---|---|---|---|
| 分子哈密顿量符号与 \(1/2\) 因子 | `ch:02:eq:mol-hamiltonian` | 28 | PASS：核/电子动能均为 \(-1/2\)（核带 \(1/M_A\)），\(e\)-\(e\) 与核-核排斥为正 |
| BO 分离 | `ch:02:eq:bo-separation` | 35 | PASS：\(\Psi\approx\chi(\mathbf R)\psi(\mathbf r;\mathbf R)\) |
| 电子哈密顿量符号 | `ch:02:eq:el-hamiltonian` | 45 | PASS：电子动能、核吸引、\(e\)-\(e\) 排斥符号正确 |
| 反对称性 | `ch:02:eq:antisymmetry` | 60 | PASS：交换两电子坐标变号 |
| Slater 行列式归一化 | `ch:02:eq:slater` | 72 | PASS：\(1/\sqrt{N!}\) |
| 行列式归一化条件 | `ch:02:eq:determinant-normalization` | 77 | PASS：\(\langle\Phi_0|\Phi_0\rangle=1\) |
| FCI 展开 | `ch:02:eq:fci-expansion` | 84 | PASS：\(\Psi_{\mathrm{FCI}}=\sum_I c_I\Phi_I\) |
| 基组展开 | `ch:02:eq:basis-expansion` | 94 | PASS：\(\phi_p=\sum_\mu C_{\mu p}\chi_\mu\) |
| BSSE 定义 | `ch:02:eq:bsse` | 125 | **FAIL（F1）** |
| 变分原理 | `ch:02:eq:variational` | 137 | PASS：\(E[\Psi]\ge E_0\)，分母 \(\langle\Psi|\Psi\rangle\) 正确 |
| HF 能量与 \(1/2\) | `ch:02:eq:hf-energy` | 144 | PASS：\(\sum_i h_{ii}+\frac12\sum_{ij}[(ii|jj)-(ij|ji)]\) |
| 1-RDM 定义与归一化 | `ch:02:eq:1rdm` | 154 | PASS：前置因子 \(N\)，积分 \(\dd\mathbf x_2\cdots\dd\mathbf x_N\)；\(\mathrm{Tr}\,\gamma_1=N\) |
| 自然轨道本征方程 | `ch:02:eq:natural-orbital` | 160 | PASS：\(\int\gamma_1(\mathbf x,\mathbf x')\phi_k(\mathbf x')\dd\mathbf x'=n_k\phi_k(\mathbf x)\) |
| 相关能定义 | `ch:02:eq:corr-energy` | 170 | PASS：\(E_{\mathrm{corr}}=E_{\mathrm{exact}}-E_{\mathrm{HF}}\)（Löwdin） |
| 尺寸一致性 | `ch:02:eq:size-consistency` | 189 | PASS：\(E_{AB}(R\to\infty)=E_A+E_B\) |
| 尺寸广延性 | `ch:02:eq:size-extensivity` | 194 | PASS：\(E_{A_n}=nE_A\) |

### 第 3 章（`ch03-hf.tex`，17 个编号公式）

| 审计项 | 编号公式 | 行号 | 结论 |
|---|---|---|---|
| 电子哈密顿量拆分 | `ch:03:eq:h-electronic` | 39 | PASS：\(\op H=\sum_i\op h(i)+\sum_{i<j}1/r_{ij}\) |
| 单/双电子积分定义 | `ch:03:eq:integrals` | 58 | PASS：化学家记号 \((pq|rs)\) 的电子 1/电子 2 分组正确 |
| HF 能量与 \(1/2\) | `ch:03:eq:hf-energy` | 68 | PASS：\(\sum_i h_{ii}+\frac12\sum_{ij}[(ii|jj)-(ij|ji)]\) |
| \(J_{ij}\)、\(K_{ij}\) 定义 | `ch:03:eq:jk-integrals` | 82 | PASS：\(J_{ij}=(ii|jj)\)，\(K_{ij}=(ij|ji)\) |
| 库仑/交换算符 | `ch:03:eq:jk-operators` | 93 | PASS：\(\op J_j\) 局域、\(\op K_j\) 非局域，积分核与轨道指标正确 |
| Fock 算符 | `ch:03:eq:fock` | 99 | PASS：\(\op F=\op h+\sum_j^{\mathrm{occ}}(\op J_j-\op K_j)\) |
| 轨道能 | `ch:03:eq:orbital-energy` | 107 | PASS：\(\varepsilon_i=h_{ii}+\sum_j(J_{ij}-K_{ij})\) |
| 总能量由轨道能还原 | `ch:03:eq:energy-from-eps` | 112 | PASS：\(E_{\mathrm{HF}}=\frac12\sum_i(h_{ii}+\varepsilon_i)\) |
| 正则 HF 方程 | `ch:03:eq:canonical` | 122 | PASS：\(\op F\psi_i=\varepsilon_i\psi_i\) |
| 闭壳层密度矩阵 | `ch:03:eq:density-matrix` | 127 | PASS：\(P_{\mu\nu}=2\sum_i^{\mathrm{occ}}C_{\mu i}C_{\nu i}\) |
| 闭壳层 Fock 矩阵与 \(1/2\) | `ch:03:eq:fock-matrix` | 136 | PASS：\(F_{\mu\nu}=h_{\mu\nu}+\sum_{\lambda\sigma}P_{\lambda\sigma}[(\mu\nu|\lambda\sigma)-\frac12(\mu\lambda|\nu\sigma)]\) |
| Roothaan–Hall 方程 | `ch:03:eq:roothaan-hall` | 141 | PASS：\(\mathbf F\mathbf C=\mathbf S\mathbf C\boldsymbol\varepsilon\) |
| SCF 循环 | `ch:03:eq:scf-cycle` | 153 | PASS：\(\mathbf P\to\mathbf F\to\mathbf C\to\mathbf P\) 链正确 |
| UHF Fock 算符 | `ch:03:eq:fock-uhf` | 167 | PASS：库仑对全部占据求和，交换只对同自旋求和 |
| UHF \(\langle S^2\rangle\) | `ch:03:eq:s2` | 175 | PASS：\(S(S+1)+N_\beta-\sum_i^{N_\alpha}\sum_j^{N_\beta}|\langle\psi_i^\alpha|\psi_j^\beta\rangle|^2\)，适用 \(N_\alpha\ge N_\beta\) |
| Koopmans IP | `ch:03:eq:koopmans` | 204 | PASS：\(\mathrm{IP}_k\approx-\varepsilon_k\) |
| Koopmans EA | `ch:03:eq:koopmans-ea` | 211 | PASS：\(\mathrm{EA}_a\approx-\varepsilon_a\) |

### 第 4 章（`ch04-mp2.tex`，13 个编号公式）

| 审计项 | 编号公式 | 行号 | 结论 |
|---|---|---|---|
| MP2 总能量与相关能 | `ch:04:eq:mp2-total` | 38 | PASS：\(E_{\mathrm{MP2}}=E_{\mathrm{HF}}+E^{(2)}\) |
| RS 微扰划分 | `ch:04:eq:partition` | 48 | PASS：\(\op H=\op H_0+\lambda\op V\)，\(\lambda=1\) |
| RS 能量/波函数展开 | `ch:04:eq:rs-expansion` | 55 | PASS：中间归一化 \(\langle\Phi_0|\Psi\rangle=1\) 与展开阶数正确 |
| 一阶能量 | `ch:04:eq:e1` | 60 | PASS：\(E^{(1)}=\langle\Phi_0|\op V|\Phi_0\rangle\) |
| 二阶能量分母 | `ch:04:eq:rs-e2` | 68 | PASS：\(\sum_{n\ne0}|\langle\Phi_n|\op V|\Phi_0\rangle|^2/(E_0^{(0)}-E_n^{(0)})\) |
| MP 划分 | `ch:04:eq:mp-h0` | 81 | PASS：\(\op H_0=\sum_i\op F(i)\)，\(\op V=\sum_{i<j}1/r_{ij}-\sum_i\op v_{\mathrm{HF}}(i)\) |
| 双激发零阶能量 | `ch:04:eq:mp-denominator` | 89 | PASS：\(E_0^{(0)}+\varepsilon_a+\varepsilon_b-\varepsilon_i-\varepsilon_j\) |
| MP1 还原 HF | `ch:04:eq:mp1` | 101 | PASS：\(E^{(1)}=-\frac12\sum_{ij}^{\mathrm{occ}}\langle ij||ij\rangle\)，符号正确 |
| 自旋轨道 MP2 与 \(1/4\) | `ch:04:eq:mp2-energy` | 116 | PASS：\(\frac14\sum_{ij}\sum_{ab}|\langle ij||ab\rangle|^2/(\varepsilon_i+\varepsilon_j-\varepsilon_a-\varepsilon_b)\) |
| 闭壳层空间轨道 MP2 | `ch:04:eq:mp2-closed` | 126 | PASS：\(\sum_{ij}\sum_{ab}(ia|jb)[2(ia|jb)-(ib|ja)]/D\)，因子 2 正确 |
| MP3/MP4 | `ch:04:eq:mp3` | 142 | PASS：\(E_{\mathrm{MP3}}=E_{\mathrm{HF}}+E^{(2)}+E^{(3)}\)，\(E_{\mathrm{MP4}}=E_{\mathrm{MP3}}+E^{(4)}\) |
| SCS-MP2 因子 | `ch:04:eq:scs-mp2` | 156 | PASS：\(c_{\mathrm{OS}}=6/5\)，\(c_{\mathrm{SS}}=1/3\) |
| RI-MP2 分解 | `ch:04:eq:ri-mp2` | 165 | PASS：\((ia|jb)\approx\sum_P B_{ia}^P B_{jb}^P\)，\(B_{ia}^P=\sum_Q(ia|Q)(Q|P)^{-1/2}\) |

### 第 5 章（`ch05-ci.tex`，13 个编号公式）

| 审计项 | 编号公式 | 行号 | 结论 |
|---|---|---|---|
| CI 展开 | `ch:05:eq:ci-expansion` | 37 | PASS：\(|\Psi_{\mathrm{CI}}\rangle=\sum_I c_I|\Phi_I\rangle=(1+\op C)|\Phi_0\rangle\) |
| 激发算子与双激发 \(1/4\) | `ch:05:eq:excitation-operator` | 48 | PASS：\(\op C=\sum c_i^a a_a^\dagger a_i+\frac14\sum c_{ij}^{ab}a_a^\dagger a_b^\dagger a_j a_i+\cdots\) |
| CISD 展开 | `ch:05:eq:cisd` | 58 | PASS：单激发 \(\sum_{i,a}\)，双激发 \(\sum_{i<j}\sum_{a<b}\)，无重复计数 |
| FCI 维数 | `ch:05:eq:fci-dimension` | 71 | PASS：\(\binom{K}{N_\alpha}\binom{K}{N_\beta}\) |
| Slater–Condon 对角元 | `ch:05:eq:slater-diagonal` | 110 | PASS：占据集合上的 HF 型能量 |
| Slater–Condon 非对角元与符号 | `ch:05:eq:slater-offdiagonal` | 123 | PASS：单激发 \(f_{ia}\)，双激发 \(\pm[(ij|ab)-(ib|ja)]\)，\(\pm\) 由置换次数决定 |
| CI 本征方程 | `ch:05:eq:ci-eigen` | 135 | PASS：\(\mathbf H\mathbf c=E\mathbf c\)，\(H_{IJ}=\langle\Phi_I|\op H|\Phi_J\rangle\) |
| 变分能量 | `ch:05:eq:ci-variational` | 143 | PASS：\(\mathbf c^\dagger\mathbf H\mathbf c/\mathbf c^\dagger\mathbf c\ge E_0\) |
| Davidson 预条件 | `ch:05:eq:davidson` | 152 | PASS：\(\mathbf r=\mathbf H\mathbf c-E\mathbf c\)，\(\mathbf d=-(\mathbf D-E\mathbf I)^{-1}\mathbf r\) |
| Davidson 校正 | `ch:05:eq:davidson-correction` | 162 | **FAIL（F2）** |
| 两片段乘积波函数 | `ch:05:eq:product-wavefunction` | 184 | PASS：片段单/双激发乘积中的交叉项在超体系为四激发 |
| 尺寸一致性失败 | `ch:05:eq:size-consistency-failure` | 190 | PASS：\(E_{\mathrm{CISD}}(AB;R\to\infty)\ne E_{\mathrm{CISD}}(A)+E_{\mathrm{CISD}}(B)\) |
| 片段对误差标度 | `ch:05:eq:pair-error` | 199 | **FAIL（F3）** |

### 第 6 章（`ch06-cc.tex`，16 个编号公式）

| 审计项 | 编号公式 | 行号 | 结论 |
|---|---|---|---|
| CC 指数拟设 | `ch:06:eq:cc-wavefunction` | 38 | PASS：\(|\Psi_{\mathrm{CC}}\rangle=e^{\op T}|\Phi_0\rangle\)，\(\op T=\sum_n\op T_n\) |
| 指数展开 | `ch:06:eq:exponential` | 44 | PASS：\(e^{\op T}=1+\op T+\frac12\op T^2+\frac16\op T^3+\cdots\) |
| 一般簇算符 \(1/(n!)^2\) | `ch:06:eq:cluster-general` | 56 | PASS：占据/虚指标各带来 \(1/n!\) |
| \(T_1\) 算符 | `ch:06:eq:t1` | 66 | PASS：\(\op T_1=\sum_{i,a}t_i^a a_a^\dagger a_i\) |
| \(T_2\) 算符 \(1/4\) | `ch:06:eq:t2` | 72 | PASS：\(\op T_2=\frac14\sum t_{ij}^{ab}a_a^\dagger a_b^\dagger a_j a_i\) |
| \(T_1\) 诊断 | `ch:06:eq:t1-diagnostic` | 81 | PASS：\(T_1=\sqrt{\frac1N\sum_{i,a}|t_i^a|^2}\)，\(N\) 取电子数 |
| 相似变换 Hamiltonian | `ch:06:eq:similarity` | 95 | PASS：\(\bar H=e^{-\op T}\op H e^{\op T}\)，\(\bar H|\Phi_0\rangle=E|\Phi_0\rangle\) |
| BCH 展开与四体截断 | `ch:06:eq:bch` | 106 | PASS：\([\op H,\op T]\)、\(\frac12[[\op H,\op T],\op T]\) 至 \(\frac1{24}\) 四重对易子，符号正确 |
| CCSD 能量与 \(1/4\)/\(2\) | `ch:06:eq:cc-energy` | 121 | PASS：\(E_{\mathrm{HF}}+\sum f_{ia}t_i^a+\frac14\sum[(ij|ab)-(ij|ba)](t_{ij}^{ab}+2t_i^at_j^b)\)，指标按第 4 章反对称化约定 |
| 振幅投影 | `ch:06:eq:cc-amplitude` | 130 | PASS：\(\langle\Phi_i^a|\bar H|\Phi_0\rangle=0\)，\(\langle\Phi_{ij}^{ab}|\bar H|\Phi_0\rangle=0\) |
| 双激发方程示意 | `ch:06:eq:ccsd-doubles` | 139 | PASS（示意）：\(\Delta_{ij}^{ab}t_{ij}^{ab}=\langle ij|ab\rangle+\cdots\)，\(\Delta=\varepsilon_i+\varepsilon_j-\varepsilon_a-\varepsilon_b\) |
| CCSD(T) \(1/36\) 与分母 | `ch:06:eq:ccsd-t` | 159 | PASS：\(\frac1{36}\sum|W_{ijk}^{abc}|^2/\Delta_{ijk}^{abc}\)，\(\Delta=\varepsilon_i+\varepsilon_j+\varepsilon_k-\varepsilon_a-\varepsilon_b-\varepsilon_c\) |
| EOM-CC 左右本征方程 | `ch:06:eq:eom-cc` | 177 | PASS：\(\bar H\op R_k|\Phi_0\rangle=\omega_k\op R_k|\Phi_0\rangle\)，\(\langle\Phi_0|\op L_k\bar H=\omega_k\langle\Phi_0|\op L_k\) |
| \(\Lambda\) 方程 | `ch:06:eq:lambda` | 186 | PASS：\(\langle\Phi_0|(1+\op\Lambda)(\bar H-E)|\Phi_i^a\rangle=0\)（及双激发） |
| 指数因子化 | `ch:06:eq:factorization` | 197 | PASS：\(e^{\op T_A+\op T_B}=e^{\op T_A}e^{\op T_B}\)（不相交轨道对易） |
| CC 能量可加性 | `ch:06:eq:cc-additivity` | 203 | PASS：\(E_{AB}(R\to\infty)=E_A+E_B\) |

### 第 7 章（`ch07-casscf.tex`，10 个编号公式）

| 审计项 | 编号公式 | 行号 | 结论 |
|---|---|---|---|
| 两行列式波函数与归一化 | `ch:07:eq:static-two-det` | 40 | PASS：\(|c_1|^2+|c_2|^2=1\) |
| CAS\((n_{\mathrm{el}},n_{\mathrm{orb}})\) 定义 | `ch:07:eq:active-space` | 54 | PASS：\(n_{\mathrm{el}}=\sum_{p\in\mathcal A}n_p\)，\(|\mathcal A|=n_{\mathrm{orb}}\) |
| CASSCF 波函数 | `ch:07:eq:casscf-wavefunction` | 71 | PASS：非活性双占据 \(\prod a_i^\dagger a_{\bar i}^\dagger\) 作用于活性真空 |
| CASSCF 能量期望 | `ch:07:eq:casscf-energy` | 80 | PASS：\(\langle\Psi|\op H|\Psi\rangle/\langle\Psi|\Psi\rangle\) |
| 轨道旋转生成元反厄米性 | `ch:07:eq:orbital-generator` | 92 | PASS：\(\kappa_{pq}=-\kappa_{qp}^{*}\) |
| 幺正变换 \(e^\kappa\) | `ch:07:eq:orbital-rotation` | 99 | PASS：\(\op U=e^{\op\kappa}\)，\(|\tilde p\rangle=\op U|p\rangle\) |
| 活性空间 CI 本征方程 | `ch:07:eq:ci-eigen` | 109 | PASS：\(\sum_J\langle\Phi_I|\op H_{\mathrm{act}}|\Phi_J\rangle c_J=E c_I\) |
| 轨道-CI 梯度对易子 | `ch:07:eq:orbital-ci-gradient` | 118 | PASS：\(\partial E/\partial\kappa_{pq}=0\iff\langle\Psi|[\op H,a_p^\dagger a_q]|\Psi\rangle=0\)，符号与反厄米参数化一致 |
| 态平均权重 | `ch:07:eq:state-average` | 132 | PASS：\(E_{\mathrm{avg}}=\sum_k w_kE_k\)，\(\sum_k w_k=1\) |
| 自然占据数求和与行列式标度 | `ch:07:eq:determinant-count` | 146 | PASS：\(N_{\det}\sim\binom{2n_{\mathrm{orb}}}{n_{\mathrm{el}}}\)（标度估计；固定 \(M_S\) 时实际数更小） |

### 第 8 章（`ch08-mrpt-mrci.tex`，8 个编号公式）

| 审计项 | 编号公式 | 行号 | 结论 |
|---|---|---|---|
| CASPT2 划分 | `ch:08:eq:partition` | 38 | PASS：\(\op H=\op H_0+\op V\)，\(\op H_0=\op P\op F\op P+\op Q\op F\op Q\) |
| 二阶有效 Hamiltonian | `ch:08:eq:caspt2-effective` | 49 | PASS：\(\op P\op H\op P+\op P\op V\op Q(E_0-\op H_0)^{-1}\op Q\op V\op P\) |
| PT2 能量与分母符号 | `ch:08:eq:pt2-energy` | 57 | PASS：\(\sum_{K\notin P}|\langle\Phi_K|\op V|\Psi_0\rangle|^2/(E_0-E_K)\)，基态分母为负，修正为负 |
| Dyall Hamiltonian | `ch:08:eq:dyall` | 72 | PASS：非活性/虚轨道单体项 \(+\) 活性空间 \(\op H_{\mathrm{act}}\) |
| NEVPT2 八类求和 | `ch:08:eq:nevpt2-energy` | 83 | PASS：\(\sum_{l=1}^{8}\sum_{K\in Q_l}|\langle\Phi_K|\op V|\Psi_0\rangle|^2/(E_0^{(0)}-E_K^{(0)})\) |
| MRCI 展开 | `ch:08:eq:mrci-wavefunction` | 94 | PASS：\(|\Psi_{\mathrm{MRCI}}\rangle=\sum_I c_I|\Phi_I\rangle\)，参考 \(+\) 单双激发 |
| Davidson 校正符号/因子 | `ch:08:eq:davidson` | 104 | PASS：\(E_{\mathrm{MRCI}}+(1-\sum_{I\in\mathrm{ref}}|c_I|^2)(E_{\mathrm{MRCI}}-E_{\mathrm{ref}})\)，求和为参考态权重，因子为激发权重 |
| 尺寸一致性条件 | `ch:08:eq:size-consistency` | 111 | PASS：\(E_{AB}(R\to\infty)=E_A+E_B\) |

### 第 9 章（`ch09-dft.tex`，12 个编号公式）

| 审计项 | 编号公式 | 行号 | 结论 |
|---|---|---|---|
| HK1 | `ch:09:eq:hk1` | 35 | PASS：\(\rho_0\leftrightarrow v_{\mathrm{ext}}+\text{const}\) |
| HK2 | `ch:09:eq:hk2` | 48 | PASS：\(E[\rho]\ge E[\rho_0]=E_0\)，\(\int\rho=N\) |
| Levy 约束搜索 | `ch:09:eq:levy` | 58 | PASS：\(F[\rho]=\min_{\Psi\to\rho}\langle\Psi|\op T+\op V_{ee}|\Psi\rangle\) |
| 能量泛函 | `ch:09:eq:energy-functional` | 63 | PASS：\(E[\rho]=F[\rho]+\int v_{\mathrm{ext}}\rho\,\dd\mathbf r\) |
| KS 密度 | `ch:09:eq:ks-density` | 73 | PASS：\(\rho=\sum_i^{\mathrm{occ}}|\phi_i|^2\) |
| KS 轨道方程与 \(v_s\) | `ch:09:eq:ks-equation` | 81 | PASS：\([-\frac12\nabla^2+v_s]\phi_i=\varepsilon_i\phi_i\)，\(v_s=v_{\mathrm{ext}}+v_{\mathrm H}+v_{\mathrm{xc}}\) |
| KS 能量泛函 | `ch:09:eq:ks-energy` | 90 | PASS：\(T_s+\int v_{\mathrm{ext}}\rho+J+E_{\mathrm{xc}}\) |
| \(E_{\mathrm{xc}}\) 定义 | `ch:09:eq:exc-def` | 97 | PASS：\(E_{\mathrm{xc}}=T-T_s+V_{ee}-J\) |
| \(v_{\mathrm{xc}}\) 泛函导数 | `ch:09:eq:vxc` | 102 | PASS：\(v_{\mathrm{xc}}=\delta E_{\mathrm{xc}}/\delta\rho\) |
| XC 穴求和规则 | `ch:09:eq:xc-hole` | 112 | PASS：\(\int\rho_{\mathrm{xc}}(\mathbf r,\mathbf r')\,\dd\mathbf r'=-1\) |
| 交换/相关拆分 | `ch:09:eq:exc-split` | 119 | PASS：\(E_{\mathrm{xc}}=E_x+E_c\) |
| 绝热连接 | `ch:09:eq:ac` | 134 | PASS：\(E_{\mathrm{xc}}=\int_0^1\dd\lambda\langle\Psi_\lambda|\op V_{ee}|\Psi_\lambda\rangle-J\) |

### 第 10 章（`ch10-lda-gga.tex`，12 个编号公式）

| 审计项 | 编号公式 | 行号 | 结论 |
|---|---|---|---|
| LDA 能量 | `ch:10:eq:lda-energy` | 36 | PASS：\(\int\rho\,\varepsilon_{\mathrm{xc}}^{\mathrm{unif}}(\rho)\,\dd\mathbf r\) |
| LDA 交换与 \(C_x\) | `ch:10:eq:lda-exchange` | 51 | PASS：\(E_x=-C_x\int\rho^{4/3}\)，\(C_x=\frac34(\frac3\pi)^{1/3}\approx0.7386\) |
| VWN5 相关 | `ch:10:eq:lda-correlation` | 63 | PASS：\(r_s=(3/(4\pi\rho))^{1/3}\)，\(\zeta=(\rho_\alpha-\rho_\beta)/\rho\) |
| LDA 交换势 | `ch:10:eq:lda-potential` | 72 | PASS：\(v_x=-\frac43C_x\rho^{1/3}\) |
| 约化密度梯度 | `ch:10:eq:reduced-gradient` | 84 | PASS：\(s=|\nabla\rho|/(2k_F\rho)\)，\(k_F=(3\pi^2\rho)^{1/3}\) |
| GGA 交换 | `ch:10:eq:gga-exchange` | 91 | PASS：\(\int\rho\,\varepsilon_x^{\mathrm{unif}}(\rho)F_x(s)\,\dd\mathbf r\) |
| PBE 增强因子与 \(\kappa,\mu\) | `ch:10:eq:gga-enhancement` | 106 | PASS：\(F_x=1+\kappa-\kappa/(1+\mu s^2/\kappa)\)，\(\kappa=0.804\)，\(\mu=0.21951\) |
| PBE 极限 | `ch:10:eq:enhancement-limits` | 113 | PASS：\(F_x(0)=1\)，\(F_x(\infty)=1+\kappa\approx1.804\) |
| PBE 相关 \(H\) 与 \(t\) | `ch:10:eq:pbe-correlation` | 126 | PASS：\(H=\gamma\phi^3\ln\{1+\frac\beta\gamma t^2\frac{1+At^2}{1+At^2+A^2t^4}\}\)，\(t=|\nabla\rho|/(2\phi k_s\rho)\)，\(k_s=(4k_F/\pi)^{1/2}\)，\(A\) 定义正确 |
| D3(BJ) 阻尼 | `ch:10:eq:d3bj` | 140 | PASS：\(R^6+(a_1R^0+a_2)^6\) 与 \(R^8+(a_1R^0+a_2)^8\) |
| B97-3c 能量分解 | `ch:10:eq:b973c-energy` | 151 | PASS：\(E_{\mathrm{xc}}^{\mathrm{B97}}+E_{D3(\mathrm{BJ})}+E_{\mathrm{SRB}}+E_{\mathrm{nuc}}\) |
| Becke 网格求积权重 | `ch:10:eq:grid-quadrature` | 166 | **FAIL（F4）** |

### 第 11 章（`ch11-meta-gga.tex`，10 个编号公式）

| 审计项 | 编号公式 | 行号 | 结论 |
|---|---|---|---|
| 动能密度 \(\tau\) | `ch:11:eq:tau` | 35 | PASS：\(\tau=\frac12\sum_i^{\mathrm{occ}}|\nabla\phi_i|^2\) |
| \(\tau_W\)、\(\tau_{\mathrm{unif}}\) | `ch:11:eq:tau-components` | 44 | PASS：\(\tau_W=|\nabla\rho|^2/(8\rho)\)，\(\tau_{\mathrm{unif}}=\frac3{10}(3\pi^2)^{2/3}\rho^{5/3}\) |
| 等轨道指示器 \(\alpha\) | `ch:11:eq:alpha` | 49 | PASS：\(\alpha=(\tau-\tau_W)/\tau_{\mathrm{unif}}\) |
| meta-GGA 一般形式 | `ch:11:eq:meta-form` | 58 | PASS：\(\int\rho\,\varepsilon_{\mathrm{xc}}(\rho,\nabla\rho,\tau)=\int\rho\,\varepsilon_{\mathrm{xc}}(\rho,s,\alpha)\) |
| TPSS 增强因子与 \(x,z,c,\kappa\) | `ch:11:eq:tpss-enhancement` | 73 | PASS：\(F_x=1+\kappa-\kappa/(1+x/\kappa)\)，\(x=[(10/81+cz^2)/(1+z^2)^2]p\)，\(z=\frac53\tau_W/\tau\)，\(c=1.59096\)，\(\kappa=0.804\) |
| r²SCAN 正则化 \(\alpha\) 与 \(\eta\) | `ch:11:eq:r2scan-alpha` | 89 | PASS：\(\bar\alpha=(\tau-\tau_W)/(\tau_{\mathrm{unif}}+\eta\tau_W)\)，\(\eta=0.001\) |
| r²SCAN 增强因子 | `ch:11:eq:r2scan-enhancement` | 97 | PASS（示意）：与 TPSS 同形式，\(x=x(p,\bar\alpha)\)，\(\kappa=0.804\) |
| D4 色散 | `ch:11:eq:d4` | 111 | PASS：\(-\frac12\sum_{A\ne B}[s_6C_6(\mathbf q)f_6/R^6+s_8C_8(\mathbf q)f_8/R^8]\) |
| gCP | `ch:11:eq:gcp` | 120 | PASS：\(\sum_{A<B}\epsilon_{AB}\exp[-\alpha_{AB}(R_{AB}-R_{AB}^0)]\) |
| r²SCAN-3c 能量分解 | `ch:11:eq:r2scan3c-energy` | 131 | PASS：\(E_{\mathrm{xc}}^{\mathrm{r^2SCAN}}+E_{D4}+E_{\mathrm{gCP}}+E_{\mathrm{nuc}}\) |

### 第 12 章（`ch12-hybrid.tex`，9 个编号公式）

| 审计项 | 编号公式 | 行号 | 结论 |
|---|---|---|---|
| SIE 残余 | `ch:12:eq:sie` | 44 | PASS：\(\Delta_{\mathrm{SIE}}=E_{\mathrm H}+E_{\mathrm{xc}}\ne0\)，\(E_{\mathrm H}=\frac12\iint\rho_1\rho_1'/|\mathbf r-\mathbf r'|\) |
| 杂化 SIE 缩放 | `ch:12:eq:sie-hybrid` | 52 | PASS：\(\Delta_{\mathrm{SIE}}^{\mathrm{hybrid}}\approx(1-a_x)\Delta_{\mathrm{SIE}}^{\mathrm{DFT}}\) |
| 全局杂化 | `ch:12:eq:global-hybrid` | 65 | PASS：\(a_xE_x^{\mathrm{HF}}+(1-a_x)E_x^{\mathrm{DFT}}+E_c^{\mathrm{DFT}}\) |
| B3LYP 系数 | `ch:12:eq:b3lyp` | 77 | PASS：\(0.20/0.80/0.72/0.81/0.19\)，\(\Delta E_x^{\mathrm{B88}}=E_x^{\mathrm{B88}}-E_x^{\mathrm{LDA}}\) |
| 范围分离恒等式 | `ch:12:eq:range-separation` | 89 | PASS：\(1/r=\operatorname{erf}(\omega r)/r+\operatorname{erfc}(\omega r)/r\)；\(\operatorname{erf}/r\) 为长程，\(\operatorname{erfc}/r\) 为短程 |
| RSH 交换 | `ch:12:eq:rsh-exchange` | 97 | PASS：\(E_{x,\mathrm{SR}}^{\mathrm{DFT}}+a_{\mathrm{SR}}E_{x,\mathrm{SR}}^{\mathrm{HF}}+a_{\mathrm{LR}}E_{x,\mathrm{LR}}^{\mathrm{HF}}\)（\(a_{\mathrm{LR}}=1\) 时无长程 DFT 交换） |
| VV10 能量 | `ch:12:eq:vv10` | 113 | PASS：\(\frac12\iint\rho\rho'K_{\mathrm{nl}}\,\dd\mathbf r\,\dd\mathbf r'\) |
| VV10 核 | `ch:12:eq:vv10-kernel` | 124 | PASS：\(-\frac32/[g(\mathbf r,\mathbf r')g(\mathbf r',\mathbf r)(g(\mathbf r,\mathbf r')+g(\mathbf r',\mathbf r))]\)，\(g=\omega_0|\mathbf r-\mathbf r'|^2+\kappa\) |
| 杂化成本 | `ch:12:eq:hybrid-cost` | 136 | PASS：\(c_3N^3+c_4N^4=\mathcal O(N^4)\) |

### 第 13 章（`ch13-double-hybrid.tex`，8 个编号公式）

| 审计项 | 编号公式 | 行号 | 结论 |
|---|---|---|---|
| 双杂化一般式 | `ch:13:eq:double-hybrid` | 41 | PASS：\(a_xE_x^{\mathrm{HF}}+(1-a_x)E_x^{\mathrm{DFT}}+(1-a_c)E_c^{\mathrm{DFT}}+a_cE_c^{\mathrm{MP2}}\) |
| B2PLYP 参数 | `ch:13:eq:b2plyp` | 57 | PASS：\(0.53/0.47/0.73/0.27\) |
| PWPB95 参数与 OS-PT2 | `ch:13:eq:pwpb95` | 71 | PASS：\(0.50/0.50/0.731/0.269\)，OS-PT2 只保留反旋项 |
| MP2 项 \(1/4\) 与分母 | `ch:13:eq:mp2-term` | 87 | PASS：\(\frac14\sum_{ij}\sum_{ab}|\langle ij||ab\rangle|^2/(\varepsilon_i+\varepsilon_j-\varepsilon_a-\varepsilon_b)\) |
| OS/SS 拆分 | `ch:13:eq:mp2-split` | 92 | PASS：\(E_c^{\mathrm{MP2}}=E_{\mathrm{OS}}+E_{\mathrm{SS}}\) |
| SCS 因子 | `ch:13:eq:scs` | 99 | PASS：\(c_{\mathrm{OS}}=6/5\)，\(c_{\mathrm{SS}}=1/3\) |
| 双杂化成本 | `ch:13:eq:dh-cost` | 111 | PASS：\(c_3N^3+c_4N^4+c_5N^5=\mathcal O(N^5)\) |
| RI/AuxC 分解 | `ch:13:eq:ri` | 121 | PASS：\((pq|rs)\approx\sum_{P,Q}(pq|P)[\mathbf V^{-1}]_{PQ}(Q|rs)\)，\(V_{PQ}=(P|Q)\) |

### 第 14 章（`ch14-xtb.tex`，8 个编号公式）

| 审计项 | 编号公式 | 行号 | 结论 |
|---|---|---|---|
| 紧束缚 Hamiltonian | `ch:14:eq:tb-hamiltonian` | 47 | PASS：\(H_{\mu\nu}=\varepsilon_\mu^{(0)}\delta_{\mu\nu}+(1-\delta_{\mu\nu})t_{\mu\nu}(R_{AB})\) |
| GFN2-xTB 能量分解 | `ch:14:eq:gfn2-energy` | 63 | PASS：\(E_{H0}+E_{\mathrm{SCC}}+E_{\mathrm{rep}}+E_{\mathrm{disp}}+E_{\mathrm{bond}}+E_{\mathrm{ang}}+E_{\mathrm{tor}}\) |
| SCC 电荷 | `ch:14:eq:scc-charge` | 77 | PASS：\(P_{\mu\nu}=\sum_i n_ic_{\mu i}c_{\nu i}\)，\(q_A=Z_A-\sum_{\mu\in A}(PS)_{\mu\mu}\) |
| SCC Hamiltonian | `ch:14:eq:scc-hamiltonian` | 85 | PASS：\(H_{\mu\nu}=H_{\mu\nu}^{(0)}-\frac12S_{\mu\nu}(v_\mu+v_\nu)\)，\(v_A=\partial E_{\mathrm{SCC}}/\partial q_A\) |
| SCC 能量与 \(v_A\) | `ch:14:eq:scc-energy` | 94 | PASS：\(\frac12\sum_{A,B}\gamma_{AB}q_Aq_B+\frac13\sum_A\Gamma_Aq_A^3\)，\(v_A=\sum_B\gamma_{AB}q_B+\Gamma_Aq_A^2\) |
| 参数化目标 | `ch:14:eq:param-objective` | 116 | PASS：\(\sum_kw_k[X_k^{\mathrm{calc}}-X_k^{\mathrm{ref}}]^2/\sum_kw_k\) |
| D4 色散 | `ch:14:eq:dispersion` | 125 | PASS：\(-\frac12\sum_{A\ne B}\sum_{n=6,8}s_nC_n^{AB}/R_{AB}^n f_n(R_{AB})\) |
| 成本标度 | `ch:14:eq:cost-scaling` | 135 | PASS：\(c_2N^2+c_3N^3\) |

### 第 15 章（`ch15-force-field.tex`，10 个编号公式）

| 审计项 | 编号公式 | 行号 | 结论 |
|---|---|---|---|
| 总能分解 | `ch:15:eq:total-energy` | 37 | PASS：键合项 \(+\) 非键合项 \(+\) 极化项 |
| 键伸缩谐振子 | `ch:15:eq:bond-stretch` | 45 | PASS：\(\frac12k_b(r-r_0)^2\) |
| 角弯曲谐振子 | `ch:15:eq:angle-bend` | 54 | PASS：\(\frac12k_\theta(\theta-\theta_0)^2\) |
| 二面角 Fourier | `ch:15:eq:dihedral` | 63 | PASS：\(\sum_n\frac{V_n}{2}[1+\cos(n\varphi-\gamma_n)]\) |
| improper 谐振子 | `ch:15:eq:improper` | 71 | PASS：\(\frac12k_\xi(\xi-\xi_0)^2\) |
| LJ 12-6 | `ch:15:eq:lj` | 84 | PASS：\(4D[(\sigma/R)^{12}-(\sigma/R)^6]\) |
| Coulomb | `ch:15:eq:coulomb` | 92 | PASS：\(\sum_{A<B}q_Aq_B/R_{AB}\)（原子单位） |
| 极化 | `ch:15:eq:polarization` | 105 | PASS：\(-\frac12\sum_A\alpha_A|\mathbf E_A|^2\) |
| Ewald 求和 | `ch:15:eq:ewald` | 125 | PASS：实空间 \(\operatorname{erfc}(\kappa R)/R\)，倒空间 \(2\pi/V\)，自能 \(-\kappa/\sqrt\pi\sum_Aq_A^2\)，因子均正确 |
| GFN-FF 分解 | `ch:15:eq:gfnff-energy` | 140 | PASS：\(E_{\mathrm{bond}}+E_{\mathrm{ang}}+E_{\mathrm{tor}}+E_{\mathrm{rep}}+E_{\mathrm{es}}+E_{\mathrm{disp}}+E_{\mathrm{HB}}+E_{\mathrm{XB}}\) |

### 第 16 章（`ch16-summary.tex`，1 个编号公式）

| 审计项 | 编号公式 | 行号 | 结论 |
|---|---|---|---|
| \(\Delta E\) 定义与换算因子 | `ch:16:eq:delta-e` | 24 | PASS：\(\Delta E=(E_{\mathrm{method}}-E_{\mathrm{CCSD(T)}})\times627.509474\) |
| 表值与符号约定 | 表 `ch:16:tab:ch4-summary` | 27–62 | PASS：20 行能量与 `data/ch4_results.csv` 逐位一致；\(\Delta E\) 与 CSV 换算一致（HF +140.68、MP2 +16.63、CISD +9.99、SVWN5 +201.32、PBE −16.14、B97-3c −36.89、TPSS −64.56、r²SCAN −39.15、r²SCAN-3c −35.31、B3LYP −40.59、ωB97M-V −34.11、B2PLYP −30.55、PWPB95 −32.00、CASSCF +88.75、CASPT2 +11.22、NEVPT2 +20.56、MRCI +6.28） |
| H₂⁻ 表值与 Ch7/Ch8 一致性 | 表 `ch:16:tab:h2m-summary` | 120–140 | PASS：R=0.6/1.5/3.0 的 UHF、MP2、CCSD(T)、CASSCF、NEVPT2、MRCI 能量与 `data/h2m_pes.csv` 一致；\(\langle S^2\rangle\) 与 CSV 一致 |
| 与 Ch3–Ch15 的物理一致性 | 全表 | — | PASS：未发现能量、符号或方法标度上的矛盾 |

---

## 3. 重点“易错点”专项核对（均 PASS）

| 项目 | 位置 | 核对结果 |
|---|---|---|
| Ch4 闭壳层 MP2 因子 | `ch04-mp2.tex:120-128`（`ch:04:eq:mp2-closed`） | PASS：分子 \((ia|jb)[2(ia|jb)-(ib|ja)]\)，分母 \(\varepsilon_i+\varepsilon_j-\varepsilon_a-\varepsilon_b\)，与自旋轨道式 \(1/4\) 相容 |
| Ch6 CCSD 能量因子 | `ch06-cc.tex:113-123`（`ch:06:eq:cc-energy`） | PASS：\(\frac14\sum[(ij|ab)-(ij|ba)](t_{ij}^{ab}+2t_i^at_j^b)\)；按第 4 章反对称化约定 \((ij|ab)-(ij|ba)=(ia|jb)-(ib|ja)\) |
| Ch7 CASSCF 轨道-CI 梯度对易子 | `ch07-casscf.tex:113-120`（`ch:07:eq:orbital-ci-gradient`） | PASS：\(\langle\Psi|[\op H,a_p^\dagger a_q]|\Psi\rangle=0\)，与 \(e^{\kappa}\) 参数化一致 |
| Ch8 NEVPT2 八类求和 | `ch08-mrpt-mrci.tex:76-85`（`ch:08:eq:nevpt2-energy`） | PASS：\(l=1,\ldots,8\)，\(Q_l\) 为外部组态分类，分母 \(E_0^{(0)}-E_K^{(0)}\) |
| Ch10 PBE 相关 \(H\) 与 \(t\) | `ch10-lda-gga.tex:117-128`（`ch:10:eq:pbe-correlation`） | PASS：\(H\)、\(t\)、\(k_s\)、\(\phi\)、\(\gamma\)、\(A\) 均与标准 PBE 一致 |
| Ch11 TPSS \(z\) 与 \(c\) | `ch11-meta-gga.tex:65-75`（`ch:11:eq:tpss-enhancement`） | PASS：\(z=\frac53\tau_W/\tau\)，\(c=1.59096\)，\(x=[(10/81+cz^2)/(1+z^2)^2]p\) |
| Ch12 VV10 核 | `ch12-hybrid.tex:115-126`（`ch:12:eq:vv10-kernel`） | PASS：\(-\frac32/[g g'(g+g')]\)，\(g=\omega_0R^2+\kappa\) |
| Ch13 PWPB95 参数 | `ch13-double-hybrid.tex:64-73`（`ch:13:eq:pwpb95`） | PASS：\(0.50/0.50/0.731/0.269\)，OS-PT2 |
| Ch15 Ewald \(2\pi/V\) 因子 | `ch15-force-field.tex:114-127`（`ch:15:eq:ewald`） | PASS：实空间、倒空间、自能三项因子均正确 |

---

## 4. 非公式级观察（不计入 FAIL 计数）

以下不是方程级物理错误，但建议集成者留意：

1. **Ch16 文字重复**：`sections/ch16-summary.tex:205` 写作“先看 \(\langle S^2\rangle\) 与 \(\langle S^2\rangle\) 的增长”，第二个 \(\langle S^2\rangle\) 疑为重复；不影响公式。
2. **Ch16 “正”包含 0**：`sections/ch16-summary.tex:64` 说“波函数方法的 \(\Delta E\) 则为正”，随后列出 CCSD(T) 的 \(0.00\)。属于措辞不严谨，不是数据错误。
3. **AuxC 行为表述差异**：`sections/ch13-double-hybrid.tex:123` 说缺少 `def2-TZVPP/C` 时 ORCA“会直接报错”；`sections/ch16-summary.tex:207` 说“会退回 AutoAux 或直接失败”。两者不是严格的物理矛盾（取决于 ORCA 版本与关键词），但建议统一措辞。
4. **Ch10 “功能”笔误**：`sections/ch10-lda-gga.tex:153` “三层校正（功能、基组、色散/短程）”中“功能”应为“泛函”。
5. **Ch7/Ch16 的 CASSCF 数据叙事**：CAS(3,2) 占据数 2.0/1.0、CASSCF 能量高于 UHF 是 `nroots 1` 与自旋约束的结果，**不是公式错误**；本报告未将其判为 FAIL，也未建议“修正”。

---

## 5. 最终计数

**163 个编号公式：159 PASS / 4 FAIL。**

4 个 FAIL 分别为：

1. `sections/ch02-foundations.tex:123-125` — `ch:02:eq:bsse`（BSSE 符号）
2. `sections/ch05-ci.tex:157-162` — `ch:05:eq:davidson-correction`（Davidson 校正因子）
3. `sections/ch05-ci.tex:195-199` — `ch:05:eq:pair-error`（CISD 尺寸误差符号）
4. `sections/ch10-lda-gga.tex:159-166` — `ch:10:eq:grid-quadrature`（Becke 网格权重）

> 本次审计为只读：**未修改任何章节文件，未执行 git commit**。所有修正建议仅记录在本报告中，供集成者裁决。

---

## T19 修复后复审

> 复审对象：T19 修改后的 `sections/ch01-overview.tex`、`sections/ch02-foundations.tex`、`sections/ch05-ci.tex`、`sections/ch09-dft.tex`、`sections/ch10-lda-gga.tex`、`sections/ch16-summary.tex`；全书重新编译并逐条复核 4 个 FAIL 公式。
> 复审方式：读取修改后的公式源码 + `latexmk`/`bibtex` 全量重编译（102 页，0 编译错误），确认公式标签、编号与交叉引用未变。

| 原 FAIL | 章节 | label | 修复后位置 | 修复内容 | 结论 |
|---|---|---|---|---|---|
| F1 | Ch2 | `ch:02:eq:bsse` | `sections/ch02-foundations.tex:122-131` | 改为对齐两式：`ΔE_BSSE=(E_A^A+E_B^B)-(E_A^AB+E_B^AB)≥0`，并给出 `ΔE_int^CP=E_AB^AB-E_A^AB-E_B^AB`；正文改为“BSSE 是……正能量”，并说明第一式/第二式含义 | **PASS** |
| F2 | Ch5 | `ch:05:eq:davidson-correction` | `sections/ch05-ci.tex:157-164` | 因子由 `1-Σ_{I≠0}|c_I|²`（实为参考态权重）改为 `1-|c_0|²`（激发组态权重）；正文同步改为“当 `1-|c_0|²` 较小……” | **PASS** |
| F3 | Ch5 | `ch:05:eq:pair-error` | `sections/ch05-ci.tex:195-201` | 右端符号由 `-ΣΔ_pq` 改为 `+ΣΔ_pq`；正文明确 `Δ_pq>0` 是“被截掉的负相关贡献的绝对值”，与“误差随片段数二次增长”一致 | **PASS** |
| F4 | Ch10 | `ch:10:eq:grid-quadrature` | `sections/ch10-lda-gga.tex:159-166` | 求积式补上径向--角向权重：`Σ_A Σ_{i∈A} [P_A(r_i)/Σ_B P_B(r_i)] ω_i^(A) f(r_i)`；正文说明 `ω_i^(A)` 含径向 Jacobian，量纲恢复一致 | **PASS** |

### 更新后统计

| 项目 | 数量 |
|---|---:|
| 编号公式总数 | 163 |
| PASS | **163** |
| FAIL | **0** |

- 4 个 FAIL 全部转为 PASS；公式总数、label 数量与 `\eqref` 覆盖均未变化（163 个公式 label，0 个未被引用）。
- 未新增 label、未删改任何公式编号；`main.log` 无 multiply-defined、无 undefined reference。
