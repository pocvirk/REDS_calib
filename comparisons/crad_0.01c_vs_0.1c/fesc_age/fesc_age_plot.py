"""Plots of fesc_age.py: c_rad 0.01c vs 0.1c (PO 2026-11-26).
fig 1 <out>_age.png : photon-weighted ray-traced f_esc vs stellar age, per halo mass bin (top), share of intrinsic photons per age bin (bottom)
fig 2 <out>_gas.png : gas around young (< 5 Myr) star particles: median n_H(r), x_HI(r) (volume-weighted), CDF of x_HI (mass-weighted, < 0.3 pkpc)
<out>.txt           : the numbers
usage: python fesc_age_plot.py <npz dir> <out prefix>
"""
import sys, glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D, out = sys.argv[1], sys.argv[2]
F = "h2_eps0.03n0.5c0.1_mech_snx2_ssp300"
RUNS = [(F, "fiducial c_rad 0.01c", "-"), (F + "_crad0.1", "c_rad 0.1c (reion_accel)", "--")]
AS = ["0.13", "0.145", "0.1667"]
AGE = np.array([0, 1, 2, 3, 5, 7, 10, 15, 20, 30, 50])
MB = [(7.0, 8.5, "C0"), (8.5, 9.5, "C1"), (9.5, 11.0, "C3")]
TITLE = "smooth SF eps0.03 (n/n_th)^0.5, mech FB 2x SN, t_SNII 10 Myr, BPASS M_max 300 (closest MEGATRON recipe: smooth), 4 cMpc/h"
dat = {(r, A): np.load(f"{D}/{r}_a{A}.npz", allow_pickle=True) for r, _, _ in RUNS for A in AS if glob.glob(f"{D}/{r}_a{A}.npz")}
AS = [A for A in AS if all((r, A) in dat for r, _, _ in RUNS)]
txt = open(out + ".txt", "w")

# ---- fig 1
fig = plt.figure(figsize=(5 * len(AS) + 3.2, 7.6)); gs = fig.add_gridspec(2, len(AS) + 1, height_ratios=[1.6, 1], width_ratios=[1] * len(AS) + [0.62])
ac = 0.5 * (AGE[1:] + AGE[:-1])
for j, A in enumerate(AS):
    a1 = fig.add_subplot(gs[0, j]); a2 = fig.add_subplot(gs[1, j], sharex=a1)
    for r, lab, ls in RUNS:
        g = dat[(r, A)]; age, nd, fs, hmh = g["age"], g["ndot"], g["fesc_star"], g["host_mh"]
        ok = np.isfinite(fs) & (nd > 0)
        tot = nd[ok].sum(); gl = np.sum(fs[ok] * nd[ok]) / tot
        txt.write(f"== {lab} z={float(g['z']):.2f}: global photon-weighted fesc_RT {gl:.4f}\n")
        for lo, hi, col in MB:
            mm = ok & (np.log10(np.where(np.isfinite(hmh), hmh, 1)) >= lo) & (np.log10(np.where(np.isfinite(hmh), hmh, 1)) < hi)
            y = []; sh = []
            for a0, a9 in zip(AGE[:-1], AGE[1:]):
                s = mm & (age >= a0) & (age < a9)
                y.append(np.sum(fs[s] * nd[s]) / nd[s].sum() if nd[s].sum() > 0 and s.sum() >= 3 else np.nan); sh.append(nd[s].sum() / tot)
            a1.plot(ac, y, ls, marker="o", ms=3, color=col, lw=1.6, label=f"{lab}, log Mh {lo}-{hi}")
            a2.plot(ac, sh, ls, marker="o", ms=3, color=col, lw=1.4)
            fm = np.sum(fs[mm] * nd[mm]) / max(nd[mm].sum(), 1e-99)
            txt.write(f"  log Mh {lo}-{hi}: fesc {fm:.3f}, photon share {nd[mm].sum() / tot:.3f}; fesc per age bin " +
                      " ".join(f"[{a0}-{a9}] {v:.3f}" for a0, a9, v in zip(AGE[:-1], AGE[1:], y)) + "\n")
        y = []
        for a0, a9 in zip(AGE[:-1], AGE[1:]):
            s = ok & (age >= a0) & (age < a9); y.append(np.sum(fs[s] * nd[s]) / nd[s].sum() if nd[s].sum() > 0 else np.nan)
        a1.plot(ac, y, ls, color="k", lw=2.4, label=f"{lab}, all halos")
        txt.write("  all halos: fesc per age bin " + " ".join(f"[{a0}-{a9}] {v:.3f}" for a0, a9, v in zip(AGE[:-1], AGE[1:], y)) + "\n")
    a1.set_yscale("log"); a1.set_ylim(3e-3, 1.1); a1.grid(alpha=0.3); a1.set_title(f"z = {1 / float(A) - 1:.2f}", fontsize=10)
    a1.set_ylabel("photon-weighted f_esc (ray-traced, R200)"); a2.set_yscale("log"); a2.set_ylim(1e-4, 1); a2.grid(alpha=0.3)
    a2.set_ylabel("share of intrinsic ionizing photons"); a2.set_xlabel("stellar age [Myr]"); a2.set_xscale("log"); a2.set_xlim(0.4, 45)
    if j == 0: h_, l_ = a1.get_legend_handles_labels()
