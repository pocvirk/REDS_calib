# Idealised hydro tests (dyablo non-regression suite)

Four tests that validate the hydro scheme in the cosmological-reionization regime. Each targets a failure we actually
hit in November 2026. **Run them on every new dyablo version** (CEA release, a colleague's branch) before calibration or
production. The production configuration they validate: `HydroUpdate_RK2_ion` (SSP-RK2, minmod, cfl 0.8, no dual-energy
switch), `[amr] remap = MapUserData_mean_eint`, `mass_refine_ramses = true`, `smallp = 1e-50`, `[rad] compton = true`,
`negative_p_fallback = adiabat`. Full description in `reports/2026-11-17_hydro_validation.pdf`.

| # | folder | test | what it catches | RAMSES twin |
|---|---|---|---|---|
| 1 | `t1_pancake/` | Einstein-de Sitter Zel'dovich pancake at rest (1D, Tep et al. App. B) | shock heating, adiabatic infall, heating by coarsening, 1st-order heating | yes |
| 2 | `t2_pancake_galilean/` | same pancake with a uniform transverse velocity (504-3363 km/s) | frame-dependent heating from a per-step dual-energy switch (entropy eta > 0, RAMSES pressure_fix beta > 0) | yes |
| 3 | `t3_adiabatic_cosmo/` | adiabatic cosmological twin of the boxB runs (DM + gas, no cooling/RT/SF), z = 9 | halo virialization (T_halo ~ T_vir), baryon fractions, IGM shock heating, refinement criterion | yes |
| 4 | `t4_single_sn/` | one SN (1e51 erg) in a uniform medium, thermal and mechanical feedback, cooling | energy / momentum lost at SN shocks by the negative-pressure floor or a switch | not yet |

`setup/` holds the inis/namelists, IC generators, job and analysis scripts (tests 1 and 2 share `t1_pancake/setup/`:
the boosted runs are the `*_vy15k*` files with `make_ic.py 64 VY`).

## 1. Pancake at rest
L = 64 Mpc/h, Omega_m = Omega_b = 1, gas only, caustic at z_c = 1, from z_i = 50, 64^3 + 2 refinement levels.
Figures: `eds_z0.png`, `eds_z2.png` (rho, v, T, T/T_analytic vs Tep et al. eqs. B1-B4, AMR level), `eds_scan_*` (scheme scan), `eds_mesh_z0.png`.

| run (z = 0) | T_max | rho_max | shocked mass (a = 0.667) |
|---|---|---|---|
| dyablo production | 9.7e7 K | 39 | 0.94 |
| dyablo + Tep entropy eta 0.1 | 9.1e7 K | 39 | 0.73 |
| RAMSES (no fix) | 8.8e7 K | 43 | 0.91 |
| strong-shock estimate | 6-8e7 K | | |

**Pass**: T_max 6e7-1.2e8 K, rho_max 35-45, shocked fraction > 0.85, no pre-shock gas above 1e4 K.

## 2. Galilean pancake
Test 1 plus a uniform v_y (decays as 1/a: 504, 1009, 2018, 3363 km/s at a = 0.58). The exact solution in x does not change.
Figures: `ladder_T.png` (T profiles along the boost ladder), `boost_rho.png`, `boost_T.png` (3363 km/s case).

| shocked mass fraction at boost [km/s] | 0 | 504 | 1009 | 2018 | 3363 |
|---|---|---|---|---|---|
| dyablo production (and adiabat fallback) | 0.94 | 0.94 | 0.94 | 0.94 | 0.95 |
| RAMSES no fix | 0.91 | 0.91 | 0.89 | 0.89 | 0.89 |
| dyablo + Tep entropy eta 0.1 | 0.73 | 0.44 | 0.00 | 0.00 | 0.00 |
| RAMSES pressure_fix beta 0.5 | 0.80 | 0.00 | 0.00 | 0.00 | 0.00 |

**Pass**: shocked fraction within 0.05 of the unboosted run at every boost. Shock heating that disappears with the boost
= a dual-energy switch is active (eta = 0.1 is a grid-frame Mach > 4 test).

## 3. Adiabatic cosmological twin (T_halo vs T_vir)
boxB ICs (4 Mpc/h, 256^3, z = 100), production hydro and refinement, no cooling / chemistry / RT / SF, analysed at z = 9;
halos from the RAMSES FoF catalogue, each run recentred on its own DM. T200 = mu m_p G M200 / (2 k R200).
Figures: `adiabatic_halos_a0.100*.png` (T(<R200)/T200 and f_gas vs mass), `adiabatic_phase_a0.100*.png` (phase diagram
vs the adiabat), `fix_profiles_a0.100.png`, `fix_maps_{small,medium,massive}_a0.100.png` (rho, T maps and profiles of
5.5e7, 5.5e8, 3.3e9 Msun halos). `_fb_rc` = negative-pressure fallback flavours, recentred.

| M200 [Msun] | median T/T200, f_gas/(Ob/Om): RAMSES | dyablo production | dyablo + Tep entropy |
|---|---|---|---|
| 3e7-1e8 | 1.39, 0.47 | 1.27, 0.45 | **0.01**, 0.65 |
| 1e8-3e8 | 1.23, 0.67 | 1.16, 0.65 | 0.81, 0.81 |
| 3e8-1e9 | 1.05, 0.81 | 0.99, 0.78 | 0.81, 0.88 |
| 1e9-1e10 | 0.90, 0.89 | 0.83, 0.84 | 0.72, 0.89 |

**Pass**: T/T200 within 15% of RAMSES and > 0.7 in every bin, f_gas within 10%, < 1% of void gas below 0.8x the adiabat.
T/T200 ~ 0 in small halos = missing shock heating (dual-energy switch).

## 4. Single SN in a uniform medium
One SN (1e51 erg, 10 Msun ejecta), uniform medium at ~1e4 K, primordial cooling, to 1 Myr; n_H = 1 (dx 2, 12.5, 50 pc)
and n_H = 100 (dx 0.3, 50 pc); thermal and mechanical feedback; negative-pressure flavours A (floor), B (adiabat
fallback, production), C (RAMSES pf beta 0), D (Tep entropy eta 0.1), E (entropy only where e_int < 0).
Figures: `fb_history.png` (radial momentum, kinetic and thermal energy vs time), `fb_slices.png` (T slices).

| setup | p_r at 1 Myr [Msun km/s], A thermal / mech | B/A | D/A |
|---|---|---|---|
| n_H 1, dx 2 pc | 3.38e5 / 3.30e5 | 1.035 / 1.024 | 1.045 / 1.027 |
| n_H 1, dx 12.5 pc | 2.95e5 / 3.38e5 | 1.000 | 1.007 / 1.001 |
| n_H 1, dx 50 pc | 1.53e5 / 5.05e5 | 1.000 | 1.000 |
| n_H 100, dx 0.3 pc | 1.18e5 / 1.14e5 | 1.050 / 1.020 | 1.056 / 1.019 |

**Pass**: momentum within 5% of the reference (same cfl) in every setup. Flavour differences are <= 5% and vanish at
smaller time steps; the time step itself matters more (resolved SN momentum -5 to -17% from cfl 0.8 to 0.1).
