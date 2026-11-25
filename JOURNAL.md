# Calibration journal (newest first)

Recipe labels as in the README: `<SF>_<FB>[_snx<k>]_t<t_SNII>[_<hydro>]`.

## 2026-11-25 (18:50): c_rad 0.1c at z = 6.69; 8 cMpc/h UV LF at z = 7.33
`comparisons/fiducial_twins/crad_sfr_*.png`, `comparisons/compare_twins_z6.69` (now 4 runs incl. c_rad 0.1c),
`comparisons/box_size_4_vs_8mpc/uvlf_boxC_z8.52_8.09_7.33.png`. Fiducial: smooth SF eps0.03 (n/n_th)^0.5, mech FB 2x SN,
t_SNII 10 Myr, M_max 300 (closest MEGATRON recipe: smooth).
- c_rad 0.1c vs 0.01c at z = 6.69 (box x_HII ~ 0.35-0.4): SFR(Mh) identical from 10^7.1 to 10^9.9 Msun; the 10^7.5-8 bin
  (0.82-0.91 before) is now 1.10. No radiative-suppression difference between the two c values so far.
- 8 cMpc/h UV LF at z = 7.33: reaches M_UV ~ -19.3; 1.5-2x above Bouwens+21/22 and Harikane+25 at -17 to -19 (edge of the
  Poisson band, few objects per bin); faint end (-13 to -16) in line with the Bouwens+22 lensed points, Atek+26 GLIMPSE ~3x
  higher at -13 to -14. Bright-end excess growing slowly since z = 8.09.
- Status: all 4 follow-ups queued since 15:47 (Frontier: est. start 19:30). thermal z 5.09 (x_HII 0.995), constant eps z 5.41
  (0.71), c_rad 0.1c z 6.28 (0.57), 8 cMpc/h z 7.20 (0.28). No crashes.

## 2026-11-25 (12:50): radiative suppression test, c_rad 0.01c vs 0.1c (Ocvirk+16 SFR(Mh))
`comparisons/fiducial_twins/crad_sfr_mh.png`, `crad_sfr_z.png`, `crad_sfr.txt` (mean SFR over the last 10 Myr of all halos in a
Mh bin, from the dashboard; `runs/reio_v2/twins/sfr_mh.py`). Fiducial: smooth SF eps0.03 (n/n_th)^0.5, mech FB 2x SN, t_SNII 10 Myr,
M_max 300 (closest MEGATRON recipe: smooth).
- c consistency checked: every module reads `[rad] c_rad` (M1 transport, RT dt, Chem_Ramses chemistry in physical units,
  AveragesLogger), so the photoionization / heating rates use the same reduced c as the transport. reion_accel only skips RT
  before the first star.
- The fiducial shows the Ocvirk+16 kink: from z = 10 to 5, <SFR> drops x2-3 at 1e9 Msun but x40-100 below ~10^8.3 Msun,
  faster after z ~ 7 (x_HII > 0.3). Kink at lower mass than CoDa I/II (higher resolution, but different SF + SN FB recipe).
- 0.1c vs 0.01c at z = 10.1 - 7.3: no kink difference yet. The SFR ratio scatters 0.65-1.25 between snapshots (run-to-run
  noise); only the 10^7.5-8 bin is steadily lower (0.82-0.91). The earlier "stronger radiative feedback at 0.1c" reading
  (15% fewer stars) is withdrawn: within noise, no mass trend. The real test is z <= 6.7 (0.1c run at z 6.65; added
  automatically by `twins/crad_watch.sh`).
- Status: all 4 follow-ups queued since 10:25 (Frontier: est. start 15:00). thermal z 5.35 (x_HII 0.95), constant eps z 5.72
  (0.59), c_rad 0.1c z 6.65 (0.41), 8 cMpc/h z 7.42 (0.25). No crashes.

## 2026-11-25 (09:30): fiducial vs its 3 twins (thermal FB, constant eps, c_rad 0.1c), z = 8.09 - 5.90
`comparisons/compare_twins_z{8.09,7.33,6.69,5.90}`, `comparisons/fiducial_twins/` (f_esc vs Mh / M* / M_UV, photon budget by Mh,
UV LF z 6-8 with the new compilation). Fiducial: smooth SF eps0.03 (n/n_th)^0.5 <= 0.1, mech FB 2x SN, t_SNII 10 Myr, M_max 300,
c_rad 0.01c (closest MEGATRON recipe: smooth). 4 cMpc/h; each twin changes one thing.

| z = 7.33 | M* [Msun] | f_esc RT (global) | f_esc RT, Mh 10^9.5-10 | x_HII |
|---|---|---|---|---|
| fiducial `eps0.03n0.5c0.1_mech_snx2_t10` | 1.60e8 | 0.19 | 0.095 | 0.20 |
| thermal FB `eps0.03n0.5c0.1_thermal_snx2_t10` | 2.27e8 | 0.15 | 0.080 | 0.27 |
| constant eps `eps0.03_mech_snx2_t10` | 1.90e8 | 0.12 | **0.041** | 0.18 |
| c_rad 0.1c `eps0.03n0.5c0.1_mech_snx2_t10_crad0.1` | 1.36e8 | 0.21 | 0.116 | 0.22 |

- **Thermal FB:** 1.3-1.45x the stars at every z, f_esc 10-20% lower; x_HII ahead by ~0.1 (more stars win). Same f_esc(Mh)
  shape. Mechanical FB does real work in limiting SF.
- **Constant eps (no sqrt(n) boost):** 1.15-1.25x the stars, global f_esc 0.6-0.7x, x_HII behind by 0.03-0.08. The f_esc(Mh)
  slope is **steeper**: f_esc(10^9.5-10) 0.045 / 0.041 / 0.050 at z 8.09 / 7.33 / 6.69 (fiducial 0.087 / 0.095 / 0.107),
  0.034 at 10^10-10.5 (z 6.69). This is the CoDa direction at the massive end (f_esc(1e10) ~ 0.02-0.05), but f_esc(1e9) also drops
  (0.12-0.13 vs 0.17-0.18; target ~ 0.5). The sqrt(n) term helps massive halos leak (SF concentrated in the densest clumps).
- **c_rad 0.1c (reion_accel on):** 0.8-0.85x the stars, global f_esc 1.1-1.15x, x_HII about the same or slightly ahead. With
  0.01c the fiducial overstates M* by ~15% and understates f_esc by ~10%: worth keeping in mind for the 8 cMpc/h recipe.
- UV LF: all four within errors of each other at z ~ 6-8; same faint-end deficit against the lensed points. Gamma: indistinguishable.
- None of the twins fixes the flat f_esc(Mh). Constant eps is the only step in the right direction at high mass.
- Status: thermal twin z 5.6 (x_HII 0.85), constant eps z 6.0 (0.48), c_rad 0.1c z 6.9 (0.31), 8 cMpc/h z 7.7 (0.20). No crashes.

