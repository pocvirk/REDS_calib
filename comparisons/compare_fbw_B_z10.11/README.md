# compare_fbw_B_z10.11

z = 10.11 (a = 0.090). FB campaign series B (bursty SF): eps 0.3, n_th 10, mechanical FB, SN energy 2x / 5x / 10x
(4e49 / 1e50 / 2e50 erg/Msun), t_SNII 3 Myr, eta_SNII 0.2, production hydro, BPASS SSP M_max 300 tables (`src_files/`).
Numbers: `../fbw_trend/fbtrend_a0.090.txt`.

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|---|
| `eps0.3_n10_mech_snx2_t3_ssp300_h2` | 2.83e7 | 1.76e53 | 0.046 / 0.023 | 8.1e51 | 0.0042 |
| `eps0.3_n10_mech_snx5_t3_ssp300_h2` | 1.02e7 | 6.43e52 | 0.100 / 0.070 | 6.4e51 | 0.0049 |
| `eps0.3_n10_mech_snx10_t3_ssp300_h2` | 7.49e6 | 3.70e52 | 0.245 / 0.164 | 9.1e51 | **0.0072** |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.3_n10_mech_snx2_t3_ssp300_h2` | `reio_v2/h2_eps0.3_mech_n10_snx2_t3_ssp300` | `halos_iter0023792.txt` |
| `eps0.3_n10_mech_snx5_t3_ssp300_h2` | `reio_v2/h2_eps0.3_mech_n10_snx5_t3_ssp300` | `halos_iter0026782.txt` |
| `eps0.3_n10_mech_snx10_t3_ssp300_h2` | `reio_v2/h2_eps0.3_mech_n10_snx10_t3_ssp300` | `halos_iter0032206.txt` |
