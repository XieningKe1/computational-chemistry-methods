# H2^- (charge -1, doublet) def2-TZVPP PES scan — diagnostics

Generated from `data/h2m_pes.csv` and `data/h2m_occupations.csv`; raw ORCA outputs live in `runs/h2m/<method>/R<value>/`.

## Job status

All 48 jobs (6 methods × 8 R) terminated normally and contain `FINAL SINGLE POINT ENERGY`. No `.failed.out` files were produced; no retries were needed. Total wall time for the whole batch: **1 min 17 s** (22 concurrent ORCA processes max).

| method | R=0.6 | R=0.8 | R=1.0 | R=1.2 | R=1.5 | R=2.0 | R=2.5 | R=3.0 |
|---|---|---|---|---|---|---|---|---|
| UHF | OK | OK | OK | OK | OK | OK | OK | OK |
| MP2 | OK | OK | OK | OK | OK | OK | OK | OK |
| CCSD(T) | OK | OK | OK | OK | OK | OK | OK | OK |
| CASSCF | OK | OK | OK | OK | OK | OK | OK | OK |
| NEVPT2 | OK | OK | OK | OK | OK | OK | OK | OK |
| MRCI | OK | OK | OK | OK | OK | OK | OK | OK |

## Energies (Eh)

| R (Å) | UHF | MP2 | CCSD(T) | CASSCF | NEVPT2 | MRCI |
|---|---|---|---|---|---|---|
| 0.6 | -0.934317 | -0.971165 | -0.979462 | -0.933069 | -0.966218 | -0.979145 |
| 0.8 | -0.977755 | -1.015202 | -1.024296 | -0.976123 | -1.010539 | -1.023894 |
| 1.0 | -0.986566 | -1.023958 | -1.033808 | -0.984600 | -1.019752 | -1.033352 |
| 1.2 | -0.988117 | -1.024562 | -1.035040 | -0.985448 | -1.020944 | -1.034539 |
| 1.5 | -0.988296 | -1.022084 | -1.033385 | -0.983600 | -1.019481 | -1.032789 |
| 2.0 | -0.984874 | -1.014576 | -1.027004 | -0.976261 | -1.013187 | -1.026244 |
| 2.5 | -0.978266 | -1.005799 | -1.019093 | -0.966776 | -1.004905 | -1.018147 |
| 3.0 | -0.971787 | -0.998513 | -1.012426 | -0.958695 | -0.997767 | -1.011445 |

## ΔE vs CASSCF (Eh)

| R (Å) | UHF−CASSCF | NEVPT2−CASSCF | MRCI−CASSCF | MRCI−NEVPT2 |
|---|---|---|---|---|
| 0.6 | -0.001248 | -0.033149 | -0.046076 | -0.012927 |
| 0.8 | -0.001632 | -0.034416 | -0.047771 | -0.013355 |
| 1.0 | -0.001966 | -0.035153 | -0.048752 | -0.013599 |
| 1.2 | -0.002669 | -0.035496 | -0.049090 | -0.013595 |
| 1.5 | -0.004696 | -0.035881 | -0.049189 | -0.013308 |
| 2.0 | -0.008613 | -0.036926 | -0.049983 | -0.013058 |
| 2.5 | -0.011490 | -0.038129 | -0.051371 | -0.013242 |
| 3.0 | -0.013092 | -0.039072 | -0.052750 | -0.013678 |

**Ordering checks:** NEVPT2 < CASSCF at every R: **PASS** (ΔE from −0.0331 to −0.0391 Eh). MRCI < NEVPT2 at every R: **PASS** (ΔE from −0.0129 to −0.0137 Eh). CASSCF is consistently slightly *above* UHF (by 0.0012–0.0131 Eh); this is allowed by the plan and is not a failure. CAS(3,2) uses two common spatial orbitals for both spins, whereas UHF can use different alpha/beta spatial orbitals (the spin contamination reflected in S² > 0.75), which lowers the UHF energy.

## UHF ⟨S²⟩ vs R (identical reference values for MP2 and CCSD(T))

| R (Å) | ⟨S²⟩ |
|---|---|
| 0.6 | 0.754473 |
| 0.8 | 0.755273 |
| 1.0 | 0.754710 |
| 1.2 | 0.755706 |
| 1.5 | 0.764251 |
| 2.0 | 0.786138 |
| 2.5 | 0.806405 |
| 3.0 | 0.821141 |

