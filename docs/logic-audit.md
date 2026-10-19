# 全书逻辑与结构审计（T17）

审计对象：`sections/ch01-overview.tex` … `sections/ch16-summary.tex`（16 章）、
`CONTRACT.md` §4–§5、`data/ch4_results.csv`、`data/h2m_pes.csv`、`data/h2m_occupations.csv`。

审计方式：逐章阅读正文，逐项对照 CONTRACT §4 模板与 §5 问题链交接表；数值只做结构性核对（T18 负责逐位数值 reconciliation）。本次审计为只读，未修改任何章节文件，未提交。

## 1. 总结

- **章级结果：12 PASS / 4 FAIL**。
- **FAIL 章节：第 1、9、10、16 章**。
- **FAIL 条目：4 条**（第 1 章 2 条数据/协议描述；第 9–10 章 1 条标题漂移；第 16 章 1 条跨章 AuxC 说法冲突）。
- 16 章的 `problemchain` 三问齐全，且与 §5 交接表实质一致；13 个方法章（第 3–15 章）的 `methodcard`、`ch4box`、`pitfall`、`小结` 全部存在。
- 第 7 章与第 16 章的 H₂⁻ 叙事一致：CASSCF(3,2) 在所有 R 上高于 UHF，占据数为 2.0/1.0，未把 1.5/1.5 当作基态证据；多参考证据来自 ⟨S²⟩ 增长与 NEVPT2/MRCI 修正。该结果被明确认定为数据事实，不视为逻辑失败。
- 第 16 章 20 行 CH₄ 表含全部 20 个方法；H₂⁻ 表含 6 个方法 + UHF ⟨S²⟩ 行。

## 2. 章级结构表

| 章 | problemchain | methodcard | ch4box | pitfall | 小结 | 过渡 | 备注 |
|---|---|---|---|---|---|---|---|
| 1 | PASS | N/A | N/A | PASS | PASS | PASS | 17 行表与地图存在且被后文引用；F1、F2 见下 |
| 2 | PASS | N/A | N/A | PASS | PASS | PASS | 基础章；无方法卡/CH₄ 框，符合 §4 |
| 3 | PASS | PASS | PASS | PASS | PASS | PASS | ch4box +140.68 与 CSV 一致 |
| 4 | PASS | PASS | PASS | PASS | PASS | PASS | ch4box +16.63 与 CSV 一致 |
| 5 | PASS | PASS | PASS | PASS | PASS | PASS | ch4box +9.99 与 CSV 一致 |
| 6 | PASS | PASS | PASS | PASS | PASS | PASS | ch4box 0.00 与 CSV 一致；EOM-CC“简述”见备注 N4 |
| 7 | PASS | PASS | PASS | PASS | PASS | PASS | H₂⁻ 数据与 CSV 一致；2.0/1.0 叙事正确 |
| 8 | PASS | PASS | PASS | PASS | PASS | PASS | CASPT2/NEVPT2/MRCI 数值与 CSV 一致；ORCA bug 注记完整 |
| 9 | PASS | PASS | PASS | PASS | PASS | **FAIL** | F3：过渡句与第 10 章实际标题不一致 |
| 10 | PASS | PASS | PASS | PASS | PASS | PASS | F3 根因：章标题偏离 §5 冻结标题 |
| 11 | PASS | PASS | PASS | PASS | PASS | PASS | 3c 复合方法标注明确 |
| 12 | PASS | PASS | PASS | PASS | PASS | PASS | 数值与 CSV 一致 |
| 13 | PASS | PASS | PASS | PASS | PASS | PASS | AuxC 说法与第 16 章冲突，见 F4（本条计入第 16 章） |
| 14 | PASS | PASS | PASS | PASS | PASS | PASS | 明确“与量子化学方法不可直接比较” |
| 15 | PASS | PASS | PASS | PASS | PASS | PASS | 明确“与量子化学方法不可直接比较” |
| 16 | PASS | N/A | N/A | PASS | PASS | N/A | 收束全书，无下一章；F4；20 行表/6 方法表均完整 |

> N/A 说明：CONTRACT §4 只要求“方法章”（第 3–15 章）有 `methodcard` 与 `ch4box`；第 1 章为总览、第 2 章为基础、第 16 章为总结，允许省略。第 16 章没有“过渡”，因为它必须收束全书。

