# compare_fbw_M_z5.00

z = 5.00 (a = 0.167). BPASS M_max 100 vs 300 twins (pair M; smooth SF, closest MEGATRON recipe: smooth): density-dependent
eps (0.03 (n/n_th)^0.5 <= 0.1), mechanical FB, 4x SN, t_SNII 10 Myr, eta_SNII 0.2, production hydro, SSP tables from
`src_files/`. Run end (a = 1/6).
Numbers: `../fbw_trend/fbtrend_a0.167.txt`.

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|---|
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp100_h2` | 2.76e+08 | 2.86e+53 | 0.140 / 0.140 | 4e+52 | 0.2273 |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | 2.65e+08 | 3.94e+53 | 0.170 / 0.202 | 6.7e+52 | 0.4139 |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp100_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx4_ssp100` | `halos_iter0070294.txt` |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx4_ssp300` | `halos_iter0068658.txt` |
