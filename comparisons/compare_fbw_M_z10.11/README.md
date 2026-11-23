# compare_fbw_M_z10.11

z = 10.11 (a = 0.090). BPASS M_max 100 vs 300 twins (FB campaign, pair M): density-dependent eps (0.03 (n/n_th)^0.5 <= 0.1,
n_th 0.1), mechanical FB, 4x SN (8e49 erg/Msun), t_SNII 10 Myr, eta_SNII 0.2, production hydro; single-burst (SSP)
emissivity tables from `src_files/`. UV magnitudes from each run's own table. Numbers: `../fbw_trend/fbtrend_a0.090.txt`.

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|---|
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp100_h2` | 1.45e7 | 2.9e52 | 0.52 / 0.43 | 1.5e52 | 0.0145 |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | 1.37e7 | 3.8e52 | 0.52 / 0.44 | 2.0e52 | 0.0256 |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp100_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx4_ssp100` | `halos_iter0025905.txt` |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx4_ssp300` | `halos_iter0024474.txt` |
