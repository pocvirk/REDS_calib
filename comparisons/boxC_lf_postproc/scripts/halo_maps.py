"""Stamp maps of a mass sequence of halos (PO 2026-11-26, post-processing only): morphology, multiplicity (detected segments)
and the size estimators of mock_phot.py, with and without noise.
Per halo (row): intrinsic (no PSF, no noise) | PSF, no noise | <survey1> noisy | <survey1> segmentation | <survey2> noisy | <survey2> seg.
Same pipeline as mock_phot.py (same PSF, noise, detection, deblending, Kron, non-parametric sizes) run on a padded stamp around each halo.
usage: python -I halo_maps.py <npz> <out.png> [--axis 0] [--logm 9.5 9.75 ...] [--surveys JADES GLIMPSE_mu20] [--seed 1]
"""
import sys, argparse
import numpy as np
sys.path.insert(0, "/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/runs/reio_v2/boxsize/lfpp")
from mock_phot import SURVEYS, PSF, PIX, moffat_kernel, moffat_scaled, np_radius, gauss_kernel, dbtg
from astropy.cosmology import FlatLambdaCDM
from scipy.signal import fftconvolve
from scipy import ndimage
from photutils.segmentation import detect_sources, deblend_sources, SourceCatalog
from photutils.aperture import CircularAperture, aperture_photometry
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse
from matplotlib.colors import ListedColormap

ap = argparse.ArgumentParser()
ap.add_argument("npz"); ap.add_argument("out"); ap.add_argument("--axis", type=int, default=0)
ap.add_argument("--logm", type=float, nargs="+", default=[9.5, 9.75, 10.0, 10.25, 10.5, 99])
ap.add_argument("--surveys", nargs="+", default=["JADES", "GLIMPSE_mu20"]); ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--halfwidth", type=float, default=7.0, help="display half-width [pkpc]")
A = ap.parse_args()

d = np.load(A.npz, allow_pickle=True)
z = float(d["z"]); L = float(d["lbox"]); h = float(d["h"]); bx = int(d["bx"])
c = FlatLambdaCDM(H0=100 * h, Om0=0.307, Ob0=0.0482, Tcmb0=2.725)
scale = c.kpc_proper_per_arcmin(z).value / 60; DM = c.distmod(z).value
filt = "F115W" if z < 7.0 else "F150W"
fwhm, ee015 = PSF[filt]; psf0, EE0, mb, ma = moffat_kernel(fwhm, ee015)
ax2 = [i for i in range(3) if i != A.axis]
pos = d["spos"][:, ax2] * 1e3 / (1 + z) / scale                      # arcsec
Lang = L * 1e3 / (1 + z) / scale
T = dbtg.gen_age_Z_interpolator(str(d["mag_file"]))[0]
hm, off, fl = d["hm"], d["off"], d["flat"]
r200 = d["r200"] * 1e3 / (1 + z) / scale                               # cMpc -> arcsec
dx_arc = L / (bx * 2**11) * 1e3 / (1 + z) / scale; sig_part = 0.5 * dx_arc / PIX
m2M = lambda f: -2.5 * np.log10(f) + 31.4 - DM + 2.5 * np.log10(1 + z) if f > 0 else np.nan
kern = gauss_kernel(3.0 / 2.3548, size=5)
RAP = int(round(1.0 / PIX)); yy, xx = np.mgrid[-RAP:RAP + 1, -RAP:RAP + 1]; inap = xx**2 + yy**2 <= RAP**2

# halo choice: nearest in log Mh to each requested value (99 = most massive)
lm = np.log10(hm); picks = []
for v in A.logm:
    k = int(np.argmax(hm)) if v > 50 else int(np.argmin(abs(lm - v) + 1e3 * np.isin(np.arange(len(hm)), picks)))
    picks.append(k)

def survey_setup(name):
    S = dict(SURVEYS[name]); mu = S.get("mu", 1)
    psf, EE = moffat_scaled(ma / np.sqrt(mu), mb) if mu > 1 else (psf0, EE0)
    f5 = 10 ** (-0.4 * (S["depth"][filt] - 31.4)); r_ap = S["D"] / 2
    sig_pix = f5 * EE0(r_ap) / 5 / np.sqrt(np.pi * (r_ap / PIX) ** 2) / np.sqrt(mu)
    return S, psf, EE, sig_pix, fftconvolve(psf, kern, mode="same")

