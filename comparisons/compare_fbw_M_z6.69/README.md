# compare_fbw_M_z6.69

z = 6.69 (a = 0.130). BPASS M_max 100 vs 300 twins (pair M; smooth SF, closest MEGATRON recipe: smooth): density-dependent
eps (0.03 (n/n_th)^0.5 <= 0.1), mechanical FB, 4x SN, t_SNII 10 Myr, eta_SNII 0.2, production hydro, SSP tables from
`src_files/`. Numbers: `../fbw_trend/fbtrend_a0.130.txt`.

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|---|
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp100_h2` | 8.61e7 | 1.26e53 | 0.273 / 0.280 | 3.4e52 | 0.065 |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | 8.59e7 | 1.75e53 | 0.357 / 0.377 | 6.2e52 | **0.130** |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp100_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx4_ssp100` | `halos_iter0050693.txt` |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx4_ssp300` | `halos_iter0049140.txt` |
