# compare_h2_z5

z = 5 (end of the run). Production hydro (h2) density-dependent eps recipe with thermal FB vs the same recipe in 1st-order
hydro, and the eps 0.01 dyablo-production vs RAMSES-RT baseline (matched galaxies, `compare_cmp_ramses_z5`).

| run | M* in halos [Msun] | intrinsic Ndot [ph/s] | global f_esc (ray-traced) | escaping rate [ph/s] | x_HII (volume) |
|---|---|---|---|---|---|
| `eps0.03n0.5c0.1_th_t10_h2` | 7.0e9 | 1.0e55 | 0.035 | 3.5e53 | 0.96 |
| `eps0.03n0.5c0.1_th_t10_1st_order` | 8.3e9 | 9.7e54 | 0.016 | 1.6e53 | 0.88 |
| `dyablo_production_eps0.01_th_t10` | 1.1e10 | 1.0e55 | 0.006 | 6.0e52 | 0.31 |
| `RAMSES_eps0.01_th_t10` | 1.0e10 | 8.4e54 | 0.005 | 4.6e52 | 0.43 |

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `eps0.03n0.5c0.1_th_t10_h2` | `reio_v2/h2_epsn0.03c0.1` | `halos_iter0068037.txt` |
| `eps0.03n0.5c0.1_th_t10_1st_order` | `reio_v2/epsn0.03c0.1_chemfix` | `halos_iter0062830.txt` |
| `dyablo_production_eps0.01_th_t10` | `reio_v2/eps0.01_rk2_ei_rr_cmp` | `halos_iter0066585.txt` |
| `RAMSES_eps0.01_th_t10` | `ramses_box/eps0.01_s1_b0_ics` | `halos_iter0000041.txt` |
