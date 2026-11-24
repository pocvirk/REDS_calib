# compare_fbw_M_z5.90

z = 5.90 (a = 0.145). BPASS M_max 100 vs 300 twins (pair M; smooth SF, closest MEGATRON recipe: smooth): density-dependent
eps (0.03 (n/n_th)^0.5 <= 0.1), mechanical FB, 4x SN, t_SNII 10 Myr, eta_SNII 0.2, production hydro, SSP tables from
`src_files/`. Nearest snapshot to z = 6.
Numbers: `../fbw_trend/fbtrend_a0.145.txt`.

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|---|
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp100_h2` | 1.45e+08 | 1.5e+53 | 0.220 / 0.233 | 3.3e+52 | 0.1204 |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | 1.41e+08 | 1.89e+53 | 0.266 / 0.271 | 5e+52 | 0.2312 |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp100_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx4_ssp100` | `halos_iter0059000.txt` |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx4_ssp300` | `halos_iter0057425.txt` |
