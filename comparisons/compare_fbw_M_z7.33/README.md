# compare_fbw_M_z7.33

z = 7.33 (a = 0.120). BPASS M_max 100 vs 300 twins (pair M; smooth SF): density-dependent eps, mechanical FB, 4x SN, t_SNII 10 Myr,
eta_SNII 0.2, production hydro, SSP tables from `src_files/`.
Numbers: `../fbw_trend/fbtrend_a0.120.txt`.

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|---|
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp100_h2` | 5.6e+07 | 9.14e+52 | 0.317 / 0.278 | 2.9e+52 | 0.0410 |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | 5.64e+07 | 1.48e+53 | 0.407 / 0.359 | 6e+52 | 0.0786 |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp100_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx4_ssp100` | `halos_iter0044847.txt` |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx4_ssp300` | `halos_iter0043345.txt` |