## 3. 专项检查

### 3.1 problemchain 完整性

16/16 章均为三问齐全，且与 CONTRACT.md §5 的三列实质一致：

- 第 1–8 章：`sections/ch01-overview.tex:10-14`、`ch02-foundations.tex:10-14`、`ch03-hf.tex:10-14`、`ch04-mp2.tex:10-14`、`ch05-ci.tex:10-14`、`ch06-cc.tex:10-14`、`ch07-casscf.tex:10-14`、`ch08-mrpt-mrci.tex:10-14`。
- 第 9–16 章：`sections/ch09-dft.tex:10-14`、`ch10-lda-gga.tex:10-14`、`ch11-meta-gga.tex:10-14`、`ch12-hybrid.tex:10-14`、`ch13-double-hybrid.tex:10-14`、`ch14-xtb.tex:10-14`、`ch15-force-field.tex:10-14`、`ch16-summary.tex:10-14`。

无章节发明替代问题。第 10 章在新问题中补充了“无色散、带隙低估”（`ch10-lda-gga.tex:13`），第 14/15 章对成本与参数域作了展开；这些是 §5 单元格的细化，不改变问题实质。

### 3.2 methodcard / ch4box / pitfall / 小结

- `methodcard`：第 3–15 章全部存在，均位于 problemchain 之后、正文之前（如 `ch03-hf.tex:17-26`、`ch15-force-field.tex:17-26`）。第 1、2、16 章无，属 N/A。
- `ch4box`：第 3–15 章全部存在，且数值按 CSV 四舍五入一致：
  - `ch03-hf.tex:231-246` HF −40.214415，+140.68；
  - `ch04-mp2.tex:203-224` MP2 −40.412099，+16.63；
  - `ch05-ci.tex:206-211` CISD −40.422685，+9.99；
  - `ch06-cc.tex:229-235` CCSD(T) −40.438598，0.00；
  - `ch07-casscf.tex:203-210` CASSCF −40.297163，+88.75；
  - `ch08-mrpt-mrci.tex:163-176` CASPT2 −40.420721/+11.22、NEVPT2 −40.405834/+20.56、MRCI −40.428596/+6.28；
  - `ch09-dft.tex:189-203` PBE −40.464324，−16.14；
  - `ch10-lda-gga.tex:178-199` SVWN5 +201.32、PBE −16.14、B97-3c −36.89；
  - `ch11-meta-gga.tex:143-164` TPSS −64.56、r²SCAN −39.15、r²SCAN-3c −35.31；
  - `ch12-hybrid.tex:143-174` B3LYP −40.59、ωB97M-V −34.11；
  - `ch13-double-hybrid.tex:135-166` B2PLYP −30.55、PWPB95 −32.00；
  - `ch14-xtb.tex:150-157` GFN2-xTB −4.175157，且明确不与 QM 比较；
  - `ch15-force-field.tex:171-178` GFN-FF −0.630874，且明确不与 QM 比较。
- `pitfall` 与 `小结`：16/16 章均存在，且顺序正确（正文 → ch4box → pitfall → 小结）。例如 `ch16-summary.tex:201-211`、`ch16-summary.tex:213-214`。

### 3.3 过渡句

第 1–15 章的过渡句均在 `小结` 末尾点名下一章标题。逐字比对结果：

- 通过：Ch1→2、Ch2→3、Ch3→4、Ch4→5、Ch5→6、Ch6→7、Ch7→8、Ch8→9、Ch10→11、Ch11→12、Ch12→13、Ch13→14、Ch14→15、Ch15→16。
- **失败：Ch9→10**。`ch09-dft.tex:216` 写“第 10 章：LDA/GGA：密度泛函前两级够用吗？”，而第 10 章实际标题是“LDA/GGA：密度泛函的**前两级阶梯**够用吗？”（`ch10-lda-gga.tex:6`）。根因是第 10 章标题偏离 §5 冻结标题（`CONTRACT.md:207`），见 F3。
- 第 16 章无下一章；`grep` 未发现“第 17 章”“下一章”“进入第”等字样，收束正确。

### 3.4 第 1 章 17 行表与方法地图

