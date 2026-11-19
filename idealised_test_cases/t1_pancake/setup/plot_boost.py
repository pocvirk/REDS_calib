"""Galilean-invariance test of the dual-energy switches (2026-11-16 night).
Same EdS pancake as plot_eds.py, boosted by a uniform transverse peculiar velocity v_y = 1e5 km/s at z_i (decays as 1/a:
3400 km/s at a = 0.58, 2000 km/s at a = 1; ICs make_ic.py 64 1e5). With no y gradients, the y fluxes cancel exactly and
the x solution of the Euler equations is unchanged; only e_kin (hence e_int/e_tot) changes. A frame-independent scheme
gives identical boosted and unboosted pancakes. Shortly after the caustic (a_c = 0.5) the shock is young and weak, and
its heat is a few % of e_tot in the boosted frame: the 3D sheet situation.
usage: plot_boost.py -> boost_T.png, boost_rho.png, boost_summary.txt"""
import os
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "plot_eds.py")).read()
exec(src[: src.index("Ti = {}")])   # loaders (snap_dyablo, snap_ramses, load), analytic(), constants

PAIRS = [("dyablo RK2 + entropy eta=0.1 (Tep) + e_int remap", "e_dy_rk2_ent_ei"),
         ("dyablo RK2 no fix + e_int remap", "e_dy_rk2_ei"),
         ("dyablo RK2 + entropy + shock-aware beta=0.5", "e_dy_rk2_entb0.5_ei"),
         ("RAMSES MUSCL-Hancock + pressure fix beta=0.5", "e_ra_o2_pf"),
         ("RAMSES MUSCL-Hancock no fix", "e_ra_o2"),
         ("RAMSES 1st order + pressure fix beta=0.5", "e_ra_o1_pf")]
UNB = lambda n: n + "_v0" if n.startswith("e_ra") else n     # RAMSES unboosted twins rerun with the boosted runs' aout
TIMES = [0.58333333, 0.66666667, 0.75, 1.0]
summ = open(f"{H}/boost_summary.txt", "w")
summ.write("# scheme, a: unboosted | boosted: T_max [K], rho_max, shocked mass fraction (cells with T/mu > 1e4 K), in the slab |x-0.5|<0.15\n")
figs = {f: plt.subplots(len(PAIRS), len(TIMES), figsize=(4.2 * len(TIMES), 2.6 * len(PAIRS)), sharex=True, constrained_layout=True)
        for f in ("T", "rho")}
for i, (lab, name) in enumerate(PAIRS):
    for j, at in enumerate(TIMES):
        row = []
        for tag, nm, c in (("unboosted", UNB(name), "k"), ("boosted v_y", name + "_vy", "C3")):
            d = load(nm, at)
            if d is None and nm != name and tag == "unboosted":   # _v0 twin not run yet: original unboosted run
                d = load(name, at)
            for f, (fig, ax) in figs.items():
                a_ = ax[i, j]
                if d is not None:
                    a_.plot(d["x"], d[f], color=c, lw=1, marker="o", ms=2.5, label=f"{tag} (a={d['a']:.3f})")
            if d is None:
                row.append("   (missing)          ")
                continue
            s = np.abs(d["x"] - 0.5) < 0.15
            m = d["rho"][s]
            fsh = m[d["T"][s] > 1e4].sum() / m.sum()
            row.append(f"{d['T'].max():9.3e} {d['rho'].max():6.1f} {fsh:6.3f}")
        summ.write(f"{lab:48s} a={at:.3f}: " + " | ".join(row) + "\n")
        for f, (fig, ax) in figs.items():
            a_ = ax[i, j]
            a_.set(yscale="log", xlim=(0.38, 0.62))
            if f == "T":
                a_.set(ylim=(1e-3, 3e8))
            else:
                a_.set(ylim=(0.3, 100))
            if i == 0:
                a_.set_title(f"a = {at:.3f} (z = {1 / at - 1:.2f})")
            if j == 0:
                a_.set_ylabel(("T/$\\mu$ [K]" if f == "T" else "$\\rho/\\bar\\rho$") + "\n" + lab.replace(" + ", "\n+ ", 1), fontsize=7)
            if i == len(PAIRS) - 1:
                a_.set_xlabel("x / L$_{box}$")
            a_.legend(fontsize=6, loc="upper left")
for f, (fig, ax) in figs.items():
    fig.suptitle("Galilean test: EdS pancake (Tep et al. App. B) unboosted (black) vs boosted by a uniform transverse v$_y$ "
                 "(1e5 km/s at z$_i$ = 3400 km/s at a = 0.58; red). A frame-independent scheme gives identical curves.", fontsize=10)
    fig.savefig(f"{H}/boost_{f}.png", dpi=75)
summ.close()
print(open(f"{H}/boost_summary.txt").read())
