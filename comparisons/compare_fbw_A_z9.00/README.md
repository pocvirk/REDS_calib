# compare_fbw_A_z9.00

z = 9.00 (a = 0.100). FB campaign series A (smooth SF): density-dependent eps (0.03 (n/n_th)^0.5 <= 0.1, n_th 0.1), mechanical FB, SN energy
2x / 4x / 10x (4e49 / 8e49 / 2e50 erg/Msun), t_SNII 10 Myr, eta_SNII 0.2, production hydro, BPASS SSP M_max 300
(`src_files/`). Numbers: `../fbw_trend/fbtrend_a0.100.txt`.

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|---|
| `eps0.03n0.5c0.1_mech_snx2_t10_ssp300_h2` | 4.74e7 | 1.64e53 | 0.30 / 0.31 | 4.9e52 | **0.061** |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | 2.28e7 | 4.93e52 | 0.52 / 0.43 | 2.6e52 | 0.040 |
| `eps0.03n0.5c0.1_mech_snx10_t10_ssp300_h2` | 1.34e7 | 2.36e52 | 0.57 / 0.50 | 1.3e52 | 0.052 |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.03n0.5c0.1_mech_snx2_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx2_ssp300` | `halos_iter0028838.txt` |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx4_ssp300` | `halos_iter0030967.txt` |
| `eps0.03n0.5c0.1_mech_snx10_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx10_ssp300` | `halos_iter0035301.txt` |