- 17 行表存在：`ch01-overview.tex:98-138`，数据行 17 行（`ch01-overview.tex:118-134`），覆盖 HF、MP2、CISD、CCSD(T)、CASSCF、CASPT2、NEVPT2、MRCI、SVWN5、PBE、TPSS、r²SCAN、B3LYP、ωB97M-V、B2PLYP、PWPB95、GFN2-xTB/GFN-FF。
- 方法地图存在：`ch01-overview.tex:33-83`，左列波函数路线、右列 DFT 天梯、末端 xTB/力场，与后续章节的方法次序一致。
- 表被第 2 章与第 9 章引用（`ch02-foundations.tex:179,203`；`ch09-dft.tex:155`）；地图被第 14 章正文回指（`ch14-xtb.tex:132`）。
- 但第 1 章对 20 个方法的基组计数写错，见 F1。

### 3.5 DFT 天梯与 3c 复合方法

- 第 9 章给出五级天梯：`ch09-dft.tex:143-151`，并在 `ch09-dft.tex:153` 首次声明 B97-3c/r²SCAN-3c 是“经验复合方法……不是新梯级”。
- 第 10 章明确“B97-3c：复合方法，不是新梯级”：`ch10-lda-gga.tex:130-153`，尤其 `ch10-lda-gga.tex:153`。
- 第 11 章明确“r²SCAN-3c……不是新 rung（非新梯级）”：`ch11-meta-gga.tex:101-133`，尤其 `ch11-meta-gga.tex:133`。
- 第 12 章解释精确交换修补 SIE，第 13 章解释 MP2 项补动态相关；Ch9→10→11→12→13 的“下一级增加什么”均在章末或下一章开头交代（`ch10-lda-gga.tex:175`、`ch11-meta-gga.tex:140`、`ch12-hybrid.tex:188`、`ch13-double-hybrid.tex:181`）。
- 第 16 章在表格备注与表注中称 3c 为“复合方法”（`ch16-summary.tex:42,45,61`），但没有再次使用“非新梯级”四字；没有文本把它们当作天梯新级，故不判 FAIL，建议补一句以逐字对齐 §4/§5 口径（N1）。

### 3.6 xTB 与力场：牺牲什么、能量为何不可比

- 第 14 章：只保留价电子与最小价基组、积分参数化（`ch14-xtb.tex:18-25,32-53`）；明确不能做热化学、电子转移、激发态、断键（`ch14-xtb.tex:147`）；明确 GFN2-xTB 总能“与量子化学方法不可直接比较”（`ch14-xtb.tex:156`）。
- 第 15 章：电子自由度被完全积分掉（`ch15-force-field.tex:18-25,155-168`）；明确不能断键、电子转移、激发态、质子转移、自旋态变化（`ch15-force-field.tex:160-166`）；明确 GFN-FF 总能“与量子化学方法不可直接比较”（`ch15-force-field.tex:177`）。
- 两章均未把 xTB/FF 的绝对能量放进 QM 比较，符合要求。

### 3.7 第 16 章决策树

- 组织方式是“问题类型优先”：第一问是否需要电子结构，第二问是否有强静态相关/近简并，第三问单参考目标（`ch16-summary.tex:150-196`）。不是按方法清单线性排列；正文也明确说“这棵树刻意不按‘方法清单’组织”（`ch16-summary.tex:196`）。
- 分支与各章一致：力场（第 15 章）、CASSCF→NEVPT2/MRCI（第 7–8 章）、CCSD(T)（第 6 章）、双杂化（第 13 章）、杂化/meta-GGA（第 11–12 章）、ωB97M-V（第 12 章）、xTB/PBE（第 10、14 章）。
- 两处可改进但不构成逻辑失败：树中叶写“ωB97M-V (+D4)”（`ch16-summary.tex:153,176`），而第 12 章已说明 ωB97M-V 自带 VV10 非局域相关（`ch12-hybrid.tex:106-126`），D4 可能重复；双杂化叶未写“+D3”，而第 13 章说 B2PLYP/PWPB95 本身不含长程色散（`ch13-double-hybrid.tex:175`）。见 N2、N3。
- 树底部“成本 ↑（向右）”箭头（`ch16-summary.tex:189-190`）与五个叶子的纵向排布不完全对应；这是绘图可读性问题，不影响分支逻辑（N5）。

### 3.8 “仅为介绍”式段落

逐章检查了方法节的动机句。第 3–15 章的方法节均回答了“上一级缺什么、本方法加什么”；未发现只作介绍、不解释必要性的整段文字。

