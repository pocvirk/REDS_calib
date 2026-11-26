"""Figures from mock_phot.py outputs (PO 2026-11-26). usage: python -I mock_plots.py <mock dir> <out prefix> <iter> [<iter> ...]
(1) <out>_lf.png     UV LF of detected sources (aperture S/N > 5; Kron total and point-source-corrected 0.2/0.3" aperture mags),
                     per survey, mean of the 3 projections (band = min/max), vs the intrinsic halo LF (R200, dashboard) and data
(2) <out>_halos.png  massive halos: detected light fraction, M_kron(main segment) - M_true, number of segments, vs M_true
(3) <out>_sizes.png  half-light radii: all R200 stars (projected), intrinsic light of the main detected segment, observed
                     (PSF-convolved, Kron) vs observed size-luminosity relations; sim resolution and PSF marked
"""
import sys, glob
import numpy as np
B = "/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026"
sys.path.insert(0, B + "/analysis/dyablo_tools/dashboard_dyablo_reio")
from dashboard_reio_dyablo import obs_uvlf as O
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D, pre, its = sys.argv[1], sys.argv[2], sys.argv[3:]
SUR = [("CEERS", "C0"), ("JADES", "C1"), ("GLIMPSE", "C3"), ("GLIMPSE_mu5", "C4"), ("GLIMPSE_mu20", "C5")]
SNR = 5.0
bins = np.arange(-23, -9.99, 0.5); cen = 0.5 * (bins[1:] + bins[:-1])
DXMIN_C = 11.920726776123047 / 8192 * 1e3      # ckpc
TITLE = ("boxC 8 cMpc/h fiducial reio model (smooth SF eps0.03 (n/n_th)^0.5, mech FB 2x SN, t_SNII 10 Myr, BPASS SSP M_max 300; closest MEGATRON "
         "recipe: smooth). Mock NIRCam rest-UV imaging (0.03\"/pix, Moffat PSF, white noise at survey depth), photutils detection, no dust.")

def yang22(M):   # Yang+22 GLASS z>7 rest-UV: r_e = 0.45 kpc (L / L(M=-21))^0.2
    return 0.45 * 10 ** (-0.4 * (M + 21) * 0.2)
def kawamata18(M):   # Kawamata+18 HFF z~6-7 (Table 2): r0 = 0.94 kpc at M_UV = -21, beta = 0.46, sigma_lnr = 0.87
    return 0.94 * 10 ** (-0.4 * (M + 21) * 0.46)
def ono25(M, z):     # Ono+25 z~10-13: r0 = 0.20 kpc, alpha = 0.19; scaled to z with their r_e ~ (1+z)^-1.28 (z_ref = 11.5; extrapolation)
    return 0.20 * ((1 + z) / 12.5) ** -1.28 * 10 ** (-0.4 * (M + 21) * 0.19)

def load(it, s):
    C = [np.load(f, allow_pickle=True) for f in sorted(glob.glob(f"{D}/boxC_{it}_{s}_ax?_cat.npz"))]
    H = [np.loadtxt(f, ndmin=2) for f in sorted(glob.glob(f"{D}/boxC_{it}_{s}_ax?_halos.txt"))]
    return C, H

zs = {}
for it in its:
    c, _ = load(it, "JADES"); zs[it] = float(c[0]["z"]) if c else np.nan
data = O.load()

