# compare_tsn_z9

z = 9 (a = 0.100, same snapshot in every run), production hydro (h2). t_SNII scan of the constant-eps mechanical recipe
(eps 0.03, 2x SN, t_SNII = 3 / 10 / 20 Myr), and the density-dependent eps recipe with mechanical vs thermal feedback.
Longer t_SNII: more stars (total M* in halos 4.5e7 / 5.1e7 / 6.7e7 Msun) and higher x_HII (0.015 / 0.019 / 0.025); global
f_esc not monotonic (M1 0.17 / 0.17 / 0.21). Mechanical feedback with density-dependent eps: 2.8x fewer stars than thermal,
2x higher f_esc, x_HII 0.022 vs 0.048.

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.03_mech_snx2_t3_h2` | `reio_v2/h2_eps0.03_mech_snx2_t3` | `halos_iter0021254.txt` |
| `eps0.03_mech_snx2_t10_h2` | `reio_v2/h2_eps0.03_mech_snx2` | `halos_iter0030152.txt` |
| `eps0.03_mech_snx2_t20_h2` | `reio_v2/h2_eps0.03_mech_snx2_t20` | `halos_iter0032849.txt` |
| `eps0.03n0.5c0.1_mech_snx2_t10_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx2` | `halos_iter0030423.txt` |
| `eps0.03n0.5c0.1_th_t10_h2` | `reio_v2/h2_epsn0.03c0.1` | `halos_iter0030454.txt` |