## 2026-11-25 (06:45): box size: the 4 cMpc/h calibration does not hold in 8 cMpc/h
`comparisons/compare_box_z8.52`, `comparisons/box_size_4_vs_8mpc/` (fiducial reio model: smooth SF eps0.03 (n/n_th)^0.5, mech FB
2x SN, t_SNII 10 Myr, M_max 300; closest MEGATRON recipe: smooth)
- Same physics, same resolution, 4 vs 8 cMpc/h (no setup difference besides box size, levels and seed). Identical to z ~ 12, then
  the 8 cMpc/h box pulls ahead: stars per volume x2.8, photon rate x3.2, x_HII x1.36 at z = 8.4.
- The 4 cMpc/h box is a median region: in 4 cMpc/h octants of the 8 cMpc/h box the stellar mass ranges 0.3-13x the 4 cMpc/h box
  (median 0.8); the 2 octants with +27% DM hold 81% of the stars (9 halos > 1e10 Msun, none in the 4 cMpc/h box).
- f_esc(Mh) is the same in both boxes (per-halo physics converged): ~0.5 at 1e8, 0.25 at 1e9, 0.09 at 1e10 Msun. Too flat compared
  with the CoDa target (f_esc(1e9) ~ 0.5, f_esc(1e10) ~ 0.02-0.05). In 8 cMpc/h the 9 halos > 1e10 give 32% of the escaping
  photons (4 cMpc/h: 0%).
- UV LF (new JWST + HST + lensed compilation, 265 points incl. Atek+26 GLIMPSE z~7, Bouwens+22 HFF): at z = 8.09 the 8 cMpc/h box
  matches the bright end within errors (to M_UV -19.3); the faint end (-12 to -15) is 3-10x below the lensed z~8 points in both
  boxes. Bright-end excess expected to grow by z ~ 7-6 (watched automatically).
- Conclusion (PO): calibration boxes must be 8 cMpc/h; 4 cMpc/h does not show what the sub-grid model does to massive halos.
  Next: a recipe with bursty SF in small halos and smooth, inefficient SF in big ones (options under discussion).
- Follow-ups: thermal twin z 6.0 (x_HII 0.72), constant eps z 6.4 (0.37), c_rad 0.1c z 7.25 (0.24), 8 cMpc/h z 7.95 (0.17). No crashes.

## 2026-11-25 (01:00): FB campaign complete (all 7 runs at z = 5); final series B comparison
`comparisons/compare_fbw_B_z5.00` (now 2x / 5x / 10x), `fbw_trend/fbtrend_a0.167.*`
- **Series B (bursty SF; closest MEGATRON recipe: bursty, also high eps; t_SNII 3) at z = 5:** 2x / 5x / 10x: M* 1.9e9 /
  3.7e8 / 1.2e8 Msun, f_esc RT 0.012 / 0.027 / 0.124, x_HII **0.116 / 0.091 / 0.088**. f_esc keeps rising with FB, but not
  enough to offset the lost stars: escaping rates 5.1 / 1.8 / 0.44e52 ph/s. Both steps are partial (more stars win on x_HII).
- **Campaign result (final):** stronger FB always lowers M* and raises f_esc (both series, every z). The full MEGATRON trend
  (x_HII also rising) appears only in series B at z >= 7.3 (10x vs 5x); by z = 5.9 B's FB strength is neutral for x_HII, and
  at z = 5 it is reversed (weakly). Series A shows only the partial trend at every z (x_HII 0.96 / 0.41 / 0.14 for 2x / 4x /
  10x at z = 5). In our 4 cMpc/h box, f_esc rises too slowly with FB (dlog f_esc / dlog M* -0.5 to -1.3, needs < -1 on both
  estimates) for the MEGATRON trend to survive to the end of reionization. M_max 300 vs 100: 1.8-1.9x the x_HII at fixed M*.
- Production `h2_eps0.3_mech_n10_snx2_t10` (t_SNII scan) done: x_HII 0.59 at z = 5.
- Fiducial follow-ups (run index): thermal twin z ~ 7.7, constant eps z ~ 8.0, c_rad 0.1c (8 nodes) z ~ 8.4, 8 cMpc/h box z ~ 9.3.
  No crashes.

## 2026-11-24 (19:00): series B 5x done at z = 5; node-scaling tests for the c_rad 0.1c run
`comparisons/compare_fbw_B_z5.00` (2x and 5x; 10x at z = 5.04 will be added by the watcher), `fbw_trend/fbtrend_a0.167.*`
- **Series B (bursty SF; closest MEGATRON recipe: bursty, also high eps; t_SNII 3) at z = 5:** 2x / 5x: M* 1.9e9 / 3.7e8 Msun,
  f_esc RT 0.012 / 0.027, x_HII **0.116 / 0.091**. Partial step (f_esc anticorrelated with M*, slope -0.5), more stars win on
  x_HII. B ends 8-10x below A 2x (0.96): bursty SF with high eps traps its photons (f_esc 1-3%) and no B run gets near overlap.
- **Campaign summary so far:** the MEGATRON trend in full (stronger FB -> lower M* and higher x_HII) appears only in series B at
  z >= 7.3 (10x vs 5x); at z <= 6.7 B is flat or partial. Series A shows only the partial trend at every z (2x > 4x > 10x in
  x_HII). M_max 300 vs 100 gives 1.8-1.9x the x_HII at fixed M*.
- **c_rad 0.1c run speed (fiducial follow-up):** this morning it ran ~30x faster on 8 nodes than on 1 node. Short tests from
  its checkpoints (dyablo timer tables, `runs/reio_v2/nodescan/`) split this into (a) a real 1 -> 8 node gain of 5.4x over
  iterations 400-500, driven by the chemistry (SourceUpdate 408 s -> 30 s, 14x: likely load imbalance of the stiff chemistry
  around the first sources) and 2.5x over 500-538; and (b) a further ~3x slowdown of this morning's 1-node jobs that does not
  reproduce now (cause unknown). GPU-aware MPI, OpenMP threads and the averages writer are not the cause; IPC on crashes.
  The c_rad 0.01c fiducial is 2x faster on 8 nodes (4x more node-hours), so 1 node stays right for the c = 0.01c runs.
- Production `h2_eps0.3_mech_n10_snx2_t10` at z = 5.03. No campaign crashes.

