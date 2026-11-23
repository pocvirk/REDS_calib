# compare_fbw_B_z9.00

z = 9.00 (a = 0.100). FB campaign series B (bursty SF): eps 0.3, n_th 10, mechanical FB, SN energy 2x / 5x,
t_SNII 3 Myr, eta_SNII 0.2, production hydro, BPASS SSP M_max 300 (`src_files/`). The 10x run is not at z = 9 yet.
Numbers: `../fbw_trend/fbtrend_a0.100.txt`.

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|---|
| `eps0.3_n10_mech_snx2_t3_ssp300_h2` | 6.56e7 | 3.61e53 | 0.071 / 0.050 | 2.6e52 | 0.0062 |
| `eps0.3_n10_mech_snx5_t3_ssp300_h2` | 2.02e7 | 8.88e52 | 0.144 / 0.118 | 1.3e52 | **0.0078** |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.3_n10_mech_snx2_t3_ssp300_h2` | `reio_v2/h2_eps0.3_mech_n10_snx2_t3_ssp300` | `halos_iter0030445.txt` |
| `eps0.3_n10_mech_snx5_t3_ssp300_h2` | `reio_v2/h2_eps0.3_mech_n10_snx5_t3_ssp300` | `halos_iter0033873.txt` |
