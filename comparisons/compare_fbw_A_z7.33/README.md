# compare_fbw_A_z7.33

z = 7.33 (a = 0.120). FB campaign series A (smooth SF; closest MEGATRON recipe: smooth): density-dependent eps (0.03 (n/n_th)^0.5 <= 0.1,
n_th 0.1), mechanical FB, SN 2x / 4x / 10x, t_SNII 10 Myr, eta_SNII 0.2, production hydro, BPASS SSP M_max 300.
Numbers: `../fbw_trend/fbtrend_a0.120.txt`.

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|---|
| `eps0.03n0.5c0.1_mech_snx10_t10_ssp300_h2` | 2.37e+07 | 2.46e+52 | 0.548 / 0.425 | 1.3e+52 | 0.0760 |
| `eps0.03n0.5c0.1_mech_snx2_t10_ssp300_h2` | 1.6e+08 | 5.09e+53 | 0.188 / 0.227 | 9.6e+52 | 0.2010 |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | 5.64e+07 | 1.48e+53 | 0.407 / 0.359 | 6e+52 | 0.0786 |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.03n0.5c0.1_mech_snx10_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx10_ssp300` | `halos_iter0047900.txt` |
| `eps0.03n0.5c0.1_mech_snx2_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx2_ssp300` | `halos_iter0041266.txt` |
| `eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx4_ssp300` | `halos_iter0043345.txt` |
