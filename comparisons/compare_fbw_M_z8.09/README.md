# compare_fbw_M_z8.09

z = 8.09 (a = 0.110). BPASS M_max 100 vs 300 twins (pair M; smooth SF): density-dependent eps, mechanical FB, 4x SN,
t_SNII 10 Myr, eta_SNII 0.2, production hydro, SSP tables from `src_files/`. Numbers: `../fbw_trend/fbtrend_a0.110.txt`.

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|---|
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp100_h2` | 3.66e7 | 5.63e52 | 0.43 / 0.43 | 2.4e52 | 0.029 |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | 3.53e7 | 7.90e52 | 0.48 / 0.48 | 3.8e52 | **0.054** |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp100_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx4_ssp100` | `halos_iter0038787.txt` |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx4_ssp300` | `halos_iter0037295.txt` |
