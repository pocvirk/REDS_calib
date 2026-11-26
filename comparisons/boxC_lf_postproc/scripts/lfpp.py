"""boxC UV LF post-processing variants (PO request 2026-11-26; post-processing only, nothing in dyablo).
Input: npz from extract.py (b=0.15 FoF halos, stars within R200, initial masses, ages); BPASS v2.2.1 SSP M_max=300 mag table.
Variants of the intrinsic M_AB1600 per halo:
  (1) aperture: only stars within r_ap (1 and 0.5 physical kpc) of the brightest finest-level cell (dx = L/(bx 2^lmax),
      stellar L1600 binned on that grid; stars form at lmax) instead of all stars within R200
  (2a) constant metallicity for all stars: Z = 1e-4 ... 0.02 (baseline dashboard: Z = 0.001 = 0.05 Zsun)
  (2b) Z(M*) from JWST gas-phase MZRs at z ~ 4-10 applied to each halo's M* (all its stars get the halo Z);
       Z = 0.0142 * 10^(12+log(O/H) - 8.69) (Asplund+09)
  (3) dust: A_1600(M_UV) laws applied to the intrinsic baseline mags, + the attenuation required to match an observed LF
      (abundance matching of cumulative number densities).
usage: python -I lfpp.py <out prefix> <npz> [<npz> ...]
"""
import sys
import numpy as np
B = "/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026"
sys.path.insert(0, B + "/analysis/dyablo_tools/dashboard_dyablo_reio")
from dashboard_reio_dyablo import obs_uvlf as O
from dashboard_reio_dyablo.rc import dashboard_tools_galaxies as dbtg
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LMAX = 11
ZCONST = [1e-4, 1e-3, 2e-3, 4e-3, 8e-3, 2e-2]
# 12+log(O/H)(log M*): JWST gas-phase MZRs
MZR = {"Curti+24 (JADES, z 3-10)": lambda x: 7.72 + 0.17 * (x - 8),                      # A&A 684 A75, low-mass fit
       "Nakajima+23 (z 4-10)": lambda x: 8.24 + 0.25 * (x - 10),                          # ApJS 269 33, Eq. 1
       "Chemerynska+24 (lensed, z 6-8)": lambda x: -0.076 * x**2 + 1.61 * x - 0.26}       # ApJL 976 L15, quadratic
def oh2z(oh): return np.clip(0.0142 * 10 ** (oh - 8.69), 1e-5, 0.04)

# Bouwens+14 beta(M_UV) (ApJ 793 115): beta(-19.5), dbeta/dM at z ~ 6, 7; Meurer+99 IRX-beta with sigma_beta = 0.34 scatter
B14 = {6: (-2.00, -0.20), 7: (-2.05, -0.20)}
def a_meurer(M, z):
    zz = np.clip(z, 6, 7); f = zz - 6
    b0 = (1 - f) * B14[6][0] + f * B14[7][0]; db = (1 - f) * B14[6][1] + f * B14[7][1]
    beta = b0 + db * (M + 19.5)
    return np.maximum(0, 4.43 + 0.79 * np.log(10) * 0.34**2 + 1.99 * beta)
def a_park(M, z):   # Park+26 (arXiv:2604.26331), CoDa III, after Ocvirk+25 calibration: only M_int < -21
    return np.maximum(0, -(M + 21) / 2.5)
def a_casey(M, z, ms):   # Casey+26 (arXiv:2606.17270) Table 1, Eq. 11 for A_UV(log M*, z), clipped at 0 (fit to COSMOS/JWST, 0<z<8)
    x = np.log10(np.maximum(ms, 1.0))
    return np.maximum(0, 16.33 / (1 + np.exp(-0.970 * (x - 11.652))) - np.exp(-8.84 + 0.722 * x) * (1 + z))
DUST = {"Park+26 CoDa III (Ocvirk+25 calib.)": lambda M, z, ms: a_park(M, z),
        "Meurer+99 IRX-beta + Bouwens+14 beta(M_UV)": lambda M, z, ms: a_meurer(M, z),
        "Casey+26 A_UV(M*, z) (sim M*)": a_casey}
# targets for the required attenuation: Atek+26 GLIMPSE z~7 (dashboard fit), Bouwens+21 HST z~7 Schechter (2102.07775 Table)
TARGETS = {"Atek+26 fit": (-3.68, -21.29, -1.98), "Bouwens+21 z~7 fit": (np.log10(0.19e-3), -21.15, -2.06)}

