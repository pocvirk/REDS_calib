"""LF post-processing (PO 2026-11-26): extract halos (b=0.15 FoF, existing catalogue) + stars + R200 membership to a small npz,
so aperture / metallicity / dust variants can be computed offline.  usage: python -I extract.py <rundir> <iter> <out.npz>"""
import sys, os, glob
sys.path.insert(0, "/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/analysis/dyablo_tools/dashboard_dyablo_reio")
import numpy as np, astropy.units as u
from dashboard_reio_dyablo.run import DyabloRun
from dashboard_reio_dyablo import galaxies as G
from dashboard_reio_dyablo.rc import dashboard_tools_galaxies as dbtg
d, it, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
run = DyabloRun(d)
grid, part = [(g, p) for i, g, p in run.snapshots() if i == it][0]
a = run.snapshot_aexp(grid); z = 1 / a - 1
dbtg.set_cosmology(run.cosmo)
boxh = run.lbox_mpc * run.h; ngrid = run.npart_1d
fd = os.path.join(d, "dashboard", "fof", f"iter{it:07d}_b0.15")
fd = os.path.join(fd, "outputs"); assert glob.glob(os.path.join(fd, "*masst*")), fd
halos = dbtg.readfof(fd, boxh, ngrid)
boxsize = run.lbox_mpc * u.Mpc
mbox = (run.cosmo.critical_density(0) * boxsize.to(u.cm)**3).to(u.Msun) * run.cosmo.Om0
hmass = halos[:, 1] * mbox / ngrid**3
hx, hy, hz = (halos[:, 2] * boxsize, halos[:, 3] * boxsize, halos[:, 4] * boxsize)
spos, smass, sm_init, sage = G.star_arrays(run, part, a)
inds, hind = dbtg.associate_star_halo2(spos[:, 0] * u.Mpc, spos[:, 1] * u.Mpc, spos[:, 2] * u.Mpc, hx, hy, hz, hmass, boxh,
                                       Minf=1e7 * u.Msun, workers=16)
off = np.concatenate([[0], np.cumsum([len(i) for i in inds])]).astype(np.int64)
flat = np.concatenate([np.asarray(i, dtype=np.int64) for i in inds]) if len(inds) else np.zeros(0, np.int64)
hm = hmass[hind].value
np.savez(out, z=z, aexp=a, lbox=run.lbox_mpc, h=run.h, bx=run.bx, hm=hm, hpos=np.column_stack([hx[hind].value, hy[hind].value, hz[hind].value]),
         r200=dbtg.R200(hm * u.Msun, run.cosmo).value, off=off, flat=flat, spos=spos, smass=smass, sm_init=sm_init, sage=sage,
         mag_file=G.mag_table(run) or "")
print("wrote", out, "z", z, "halos", len(hm), "stars", len(smass), "members", len(flat))