SV = {s: survey_setup(s) for s in A.surveys}
print(f"z = {z:.3f} {filt}, {scale:.2f} pkpc/\", dx_min = {dx_arc * scale * 1e3:.0f} ppc, axis {A.axis}", flush=True)

def stamp(k, rng):
    s = fl[off[k]:off[k + 1]]; f_h = d["sm_init"][s] * 10 ** (-0.4 * (T(d["sage"][s], 1e-3) + DM - 2.5 * np.log10(1 + z) - 31.4))
    cen = (pos[s] * f_h[:, None]).sum(0) / f_h.sum()                     # halo L-weighted centre (arcsec)
    W = A.halfwidth / scale; N = int(np.ceil((max(W, 1.15 * r200[k]) + 1.3) / PIX))   # display half-width W; detection on R200 + PSF / 1" aperture pad
    cp = np.floor(cen / PIX).astype(int); x0 = (cp - N) * PIX
    dp = (pos - cen + Lang / 2) % Lang - Lang / 2                         # periodic offsets
    sel = np.all(abs(dp) < (N + 1) * PIX, axis=1); sel_i = np.where(sel)[0]
    fnu = d["sm_init"][sel_i] * 10 ** (-0.4 * (T(d["sage"][sel_i], 1e-3) + DM - 2.5 * np.log10(1 + z) - 31.4))
    p = cen + dp[sel_i] - x0; n = 2 * N + 1
    img = np.histogram2d(p[:, 1], p[:, 0], bins=n, range=[[0, n * PIX], [0, n * PIX]], weights=fnu)[0]
    true = fftconvolve(img, gauss_kernel(sig_part), mode="same")
    own = np.isin(sel_i, s); po = p[own]; fo = fnu[own]
    # intrinsic sizes of all R200 stars
    cl = (po * fo[:, None]).sum(0) / fo.sum(); r = np.sqrt(((po - cl) ** 2).sum(1)); o = np.argsort(r)
    rh_all = r[o][np.searchsorted(np.cumsum(fo[o]), 0.5 * fo.sum())]
    cx, cy = cl / PIX - 0.5; i0, j0 = int(round(cy)), int(round(cx))
    ct = true[i0 - RAP:i0 + RAP + 1, j0 - RAP:j0 + RAP + 1]
    rnp_t = np_radius(ct[inap])
    v = np.sort(ct[inap][ct[inap] > 0])[::-1]; thr_t = v[np.searchsorted(np.cumsum(v), 0.5 * v.sum())]   # half-light isophote
    out = dict(k=k, n=n, N=N, W=W, true=true, cl=cl, rh_all=rh_all, rnp_t=rnp_t, thr_t=thr_t, Mtrue=m2M(fo.sum()), ij=(i0, j0))
    ixy = np.clip((po / PIX).astype(int), 0, n - 1)
    for name, (S, psf, EE, sig_pix, psf_sm) in SV.items():
        conv = fftconvolve(true, psf, mode="same"); obs = conv + rng.normal(0, sig_pix, conv.shape)
        sm = fftconvolve(obs, kern, mode="same"); sig_sm = sig_pix * np.sqrt((kern**2).sum())
        seg = detect_sources(sm, S["thr"] * sig_sm, npixels=S["npix"]); R = dict(conv=conv, obs=obs, sm=sm, sig_pix=sig_pix, sig_sm=sig_sm, seg=None)
        if seg is not None:
            labs = np.arange(1, seg.max_label + 1)
            fs = ndimage.sum_labels(obs, seg.data, labs); npx = ndimage.sum_labels(np.ones_like(obs), seg.data, labs)
            keep = labs[fs / (sig_pix * np.sqrt(np.maximum(npx, 1))) > 4]
            if len(keep):
                seg.keep_labels(keep, relabel=True)
                seg = deblend_sources(sm, seg, npixels=S["npix"], nlevels=S["nlev"], contrast=S["contrast"], progress_bar=False)
                R["seg"] = seg
        if R["seg"] is not None:
            seg = R["seg"]; cat = SourceCatalog(obs, seg, convolved_data=sm, error=np.full(obs.shape, sig_pix, np.float32))
            sid = seg.data[ixy[:, 1], ixy[:, 0]]; det = sid > 0
            R["fdet"] = fo[det].sum() / fo.sum()
            if det.any() and fo[det].sum() / fo.sum() > 0.02:
                lb, inv = np.unique(sid[det], return_inverse=True); flb = np.bincount(inv, weights=fo[det])
                main = lb[np.argmax(flb)]
                j = list(cat.label).index(main)
                R.update(main=main, nseg=len(lb), halo_labs=lb, fmain=flb.max() / fo.sum(),
                         xc=cat.xcentroid[j], yc=cat.ycentroid[j], Mk=m2M(cat.kron_flux[j]), kron=cat.kron_aperture[j],
                         rh_obs=cat.fluxfrac_radius(0.5).value[j])
                m = sid == main; pm, fm = po[m], fo[m]; cm = (pm * fm[:, None]).sum(0) / fm.sum()
                rm = np.sqrt(((pm - cm) ** 2).sum(1)); om = np.argsort(rm)
                R.update(rh_det=rm[om][np.searchsorted(np.cumsum(fm[om]), 0.5 * fm.sum())], cm=cm)
        # non-parametric observed size: 5 sigma pixels of the detection image in the 1" aperture around the halo centre
        cs = sm[i0 - RAP:i0 + RAP + 1, j0 - RAP:j0 + RAP + 1]; co = obs[i0 - RAP:i0 + RAP + 1, j0 - RAP:j0 + RAP + 1]
        m5 = inap & (cs > 5 * sig_sm); R["m5"] = m5
        if m5.sum() >= 3:
            rr = np_radius(co[m5]); f5s = co[m5].sum(); c0 = psf.shape[0] // 2; hw = min(c0, RAP)
            pq = (psf_sm * f5s)[c0 - hw:c0 + hw + 1, c0 - hw:c0 + hw + 1]; pp = (psf * f5s)[c0 - hw:c0 + hw + 1, c0 - hw:c0 + hw + 1]
            rp = np_radius(pp[pq > 5 * sig_sm]) if np.any(pq > 5 * sig_sm) else 0.0
            R.update(rnp_raw=rr, rnp_o=np.sqrt(max(rr**2 - rp**2, 0)), rnp_psf=rp)
        out[name] = R
    return out

