# compare_fbw_A_z8.09

z = 8.09 (a = 0.110). FB campaign series A (smooth SF; closest MEGATRON recipe: smooth): density-dependent eps
(0.03 (n/n_th)^0.5 <= 0.1, n_th 0.1), mechanical FB, t_SNII 10 Myr, eta_SNII 0.2, production hydro, BPASS SSP M_max 300.
SN 2x / 4x / 10x. Numbers: `../fbw_trend/fbtrend_a0.110.txt`.

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|---|
| `eps0.03n0.5c0.1_mech_snx2_t10_ssp300_h2` | 8.91e7 | 2.85e53 | 0.23 / 0.27 | 6.7e52 | **0.115** |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | 3.53e7 | 7.90e52 | 0.48 / 0.48 | 3.8e52 | 0.054 |
| `eps0.03n0.5c0.1_mech_snx10_t10_ssp300_h2` | 1.78e7 | 2.71e52 | 0.62 / 0.52 | 1.7e52 | 0.065 |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.03n0.5c0.1_mech_snx2_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx2_ssp300` | `halos_iter0035161.txt` |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx4_ssp300` | `halos_iter0037295.txt` |
| `eps0.03n0.5c0.1_mech_snx10_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx10_ssp300` | `halos_iter0041695.txt` |
