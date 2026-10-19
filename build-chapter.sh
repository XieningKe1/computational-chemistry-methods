#!/usr/bin/env bash
# build-chapter.sh — 全量或单章（\includeonly）构建
# 用法:
#   ./build-chapter.sh                                  # 全量 latexmk
#   ./build-chapter.sh sections/ch03-hf                  # 单章
#   ./build-chapter.sh sections/ch03-hf sections/ch04-mp2 # 多章
set -euo pipefail

cd "$(dirname "$0")"
export PATH="$HOME/.local/bin:$HOME/bin:$PATH"

if [ "$#" -gt 0 ]; then
  INC=$(IFS=,; echo "$*")
  JOBN=${JOBN:-chapter-build}

  xelatex -interaction=nonstopmode -halt-on-error \
    -jobname="$JOBN" "\def\ChapterIncludeOnly{$INC}\input{main.tex}"
  # 无引用时 bibtex 会以非零退出，这里容忍
  bibtex "$JOBN" || true
  xelatex -interaction=nonstopmode -halt-on-error \
    -jobname="$JOBN" "\def\ChapterIncludeOnly{$INC}\input{main.tex}"
  xelatex -interaction=nonstopmode -halt-on-error \
    -jobname="$JOBN" "\def\ChapterIncludeOnly{$INC}\input{main.tex}"
else
  latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
fi
