# compare_fbw_A_z5.00

z = 5.00 (a = 0.167). FB campaign series A (smooth SF; closest MEGATRON recipe: smooth): density-dependent eps (0.03 (n/n_th)^0.5 <= 0.1),
mechanical FB, SN 2x / 4x / 10x, t_SNII 10 Myr, eta_SNII 0.2, production hydro, BPASS SSP M_max 300. Run end: all three runs finished (a = 1/6). A 2x reaches near-overlap.
Numbers: `../fbw_trend/fbtrend_a0.167.txt`.

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|---|
| `eps0.03n0.5c0.1_mech_snx2_t10_ssp300_h2` | 1.38e+09 | 2.77e+54 | 0.061 / 0.090 | 1.7e+53 | 0.9580 |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | 2.65e+08 | 3.94e+53 | 0.170 / 0.202 | 6.7e+52 | 0.4139 |
| `eps0.03n0.5c0.1_mech_snx10_t10_ssp300_h2` | 5.89e+07 | 4.43e+52 | 0.351 / 0.311 | 1.5e+52 | 0.1380 |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.03n0.5c0.1_mech_snx2_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx2_ssp300` | `halos_iter0066861.txt` |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx4_ssp300` | `halos_iter0068658.txt` |
| `eps0.03n0.5c0.1_mech_snx10_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx10_ssp300` | `halos_iter0073519.txt` |
