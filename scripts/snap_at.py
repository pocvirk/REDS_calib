"""print the iteration of the particle snapshot of <rundir> at scale factor a (|da| < 2e-4), or nothing (2026-11-19, auto_h2z.sh)"""
import sys
sys.path.insert(0, "/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/analysis/dyablo_tools/dashboard_dyablo_reio")
from dashboard_reio_dyablo.run import DyabloRun
r = DyabloRun(sys.argv[1]); a = float(sys.argv[2])
for it, g, p in r.snapshots():
    if p and abs(r.snapshot_aexp(g) - a) < 2e-4:
        print(it); break
