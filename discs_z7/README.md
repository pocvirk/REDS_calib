# discs_z7

Isolated z = 7 discs in halos of 1e9, 3e9 and 1e10 Msun, dx_min = 195 pc, eps = 0.03, n_th = 0.1, mechanical SN feedback.
- `z7_tsn.png`: stars formed and photon-weighted f_esc (M1 and ray-traced) vs SN energy boost b = 1, 2, 4, 10, for
  t_SNII = 3 and 10 Myr (scan 2).
- `z7_fesc_vs_mass.png`, `z7_timeseries.png`: scan 1 (recipes vs halo mass, time series).
- `z7_cf_compare.png`, `z7_rt_cf_compare.png`: before / after the chemistry fix.
Templates and generator: `inis/disc_z7/`; scripts `scripts/analyse_z7.py`, `raytrace_z7.py`, `plot_z7_tsn.py`.
