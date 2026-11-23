# compare_tsn_z8.09

z = 8.09 (a = 0.110, same snapshot in every run), production hydro (h2). Same five runs as `compare_tsn_z9`: t_SNII scan of
the constant-eps mechanical recipe (eps 0.03, 2x SN, t_SNII = 3 / 10 / 20 Myr), and the density-dependent eps recipe with
mechanical vs thermal feedback. `fbtrend_a0.110.{txt,png}` (`scripts/` / `runs/reio_v2/fbtrend.py`): total M* in halos,
intrinsic and escaping ionizing rate, photon-weighted global f_esc (ray-traced, M1) and volume x_HII per run.

| run | M* [Msun] | f_esc RT / M1 | escaping rate [ph/s] | x_HII |
|---|---|---|---|---|
| `eps0.03_mech_snx2_t3_h2` | 9.0e7 | 0.154 / 0.109 | 3.5e52 | 0.024 |
| `eps0.03_mech_snx2_t10_h2` | 9.8e7 | 0.118 / 0.116 | 2.5e52 | 0.032 |
| `eps0.03_mech_snx2_t20_h2` | 1.17e8 | 0.117 / 0.135 | 2.6e52 | 0.039 |
| `eps0.03n0.5c0.1_mech_snx2_t10_h2` | 8.4e7 | 0.174 / 0.180 | 2.9e52 | 0.036 |
| `eps0.03n0.5c0.1_th_t10_h2` | 3.0e8 | 0.111 / 0.133 | 8.1e52 | 0.102 |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.03_mech_snx2_t3_h2` | `reio_v2/h2_eps0.03_mech_snx2_t3` | `halos_iter0026703.txt` |
| `eps0.03_mech_snx2_t10_h2` | `reio_v2/h2_eps0.03_mech_snx2` | `halos_iter0036464.txt` |
| `eps0.03_mech_snx2_t20_h2` | `reio_v2/h2_eps0.03_mech_snx2_t20` | `halos_iter0039482.txt` |
| `eps0.03n0.5c0.1_mech_snx2_t10_h2` | `reio_v2/h2_eps0.03n0.5c0.1_mech_snx2` | `halos_iter0036735.txt` |
| `eps0.03n0.5c0.1_th_t10_h2` | `reio_v2/h2_epsn0.03c0.1` | `halos_iter0036767.txt` |
