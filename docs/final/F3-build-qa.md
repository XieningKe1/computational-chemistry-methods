# F3 Build-Artifact QA

- Date: 2026-10-20
- Workspace: `/home/xieningke/课程/计算化学/泛函详解`
- Product under test: `main.tex` → `main.pdf`
- Method: clean rebuild from zero, then command-line artifact inspection only (no source edits).

## 1. Clean rebuild

Baseline removed with `latexmk -C` (exit 0). Then the required chain was executed in order.

| # | Command | Exit code | Evidence |
|---|---------|-----------|----------|
| 0 | `latexmk -C` | 0 | `main.pdf` removed |
| 1 | `latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex` | 0 | 102-page PDF produced; latexmk internally ran xelatex/bibtex to convergence |
| 2 | `bibtex main` | 0 | `main.blg`: 0 `Warning--` entries |
| 3 | `latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex` | 0 | "All targets (main.xdv main.pdf) are up-to-date" |
| 4 | `latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex` | 0 | "All targets (main.xdv main.pdf) are up-to-date" |

Notes:
- Pass 1 performed the actual multi-pass work (log shows repeated xelatex and bibtex rules); the explicit `bibtex main` regenerated an identical `.bbl`.
- Passes 3 and 4 reported nothing to do because latexmk considered the build current. Both exited 0; this is the expected idempotent result, not a skipped check.
- Final PDF: `main.pdf`, 1,208,499 bytes, sha256 `dcb2e9e5170cdf8653b74fdc2f1e63696aeecf5042000d4193b927ae87d3cc54`.

## 2. Artifact checks

| Check | Command | Actual result | Gate | Status |
|-------|---------|---------------|------|--------|
| Page count | `pdfinfo main.pdf \| grep Pages` | `Pages: 102` | 95–105 | PASS |
| Page size | `pdfinfo main.pdf \| grep 'Page size'` | `595.28 x 841.89 pts (A4)` | A4 | PASS |
| Fonts embedded | `pdffonts main.pdf` (parse `emb` column) | 46 fonts, 46 × `emb=yes`, 0 non-embedded | 0 non-embedded | PASS |
| Fonts subset | `pdffonts main.pdf` (parse `sub` column) | 46 × `sub=yes` | — | PASS |
| Missing glyphs | `grep -c 'Missing character' main.log` | `0` | 0 | PASS |
| Overfull boxes | `grep -c 'Overfull' main.log` | `5` | ≤ 5 | PASS |
| Overfull sizes | `grep 'Overfull' main.log` | max 3.56561pt; all < 10pt | each < 10pt | PASS |
| Replacement glyphs | `pdftotext main.pdf - \| grep -c '??'` | `0` | 0 | PASS |
| Citation warnings | `grep -c 'LaTeX Warning: Citation' main.log` | `0` | 0 | PASS |
| Reference warnings | `grep -c 'LaTeX Warning: Reference' main.log` | `0` | 0 | PASS |
| Multiply defined labels | `grep -c 'multiply defined' main.log` | `0` | 0 | PASS |
| Undefined refs/cites | `grep -c 'undefined' main.log` | `0` | 0 | PASS |
| Extractable text | `pdftotext main.pdf - \| wc -c` | `250604` chars | > 50000 | PASS |

### Overfull boxes (all five)

```
Overfull \hbox (2.82448pt too wide) in paragraph at lines 134--134
Overfull \hbox (1.23936pt too wide) in paragraph at lines 180--181
Overfull \hbox (0.38074pt too wide) in paragraph at lines 144--145
Overfull \hbox (1.10976pt too wide) in paragraph at lines 191--192
Overfull \hbox (3.56561pt too wide) in paragraph at lines 32--54
```

### Font embedding note

The literal command from the plan, `pdffonts main.pdf | grep -c 'no'`, returns `14`, but those matches are **not** non-embedded fonts: they are `uni=no` values and font names containing "No" (e.g. `NotoSansCJKjp`). Column-wise parsing of `emb` gives 46/46 `yes` and 0 `no`. The actual gate (no non-embedded fonts) passes.

Other observations (non-gating):
- One `LaTeX Warning: 'h' float specifier changed to 'ht'` at log line 2263; layout hint only, no undefined output.
- `pdftotext` warnings about binary characters are due to embedded control glyphs; `-enc UTF-8` extraction is complete.

## 3. Rendered PNG samples

| Sample | PDF page | Command | File | Size |
|--------|----------|---------|------|------|
| Title page | 1 | `pdftoppm -png -r 150 -f 1 -l 1 main.pdf figures/qa-title` | `figures/qa-title-001.png` | 49,777 B |
| TOC (spans pp. 2–5; page 3 sampled) | 3 | `pdftoppm -png -r 150 -f 3 -l 3 main.pdf figures/qa-toc` | `figures/qa-toc-003.png` | 324,570 B |
| Ch. 1 first page | 5 | `pdftoppm -png -r 150 -f 5 -l 5 main.pdf figures/qa-ch1` | `figures/qa-ch1-005.png` | 186,160 B |
| Ch. 9 first page | 47 | `pdftoppm -png -r 150 -f 47 -l 47 main.pdf figures/qa-ch9` | `figures/qa-ch9-047.png` | 265,013 B |
| Last page (references) | 102 | `pdftoppm -png -r 150 -f 102 -l 102 main.pdf figures/qa-last` | `figures/qa-last-102.png` | 44,950 B |

All five are valid PNGs, 1241 × 1754 px (A4 at 150 dpi), and every file exceeds 20 KB.