# (1) LF
fig, axs = plt.subplots(1, len(its), figsize=(6.2 * len(its), 5), squeeze=False); axs = axs[0]
txt = open(pre + ".txt", "w")
for ax, it in zip(axs, its):
    z = zs[it]; O.plot_obs(ax, z, data)
    base = np.loadtxt(f"{B}/runs/reio_v2/boxsize/boxC_mags_iter{it}.txt", ndmin=2)[:, 2]
    m, p, e, n = O.sim_lf(base[np.isfinite(base)], 11.920726776123047); s = n > 0
    ax.plot(m[s], p[s], "-", color="k", lw=2.2, label="intrinsic (halos, R200 stars)", zorder=5)
    ax.fill_between(m[s], np.maximum(e[0][s], 1e-8), e[1][s], color="k", alpha=0.12, lw=0, zorder=4)
    txt.write(f"== z = {z:.3f}\n")
    for sv, col in SUR:
        C, H = load(it, sv)
        if not C: continue
        for key, ls in (("M_kron", "-"),):
            P = []
            for c in C:
                ok = (c["snr_ap"] > SNR) & np.isfinite(c[key])
                mn = np.asarray(c["M_neg"])[np.asarray(c["snr_neg_ap"]) > SNR] if "M_neg" in c.files else np.zeros(0)
                P.append(np.maximum(np.histogram(c[key][ok], bins)[0] - np.histogram(mn, bins)[0], 0) / float(c["vol_cmpc3"]) / 0.5)
            P = np.array(P); pm = P.mean(0); g = pm > 0
            ax.plot(cen[g], pm[g], ls, color=col, lw=1.8, zorder=6,
                    label=f"{sv} detected (Kron, S/N_ap>5, false subtracted)")
            if key == "M_kron":
                ax.fill_between(cen[g], P.min(0)[g], P.max(0)[g], color=col, alpha=0.2, lw=0, zorder=5)
                txt.write(f"{sv} Kron LF (mean of {len(C)} axes): " + " ".join(f"{a:.1f}:{b:.2e}" for a, b in zip(cen[g], pm[g])) + "\n")
        nfalse = [int(np.sum(np.asarray(c["snr_neg_ap"]) > 5)) for c in C]
        txt.write(f"{sv}: sources S/N_ap>5 per axis {[int(np.sum(c['snr_ap'] > 5)) for c in C]}, false (inverted image) {nfalse}, "
                  f"1 sigma/pix SB {float(C[0]['sb1']):.2f} mag/arcsec^2\n")
    base_lf = np.histogram(base[np.isfinite(base)], bins)[0] / 11.920726776123047**3 / 0.5
    txt.write("intrinsic halo LF: " + " ".join(f"{a:.1f}:{b:.2e}" for a, b in zip(cen, base_lf) if b > 0) + "\n")
    ax.set_yscale("log"); ax.set_xlim(-12, -22.5); ax.set_ylim(1e-6, 1); ax.grid(alpha=0.25)
    ax.axhline(1 / 0.5 / 11.920726776123047**3, color="0.5", ls=":", lw=1)
    ax.set_xlabel(r"$M_{\rm UV}$ (AB)"); ax.set_ylabel(r"$\Phi$ [mag$^{-1}$ cMpc$^{-3}$]"); ax.set_title(f"z = {z:.2f}: mock-detected UV LF")
    ax.legend(fontsize=5.5, loc="lower left", ncol=2)
fig.text(0.005, 0.003, TITLE, fontsize=6.5, ha="left", va="bottom")
fig.tight_layout(rect=(0, 0.025, 1, 1)); fig.savefig(pre + "_lf.png", dpi=110); plt.close(fig)

# (2) halo-level detection
# columns: 0 halo 1 Mh 2 M_true 3 M_true(any seg) 4 M_kron(main) 5 M_ap(main) 6 frac_det 7 frac_main 8 nseg 9 own 10 rh_all 11 rh_det 12 rh_obs
fig, axs = plt.subplots(len(its), 3, figsize=(16, 4.3 * len(its)), squeeze=False)
for row, it in zip(axs, its):
    z = zs[it]
    for sv, col in SUR:
        _, H = load(it, sv)
        if not H: continue
        h = np.vstack(H); Mt = h[:, 2]
        nd = h[:, 13] <= SNR; h[nd, 6] = 0; h[nd, 7] = 0; h[nd, 8] = 0; h[nd, 4] = np.nan
        row[0].scatter(Mt, h[:, 6], s=6, color=col, alpha=0.4, label=f"{sv}: all segments")
        row[0].scatter(Mt, h[:, 7], s=6, color=col, alpha=0.4, marker="x")
        bl = h[:, 9] < 0.7                                         # main segment mostly another halo's light (blend)
        row[1].scatter(Mt[~bl], (h[:, 4] - Mt)[~bl], s=6, color=col, alpha=0.5, label=f"{sv}: Kron (main segment)")
        row[1].scatter(Mt[bl], (h[:, 4] - Mt)[bl], s=22, color=col, marker="^", facecolors="none",
                       label=f"{sv}: main segment mostly another halo's light (blend)")
        row[2].scatter(Mt + 0.05 * (SUR.index((sv, col)) - 1), h[:, 8], s=6, color=col, alpha=0.4, label=sv)
        bb = np.arange(-20, -12.9, 0.5)
        for j, (k, mk) in enumerate(((6, "-"), (7, ":"))):
            med = [np.median(h[(Mt >= lo) & (Mt < hi), k]) if np.sum((Mt >= lo) & (Mt < hi)) > 2 else np.nan for lo, hi in zip(bb[:-1], bb[1:])]
            row[0].plot(0.5 * (bb[1:] + bb[:-1]), med, mk, color=col, lw=2)
        dm = np.where(bl, np.nan, h[:, 4] - Mt)
        med = [np.nanmedian(dm[(Mt >= lo) & (Mt < hi)]) if np.sum(np.isfinite(dm[(Mt >= lo) & (Mt < hi)])) >= 3 else np.nan
               for lo, hi in zip(bb[:-1], bb[1:])]
        row[1].plot(0.5 * (bb[1:] + bb[:-1]), med, "-", color=col, lw=2)
    row[0].set_ylabel("fraction of L1600 (R200) in detected pixels, S/N_ap>5\n(o, solid: all segments; x, dotted: main)")
    row[1].set_ylabel("M_kron(main) - M_true(R200) [mag]\n(>0: fainter than true)")
    row[1].axhline(0, color="0.5", lw=0.8)
    row[2].set_ylabel("number of segments holding the halo's stars")
    for x in row:
        x.set_xlabel("true M_UV (all R200 stars)"); x.invert_xaxis(); x.grid(alpha=0.3); x.legend(fontsize=6); x.set_title(f"z = {z:.2f}, Mh >= 10^9.5", fontsize=9)
    row[0].set_ylim(0, 1.05)
