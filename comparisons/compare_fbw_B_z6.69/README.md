# compare_fbw_B_z6.69

z = 6.69 (a = 0.130). FB campaign series B (bursty SF; closest MEGATRON recipe: bursty, also high eps): eps 0.3, n_th 10, mechanical FB,
SN 2x / 5x / 10x, t_SNII 3 Myr, eta_SNII 0.2, production hydro, BPASS SSP M_max 300. The 10x run is not at this z yet.
Numbers: `../fbw_trend/fbtrend_a0.130.txt`.

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|---|
| `eps0.3_n10_mech_snx2_t3_ssp300_h2` | 4.41e+08 | 7.14e+53 | 0.021 / 0.019 | 1.5e+52 | 0.0442 |
| `eps0.3_n10_mech_snx5_t3_ssp300_h2` | 1.08e+08 | 2.17e+53 | 0.113 / 0.057 | 2.4e+52 | 0.0348 |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.3_n10_mech_snx2_t3_ssp300_h2` | `reio_v2/h2_eps0.3_mech_n10_snx2_t3_ssp300` | `halos_iter0049000.txt` |
| `eps0.3_n10_mech_snx5_t3_ssp300_h2` | `reio_v2/h2_eps0.3_mech_n10_snx5_t3_ssp300` | `halos_iter0056454.txt` |
