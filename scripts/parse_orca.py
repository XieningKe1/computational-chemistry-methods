#!/usr/bin/env python3
"""Parse ORCA 6.x output files into structured JSON or CSV.

Single-file mode prints a JSON object to stdout:

    {"method": "HF", "basis": "def2-SVP", "energy": -40.169177376015,
     "s2": null, "converged": true, "runtime": "00:00:01.910",
     "inp_path": "/path/to/ch4_hf.inp"}

Batch mode accepts a directory or a glob pattern, e.g.:

    python3 scripts/parse_orca.py --batch runs/ch4 --csv data/ch4_results.csv

CSV columns (exactly, in this order):

    method,basis,energy,s2,converged,runtime,inp_path

Notes
-----
* ``energy`` is the last ``FINAL SINGLE POINT ENERGY`` in Eh, or null.
* ``s2`` is the last ``Expectation value of <S**2>`` or null when absent.
* ``converged`` is true only when ``ORCA TERMINATED NORMALLY`` is present.
* ``runtime`` is normalized to ``HH:MM:SS`` / ``HH:MM:SS.mmm`` or null.
* ``basis`` is ``"none"`` for xTB / GFN-FF runs where no basis is specified.
* Failed or truncated jobs never raise; the row is emitted with nulls and a
  warning is printed to stderr.
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import re
import sys
from typing import Dict, Iterable, List, Optional

ECHO_RE = re.compile(r"^\|\s*\d+>\s*!\s*(.+?)\s*$")
ENERGY_RE = re.compile(r"FINAL SINGLE POINT ENERGY\s+(-?\d+\.\d+)")
S2_RE = re.compile(
    r"Expectation value of\s*<S\*\*2>\s*:\s*(-?\d+\.\d+(?:[EeDd][+-]?\d+)?|\*+)"
)
RUNTIME_RE = re.compile(
    r"TOTAL RUN TIME:\s*(?:(\d+)\s+days?\s+)?(\d+)\s+hours?\s+"
    r"(\d+)\s+minutes?\s+(\d+)\s+sec(?:onds?)?(?:\s+(\d+)\s+msec)?"
)
BASIS_RE = re.compile(r"^(def2|aug-|ma-|cc-p|6-31|STO-)", re.IGNORECASE)
BASIS_HEADER_RE = re.compile(r"^Your calculation utilizes the basis:\s*(\S+)\s*$")

CSV_FIELDS = ["method", "basis", "energy", "s2", "converged", "runtime", "inp_path"]

# Keywords that appear on the simple input line but are not the method name.
_OPTION_KEYWORDS = {
    # SCF / convergence
    "TIGHTSCF", "VERYTIGHTSCF", "NORMALSCF", "LOOSESCF", "SLOWCONV",
    "VERYSLOWCONV", "SOSCF", "NOSOSCF", "DIRECT", "NODIRECT",
    # RI / integrals
    "RI", "NORI", "RIJCOSX", "RIJK", "RIJ", "RIJONX", "NORIJCOSX",
    "AUTOAUX", "NOAUTOAUX", "DEFGRID1", "DEFGRID2", "DEFGRID3",
    "DEFGRID", "GRID5", "GRID6", "GRID7",
    # job types
    "SP", "OPT", "OPTOPT", "FREQ", "NUMFREQ", "ENGRAD", "OPTTS",
    "TS", "IRC", "NEB", "MD", "MDRUN", "SOC", "COORDS",
    # misc
    "NOSYM", "SYM", "NOXYZ", "XYZFILE", "PRINTBASIS", "MOREAD",
    "NOPRINT", "MINIPRINT", "SMALLPRINT", "LARGEPRINT",
    "NOAUTOSTART", "AUTOSTART", "ALLOWRHF", "NOALLOWRHF",
    "KEEPINTS", "NOKEEPINTS",
}


def _token_upper(tok: str) -> str:
    return tok.strip().rstrip(",").upper()


def _is_option(tok: str) -> bool:
    upper = _token_upper(tok)
    if upper in _OPTION_KEYWORDS:
        return True
    if upper.startswith("PAL"):  # PAL2, PAL4, PAL8 ...
        return True
    if upper.startswith("%") or upper.startswith("#"):
        return True
    return False


def _is_basis_token(tok: str) -> bool:
    """True for basis-set names; excludes auxiliary basis (contains '/')."""
    if "/" in tok:
        return False
    return bool(BASIS_RE.match(tok))


def _split_simple_line(line: str) -> Dict[str, Optional[str]]:
    """Extract ``method`` and ``basis`` from an ORCA ``!`` input line."""
    tokens = line.replace(",", " ").split()
    method: Optional[str] = None
    basis: Optional[str] = None

    # Basis = first token that looks like a real (non-auxiliary) basis set.
    for tok in tokens:
        if _is_basis_token(tok):
            basis = tok
            break

    # Method = first token that is neither an option, a basis, nor a number.
    for tok in tokens:
        cleaned = tok.strip().rstrip(",")
        if not cleaned:
            continue
        if _is_option(cleaned):
            continue
        if _is_basis_token(cleaned) or "/" in cleaned:
            continue
        if re.fullmatch(r"[-+]?\d+(?:\.\d*)?", cleaned):
            continue
        upper = _token_upper(cleaned)
        if upper in {"(", ")"} or cleaned.startswith("("):
            continue
        method = cleaned
        break

    return {"method": method, "basis": basis}


def _read_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError as exc:  # unreadable file: never traceback
        print(f"warning: cannot read {path}: {exc}", file=sys.stderr)
        return ""


def _find_input_line(text: str, inp_path: Optional[str]) -> Optional[str]:
    """Prefer the echoed ``|  1> ! ...`` line, fall back to the sibling .inp."""
    for line in text.splitlines():
        match = ECHO_RE.match(line.strip())
        if match:
            return match.group(1)
    if inp_path and os.path.isfile(inp_path):
        inp_text = _read_text(inp_path)
        for line in inp_text.splitlines():
            stripped = line.strip()
            if stripped.startswith("!"):
                return stripped[1:].strip()
    return None


def _normalize_runtime(text: str) -> Optional[str]:
    matches = list(RUNTIME_RE.finditer(text))
    if not matches:
        return None
    match = matches[-1]
    days = int(match.group(1) or 0)
    hours = int(match.group(2)) + 24 * days
    minutes = int(match.group(3))
    seconds = int(match.group(4))
    msec = match.group(5)
    stamp = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    if msec is not None:
        stamp += f".{int(msec):03d}"
    return stamp


def _to_float(value: str) -> Optional[float]:
    try:
        return float(value.replace("D", "E").replace("d", "e"))
    except (TypeError, ValueError):
        return None


def parse_output(path: str) -> Dict[str, object]:
    """Parse a single ORCA output file; never raises on malformed content."""
    path = os.path.abspath(path)
    inp_path = None
    candidate_inp = os.path.splitext(path)[0] + ".inp"
    if os.path.isfile(candidate_inp):
        inp_path = os.path.abspath(candidate_inp)

    text = _read_text(path)

    result: Dict[str, object] = {
        "method": None,
        "basis": None,
        "energy": None,
        "s2": None,
        "converged": False,
        "runtime": None,
        "inp_path": inp_path,
    }

    input_line = _find_input_line(text, inp_path)
    if input_line:
        parsed = _split_simple_line(input_line)
        result["method"] = parsed["method"]
        result["basis"] = parsed["basis"]

    # ORCA may rely on its default basis (e.g. ``! PBE0 TightSCF``); the
    # output header then names the basis actually used.
    if result["basis"] is None:
        for line in text.splitlines():
            match = BASIS_HEADER_RE.match(line.strip())
            if match:
                result["basis"] = match.group(1)
                break

    # xTB / GFN-FF runs legitimately carry no basis set.
    if result["basis"] is None:
        method_upper = (result["method"] or "").upper()
        if "XTB" in method_upper or "GFN" in method_upper:
            result["basis"] = "none"

    energies = ENERGY_RE.findall(text)
    if energies:
        result["energy"] = _to_float(energies[-1])

    s2_values = S2_RE.findall(text)
    if s2_values:
        last = s2_values[-1]
        if not set(last) <= {"*"}:
            result["s2"] = _to_float(last)

    result["converged"] = "ORCA TERMINATED NORMALLY" in text
    result["runtime"] = _normalize_runtime(text)

    if result["energy"] is None or not result["converged"]:
        reasons = []
        if result["energy"] is None:
            reasons.append("no FINAL SINGLE POINT ENERGY")
        if not result["converged"]:
            reasons.append("ORCA TERMINATED NORMALLY missing")
        print(
            f"warning: {path}: {'; '.join(reasons)} (failed/truncated job?)",
            file=sys.stderr,
        )

    return result


def _collect_outputs(batch: str) -> List[str]:
    """Resolve a directory or glob pattern to a sorted list of .out files."""
    if os.path.isdir(batch):
        paths = glob.glob(os.path.join(batch, "**", "*.out"), recursive=True)
    else:
        paths = glob.glob(batch, recursive=True)
    return sorted(os.path.abspath(p) for p in paths if os.path.isfile(p))


def _write_csv(rows: Iterable[Dict[str, object]], csv_path: str) -> None:
    parent = os.path.dirname(os.path.abspath(csv_path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in rows:
            out = dict(row)
            if out.get("energy") is None:
                out["energy"] = ""
            if out.get("s2") is None:
                out["s2"] = ""
            if out.get("method") is None:
                out["method"] = ""
            if out.get("basis") is None:
                out["basis"] = ""
            if out.get("runtime") is None or out.get("inp_path") is None:
                out["runtime"] = out.get("runtime") or ""
                out["inp_path"] = out.get("inp_path") or ""
            writer.writerow(out)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Parse ORCA 6.x output files into JSON or CSV.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "CSV columns: method,basis,energy,s2,converged,runtime,inp_path\n"
            "energy is in Eh; runtime is normalized to HH:MM:SS[.mmm].\n\n"
            "Examples:\n"
            "  %(prog)s ch4_hf.out\n"
            "  %(prog)s --batch runs/ch4 --csv /tmp/ch4.csv\n"
            "  %(prog)s --batch 'runs/h2m/*.out' --csv /tmp/h2m.csv\n"
        ),
    )
    parser.add_argument("path", nargs="?", help="single ORCA .out file")
    parser.add_argument(
        "--batch",
        metavar="DIR_OR_GLOB",
        help="parse all .out files under a directory (recursive) or a glob pattern",
    )
    parser.add_argument(
        "--csv", metavar="PATH", help="write parsed rows to this CSV file"
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    if not args.path and not args.batch:
        build_parser().error("provide a single .out path or --batch DIR_OR_GLOB")
    if args.path and args.batch:
        build_parser().error("use either a single path or --batch, not both")

    if args.path:
        if not os.path.isfile(args.path):
            print(f"error: file not found: {args.path}", file=sys.stderr)
            return 2
        row = parse_output(args.path)
        if args.csv:
            _write_csv([row], args.csv)
        else:
            print(json.dumps(row, indent=2, ensure_ascii=False))
        return 0

    paths = _collect_outputs(args.batch)
    if not paths:
        print(f"error: no .out files matched {args.batch!r}", file=sys.stderr)
        return 2

    rows = [parse_output(path) for path in paths]
    if args.csv:
        _write_csv(rows, args.csv)
        converged = sum(1 for row in rows if row["converged"])
        print(
            f"parsed {len(rows)} file(s) -> {os.path.abspath(args.csv)} "
            f"({converged} converged, {len(rows) - converged} failed)",
            file=sys.stderr,
        )
    else:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
