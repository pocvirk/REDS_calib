# compare_fbw_B_z7.33

z = 7.33 (a = 0.120). FB campaign series B (bursty SF; closest MEGATRON recipe: bursty, also high eps): eps 0.3, n_th 10, mechanical FB,
SN 2x / 5x / 10x, t_SNII 3 Myr, eta_SNII 0.2, production hydro, BPASS SSP M_max 300.
Numbers: `../fbw_trend/fbtrend_a0.120.txt`.

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|---|
| `eps0.3_n10_mech_snx2_t3_ssp300_h2` | 2.61e+08 | 9.14e+53 | 0.030 / 0.017 | 2.7e+52 | 0.0154 |
| `eps0.3_n10_mech_snx5_t3_ssp300_h2` | 6.9e+07 | 2.08e+53 | 0.064 / 0.034 | 1.3e+52 | 0.0228 |
| `eps0.3_n10_mech_snx10_t3_ssp300_h2` | 3.35e+07 | 1.01e+53 | 0.203 / 0.186 | 2e+52 | 0.0290 |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.3_n10_mech_snx2_t3_ssp300_h2` | `reio_v2/h2_eps0.3_mech_n10_snx2_t3_ssp300` | `halos_iter0042983.txt` |
| `eps0.3_n10_mech_snx5_t3_ssp300_h2` | `reio_v2/h2_eps0.3_mech_n10_snx5_t3_ssp300` | `halos_iter0048855.txt` |
| `eps0.3_n10_mech_snx10_t3_ssp300_h2` | `reio_v2/h2_eps0.3_mech_n10_snx10_t3_ssp300` | `halos_iter0056360.txt` |
