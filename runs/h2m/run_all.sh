#!/usr/bin/env bash
# H2- (charge -1, doublet) def2-TZVPP PES scan: 6 methods x 8 bond lengths.
# Run from anywhere; all paths are resolved relative to this script.
set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"
export PATH="$HOME/openmpi418/bin:$PATH"
export LD_LIBRARY_PATH="$HOME/openmpi418/lib:${LD_LIBRARY_PATH:-}"
ORCA="/home/xieningke/orca611/orca"
RS=(0.6 0.8 1.0 1.2 1.5 2.0 2.5 3.0)

run_method() {
  local m="$1" mr="$2" np="$3" prev_dir="" rc
  local i=0
  for R in "${RS[@]}"; do
    local d="$ROOT/$m/R$R"
    if [[ "$mr" == "1" && -n "$prev_dir" ]]; then
      cp "$prev_dir/$m.gbw" "$d/start.gbw" || echo "[$m R$R] WARNING: no previous gbw from $prev_dir"
    fi
    ( cd "$d" && timeout 3600 "$ORCA" "$m.inp" > "$m.out" 2>&1 )
    rc=$?
    if [[ $rc -ne 0 ]] || ! grep -q "FINAL SINGLE POINT ENERGY" "$d/$m.out"; then
      echo "[$m R$R] first attempt rc=$rc missing energy; preserving .failed.out and retrying nprocs 1"
      mv "$d/$m.out" "$d/$m.failed.out"
      sed -e 's/^%pal nprocs [0-9]* end/%pal nprocs 1 end/' -e 's/ MORead$//' "$d/$m.inp" > "$d/${m}_retry.inp"
      ( cd "$d" && timeout 3600 "$ORCA" "${m}_retry.inp" > "$m.out" 2>&1 )
      if ! grep -q "FINAL SINGLE POINT ENERGY" "$d/$m.out"; then
        echo "[$m R$R] RETRY FAILED"
      else
        echo "[$m R$R] retry OK"
      fi
    fi
    if grep -q "FINAL SINGLE POINT ENERGY" "$d/$m.out"; then
      echo "[$m R$R] OK $(grep 'FINAL SINGLE POINT ENERGY' "$d/$m.out" | tail -1)"
    fi
    prev_dir="$d"
    i=$((i+1))
  done
}

rc_master=0
run_method uhf    0 4 & p_uhf=$!
run_method mp2    0 4 & p_mp2=$!
run_method ccsdt  0 2 & p_ccsdt=$!
run_method casscf 1 4 & p_casscf=$!
run_method nevpt2 1 4 & p_nevpt2=$!
run_method mrci   1 4 & p_mrci=$!

for p in $p_uhf $p_mp2 $p_ccsdt $p_casscf $p_nevpt2 $p_mrci; do
  wait "$p" || rc_master=1
done
echo "ALL DONE rc=$rc_master"