T = None
def mag_tab(f):
    global T
    if T is None:
        T = dbtg.gen_age_Z_interpolator(f)[0]
    return T

def halo_sum(v, off):
    """sum of member values per halo (off: CSR offsets), 0 for empty halos"""
    c = np.concatenate([[0], np.cumsum(v)])
    return c[off[1:]] - c[off[:-1]]

def tomag(L): return np.where(L > 0, -2.5 * np.log10(np.where(L > 0, L, 1)), np.nan)

def analyse(fn):
    d = np.load(fn, allow_pickle=True)
    z = float(d["z"]); a = float(d["aexp"]); lbox = float(d["lbox"]); off = d["off"]; fl = d["flat"]
    tab = mag_tab(str(d["mag_file"]))
    mi, age, ms, pos = d["sm_init"][fl], d["sage"][fl], d["smass"][fl], d["spos"][fl]
    hk = np.repeat(np.arange(len(off) - 1), np.diff(off))           # halo index of each member entry
    Mstar = halo_sum(ms, off)
    out = {"z": z, "lbox": lbox, "hm": d["hm"], "Mstar": Mstar}
    Lb = mi * 10 ** (-0.4 * tab(age, 1e-3))
    out["base"] = tomag(halo_sum(Lb, off))
    # (1) apertures around the brightest finest-level cell
    dx = lbox / (int(d["bx"]) * 2**LMAX)
    ijk = np.floor(pos / dx).astype(np.int64) % int(round(lbox / dx))
    for rp in (1.0, 0.5):
        rc = rp * 1e-3 / a                                           # physical kpc -> comoving Mpc
        Lap = np.zeros(len(off) - 1)
        for k in np.where(np.diff(off) > 0)[0]:
            s = slice(off[k], off[k + 1])
            key = ijk[s, 0] * 2**40 + ijk[s, 1] * 2**20 + ijk[s, 2]
            u, inv = np.unique(key, return_inverse=True)
            j = np.argmax(np.bincount(inv, weights=Lb[s]))
            c = (ijk[s][inv == j][0] + 0.5) * dx
            dr = (pos[s] - c + 0.5 * lbox) % lbox - 0.5 * lbox
            Lap[k] = Lb[s][np.sum(dr**2, axis=1) <= rc**2].sum()
        out[f"ap{rp:g}"] = tomag(Lap)
    # (2a) constant Z
    for Z in ZCONST:
        out[f"Z{Z:g}"] = tomag(halo_sum(mi * 10 ** (-0.4 * tab(age, Z)), off))
    # (2b) MZR
    lm = np.log10(np.maximum(Mstar, 1.0))
    for nm, f in MZR.items():
        Zh = oh2z(f(lm))
        out["mzr:" + nm] = tomag(halo_sum(mi * 10 ** (-0.4 * tab(age, Zh[hk])), off))
        out["Zh:" + nm] = Zh
    # (3) dust
    for nm, f in DUST.items():
        out["dust:" + nm] = out["base"] + f(out["base"], z, Mstar)
    return out

def required_A(mags, lbox, target, Mgrid):
    """A(M_int) such that n_sim(< M_int) = n_obs(< M_int + A); nan where the sim has < 3 objects brighter"""
    V = lbox**3; m = np.sort(mags[np.isfinite(mags)])
    Mo = np.linspace(-26, -8, 3601); phi = O.schechter(Mo, *target)
    nob = np.concatenate([[0], np.cumsum(0.5 * (phi[1:] + phi[:-1]) * np.diff(Mo))])      # n(< M), increasing with M
    res = np.full(len(Mgrid), np.nan)
    for i, M in enumerate(Mgrid):
        N = np.searchsorted(m, M)
        if N < 3: continue
        res[i] = np.interp(N / V, nob, Mo) - M
    return res

def lf(m, lbox):
    mm, p, e, n = O.sim_lf(m[np.isfinite(m)], lbox); s = n > 0
    return mm[s], p[s], (e[0][s], e[1][s]), n[s]

