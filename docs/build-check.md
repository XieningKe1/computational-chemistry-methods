# Full-Book Build Check (T15)

- **Repository**: `/home/xieningke/课程/计算化学/泛函详解`
- **HEAD**: `5252f1d`
- **Date**: 2026-10-20
- **Engine**: XeTeX 3.14159265-2.6-0.999992 (TeX Live 2020); Latexmk 4.88; BibTeX 0.99d
- **Working tree**: only untracked `.omo/`, `docs/` (this report), and `main.pdf`; no source files modified, no commit made.

## 1. Build commands and exit codes

All commands run from the repository root with `export PATH="$HOME/.local/bin:$HOME/bin:$PATH"`.

| # | Command | Exit code | Result |
|---|---------|-----------|--------|
| 1 | `latexmk -C` | 0 | Full clean; `main.pdf` and generated artifacts removed |
| 2 | `latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex` | 0 | Fresh PDF produced, 102 pages |
| 3 | `bibtex main` | 0 | `plainnat.bst`, `refs.bib`; 60 `\bibitem` entries |
| 4 | `latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex` | 0 | "All targets (main.xdv main.pdf) are up-to-date" |
| 5 | `latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex` | 0 | "All targets (main.xdv main.pdf) are up-to-date" |

The canonical sequence in the plan (`latexmk -C && latexmk -xelatex main.tex && bibtex main && latexmk -xelatex main.tex && latexmk -xelatex main.tex`) targets `main.tex` explicitly. Steps 4 and 5 are no-ops because the first Latexmk pass already converged and the manual BibTeX output was byte-identical, so no rerun was needed; both invocations still exit 0.

### Note on bare `latexmk` (harness quirk, not a book failure)

Running `latexmk` with **no file argument** makes Latexmk treat every `.tex` file in the directory as a target, including the non-standalone `preamble.tex`:

```
Running 'xelatex ... "preamble.tex"'
! LaTeX Error: \usepackage before \documentclass.
Latexmk: Some operations failed ... preamble.tex
exit code 12
```

`main.tex` itself built successfully in that same invocation ("Nothing to do for 'main.tex'"). This is an invocation-scope artifact of having `preamble.tex` in the root, not a defect in the book sources. The authoritative `main.tex`-targeted builds all exit 0. No source or config file was edited to work around it.

## 2. Acceptance checks

| Item | Command | Expected | Actual | Verdict |
|------|---------|----------|--------|---------|
| Fresh build exits 0 | steps 1–5 above | all 0 | 0, 0, 0, 0, 0 | **PASS** |
| Page count | `pdfinfo main.pdf \| grep Pages` | 95–105 | `Pages: 102` | **PASS** |
| Citation warnings | `grep 'LaTeX Warning: Citation' main.log \| wc -l` | 0 | `0` | **PASS** |
| Reference warnings | `grep 'LaTeX Warning: Reference' main.log \| wc -l` | 0 | `0` | **PASS** |
| Unresolved `??` in PDF | `pdftotext main.pdf - \| grep -c '??'` | 0 | `0` | **PASS** |
| Multiply-defined labels | `grep -c 'multiply defined' main.log` | 0 | `0` | **PASS** |
| Missing characters | `grep -c 'Missing character' main.log` | 0 | `0` | **PASS** |
| Overfull boxes | `grep -c 'Overfull' main.log` | ≤ 5, each < 10pt | 5, max 3.56561pt | **PASS** |
| TOC renders | `pdftotext main.pdf - \| sed -n '1,80p'` | contains 目录 + chapter entries | 目录 on line 8; chapters 1–2 visible; 128 `\contentsline` entries, 16 chapters | **PASS** |
| Bibliography renders | `pdftotext main.pdf - \| grep -a '参考文献'` | present | heading on printed pp. 96–101 (physical 97–102), 60 entries | **PASS** |
| No commit | `git status --porcelain` | no commit | only untracked `.omo/`, `main.pdf` | **PASS** |

PDF details: A4 (595.28 × 841.89 pt), 1.2 MB, SHA-256 `2f18fc83c6b9eca573034c9137010efd5d080d29acb922ed9b03357d5ae2b4f2`.

## 3. Overfull box list

Gate: total ≤ 5 and every box < 10pt. Total = 5; maximum = 3.56561pt.

| # | Source file | Log lines | Size (pt) |
|---|-------------|-----------|-----------|
| 1 | `sections/ch01-overview.tex` | 134–134 | 2.82448 |
| 2 | `sections/ch02-foundations.tex` | 176–177 | 1.23936 |
| 3 | `sections/ch16-summary.tex` | 144–145 | 0.38074 |
| 4 | `sections/ch16-summary.tex` | 191–192 | 1.10976 |
| 5 | `appendix/app-data.tex` | 32–54 | 3.56561 |

Non-blocking observations (not part of the acceptance gate): 84 underfull hboxes, and one warning `` `h' float specifier changed to `ht' ``. Neither affects references, citations, or rendering checks.

## 4. BibTeX log (`main.blg`)

- `grep -i -E "warning--|error|didn't find|couldn't" main.blg` → no matches.
- Database `refs.bib`, style `plainnat.bst`, 60 `\bibitem` entries in `main.bbl`.
- Consistent with 0 citation warnings and 0 `??` in the PDF.

## 5. TOC and page ranges

TOC evidence (`pdftotext main.pdf - | sed -n '1,80p'`): `目录` appears on line 8; chapter entries such as `第 1 章 计算化学到底在解什么问题？` and `第 2 章 …` are present with page numbers.

From `main.toc` (printed page numbers):

| Part | Start page | Range |
|------|-----------|-------|
| 第16章 CH4/H2−：同一分子、不同方法，如何选？ | 79 | 79–84 |
| 附录 A ORCA 环境与输入模板 | 85 | 85–88 |
| 附录 B 数据获取方式说明 | 89 | 89–90 |
| 附录 C 习题与解答 | 91 | 91–93 |
| 附录 D 术语中英对照表 | 94 | 94–95 |
| 参考文献 | 96 | 96–101 |

Physical PDF pages are offset by +1 from printed page numbers (cover is physical page 1); physical total 102.

## 6. Verdict

**PASS** — the full book builds cleanly from scratch with `main.tex` as the target: 102 pages (within 95–105), zero citation/reference/multiply-defined/missing-character/`??` issues, 5 overfull boxes all below 4pt, valid TOC, and a rendered 60-entry bibliography. No source files were modified and no commit was created. The only caveat is the bare `latexmk` invocation quirk described in §1, which is unrelated to the book content and does not affect the `main.tex` build.
