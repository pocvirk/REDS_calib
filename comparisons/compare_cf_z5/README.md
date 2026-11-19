# compare_cf_z5

z = 5. Constant-eps recipes after the chemistry fix (1st-order hydro): mechanical FB with 2x / 3x SN energy, delayed cooling, the bursty n_th = 10 recipe, vs the CoDa III-like run and RAMSES.

| label (legend) | run directory (Frontier, runs/) | halo catalogue |
|---|---|---|
| `RAMSES_eps0.01_th_t10` | `ramses_box/eps0.01` | `halos_iter0000019.txt` |
| `codalike_eps0.03_th_t10_dx11.6kpc` | `reio_v2/codalike_chemfix` | `halos_iter0002193.txt` |
| `eps0.03_mech_snx2_t10` | `reio_v2/cf_eps0.03_mech_snx2` | `halos_iter0059083.txt` |
| `eps0.03_mech_snx3_t10` | `reio_v2/cf_eps0.03_mech_snx3` | `halos_iter0059401.txt` |
| `eps0.03_dc_snx2_t10` | `reio_v2/cf_eps0.03_dc_snx2` | `halos_iter0062021.txt` |
