#!/usr/bin/env python3
"""Plot two-panel H2 potential-energy and spin-contamination figure.

Reads ``data/h2m_pes.csv`` (columns ``method,R,energy,s2``; override with
``--csv``) and writes a vector PDF with:
  (a) E - E_min per method versus R in Angstrom,
  (b) <S**2> versus R for every method that reports a value.

Usage:
    python3 scripts/plot_h2m.py
    python3 scripts/plot_h2m.py --csv data/h2m_pes.csv --out figures/h2m_pes.pdf
"""

from __future__ import annotations

import argparse
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

COLORS = [
    "#0072B2",
    "#E69F00",
    "#009E73",
    "#CC79A7",
    "#56B4E9",
    "#D55E00",
    "#F0E442",
    "#000000",
]
MARKERS = ["o", "s", "^", "D", "v", "P", "X", "*"]

plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK JP",
    "Droid Sans Fallback",
    "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False


def _fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_data(csv_path: str) -> pd.DataFrame:
    if not os.path.isfile(csv_path):
        _fail(f"CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)
    required = {"method", "R", "energy", "s2"}
    missing = required - set(df.columns)
    if missing:
        _fail(f"{csv_path} is missing required column(s): {sorted(missing)}")

    df = df.copy()
    df["method"] = df["method"].astype(str).str.strip()
    df["R"] = pd.to_numeric(df["R"], errors="coerce")
    df["energy"] = pd.to_numeric(df["energy"], errors="coerce")
    df["s2"] = pd.to_numeric(df["s2"], errors="coerce")
    df = df[(df["method"].str.len() > 0) & df["R"].notna()]
    df = df.sort_values(["method", "R"]).reset_index(drop=True)

    if df[df["energy"].notna()].empty:
        _fail(f"no valid energy rows in {csv_path}")
    return df


def _style(method: str, index: int) -> dict:
    return {
        "color": COLORS[index % len(COLORS)],
        "marker": MARKERS[index % len(MARKERS)],
        "markersize": 4.5,
        "linewidth": 1.4,
    }


def make_plot(df: pd.DataFrame, out_path: str) -> None:
    methods = list(dict.fromkeys(df["method"]))
    styles = {method: _style(method, i) for i, method in enumerate(methods)}

    fig, (ax1, ax2) = plt.subplots(
        2,
        1,
        sharex=True,
        figsize=(8.0, 7.4),
        gridspec_kw={"height_ratios": [2.2, 1.0]},
    )

    for method in methods:
        sub = df[(df["method"] == method) & df["energy"].notna()]
        if sub.empty:
            continue
        y = sub["energy"] - sub["energy"].min()
        ax1.plot(sub["R"], y, label=method, **styles[method])

    ax1.set_ylabel(r"$E - E_{min}$ / Eh")
    ax1.set_title("Potential energy curves")
    ax1.grid(color="0.88", linewidth=0.6)
    ax1.legend(
        loc="upper left",
        bbox_to_anchor=(1.01, 1.0),
        frameon=False,
        fontsize=8,
        title="Method",
        title_fontsize=8,
    )

    s2_methods = [
        method
        for method in methods
        if df[(df["method"] == method) & df["s2"].notna()].shape[0] > 0
    ]
    for method in s2_methods:
        sub = df[(df["method"] == method) & df["s2"].notna()]
        style = dict(styles[method])
        style["marker"] = MARKERS[methods.index(method) % len(MARKERS)]
        ax2.plot(sub["R"], sub["s2"], label=method, **style)

    if s2_methods:
        ax2.legend(
            loc="upper left",
            bbox_to_anchor=(1.01, 1.0),
            frameon=False,
            fontsize=8,
            title="Method",
            title_fontsize=8,
        )
    else:
        ax2.text(
            0.5,
            0.5,
            r"No $\langle S^2 \rangle$ values available",
            transform=ax2.transAxes,
            ha="center",
            va="center",
        )

    ax2.set_xlabel("R / Å")
    ax2.set_ylabel(r"$\langle S^2 \rangle$")
    ax2.set_title("Spin contamination")
    ax2.grid(color="0.88", linewidth=0.6)

    fig.tight_layout()
    parent = os.path.dirname(os.path.abspath(out_path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    fig.savefig(out_path, format="pdf", bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out_path}")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", default="data/h2m_pes.csv", help="input CSV")
    parser.add_argument(
        "--out", default="figures/h2m_pes.pdf", help="output PDF path"
    )
    args = parser.parse_args(argv)

    make_plot(load_data(args.csv), args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
