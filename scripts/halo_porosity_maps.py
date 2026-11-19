"""Halo maps to illustrate why the production hydro (h2) gives a higher fesc than 1st order at fixed recipe (2026-11-19).
Same halos (same ICs, matched by position) in the 1st-order and h2 versions of 3 recipes at a = 0.100 (z = 9).

  compute <rundir> <label> <out.npz> : per halo, cube of half-width 2 R200 painted at the finest local cell size
        (raytrace.paint), centred on the run's own FoF centre:
        N_H and N_HI columns through the slab |z| < R200, mass-weighted T through the same slab, young stars (< 10 Myr),
        and the photon-weighted transmission sky map on the R200 sphere (HEALPix nside 12, same rays and opacity as the
        dashboard's ray-traced fesc: exp(-sigma N_HI) from every star group, weighted by the stars' photon rates).
  plot <out.npz> ...                : one figure per halo (rows = runs, columns = N_H, N_HI, T, sky map)
                                     -> halo_porosity_<k>.png, + halo_porosity_summary.txt
Halos: the NHALO most massive ones of REF (h2_eps0.03_mech_snx2) at a=0.100."""
import os, sys
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
B = "/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026"
sys.path.insert(0, f"{B}/analysis/dyablo_tools/dashboard_dyablo_reio")
R = f"{B}/runs/reio_v2"
REF, AT, NHALO = f"{R}/h2_eps0.03_mech_snx2", 0.100, 3
KB = 1.380649e-23


def catalogue(rundir, at=AT):
    from dashboard_reio_dyablo.run import DyabloRun
    run = DyabloRun(rundir)
    snaps = [(abs(run.snapshot_aexp(g) - at), it, g, p) for it, g, p in run.snapshots() if p]
    _, it, g, p = min(snaps)
    cat = np.loadtxt(f"{rundir}/dashboard/halos_iter{it:07d}.txt")
    return run, it, g, p, cat


