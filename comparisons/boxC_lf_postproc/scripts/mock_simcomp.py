"""boxC mock sizes vs other simulations (PO 2026-11-26): size-M_UV, size-M*, size-depth and detected-light-fraction-depth.
usage: python -I mock_simcomp.py <mock dir> <npz dir> <out.png> <iter> [<iter> ...]
Literature (simulations):
  THESAN-ZOOM (McClymont+25, 2503.04894, Table 1): 2D R_eff^UV = 1.2 kpc (M*/1e8)^0.18 (1+z)^mu, mu = mu1 + (1+tanh((z-9.5)/2.5))/2 (mu2-mu1),
      mu1=-0.07, mu2=-0.38 (raw, no selection; after a JWST-like SB cut they come within 0.1-0.2 dex of observations)
  THESAN-1/HR (Shen+24, 2402.08717): no fits published; intrinsic r1/2 >~ 1 pkpc at M* <~ 1e9 (hump at 1e8), <~ 1 pkpc at >~ 1e10;
      UV sizes >= 3x observed at -20 <~ M_UV <~ -15 (drawn as 3x Kawamata+18, lower bound)
  FLARES (Roper+22, 2203.12627, Table 2): dust-attenuated FUV R = R0 (L/L*_z=3)^beta, L* <-> M=-21: z6 (1.370, 0.279), z7 (1.126, 0.290);
      intrinsic relation negative (ultra-compact bright galaxies), no fit published
  FIRE-2 (Ma+18, 1710.00008): intrinsic UV R50 at z=5 (Table 1): 0.76/0.55/0.49 kpc at M_UV=-18/-16/-14, x ((1+z)/6)^-1.87;
      at a 26.5 mag/arcsec^2 SB limit the lost UV light fraction rises linearly from 0 at M_UV=-22 to 1 at -12;
      one galaxy's observed R50 drops 0.1" -> 0.01" from 29 to 28 mag/arcsec^2 at z=6
"""
import sys, glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D, NPZ, out, its = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
SUR = [("CEERS", "C0"), ("JADES", "C1"), ("GLIMPSE", "C3"), ("GLIMPSE_mu5", "C4"), ("GLIMPSE_mu20", "C5")]
BINS = [(-19.75, -18.5), (-18.5, -17.5), (-17.5, -16.5)]
BCOL = ["k", "C2", "C9"]
SNR = 5.0

def thesan_zoom(ms, z):
    mu = -0.07 + 0.5 * (1 + np.tanh((z - 9.5) / 2.5)) * (-0.38 + 0.07)
    return 1.2 * (ms / 1e8) ** 0.18 * (1 + z) ** mu
def flares(M, z):
    f = np.clip(z - 6, 0, 1); R0 = (1 - f) * 1.370 + f * 1.126; b = (1 - f) * 0.279 + f * 0.290
    return R0 * 10 ** (-0.4 * (M + 21) * b)
def fire2(M, z):
    return np.interp(M, [-18, -16, -14], [0.76, 0.55, 0.49]) * ((1 + z) / 6) ** -1.87
def kawamata18(M):
    return 0.94 * 10 ** (-0.4 * (M + 21) * 0.46)