def main():
    pre = sys.argv[1]; R = [analyse(f) for f in sys.argv[2:]]
    data = O.load()
    title = ("boxC 8 cMpc/h, fiducial reio model (smooth SF eps0.03 (n/n_th)^0.5, mech FB 2x SN, t_SNII 10 Myr, BPASS SSP M_max 300; "
             "closest MEGATRON recipe: smooth); b=0.15 FoF. Baseline = dashboard: stars in R200, Z=0.001, no dust. Post-processing only.")
    cols = ["aperture", "constant Z (all stars)", "Z(M*) from JWST MZRs", "dust A_1600(M_UV)"]
    fig, axs = plt.subplots(len(R), 4, figsize=(19, 4.3 * len(R)), sharey=True, squeeze=False)
    Mg = np.arange(-20.5, -13.9, 0.25)
    txt = open(pre + ".txt", "w")
    for r, row in zip(R, axs):
        z, L = r["z"], r["lbox"]
        for ax, c in zip(row, cols):
            O.plot_obs(ax, z, data)
            m, p, e, n = lf(r["base"], L)
            ax.plot(m, p, "-", color="k", lw=2.2, label="baseline (R200, Z=0.001)", zorder=5)
            ax.fill_between(m, np.maximum(e[0], 1e-8), e[1], color="k", alpha=0.15, lw=0, zorder=4)
            ax.set_title(f"z = {z:.2f}: {c}", fontsize=10)
        V = [("ap1", "1 pkpc around brightest cell", "C3"), ("ap0.5", "0.5 pkpc around brightest cell", "C1")]
        for k, lab, col in V:
            m, p, e, n = lf(r[k], L); row[0].plot(m, p, "-", color=col, lw=1.8, label=lab, zorder=6)
        cm = plt.get_cmap("plasma")
        for i, Z in enumerate(ZCONST):
            if Z == 1e-3: continue
            m, p, e, n = lf(r[f"Z{Z:g}"], L)
            row[1].plot(m, p, "-", color=cm(i / len(ZCONST)), lw=1.6, label=f"Z = {Z:g} ({Z / 0.02:g} Zsun)", zorder=6)
        for (nm, _), col in zip(MZR.items(), ["C2", "C4", "C9"]):
            m, p, e, n = lf(r["mzr:" + nm], L); row[2].plot(m, p, "-", color=col, lw=1.8, label=nm, zorder=6)
        for (nm, _), col in zip(DUST.items(), ["C3", "C0", "C2"]):
            m, p, e, n = lf(r["dust:" + nm], L); row[3].plot(m, p, "-", color=col, lw=1.8, label=nm, zorder=6)
        for ax in row:
            ax.set_yscale("log"); ax.set_xlim(-12, -22.5); ax.set_ylim(1e-6, 1); ax.grid(alpha=0.25)
            ax.axhline(1 / 0.5 / L**3, color="0.5", ls=":", lw=1); ax.set_xlabel(r"$M_{\rm UV}$ (AB)"); ax.legend(fontsize=5.5, loc="lower left")
        row[0].set_ylabel(r"$\Phi$ [mag$^{-1}$ cMpc$^{-3}$]")
        # text summary: mean magnitude shift vs baseline for halos brighter than -17 / in -17..-15, and LF at bins
        b = r["base"]; txt.write(f"== z = {z:.3f} (box {L:.3f} cMpc)\n")
        keys = ["ap1", "ap0.5"] + [f"Z{Z:g}" for Z in ZCONST] + ["mzr:" + k for k in MZR] + ["dust:" + k for k in DUST]
        txt.write("variant | median dM (variant - base) for base < -18 | -18..-16 | -16..-14 | N(< -18) base->variant\n")
        for k in keys:
            dm = r[k] - b
            q = [np.nanmedian(dm[(b >= lo) & (b < hi)]) for lo, hi in ((-30, -18), (-18, -16), (-16, -14))]
            txt.write(f"{k:45s} {q[0]:+.2f} {q[1]:+.2f} {q[2]:+.2f}   {np.sum(b < -18)} -> {np.sum(r[k] < -18)}\n")
        for nm in MZR:
            s = np.isfinite(b) & (r["Mstar"] > 0)
            txt.write(f"  {nm}: Z at M* = 1e6/1e7/1e8/1e9 = " + ", ".join(f"{oh2z(MZR[nm](x)):.4f}" for x in (6, 7, 8, 9)) + "\n")
        for tn, tp in TARGETS.items():
            Ar = required_A(b, L, tp, Mg); r["req:" + tn] = Ar
            txt.write(f"required A to match {tn}: " + " ".join(f"{M:.2f}:{A:.2f}" for M, A in zip(Mg, Ar) if np.isfinite(A)) + "\n")
        # median M* in base magnitude bins (to read the required A as A(M*))
        txt.write("median log M* in M_UV bins: " + " ".join(
            f"{M:.1f}:{np.log10(np.nanmedian(r['Mstar'][(b >= M - 0.5) & (b < M + 0.5)])):.2f}" for M in range(-20, -13)
            if np.sum((b >= M - 0.5) & (b < M + 0.5)) > 0) + "\n")
    fig.text(0.005, 0.003, title, fontsize=7, ha="left", va="bottom")
    fig.tight_layout(rect=(0, 0.02, 1, 1)); fig.savefig(pre + "_lf.png", dpi=110); plt.close(fig)

    # diagnostics: aperture flux fraction, Z(M*), A laws + required A
    fig, ax = plt.subplots(1, 3, figsize=(16, 4.5))
    for r, ls in zip(R, ["-", "--"]):
        b = r["base"]; s = np.isfinite(b)
        for k, col in (("ap1", "C3"), ("ap0.5", "C1")):
            fr = 10 ** (-0.4 * (r[k] - b))
            bins = np.arange(-20, -9.9, 0.5); c = 0.5 * (bins[1:] + bins[:-1])
            med = [np.nanmedian(np.nan_to_num(fr[s & (b >= lo) & (b < hi)], nan=0)) if np.sum(s & (b >= lo) & (b < hi)) > 2 else np.nan
                   for lo, hi in zip(bins[:-1], bins[1:])]
            ax[0].plot(c, med, ls, color=col, label=f"{k.replace('ap', '')} pkpc, z={r['z']:.2f}")
        xm = np.linspace(6, 10, 50)
        if ls == "-":
            for (nm, f), col in zip(MZR.items(), ["C2", "C4", "C9"]):
                ax[1].plot(10**xm, oh2z(f(xm)), color=col, label=nm)
        Mg2 = np.linspace(-23, -12, 100)
        b = r["base"]; bb = np.arange(-20.5, -11.9, 0.5); cc = 0.5 * (bb[1:] + bb[:-1])
        for (nm, f), col in zip(DUST.items(), ["C3", "C0", "C2"]):
            if "Casey" in nm:
                A = r["dust:" + nm] - b
                med = [np.nanmedian(A[(b >= lo) & (b < hi)]) if np.sum((b >= lo) & (b < hi)) > 2 else np.nan for lo, hi in zip(bb[:-1], bb[1:])]
                ax[2].plot(cc, med, ls, color=col, label=f"{nm}, median per M_UV bin (z={r['z']:.2f})")
            else:
                ax[2].plot(Mg2, f(Mg2, r["z"], None), ls, color=col, label=f"{nm} (z={r['z']:.2f})")
        for (tn, _), col in zip(TARGETS.items(), ["k", "0.5"]):
            ax[2].plot(Mg, r["req:" + tn], ls, color=col, lw=2, marker="o", ms=3, label=f"required to match {tn} (z={r['z']:.2f})")
    ax[0].set_xlabel("baseline M_UV (R200)"); ax[0].set_ylabel("median L1600(aperture) / L1600(R200)"); ax[0].invert_xaxis(); ax[0].set_ylim(0, 1.05)
    ax[1].set_xscale("log"); ax[1].set_yscale("log"); ax[1].set_xlabel("M* [Msun]"); ax[1].set_ylabel("Z (mass fraction)")
    ax[1].axhline(1e-3, color="k", ls=":", label="baseline Z = 0.001"); ax[1].set_xlim(1e6, 1e10)
    ax[2].set_xlabel("intrinsic M_UV"); ax[2].set_ylabel("A_1600 [mag]"); ax[2].invert_xaxis(); ax[2].axhline(0, color="0.6", lw=0.8)
    for x in ax: x.grid(alpha=0.3); x.legend(fontsize=6)
    fig.suptitle("boxC LF post-processing diagnostics: aperture flux fraction, Z(M*) relations, dust laws vs required attenuation", fontsize=9)
    fig.tight_layout(); fig.savefig(pre + "_diag.png", dpi=110); plt.close(fig)
    print("wrote", pre + "_lf.png", pre + "_diag.png", pre + ".txt")

main()