def compute(rundir, label, out):
    from scipy.spatial import cKDTree
    import h5py
    from dashboard_reio_dyablo import raytrace, galaxies
    from dashboard_reio_dyablo.run import MPC, MP
    run, it, gf, pf, cat = catalogue(rundir)
    _, _, _, _, ref = catalogue(REF)
    top = ref[np.argsort(-ref[:, 4])[:NHALO]]
    a = run.snapshot_aexp(gf)
    L = run.lbox_mpc
    with h5py.File(gf) as h:
        rho, rhii, e = h["rho"][()], h["rho_HII"][()], h["e_tot"][()]
        ek = 0.5 * (h["rho_vx"][()]**2 + h["rho_vy"][()]**2 + h["rho_vz"][()]**2) / rho
        lev = h["level"][()]
    dx = L / (run.bx * 2.0**lev)
    nh = rho / MP / a**3 * 1e-6                                   # physical cm^-3 (as the dashboard)
    xh = np.clip(rhii / rho, 0, 1)
    nhi = nh * (1 - xh)
    mu = 1 / (0.76 * (1 + xh) + 0.06)                             # H ionisation only, He neutral
    T = (2 / 3) * (e - ek) / rho * (MPC / 3.15576e13)**2 / a**2 * MP / KB * mu
    del e, ek, rhii
    cc = run.cell_centers(gf)
    tree = cKDTree(cc, boxsize=L * (1 + 1e-12))
    spos, smass, sm_init, sage = galaxies.star_arrays(run, pf, a)
    ndot = run.photon_rate(smass, sage)
    tocm = a * MPC * 100
    sig = run.sigma_n * 1e4
    dirs = raytrace.healpix_dirs(12)
    res = dict(label=label, a=a, it=it)
    for k, hr in enumerate(top):
        d = np.sqrt(np.sum(((cat[:, 1:4] - hr[1:4] + 0.5 * L) % L - 0.5 * L)**2, axis=1))
        j = int(np.argmin(d))
        h = cat[j] if d[j] < 0.5 * hr[5] else hr                  # own FoF centre, else the reference one
        c, r200 = h[1:4], h[5]
        half = 2 * r200
        idx = np.array(tree.query_ball_point(c, np.sqrt(3) * half + dx.max()), dtype=int)
        rel = (cc[idx] - c + 0.5 * L) % L - 0.5 * L
        G = {}
        for name, v in (("nh", nh), ("nhi", nhi), ("nhT", nh * T)):
            G[name], dv, lo = raytrace.paint(rel, dx[idx], v[idx], half)
        n = G["nh"].shape[0]
        zc = lo + (np.arange(n) + 0.5) * dv
        sl = np.abs(zc) < r200                                    # slab |z| < R200
        dl = dv * tocm
        NH = G["nh"][:, :, sl].sum(-1) * dl
        NHI = G["nhi"][:, :, sl].sum(-1) * dl
        Tm = G["nhT"][:, :, sl].sum(-1) / np.maximum(G["nh"][:, :, sl].sum(-1), 1e-300)
        rs = (spos - c + 0.5 * L) % L - 0.5 * L
        rr = np.sqrt(np.sum(rs**2, axis=1))
        yng = (np.all(np.abs(rs) < half, axis=1)) & (sage < 10)
        ins = (rr < r200) & (ndot > 0)
        # photon-weighted transmission per direction (rays as raytrace.fesc_halo, kept per control point)
        sky = np.full(len(dirs), np.nan)
        if ins.any():
            Gc = G["nhi"]
            rstar, w = rs[ins] * tocm, ndot[ins]
            vox = np.clip(np.floor((rstar - lo * tocm) / (dv * tocm)).astype(int), 0, n - 1)
            key = np.ravel_multi_index(tuple(vox.T), (n, n, n))
            uk, inv = np.unique(key, return_inverse=True)
            wg = np.bincount(inv, weights=w)
            order = np.argsort(-wg)[:2000]
            start = np.array([rstar[inv == g].mean(0) for g in order])
            ends = r200 * tocm * dirs
            nstep = int(np.ceil(2 * r200 / (0.5 * dv)))
            f = (np.arange(nstep) + 0.5) / nstep
            acc = np.zeros(len(dirs))
            for c0 in range(0, len(start), 8):
                s = start[c0:c0 + 8]
                seg = ends[None] - s[:, None]
                Ls = np.linalg.norm(seg, axis=-1)
                pts = s[:, None, None] + seg[:, :, None] * f[None, None, :, None]
                ii = np.floor((pts - lo * tocm) / (dv * tocm)).astype(int)
                ok = np.all((ii >= 0) & (ii < n), axis=-1)
                nn = np.where(ok, Gc[tuple(np.clip(ii, 0, n - 1).transpose(3, 0, 1, 2))], 0.0)
                acc += (np.exp(-sig * nn.sum(-1) * Ls / nstep) * wg[order[c0:c0 + 8], None]).sum(0)
            sky = acc / wg[order].sum()
        inr = np.linalg.norm(rel, axis=1) < r200
        mgas = np.sum(nh[idx][inr] * (dx[idx][inr] * tocm)**3) * MP * 1e3 / 1.989e33   # Msun (H only)
        vf = np.sum((dx[idx][inr]**3)[nh[idx][inr] < 0.1]) / np.sum(dx[idx][inr]**3)
        res[f"h{k}"] = dict(c=c, r200=r200, mh=h[4], mstar=h[7], fesc_rt=h[15], fesc_m1=h[10], NH=NH, NHI=NHI, T=Tm,
                            ext=half * 1e3, young=rs[yng][:, :2] * 1e3, sky=sky, mgas=mgas, vf01=vf, dv=dv * 1e3)
        print(f"{label} halo {k}: Mh {h[4]:.2e} R200 {r200 * 1e3:.1f} ckpc, voxel {dv * 1e3:.2f} ckpc, n {n}, "
              f"fesc_RT {h[15]:.3f}, sky mean {np.nanmean(sky):.3f}, Mgas(H) {mgas:.2e}, V(n<0.1)/V {vf:.2f}", flush=True)
    np.save(out, res, allow_pickle=True)