⟨S²⟩(3.0)=0.821141 > ⟨S²⟩(1.5)=0.764251 > 0.75; growth 0.6→3.0 = **0.066668 > 0.02**. The increase is not strictly monotonic at the finest resolution: R=0.8 (0.755273) is 0.000563 above R=1.0 (0.754710). The explicit acceptance criteria are still met; the small dip is reported rather than smoothed.

## CASSCF active-space natural occupations

| R (Å) | occ1 | occ2 | deviation from {0,2} |
|---|---|---|---|
| 0.6 | 2.0000 | 1.0000 | 1.0000 |
| 0.8 | 2.0000 | 1.0000 | 1.0000 |
| 1.0 | 2.0000 | 1.0000 | 1.0000 |
| 1.2 | 2.0000 | 1.0000 | 1.0000 |
| 1.5 | 2.0000 | 1.0000 | 1.0000 |
| 2.0 | 2.0000 | 1.0000 | 1.0000 |
| 2.5 | 2.0000 | 1.0000 | 1.0000 |
| 3.0 | 2.0000 | 1.0000 | 1.0000 |

**Interpretation (honest):** the occupations are exactly 2.0 and 1.0 at *every* R. The CASSCF CI vector is a single configuration (`1.00000 [1]:21`) at every R, so the nroots=1 CASSCF(3,2) ground state is a single determinant in localized orbitals. The numerical criterion (at R >= 2.0 A at least one active occupation deviates from 0 or 2 by > 0.1) is satisfied because the singly occupied active orbital has occ=1.0 (deviation 1.0), but this is **not** fractional static correlation. The earlier pilot's 1.5/1.5 occupations came from state-averaged `nroots 2`; that is the average of two states and is not the ground state. No nroots=2 calculation was used in this scan.

## CSV row counts

- `data/h2m_pes.csv`: **48 data rows** + header; columns `method,R,energy,s2`; 24 rows have a null `s2` (CASSCF/NEVPT2/MRCI print no `<S**2>`).
- `data/h2m_occupations.csv`: **8 data rows** + header; columns `R,occ1,occ2,deviation_from_0_or_2`.

## Orbital continuity mechanism (what worked)

For each of CASSCF/NEVPT2/MRCI at R > 0.6 Å, the previous R point's `<method>.gbw` was copied to `start.gbw` and the input carried both `! <METHOD> def2-TZVPP TightSCF MORead` and `%moinp "start.gbw"`. Without the `MORead` keyword ORCA warns `MOInp is set but Guess=PModel. MOInp will be ignored!`; with it, all 21 continuity runs print `INITIAL GUESS: MOREAD`. Adjacent CASSCF energy changes are at most 0.0431 Eh (0.6→0.8 Å) and no root flip/red-flag jump (>0.05 Eh) occurred.

## ORCA quirks / notes

- `! UHF`, `! MP2`, `! CCSD(T)` (no `U` prefix) correctly treat the `* xyz -1 2` open-shell system; charge/multiplicity were kept on the `* xyz` line, never inside `%casscf`.
- CCSD(T) ran with `%pal nprocs 2`; the earlier pilot with nprocs 4 aborted in MDCI (`mdci_state.cpp`, pair-count/MPI issue). All 8 CCSD(T) points completed at nprocs 2.
- ORCA 6.1.1 does not print a block literally titled `Natural Orbital Occupation Numbers` for these CASSCF runs. The active-space natural occupations are the `OCC` column of the final `ORBITAL ENERGIES` table (and are confirmed by the `N(occ)=` line and the `DENSITY MATRIX` diagonal). The parser reads that table.
- CASPT2 was not run (known cleanup segfault for H2^-/CAS(3,2) in ORCA). `nroots 1` was used for all 24 CASSCF-family jobs.
- `FINAL SINGLE POINT ENERGY` is the ground-state energy in all runs: for CASSCF it equals `Final CASSCF energy`; for NEVPT2 it includes the NEVPT2 correction; for MRCI it is the MRCI energy. NEVPT2/MRCI also print CASSCF intermediate energies, which were not used in the CSV.
