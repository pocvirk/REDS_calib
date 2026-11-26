"""Mock JWST/NIRCam rest-UV photometry of a simulated snapshot (PO 2026-11-26; post-processing only).
Full-box projected image (all star particles, L1600 from the run's BPASS SSP M_max=300 table, Z=0.001, no dust) at 0.03"/pix
(>= 0.5 dx_min), smoothed by a Gaussian sigma = 0.5 dx_min (particle -> cell), convolved with a Moffat PSF matched to the survey's
FWHM + aperture correction, white noise calibrated on the survey 5 sigma point-source depth in its aperture.
Detection / deblending / Kron + aperture photometry with photutils. Halo matching for halos with Mh >= MH_MATCH.
usage: python -I mock_phot.py <npz from extract.py> <survey> <axis 0|1|2> <out prefix> [--contrast c] [--region N]
surveys: CEERS (Finkelstein+24), JADES (Rieke+23), GLIMPSE (Atek+25, unlensed: surface-brightness depth = image-plane depth)
"""
import sys, argparse, time
import numpy as np
B = "/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026"
sys.path.insert(0, B + "/analysis/dyablo_tools/dashboard_dyablo_reio")
from dashboard_reio_dyablo.rc import dashboard_tools_galaxies as dbtg
from astropy.cosmology import FlatLambdaCDM
from scipy.signal import fftconvolve
from photutils.segmentation import detect_sources, deblend_sources, SourceCatalog
from photutils.aperture import CircularAperture, aperture_photometry

PIX = 0.03                      # arcsec
MH_MATCH = 10**9.5              # Msun: halos analysed individually (sizes, flux fractions)
# 5 sigma point-source depths [AB] (total, i.e. aperture-corrected), aperture diameter, detection threshold [sigma], npixels,
# deblending (nlevels, contrast).  CEERS: Finkelstein+24 Table 1 (0.2", SE DETECT_THRESH 1.4, MINAREA 5);
# JADES: Rieke+23 Table 2 (0.3", photutils SNR 1.5, nlevels 16, contrast 0.1); GLIMPSE: Atek+25 Table 1 (0.2", SExtractor)
SURVEYS = {"CEERS":   dict(depth={"F115W": 29.20, "F150W": 29.01}, D=0.2, thr=1.4, npix=5, nlev=32, contrast=0.005),
           "JADES":   dict(depth={"F115W": 29.82, "F150W": 29.74}, D=0.3, thr=1.5, npix=5, nlev=16, contrast=0.1),
           "GLIMPSE": dict(depth={"F115W": 30.87, "F150W": 30.77}, D=0.2, thr=1.5, npix=5, nlev=32, contrast=0.005)}
# lensed GLIMPSE: magnification mu conserves surface brightness but spreads a source over mu x more image pixels. Isotropic
# source-plane equivalent: per-pixel noise / sqrt(mu), PSF scale / sqrt(mu) (pixel 0.03" kept >= 0.5 dx_min; sub-pixel PSF then)
for _mu in (5, 20):
    SURVEYS[f"GLIMPSE_mu{_mu}"] = dict(SURVEYS["GLIMPSE"], mu=_mu)
# NIRCam PSF: FWHM ["] and encircled energy at r = 0.15" (1 / JADES 0.3" aperture correction, Rieke+23 Table 2)
PSF = {"F115W": (0.040, 1 / 1.24), "F150W": (0.050, 1 / 1.22)}