唯一需要标注的是第 6 章的 EOM-CC/Λ 小节：标题带“（简述）”（`ch06-cc.tex:167`），并写“本书不展开其推导”（`ch06-cc.tex:188`）。但该小节给出了 EOM-CC 与 Λ 方程的两个实质方程，并说明它补的是“基态 CC 不提供的激发态”，不是空泛介绍，因此不计入 FAIL；若项目对“简述”字样零容忍，可去掉括号或移到附录（N4）。

### 3.9 H₂⁻ 叙事一致性

- 第 7 章：CASSCF(3,2) 在每个 R 上高于 UHF，差值 0.0012–0.0131 Eh（`ch07-casscf.tex:164`）；占据数在所有 R 上为 2.0000/1.0000（`ch07-casscf.tex:177-189`）；明确 1.5/1.5 只可能来自 `nroots 2` 态平均，本书不使用（`ch07-casscf.tex:136,189,217`）；多参考证据来自 ⟨S²⟩ 从 0.754473 增至 0.821141，以及 NEVPT2/MRCI 修正（`ch07-casscf.tex:191`）。
- 第 16 章：重复同一组事实（`ch16-summary.tex:142-146`），并明确“用 CASSCF 更低来论证多参考必要性是错的”（`ch16-summary.tex:142`）。
- 未发现其他章节把 CASSCF 写成低于 UHF，或把 1.5/1.5 当作基态占据。第 8 章只比较 CASSCF 之上的 NEVPT2/MRCI，未与 UHF 混比（`ch08-mrpt-mrci.tex:142`）。**该项 PASS。**

### 3.10 跨章一致性

- CCSD(T)/def2-TZVPP 参考值 −40.438598 Eh：第 1、3、5、6、8、9、10、11、12、13、14、15、16 章一致。
- B97-3c 用 def2-mTZVP、r²SCAN-3c 用 def2-mTZVPP：第 1、10、11、16 章一致。
- AuxC 写作 `def2-TZVPP/C`：第 1、2、13、16 章一致（但“缺失时行为”的表述冲突，见 F4）。
- 泛函名（SVWN5、PBE、TPSS、r²SCAN、B3LYP、ωB97M-V、B2PLYP、PWPB95）前后一致。
- H₂⁻ R 网格：CSV 为 0.6、0.8、1.0、1.2、1.5、2.0、2.5、3.0 Å；第 1 章的文字描述有误，见 F2。
- CH₄ 20 个方法：第 16 章表 20 行完整；第 1 章的基组计数有误，见 F1。

### 3.11 第 16 章两张表

- CH₄ 表：`ch16-summary.tex:27-62`，数据行 20 行（`ch16-summary.tex:36-55`），按 CSV 行序排列；GFN2-xTB/GFN-FF 的 ΔE 为“—”，表注说明不可比（`ch16-summary.tex:61`）。
- H₂⁻ 表：`ch16-summary.tex:120-140`，含 UHF、MP2、CCSD(T)、CASSCF、NEVPT2、MRCI 共 6 个方法，外加 UHF ⟨S²⟩ 行（`ch16-summary.tex:136`）；数值与 `data/h2m_pes.csv` 一致。
- **两张表均完整，PASS。**

## 4. 逐章发现（含精确 file:line）

### 第 1 章 `sections/ch01-overview.tex`

- `10-14`：problemchain 三问齐全，与 §5 一致。
- `33-83`：方法地图；`98-138`：17 行表；`118-134`：17 个数据行。
- `140-147`：两个算例协议；`163-169`：pitfall；`172-173`：小结+过渡（点名第 2 章）。
- **F1** `145`：基组计数错误。原文“20 个方法中有 18 个在 def2-TZVPP 下计算，B97-3c 与 r²SCAN-3c 使用各自内置基组”。按 `data/ch4_results.csv` 的 `basis` 列：16 个 def2-TZVPP、2 个内置基组（B97-3c 的 def2-mTZVP、r²SCAN-3c 的 def2-mTZVPP）、2 个无基组（GFN2-xTB、GFN-FF）。原文的 18+2 没有给 xTB/FF 留位置；第 16 章 `ch16-summary.tex:69` 的“18 个量子化学方法”是另一层含义（20−2 个非 QM），不能与“18 个在 def2-TZVPP 下”混用。
- **F2** `147`：H₂⁻ R 网格描述错误。原文“$R=0.6$–$3.0$ Å（$0.6$–$1.5$ 步长 0.2，其后步长 0.5）”。`data/h2m_pes.csv` 的实际 8 个点是 0.6、0.8、1.0、1.2、1.5、2.0、2.5、3.0；按“0.6–1.5 步长 0.2”会得到 1.4 而非 1.5，按“其后步长 0.5”会得到 1.9/2.4/2.9 而非 2.0/2.5/3.0。

