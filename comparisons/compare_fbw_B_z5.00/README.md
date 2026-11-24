# compare_fbw_B_z5.00

z = 5.00 (a = 0.167). FB campaign series B (bursty SF; closest MEGATRON recipe: bursty, also high eps): eps 0.3, n_th 10, mechanical FB,
SN 2x / 5x / 10x, t_SNII 3 Myr, eta_SNII 0.2, production hydro, BPASS SSP M_max 300. Run end (a = 1/6) for 2x and 5x; 10x still running (z = 5.04), the watcher redoes this set with 10x when it ends.
Numbers: `../fbw_trend/fbtrend_a0.167.txt`.

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|---|
| `eps0.3_n10_mech_snx2_t3_ssp300_h2` | 1.89e+09 | 4.34e+54 | 0.012 / 0.007 | 5.1e+52 | 0.1162 |
| `eps0.3_n10_mech_snx5_t3_ssp300_h2` | 3.68e+08 | 6.45e+53 | 0.027 / 0.057 | 1.8e+52 | 0.0907 |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.3_n10_mech_snx2_t3_ssp300_h2` | `reio_v2/h2_eps0.3_mech_n10_snx2_t3_ssp300` | `halos_iter0070026.txt` |
| `eps0.3_n10_mech_snx5_t3_ssp300_h2` | `reio_v2/h2_eps0.3_mech_n10_snx5_t3_ssp300` | `halos_iter0084220.txt` |