rng = np.random.default_rng(A.seed + 10 * A.axis)
rows = []
for k in picks:
    rows.append(stamp(k, rng)); R = rows[-1]
    print(f"halo {k}: log Mh {np.log10(hm[k]):.2f}, R200 {r200[k] * scale:.1f} pkpc, M_true {R['Mtrue']:.2f}, rh_all {R['rh_all'] * scale:.2f} pkpc, "
          f"rnp_int {R['rnp_t'] * PIX * scale:.2f} pkpc | " +
          " | ".join(f"{s}: nseg {R[s].get('nseg', 0)}, fdet {R[s].get('fdet', 0):.2f}, Mkron {R[s].get('Mk', np.nan):.2f}, "
                     f"rnp_obs {R[s].get('rnp_o', np.nan) * PIX * scale:.2f}" for s in A.surveys), flush=True)

# ---------------- figure
SBMIN, SBMAX = 22.5, 31.0
def sbmap(im):                                       # nJy/pix -> mag/arcsec^2, blank (faintest) below 0
    return np.where(im > 0, -2.5 * np.log10(np.maximum(im, 1e-30) / PIX**2) + 31.4, SBMAX)
cmap = plt.get_cmap("magma_r").copy(); SNRMAX = 25
ncol = 2 + 2 * len(A.surveys); nrow = len(rows)
fig, axs = plt.subplots(nrow, ncol, figsize=(2.35 * ncol, 2.45 * nrow), squeeze=False)
rngc = np.random.default_rng(3); segcols = rngc.uniform(0.35, 0.95, (4096, 3))
for i, R in enumerate(rows):
    k = R["k"]; N = R["N"]; Wp = int(np.ceil(R["W"] / PIX)); sl = slice(N - Wp, N + Wp + 1)
    ext = np.array([-Wp - 0.5, Wp + 0.5, -Wp - 0.5, Wp + 0.5]) * PIX * scale       # pkpc around the stamp centre pixel
    def to_kpc(xpix, ypix): return ((xpix - N) * PIX * scale, (ypix - N) * PIX * scale)
    def P(a, im, **kw): a.imshow(im[sl, sl], origin="lower", extent=ext, interpolation="nearest", **kw)
    cxk, cyk = to_kpc(*(R["cl"] / PIX - 0.5))
    # (1) intrinsic
    a = axs[i, 0]; P(a, sbmap(R["true"]), cmap=cmap, vmin=SBMIN, vmax=SBMAX)
    a.add_patch(Circle((cxk, cyk), r200[k] * scale, fill=False, ls="--", color="c", lw=1))
    a.add_patch(Circle((cxk, cyk), R["rh_all"] * scale, fill=False, color="c", lw=1.3))
    a.contour(R["true"][sl, sl] >= R["thr_t"], levels=[0.5], extent=ext, colors="lime", linewidths=0.8)
    a.add_patch(Circle((cxk, cyk), R["rnp_t"] * PIX * scale, fill=False, color="lime", lw=1.3, ls=":"))
    a.text(0.03, 0.97, f"log M$_h$ = {np.log10(hm[k]):.2f} (R$_{{200}}$ = {r200[k] * scale:.0f} pkpc)\nM$_{{UV}}$(R$_{{200}}$) = {R['Mtrue']:.2f}\n"
           f"r$_{{1/2,all}}$ = {R['rh_all'] * scale:.2f}\nr$_{{np,int}}$ = {R['rnp_t'] * PIX * scale:.2f} pkpc",
           transform=a.transAxes, va="top", fontsize=6.5, color="k", bbox=dict(fc="w", alpha=0.7, lw=0))
    # (2) PSF, no noise (first survey's PSF)
    s1 = A.surveys[0]; a = axs[i, 1]; P(a, sbmap(R[s1]["conv"]), cmap=cmap, vmin=SBMIN, vmax=SBMAX)
    for j, s in enumerate(A.surveys):
        sbl = -2.5 * np.log10(SURVEYS[s]["thr"] * R[s]["sig_sm"] / PIX**2) + 31.4
        a.contour(sbmap(fftconvolve(R[s]["conv"], kern, mode="same"))[sl, sl], levels=[sbl], extent=ext, colors=["c", "lime"][j], linewidths=0.8)
    a.text(0.03, 0.97, f"{filt} PSF, no noise\ncontours: isophote\n" + "\n".join(f"{s}: {-2.5 * np.log10(SURVEYS[s]['thr'] * R[s]['sig_sm'] / PIX**2) + 31.4:.1f}"
           for s in A.surveys), transform=a.transAxes, va="top", fontsize=6, bbox=dict(fc="w", alpha=0.7, lw=0))
    for j, s in enumerate(A.surveys):
        Q = R[s]
        # (3) noisy
        a = axs[i, 2 + 2 * j]; snr = Q["obs"] / Q["sig_pix"]
        P(a, np.arcsinh(snr / 2), cmap="gray_r", vmin=np.arcsinh(-1), vmax=np.arcsinh(SNRMAX / 2))
        m5full = np.zeros_like(Q["obs"], bool); i0, j0 = R["ij"]; m5full[i0 - RAP:i0 + RAP + 1, j0 - RAP:j0 + RAP + 1] = Q["m5"]
        if m5full.any(): a.contour(m5full[sl, sl], levels=[0.5], extent=ext, colors="c", linewidths=0.8)
        txt = f"{s} noisy (S/N/pix, asinh)\n"
        if "rnp_o" in Q:
            a.add_patch(Circle((cxk, cyk), Q["rnp_raw"] * PIX * scale, fill=False, color="c", lw=1.3, ls=":"))
            txt += f"r$_{{np,obs}}$ = {Q['rnp_o'] * PIX * scale:.2f} pkpc\n(raw {Q['rnp_raw'] * PIX * scale:.2f}, PSF {Q['rnp_psf'] * PIX * scale:.2f})"
        else:
            txt += "< 3 pixels at 5$\\sigma$"
        a.text(0.03, 0.97, txt, transform=a.transAxes, va="top", fontsize=6, bbox=dict(fc="w", alpha=0.7, lw=0))
        # (4) segmentation
        a = axs[i, 3 + 2 * j]; a.set_facecolor("w")
        if Q["seg"] is not None:
            sd = Q["seg"].data; rgb = np.ones(sd.shape + (3,)); u = sd > 0
            rgb[u] = 0.8 * segcols[sd[u] % 4096] + 0.2                      # pale: other sources
            if "main" in Q:
                hl = np.isin(sd, Q["halo_labs"]); rgb[hl] = segcols[sd[hl] % 4096] * 0.75
                rgb[sd == Q["main"]] = (0.85, 0.1, 0.1)
            a.imshow(rgb[sl, sl], origin="lower", extent=ext, interpolation="nearest")
        if "main" in Q:
            xk, yk = to_kpc(Q["xc"], Q["yc"]); ka = Q["kron"]
            a.add_patch(Ellipse(to_kpc(ka.positions[0], ka.positions[1]), 2 * ka.a * PIX * scale, 2 * ka.b * PIX * scale,
                                angle=np.degrees(ka.theta.to_value("rad") if hasattr(ka.theta, "to_value") else ka.theta), fill=False, color="k", lw=1))
            a.add_patch(Circle((xk, yk), Q["rh_obs"] * PIX * scale, fill=False, color="b", lw=1.3))
            a.add_patch(Circle(to_kpc(*(Q["cm"] / PIX - 0.5)), Q["rh_det"] * scale, fill=False, color="g", lw=1.3, ls="--"))
            a.text(0.03, 0.97, f"{s}: n$_{{seg}}$ = {Q['nseg']}\nf$_{{det}}$ = {Q['fdet']:.2f}, f$_{{main}}$ = {Q['fmain']:.2f}\n"
                   f"M$_{{Kron}}$ = {Q['Mk']:.2f}\nr$_{{1/2,obs}}$ = {Q['rh_obs'] * PIX * scale:.2f}\nr$_{{1/2,det,int}}$ = {Q['rh_det'] * scale:.2f}",
                   transform=a.transAxes, va="top", fontsize=6, bbox=dict(fc="w", alpha=0.7, lw=0))
        else:
            a.text(0.5, 0.5, f"{s}: not detected\n(f$_{{det}}$ = {Q.get('fdet', 0):.2f} in other sources)", transform=a.transAxes, ha="center", fontsize=7)
        a.add_patch(Circle((cxk, cyk), r200[k] * scale, fill=False, ls="--", color="gray", lw=0.8))
