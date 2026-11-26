"""sanity check of the aperture variant: cumulative L1600(<r) around the brightest finest cell, the L-weighted centre and the FoF centre."""
import sys; sys.path.insert(0, "/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/analysis/dyablo_tools/dashboard_dyablo_reio")
import numpy as np
from dashboard_reio_dyablo.rc import dashboard_tools_galaxies as dbtg
d = np.load(sys.argv[1], allow_pickle=True); ref = np.loadtxt(sys.argv[2])
T = dbtg.gen_age_Z_interpolator(str(d["mag_file"]))[0]
a = float(d["aexp"]); L = float(d["lbox"]); off = d["off"]; fl = d["flat"]
dx = L / (int(d["bx"]) * 2**11)
Lb = d["sm_init"] * 10 ** (-0.4 * T(d["sage"], 1e-3))
c = np.concatenate([[0], np.cumsum(Lb[fl])]); tot = c[off[1:]] - c[off[:-1]]
mag = np.where(tot > 0, -2.5 * np.log10(np.maximum(tot, 1e-300)), np.nan)
print("baseline vs dashboard mags file (brightest 5):", np.sort(mag[np.isfinite(mag)])[:5].round(2), np.sort(ref[np.isfinite(ref[:, 2]), 2])[:5].round(2))
rr = np.array([0.25, 0.5, 1, 2, 4, 8])   # pkpc
print("halo  logMh  R200[pkpc]  M_UV  age_med(L-wtd,Myr) | L(<r)/L(R200) around brightest cell for r =", rr, "| same around L-weighted centre | offset brightest cell - FoF centre [pkpc]")
for k in np.argsort(mag)[:12]:
    s = fl[off[k]:off[k + 1]]; p = d["spos"][s]; l = Lb[s]
    ijk = np.floor(p / dx).astype(np.int64)
    key = ijk[:, 0] * 2**40 + ijk[:, 1] * 2**20 + ijk[:, 2]; u, inv = np.unique(key, return_inverse=True)
    j = np.argmax(np.bincount(inv, weights=l)); cb = (ijk[inv == j][0] + 0.5) * dx
    def prof(cen):
        dr = (p - cen + 0.5 * L) % L - 0.5 * L; r = np.sqrt((dr**2).sum(1)) * a * 1e3
        return np.array([l[r <= x].sum() / l.sum() for x in rr])
    h = d["hpos"][k]; dh = (p - h + 0.5 * L) % L - 0.5 * L; cl = h + (l[:, None] * dh).sum(0) / l.sum()
    o = np.sqrt((((cb - h + 0.5 * L) % L - 0.5 * L)**2).sum()) * a * 1e3
    age = d["sage"][s]; ia = np.argsort(age); am = age[ia][np.searchsorted(np.cumsum(l[ia]), 0.5 * l.sum())]
    print(f"{k:6d} {np.log10(d['hm'][k]):.2f} {d['r200'][k] * a * 1e3:6.2f} {mag[k]:6.2f} {am:6.1f} |", prof(cb).round(2), "|", prof(cl).round(2), f"| {o:.2f}")