### 第 2 章 `sections/ch02-foundations.tex`

- `10-14`：problemchain；`102-118`：def2/辅助基组表；`200-217`：三把尺子表。
- `248-254`：pitfall；`257-258`：小结+过渡（点名第 3 章）。
- 无 methodcard/ch4box，符合 CONTRACT §4 对基础章的豁免。
- 未发现逻辑/结构问题。

### 第 3 章 `sections/ch03-hf.tex`

- `17-26`：methodcard；`231-246`：ch4box；`249-255`：pitfall；`258-259`：小结+过渡（点名第 4 章）。
- ch4box 的 HF 能量、CCSD(T) 参考与 ΔE 均与 CSV 一致。
- 未发现问题。

### 第 4 章 `sections/ch04-mp2.tex`

- `17-26`：methodcard；`203-224`：ch4box；`227-233`：pitfall；`236-237`：小结+过渡（点名第 5 章）。
- ch4box 与 CSV 一致；MP2 相关能 −0.197684 Eh 与“约 88.2%”换算正确。
- 未发现问题。

### 第 5 章 `sections/ch05-ci.tex`

- `17-26`：methodcard；`206-211`：ch4box；`214-221`：pitfall；`224-225`：小结+过渡（点名第 6 章）。
- CISD +9.99 与 CSV 一致；尺寸不一致论证完整。
- 未发现问题。

### 第 6 章 `sections/ch06-cc.tex`

- `17-26`：methodcard；`229-235`：ch4box；`238-245`：pitfall；`248-249`：小结+过渡（点名第 7 章）。
- CCSD(T) 参考值与 CSV 一致。
- 备注 N4：`167` 的“（简述）”与 `188` 的“本书不展开其推导”属于可选扩展小节的自我限定；该小节有实质方程并说明 EOM-CC 补的是激发态，未判为 FAIL，但若严格执行“无简述”口径，建议去掉该措辞或移入附录。

### 第 7 章 `sections/ch07-casscf.tex`

- `17-27`：methodcard；`203-210`：ch4box；`213-220`：pitfall；`223-224`：小结+过渡（点名第 8 章）。
- `164,177-191`：H₂⁻ 数据解读；CASSCF 高于 UHF、2.0/1.0 占据、1.5/1.5 仅属态平均等表述均正确。
- 未发现逻辑失败；该章的“诚实结果”是数据事实，不计为失败。

### 第 8 章 `sections/ch08-mrpt-mrci.tex`

- `17-27`：methodcard；`163-176`：ch4box；`179-186`：pitfall；`189-190`：小结+过渡（点名第 9 章）。
- `142-153`：H₂⁻ 的 NEVPT2/MRCI 曲线；`153` 的 ORCA CASPT2 bug 注记与第 16 章一致。
- CH₄ 的 CASPT2/NEVPT2/MRCI 数值与 CSV 一致。
- 未发现问题。

### 第 9 章 `sections/ch09-dft.tex`

- `17-26`：methodcard；`189-203`：ch4box；`206-212`：pitfall；`215-216`：小结+过渡。
- `140-155`：雅各布天梯与 3c 复合方法说明；`153` 明确“复合方法，不是新梯级”。
- **F3** `216`：过渡句写“第 10 章：LDA/GGA：密度泛函前两级够用吗？”，与 `ch10-lda-gga.tex:6` 的实际标题“LDA/GGA：密度泛函的前两级阶梯够用吗？”不一致。根因是第 10 章标题漂移，见 F3 的第 10 章条目。

### 第 10 章 `sections/ch10-lda-gga.tex`

