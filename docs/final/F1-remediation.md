# F1 阻断项 B1 修复记录：将 pgfplots 移出 `~/texmf` 并接入 `TEXINPUTS`

- 修复对象：`docs/final/F1-plan-compliance.md` 中的 B1
- 违反条款（Must NOT）："不修改 ~/texmf 中除 tcolorbox 外的任何内容"
- 违规事实：`~/texmf/tex/latex/pgfplots/` 与 `~/texmf/tex/generic/pgfplots/` 创建于 2026-10-19 22:33:10
- 修复原则：不删除 pgfplots，只将其移出受保护的 `~/texmf`，通过构建脚本的 `TEXINPUTS` 继续使用

## 1. 目录迁移

### 迁移前

| 路径 | mtime |
|---|---|
| `~/texmf/tex/latex/pgfplots` | 2026-10-19 22:33:10.460596158 +0800 |
| `~/texmf/tex/generic/pgfplots` | 2026-10-19 22:33:10.459596160 +0800 |

执行命令：

```bash
mkdir -p ~/texmf-disabled/pgfplots-4.42/tex/latex ~/texmf-disabled/pgfplots-4.42/tex/generic
mv ~/texmf/tex/latex/pgfplots ~/texmf-disabled/pgfplots-4.42/tex/latex/
mv ~/texmf/tex/generic/pgfplots ~/texmf-disabled/pgfplots-4.42/tex/generic/
rmdir ~/texmf/tex/generic   # 迁移后为空
```

`~/texmf` 中其余内容（chemfig / everysel / makecell / multirow，均为 7 月创建）与 `tex/latex/tcolorbox` 未改动；`~/texmf-disabled/tcolorbox-2026` 未改动。

### 迁移后

| 路径 | mtime |
|---|---|
| `~/texmf-disabled/pgfplots-4.42/tex/latex/pgfplots` | 2026-10-19 22:33:10.460596158 +0800 |
| `~/texmf-disabled/pgfplots-4.42/tex/generic/pgfplots` | 2026-10-19 22:33:10.459596160 +0800 |
| `~/texmf/tex/latex/tcolorbox/tcolorbox.sty`（未动，4.42） | 2020-10-10 04:21:47 +0800 |
| `~/texmf-disabled/tcolorbox-2026`（未动） | 2026-07-03 00:10:07 +0800 |

## 2. TEXINPUTS 接入

### `latexmkrc`（文件顶部）

```perl
$ENV{'TEXINPUTS'} = "$ENV{HOME}/texmf-disabled/pgfplots-4.42//:" . ($ENV{'TEXINPUTS'} // '');
$pdf_mode = 5;
$xelatex = 'xelatex -interaction=nonstopmode -halt-on-error %O %S';
$bibtex_use = 2;
```

### `build-chapter.sh`（`cd` / `PATH` 之后，任何 xelatex/latexmk 调用之前）

```bash
cd "$(dirname "$0")"
export PATH="$HOME/.local/bin:$HOME/bin:$PATH"
export TEXINPUTS="$HOME/texmf-disabled/pgfplots-4.42//:${TEXINPUTS:-}"
```

路径语法：`//` 表示递归搜索，结尾 `:` 保留 kpathsea 默认搜索路径。

## 3. kpsewhich 验证

```bash
test ! -e ~/texmf/tex/latex/pgfplots/pgfplots.sty     # OK
test ! -e ~/texmf/tex/generic/pgfplots                 # OK
kpsewhich pgfplots.sty                                 # 无输出（默认路径中不再存在）
TEXINPUTS="$HOME/texmf-disabled/pgfplots-4.42//:" kpsewhich pgfplots.sty
# /home/xieningke/texmf-disabled/pgfplots-4.42/tex/latex/pgfplots/pgfplots.sty
kpsewhich tcolorbox.sty
# /home/xieningke/texmf/tex/latex/tcolorbox/tcolorbox.sty
```

构建日志中的实际加载路径也确认来自新位置：

```
(/home/xieningke/texmf-disabled/pgfplots-4.42/tex/latex/pgfplots/pgfplots.sty
```

## 4. 附录 A 措辞对齐

`appendix/app-orca.tex` §A.4（第 87 行）：

- 修改前：`只写 \texttt{def2-TZVPP} 会退回 AutoAux 或直接报错，能量不可复现。`
- 修改后：`只写 \texttt{def2-TZVPP} 会直接报错（不会自动退回四指数 MP2），能量不可复现。`

与 `sections/ch13-double-hybrid.tex` 与 `sections/ch16-summary.tex` 的表述一致。

## 5. 重建命令与结果

```bash
export PATH="$HOME/.local/bin:$HOME/bin:$PATH"
latexmk -C                                                                    # exit 0
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex             # exit 0
bibtex main                                                                   # exit 0
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex             # exit 0
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex             # exit 0
```

## 6. 构建指标

| 指标 | 结果 |
|---|---|
| 页数 | 102（要求 95–105） |
| 纸张 | A4，595.28 × 841.89 pt |
| `Citation.*undefined` | 0 |
| `Reference.*undefined` | 0 |
| `multiply defined` | 0 |
| `Missing` | 0 |
| `??`（main.log） | 0 |
| `??`（`pdftotext main.pdf - \| grep -c`） | 0 |
| Overfull hbox | 5 处，最大 3.56561pt（全部 < 10pt） |

Overfull 明细：3.56561pt、2.82448pt、1.23936pt、1.10976pt、0.38074pt。

## 7. 验证命令汇总

```bash
# 目录与解析
test ! -e ~/texmf/tex/latex/pgfplots/pgfplots.sty
test ! -e ~/texmf/tex/generic/pgfplots
kpsewhich pgfplots.sty
TEXINPUTS="$HOME/texmf-disabled/pgfplots-4.42//:" kpsewhich pgfplots.sty
kpsewhich tcolorbox.sty

# 构建与指标
pdfinfo main.pdf | grep -E '^Pages|^Page size'
grep -cE 'Citation.*undefined|Reference.*undefined|multiply defined|Missing' main.log
pdftotext main.pdf - | grep -c '??'
grep -oE 'Overfull \\hbox \([0-9.]+pt too wide\)' main.log | sort -u
```

结论：B1 已修复，`~/texmf` 不再包含 pgfplots；书稿在新 TEXINPUTS 下完整构建并通过全部指标。
