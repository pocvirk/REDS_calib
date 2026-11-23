# compare_fbw_M_z9.00

z = 9.00 (a = 0.100). BPASS M_max 100 vs 300 twins (pair M): density-dependent eps (0.03 (n/n_th)^0.5 <= 0.1, n_th 0.1), mechanical FB, 4x SN,
t_SNII 10 Myr, eta_SNII 0.2, production hydro, SSP tables from `src_files/`. Numbers: `../fbw_trend/fbtrend_a0.100.txt`.

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|---|
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp100_h2` | 2.35e7 | 3.70e52 | 0.41 / 0.35 | 1.5e52 | 0.021 |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | 2.28e7 | 4.93e52 | 0.52 / 0.43 | 2.6e52 | **0.040** |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp100_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx4_ssp100` | `halos_iter0032476.txt` |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx4_ssp300` | `halos_iter0030967.txt` |