- `17-26`：methodcard；`178-199`：ch4box；`202-208`：pitfall；`211-212`：小结+过渡（点名第 11 章）。
- `130-153`：B97-3c 复合方法专节，`153` 明确“复合方法，非新 rung”。
- **F3 根因** `6`（以及文件头注释 `2`）：标题为“LDA/GGA：密度泛函的前两级阶梯够用吗？”，而 CONTRACT.md §5 冻结标题为“LDA/GGA：密度泛函前两级够用吗？”（`CONTRACT.md:207`）。这一字面漂移导致 `ch09-dft.tex:216` 的过渡句与第 10 章实际标题对不上。

### 第 11 章 `sections/ch11-meta-gga.tex`

- `17-26`：methodcard；`143-164`：ch4box；`167-173`：pitfall；`176-177`：小结+过渡（点名第 12 章）。
- `101-133`：r²SCAN-3c 复合方法专节，`133` 明确“不是新 rung（非新梯级）”。
- 未发现问题。

### 第 12 章 `sections/ch12-hybrid.tex`

- `17-26`：methodcard；`143-174`：ch4box；`177-184`：pitfall；`187-188`：小结+过渡（点名第 13 章）。
- 数值与 CSV 一致；VV10 与范围分离解释完整。
- 未发现独立问题；`106-126` 的 VV10 说明与第 16 章树中的“+D4”存在可澄清之处，见 N2（不计 FAIL）。

### 第 13 章 `sections/ch13-double-hybrid.tex`

- `17-26`：methodcard；`135-166`：ch4box；`169-177`：pitfall；`180-181`：小结+过渡（点名第 14 章）。
- `123` 与 `172`：AuxC 缺失时“ORCA 会直接报错”“不会自动退回四指数 MP2”。
- **F4 的对立方**：`ch16-summary.tex:207` 写“省略 AuxC 会退回 AutoAux 或直接失败”，与本章 `123,172` 的绝对说法冲突。本章自身结构无问题；跨章表述需统一，见 F4。

### 第 14 章 `sections/ch14-xtb.tex`

- `17-26`：methodcard；`150-157`：ch4box；`160-167`：pitfall；`170-171`：小结+过渡（点名第 15 章）。
- `147`：明确 xTB 不适合热化学、电子转移、激发态、断键；`156`：明确总能量与 QM 不可直接比较。
- 未发现问题。

### 第 15 章 `sections/ch15-force-field.tex`

- `17-26`：methodcard；`171-178`：ch4box；`181-188`：pitfall；`191-192`：小结+过渡（点名第 16 章）。
- `160-166`：四条硬边界（断键/电子转移/激发态/质子转移与自旋态）；`177`：明确总能量与 QM 不可直接比较。
- 未发现问题。

### 第 16 章 `sections/ch16-summary.tex`

- `10-14`：problemchain；`27-62`：20 行 CH₄ 表；`120-140`：6 方法 + UHF ⟨S²⟩ 的 H₂⁻ 表；`150-196`：按问题类型组织的决策树；`201-211`：pitfall；`213-214`：小结（无下一章）。
- `142-146`：H₂⁻ 叙事与第 7 章一致（CASSCF 高于 UHF、2.0/1.0、1.5/1.5 仅属态平均、多参考证据来自 ⟨S²⟩ 与 NEVPT2/MRCI）。
- **F4** `207`：AuxC 缺失时“会退回 AutoAux 或直接失败”，与 `ch13-double-hybrid.tex:172` 的“直接报错，不会自动退回四指数 MP2”冲突。
- 备注 N1：`42,45,61` 将 B97-3c/r²SCAN-3c 标为“复合方法”，但未再次写“非新梯级”；无文本把它们当天梯新级，建议补一句。
- 备注 N2/N3/N5：决策树叶的 `+D4`/缺 `+D3` 与成本箭头排布，见 §3.7。

## 5. FAIL 清单与修改建议

### F1 — 第 1 章：20 个方法的基组计数错误

- 位置：`sections/ch01-overview.tex:145`
- 证据：`data/ch4_results.csv` 的 `basis` 列为 16 个 def2-TZVPP、2 个内置基组（B97-3c/r²SCAN-3c）、2 个无基组（GFN2-xTB/GFN-FF）；`sections/ch16-summary.tex:69` 的 18 是“20 − 2 个非 QM 方法”，不是“18 个在 def2-TZVPP 下”。
- 建议：改为“20 个方法中，16 个用 def2-TZVPP，B97-3c 与 r²SCAN-3c 使用各自内置基组（def2-mTZVP / def2-mTZVPP），GFN2-xTB 与 GFN-FF 不含外部基组”。