fig.suptitle("mock detection of massive boxC halos (3 projections)", fontsize=10)
fig.text(0.005, 0.003, TITLE, fontsize=6.5, ha="left", va="bottom")
fig.tight_layout(rect=(0, 0.02, 1, 1)); fig.savefig(pre + "_halos.png", dpi=110); plt.close(fig)

# (3) sizes
fig = plt.figure(figsize=(6.5 * len(its), 6.6)); gs = fig.add_gridspec(2, len(its), height_ratios=[5, 1.2])
axs = [fig.add_subplot(gs[0, j]) for j in range(len(its))]; lax = fig.add_subplot(gs[1, :]); lax.axis("off")
for ax, it in zip(axs, its):
    z = zs[it]; Mg = np.linspace(-22, -13, 50)
    for sv, col in SUR:
        _, H = load(it, sv)
        if not H: continue
        h = np.vstack(H); nd = h[:, 13] <= SNR; h[nd, 4] = np.nan; h[nd, 11] = np.nan; h[nd, 12] = np.nan
        if sv == "JADES":
            ax.scatter(h[:, 2], h[:, 10], s=8, color="0.45", label="all R200 stars (true M_UV), 3 projections")
        if "mu" in sv: continue
        ax.scatter(h[:, 4], h[:, 11], s=8, color=col, alpha=0.5, label=f"{sv}: intrinsic light in main segment (M_kron)")
        ax.scatter(h[:, 4], h[:, 12], s=8, color=col, alpha=0.5, marker="x", label=f"{sv}: observed, PSF-convolved (Kron)")
        txt.write(f"z={z:.2f} {sv}: median rhalf [pkpc] all-stars {np.nanmedian(h[:, 10]):.2f}, main-seg intrinsic {np.nanmedian(h[:, 11]):.2f}, "
                  f"observed {np.nanmedian(h[:, 12]):.2f}; median frac detected {np.nanmedian(h[:, 6]):.2f}, median dM_kron {np.nanmedian(h[:, 4] - h[:, 2]):+.2f}, "
                  f"median nseg {np.nanmedian(h[:, 8]):.0f} (N halos x axes = {len(h)})\n")
    ax.plot(Mg, yang22(Mg), "k--", lw=1.5, label="Yang+22 (GLASS, z>7, rest-UV): 0.45 kpc (L/L_-21)^0.2")
    ax.plot(Mg, kawamata18(Mg), "-", color="m", lw=1.8, label="Kawamata+18 (HFF z~6-7): 0.94 kpc (L/L_-21)^0.46, band = sigma_lnr 0.87")
    ax.fill_between(Mg, kawamata18(Mg) * np.exp(-0.87), kawamata18(Mg) * np.exp(0.87), color="m", alpha=0.08, lw=0)
    ax.plot(Mg, ono25(Mg, z), ":", color="k", lw=1.8, label="Ono+25 z~10-13 fit scaled to this z with (1+z)^-1.28 (extrapolated)")
    ap = 1 / (1 + z)
    for f, ls, lab in ((1, ":", "finest cell dx"), (4, "-.", "4 dx (effective resolution)")):
        ax.axhline(f * DXMIN_C * ap, color="0.4", ls=ls, lw=1, label=f"sim {lab} ({DXMIN_C:.2f} ckpc" + (")" if f == 1 else " x 4)"))
    sc = {6.69: 5.56, 7.33: 5.26}.get(round(z, 2), 5.4)
    ax.axhline(0.5 * (0.040 if z < 7 else 0.050) * sc, color="C2", ls=":", lw=1.2, label="NIRCam PSF HWHM")
    ax.set_yscale("log"); ax.set_ylim(0.05, 10); ax.set_xlim(-12.5, -21.5); ax.grid(alpha=0.3)
    ax.set_xlabel(r"$M_{\rm UV}$"); ax.set_ylabel("half-light radius [pkpc]"); ax.set_title(f"z = {z:.2f}: sizes of Mh >= 10^9.5 halos (3 projections)", fontsize=9)
h_, l_ = axs[0].get_legend_handles_labels(); lax.legend(h_, l_, loc="upper center", ncol=3, fontsize=7.5, frameon=False)
fig.text(0.005, 0.003, TITLE, fontsize=6.5, ha="left", va="bottom")
fig.tight_layout(rect=(0, 0.025, 1, 1)); fig.savefig(pre + "_sizes.png", dpi=110); plt.close(fig)
print("wrote", pre + "_lf.png", pre + "_halos.png", pre + "_sizes.png", pre + ".txt")
