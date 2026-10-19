# CH4 single-point results — notes

All 20 calculations use the same Td geometry (r(C–H) = 1.087 Å, coordinates
`a = 0.6276 Å`), charge 0, multiplicity 1, ORCA 6.1.1, and
`%pal nprocs 4` / `%maxcore 2500`. QM methods use def2-TZVPP; B97-3c and
r2SCAN-3c use their built-in composite bases (verified in the outputs, see
below). xTB and GFN-FF carry no basis. Energies are the last
`FINAL SINGLE POINT ENERGY` in each `runs/ch4/<name>/<name>.out`.

## HF/def2-TZVPP HOMO–LUMO gap

From the `ORBITAL ENERGIES` table in `runs/ch4/hf/hf.out`:

| orbital | occupation | E (Eh) | E (eV) |
|---|---|---|---|
| HOMO (NO 4, t2) | 2.0000 | −0.545435 | −14.8420 |
| LUMO (NO 5, a1*) | 0.0000 | +0.149903 | +4.0791 |

- Gap in Eh: `0.149903 − (−0.545435) = 0.695338 Eh`
- Gap in eV: `0.695338 × 27.211386245988 = 18.9211 eV`
- Also consistent with the printed eV column: `4.0791 − (−14.8420) = 18.9211 eV`
- **HF HOMO–LUMO gap = 18.9211 eV** (≈ 0.6953 Eh)

## CASSCF(8,8)/def2-TZVPP natural-orbital occupation numbers

From `runs/ch4/casscf/casscf.out` (`%casscf nel 8 norb 8 mult 1 nroots 1 end`;
active orbitals are printed as natural orbitals, final printing iteration):

```
N(occ)=  1.98429 1.97895 1.97895 1.97895 0.01971 0.01971 0.01971 0.01971
```

Interpretation: four essentially doubly occupied active orbitals
(1.98429, and 1.97895 × 3) and four essentially empty ones
(0.01971 × 4); sum = 8.00000 electrons. The small active-space occupations
outside 0/2 reflect the weak static correlation of CH4 captured by CAS(8,8).
The final `ORBITAL ENERGIES` table rounds these to 1.9843, 1.9790 × 3 and
0.0197 × 4. CASSCF(8,8) total energy: −40.297162861153 Eh.

## 3c basis verification

- `runs/ch4/b973c/b973c.out`: `Your calculation utilizes the basis: def2-mTZVP`
  (no explicit basis keyword in the input).
- `runs/ch4/r2scan3c/r2scan3c.out`: `Your calculation utilizes the basis: def2-mTZVPP`
  (no explicit basis keyword in the input).

## Caveats

- xTB (GFN2-xTB, −4.175157467990 Eh) and GFN-FF (−0.630873896930 Eh) are
  force-field / semiempirical total energies and are **not** comparable with
  the QM total energies; they are listed in the CSV but must be excluded from
  any ΔE comparison against CCSD(T).
- All runs are closed-shell singlets, so the CSV `s2` column is empty (null).
- The CCSD(T)/def2-TZVPP reference energy is −40.438597868462 Eh, inside the
  required sanity window of −40.4 to −40.6 Eh.