def plot(files):
    import healpy as hp
    R_ = [np.load(f, allow_pickle=True).item() for f in files]
    summ = open("halo_porosity_summary.txt", "w")
    summ.write("# label halo Mh Mstar fesc_RT(dashboard) sky-mean transmission  open-sky fraction (T>0.5)  "
               "Mgas_H(<R200) V(n_H<0.1)/V(<R200)\n")
    for k in range(NHALO):
        nr = len(R_)
        fig = plt.figure(figsize=(17, 3.3 * nr))
        for i, r in enumerate(R_):
            h = r[f"h{k}"]
            e = h["ext"]
            ext = [-e, e, -e, e]
            panels = [(h["NH"], LogNorm(1e19, 1e23), "viridis", "N$_H$ [cm$^{-2}$], |z| < R$_{200}$"),
                      (np.maximum(h["NHI"], 1e14), LogNorm(1e16, 1e23), "magma_r", "N$_{HI}$ [cm$^{-2}$] (1/$\\sigma$ = 1.6e17)"),
                      (h["T"], LogNorm(1e2, 1e7), "inferno", "mass-weighted T [K]")]
            for jc, (img, nrm, cm, tl) in enumerate(panels):
                ax = fig.add_subplot(nr, 4, 4 * i + jc + 1)
                im = ax.imshow(img.T, origin="lower", extent=ext, norm=nrm, cmap=cm)
                ax.add_patch(plt.Circle((0, 0), h["r200"] * 1e3, fill=False, color="w", lw=0.8, ls="--"))
                if jc == 0 and len(h["young"]):
                    ax.plot(h["young"][:, 0], h["young"][:, 1], ".", ms=1.5, color="cyan", alpha=0.7)
                ax.set_title(f"{r['label']}: {tl}" if jc == 0 else tl, fontsize=8)
                ax.tick_params(labelsize=6)
                if i == nr - 1:
                    ax.set_xlabel("ckpc", fontsize=7)
                plt.colorbar(im, ax=ax, fraction=0.046, pad=0.02).ax.tick_params(labelsize=6)
            s = h["sky"]
            op = np.nanmean(s > 0.5) if np.isfinite(s).any() else np.nan
            hp.mollview(np.log10(np.clip(s, 1e-4, 1)) if np.isfinite(s).any() else np.full(len(s), hp.UNSEEN),
                        fig=fig.number, sub=(nr, 4, 4 * i + 4), min=-4, max=0, cmap="cividis", cbar=True,
                        title=f"log transmission at R200: fesc {np.nanmean(s):.3f}, open (>0.5) {op:.2f}",
                        unit="", notext=True)
            plt.gca().title.set_fontsize(8)
            summ.write(f"{r['label']:32s} {k} {h['mh']:.2e} {h['mstar']:.2e} {h['fesc_rt']:.3f} {np.nanmean(s):.3f} "
                       f"{op:.2f} {h['mgas']:.2e} {h['vf01']:.2f}\n")
        h0 = R_[0][f"h{k}"]
        fig.suptitle(f"halo {k}: M$_h$ ~ {h0['mh']:.1e} M$_\\odot$, z = 9; maps 4 R$_{{200}}$ wide (dashed circle R$_{{200}}$), "
                     "cyan: stars < 10 Myr. Sky map: photon-weighted transmission exp(-$\\sigma$N$_{HI}$) from all stars "
                     "to each direction on the R$_{200}$ sphere", fontsize=10)
        fig.tight_layout(rect=(0, 0, 1, 0.98))
        fig.savefig(f"halo_porosity_{k}.png", dpi=85)
    summ.close()
    print(open("halo_porosity_summary.txt").read())


if __name__ == "__main__":
    if sys.argv[1] == "compute":
        compute(*sys.argv[2:5])
    else:
        plot(sys.argv[2:])
