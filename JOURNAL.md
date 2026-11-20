# Calibration journal (newest first)

Recipe labels as in the README: `<SF>_<FB>[_snx<k>]_t<t_SNII>[_<hydro>]`.

## 2026-11-20 (later): MEGATRON feedback levers (Choustikov et al. 2026, arXiv:2611.15931; Katz et al. arXiv:2411.07282)
- MEGATRON (RAMSES-RTZ, ~5 pc, zoom on a Milky Way progenitor): the model with the **fewest** galaxies (100% eps_ff in
  lower-density gas + hypernovae) reionizes fastest (volume almost fully ionized at z ~ 8.5, vs 1/3 for the "Efficient"
  model, which has 10x more UV-bright galaxies). Their f_esc rises faster than 1/M*; ours does not
  (d log f_esc / d log M* = -0.8 ray-traced, -0.5 M1, thermal vs mechanical at z = 9), so in our boxes more stars still
  means more ionization.
- Their key timescale: burst -> efficient LyC escape = 2.5 Myr (HN), 4 Myr (Bursty, 5x E_SN), 11 Myr (Efficient). Late
  escape is wasted ("remnant leakers": high f_esc, no young stars). Our global f_esc is photon-weighted, so it already
  discounts them. At 150 pc the birth cloud is one cell and its photons are injected at full luminosity (implicit
  birth-cloud f_esc = 1): resolution favours high-M* runs.
- **Levers** (specific SN energy, eta E_SNII / M_SNII; E_SNII and M_SNII are degenerate in dyablo):

  | model | erg per Msun formed | timing |
  |---|---|---|
  | MEGATRON fiducial (Kroupa, 1e51 per 8-25 Msun star = 1 SN / 115 Msun) | 0.85e49 | individual SNe, ~7-40 Myr |
  | REDS base (eta 0.2, M_SNII 10) | 2e49 | all at t_SNII |
  | REDS `snx2` (most runs) | 4e49 | all at t_SNII |
  | MEGATRON Bursty (5e51 per SN) | 4.2e49 | ~7-40 Myr |
  | MEGATRON HN (>= 25 Msun stars, up to 10x E_SN, mass/Z dependent fraction) | <~3e49 | from ~3.5 Myr |
  | REDS `snx5` (PO: "E_SN up to 10e51", exploration beyond MEGATRON) | 1e50 | all at t_SNII |

  Our `t3` runs are an extreme early-energy (HN-like) case. MEGATRON's space maps onto our (snx, t_SNII) plane.
- **IMF upper mass**: MEGATRON uses BPASS Kroupa binary with M_max = 300 Msun (BPASS `imf135_300`); REDS uses
  M_max = 100 Msun (`cstSFR_5Myr_BPASSv2.2.1_kroupa_binary_MMax=100`, from dashboard_rc). Decision (PO): move to
  M_max = 300 for new runs. No M_max = 300 table exists on disk (dashboard_rc has M_max = 100 only; the RAMSES SED.zip has
  BC03 only; RAMSES `utils/py/sed_utils.py` converts BC03 / Starburst99, not BPASS): needs the BPASS v2.2.1 `imf135_300`
  binary ionizing tables.
- Next diagnostic: f_esc and escaping photon rate vs star-particle age (our own burst -> escape delay).

## 2026-11-20: t_SNII scan at z = 9 (production hydro)
`comparisons/compare_tsn_z9`
- Same snapshot (a = 0.100):

  | recipe | x_HII (vol) | global f_esc ray-traced / M1 | M* in halos [Msun] | Ndot [ph/s] |
  |---|---|---|---|---|
  | eps0.03_mech_snx2_t3_h2 | 0.015 | 0.248 / 0.168 | 4.5e7 | 0.96e53 |
  | eps0.03_mech_snx2_t10_h2 | 0.019 | 0.179 / 0.174 | 5.1e7 | 1.21e53 |
  | eps0.03_mech_snx2_t20_h2 | 0.025 | 0.206 / 0.211 | 6.7e7 | 1.35e53 |
  | eps0.03n0.5c0.1_mech_snx2_t10_h2 | 0.022 | 0.248 / 0.231 | 4.7e7 | 0.87e53 |
  | eps0.03n0.5c0.1_th_t10_h2 | 0.048 | 0.110 / 0.135 | 1.3e8 | 3.6e53 |

- In the box, a longer t_SNII mainly lets more stars form before the first SN (CSFRD of t20 is ~0.15 dex higher at z > 10;
  SMHM up at 1e9 Msun); f_esc moves little and not monotonically (unlike the isolated discs, where t10 raised f_esc 2-3x).
  x_HII rises 1.7x from t3 to t20, still far below the thermal density-dependent recipe.
- Density-dependent eps + mechanical FB: f_esc as high as the best constant-eps case, but 2.8x fewer stars than with
  thermal FB, so half the x_HII. Thermal FB with density-dependent eps remains the only recipe on track at z = 9.

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
