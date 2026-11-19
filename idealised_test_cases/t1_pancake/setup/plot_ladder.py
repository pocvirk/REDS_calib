"""Galilean test with a ladder of boosts (2026-11-17): EdS pancake (Tep et al. App. B) with a uniform transverse v_y.
v_y decays as 1/a: VY at z_i = 0, 1.5e4, 3e4, 6e4, 1e5 km/s -> 0, 504, 1009, 2018, 3363 km/s at a = 0.583
(0, 294, 588, 1176, 1961 km/s at z = 0); the pancake infall speed is ~1800 km/s.
usage: plot_ladder.py -> ladder_T.png, ladder_summary.txt"""
import os
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "plot_eds.py")).read()
exec(src[: src.index("Ti = {}")])   # loaders (load), constants, H
SCHEMES = [("dyablo RK2 + entropy eta=0.1 (Tep et al.)", "e_dy_rk2_ent_ei"),
           ("RAMSES MUSCL-Hancock + pressure_fix 0.5", "e_ra_o2_pf"),
           ("dyablo RK2, no switch", "e_dy_rk2_ei"),
           ("RAMSES MUSCL-Hancock, no fix", "e_ra_o2"),
           ("dyablo RK2 + entropy only where e_int < 0 (eta = 0)", "e_dy_rk2_eta0_ei"),
           ("dyablo RK2 + adiabat fallback where p < 0", "e_dy_rk2_fbad_ei")]
BOOST = [("0", ""), ("504", "_vy15k"), ("1009", "_vy30k"), ("2018", "_vy60k"), ("3363", "_vy")]
TIMES = [0.66666667, 1.0]
C = ["#000000", "#2a6fdb", "#1aa39a", "#e8590c", "#c2255c"]


def run(name, suf):
    if suf == "" and name.startswith("e_ra"):     # unboosted RAMSES: _v0 twin (same aout as the boosted runs), else original
        return [name + "_v0", name]
    return [name + suf]


summ = open(f"{H}/ladder_summary.txt", "w")
summ.write("# T_max [K] / rho_max / shocked mass fraction (T/mu > 1e4 K, slab |x-0.5|<0.15) per boost v_y(a=0.583) [km/s]\n")
fig, ax = plt.subplots(len(SCHEMES), len(TIMES), figsize=(6.2 * len(TIMES), 2.9 * len(SCHEMES)), sharex=True, constrained_layout=True)
for i, (lab, name) in enumerate(SCHEMES):
    for j, at in enumerate(TIMES):
        row = []
        for (vy, suf), c in zip(BOOST, C):
            d = None
            for nm in run(name, suf):
                d = load(nm, at)
                if d is not None:
                    break
            if d is None:
                row.append(f"{vy:>5s}: missing")
                continue
            ax[i, j].plot(d["x"], d["T"], color=c, lw=1.2, marker="o", ms=2, label=f"v$_y$ = {vy} km/s")
            s = np.abs(d["x"] - 0.5) < 0.15; m = d["rho"][s]
            row.append(f"{vy:>5s}: {d['T'].max():8.2e} {d['rho'].max():5.1f} {m[d['T'][s] > 1e4].sum() / m.sum():5.2f}")
        summ.write(f"{lab:44s} a={at:.3f} | " + " | ".join(row) + "\n")
        a_ = ax[i, j]
        a_.set(yscale="log", xlim=(0.4, 0.6), ylim=(1e-3, 3e8))
        if i == 0:
            a_.set_title(f"a = {at:.3f} (z = {1 / at - 1:.2f})")
        if j == 0:
            a_.set_ylabel("T/$\\mu$ [K]\n" + lab.replace(" + ", "\n+ ", 1).replace(", ", ",\n", 1), fontsize=8)
        if i == len(SCHEMES) - 1:
            a_.set_xlabel("x / L$_{box}$")
        a_.grid(alpha=0.25, lw=0.5)
ax[0, 0].legend(fontsize=7, loc="upper left", title="boost at a = 0.58", title_fontsize=7)
fig.suptitle("Galilean test, boost ladder: same pancake with a uniform transverse v$_y$ (values at a = 0.58; pancake infall ~1800 km/s). "
             "Frame independence = all colours on top of each other.", fontsize=9)
fig.savefig(f"{H}/ladder_T.png", dpi=90)
summ.close()
print(open(f"{H}/ladder_summary.txt").read())
