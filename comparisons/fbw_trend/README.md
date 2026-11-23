# fbw_trend

FB-strength campaign summary (`scripts/fbtrend.py`, run by `scripts/auto_fbw.sh` after each new dashboard), one file per
target a = 0.090 / 0.100 / 0.110 / 0.120 / 0.130 (z = 10.1 / 9 / 8.1 / 7.3 / 6.7). Per run: total M* in halos, intrinsic
ionizing rate, photon-weighted global f_esc (ray-traced; M1), escaping rate and volume x_HII (runtime `averages.txt`).
Per series (A: smooth SF t10 snx2/4/10; B: bursty n10 t3 snx2/5/10; M: M_max 100 vs 300), runs ordered by M*:
slope d log f_esc / d log M* between neighbours. MEGATRON-like = the lower-M* run has the higher x_HII (needs slope < -1).
Panels: x_HII(z), f_esc vs M* (dotted: f_esc ~ 1/M*, equal escaping photons), x_HII vs M*, escaping rate vs M*.
The snx4_ssp300 run belongs to both series A and pair M (labelled A).
