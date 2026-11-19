# compare_h2_z8.09

z = 8.09 (a = 0.110, same snapshot in every run). Same 6 runs as `compare_h2_z9`, 1st-order vs production (h2) hydro. Stellar masses still match (h2 slightly higher). The f_esc gap has narrowed to 1.5-3x (ray-traced), and h2 x_HII is 1.9-2.5x higher.

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.03n0.5c0.1_th_t10_1st_order` | `reio_v2/epsn0.03c0.1_chemfix` | `halos_iter0031627.txt` |
| `eps0.03_mech_snx2_t10_1st_order` | `reio_v2/cf_eps0.03_mech_snx2` | `halos_iter0027807.txt` |
| `eps0.3_mech_n10_snx2_t3_1st_order` | `reio_v2/cf_eps0.3_mech_n10_snx2` | `halos_iter0029668.txt` |
| `eps0.03n0.5c0.1_th_t10_h2` | `reio_v2/h2_epsn0.03c0.1` | `halos_iter0036767.txt` |
| `eps0.03_mech_snx2_t10_h2` | `reio_v2/h2_eps0.03_mech_snx2` | `halos_iter0036464.txt` |
| `eps0.3_mech_n10_snx2_t3_h2` | `reio_v2/h2_eps0.3_mech_n10_snx2` | `halos_iter0041340.txt` |
