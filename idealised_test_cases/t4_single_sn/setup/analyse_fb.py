"""Negative-pressure fallback flavours on the idealised SN tests (make_inis.py): radial momentum, kinetic and thermal energy
vs time for A (floor), B (adiabat), C (RAMSES pf beta 0), the number of corrected cells per run (logs), and temperature
slices of the resolved cases. Reuses runs/fbcomp/analyse.py (history, slice_). Run from this directory.
-> fb_history.png, fb_slices.png, fb_summary.txt"""
import os, sys, re
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(H), "fbcomp"))
try:
    from analyse import history, slice_, setups          # runs/fbcomp/analyse.py
except ImportError:                                       # KB copy: same file, renamed analyse_base.py
    sys.path.insert(0, H); from analyse_base import history, slice_, setups
os.chdir(H)
FL = {"A": ("A: floor (current)", "#1aa39a"), "B": ("B: adiabat fallback", "#7048e8"), "C": ("C: RAMSES pf beta 0", "#c2255c"),
      "D": ("D: Tep entropy eta 0.1", "#e8590c"), "E": ("E: entropy fallback eta 0", "#2b8a3e")}
REFS = ["A_c02", "A_c01", "B_c02"]   # time-step references (resolved setups only)
FB = {"th": ("thermal (production)", "--"), "mech": ("mechanical", "-")}


def ncorr(run):
    """corrected cells over the run: A counts steps with a negative pressure (cells not printed)"""
    try:
        s = open(f"{run}.log").read()
    except OSError:
        return "missing"
    a = s.count("Negative pressure detected")
    b = sum(int(x) for x in re.findall(r"fallback \(adiabat\) cells: (\d+)", s))
    c = sum(int(x) for x in re.findall(r"Pressure fix cells: (\d+)", s))
    st = {k: sum(int(x) + int(y) for x, y in re.findall(rf"RK2 {k}: negative pressure cells (\d+), adiabat fallback cells (\d+)", s))
          for k in ("stage 1", "final")}
    return f"floor steps {a:5d} | adiabat cells {b:7d} | pf cells {c:7d} | p<0 cells stage 1 {st['stage 1']:7d}, final {st['final']:7d}"


Hs = {}
summ = open("fb_summary.txt", "w")
summ.write("# per run: corrected cells (logs); final radial momentum [Msun km/s], kinetic and thermal(-ambient) energy [erg];"
           " B/A and C/A ratios of the final values\n")
for name, (n, dx) in setups.items():
    for fb in FB:
        for fl in FL:
            run = f"{name}_{fb}_{fl}"
            try:
                Hs[run] = history(run, dx)
            except Exception as e:
                print(run, "skipped:", e); continue
            ts, o = Hs[run]
            summ.write(f"{run:22s} t_end {ts[-1]:.3f} Myr | p {o[-1, 0]:9.3e} Ek {o[-1, 1]:9.3e} Eth {o[-1, 2]:10.3e} | {ncorr(run)}\n")
        for ref in REFS:
            run = f"{name}_{fb}_{ref}"
            if os.path.exists(f"{run}.ini"):
                try:
                    Hs[run] = history(run, dx); ts, o = Hs[run]
                    summ.write(f"{run:22s} t_end {ts[-1]:.3f} Myr | p {o[-1, 0]:9.3e} Ek {o[-1, 1]:9.3e} Eth {o[-1, 2]:10.3e} | {ncorr(run)}\n")
                except Exception as e:
                    print(run, "skipped:", e)
        if f"{name}_{fb}_A" in Hs:
            A = Hs[f"{name}_{fb}_A"][1][-1]
            r = "  ".join(f"{fl}/A: p {Hs[f'{name}_{fb}_{fl}'][1][-1, 0] / A[0]:.4f} Ek {Hs[f'{name}_{fb}_{fl}'][1][-1, 1] / A[1]:.4f}"
                          for fl in list(FL)[1:] + REFS if f"{name}_{fb}_{fl}" in Hs)
            summ.write(f"   {name}_{fb}: {r}\n")
summ.close()
print(open("fb_summary.txt").read())

# histories: rows = setups, columns = momentum, E_kin, |E_th - ambient|
names = list(setups)
fig, ax = plt.subplots(len(names), 3, figsize=(15, 3.2 * len(names)), constrained_layout=True, sharex="row")
for i, name in enumerate(names):
    for fb, (fbl, ls) in FB.items():
        for fl, (fll, c) in FL.items():
            run = f"{name}_{fb}_{fl}"
            if run not in Hs:
                continue
            ts, o = Hs[run]
            for k in range(3):
                ax[i, k].plot(ts, np.abs(o[:, k]) if k else o[:, k], ls, color=c, lw=1.4, label=f"{fll}, {fbl}")
        run = f"{name}_{fb}_A_c01"
        if run in Hs:
            ts, o = Hs[run]
            for k in range(3):
                ax[i, k].plot(ts, np.abs(o[:, k]) if k else o[:, k], ls, color="k", lw=0.9, label=f"A at cfl 0.1 (reference), {fbl}")
    n, dx = setups[name]
    for k, yl in enumerate(["radial momentum [M$_\\odot$ km/s]", "kinetic energy [erg]", "|thermal - ambient| [erg]"]):
        a = ax[i, k]; a.set_yscale("log"); a.grid(alpha=0.3, which="both"); a.set_ylabel(yl, fontsize=8)
        a.set_title(f"n$_H$ = {n:g} cm$^{{-3}}$, dx = {dx:g} pc", fontsize=9)
    ax[i, 1].set_ylim(1e46, 2e51); ax[i, 2].set_ylim(1e46, 2e51)
for k in range(3):
    ax[-1, k].set_xlabel("t [Myr]")
ax[0, 0].legend(fontsize=6.5)
fig.suptitle("One SN (1e51 erg), uniform medium, cooling, production hydro (RK2, minmod, cfl 0.8): negative-pressure fallback "
             "flavours. Agreement = curves on top of each other.", fontsize=10)
fig.savefig("fb_history.png", dpi=95)

# T slices of the resolved cases (where the floor fires), thermal feedback (production)
cases = [("n100_dx0.3", 0.1), ("n1_dx2", 0.3), ("n1_dx12", 1.0)]
fig, ax = plt.subplots(len(cases), 3, figsize=(13, 4.1 * len(cases)), constrained_layout=True, squeeze=False)
for i, (name, t) in enumerate(cases):
    for j, fl in enumerate(FL):
        try:
            rho, T, tt, L = slice_(f"{name}_th_{fl}", setups[name][1], t)
        except Exception as e:
            print(e); continue
        im = ax[i, j].imshow(np.maximum(T, 1), origin="lower", extent=[0, L, 0, L], norm=LogNorm(1e2, 1e8), cmap="inferno")
        ax[i, j].set_title(f"{name} thermal, {FL[fl][0]}, t = {tt:.2f} Myr", fontsize=8.5)
    fig.colorbar(im, ax=ax[i, :], shrink=0.8, label="T [K] (floored to 1 K for display)")
fig.savefig("fb_slices.png", dpi=90)