### F2 — 第 1 章：H₂⁻ R 网格描述与 CSV 不符

- 位置：`sections/ch01-overview.tex:147`
- 证据：`data/h2m_pes.csv` 的 R 列为 0.6、0.8、1.0、1.2、1.5、2.0、2.5、3.0；原文“0.6–1.5 步长 0.2，其后步长 0.5”无法生成这 8 个点。
- 建议：直接列出 8 个点，或改为“0.6–1.2 步长 0.2，随后 1.5，之后 2.0–3.0 步长 0.5”。

### F3 — 第 10 章标题漂移，导致第 9 章过渡句失配

- 位置：`sections/ch10-lda-gga.tex:6`（文件头注释 `2` 同）；`sections/ch09-dft.tex:216`；冻结源 `CONTRACT.md:207`。
- 证据：CONTRACT §5 第 10 行标题为“LDA/GGA：密度泛函前两级够用吗？”；实际章标题多出“的”和“阶梯”；第 9 章过渡句按 §5 写，因此与第 10 章实际标题不一致。
- 建议：把 `ch10-lda-gga.tex` 的 `\section`（及文件头注释）改回 §5 冻结标题“LDA/GGA：密度泛函前两级够用吗？”。这样第 9 章过渡句自动匹配，且不必改 CONTRACT。若确实想保留“前两级阶梯”措辞，则必须同步修改 CONTRACT §5 与第 9 章过渡句，但 CONTRACT 是冻结源，不推荐。

### F4 — 第 16 章与第 13 章对“缺少 AuxC 时 ORCA 行为”的说法冲突

- 位置：`sections/ch16-summary.tex:207` vs `sections/ch13-double-hybrid.tex:123,172`
- 证据：第 13 章说“缺少 def2-TZVPP/C 时……ORCA 会直接报错”“不会自动退回四指数 MP2”；第 16 章说“省略 AuxC 会退回 AutoAux 或直接失败”。两者对是否存在 AutoAux 回退给出相反说法，属于跨章 claim 不一致。
- 建议：用 ORCA 6.1.1 实测或查官方文档确认后统一。若存在 AutoAux 回退，第 13 章改为“可能自动生成 AutoAux，或直接报错；结果依赖版本，必须显式给定”；若不存在回退，第 16 章改为“直接报错，不会自动退回四指数 MP2”。无论哪种，都应在两处使用同一句。

## 6. 非 FAIL 备注（建议但不计入章级失败）

- **N1（第 16 章 3c 措辞）**：`ch16-summary.tex:42,45,61` 已标“复合方法”，但未写“非新梯级”。建议在表注补“，不是雅各布天梯的新梯级”，与 `ch10-lda-gga.tex:153`、`ch11-meta-gga.tex:133` 完全对齐。
- **N2（第 16 章 ωB97M-V +D4）**：`ch16-summary.tex:153,176` 写“ωB97M-V (+D4)”，而 `ch12-hybrid.tex:106-126` 说明 ωB97M-V 已含 VV10 非局域相关。建议改为“ωB97M-V（已含 VV10）”或明确“D4 仅在特定版本/额外需求下加”，避免重复计色散。
- **N3（第 16 章双杂化 +D3）**：`ch16-summary.tex:174` 的双杂化叶未提色散校正，而 `ch13-double-hybrid.tex:175` 明确 B2PLYP/PWPB95 本身不含长程色散。建议在“非共价”后补“+D3(BJ)”。
- **N4（第 6 章 EOM-CC“简述”）**：`ch06-cc.tex:167,188`。该小节有实质方程，未判 FAIL；若项目严格禁止“简述/不展开”措辞，可去掉“（简述）”与“本书不展开其推导”，或移到附录。
- **N5（第 16 章决策树排版）**：`ch16-summary.tex:189-190` 的“成本 ↑（向右）”与 `ch16-summary.tex:173-177` 五个叶子的纵向排布不完全对应；建议把叶子按成本从左到右展开，或把箭头改为“成本 ↑（向下）”。不影响分支逻辑。
- **N6（第 10 章 problemchain 的细化）**：`ch10-lda-gga.tex:13` 在 §5 的“半局域、自相互作用误差”之外补了“无色散、带隙低估”。这是本章失效模式的合理细化，不构成问题漂移；若要求逐字，可只保留 §5 两项。