## 2026-11-24 (12:50): series B at z = 5.9 (FB strength no longer matters for x_HII); M_max pair at z = 5.9 / 5; fiducial follow-ups launched
`comparisons/compare_fbw_B_z5.90`, `compare_fbw_M_z5.90`, `compare_fbw_M_z5.00`, `compare_fbw_A_z5.00`, `fbw_trend/fbtrend_a0.{145,167}.*`
- **Series B (bursty SF; closest MEGATRON recipe: bursty, also high eps; t_SNII 3) at z = 5.90:** 2x / 5x / 10x:
  M* 8.4e8 / 1.9e8 / 7.4e7 Msun, f_esc RT 0.021 / 0.16 / 0.24, x_HII **0.064 / 0.055 / 0.056**. f_esc compensates M*
  almost exactly: the escaping photon rates are 3.8 / 5.5 / 3.0e52 ph/s and the three x_HII(z) curves lie on top of each
  other. Formally 10x vs 5x is still a "full" MEGATRON step (x 0.0556 vs 0.0546), but the difference (2%) is noise; 2x has
  the highest x_HII (partial step 5x vs 2x). So series B shows the f_esc-M* anticorrelation at every z, and a full trend only
  at z >= 7.3; at z <= 6.7 FB strength is neutral for x_HII. All B runs stay far below the z ~ 7 constraints (x_HII < 0.07
  at z = 6). B 2x ended at x_HII 0.12 (z = 5).
- **Series A (smooth SF; closest MEGATRON recipe: smooth; t_SNII 10) at z = 5 (run end, all done):** 2x / 4x / 10x M*
  1.4e9 / 2.7e8 / 5.9e7, f_esc RT 0.061 / 0.17 / 0.35, x_HII **0.96** / 0.41 / 0.14 (partial trend at both steps, slopes
  -0.62 / -0.48).
- **M_max 100 vs 300 (smooth, mech 4x SN, t_SNII 10):** same M* (2.8e8 / 2.7e8 at z = 5), the M_max 300 run has 1.4x the
  intrinsic photon rate, a higher f_esc (0.17 vs 0.14) and **1.8-1.9x the x_HII**: 0.23 vs 0.41 at z = 5, 0.12 vs 0.23 at z = 5.9.
- **Fiducial model:** PO chose A 2x (`h2_eps0.03n0.5c0.1_mech_snx2_ssp300`) as the fiducial. Four follow-up runs started
  08:13 to test the physics choices around it (run index): thermal twin (FB type), constant eps 0.03 (is the sqrt(n) SF law
  needed?), c_rad 0.1 c from the ICs (reion_accel on), and an 8 cMpc/h box (512^3, same resolution, 8 nodes). At 12:50 they
  are at z ~ 13 / 13 / 16.6 / 15.
