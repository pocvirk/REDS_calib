# compare_fbw_B_z5.90

z = 5.90 (a = 0.145). FB campaign series B (bursty SF; closest MEGATRON recipe: bursty, also high eps): eps 0.3, n_th 10, mechanical FB,
SN 2x / 5x / 10x, t_SNII 3 Myr, eta_SNII 0.2, production hydro, BPASS SSP M_max 300. Nearest snapshot to z = 6. All three within 0.055-0.064 in x_HII: FB strength barely matters for x_HII in series B here.
Numbers: `../fbw_trend/fbtrend_a0.145.txt`.

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|---|
| `eps0.3_n10_mech_snx2_t3_ssp300_h2` | 8.35e+08 | 1.78e+54 | 0.021 / 0.009 | 3.8e+52 | 0.0637 |
| `eps0.3_n10_mech_snx5_t3_ssp300_h2` | 1.87e+08 | 3.47e+53 | 0.159 / 0.172 | 5.5e+52 | 0.0546 |
| `eps0.3_n10_mech_snx10_t3_ssp300_h2` | 7.37e+07 | 1.22e+53 | 0.244 / 0.204 | 3e+52 | 0.0556 |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.3_n10_mech_snx2_t3_ssp300_h2` | `reio_v2/h2_eps0.3_mech_n10_snx2_t3_ssp300` | `halos_iter0057798.txt` |
| `eps0.3_n10_mech_snx5_t3_ssp300_h2` | `reio_v2/h2_eps0.3_mech_n10_snx5_t3_ssp300` | `halos_iter0067902.txt` |
| `eps0.3_n10_mech_snx10_t3_ssp300_h2` | `reio_v2/h2_eps0.3_mech_n10_snx10_t3_ssp300` | `halos_iter0076982.txt` |
