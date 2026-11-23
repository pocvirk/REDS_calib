# compare_fbw_B_z9.00

z = 9.00 (a = 0.100). FB campaign series B (bursty SF; closest MEGATRON recipe: bursty, also high eps): eps 0.3, n_th 10, mechanical FB,
SN 2x / 5x / 10x, t_SNII 3 Myr, eta_SNII 0.2, production hydro, BPASS SSP M_max 300.
Numbers: `../fbw_trend/fbtrend_a0.100.txt`.

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|---|
| `eps0.3_n10_mech_snx10_t3_ssp300_h2` | 1.29e+07 | 4.53e+52 | 0.306 / 0.209 | 1.4e+52 | 0.0109 |
| `eps0.3_n10_mech_snx2_t3_ssp300_h2` | 6.56e+07 | 3.61e+53 | 0.071 / 0.050 | 2.6e+52 | 0.0062 |
| `eps0.3_n10_mech_snx5_t3_ssp300_h2` | 2.02e+07 | 8.88e+52 | 0.144 / 0.118 | 1.3e+52 | 0.0078 |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.3_n10_mech_snx10_t3_ssp300_h2` | `reio_v2/h2_eps0.3_mech_n10_snx10_t3_ssp300` | `halos_iter0039787.txt` |
| `eps0.3_n10_mech_snx2_t3_ssp300_h2` | `reio_v2/h2_eps0.3_mech_n10_snx2_t3_ssp300` | `halos_iter0030445.txt` |
| `eps0.3_n10_mech_snx5_t3_ssp300_h2` | `reio_v2/h2_eps0.3_mech_n10_snx5_t3_ssp300` | `halos_iter0033873.txt` |