fig = plt.figure(figsize=(21, 4.9 * len(its) + 2.4)); gs = fig.add_gridspec(len(its) + 1, 4, height_ratios=[4.9] * len(its) + [2.4])
axs = np.array([[fig.add_subplot(gs[r, c]) for c in range(4)] for r in range(len(its))]); lax = [fig.add_subplot(gs[-1, c]) for c in range(4)]
txt = open(out.replace(".png", ".txt"), "w")
for row, it in zip(axs, its):
    d = np.load(f"{NPZ}/boxC_iter{it}.npz", allow_pickle=True)
    off = d["off"]; c = np.concatenate([[0], np.cumsum(d["smass"][d["flat"]])]); Mstar = c[off[1:]] - c[off[:-1]]
    z = float(d["z"]); Mg = np.linspace(-21, -13, 60); mg = np.logspace(6, 10.3, 60)
    H, SB = {}, {}
    for sv, col in SUR:
        fs = sorted(glob.glob(f"{D}/boxC_{it}_{sv}_ax?_halos.txt"))
        if not fs: continue
        H[sv] = np.vstack([np.loadtxt(f, ndmin=2) for f in fs])
        cc = np.load(fs[0].replace("_halos.txt", "_cat.npz"), allow_pickle=True)
        # isophotal SB limit of the detection: threshold x sigma of the smoothed image, per pixel
        thr = {"CEERS": 1.4}.get(sv, 1.5)
        SB[sv] = -2.5 * np.log10(thr * float(cc["sig_sm"]) / float(cc["pix"]) ** 2) + 31.4
    hJ = H["JADES"]; Mt = hJ[:, 2]; ms = Mstar[hJ[:, 0].astype(int)]
    # (a) size - M_UV
    ax = row[0]
    ax.scatter(Mt, hJ[:, 10], s=6, color="0.6", label="this work: all R200 stars (intrinsic, 2D)")
    for sv, col in SUR:
        h = H[sv]; det = h[:, 13] > SNR; bb = np.arange(-20, -14.4, 0.5); cb = 0.5 * (bb[1:] + bb[:-1])
        med = [np.median(h[det & (h[:, 4] >= lo) & (h[:, 4] < hi), 11]) if np.sum(det & (h[:, 4] >= lo) & (h[:, 4] < hi)) >= 3 else np.nan
               for lo, hi in zip(bb[:-1], bb[1:])]
        ax.plot(cb, med, "-o", ms=3, color=col, lw=1.6, label=f"this work, {sv}: detected core (median, vs M_kron)")
    bb = np.arange(-20, -13.9, 0.5); cb = 0.5 * (bb[1:] + bb[:-1])
    if hJ.shape[1] > 14:
        med = [np.nanmedian(hJ[(Mt >= lo) & (Mt < hi), 14]) if np.sum((Mt >= lo) & (Mt < hi)) >= 3 else np.nan for lo, hi in zip(bb[:-1], bb[1:])]
        ax.plot(cb, med, "-", color="k", lw=2.2, label="this work: NON-PARAMETRIC intrinsic (all pixels, 1\" ap., vs true M_UV)")
        for sv, col in (("JADES", "C1"), ("GLIMPSE_mu20", "C5")):
            h = H[sv]; det = h[:, 13] > SNR
            med = [np.nanmedian(h[det & (h[:, 4] >= lo) & (h[:, 4] < hi), 15]) if np.sum(det & (h[:, 4] >= lo) & (h[:, 4] < hi)) >= 3 else np.nan
                   for lo, hi in zip(bb[:-1], bb[1:])]
            ax.plot(cb, med, "--", color=col, lw=2.2, label=f"this work, {sv}: NON-PARAMETRIC observed (5 sigma pixels, PSF-sub.)")
    ax.plot(Mg, flares(Mg, z), "--", color="C6", lw=2, label="FLARES (Roper+22): dust-attenuated FUV fit (non-parametric pixel method)")
    ax.plot(Mg[Mg >= -19], fire2(Mg[Mg >= -19], z), "-.", color="C8", lw=2, label="FIRE-2 (Ma+18): intrinsic UV R50, scaled (1+z)^-1.87")
    k = (Mg >= -20) & (Mg <= -15)
    ax.plot(Mg[k], 3 * kawamata18(Mg[k]), ":", color="C7", lw=2.5, label="THESAN (Shen+24): UV sizes >= 3x observed (3 x Kawamata+18)")
    ax.annotate("", xy=(-17.5, 3 * kawamata18(-17.5) * 2.2), xytext=(-17.5, 3 * kawamata18(-17.5)), arrowprops=dict(arrowstyle="->", color="C7"))
    ax.plot(Mg, kawamata18(Mg), "-", color="m", lw=1.2, alpha=0.6, label="obs: Kawamata+18 z~6-7")
    ax.set_xlim(-13.5, -21); ax.set_xlabel(r"$M_{\rm UV}$"); ax.set_title(f"z = {z:.2f}: size vs M_UV", fontsize=10)
    # (b) size - M*
    ax = row[1]
    ax.scatter(ms, hJ[:, 10], s=6, color="0.6", label="this work: all R200 stars (intrinsic, 2D)")
    for sv, col in SUR:
        h = H[sv]; det = h[:, 13] > SNR; mm = Mstar[h[:, 0].astype(int)]
        ax.scatter(mm[det], h[det, 11], s=7, color=col, alpha=0.5, label=f"this work, {sv}: detected core")
    ax.plot(mg, thesan_zoom(mg, z), "--", color="C7", lw=2, label="THESAN-ZOOM (McClymont+25): 2D R_eff^UV fit (raw)")
    ax.fill_between(mg, thesan_zoom(mg, z) * 10**-0.3, thesan_zoom(mg, z), color="C7", alpha=0.12,
                    label="THESAN-ZOOM after JWST-like SB cut (~ -0.3 dex, to within 0.1-0.2 dex of obs)")
    ax.hlines(1.0, 1e7, 1e9, color="C7", lw=3, alpha=0.5, label="THESAN (Shen+24): intrinsic r1/2 >~ 1 pkpc at 1e7-1e9 (hump 1e8)")
    for xm in (1e7, 1e8, 1e9):
        ax.annotate("", xy=(xm, 1.8), xytext=(xm, 1.0), arrowprops=dict(arrowstyle="->", color="C7", alpha=0.6))
    ax.set_xscale("log"); ax.set_xlim(1e6, 2e10); ax.set_xlabel("M* [Msun] (current, R200)"); ax.set_title(f"z = {z:.2f}: size vs stellar mass", fontsize=10)
    for ax in row[:2]:
        ax.set_yscale("log"); ax.set_ylim(0.05, 8); ax.set_ylabel("half-light radius [pkpc]"); ax.grid(alpha=0.3)
    # (c) size - depth, (d) detected light fraction - depth
    order = [sv for sv, _ in SUR if sv in H]; x = np.array([SB[sv] for sv in order])
    txt.write(f"== z = {z:.3f}; isophotal SB limits: " + ", ".join(f"{sv} {SB[sv]:.2f}" for sv in order) + "\n")
    for (lo, hi), bc in zip(BINS, BCOL):
        sel = lambda h: (h[:, 2] >= lo) & (h[:, 2] < hi)
        r_all = np.median(hJ[sel(hJ), 10])
        r_det = [np.median(H[sv][sel(H[sv]) & (H[sv][:, 13] > SNR), 11]) if np.sum(sel(H[sv]) & (H[sv][:, 13] > SNR)) >= 3 else np.nan for sv in order]
        r_obs = [np.median(H[sv][sel(H[sv]) & (H[sv][:, 13] > SNR), 12]) if np.sum(sel(H[sv]) & (H[sv][:, 13] > SNR)) >= 3 else np.nan for sv in order]
        fdet = [np.median(np.where(H[sv][sel(H[sv]), 13] > SNR, H[sv][sel(H[sv]), 6], 0)) for sv in order]
        lab = f"true M_UV {lo:g} to {hi:g}"
        row[2].plot(x, r_det, "-o", color=bc, label=f"{lab}: detected core (intrinsic)")
        row[2].plot(x, r_obs, "--s", color=bc, ms=4, alpha=0.7, label=f"{lab}: observed (PSF-conv.)")
        row[2].axhline(r_all, color=bc, ls=":", lw=1.2, label=f"{lab}: all stars (infinite depth)")
        if hJ.shape[1] > 14:
            r_np = [np.nanmedian(H[sv][sel(H[sv]) & (H[sv][:, 13] > SNR), 15]) if np.sum(sel(H[sv]) & (H[sv][:, 13] > SNR)) >= 3 else np.nan for sv in order]
            r_npi = np.nanmedian(hJ[sel(hJ), 14])
            row[2].plot(x, r_np, "-.^", color=bc, ms=5, label=f"{lab}: NON-PARAMETRIC observed (5 sigma, PSF-sub.)")
            row[2].axhline(r_npi, color=bc, ls=(0, (1, 3)), lw=2, alpha=0.6, label=f"{lab}: NON-PARAMETRIC intrinsic (infinite depth)")
            txt.write(f"{lab}: NON-PARAM intrinsic {r_npi:.2f}; NON-PARAM observed " + " ".join(f"{v:.2f}" for v in r_np) + "\n")
        row[3].plot(x, fdet, "-o", color=bc, label=f"{lab}: this work")
        Mc = 0.5 * (lo + hi)
        row[3].plot([26.5], [1 - np.clip((Mc + 22) / 10, 0, 1)], marker="*", ms=13, color=bc, ls="none",
                    label=f"FIRE-2 (Ma+18) at 26.5 mag/arcsec^2, M_UV={Mc:g}")
        txt.write(f"{lab}: r_all {r_all:.2f}; r_det " + " ".join(f"{v:.2f}" for v in r_det) + "; r_obs " + " ".join(f"{v:.2f}" for v in r_obs)
                  + "; f_det " + " ".join(f"{v:.2f}" for v in fdet) + "\n")
    sc = 5.91 if z < 6.3 else 5.6
    row[2].plot([28, 29], [0.01 * sc, 0.1 * sc], "-", color="C8", lw=2.5, alpha=0.7, label="FIRE-2 (Ma+18): one galaxy, z=6, 28 -> 29 mag/arcsec^2")
    for sv, xx in zip(order, x):
        for a in row[2:]:
            a.axvline(xx, color="0.85", lw=0.8, zorder=0)
        row[2].text(xx, 0.055, sv.replace("GLIMPSE_", "GL "), rotation=90, fontsize=6, va="bottom", ha="right", color="0.4")
    row[2].set_yscale("log"); row[2].set_ylim(0.05, 3); row[2].set_ylabel("half-light radius [pkpc]")
    row[3].set_ylim(0, 1.05); row[3].set_ylabel("median fraction of L1600 (R200) in detected pixels")
    for a in row[2:]:
        a.set_xlabel("isophotal SB detection limit [mag/arcsec^2] (source plane for lensed)"); a.grid(alpha=0.3)
        a.set_xlim(26.2, 30.6)
    row[2].set_title(f"z = {z:.2f}: size vs depth (massive halos, 3 projections)", fontsize=10)
    row[3].set_title(f"z = {z:.2f}: detected light fraction vs depth", fontsize=10)
for c, la in enumerate(lax):
    la.axis("off"); h_, l_ = axs[0, c].get_legend_handles_labels()
    la.legend(h_, l_, loc="upper center", fontsize=6.6, frameon=False, ncol=2 if len(l_) > 14 else 1)
fig.text(0.005, 0.003, "boxC 8 cMpc/h fiducial reio model (smooth SF eps0.03 (n/n_th)^0.5, mech FB 2x SN, t_SNII 10 Myr, M_max 300; closest MEGATRON "
         "recipe: smooth); mock NIRCam (CEERS/JADES/GLIMPSE depths, GLIMPSE lensed mu 5/20), no dust. Simulation trends: THESAN-ZOOM, THESAN, FLARES, FIRE-2.",
         fontsize=6.5, ha="left", va="bottom")
fig.tight_layout(rect=(0, 0.02, 1, 1)); fig.savefig(out, dpi=105); plt.close(fig)
print("wrote", out)
