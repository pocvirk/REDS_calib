# compare_fbw_A_z6.69

z = 6.69 (a = 0.130). FB campaign series A (smooth SF; closest MEGATRON recipe: smooth): density-dependent eps (0.03 (n/n_th)^0.5 <= 0.1),
mechanical FB, SN 2x / 4x / 10x, t_SNII 10 Myr, eta_SNII 0.2, production hydro, BPASS SSP M_max 300.
Numbers: `../fbw_trend/fbtrend_a0.130.txt`.

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|---|
| `eps0.03n0.5c0.1_mech_snx2_t10_ssp300_h2` | 2.99e+08 | 7.37e+53 | 0.152 / 0.221 | 1.1e+53 | 0.3335 |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | 8.59e+07 | 1.75e+53 | 0.357 / 0.377 | 6.2e+52 | 0.1302 |
| `eps0.03n0.5c0.1_mech_snx10_t10_ssp300_h2` | 2.92e+07 | 2.17e+52 | 0.500 / 0.388 | 1.1e+52 | 0.0859 |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.03n0.5c0.1_mech_snx2_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx2_ssp300` | `halos_iter0047164.txt` |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx4_ssp300` | `halos_iter0049140.txt` |
| `eps0.03n0.5c0.1_mech_snx10_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx10_ssp300` | `halos_iter0053689.txt` |