def moffat_kernel(fwhm, ee015, size=81):
    """circular Moffat matched to FWHM and EE(0.15"); returns kernel (pixels of PIX) and EE(r) function"""
    bs = np.linspace(1.2, 8, 2000)
    al = fwhm / (2 * np.sqrt(2 ** (1 / bs) - 1))
    ee = 1 - (1 + (0.15 / al) ** 2) ** (1 - bs)
    b = bs[np.argmin(abs(ee - ee015))]; a = fwhm / (2 * np.sqrt(2 ** (1 / b) - 1))
    y, x = (np.mgrid[:size, :size] - size // 2) * PIX
    k = (1 + (x**2 + y**2) / a**2) ** (-b); k /= k.sum()
    return k, (lambda r: 1 - (1 + (r / a) ** 2) ** (1 - b)), b, a

def moffat_scaled(a, b, size=81):
    y, x = (np.mgrid[:size, :size] - size // 2) * PIX
    k = (1 + (x**2 + y**2) / a**2) ** (-b); return k / k.sum(), (lambda r: 1 - (1 + (r / a) ** 2) ** (1 - b))

def np_radius(vals):
    """non-parametric half-light radius in pixels: sort pixel values, area A of the brightest pixels holding half the sum, R = sqrt(A/pi)"""
    v = np.sort(vals[vals > 0])[::-1]
    if v.size == 0: return np.nan
    k = np.searchsorted(np.cumsum(v), 0.5 * v.sum()) + 1
    return np.sqrt(k / np.pi)

def gauss_kernel(sig_pix, size=None):
    size = size or (2 * int(np.ceil(4 * sig_pix)) + 1)
    y, x = np.mgrid[:size, :size] - size // 2
    k = np.exp(-0.5 * (x**2 + y**2) / sig_pix**2); return k / k.sum()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("npz"); ap.add_argument("survey"); ap.add_argument("axis", type=int); ap.add_argument("out")
    ap.add_argument("--contrast", type=float, default=None); ap.add_argument("--region", type=int, default=0, help="test: N x N pixel corner only")
    ap.add_argument("--seed", type=int, default=1)
    A = ap.parse_args(); S = dict(SURVEYS[A.survey])
    if A.contrast is not None: S["contrast"] = A.contrast
    t0 = time.time()
    d = np.load(A.npz, allow_pickle=True)
    z = float(d["z"]); a = float(d["aexp"]); L = float(d["lbox"]); h = float(d["h"]); bx = int(d["bx"])
    c = FlatLambdaCDM(H0=100 * h, Om0=0.307, Ob0=0.0482, Tcmb0=2.725)
    scale = c.kpc_proper_per_arcmin(z).value / 60            # pkpc / arcsec
    DM = c.distmod(z).value
    filt = "F115W" if z < 7.0 else "F150W"                   # rest ~1450-1650 A
    fwhm, ee015 = PSF[filt]; psf, EE0, mb, ma = moffat_kernel(fwhm, ee015)
    mu = S.get("mu", 1)
    psf, EE = moffat_scaled(ma / np.sqrt(mu), mb) if mu > 1 else (psf, EE0)
    # stars: L1600 -> observed nJy (flat f_nu across the filter)
    T = dbtg.gen_age_Z_interpolator(str(d["mag_file"]))[0]
    Mabs_per_msun = T(d["sage"], 1e-3)
    fnu = d["sm_init"] * 10 ** (-0.4 * (Mabs_per_msun + DM - 2.5 * np.log10(1 + z) - 31.4))   # nJy (AB zero point 31.4 for nJy)
    ax2 = [i for i in range(3) if i != A.axis]
    pos = d["spos"][:, ax2] * 1e3 / (1 + z) / scale          # arcsec
    Lang = L * 1e3 / (1 + z) / scale; n = int(np.ceil(Lang / PIX))
    if A.region: n = A.region
    img, _, _ = np.histogram2d(pos[:, 1], pos[:, 0], bins=n, range=[[0, n * PIX], [0, n * PIX]], weights=fnu)   # [y, x]
    dx_arc = L / (bx * 2**11) * 1e3 / (1 + z) / scale
    sig_part = 0.5 * dx_arc / PIX
    true = fftconvolve(img, gauss_kernel(sig_part), mode="same")          # noiseless, no PSF (particle -> cell smoothing only)
    conv = fftconvolve(true, psf, mode="same")
    # noise: 5 sigma total point-source flux f5 -> aperture flux f5 * EE(D/2); white noise per pixel
    f5 = 10 ** (-0.4 * (S["depth"][filt] - 31.4)); r_ap = S["D"] / 2
    npix_ap = np.pi * (r_ap / PIX) ** 2
    sig_pix = f5 * EE0(r_ap) / 5 / np.sqrt(npix_ap) / np.sqrt(mu)        # depth defined in the image plane
    rng = np.random.default_rng(A.seed + 10 * A.axis)
    obs = conv + rng.normal(0, sig_pix, conv.shape)
    sb1 = -2.5 * np.log10(sig_pix / PIX**2) + 31.4            # 1 sigma per-pixel surface brightness [mag/arcsec^2]
    print(f"z={z:.3f} {filt} {A.survey} axis {A.axis}: {n}^2 px, {scale:.2f} pkpc/\", DM {DM:.2f}, Moffat beta {mb:.2f}, "
          f"sigma_pix {sig_pix:.4f} nJy (1 sigma/pix = {sb1:.2f} mag/arcsec^2), particle sigma {sig_part:.2f} px", flush=True)
    # detection on the PSF-smoothed image (Gaussian FWHM 3 px kernel, photutils default practice), threshold in raw-pixel sigma
    kern = gauss_kernel(3.0 / 2.3548, size=5)
    sm = fftconvolve(obs, kern, mode="same")
    sig_sm = sig_pix * np.sqrt((kern**2).sum())               # noise of the smoothed (detection) image; thresholds are in its units
    seg = detect_sources(sm, S["thr"] * sig_sm, npixels=S["npix"])
    print(f"  detected {seg.nlabels} segments (threshold {S['thr']} x sigma_smoothed = {S['thr'] * sig_sm:.4f} nJy/pix) ({time.time() - t0:.0f} s)", flush=True)
    from scipy import ndimage
    labs = np.arange(1, seg.max_label + 1)
    fsum = ndimage.sum_labels(obs, seg.data, labs); npx = ndimage.sum_labels(np.ones_like(obs), seg.data, labs)
    keep = labs[fsum / (sig_pix * np.sqrt(np.maximum(npx, 1))) > 4]          # isophotal S/N > 4 (drops noise peaks)
    seg.keep_labels(keep, relabel=True)
    print(f"  isophotal S/N > 4: {seg.nlabels} kept ({time.time() - t0:.0f} s)", flush=True)
    seg = deblend_sources(sm, seg, npixels=S["npix"], nlevels=S["nlev"], contrast=S["contrast"], progress_bar=False)
    print(f"  deblended -> {seg.nlabels} ({time.time() - t0:.0f} s)", flush=True)
    segn = detect_sources(-sm, S["thr"] * sig_sm, npixels=S["npix"])
    if segn is not None:
        ln = np.arange(1, segn.max_label + 1)
        fn = ndimage.sum_labels(-obs, segn.data, ln); nn = ndimage.sum_labels(np.ones_like(obs), segn.data, ln)
        snr_neg = fn / (sig_pix * np.sqrt(np.maximum(nn, 1)))
        ln4 = ln[snr_neg > 4]; snr_neg_ap = np.zeros(0)
        if len(ln4):
            cm = np.array(ndimage.center_of_mass(-sm, segn.data, ln4)).reshape(-1, 2)[:, ::-1]
            apn = CircularAperture(cm, r=r_ap / PIX)
            snr_neg_ap = aperture_photometry(-obs, apn)["aperture_sum"].data / (sig_pix * np.sqrt(np.pi * (r_ap / PIX) ** 2))
    else:
        snr_neg = snr_neg_ap = np.zeros(0); ln4 = []
    M_neg = (-2.5 * np.log10(np.maximum(snr_neg_ap * sig_pix * np.sqrt(npix_ap) / EE(r_ap), 1e-30)) + 31.4 - DM + 2.5 * np.log10(1 + z))
    print(f"  inverted image: {np.sum(snr_neg > 4)} segments with iso S/N > 4, {np.sum(snr_neg_ap > 5)} with aperture S/N > 5", flush=True)
    err = np.full(obs.shape, sig_pix, dtype=np.float32)
    cat = SourceCatalog(obs, seg, convolved_data=sm, error=err)
    xc, yc = cat.xcentroid, cat.ycentroid
    kron = cat.kron_flux; kron_err = cat.kron_fluxerr
    apc = CircularAperture(np.column_stack([xc, yc]), r=r_ap / PIX)
    fap = aperture_photometry(obs, apc)["aperture_sum"].data
    snr_ap = fap / (sig_pix * np.sqrt(npix_ap))
    rhalf_obs = cat.fluxfrac_radius(0.5).value * PIX * scale  # pkpc (source plane for lensed variants), PSF-convolved, within the Kron aperture
    iso = cat.segment_flux
    true_seg = SourceCatalog(true, seg).segment_flux                     # intrinsic (noiseless, no PSF) flux in the segment
    m2M = lambda f: np.where(f > 0, -2.5 * np.log10(np.maximum(f, 1e-30)) + 31.4 - DM + 2.5 * np.log10(1 + z), np.nan)
    np.savez(A.out + "_cat.npz", M_neg=M_neg, mu=mu, snr_neg=snr_neg, snr_neg_ap=snr_neg_ap, sig_sm=sig_sm, z=z, survey=A.survey, axis=A.axis, filt=filt, sig_pix=sig_pix, sb1=sb1, scale=scale, DM=DM, pix=PIX,
             area_arcsec2=(n * PIX) ** 2, vol_cmpc3=L**3 * (n / np.ceil(Lang / PIX)) ** 2, x=xc, y=yc,
             M_kron=m2M(kron), M_ap=m2M(fap / EE(r_ap)), M_iso=m2M(iso), M_trueseg=m2M(true_seg), snr_ap=snr_ap,
             kron_snr=kron / kron_err, rhalf_obs=rhalf_obs, area=cat.area.value)
    # ---- halo matching (massive halos only): which segments hold the stars of each halo
    hm = d["hm"]; off = d["off"]; fl = d["flat"]; sel = np.where(hm >= MH_MATCH)[0]
    ix = np.clip((pos[:, 0] / PIX).astype(int), 0, n - 1); iy = np.clip((pos[:, 1] / PIX).astype(int), 0, n - 1)
    inside = (pos[:, 0] < n * PIX) & (pos[:, 1] < n * PIX)
    segid = np.where(inside, seg.data[iy, ix], -1)
    lab2row = {l: i for i, l in enumerate(cat.label)}
    rows = []
    RAP = int(round(1.0 / PIX))                                   # 1" radius (2" diameter) aperture, as Varadaraj+24
    yy, xx = np.mgrid[-RAP:RAP + 1, -RAP:RAP + 1]; inap = xx**2 + yy**2 <= RAP**2
    psf_sm = fftconvolve(psf, kern, mode="same")
    def cut(im, cx, cy):
        i0, j0 = int(round(cy)), int(round(cx))
        if i0 - RAP < 0 or j0 - RAP < 0 or i0 + RAP + 1 > n or j0 + RAP + 1 > n: return None
        return im[i0 - RAP:i0 + RAP + 1, j0 - RAP:j0 + RAP + 1]
    for k in sel:
        s = fl[off[k]:off[k + 1]]
        s = s[inside[s]]
        if len(s) == 0: continue
        f = fnu[s]; ftot = f.sum(); sid = segid[s]
        det = sid > 0
        if det.any():
            labs, inv = np.unique(sid[det], return_inverse=True); fl_lab = np.bincount(inv, weights=f[det])
            main = labs[np.argmax(fl_lab)]; j = lab2row[main]
            fmain_true = fl_lab.max(); nseg = len(labs)
            Mk, Ma, ra, own = m2M(kron[j]), m2M(fap[j] / EE(r_ap)), rhalf_obs[j], fmain_true / max(true_seg[j], 1e-30)
            snr_main = snr_ap[j]
        else:
            fmain_true, nseg, Mk, Ma, ra, own, snr_main = 0.0, 0, np.nan, np.nan, np.nan, np.nan, 0.0
        # intrinsic projected half-light radius of all R200 stars, around the L-weighted centre (periodic in the image plane)
        p = pos[s]; cen = (p * f[:, None]).sum(0) / ftot
        r = np.sqrt(((p - cen) ** 2).sum(1)) * scale; o = np.argsort(r)
        rh_all = r[o][np.searchsorted(np.cumsum(f[o]), 0.5 * ftot)]
        # half-light radius of the intrinsic light inside the main detected segment only
        if det.any():
            m = sid == main; pm, fm = p[m], f[m]; cm = (pm * fm[:, None]).sum(0) / fm.sum()
            rm = np.sqrt(((pm - cm) ** 2).sum(1)) * scale; om = np.argsort(rm)
            rh_det = rm[om][np.searchsorted(np.cumsum(fm[om]), 0.5 * fm.sum())]
        else:
            rh_det = np.nan
        # non-parametric sizes in a 1" aperture around the L-weighted centre: intrinsic (noiseless, no PSF, all pixels) and
        # observed (pixels with S/N > 5 in the smoothed detection image), PSF size (same method, PSF scaled to the thresholded flux)
        # subtracted in quadrature
        cx, cy = cen / PIX - 0.5
        ct, co, cs = cut(true, cx, cy), cut(obs, cx, cy), cut(sm, cx, cy)
        if ct is None:
            rnp_t = rnp_o = rnp_raw = np.nan
        else:
            rnp_t = np_radius(ct[inap]) * PIX * scale
            m5 = inap & (cs > 5 * sig_sm)
            if m5.sum() >= 3:
                rr = np_radius(co[m5]); fl5 = co[m5].sum()
                ps = psf * fl5; pss = psf_sm * fl5; c0 = psf.shape[0] // 2
                pp = ps[c0 - min(c0, RAP):c0 + min(c0, RAP) + 1, c0 - min(c0, RAP):c0 + min(c0, RAP) + 1]
                pq = pss[c0 - min(c0, RAP):c0 + min(c0, RAP) + 1, c0 - min(c0, RAP):c0 + min(c0, RAP) + 1]
                rp = np_radius(pp[pq > 5 * sig_sm]) if np.any(pq > 5 * sig_sm) else 0.0
                rnp_raw = rr * PIX * scale; rnp_o = np.sqrt(max(rr**2 - rp**2, 0)) * PIX * scale
            else:
                rnp_o = rnp_raw = np.nan
        rows.append((k, hm[k], m2M(ftot), m2M(f[det].sum()) if det.any() else np.nan, Mk, Ma, f[det].sum() / ftot,
                     fmain_true / ftot, nseg, own, rh_all, rh_det, ra, snr_main, rnp_t, rnp_o, rnp_raw))
    np.savetxt(A.out + "_halos.txt", np.array(rows), fmt="%.5g",
               header=f"{A.survey} {filt} z={z:.3f} axis {A.axis}: halo Mh M_true(R200) M_true(in any segment) M_kron(main seg) M_ap(main) "
                      "frac_L_detected frac_L_mainseg n_segments frac_mainseg_flux_from_this_halo rhalf_all[pkpc] rhalf_mainseg_intrinsic[pkpc] "
                      "rhalf_obs_main(PSF-conv, Kron)[pkpc] snr_ap_main rnp_intrinsic[pkpc] rnp_obs_5sig_PSFsub[pkpc] rnp_obs_5sig_raw[pkpc]")
    print(f"  wrote {A.out}_cat.npz ({len(cat.label)} sources), {A.out}_halos.txt ({len(rows)} halos >= {MH_MATCH:.1e}) "
          f"in {time.time() - t0:.0f} s", flush=True)

if __name__ == "__main__":
    main()
