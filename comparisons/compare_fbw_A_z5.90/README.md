# compare_fbw_A_z5.90

z = 5.90 (a = 0.145). FB campaign series A (smooth SF; closest MEGATRON recipe: smooth): density-dependent eps (0.03 (n/n_th)^0.5 <= 0.1),
mechanical FB, SN 2x / 4x / 10x, t_SNII 10 Myr, eta_SNII 0.2, production hydro, BPASS SSP M_max 300. Nearest snapshot to z = 6 (snapshots every da = 0.005).
Numbers: `../fbw_trend/fbtrend_a0.145.txt`.

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|---|
| `eps0.03n0.5c0.1_mech_snx2_t10_ssp300_h2` | 5.7e+08 | 1.12e+54 | 0.120 / 0.167 | 1.3e+53 | 0.6243 |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | 1.41e+08 | 1.89e+53 | 0.266 / 0.271 | 5e+52 | 0.2312 |
| `eps0.03n0.5c0.1_mech_snx10_t10_ssp300_h2` | 3.9e+07 | 3.33e+52 | 0.477 / 0.429 | 1.6e+52 | 0.1022 |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.03n0.5c0.1_mech_snx2_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx2_ssp300` | `halos_iter0055477.txt` |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx4_ssp300` | `halos_iter0057425.txt` |
| `eps0.03n0.5c0.1_mech_snx10_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx10_ssp300` | `halos_iter0062064.txt` |
