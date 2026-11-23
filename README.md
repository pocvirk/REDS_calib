# REDS_calib: calibration of the REDS reionization simulations (dyablo)

Figures, configurations and notes from the calibration of the sub-grid star formation (SF) and supernova (SN) feedback
for the REDS simulations (dyablo, GPU AMR + M1 radiative transfer) on Frontier. Goal: a recipe that, at ~150-250 pc
resolution, gives the observed cosmic SFR density / UV LF / stellar-to-halo mass relation **and** reionizes the
Universe by z ~ 5.5-6.

Start with [`JOURNAL.md`](JOURNAL.md) (dated findings), then the comparison figures in [`comparisons/`](comparisons/).

## Layout

| folder | content |
|---|---|
| `comparisons/<set>/` | multi-run overlays at one redshift (`compare_dashboard.py`): CSFRD, UV LF, SMHM + f_esc vs halo mass, x_HII(z), x_HI, Gamma, tau, HMF, flows. `dashboard_compare.pdf` = all panels in one file. Each set has a `README.md` listing its runs and labels |
| `dashboards/<run>/` | single-run dashboard (`run_dashboard.py`); galaxy plots carry the redshift in the file name, IGM plots are the full history |
| `idealised_test_cases/` | the 4 hydro validation tests (pancake, Galilean pancake, adiabatic cosmo T_halo vs T_vir, single SN): figures, reference values, pass criteria, setups |
| `maps/` | halo maps (gas / HI columns, temperature, escape sky maps), e.g. `porosity_z9/` |
| `discs_z7/` | isolated z = 7 disc tests (1e9 - 1e10 Msun halos, 195 pc): SF and f_esc vs SN energy and t_SNII |
| `inis/boxB/` | dyablo `.ini` of every cosmological run (header comment = what changed vs which parent, and why) |
| `inis/ramses_box/` | RAMSES-RT namelists of the twin runs (same ICs) |
| `inis/disc_z7/` | disc test templates + generator |
| `tables/averages/` | IGM history per run (`iter aexp z xHII_V xHII_M nH xnH Gamma_V Gamma_ion f_ion S T`) for replotting |
| `scripts/` | analysis / job scripts that are not in [dyablo_tools](https://github.com/pocvirk/dyablo_tools) |
| `reports/` | short PDF reports |
| `sync.sh` | refreshes this repo from the Frontier run directories |

## Setup

**Cosmological box ("boxB")**, all runs unless stated otherwise:

| | |
|---|---|
| volume | 4 cMpc/h (5.96 cMpc), 256^3 DM particles (m_DM ~ 4e5 Msun) |
| cosmology | H0 = 67.06, Om = 0.3175, Ob = 0.049, sigma_8 = 0.8344, n_s = 0.9624 (Planck-like) |
| ICs | grafic, z = 100, `ics/boxB_4mpc_256/level_008` (same ICs in dyablo and RAMSES) |
| AMR | levels 6-10, blocks of 4^3 -> dx_min = 1.46 ckpc (146 pc physical at z = 9, 240 pc at z = 5); quasi-Lagrangian refinement |
| RT | M1, 1 group, c_rad = 0.01 c, BPASS v2.2.1 binary Kroupa M_max = 100 Msun emissivity (5 Myr constant-SFR particles, Z = 0.001, to 200 Myr; `_ssp<M>` runs: single-burst tables with M_max = 100 / 300, `src_files/`), black body 5e4 K opacity, H chemistry (Chem_Ramses) |
| stars | particle mass 1e4 Msun; Schmidt law rho_dot = eps rho / t_ff above n_th |
| SN | eta_SNII = 0.2, E_SNII = 1e51 erg, M_SNII = 10 Msun (1 SN / 50 Msun formed = 2e49 erg/Msun; `snx<k>`: k x that; MEGATRON fiducial 0.85e49, Bursty 4.2e49), t_SNII = 10 Myr unless stated |
| feedback | thermal (default), Kimm & Cen 2014 mechanical (`mech`), or delayed cooling (`dc`) |
| hydro | `h2_` runs: validated production hydro (RK2 + minmod, e_int-conserving remap, RAMSES-like refinement, smallp 1e-50, Compton cooling, adiabat fallback for negative pressure). Older runs: 1st order (see caveat below) |
| z_end | 5 |

**RAMSES-RT twins** (`*_RAMSES_*`, `inis/ramses_box/`): same ICs, SF/FB/RT settings matched to the dyablo
`eps0.01` run. dyablo production hydro reproduces their galaxies (CSFRD, SMHM, UV LF) at z = 5.

**Isolated discs** (`discs_z7/`): z = 7 halos of 1e9, 3e9, 1e10 Msun, dx_min = 195 pc, mechanical feedback,
eps = 0.03, n_th = 0.1; scans in SN energy (boost b = 1, 2, 4, 10) and t_SNII (3, 10 Myr).

**Analysis**: [dyablo_tools](https://github.com/pocvirk/dyablo_tools) `dashboard_dyablo_reio`: FoF halos (b = 0.15,
>= 20 particles), stars within R200, BPASS UV magnitudes, f_esc through R200 measured two ways: M1 flux through the
R200 shell, and ray-traced exp(-sigma N_HI) from every star to 1728 HEALPix points on the R200 sphere (photon-weighted).
Observations in the plots: Bouwens+14/15/16 (CSFRD, UV LF), Behroozi+19, Stefanon+21 (SMHM), Read+17, Planck tau,
x_HII constraints (Davies+18, Mason+18, Greig+17, Hoag+19).

## Run naming convention

Run names are built from tokens. **The `.ini` header is authoritative**; this table is the decoder.

| token | meaning | ini key |
|---|---|---|
| `eps<x>` | constant SF efficiency eps = x | `[star_formation] epsilon_star` |
| `eps<x>n0.5c<y>` | density-dependent eps = x (n/n_th)^0.5, capped at y | `epsilon_star_density_slope`, `epsilon_star_max` |
| `epsn<x>c<y>` | same, older name (slope 0.5 implicit) | |
| `n<x>` | SF density threshold n_th = x cm^-3 (absent: 0.1) | `density_threshold` |
| `mech` | mechanical SN feedback (absent: thermal) | `ParticleUpdate_feedback_mechanical` |
| `dc` | delayed cooling SN feedback | `ParticleUpdate_feedback_delayed_cooling` |
| `snx<k>` | k x more SNe per stellar mass (M_SNII = 10/k Msun), i.e. k x SN energy | `[star_feedback] M_SNII` |
| `t<x>` | t_SNII = x Myr (absent: 10 Myr) | `[star_feedback] t_SNII` |
| **exception** | **all `eps0.3_mech_n10*` runs without `t<x>` use t_SNII = 3 Myr** | |
| `h2_` | validated production hydro, frozen build `build_h2` | several |
| `cf_`, `chemfix` | fixed chemistry build (1st-order hydro) | build |
| `codalike` | CoDa III-like: dx_min 11.6 ckpc (8x coarser), SF only at overdensity > 50, eps 0.03 | several |
| `rk2`, `s1`, `ei`, `rr`, `cmp`, `pf`, `sp50`, `m2` | hydro-scan variants (RK2, minmod slopes, e_int remap, RAMSES refinement, Compton, pressure fix, smallp, finer refinement) | |
| `adi_` | adiabatic twin (no cooling, SF, FB, RT) | |
| `boxC_` | 8 cMpc/h box (512^3) | |
| `RAMSES_` | RAMSES-RT twin | |

**Hydro-order caveat**: every run without `h2_`, `rk2` or `s1` in its name is 1st-order hydro. Compare it with other
1st-order runs, not with `h2_` runs or RAMSES at face value (at z = 9 the production hydro gives 2-5x higher f_esc at
fixed recipe, see `JOURNAL.md`).

**Plot labels** (from 2026-11-18 on) spell out the full recipe read from the ini, not the run name:
`<SF>_<FB: th|mech|dc>[_snx<k>]_t<t_SNII>[_<hydro>]`, e.g. `eps0.3_mech_n10_snx2_t3_h2`. Older comparison sets
(`compare_z7.7`, `compare_z8.09`, `compare_codalike_z9`, `ramses_box_*`) use run names as labels.

## Run index (status 2026-11-23, 01:00 EST)

| run | hydro | SF | FB | status / role |
|---|---|---|---|---|
| `eps0.01`, `eps0.02`, `eps0.03` | 1st | eps const, n_th 0.1 | thermal | first eps scan (to z 6.4-7) |
| `eps0.03_mech`, `eps0.03_mech_snx2`, `eps0.3_mech_n10` | 1st | const | mech | first FB scan |
| `eps0.01_chemfix`, `eps0.01_oldchem` | 1st | 0.01 | thermal | chemistry fix test |
| `codalike_chemfix` | 1st | 0.03, Delta > 50 | thermal | CoDa III-like; z = 5, x_HII 0.72 |
| `cf_eps0.03_mech_snx2`, `_snx3` | 1st | 0.03 | mech, 2x / 3x SN, t10 | z = 5, x_HII 0.20 (snx2) |
| `cf_eps0.03_dc_snx2` | 1st | 0.03 | delayed cooling, 2x SN, t10 | z = 5 |
| `cf_eps0.3_mech_n10_snx2` | 1st | 0.3, n_th 10 | mech, 2x SN, **t3** | bursty; z = 5, x_HII 0.34 |
| `epsn0.03c0.1_chemfix` | 1st | 0.03 (n/n_th)^0.5 <= 0.1 | thermal, t10 | z = 5, x_HII 0.88 |
| `eps0.01_*` hydro scan | various | 0.01 | thermal | dyablo vs RAMSES hydro study |
| `eps0.01_rk2_ei_rr_cmp` | production | 0.01 | thermal, t10 | baseline matched to `RAMSES_eps0.01_s1_b0_ics`; galaxies match RAMSES at z = 5 |
| `h2_epsn0.03c0.1` | **h2** | 0.03 (n/n_th)^0.5 <= 0.1 | thermal, t10 | **done (z = 5), x_HII 0.96**; `compare_h2_z5` |
| `h2_eps0.03_mech_snx2` | **h2** | 0.03 | mech, 2x SN, t10 | running (z ~ 5.8) |
| `h2_eps0.3_mech_n10_snx2` | **h2** | 0.3, n_th 10 | mech, 2x SN, **t3** | running (z ~ 6.3) |
| `h2_eps0.03n0.5c0.1_mech_snx2` | **h2** | 0.03 (n/n_th)^0.5 <= 0.1 | mech, 2x SN, t10 | running (z ~ 6.7) |
| `h2_eps0.03_mech_snx2_t3`, `_t20` | **h2** | 0.03 | mech, 2x SN, t_SNII 3 / 20 | t_SNII scan, running (z ~ 6.4 / 7.2) |
| `h2_eps0.3_mech_n10_snx2_t10` | **h2** | 0.3, n_th 10 | mech, 2x SN, t10 | t_SNII scan, running (z ~ 9.9) |
| `h2_eps0.03n0.5c0.1_mech_snx4_ssp100`, `_ssp300` | **h2** | 0.03 (n/n_th)^0.5 <= 0.1 | mech, 4x SN, t10 | BPASS SSP M_max 100 vs 300 (`src_files/`); running (z ~ 13.5 / 13.3) |
| `h2_eps0.03n0.5c0.1_mech_snx2_ssp300`, `_snx10_ssp300` | **h2** | 0.03 (n/n_th)^0.5 <= 0.1 | mech, 2x / 10x SN, t10, M_max 300 | FB campaign series A; running (z ~ 13.2 / 13.9) |
| `h2_eps0.3_mech_n10_snx{2,5,10}_t3_ssp300` | **h2** | 0.3, n_th 10 | mech, 2x / 5x / 10x SN, t3, M_max 300 | FB campaign series B; running (z ~ 13.9 / 14.5 / 15.1) |

## Updating

On Frontier: `./sync.sh && git add -A && git commit -m "<what>" && git push`. Add new comparison sets / maps to
`sync.sh`, a line to `JOURNAL.md`, a row to the run index, and a `README.md` in each new comparison folder.
