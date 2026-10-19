# F2 — LaTeX Code-Quality Review (final gate)

- **Repository**: `/home/xieningke/课程/计算化学/泛函详解`
- **HEAD**: `b720d76` (`fix: resolve all audit findings`)
- **Scope**: `preamble.tex`, `main.tex`, `sections/ch01–ch16`, `appendix/app-*`, `CONTRACT.md` §3–§4/§12–§14, `refs.bib`, existing build artifacts.
- **Mode**: READ-ONLY. No source file edited, no rebuild run (`latexmk` not invoked), no commit.
- **Method**: static inspection (`grep`, `python3` source parsing) plus the existing `main.log` / `main.pdf` and `docs/build-check.md` / `docs/audit-fixes.md`. The `\braket`/`\bracket` splitter was additionally exercised in an isolated `/tmp` test document (not part of the book build).

## 1. Summary metrics

| Metric | Value |
|---|---|
| Project macros in `preamble.tex` | **10** (`\dd \ee \ii \HF \xc \braket \bracket \ket \bra \op`), each defined exactly once |
| `\newcommand` / `\renewcommand` / `\DeclareMathOperator` / `\def` in chapters + appendix | **0** |
| `\usepackage` in chapters + appendix | **0** |
| Raw `\hat` in chapters + appendix | **0** (`\op{...}` used 242 times) |
| Raw `\mathrm{d}` / `\mathrm{e}` / `\mathrm{i}` | **0 / 0 / 0** (`\dd` used 32×, `\ee` 24×, `\ii` 1×) |
| `\definecolor` in `preamble.tex` | **6** (Okabe–Ito) |
| `\definecolor` / `\color{...}` / hex / rgb literal in chapters + appendix | **0 / 0 / 0** |
| tcolorbox environments | **4** definitions, used **58** times (problemchain 16, methodcard 13, ch4box 13, pitfall 16) |
| Tables | **17** (15 `tabular` + 2 `longtable`); all `booktabs`; 0 vertical rules; 0 `\hline`/`\cline` |
| Figures | **6** (5 `figure` floats + 1 `\captionof{figure}` inside a TikZ block) |
| Floats missing caption or label | **0** |
| Unreferenced `eq`/`fig`/`tab` labels | **0** |
| Labels / duplicate labels | **304 / 0** |
| `\ref`/`\eqref` calls / undefined | **493 / 0** |
| Bib entries / distinct cited / cited-but-missing | **63 / 60 / 0** |
| Pages | **102** (gate 95–105) |
| Overfull boxes | **5**, maximum **3.56561 pt** (gate: ≤5, each <10 pt) |
| Missing characters | **0** |
| Undefined citations / references / `??` in PDF | **0 / 0 / 0** |
| TODO / FIXME / HACK / XXX | **0** |

