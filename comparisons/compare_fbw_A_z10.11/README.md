# compare_fbw_A_z10.11

z = 10.11 (a = 0.090). FB campaign series A (smooth SF): density-dependent eps (0.03 (n/n_th)^0.5 <= 0.1, n_th 0.1),
mechanical FB, SN energy 2x / 4x / 10x (4e49 / 8e49 / 2e50 erg/Msun), t_SNII 10 Myr, eta_SNII 0.2, production hydro,
BPASS SSP M_max 300 tables (`src_files/`). Numbers: `../fbw_trend/fbtrend_a0.090.txt`.

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|---|
| `eps0.03n0.5c0.1_mech_snx2_t10_ssp300_h2` | 2.37e7 | 1.09e53 | 0.44 / 0.44 | 4.8e52 | 0.0317 |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | 1.37e7 | 3.77e52 | 0.52 / 0.44 | 2.0e52 | 0.0256 |
| `eps0.03n0.5c0.1_mech_snx10_t10_ssp300_h2` | 8.7e6 | 2.28e52 | 0.63 / 0.51 | 1.4e52 | **0.0343** |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.03n0.5c0.1_mech_snx2_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx2_ssp300` | `halos_iter0022257.txt` |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx4_ssp300` | `halos_iter0024474.txt` |
| `eps0.03n0.5c0.1_mech_snx10_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx10_ssp300` | `halos_iter0028380.txt` |