lax = fig.add_subplot(gs[:, -1]); lax.axis("off"); lax.legend(h_, l_, loc="center left", fontsize=7.5, frameon=False)
fig.suptitle("Test 1: f_esc by stellar age, c_rad 0.01c (solid) vs 0.1c (dashed). " + TITLE, fontsize=8.5)
fig.tight_layout(rect=(0, 0, 1, 0.97)); fig.savefig(out + "_age.png", dpi=110); plt.close(fig)

# ---- fig 2
fig = plt.figure(figsize=(5 * len(AS) + 3.2, 11)); gs = fig.add_gridspec(3, len(AS) + 1, width_ratios=[1] * len(AS) + [0.62])
for j, A in enumerate(AS):
    ax = [fig.add_subplot(gs[i, j]) for i in range(3)]
    for r, lab, ls in RUNS:
        g = dat[(r, A)]; y = g["young"]; hmh = g["host_mh"][y]; re = g["redges"]; rc = np.sqrt(re[1:] * re[:-1])
        txt.write(f"== {lab} z={float(g['z']):.2f}: young (< 5 Myr) star particles profiled: {len(y)}\n")
        for lo, hi, col in MB:
            m = (np.log10(hmh) >= lo) & (np.log10(hmh) < hi)
            if m.sum() < 5: continue
            pn = np.nanmedian(g["prof_nH"][m], 0); px = np.nanmedian(g["prof_xHI"][m], 0)
            ax[0].plot(rc, pn, ls, color=col, lw=1.6, label=f"{lab}, log Mh {lo}-{hi} (N={m.sum()})")
            ax[1].plot(rc, px, ls, color=col, lw=1.6)
            xs = np.sort(g["xHI_r"][m, 1][np.isfinite(g["xHI_r"][m, 1])])
            ax[2].plot(xs, np.arange(1, len(xs) + 1) / len(xs), ls, color=col, lw=1.6)
            txt.write(f"  log Mh {lo}-{hi}: N={m.sum()}, median host-cell n_H {np.nanmedian(g['cell_nH'][m]):.3g}, x_HI {np.nanmedian(g['cell_xHI'][m]):.3g}; "
                      f"<0.1 pkpc n_H {np.nanmedian(g['nH_r'][m, 0]):.3g} x_HI {np.nanmedian(g['xHI_r'][m, 0]):.3g}; "
                      f"<0.3 pkpc n_H {np.nanmedian(g['nH_r'][m, 1]):.3g} x_HI {np.nanmedian(g['xHI_r'][m, 1]):.3g}; "
                      f"fraction with x_HI(<0.3) < 0.1: {np.mean(xs < 0.1):.2f}\n")
    for x in ax[:2]: x.set_xscale("log"); x.set_yscale("log"); x.grid(alpha=0.3)
    ax[0].set_title(f"z = {1 / float(A) - 1:.2f}: gas around star particles < 5 Myr", fontsize=10)
    ax[0].set_ylabel("median n_H(r) [cm^-3] (volume-weighted shell)"); ax[1].set_ylabel("median x_HI(r) (HI / H in shell)")
    ax[1].set_xlabel("r [pkpc] from the star particle"); ax[1].set_ylim(1e-6, 1.5)
    ax[2].set_xscale("log"); ax[2].set_xlim(1e-6, 1.05); ax[2].grid(alpha=0.3); ax[2].set_xlabel("x_HI (mass-weighted, r < 0.3 pkpc)"); ax[2].set_ylabel("cumulative fraction of young star particles")
    if j == 0: h_, l_ = ax[0].get_legend_handles_labels()
lax = fig.add_subplot(gs[:, -1]); lax.axis("off"); lax.legend(h_, l_, loc="center left", fontsize=7.5, frameon=False)
fig.suptitle("Test 2: gas around young stars, c_rad 0.01c (solid) vs 0.1c (dashed). " + TITLE, fontsize=8.5)
fig.tight_layout(rect=(0, 0, 1, 0.97)); fig.savefig(out + "_gas.png", dpi=110); plt.close(fig)
print("wrote", out + "_age.png", out + "_gas.png", out + ".txt")