## 2. PASS/FAIL table

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | No duplicate macro definitions; 10 project macros defined once in `preamble.tex` | **PASS** | `preamble.tex:53–60` (8 `\newcommand`) + `:66–76` (`\def\braket`, `\def\bracket`); name scan shows multiplicity 1 for every macro |
| 2 | No `\newcommand`/`\renewcommand`/`\DeclareMathOperator` in chapters or appendix | **PASS** | `grep` over `sections/*.tex appendix/*.tex` → no matches (exit 1); also no `\def`/`\let`/`\newenvironment` |
| 3 | All 10 project macros defined and actually used | **PASS** | `\dd 32, \ee 24, \ii 1, \HF 32, \xc 55, \braket 7, \bracket 32, \ket 39, \bra 3, \op 242` |
| 4 | `\braket` / `\bracket` split on `|`, 1-bar and 2-bar cases use `\mid`, never raw `|` | **PASS** | `preamble.tex:66–76`; isolated test renders `⟨a \| b⟩`, `⟨a \| O \| b⟩`, `⟨ij \|\| ab⟩` (double bar = two `\mid`); 0 `\|` inside any call, all calls use bare `|` |
| 5 | No raw `\hat`; operators use `\op{}` | **PASS** | `grep '\\hat'` → 0 occurrences; `\op{...}` 242 uses |
| 6 | `\dd` used for differentials | **PASS** | 0 raw `\mathrm{d}`; differentials appear as `\,\dd\mathbf{r}`, `\,\dd\mathbf{x}`, `\,\dd\lambda`, etc. |
| 7 | No `\usepackage` in chapters or appendix | **PASS** | 0 matches |
| 8 | Colors centralized in `preamble.tex`; chapters use only named colors | **PASS** | 6 `\definecolor` in `preamble.tex:38–43`; chapter color usage is TikZ `color=`/`draw=`/`fill=` with `oiBlue`, `oiGreen`, `oiVermillion`, `black`, `white` only; no hex/rgb/`\color{}` |
| 9 | Tables use `booktabs`, no vertical rules | **PASS** | 17/17 tables use `\toprule`/`\midrule`/`\bottomrule`; every column spec is `@{}...@{}` with no `|`; 0 `\hline`/`\cline` |
| 10 | Figures/tables have captions and labels | **PASS** | Every `figure`/`table` float has both `\caption` and `\label`; in-box tables use `\captionof{table}` (`ch10:192`, `ch11:159`), TikZ tree uses `\captionof{figure}` (`ch16:192`) |
| 11 | Every float is referenced in text | **PASS** | 0 unreferenced `fig`/`tab` labels out of 23; 0 unreferenced `eq` labels out of 163 |
| 12 | Chapter template order: problemchain → methodcard (Ch3–15) → body → ch4box (Ch3–15) → pitfall → 小结 + transition | **PASS** | Parsed per file: all 16 chapters follow the order; Ch3–15 all contain methodcard + ch4box; Ch1/2/16 omit them as permitted |
| 13 | No TODO/FIXME/HACK/XXX/placeholders | **PASS** | 0 matches; `sections/ch06-cc.tex:40` contains the ordinary word “待定振幅”, not a placeholder marker |
| 14 | Ch1/Ch2/Ch16 omissions are justified by CONTRACT §4 | **PASS** | CONTRACT §4: methodcard “仅‘方法章’需要；第 1、2、16 章可省略”; Ch16 is the summary chapter |
| 15 | Every `\cite` key exists in `refs.bib` | **PASS** | 60 distinct cited keys, all present in the 63-entry database; 0 missing |
| 16 | Labels unique; all references resolve; `\eqref` used for equations | **PASS** | 304 labels, 0 duplicates; 493 ref calls, 0 undefined; 0 `\ref` on an `eq` label, 0 `\eqref` on a non-`eq` label |
| 17 | Build quality: 102 pages, 0 warnings, 5 overfull ≤3.57 pt, 0 `??` | **PASS** | `main.log` + `main.pdf`: `Pages: 102`; citation 0, reference 0, multiply-defined 0, Missing character 0, undefined 0, `??` 0; Overfull 5 at 2.82/1.24/0.38/1.11/3.57 pt |

## 3. Evidence details

### 3.1 Macro hygiene

`preamble.tex` defines exactly the ten contract macros:

```text
53: \newcommand{\dd}{\mathrm{d}}        56: \newcommand{\HF}{\mathrm{HF}}
54: \newcommand{\ee}{\mathrm{e}}        57: \newcommand{\xc}{\mathrm{xc}}
55: \newcommand{\ii}{\mathrm{i}}        58: \newcommand{\ket}[1]{...}
59: \newcommand{\bra}[1]{...}           60: \newcommand{\op}[1]{\hat{#1}}
66–76: \def\braket{...}, \def\bracket{...} (+ private \braket@nil / loop helpers)
```

The only other `\renewcommand`s (`preamble.tex:118,125,126`) target standard LaTeX hooks (`\refname`, `\headrulewidth`, `\footrulewidth`), not project macros. A cross-file name scan found no macro defined twice.

### 3.2 `\braket` / `\bracket` splitting

The implementation appends a sentinel `|` and recursively consumes `#1|#2\braket@nil`, emitting `\mid` whenever `#2` is non-empty. Isolated test output (XeLaTeX, 0 warnings):

```text
⟨a | b⟩          <- \braket{a|b}
⟨a | O | b⟩      <- \bracket{a|O|b}
⟨ij || ab⟩       <- \bracket{ij||ab}   (two \mid, as designed)
```

All 39 `\braket`/`\bracket` source calls use `|` as the delimiter; no call contains `\|`. The macro source never prints `|` itself, only `\mid`.

### 3.3 Chapter template

First-occurrence line numbers (strict order verified, including matching `\end` tags):

| File | problemchain | methodcard | first `\subsection` | ch4box | pitfall | 小结 | transition |
|---|---|---|---|---|---|---|---|
| ch01 | 10 | — | 17 | — | 163 | 172 | yes |
| ch02 | 10 | — | 17 | — | 252 | 261 | yes |
| ch03 | 10 | 17 | 29 | 231 | 249 | 258 | yes |
| ch04 | 10 | 17 | 29 | 203 | 227 | 236 | yes |
| ch05 | 10 | 17 | 29 | 206 | 214 | 224 | yes |
| ch06 | 10 | 17 | 29 | 229 | 238 | 248 | yes |
| ch07 | 10 | 17 | 30 | 203 | 213 | 223 | yes |
| ch08 | 10 | 17 | 30 | 163 | 179 | 189 | yes |
| ch09 | 10 | 17 | 29 | 189 | 206 | 215 | yes |
| ch10 | 10 | 17 | 29 | 176 | 200 | 209 | yes |
| ch11 | 10 | 17 | 29 | 143 | 167 | 176 | yes |
| ch12 | 10 | 17 | 29 | 143 | 177 | 187 | yes |
| ch13 | 10 | 17 | 29 | 135 | 169 | 180 | yes |
| ch14 | 10 | 17 | 29 | 150 | 160 | 170 | yes |
| ch15 | 10 | 17 | 29 | 171 | 181 | 191 | yes |
| ch16 | 10 | — | 16 | — | 201 | 213 | end of book |

