"""Ray-traced fesc(R200) of the z = 7 discs (complement of the M1-flux fesc of analyse_z7.py), with the dashboard's
raytrace module (HEALPix nside 12 = 1728 control points on the R200 sphere, transmission exp(-sigma_N N_HI) from every
young star, photon-weighted with the run's BPASS rates).
usage: raytrace_z7.py [--stride N] run1 [run2 ...]  -> z7_rt.npy {run: {t, fesc_rt, ndot}} (merged with an existing file)"""
import os, re, sys
from multiprocessing import Pool
import h5py, numpy as np
sys.path.insert(0, "/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/analysis/dyablo_tools/dashboard_dyablo_reio")
from dashboard_reio_dyablo import raytrace
from dashboard_reio_dyablo.run import _sigma_n_blackbody
from analyse_z7 import snaps, centre, R200, LBOX

PC, MSUN, MP = 3.0857e18, 1.989e33, 1.6726e-24
SIG = _sigma_n_blackbody(5e4) * 1e4                                  # cm^2 (temp_black_body = 50000 K in all runs)
DIRS = raytrace.healpix_dirs(12)


def bpass(file, Z=0.001):
    rows = [l for l in open(file) if l.strip() and not l.lstrip().startswith("#")]
    nz = int(rows[1]); ages = np.array(rows[2].split(","), float); zs = np.array(rows[3].split(","), float)
    lq = np.log10(np.array([r.split(",") for r in rows[4:4 + nz]], float)); o = np.argsort(zs)
    l = np.array([np.interp(np.log10(Z), np.log10(zs[o]), lq[o, i]) for i in range(len(ages))])
    return lambda a: 10**np.interp(np.log10(np.maximum(a, 1e-30)), np.log10(ages), l)


def params(run):
    s = open(f"{run}.ini").read()
    g = lambda k: re.search(rf"^{k}\s*=\s*([^\s#]+)", s, re.M).group(1)
    return float(g("t_SNII")), float(g("eta_SNII")), g("emissivity_file"), float(g("emissivity_Z")), float(g("emissivity_tmax"))


def one(args):
    run, t, fg, fp = args
    halo = run.split("_")[1]; L = LBOX[halo]; r200 = R200[halo]
    tsn, eta, ef, ez, tmax = params(run); Q = bpass(ef, ez)
    try:
        with h5py.File(fp) as h:
            pp = {k: h[k][:] for k in ("coordinates", "mass", "birth_time")}
        with h5py.File(fg) as h:
            c = h["coordinates"][:][h["connectivity"][:]].mean(axis=1)
            rho, rhii, lev = h["rho"][:].astype(float), h["rho_HII"][:].astype(float), h["level"][:]
    except Exception:
        return run, None
    cen = centre(pp["coordinates"][pp["birth_time"] > 999], np.full(3, L / 2), r200)
    dx = L / (4 * 2.0**lev)
    nhi = np.maximum(rho - rhii, 0) * MSUN / PC**3 / MP                       # cm^-3, H only (as the code)
    new = (pp["birth_time"] >= 0) & (pp["birth_time"] < 999)
    age = t - pp["birth_time"][new]
    m = pp["mass"][new]
    w = np.where(age < tmax, np.where(age > tsn, m / (1 - eta), m) * Q(age), 0.0)
    rs = pp["coordinates"][new] - cen
    ins = np.linalg.norm(rs, axis=1) < r200
    o = dict(t=t, ndot=w[ins].sum(), fesc_rt=np.nan)
    if o["ndot"] > 0:
        half = r200 + 2 * dx.min()
        rc = c - cen
        sel = np.all(np.abs(rc) < half + dx[:, None] / 2, axis=1)
        o["fesc_rt"], _ = raytrace.fesc_halo(rc[sel] * PC, dx[sel] * PC, nhi[sel], rs[ins] * PC, w[ins],
                                             r200 * PC, SIG, DIRS, half=half * PC)
    return run, o


if __name__ == "__main__":
    a = sys.argv[1:]; stride = 1
    if a and a[0] == "--stride":
        stride = int(a[1]); a = a[2:]
    jobs = [(r, t, fg, fp) for r in a for (t, fg, fp) in snaps(r)[::stride]]
    with Pool(min(48, len(jobs))) as pool:
        res = pool.map(one, jobs, chunksize=1)
    S = np.load("z7_rt.npy", allow_pickle=True).item() if os.path.exists("z7_rt.npy") else {}
    for r in a:
        L_ = sorted([o for rr, o in res if rr == r and o is not None], key=lambda o: o["t"])
        if L_:
            S[r] = {k: np.array([o[k] for o in L_]) for k in L_[0]}
    np.save("z7_rt.npy", S, allow_pickle=True)
    for r in a:
        if r in S:
            d = S[r]; ok = np.isfinite(d["fesc_rt"])
            print(f"{r:32s} photon-weighted fesc_RT(R200) = {np.sum(d['fesc_rt'][ok] * d['ndot'][ok]) / np.sum(d['ndot'][ok]):.3f}"
                  f"  ({ok.sum()} snapshots)")
