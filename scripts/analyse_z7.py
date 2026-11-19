"""z = 7 disc scan: photon escape fraction through spheres around the halo centre, SFR, stellar and gas masses.
fesc(R, t) = [sum over a shell of width W at R of (F . r_hat) dV / W]  /  [sum of src_ndot dV inside R]
(M1 fluxes fx/fy/fz_rad and src_ndot are in the same code units; light-crossing lag R/c_red ~ 1-3 Myr << 5 Myr outputs).
Reported: instantaneous fesc per snapshot and the photon-weighted mean over t >= TMIN (= total escaped / total emitted).
Centre: shrinking-sphere centre of the DM (birth_time = 1000 flag). New stars: 0 <= birth_time < 999.
usage: analyse_z7.py run1 [run2 ...]   -> z7_summary.npy (+ printed table)"""
import glob, re, sys, os
from multiprocessing import Pool
import h5py, numpy as np

R200 = {"1e9": 3880.0, "3e9": 5600.0, "1e10": 8360.0}
LBOX = {"1e9": 25000.0, "3e9": 25000.0, "1e10": 50000.0}
FR = (0.2, 0.5, 1.0)                                 # shells at these fractions of R200
TMIN = 50.0
ETA_SN = 0.2


def snaps(run):
    out = []
    for f in sorted(glob.glob(f"{run}/{run}_iter*.h5")):
        it = f.split("_iter")[1][:-3]
        x = f[:-3] + ".xmf"
        if not os.path.exists(x):
            continue
        t = float(re.search(r'Time TimeType="Single" Value="([^"]+)"', open(x).read()).group(1))
        out.append((t, f, f"{run}/{run}_particles_particles_iter{it}.h5"))
    return out


def centre(pos, guess, r0):
    c = guess.copy(); r = r0
    while r > 300:
        s = np.linalg.norm(pos - c, axis=1) < r
        if s.sum() < 50:
            break
        c = pos[s].mean(0); r *= 0.8
    return c


def one(args):
    run, t, fg, fp = args
    halo = run.split("_")[1]; L = LBOX[halo]; r200 = R200[halo]
    try:
        with h5py.File(fp) as h:
            pp = {k: h[k][:] for k in ("coordinates", "mass", "birth_time")}
        with h5py.File(fg) as h:
            c = h["coordinates"][:][h["connectivity"][:]].mean(axis=1)
            d = {k: h[k][:].astype(float) for k in ("rho", "rho_HII", "fx_rad", "fy_rad", "fz_rad", "src_ndot", "level")}
    except Exception as e:
        return run, None
    dm = pp["birth_time"] > 999
    cen = centre(pp["coordinates"][dm], np.full(3, L / 2), r200)
    dx = L / (4 * 2.0**d["level"]); V = dx**3; dxmin = dx.min()
    r = c - cen; rn = np.linalg.norm(r, axis=1); rhat = r / np.maximum(rn, 1e-10)[:, None]
    Fr = d["fx_rad"] * rhat[:, 0] + d["fy_rad"] * rhat[:, 1] + d["fz_rad"] * rhat[:, 2]
    o = dict(t=t)
    for f in FR:
        R = f * r200; W = max(2 * dxmin, 0.1 * R)
        sh = np.abs(rn - R) < W / 2
        o[f"Nout{f}"] = (Fr[sh] * V[sh]).sum() / W
        o[f"Nem{f}"] = (d["src_ndot"][rn < R] * V[rn < R]).sum()
        o[f"fesc{f}"] = o[f"Nout{f}"] / o[f"Nem{f}"] if o[f"Nem{f}"] > 0 else np.nan
    inside = rn < r200
    o["mgas"] = (d["rho"][inside] * V[inside]).sum()
    o["mgas_cold_dense"] = (d["rho"][inside & (rn < 0.2 * r200)] * V[inside & (rn < 0.2 * r200)]).sum()
    o["xHII"] = (d["rho_HII"][inside] * V[inside]).sum() / o["mgas"]
    new = (pp["birth_time"] >= 0) & (pp["birth_time"] < 999)
    o["mstar_new"] = pp["mass"][new].sum()
    age = t - pp["birth_time"][new]
    o["sfr10"] = (pp["mass"][new][age < 10] / np.where(age[age < 10] > 3, 1 - ETA_SN, 1)).sum() / 10e6   # Msun/yr (t_SNII <= 10)
    o["nnew"] = int(new.sum())
    return run, o


if __name__ == "__main__":
    runs = sys.argv[1:]
    jobs = [(r, t, fg, fp) for r in runs for (t, fg, fp) in snaps(r)]
    with Pool(min(32, max(1, len(jobs)))) as pool:
        res = pool.map(one, jobs)
    S = {r: sorted([o for rr, o in res if rr == r and o is not None], key=lambda o: o["t"]) for r in runs}
    S = {r: {k: np.array([o[k] for o in L]) for k in L[0]} for r, L in S.items() if L}
    if os.path.exists("z7_summary.npy"):                 # merge with earlier scans
        S = {**np.load("z7_summary.npy", allow_pickle=True).item(), **S}
    np.save("z7_summary.npy", S, allow_pickle=True)
    S = {r: S[r] for r in runs if r in S}
    print(f"{'run':28s} {'t_end':>5s} {'M*new':>8s} {'SFR':>7s} {'fesc0.2':>7s} {'fesc0.5':>7s} {'fesc1':>7s} {'xHII':>5s}   (photon-weighted, t>={TMIN:g})")
    for r, h in S.items():
        s = h["t"] >= TMIN
        fw = {f: h[f"Nout{f}"][s].sum() / max(h[f"Nem{f}"][s].sum(), 1e-300) for f in FR}
        print(f"{r:28s} {h['t'][-1]:5.0f} {h['mstar_new'][-1]:8.2e} {h['sfr10'][s].mean() if s.any() else np.nan:7.3f} "
              + " ".join(f"{fw[f]:7.3f}" for f in FR) + f" {h['xHII'][-1]:5.2f}")