Every chapter has one `\section{...}` plus `\label{ch:XX:sec:title}` at the top. Ch1–15 summaries end with an explicit “进入第 N 章：…” transition; Ch16 correctly has none.

### 3.4 Colors, tables, figures

- `preamble.tex:38–43` defines the six Okabe–Ito colors. Chapters reference them only by name inside TikZ options. No chapter defines a color and no chapter uses a hex/rgb literal. (The `ch12:79` numeric triple `(0.20,0.72,0.81)` is a set of B3LYP coefficients, not an RGB color.)
- 17 tables: 15 `tabular` + 2 `longtable` (`ch01:105`, `app-glossary:12`). All use `booktabs` rules; no `|` appears in any column specification; no `\hline`/`\cline`.
- 6 figures: `ch01`, `ch07`, `ch08`, `ch09`, `ch16` floats plus the `ch16` decision-tree TikZ block with `\captionof{figure}`. All carry captions and labels and are cited in text.

### 3.5 Labels and citations

- 304 labels: 163 `eq`, 6 `fig`, 17 `tab`, 114 `sec`, 4 appendix section labels (`app:orca`, `app:data`, `app:exercises`, `app:glossary`). Zero duplicates.
- 493 `\ref`/`\eqref` calls, all resolving. Equation labels are referenced exclusively with `\eqref`; float labels with `\ref`.
- `refs.bib` has 63 entries; 60 distinct keys are cited; all cited keys exist. No missing key.

### 3.6 Build gate (read-only)

Current artifacts agree with `docs/build-check.md` and `docs/audit-fixes.md`:

| Item | Value |
|---|---|
| `pdfinfo main.pdf` | `Pages: 102`, A4 |
| Citation / reference warnings | 0 / 0 |
| Multiply-defined labels | 0 |
| Missing character | 0 |
| Undefined control sequence | 0 |
| `??` in extracted PDF text | 0 |
| Overfull boxes | 5, max 3.56561 pt |

No rebuild was performed for this gate; `main.log` and `main.pdf` at HEAD were inspected as-is.

## 4. Notes (non-blocking)

1. **Unused bibliography entries (allowed as a note)**: `cramer2004`, `ernzerhof1999`, `neese2012orca` are present in `refs.bib` but not cited. Per the task, this is not a rejection criterion.
2. **`\text` vs `\mathrm` for two method subscripts**: `sections/ch14-xtb.tex:60,153` use `E_{\text{GFN2-xTB}}` and `sections/ch15-force-field.tex:136,174` use `E_{\text{GFN-FF}}`. They render consistently, but CONTRACT §3 recommends `\mathrm{}` for multi-character method subscripts. Cosmetic only.
3. **Fixed ch4box title**: `preamble.tex:97` hard-codes `title={CH$_4$ 算例（def2-TZVPP）}`. It therefore also appears on the Ch10/Ch11 boxes (which include 3c rows using built-in basis sets) and the Ch14/Ch15 boxes (xTB/GFN-FF use no external basis). The box bodies and table headers correctly state the actual basis, so the data are not wrong; the title is merely imprecise. A future edit could override the title in Ch14/15 or generalize it to “CH₄ 算例”. Out of F2's write scope.
4. **Within-gate typography**: 5 overfull boxes (max 3.56561 pt), 84 underfull hboxes, and one `` `h' float specifier changed to `ht' `` warning in `main.log`. All are inside the accepted build gate (`docs/build-check.md` §3).
5. **Bare `latexmk` invocation quirk**: running `latexmk` with no target also tries `preamble.tex` and fails; `latexmk -xelatex main.tex` builds cleanly. This is an invocation-scope artifact documented in `docs/build-check.md` §1, not a defect in the book sources.
6. **r²SCAN notation is uniform**: 46 occurrences of `r$^2$SCAN`, 0 of `r\textsuperscript{2}SCAN`; no cosmetic mixing remains.
7. **Ch9/Ch12–Ch15 have no tables**: this is a content choice, not a style inconsistency; all tables that do exist follow the booktabs convention.

## 5. Verdict

All 17 code-quality checks pass; build metrics are inside every gate; the only observations are non-blocking (three uncited bib entries, two cosmetic subscript spellings, one imprecise fixed box title, and typography already within tolerance).

**VERDICT: APPROVE**
