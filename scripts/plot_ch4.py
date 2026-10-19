#!/usr/bin/env python3
"""Plot CH4 method deviations relative to CCSD(T).

Reads ``data/ch4_results.csv`` (override with ``--csv``) and writes a vector
PDF bar chart. Rows for xTB / GFN-FF and rows with basis ``none`` are excluded
because their total energies are not comparable to QM methods.

Usage:
    python3 scripts/plot_ch4.py
    python3 scripts/plot_ch4.py --csv data/ch4_results.csv --out figures/ch4_deviations.pdf
"""

from __future__ import annotations

import argparse
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

HARTREE_TO_KCAL = 627.509474
NON_QM_METHODS = {"GFN2-XTB", "GFN1-XTB", "XTB", "GFN-FF"}
THREE_C_METHODS = {"B97-3C", "R2SCAN-3C"}
COLOR_QM = "#0072B2"
COLOR_3C = "#E69F00"

plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK JP",
    "Droid Sans Fallback",
    "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False


def _fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def _is_3c(method: str) -> bool:
    return method.strip().upper() in THREE_C_METHODS


def load_deviations(csv_path: str) -> pd.DataFrame:
    if not os.path.isfile(csv_path):
        _fail(f"CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)
    required = {"method", "basis", "energy"}
    missing = required - set(df.columns)
    if missing:
        _fail(f"{csv_path} is missing required column(s): {sorted(missing)}")

    df = df.copy()
    df["method"] = df["method"].astype(str).str.strip()
    df["basis"] = df["basis"].fillna("").astype(str).str.strip()
    df["energy"] = pd.to_numeric(df["energy"], errors="coerce")

    ref = df[df["method"].str.upper() == "CCSD(T)"]
    ref = ref[ref["energy"].notna()]
    if ref.empty:
        _fail(f"CCSD(T) reference row with a valid energy not found in {csv_path}")

    e_ref = float(ref.iloc[0]["energy"])
    if len(ref) > 1 and ref["energy"].nunique() > 1:
        print(
            f"warning: multiple distinct CCSD(T) energies found; using {e_ref:.12f} Eh",
            file=sys.stderr,
        )

    method_upper = df["method"].str.upper()
    is_non_qm = method_upper.isin(NON_QM_METHODS) | method_upper.str.contains(
        "XTB", na=False
    )
    has_no_basis = df["basis"].str.lower() == "none"
    df = df[(~is_non_qm) & (~has_no_basis) & df["energy"].notna()].copy()
    df = df[df["method"].str.len() > 0]

    if df.empty:
        _fail("no comparable QM rows left after filtering")

    df["delta_kcal"] = (df["energy"] - e_ref) * HARTREE_TO_KCAL
    df = df.sort_values("delta_kcal", ascending=True).reset_index(drop=True)
    return df


def make_plot(df: pd.DataFrame, out_path: str) -> None:
    labels = [
        f"{row.method} ({row.basis})" if row.basis else row.method
        for row in df.itertuples()
    ]
    colors = [COLOR_3C if _is_3c(m) else COLOR_QM for m in df["method"]]
    hatches = ["///" if _is_3c(m) else "" for m in df["method"]]

    height = max(3.6, 0.34 * len(df) + 1.6)
    fig, ax = plt.subplots(figsize=(8.4, height))
    y = np.arange(len(df))
    bars = ax.barh(
        y,
        df["delta_kcal"].to_numpy(),
        color=colors,
        edgecolor="0.25",
        linewidth=0.6,
    )
    for bar, hatch in zip(bars, hatches):
        if hatch:
            bar.set_hatch(hatch)

    ax.axvline(0.0, color="0.3", linewidth=0.9, zorder=1)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel("ΔE vs CCSD(T) / kcal·mol$^{-1}$")
    ax.set_title("CH4: method deviations from CCSD(T)")
    ax.grid(axis="x", color="0.85", linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.bar_label(bars, fmt="%+.1f", padding=2, fontsize=7)

    handles = [
        Patch(facecolor=COLOR_QM, edgecolor="0.25", label="QM method"),
        Patch(
            facecolor=COLOR_3C,
            edgecolor="0.25",
            hatch="///",
            label="3c: built-in basis",
        ),
    ]
    ax.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.12),
        ncol=2,
        frameon=False,
        fontsize=8,
    )

    fig.tight_layout()
    parent = os.path.dirname(os.path.abspath(out_path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    fig.savefig(out_path, format="pdf", bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_path}")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", default="data/ch4_results.csv", help="input CSV")
    parser.add_argument(
        "--out", default="figures/ch4_deviations.pdf", help="output PDF path"
    )
    args = parser.parse_args(argv)

    df = load_deviations(args.csv)
    make_plot(df, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