for a in axs.ravel():
    a.tick_params(labelsize=6, direction="in"); a.set_aspect("equal"); a.set_xlim(-A.halfwidth, A.halfwidth); a.set_ylim(-A.halfwidth, A.halfwidth)
for a in axs[-1]: a.set_xlabel("pkpc", fontsize=7)
titles = ["intrinsic (no PSF, no noise)", "PSF, no noise"] + sum([[f"{s} (PSF + noise)", f"{s} segmentation"] for s in A.surveys], [])
for a, t in zip(axs[0], titles): a.set_title(t, fontsize=8)
sm_ = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(SBMIN, SBMAX))
cb = fig.colorbar(sm_, cax=fig.add_axes([0.945, 0.3, 0.012, 0.4]))
cb.set_label(r"$\mu$ [mag arcsec$^{-2}$] (observed, 0.03$''$ pixels)", fontsize=8); cb.ax.invert_yaxis()
leg = ("cyan dashed: R$_{200}$; cyan solid: r$_{1/2}$ of all R$_{200}$ stars (intrinsic, L-weighted centre); green contour + dotted circle: "
       "non-parametric intrinsic (brightest pixels holding half the light, R = $\\sqrt{A/\\pi}$)\n"
       "noisy (grey, per-pixel S/N, asinh stretch, -2 to %d sigma): cyan contour" % SNRMAX + " = pixels > 5$\\sigma$ in the detection image within 1$''$ (Varadaraj+24), dotted circle = raw non-parametric radius "
       "(PSF subtracted in quadrature in the label)\n"
       "segmentation: red = main segment of the halo, dark colours = other segments holding this halo's stars, pale = other sources; "
       "black ellipse = Kron aperture; blue = r$_{1/2}$ photutils (PSF-convolved, within Kron); green dashed = intrinsic r$_{1/2}$ of the stars in the main segment")
fig.suptitle(f"boxC (8 cMpc/h, fiducial: mech FB 2x SN, t$_{{SNII}}$ 10 Myr, BPASS M$_{{max}}$300) z = {z:.2f}, {filt}, projection axis {A.axis}, "
             f"Z = 0.001, no dust; 0.03$''$ = {PIX * scale * 1e3:.0f} ppc pixels, dx$_{{min}}$ = {dx_arc * scale * 1e3:.0f} ppc", fontsize=9)
fig.text(0.01, 0.003, leg, fontsize=6.3, va="bottom")
fig.subplots_adjust(left=0.03, right=0.93, top=0.95, bottom=0.07, wspace=0.12, hspace=0.12)
fig.savefig(A.out, dpi=130); print("wrote", A.out)