## 7. 结论

- **12 PASS / 4 FAIL**（第 1、9、10、16 章）。
- 结构骨架（problemchain、methodcard、ch4box、pitfall、小结、过渡）整体完整；主要问题集中在三处跨章一致性（第 1 章的方法/基组计数与 R 网格、第 10 章标题漂移、第 16 章 AuxC 说法）和一处可选措辞（第 6 章 EOM-CC“简述”）。
- 第 7 章与第 16 章的 H₂⁻ 叙事经逐行核对一致，CASSCF 高于 UHF、2.0/1.0 占据与 1.5/1.5 的排除均正确，不是逻辑失败。
- 本次审计未修改 `sections/`、`appendix/`、`preamble.tex`、`main.tex`、`CONTRACT.md`、`refs.bib`、`data/`、`scripts/`、`runs/`，未提交。

---

## T19 修复后复审

> 复审对象：T19 修改后的第 1、9、10、16 章及相关跨章表述；全量重编译后重新核对标题、过渡句、计数与 AuxC 说法。

| 原 FAIL | 位置（修复后） | 修复内容 | 结论 |
|---|---|---|---|
| F1 第 1 章基组计数 | `sections/ch01-overview.tex:145` | 改为“20 个方法中，16 个用 def2-TZVPP；B97-3c 与 r$^2$SCAN-3c 使用各自内置基组（def2-mTZVP / def2-mTZVPP）；GFN2-xTB 与 GFN-FF 不含外部基组”，与 CSV `basis` 列 16+2+2 完全一致 | **PASS** |
| F2 第 1 章 R 网格 | `sections/ch01-overview.tex:147` | 改为“$0.6$–$1.2$ 步长 0.2，随后 $1.5$，之后 $2.0$–$3.0$ 步长 0.5”，恰好生成 CSV 的 8 个点 0.6/0.8/1.0/1.2/1.5/2.0/2.5/3.0 | **PASS** |
| F3 第 9→10 章标题漂移 | `sections/ch10-lda-gga.tex:2,6` | 章标题与文件头注释改回冻结标题“LDA/GGA：密度泛函前两级够用吗？”；`ch09-dft.tex:216` 过渡句未改，现与第 10 章标题逐字一致，也与 `CONTRACT.md:207` 一致 | **PASS** |
| F4 第 16 章 AuxC 说法 | `sections/ch16-summary.tex:207` | 改为“省略 AuxC 会直接报错（不会自动退回四指数 MP2），结果不可复现”，与 `ch13-double-hybrid.tex:123,172` 及 ORCA 6.1.1 实测一致 | **PASS** |

### 同步修复的低风险备注

| 备注 | 位置（修复后） | 修复内容 | 结论 |
|---|---|---|---|
| N1 3c 非新梯级 | `sections/ch16-summary.tex:61` | 表注补“（不是雅各布天梯的新梯级）” | **PASS** |
| N2 ωB97M-V +D4 | `sections/ch16-summary.tex:153,176` | 正文与决策树叶均改为“$\omega$B97M-V（已含 VV10）” | **PASS** |
| N3 双杂化 +D3 | `sections/ch16-summary.tex:174` | 叶子改为“双杂化（非共价 +D3(BJ)）” | **PASS** |
| N5 成本箭头 | `sections/ch16-summary.tex:189-192` | 水平箭头改为叶子右侧的竖直箭头，图注改为“成本向上递增” | **PASS** |
| 表注/计数一致性 | `sections/ch01-overview.tex:106` | 表 caption 改为“17 行（18 个方法；GFN2-xTB/GFN-FF 合并一行）” | **PASS** |

### 更新后统计

| 项目 | 数量 |
|---|---:|
| 章级 PASS | **16** |
| 章级 FAIL | **0** |
| FAIL 条目 | **0**（原 4 条全部关闭） |

- 16/16 章的 `problemchain`、`methodcard`/`ch4box`（第 3–15 章）、`pitfall`、`小结`、过渡句均通过。
- Ch9→10 过渡句、第 10 章标题、`CONTRACT.md:207` 三处现已逐字一致。
