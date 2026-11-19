# Calibration journal (newest first)

Recipe labels as in the README: `<SF>_<FB>[_snx<k>]_t<t_SNII>[_<hydro>]`.

## 2026-11-19 (later): production hydro vs 1st order at z = 8.09
`comparisons/compare_h2_z8.09`
- Same 6 runs at a = 0.110:

  | recipe | x_HII (vol) 1st / h2 | global f_esc ray-traced / M1, 1st -> h2 | M* in halos 1st / h2 |
  |---|---|---|---|
  | eps0.03n0.5c0.1_th_t10 | 0.064 / 0.102 | 0.049 / 0.069 -> 0.111 / 0.132 | 2.6e8 / 3.0e8 |
  | eps0.03_mech_snx2_t10 | 0.013 / 0.032 | 0.076 / 0.082 -> 0.118 / 0.115 | 8.5e7 / 9.8e7 |
  | eps0.3_mech_n10_snx2_t3 | 0.018 / 0.035 | 0.047 / 0.033 -> 0.158 / 0.097 | 9.2e7 / 1.1e8 |

- The h2 f_esc of the mechanical recipes falls between z = 9 and 8.09 (0.18 -> 0.12, 0.24 -> 0.16), so the h2/1st ratio
  drops from 2-5x to 1.5-3x. The thermal density-dependent recipe holds at 0.11. x_HII stays ~2x higher with h2. Only
  the thermal density-dependent recipe is on track (x_HII 0.10 at z = 8.1, Hoag+19 point 0.12 at z = 7.6); the constant-eps
  mechanical ones are 3x lower.

## 2026-11-19: production hydro vs 1st order at z = 9; halo porosity maps
`comparisons/compare_h2_z9`, `maps/porosity_z9`
- Same snapshot (a = 0.100) for the 1st-order and h2 versions of 3 recipes:

  | recipe | hydro | x_HII (vol) | global f_esc ray-traced / M1 |
  |---|---|---|---|
  | eps0.03n0.5c0.1_th_t10 | 1st / h2 | 0.028 / 0.048 | 0.055 / 0.064 -> 0.110 / 0.135 |
  | eps0.03_mech_snx2_t10 | 1st / h2 | 0.007 / 0.019 | 0.079 / 0.086 -> 0.179 / 0.174 |
  | eps0.3_mech_n10_snx2_t3 | 1st / h2 | 0.010 / 0.021 | 0.042 / 0.031 -> 0.235 / 0.158 |

- Same stellar masses and UV LFs; CSFRD of h2 a bit higher at z > 11, converged by z ~ 9 (top of the Bouwens band).
- Halo maps (3 most massive halos, 2-3.3e9 Msun): same gas mass within R200, same volume fraction of diffuse gas, but in
  h2 the HI is broken into clumps / filaments with clear sightlines (several separate SN bubbles inside R200), where 1st
  order gives a smooth HI envelope. Sky fraction with transmission > 0.1 rises from 0-0.15 to 0.2-0.7 in 7 of 9 halo/recipe
  pairs. The bursty n10 recipe is on/off halo by halo (one halo between bursts has f_esc = 0).
- For constant eps, even open directions transmit only 10-46%: the rest is absorbed next to the young stars. Only the
  bursty n10 recipe clears its birth regions (transmission up to 0.98).

## 2026-11-18: t_SNII as a free parameter; t_SNII scan launched
- At 150-250 pc much of the physics that sets f_esc is unresolved or missing (delayed / multiple SNe, pre-SN feedback,
  cosmic rays, porosity / Kimm+15 mass loading). Decision (PO): tune one effective parameter that carries it, not
  necessarily at a physically defensible value: **t_SNII**.
- Isolated z = 7 discs (`discs_z7/z7_tsn.png`): at fixed SN energy, t_SNII = 10 Myr gives a higher f_esc than 3 Myr (b = 2:
  M1 f_esc 0.80 vs 0.24 at 1e9 Msun, 0.30 vs 0.14 at 1e10); t10 quenches SF at boost >= 4. Delayed feedback makes SF
  bursty and the blow-out coherent.
- **Hidden parameter**: all `eps0.3_mech_n10*` runs had t_SNII = 3 Myr (all others 10). Plot labels now carry FB type and t_SNII.
- Launched (h2): `h2_eps0.03_mech_snx2_t3`, `_t20` (vs t10), `h2_eps0.3_mech_n10_snx2_t10` (vs t3), and
  `h2_eps0.03n0.5c0.1_mech_snx2` (density-dependent eps + mechanical FB, 2x SN).

## 2026-11-18: z = 5 results (1st-order calibration runs; dyablo production vs RAMSES)
`comparisons/compare_cf_z5`, `compare_epsn_z5`, `compare_cmp_ramses_z5`
- dyablo production hydro reproduces RAMSES-RT galaxies at matched settings (eps 0.01, thermal): CSFRD, SMHM and UV LF
  overlap; x_HII 0.31 (dyablo) vs 0.43 (RAMSES). Both ~0.5 dex above the Bouwens CSFRD at eps = 0.01.
- Constant-eps mechanical recipes sit on the Bouwens CSFRD but reionize far too late (x_HII 0.09-0.34 at z = 5).
- eps0.03n0.5c0.1_th_t10 (density-dependent eps): x_HII 0.88 at z = 5, but too many stars (SMHM ~3e8 at 1e10 Msun).
- CoDa III-like (dx 11.6 ckpc): x_HII 0.72 at z = 5; late. Suspects: c_rad 0.01 c (CoDa III used full c), small box.
- f_esc gaps in the plots: mass bins with fewer than 3 halos emitting ionizing photons (halos < 1e8 Msun mostly starless:
  atomic-cooling limit, no H2 cooling).

## 2026-11-14 to 17: hydro validation (`idealised_test_cases/`, `reports/2026-11-17_hydro_validation.pdf`)
- 1st-order dyablo over-heated pre-shock gas and under-produced shocks in small halos; RAMSES pressure_fix (any beta) and
  Tep-style entropy switch (eta 0.1) kill shock heating in moving frames (Galilean pancake) and leave < 1e8 Msun halos
  cold. Production recipe: RK2 + minmod, no dual-energy switch, e_int-conserving remap, RAMSES-like refinement,
  smallp 1e-50, Compton cooling, adiabat fallback for negative pressure -> passes all 4 tests (`h2_` runs).
