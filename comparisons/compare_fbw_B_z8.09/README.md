# compare_fbw_B_z8.09

z = 8.09 (a = 0.110). FB campaign series B (bursty SF; closest MEGATRON recipe: bursty, also high eps): eps 0.3, n_th 10, mechanical FB,
SN 2x / 5x / 10x, t_SNII 3 Myr, eta_SNII 0.2, production hydro, BPASS SSP M_max 300. The 10x run is not at this z yet.
Numbers: `../fbw_trend/fbtrend_a0.110.txt`.

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|---|
| `eps0.3_n10_mech_snx2_t3_ssp300_h2` | 1.35e+08 | 4.48e+53 | 0.019 / 0.016 | 8.6e+51 | 0.0112 |
| `eps0.3_n10_mech_snx5_t3_ssp300_h2` | 3.92e+07 | 1.24e+53 | 0.136 / 0.127 | 1.7e+52 | 0.0124 |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.3_n10_mech_snx2_t3_ssp300_h2` | `reio_v2/h2_eps0.3_mech_n10_snx2_t3_ssp300` | `halos_iter0036849.txt` |
| `eps0.3_n10_mech_snx5_t3_ssp300_h2` | `reio_v2/h2_eps0.3_mech_n10_snx5_t3_ssp300` | `halos_iter0041115.txt` |