- **c_rad 0.1 c is slow:** after the first stars the radiation step is ~1/1000 of the hydro step, so each hydro step needs
  hundreds of RT subcycles (~50 min per 100 iterations on 1 node). Speed test from the same checkpoint (iterations 400 -> 500):
  1 / 2 / 4 / 8 GPUs took 39 / **28** / 36 / 54 min, so the run is communication-bound and 2 GPUs is fastest. An 8-node job is
  being timed; the run will then move to the fastest layout. First relaunches lost ~2.3 node-hours (no checkpoint within
  the 2 h job, then an inline ini comment, which dyablo's ini parser rejects).
- Production `h2_eps0.3_mech_n10_snx2_t10` at z ~ 5.5. No campaign crashes.

## 2026-11-24 (07:00): series A, M_max pair finished at z = 5; A 2x reionizes the box (x_HII 0.96)
`comparisons/compare_fbw_A_z5.90`, `compare_fbw_B_z6.69` (10x added), `fbw_trend/fbtrend_a0.{130,145}.*`
- **Final x_HII at z = 5 (volume / mass):** A 2x **0.96 / 0.88**, A 4x 0.41 / 0.43, A 10x 0.14, M_max 100 twin of A 4x
  0.23 / 0.28. The h2 production runs with mechanical FB ended at 0.22-0.44 (thermal 0.96), so A 2x is the first
  mechanical-FB run to reach near-overlap. Its x_HII(z) goes through Hoag+19, the lower part of Mason+18 / Davies+18 at
  z ~ 7 (0.25) and rises to 0.62 at z = 5.9.
- **Series A at z = 5.90 (nearest snapshot to z = 6):** M* 5.7e8 / 1.4e8 / 3.9e7 Msun, f_esc RT 0.12 / 0.27 / 0.48,
  x_HII **0.62** / 0.23 / 0.10. Partial MEGATRON trend at both steps (slopes -0.57 / -0.45); more stars still win on x_HII.
  2x UV LF on Bouwens+16 / Bouwens+14 from M_UV -13 to -18; SMHM ~0.3-0.5 dex above the extrapolated Behroozi+19 at 3e9-1e10
  Msun (4x on it). 2x halo f_esc falls from ~0.5 at 1e8 to 0.05 at 1.3e10 Msun, the CoDa value at 1e10.
- **Open issues for A 2x:** tau_e = 0.042, below Planck+18 (0.054 +- 0.007). **Gamma is low:** the x_HII > 0.99 mean is ~4e-14 s^-1 at
  z = 5-6 (Gamma_V/x_V the same once the box is ionized), ~1-1.3 dex below the Calverley+11 / D'Aloisio+18 values.
  The box is ionized, but the emissivity or mean free path is too low for the observed post-overlap UVB.
- **Series B at z = 6.69 with 10x:** M* 4.4e8 / 1.1e8 / 4.6e7, f_esc 0.02 / 0.11 / 0.15, x_HII 0.044 / 0.035 / 0.040.
  10x vs 5x is still a full step; 2x has the highest x_HII (partial step 5x vs 2x).
- Watcher extended (PO request, 06:04): new targets a = 0.145 (z = 5.90) and a = 0.1667 (z = 5, run end; the watcher waits
  for the chain's ALL DONE). At most 3 runs per dashboard job, 1 h debug. z = 5 dashboards for series A are running.
- Series B at z ~ 5.4 / 5.5 / 6.1, production `h2_eps0.3_mech_n10_snx2_t10` at 5.9. No crashes.

## 2026-11-24 (01:00): FB campaign at z = 6.7; series B 10x at z = 8.1 and 7.3
`comparisons/compare_fbw_A_z6.69`, `compare_fbw_B_z6.69`, `compare_fbw_B_z8.09` and `_z7.33` (10x added), `fbw_trend/fbtrend_a0.{110,120,130}.*`
- **Series A 2x: x_HII 0.33 at z = 6.69** (curve ~0.37 at z = 6.6), near the lower edge of the z ~ 7 constraints
  (Mason+18, Davies+18). 2x / 4x / 10x: M* 3.0e8 / 8.6e7 / 2.9e7 Msun, f_esc RT 0.15 / 0.36 / 0.50, x_HII **0.334** /
  0.130 / 0.086. Partial MEGATRON trend at both steps (f_esc anticorrelated with M*, slopes -0.31 / -0.68), too shallow
  for x_HII: the ranking is 2x > 4x > 10x. 10x vs 4x was a full step at z = 8.1 (x 0.065 vs 0.054) and has reversed since.
  2x UV LF follows Bouwens+16 (z = 6) from M_UV -13 to -16 (box too small beyond -17). Its SMHM is ~0.3 dex above the
  extrapolated Behroozi+19 at 3-8e9 Msun (4x on it). Its halo f_esc falls from ~0.6 at 1e8 to 0.1 at 7e9 Msun.
  Gamma (x_HII > 0.99 mean) ~5.6e-14 s^-1, flat since z = 7.5; Gamma_V/x_V 0.1 dex lower.
- **Series B 10x keeps the full trend at z = 8.1 and 7.3.** At z = 8.1, 2x / 5x / 10x have M* 1.35e8 / 3.9e7 / 2.1e7,
  f_esc RT 0.02 / 0.14 / 0.26 and x_HII 0.011 / 0.012 / **0.017**. At z = 7.3, M* 2.6e8 / 6.9e7 / 3.4e7, f_esc 0.03 /
  0.06 / 0.20 and x_HII 0.015 / 0.023 / **0.029**. Both steps are full MEGATRON steps (slopes -0.6 to -1.6). The 10x
  run has as many intrinsic photons as 5x with half the stars (bursty: young populations dominate).
- **Series B at z = 6.69 (2x / 5x): the 2x run overtakes.** M* 4.4e8 / 1.1e8, f_esc 0.02 / 0.11, x_HII **0.044** /
  0.035, so B 2x vs 5x has become a partial step (as in series A). B still ionizes 7-10x less than A 2x.
  eps 0.3 builds ~1.5x more stars than A 2x, with an f_esc of 0.02.
- Campaign runs now at z ~ 5.5-6.2 (B 10x at 7.0). All 8 chain jobs are running (started 23:36-23:40). No crashes.
  Watcher alive; only B 10x at z = 6.69 is left, after which it exits (last target a = 0.130).
  Production `h2_eps0.3_mech_n10_snx2_t10` at z ~ 6.4.

## 2026-11-23 (18:50): M_max pair at z = 6.7; t_SNII scan finished at z = 5
`comparisons/compare_fbw_M_z6.69`, `comparisons/fbw_trend/fbtrend_a0.130.*`
- M_max 300 vs 100 at z = 6.69: same M* (8.6e7 Msun), intrinsic photons +39%, f_esc 0.36 vs 0.27 (RT; M1 0.38 vs 0.28),
  escaping rate +81%, **x_HII 0.130 vs 0.065 (2.0x)**. The x_HII ratio keeps growing: 1.77 (z = 10.1), 1.90 (9, 8.1, 7.3),
  2.0 (6.7); since z = 9 M_max 300 also raises f_esc, not only the photon budget.
- `h2_eps0.03_mech_snx2_t20` finished at z = 5: x_HII 0.36. The production t_SNII scan (eps 0.03, mech, 2x SN, old M_max 100
  table) ends at x_HII 0.22 / 0.30 / 0.36 for t_SNII 3 / 10 / 20 Myr: a longer delay gives more stars and more
  ionization, the same ordering as at every earlier z. Only `h2_eps0.3_mech_n10_snx2_t10` (z ~ 7.1) is still running.
- Campaign runs at z ~ 6.5-7.1 (B 10x at 8.0); all 8 remaining chain jobs pending (queue, estimated start 19:36). No crashes.

## 2026-11-23 (18:30): Gamma now averaged over ionized cells with x_HII > 0.99
- PO: Gamma must be the average over ionized regions, x_HII > 0.99. Until now the dashboard Gamma was Gamma_ion with
  x_HII > 0.5 (runtime AveragesLogger and snapshot averages alike). New `averages.gamma_ion_history` (dyablo_tools,
  local): Gamma over cells with x_HII > 0.99 from the snapshots (rho, rho_HII, e_rad), cached per snapshot,
  `<run>/dashboard/gamma_ion_x0.99.txt`; used by `run_dashboard.py` and `compare_dashboard.py` (title states the cut;
  runs without the file fall back to x > 0.5 and the title says so). Backfilled for the 7 campaign runs (37 s, debug job);
  all campaign comparisons regenerated.
- Effect: x > 0.99 Gamma is 1.4-2.2x the x > 0.5 one (A 2x at z = 7: 5.5e-14 vs 3.8e-14 s^-1; all-cell average 8e-15).
  Still 0.5-1 dex below the z = 6 measurements, but the campaign runs are at z ~ 7 and far from overlap
  (x_HII > 0.99 volume fraction 0.18 for A 2x at z = 7).
- PO: keep both estimates. Gamma plots now show solid = mean over x_HII > 0.99 cells, dashed = Gamma_V / x_HII,V (the
  ramses-cudaton estimate, Gamma ~ 0 in neutral cells; equal to the x > 0.5 cell mean within a few %). The ratio sits
  0.15-0.35 dex below the x > 0.99 mean (partly ionized I-front / self-shielded cells in x_V), most at high z and in 10x.

## 2026-11-23 (18:00): FB campaign at z = 7.3; series A 2x through the Hoag+19 point
`comparisons/compare_fbw_{A,B,M}_z7.33`, `comparisons/compare_fbw_B_z8.09`, `compare_fbw_B_z9.00` (10x added), `fbw_trend/fbtrend_a0.{100,110,120}.*`
- **Series A 2x: x_HII 0.20 at z = 7.33**, through the Hoag+19 point (z ~ 7.6) and still rising steeply. 2x / 4x / 10x:
  M* 1.6e8 / 5.6e7 / 2.4e7 Msun, f_esc RT 0.19 / 0.41 / 0.55, x_HII **0.201** / 0.079 / 0.076. The 10x run fell behind
  4x between z = 8.1 and 7.3, so the ranking is now strictly "more stars win" (partial trend at both steps: f_esc
  anticorrelated with M*, slopes -0.34 / -0.74). 2x SMHM ~0.3-0.4 dex above the extrapolated Behroozi+19 at 2-4e9 Msun
  (4x on it, 10x below); 2x f_esc falls from ~0.5 at 1e8 to 0.1 at 4e9 Msun.
- **Series B keeps the full MEGATRON trend at every z.** z = 9 (all three): M* 6.6e7 / 2.0e7 / 1.3e7, f_esc RT 0.07 / 0.14 /
  0.31, x_HII 0.0062 / 0.0078 / **0.0109** (slope 5x -> 10x -1.7). z = 8.1 (2x / 5x): f_esc 0.02 / 0.14 (slope -1.6), x_HII
  0.011 / 0.012. z = 7.3 (2x / 5x): M* 2.6e8 / 6.9e7, f_esc 0.03 / 0.06, x_HII 0.015 / 0.023. Still ~10x below series A 2x.
- M_max pair at z = 7.3: same M* (5.6e7), f_esc 0.41 vs 0.32, x_HII 0.079 vs 0.041 (+90%, steady since z = 9).
- Production h2 runs finished at z = 5: `h2_eps0.3_mech_n10_snx2` x_HII 0.35, `h2_eps0.03n0.5c0.1_mech_snx2` x_HII 0.44
  (thermal twin 0.96); `h2_eps0.03_mech_snx2_t20` at z = 5.01. These use the old constant-SFR M_max 100 table.

## 2026-11-23 (12:50): FB campaign, first z = 8.1 points (series A 2x / 4x, M_max pair)
`comparisons/compare_fbw_A_z8.09`, `comparisons/compare_fbw_M_z8.09`, `comparisons/fbw_trend/fbtrend_a0.110.*`
- **Series A 2x keeps pulling ahead: x_HII 0.115 at z = 8.1** vs 0.054 for 4x (2.5x more stars, 8.9e7 vs 3.5e7 Msun;
  f_esc RT 0.23 vs 0.48, slope -0.77: partial MEGATRON trend, more stars win on x_HII). Its SMHM lies ~0.2-0.3 dex
  above the extrapolated Behroozi+19 relation at 1-2e9 Msun (4x: on / just below it); f_esc ~0.6 below 1e8 Msun, falling
  to 0.15-0.25 at 1-2e9 Msun (CoDa: 0.5 at 1e9).
- For scale at z = 8.09 (older runs, 5 Myr constant-SFR M_max 100 table, `compare_tsn_z8.09`): thermal FB with the same
  eps had x_HII 0.102 with M* 3.0e8 Msun. **Series A 2x ionizes more with 3.4x fewer stars**: closest to the MEGATRON
  picture across recipes so far (mech + M_max 300 vs thermal + M_max 100).
- M_max pair: 300 vs 100 gives x_HII 0.054 vs 0.029 (+90%, as at z = 9), escaping rate +57%, same M*, f_esc 0.48 vs 0.43.
- Update 13:50: **series A complete at z = 8.1**: 2x / 4x / 10x M* 8.9e7 / 3.5e7 / 1.8e7, f_esc RT 0.23 / 0.48 / 0.62,
  x_HII **0.115** / 0.054 / 0.065. Same ranking as at z = 9 (2x > 10x > 4x); 10x vs 4x is the full MEGATRON step, 2x vs
  4x the partial one. Series B 5x: M* 3.9e7, f_esc 0.14, x_HII 0.012 (2x, 10x not there yet). Queue stalled again
  (10 chain jobs pending, estimated 15:40-16:40). No crashes; the 7 campaign runs
  restarted ~11:30 after the queue stall. `h2_eps0.03_mech_snx2_t3` finished at z = 5 with x_HII 0.22 (t10 twin 0.30).

## 2026-11-23 (11:30): campaign figures captioned with the series and closest MEGATRON recipe
- Every `compare_fbw_*` figure now carries a caption (new `compare_dashboard.py --title`): series A and pair M = smooth SF
  (closest MEGATRON recipe: smooth), series B = bursty SF (closest MEGATRON recipe: bursty; its eps 0.3 is also high).
  `fbtrend_*` legends are prefixed with the series key and list the series definitions; its verdict line now separates
  the partial trend (f_esc anticorrelated with M*) from the full one (x_HII also rises as M* falls). All z = 10.1 and z = 9
  figures regenerated.
- PO's reading: series B reproduces the trend but ionizes far less than series A; series A with 2x SN looks closest to
  working out in M*, f_esc and x_HII at once.
- `auto_fbw.sh` restarted (state kept) with the captions and with its dashboard jobs on the debug QOS (~2 min each; the
  batch queue is stalled and `auto_tsn.sh` no longer uses the debug job).

## 2026-11-23 (11:00): FB campaign at z = 9; series B shows the full MEGATRON trend, series A a partial one
`comparisons/compare_fbw_{A,B,M}_z9.00`, `comparisons/compare_fbw_B_z10.11` (10x added), `comparisons/fbw_trend/fbtrend_a0.{090,100}.*`
- **Series B (bursty: eps 0.3, n_th 10, t3) is MEGATRON-like at every step.** At z = 10.1 (2x / 5x / 10x SN): M* 2.8e7 /
  1.0e7 / 7.5e6 Msun, f_esc RT 0.046 / 0.100 / 0.245 (M1 0.023 / 0.070 / 0.164), x_HII 0.0042 / 0.0049 / **0.0072**.
  The 5x -> 10x slope d log f_esc / d log M* is **-2.9** (RT and M1): f_esc rises faster than 1/M*, so the run with the
  fewest stars also has the highest escaping photon rate. At z = 9 (2x / 5x; 10x not there yet): M* 6.6e7 / 2.0e7,
  f_esc 0.07 / 0.14, x_HII 0.0062 / **0.0078**.
- But series B reionizes 5-8x less than series A: bursty SF keeps f_esc low (0.05-0.25) until FB clears the gas.
- **Series A (smooth: eps0.03n0.5c0.1, t10) at z = 9: partial MEGATRON trend.** 2x / 4x / 10x: M* 4.7e7 / 2.3e7 / 1.3e7,
  f_esc RT 0.30 / 0.52 / 0.57, x_HII **0.061** / 0.040 / 0.052. The f_esc-M* anticorrelation is there (monotonic at z = 10.1
  and z = 9: higher M* -> lower f_esc), but it is too shallow (slope > -1) for x_HII to follow: f_esc saturates near 0.5-0.6
  from 4x on, so stronger FB mostly removes photons. The 10x run led x_HII(z) until z ~ 10 and the 2x run overtook it at z ~ 9.8. Slopes -0.75 (2x -> 4x),
  -0.17 (4x -> 10x).
- So both series show the anticorrelation (stronger FB -> lower M*, higher f_esc); the full trend (slope < -1, x_HII rising
  as M* falls) appears where f_esc is far from saturation (bursty, dense SF), so FB has room to raise it. Where f_esc is
  already ~0.5 (smooth SF, mech FB, 1e8-1e9 Msun halos), the slope is shallow and M* wins on x_HII.
- M_max pair at z = 9: M_max 300 gives x_HII 0.040 vs 0.021 (+90%; +77% at z = 10.1), escaping rate +68%, and now a higher
  f_esc too (0.52 vs 0.41 RT; equal at z = 10.1).
- Queue stalled again from ~10:00 (chain jobs estimated to start 14:00-16:00). The pending dashboard jobs were moved to the
  debug QOS with `scontrol update` (same job id, watcher unaffected).

## 2026-11-23 (08:00): FB campaign, series A and B at z = 10.1
`comparisons/compare_fbw_A_z10.11`, `comparisons/compare_fbw_B_z10.11`, `comparisons/fbw_trend/fbtrend_a0.090.*`
- **Series A** (eps0.03n0.5c0.1, mech, t10, M_max 300; SN energy 2x / 4x / 10x): stronger FB removes stars cleanly
  (M* 2.4e7 / 1.4e7 / 8.7e6 Msun; SMHM down ~2x per step at 1e8-1e9 Msun) and raises f_esc (RT 0.44 / 0.52 / 0.63; the
  10x run reaches f_esc ~ 1 above 2e8 Msun). x_HII 0.032 / 0.026 / **0.034**: **not monotonic**. 10x vs 4x is
  MEGATRON-like (fewer stars, more ionization), 4x vs 2x is not. The slopes d log f_esc / d log M* are only -0.3 to -0.4 (RT).
- The 10x run has the highest x_HII but the *lowest* escaping photon rate at this snapshot (1.4e52 vs 4.8e52 ph/s for 2x).
  x_HII integrates the history (10x has been on top since z ~ 15), and weaker clumping / fewer recombinations around the
  sources could also help. One snapshot of the escaping rate does not rank the runs; the z = 9 point will tell.
- **Series B** (eps 0.3, n_th 10, mech, t3, M_max 300; 2x / 5x): 2.8x fewer stars with 5x SN, f_esc doubles (0.05 -> 0.10 RT,
  0.02 -> 0.07 M1, slope -0.75 RT / -1.09 M1), x_HII 0.0042 -> 0.0049: **MEGATRON-like, marginally** (M1 slope beyond -1).
  But bursty SF traps photons: f_esc 5-10x lower than series A and x_HII 6-8x lower. The 10x run is at z ~ 10.8.
- Production h2 runs: `h2_eps0.03_mech_snx2` finished at z = 5 with x_HII 0.30 (thermal twin with density-dependent eps:
  0.96). Others at z ~ 5.3-6.0; `h2_eps0.3_mech_n10_snx2_t10` at z ~ 8.2.

## 2026-11-23 (later): FB campaign, first point: BPASS M_max 100 vs 300 at z = 10.1
`comparisons/compare_fbw_M_z10.11`, `comparisons/fbw_trend/fbtrend_a0.090.*`
- Twins eps0.03n0.5c0.1_mech_snx4_t10 with the SSP M_max = 100 / 300 tables: same stars (M* 1.45e7 / 1.37e7 Msun, SMHM
  identical), same f_esc (0.52 ray-traced, 0.43-0.44 M1, flat ~0.5 from 1e8 to 1e9 Msun, on the CoDa 1e9 value),
  **+30% intrinsic and escaping photons** (3.8e52 vs 2.9e52 ph/s) and **x_HII 0.026 vs 0.015 (+77%)**. M_max 300 shifts
  x_HII(z) by ~0.15 dex at all z < 15: more photons right after each burst (1.9x at 1 Myr), when f_esc is highest.
- For scale at z = 10.1 (older 5 Myr constant-SFR M_max 100 table): mech snx2 x_HII 0.014, thermal (same eps) 0.022.
  With M_max 300 and 4x SN the mechanical run is already ahead of the thermal one.
- UV LF: no galaxies brighter than M_UV ~ -13 yet (4 cMpc/h box); no constraint at this z.
- The other campaign runs (series A snx2 / snx10, series B) are at z ~ 9.9-11.4 (5th job); their z = 10.1 dashboards follow.

## 2026-11-23: first h2 run finished (z = 5): eps0.03n0.5c0.1_th_t10_h2
`comparisons/compare_h2_z5`, `dashboards/h2_epsn0.03c0.1`
- Thermal FB, density-dependent eps (0.03 (n/n_th)^0.5 <= 0.1), production hydro: **x_HII 0.96 at z = 5** (0.25 at z = 7,
  through the Hoag+19 point at z ~ 7.6; below the Davies/Mason z ~ 7 points). Best reionization history so far.
- vs the same recipe in 1st-order hydro: 16% fewer stars (7.0e9 vs 8.3e9 Msun in halos), same intrinsic photon rate,
  **2.2x higher global f_esc** (0.035 vs 0.016; f_esc(1e10 Msun) 0.03-0.05 vs ~0.01, on the CoDa value), x_HII 0.96 vs 0.88.
  So the hydro lever gives the MEGATRON-like direction here (fewer stars, more ionization), unlike the FB levers so far.
- Still too many stars: CSFRD ~0.5 dex above Bouwens+14 at z = 6-8, SMHM ~0.5-1 dex above Behroozi at 1e10 Msun, UV LF
  above Bouwens at M_UV > -18. Next step for this recipe: fewer stars at fixed f_esc.
- vs eps 0.01 (dyablo/RAMSES matched): similar M* (1e10) but f_esc 6x higher -> x_HII 0.96 vs 0.31 / 0.43.

## 2026-11-23: t_SNII scan at z = 8.09; Frontier queue stalled the weekend campaign
`comparisons/compare_tsn_z8.09` (+ `fbtrend_a0.110.{txt,png}`)
- t_SNII stays a weak lever at z = 8.09 (eps 0.03, mech, 2x SN; t_SNII 3 / 10 / 20 Myr): M* 9.0e7 / 9.8e7 / 1.17e8 Msun
  (M* ~ t_SNII^0.14), x_HII 0.024 / 0.032 / 0.039. Longer delay -> more stars -> more ionization, as at z = 9.
- t3 has the highest instantaneous ray-traced f_esc (0.15 vs 0.12) and escaping rate (3.5e52 vs 2.5e52 ph/s) at this
  snapshot, yet the lowest x_HII: x_HII integrates the whole history, and t3 was already behind at z = 9 (0.015 vs 0.019).
  One snapshot of f_esc is noisy (M1 ranks the runs the other way: 0.11 / 0.12 / 0.14).
- Mechanical vs thermal (density-dependent eps): 3.6x fewer stars, 1.6x higher f_esc (RT), x_HII 0.036 vs 0.102.
  Slope d log f_esc / d log M* = -0.35 (RT) / -0.25 (M1): further from the MEGATRON regime (< -1) than at z = 9
  (-0.8 / -0.5), and the x_HII gap grows (2.2x at z = 9, 2.9x now). Only the thermal run is near the Hoag+19 point.
- Weekend FB campaign (series A / B, M_max pair): queued from 2026-11-20 10:30 to 2026-11-22 ~21:45 behind 1920- and
  4096-node jobs (~500-600 small jobs ahead, shorter walltime gave no earlier start). All 7 runs started their 1st job
  then; at 2026-11-23 01:00 they are at z ~ 13-15 (2nd job). First FB-trend point (z = 10.1) expected within a day.

## 2026-11-20 (later): weekend FB-strength campaign launched (looking for the MEGATRON trend)
- Goal (PO): find a regime where stronger FB gives lower M* but f_esc rising faster than 1/M*, so x_HII(z) is *higher*
  (MEGATRON, Choustikov+2026). Levers ranked (KB reds_feedback_sf.md): E_SN, mech vs thermal, hydro order, M_max strong;
  t_SNII weak (z = 9 scan: M* ~ t_SNII^0.2).
- All runs: production hydro (build_avg, runtime averages.txt), mechanical FB, eta_SNII 0.2, SSP BPASS M_max = 300 table.
  - **Series A** (smooth SF: eps 0.03 (n/n_th)^0.5 <= 0.1, n_th 0.1, t_SNII 10 Myr): snx2 / snx4 / snx10
    (4e49 / 8e49 / 2e50 erg/Msun; snx10 = hypernova-like, beyond MEGATRON).
  - **Series B** (bursty SF: eps 0.3, n_th 10, t_SNII 3 Myr = early, HN-like energy): snx2 / snx5 / snx10. Why: in the z = 7
    discs only this recipe cleared its birth regions (transmission up to 0.98), so f_esc has room to respond to FB.
  - M_max pair: `h2_eps0.03n0.5c0.1_mech_snx4_ssp100` vs `_ssp300`.
- Analysis (`runs/reio_v2/auto_fbw.sh`): dashboards at a = 0.090 / 0.100 / 0.110 / 0.120 / 0.130 (z = 10.1 to 6.7) as each run
  passes them (batch QOS), `compare_fbw_<A|B|M>_z<z>` per series, and `fbw_trend/fbtrend_a<a>.{txt,png}`: M*, Ndot, global
  f_esc (ray-traced, M1), escaping rate and x_HII per run, with the slope d log f_esc / d log M* between neighbours
  (MEGATRON-like needs slope < -1 and x_HII rising as M* falls). Reference at z = 9 (existing runs, thermal vs mech,
  eps0.03n0.5c0.1): slope -0.80 (RT) / -0.52 (M1), more stars win.

## 2026-11-20 (later): BPASS M_max = 100 vs 300 twins launched
- New stellar emission tables (PO, remade from BPASS v2.2.1 binary imf135_100 / imf135_300 spectra): single-burst (SSP)
  emissivity + M_AB1600 + UV-slope tables, in `src_files/` (on Frontier: `REDS_src_files/`). The M_max = 100 SSP table is
  identical to the one the dashboard already used for UV magnitudes. At Z = 0.001, M_max = 300 gives 1.9x the ionizing
  rate at 1 Myr and +38% photons per Msun over 200 Myr (1.23e61 vs 8.9e60). Stars younger than 1 Myr (first table age)
  get the 1 Myr value, in dyablo and in the dashboard.
- Twins `h2_eps0.03n0.5c0.1_mech_snx4_ssp100` / `_ssp300`: density-dependent eps (0.03 (n/n_th)^0.5 <= 0.1, n_th 0.1),
  mechanical FB, 4x SN (8e49 erg/Msun, ~2x MEGATRON Bursty), t_SNII 10 Myr, eta_SNII 0.2, production hydro (build_avg,
  runtime averages.txt). Both differ from the snx2 parent in the SN energy and in the emission history (SSP instead of
  5 Myr constant SFR), so compare them with each other. The dashboard takes UV magnitudes from the run's own table.

## 2026-11-20 (later): MEGATRON feedback levers (Choustikov et al. 2026, arXiv:2611.15931; Katz et al. arXiv:2411.07282)
- MEGATRON (RAMSES-RTZ, ~5 pc, zoom on a Milky Way progenitor): the model with the **fewest** galaxies (100% eps_ff in
  lower-density gas + hypernovae) reionizes fastest (volume almost fully ionized at z ~ 8.5, vs 1/3 for the "Efficient"
  model, which has 10x more UV-bright galaxies). Their f_esc rises faster than 1/M*; ours does not
  (d log f_esc / d log M* = -0.8 ray-traced, -0.5 M1, thermal vs mechanical at z = 9), so in our boxes more stars still
  means more ionization.
- Their key timescale: burst -> efficient LyC escape = 2.5 Myr (HN), 4 Myr (Bursty, 5x E_SN), 11 Myr (Efficient). Late
  escape is wasted ("remnant leakers": high f_esc, no young stars). Our global f_esc is photon-weighted, so it already
  discounts them. At 150 pc the birth cloud is one cell and its photons are injected at full luminosity (implicit
  birth-cloud f_esc = 1): resolution favours high-M* runs.
- **Levers** (specific SN energy, eta E_SNII / M_SNII; E_SNII and M_SNII are degenerate in dyablo):

  | model | erg per Msun formed | timing |
  |---|---|---|
  | MEGATRON fiducial (Kroupa, 1e51 per 8-25 Msun star = 1 SN / 115 Msun) | 0.85e49 | individual SNe, ~7-40 Myr |
  | REDS base (eta 0.2, M_SNII 10) | 2e49 | all at t_SNII |
  | REDS `snx2` (most runs) | 4e49 | all at t_SNII |
  | MEGATRON Bursty (5e51 per SN) | 4.2e49 | ~7-40 Myr |
  | MEGATRON HN (>= 25 Msun stars, up to 10x E_SN, mass/Z dependent fraction) | <~3e49 | from ~3.5 Myr |
  | REDS `snx5` (PO: "E_SN up to 10e51", exploration beyond MEGATRON) | 1e50 | all at t_SNII |

  Our `t3` runs are an extreme early-energy (HN-like) case. MEGATRON's space maps onto our (snx, t_SNII) plane.
- **IMF upper mass**: MEGATRON uses BPASS Kroupa binary with M_max = 300 Msun (BPASS `imf135_300`); REDS uses
  M_max = 100 Msun (`cstSFR_5Myr_BPASSv2.2.1_kroupa_binary_MMax=100`, from dashboard_rc). Decision (PO): move to
  M_max = 300 for new runs. No M_max = 300 table exists on disk (dashboard_rc has M_max = 100 only; the RAMSES SED.zip has
  BC03 only; RAMSES `utils/py/sed_utils.py` converts BC03 / Starburst99, not BPASS): needs the BPASS v2.2.1 `imf135_300`
  binary ionizing tables.
- Next diagnostic: f_esc and escaping photon rate vs star-particle age (our own burst -> escape delay).

## 2026-11-20: t_SNII scan at z = 9 (production hydro)
`comparisons/compare_tsn_z9`
- Same snapshot (a = 0.100):

  | recipe | x_HII (vol) | global f_esc ray-traced / M1 | M* in halos [Msun] | Ndot [ph/s] |
  |---|---|---|---|---|
  | eps0.03_mech_snx2_t3_h2 | 0.015 | 0.248 / 0.168 | 4.5e7 | 0.96e53 |
  | eps0.03_mech_snx2_t10_h2 | 0.019 | 0.179 / 0.174 | 5.1e7 | 1.21e53 |
  | eps0.03_mech_snx2_t20_h2 | 0.025 | 0.206 / 0.211 | 6.7e7 | 1.35e53 |
  | eps0.03n0.5c0.1_mech_snx2_t10_h2 | 0.022 | 0.248 / 0.231 | 4.7e7 | 0.87e53 |
  | eps0.03n0.5c0.1_th_t10_h2 | 0.048 | 0.110 / 0.135 | 1.3e8 | 3.6e53 |

- In the box, a longer t_SNII mainly lets more stars form before the first SN (CSFRD of t20 is ~0.15 dex higher at z > 10;
  SMHM up at 1e9 Msun); f_esc moves little and not monotonically (unlike the isolated discs, where t10 raised f_esc 2-3x).
  x_HII rises 1.7x from t3 to t20, still far below the thermal density-dependent recipe.
- Density-dependent eps + mechanical FB: f_esc as high as the best constant-eps case, but 2.8x fewer stars than with
  thermal FB, so half the x_HII. Thermal FB with density-dependent eps remains the only recipe on track at z = 9.

## 2026-11-19 (later): production hydro vs 1st order at z = 8.09
`comparisons/compare_h2_z8.09`
- Same 6 runs at a = 0.110:

  | recipe | x_HII (vol) 1st / h2 | global f_esc ray-traced / M1, 1st -> h2 | M* in halos 1st / h2 |
  |---|---|---|---|
  | eps0.03n0.5c0.1_th_t10 | 0.064 / 0.102 | 0.049 / 0.069 -> 0.111 / 0.132 | 2.6e8 / 3.0e8 |
  | eps0.03_mech_snx2_t10 | 0.013 / 0.032 | 0.076 / 0.082 -> 0.118 / 0.115 | 8.5e7 / 9.8e7 |
  | eps0.3_mech_n10_snx2_t3 | 0.018 / 0.035 | 0.047 / 0.033 -> 0.158 / 0.097 | 9.2e7 / 1.1e8 |

- The h2 f_esc of the mechanical recipes falls between z = 9 and 8.09 (0.18 -> 0.12, 0.24 -> 0.16), so the h2/1st ratio
  drops from 2-5x to 1.5-3x. The thermal density-dependent recipe holds at 0.11. x_HII stays ~2x higher with h2. Only
  the thermal density-dependent recipe is on track (x_HII 0.10 at z = 8.1, Hoag+19 point 0.12 at z = 7.6); the constant-eps
  mechanical ones are 3x lower.

## 2026-11-19: production hydro vs 1st order at z = 9; halo porosity maps
`comparisons/compare_h2_z9`, `maps/porosity_z9`
- Same snapshot (a = 0.100) for the 1st-order and h2 versions of 3 recipes:

  | recipe | hydro | x_HII (vol) | global f_esc ray-traced / M1 |
  |---|---|---|---|
  | eps0.03n0.5c0.1_th_t10 | 1st / h2 | 0.028 / 0.048 | 0.055 / 0.064 -> 0.110 / 0.135 |
  | eps0.03_mech_snx2_t10 | 1st / h2 | 0.007 / 0.019 | 0.079 / 0.086 -> 0.179 / 0.174 |
  | eps0.3_mech_n10_snx2_t3 | 1st / h2 | 0.010 / 0.021 | 0.042 / 0.031 -> 0.235 / 0.158 |

- Same stellar masses and UV LFs; CSFRD of h2 a bit higher at z > 11, converged by z ~ 9 (top of the Bouwens band).
- Halo maps (3 most massive halos, 2-3.3e9 Msun): same gas mass within R200, same volume fraction of diffuse gas, but in
  h2 the HI is broken into clumps / filaments with clear sightlines (several separate SN bubbles inside R200), where 1st
  order gives a smooth HI envelope. Sky fraction with transmission > 0.1 rises from 0-0.15 to 0.2-0.7 in 7 of 9 halo/recipe
  pairs. The bursty n10 recipe is on/off halo by halo (one halo between bursts has f_esc = 0).
- For constant eps, even open directions transmit only 10-46%: the rest is absorbed next to the young stars. Only the
  bursty n10 recipe clears its birth regions (transmission up to 0.98).

## 2026-11-18: t_SNII as a free parameter; t_SNII scan launched
- At 150-250 pc much of the physics that sets f_esc is unresolved or missing (delayed / multiple SNe, pre-SN feedback,
  cosmic rays, porosity / Kimm+15 mass loading). Decision (PO): tune one effective parameter that carries it, not
  necessarily at a physically defensible value: **t_SNII**.
- Isolated z = 7 discs (`discs_z7/z7_tsn.png`): at fixed SN energy, t_SNII = 10 Myr gives a higher f_esc than 3 Myr (b = 2:
  M1 f_esc 0.80 vs 0.24 at 1e9 Msun, 0.30 vs 0.14 at 1e10); t10 quenches SF at boost >= 4. Delayed feedback makes SF
  bursty and the blow-out coherent.
- **Hidden parameter**: all `eps0.3_mech_n10*` runs had t_SNII = 3 Myr (all others 10). Plot labels now carry FB type and t_SNII.
- Launched (h2): `h2_eps0.03_mech_snx2_t3`, `_t20` (vs t10), `h2_eps0.3_mech_n10_snx2_t10` (vs t3), and
  `h2_eps0.03n0.5c0.1_mech_snx2` (density-dependent eps + mechanical FB, 2x SN).

## 2026-11-18: z = 5 results (1st-order calibration runs; dyablo production vs RAMSES)
`comparisons/compare_cf_z5`, `compare_epsn_z5`, `compare_cmp_ramses_z5`
- dyablo production hydro reproduces RAMSES-RT galaxies at matched settings (eps 0.01, thermal): CSFRD, SMHM and UV LF
  overlap; x_HII 0.31 (dyablo) vs 0.43 (RAMSES). Both ~0.5 dex above the Bouwens CSFRD at eps = 0.01.
- Constant-eps mechanical recipes sit on the Bouwens CSFRD but reionize far too late (x_HII 0.09-0.34 at z = 5).
- eps0.03n0.5c0.1_th_t10 (density-dependent eps): x_HII 0.88 at z = 5, but too many stars (SMHM ~3e8 at 1e10 Msun).
- CoDa III-like (dx 11.6 ckpc): x_HII 0.72 at z = 5; late. Suspects: c_rad 0.01 c (CoDa III used full c), small box.
- f_esc gaps in the plots: mass bins with fewer than 3 halos emitting ionizing photons (halos < 1e8 Msun mostly starless:
  atomic-cooling limit, no H2 cooling).

## 2026-11-14 to 17: hydro validation (`idealised_test_cases/`, `reports/2026-11-17_hydro_validation.pdf`)
- 1st-order dyablo over-heated pre-shock gas and under-produced shocks in small halos; RAMSES pressure_fix (any beta) and
  Tep-style entropy switch (eta 0.1) kill shock heating in moving frames (Galilean pancake) and leave < 1e8 Msun halos
  cold. Production recipe: RK2 + minmod, no dual-energy switch, e_int-conserving remap, RAMSES-like refinement,
  smallp 1e-50, Compton cooling, adiabat fallback for negative pressure -> passes all 4 tests (`h2_` runs).