Page-location evidence:
- `main.toc`: Ch. 1 starts on printed page 5; Ch. 9 starts on printed page 47.
- `pdftotext -f 2 -l 5 main.pdf -` confirms the TOC occupies PDF pages 2–5.
- PDF page 102 is the final references page (printed page 101).

## 4. Scope compliance

- No source/product file was modified: `git status --porcelain` shows no tracked modifications.
- Written artifacts: `docs/final/F3-build-qa.md` and `figures/qa-*.png` only.
- No commit was made; no `--dry-run` was used.

## 5. Acceptance summary

| Acceptance item | Status |
|-----------------|--------|
| Clean rebuild chain exits 0 | PASS |
| No non-embedded fonts | PASS |
| 0 missing characters | PASS |
| ≤ 5 overfull boxes, each < 10pt | PASS (5, max 3.57pt) |
| Page count 95–105 | PASS (102) |
| Extractable text > 50,000 chars | PASS (250,604) |
| Five PNG samples exist and are non-trivial | PASS |
| Report records commands, exit codes, numbers, PNGs | PASS |

## VERDICT: **APPROVE**

---

# Post-remediation rerun (2026-10-20, after environment change)

Trigger: `pgfplots` was moved from `~/texmf` to `~/texmf-disabled/pgfplots-4.42`, `latexmkrc`/`build-chapter.sh` were updated to prepend that tree to `TEXINPUTS`, and Appendix A received a one-line AuxC wording fix. The entire F3 build-artifact QA was repeated against the current tree.

## R1. Clean rebuild

| # | Command | Exit code | Evidence |
|---|---------|-----------|----------|
| 0 | `latexmk -C` | 0 | `main.pdf` removed |
| 1 | `latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex` | 0 | 102-page PDF produced |
| 2 | `bibtex main` | 0 | `main.blg`: 0 `Warning--` entries |
| 3 | `latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex` | 0 | up-to-date |
| 4 | `latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex` | 0 | up-to-date |

Environment verification: `main.log` records pgfplots loaded from `/home/xieningke/texmf-disabled/pgfplots-4.42/tex/latex/pgfplots/pgfplots.sty`, i.e. the new TEXINPUTS path is active.

Final artifact: `main.pdf`, 1,208,523 bytes, 102 pages, sha256 `6bb4044437571d7cd4e2efd6861908d8e84ade416df8279ddef350151cd18bdf`.

## R2. Artifact checks

| Check | Actual result | Gate | Status |
|-------|---------------|------|--------|
| `pdfinfo main.pdf \| grep Pages` | `Pages: 102` | 95–105 | PASS |
| Page size | `595.28 x 841.89 pts (A4)` | A4 | PASS |
| `pdffonts` (`emb` column) | 46 fonts, 0 non-embedded | 0 | PASS |
| `pdffonts` (`sub` column) | 46 fonts, 0 non-subset | — | PASS |
| `grep -c 'Missing character' main.log` | `0` | 0 | PASS |
| `grep -c 'Overfull' main.log` | `5` | ≤ 5 | PASS |
| Overfull max size | `3.56561pt` (all five < 10pt) | each < 10pt | PASS |
| `pdftotext main.pdf - \| grep -c '??'` | `0` | 0 | PASS |
| `grep -c 'LaTeX Warning: Citation' main.log` | `0` | 0 | PASS |
| `grep -c 'LaTeX Warning: Reference' main.log` | `0` | 0 | PASS |
| `grep -c 'multiply defined' main.log` | `0` | 0 | PASS |
| `grep -c 'undefined' main.log` | `0` | 0 | PASS |
| `pdftotext main.pdf - \| wc -c` | `250623` | > 50,000 | PASS |

Overfull boxes are unchanged:

```
Overfull \hbox (2.82448pt too wide) in paragraph at lines 134--134
Overfull \hbox (1.23936pt too wide) in paragraph at lines 180--181
Overfull \hbox (0.38074pt too wide) in paragraph at lines 144--145
Overfull \hbox (1.10976pt too wide) in paragraph at lines 191--192
Overfull \hbox (3.56561pt too wide) in paragraph at lines 32--54
```

The single remaining log warning is the non-gating `'h' float specifier changed to 'ht'` hint.

## R3. PNG samples

Page numbers did not shift (TOC pp. 2–5; Ch. 1 p. 5; Ch. 9 p. 47; last p. 102), but all five samples were re-rendered from the new PDF:

| Sample | Page | File | Size |
|--------|------|------|------|
| Title | 1 | `figures/qa-title-001.png` | 49,777 B |
| TOC | 3 | `figures/qa-toc-003.png` | 324,570 B |
| Ch. 1 first page | 5 | `figures/qa-ch1-005.png` | 186,160 B |
| Ch. 9 first page | 47 | `figures/qa-ch9-047.png` | 265,013 B |
| Last page | 102 | `figures/qa-last-102.png` | 44,950 B |

All are valid 1241 × 1754 PNGs and exceed 20 KB.

## R4. Scope compliance

- No tracked product/source file was modified (`git status --porcelain` shows no tracked modifications).
- Only this report and `figures/qa-*.png` were refreshed; no commit.

## R5. Post-remediation acceptance

| Acceptance item | Status |
|-----------------|--------|
| Clean rebuild chain exits 0 with relocated pgfplots | PASS |
| No non-embedded fonts | PASS |
| 0 missing characters | PASS |
| ≤ 5 overfull boxes, each < 10pt | PASS (5, max 3.57pt) |
| Page count 95–105 | PASS (102) |
| Extractable text > 50,000 chars | PASS (250,623) |
| Five PNG samples valid | PASS |
| No citation/reference/multiply/undefined warnings | PASS |

## VERDICT: **APPROVE**
