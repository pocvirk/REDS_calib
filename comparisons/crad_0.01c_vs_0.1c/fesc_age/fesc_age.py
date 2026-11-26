"""Why does c_rad 0.1c give a higher f_esc than 0.01c? (PO 2026-11-26)
Test 1: ray-traced f_esc per star particle (dashboard raytrace.fesc_halo, same rays / opacity as fesc_RT_R200), photon-weighted
        in stellar age bins and halo mass bins.
Test 2: gas around young star particles (age < 5 Myr): n_H and x_HI of the host cell, mass-weighted within 0.1 / 0.3 pkpc,
        and stacked median radial profiles n_H(r), x_HI(r) (0.05-3 pkpc), per halo mass bin.
Halos / star association exactly as the dashboard (fof b = 0.15 catalogue of the dashboard run, dbtg.associate_star_halo2, R200).
usage: python -I fesc_age.py <rundir> <aexp> <out.npz>
"""
import sys, time
import numpy as np
import astropy.units as u
B = "/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026"
sys.path.insert(0, B + "/analysis/dyablo_tools/dashboard_dyablo_reio")
sys.path.insert(0, B + "/analysis/dyablo_tools")
from dashboard_reio_dyablo.run import DyabloRun, MPC, MP
from dashboard_reio_dyablo import galaxies, raytrace
from dashboard_reio_dyablo.rc import dashboard_tools_galaxies as dbtg

rundir, A, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
t0 = time.time()
run = DyabloRun(rundir)
it, g, p = [s for s in run.snapshots() if s[2] and abs(run.snapshot_aexp(s[1]) - A) < 2e-4][0]
a = run.snapshot_aexp(g); z = 1 / a - 1
boxh = run.lbox_mpc * run.h; ngrid = run.npart_1d
dbtg.set_cosmology(run.cosmo)
halos = dbtg.readfof(f"{rundir}/dashboard/fof/iter{it:07d}_b0.15/outputs", boxh, ngrid)
L = run.lbox_mpc
mbox = (run.cosmo.critical_density(0) * (L * u.Mpc).to(u.cm)**3).to(u.Msun) * run.cosmo.Om0
hmass = halos[:, 1] * mbox / ngrid**3
hx, hy, hz = (halos[:, 2] * L * u.Mpc, halos[:, 3] * L * u.Mpc, halos[:, 4] * L * u.Mpc)
spos, smass, sm_init, sage = galaxies.star_arrays(run, p, a)
allstarinds, hind = dbtg.associate_star_halo2(spos[:, 0] * u.Mpc, spos[:, 1] * u.Mpc, spos[:, 2] * u.Mpc, hx, hy, hz, hmass, boxh, Minf=1e7 * u.Msun)
hm = hmass[hind].to_value(u.Msun)
centres = np.array([hx[hind].value, hy[hind].value, hz[hind].value]).T
r200 = dbtg.R200(hmass[hind], run.cosmo).to(u.Mpc).value
ndot = run.photon_rate(smass, sage)
cc, tree = galaxies.cell_tree(run, g)
d = run.read_grid(g, ["rho", "rho_HII"])
nH = d["rho"] / MP / a**3 * 1e-6                       # physical cm^-3 (all gas as H, as dyablo / the ray tracer)
xHI = np.clip(1 - d["rho_HII"] / np.maximum(d["rho"], 1e-300), 0, 1)
nhi = nH * xHI
tocm = a * MPC * 100; sig = run.sigma_n * 1e4
dirs = raytrace.healpix_dirs(12)
dxc = L / (run.bx * 2.0**d["level"].min())
print(f"{run.prefix} it {it} z={z:.3f}: {len(hm)} halos, {len(smass)} stars, {len(cc)} cells ({time.time() - t0:.0f} s)", flush=True)

ns = len(smass)
fst = np.full(ns, np.nan); host = np.full(ns, np.nan); fh = np.full(len(hm), np.nan)
for k, ii in enumerate(allstarinds):
    ii = np.asarray(ii, dtype=int)
    if ii.size == 0 or ndot[ii].sum() <= 0: continue
    dx0 = d["dx"][tree.query(centres[k])[1]]; half = r200[k] + 2 * dx0
    idx = np.array(tree.query_ball_point(centres[k], np.sqrt(3) * half + dxc), dtype=int)
    rc = (cc[idx] - centres[k] + 0.5 * L) % L - 0.5 * L
    rs = (spos[ii] - centres[k] + 0.5 * L) % L - 0.5 * L
    fh[k], fs = raytrace.fesc_halo(rc * tocm, d["dx"][idx] * tocm, nhi[idx], rs * tocm, ndot[ii], r200[k] * tocm, sig, dirs, half=half * tocm)
    fst[ii] = fs; host[ii] = hm[k]
ok = np.isfinite(fh)
print(f"  ray tracing done ({time.time() - t0:.0f} s): global fesc_RT (halo-weighted) "
      f"{np.nansum(fh[ok] * [ndot[np.asarray(i, int)].sum() for i, o in zip(allstarinds, ok) if o]) / sum(ndot[np.asarray(i, int)].sum() for i, o in zip(allstarinds, ok) if o):.4f}", flush=True)

# test 2: gas around young stars
young = np.where((sage < 5) & (ndot > 0) & np.isfinite(host))[0]
rng = np.random.default_rng(1)
if len(young) > 4000: young = np.sort(rng.choice(young, 4000, replace=False))
redges = np.geomspace(0.05, 3.0, 13)                   # pkpc
rmax = redges[-1] / 1e3 / a                            # cMpc
mass_c = d["rho"] * d["vol"]
cell_nH = np.full(len(young), np.nan); cell_x = cell_nH.copy()
m01 = np.full((len(young), 2), np.nan); x01 = m01.copy()
prof_n = np.full((len(young), len(redges) - 1), np.nan); prof_x = prof_n.copy()
for j, s in enumerate(young):
    c0 = tree.query(spos[s])[1]; cell_nH[j], cell_x[j] = nH[c0], xHI[c0]
    idx = np.array(tree.query_ball_point(spos[s], rmax), dtype=int)
    dr = (cc[idx] - spos[s] + 0.5 * L) % L - 0.5 * L; r = np.sqrt((dr**2).sum(1)) * a * 1e3     # pkpc
    for q, rr in enumerate((0.1, 0.3)):
        m = r < rr
        if m.any(): w = mass_c[idx[m]]; m01[j, q] = np.sum(w * nH[idx[m]]) / w.sum(); x01[j, q] = np.sum(w * xHI[idx[m]]) / w.sum()
    b = np.digitize(r, redges) - 1
    for q in range(len(redges) - 1):
        m = b == q
        if m.any(): w = d["vol"][idx[m]]; prof_n[j, q] = np.sum(w * nH[idx[m]]) / w.sum(); prof_x[j, q] = np.sum(w * nhi[idx[m]]) / np.sum(w * nH[idx[m]])
np.savez(out, z=z, aexp=a, it=it, run=run.prefix, c_rad=run.c_rad, age=sage, ndot=ndot, fesc_star=fst, host_mh=host, mstar=smass,
         halo_mh=hm, halo_fesc=fh, young=young, cell_nH=cell_nH, cell_xHI=cell_x, nH_r=m01, xHI_r=x01, redges=redges, prof_nH=prof_n, prof_xHI=prof_x)
print(f"  wrote {out} ({len(young)} young stars profiled, {time.time() - t0:.0f} s)", flush=True)
