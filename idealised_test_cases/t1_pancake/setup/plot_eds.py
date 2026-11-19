"""EdS gas-only Zel'dovich pancake (Tep, Aubert, Ocvirk & Marchal, App. B setup) vs their analytical solution (eqs. B1-B4):
  rho/rho0 = 1/(1 + b cos kq),  u = H0 (1+z_c)/(1+z)^(1/2) sin(kq)/k,  x = q + b sin(kq)/k,  b = (1+z_c)/(1+z)
  T = T_i [ ((1+z)/(1+z_i))^3 rho/rho0 ]^(2/3)   (T_i = each code's own initial T/mu at z_i = 50; RAMSES 35.3 K, dyablo 34.8 K)
Valid outside the shocked region.  Pre-shock gas follows it exactly (in planar symmetry the gravity on a fluid element depends only
on the mass between it and the mid-plane), so after the caustic the curve is the outer stream up to the mid-plane (Tep's Fig. B2).
Points: one per cell along x (native resolution).  Thin black line: same code, 2 more AMR levels (reference, as Tep's N=1024).
Style = scheme: dashed/open = 1st order; dotted/small = dyablo 'Euler + slopes' (minmod slopes, forward-Euler step: 2nd order in space
only); solid/filled = 2nd order in space and time (RAMSES MUSCL-Hancock, dyablo SSP-RK2).  Colour = dual-energy fix.
usage: plot_eds.py -> eds_z2.png, eds_z0.png, eds_summary.txt"""
import glob, os, sys
import numpy as np, h5py
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
TOOLS = "/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/analysis/dyablo_tools/dashboard_dyablo_reio"
sys.path.insert(0, TOOLS)
from dashboard_reio_dyablo import ramses_reader as rr
from dashboard_reio_dyablo.run import DyabloRun
MP, KB, MPC, MYR = 1.67262192e-27, 1.380649e-23, 3.0856775814913673e22, 3.15576e13
H = os.path.dirname(os.path.abspath(__file__))
H0, L, zc, zi = 67.0, 64.0 / 0.67, 1.0, 50.0
ai, ac = 1 / (1 + zi), 1 / (1 + zc)


def analytic(a, Ti):
    b = a / ac
    q = np.linspace(0, 0.5, 400001)
    x = q + b * np.sin(2 * np.pi * q) / (2 * np.pi)
    if b > 1:                                   # outer stream up to the first crossing of the mid-plane
        q = q[: np.argmax(x >= 0.5) + 1]; x = x[: len(q)]
    rho = 1 / (1 + b * np.cos(2 * np.pi * q))
    v = H0 * 2 * np.sqrt(a) * np.sin(2 * np.pi * q) * L / (2 * np.pi)
    T = Ti * (ai / a)**2 * rho**(2 / 3)
    X = np.concatenate([x, [np.nan], 1 - x[::-1]])
    m = lambda f, s: np.concatenate([f, [np.nan], s * f[::-1]])
    return X, m(rho, 1), m(v, -1), m(T, 1)


def column(x, y, z, dx):
    """one cell per x position: cells containing the line (y0, z0)"""
    y0 = z0 = 0.37 * L / 64
    return (np.abs(y - y0) < dx / 2) & (np.abs(z - z0) < dx / 2)


def snap_dyablo(name, at):
    d = f"{H}/{name}"
    if not os.path.exists(f"{d}/last.ini"):
        return None
    run = DyabloRun(d)
    snaps = [(run.snapshot_aexp(s[1]), s[1]) for s in run.snapshots()]
    a, g = min(snaps, key=lambda s: abs(s[0] - at))
    if abs(a - at) > 0.05 * at:
        return None
    with h5py.File(g) as h:
        rho, e = h["rho"][()], h["e_tot"][()]
        vx = h["rho_vx"][()] / rho
        ek = 0.5 * (h["rho_vx"][()]**2 + h["rho_vy"][()]**2 + h["rho_vz"][()]**2) / rho
        lev = h["level"][()]
    T = (2 / 3) * (e - ek) / rho * (MPC / MYR)**2 / a**2 * MP / KB
    c = run.cell_centers(g); dx = L / (4 * 2.0**lev)
    s = column(c[:, 0], c[:, 1], c[:, 2], dx)
    rbar = np.sum(rho * dx**3) / L**3
    return a, c[s, 0] / L, rho[s] / rbar, vx[s] * MPC / MYR / a / 1e3, T[s], lev[s] + 2


def snap_ramses(name, at):
    best = None
    for d in sorted(glob.glob(f"{H}/{name}/output_*")):
        f = f"{d}/info_{d[-5:]}.txt"
        if os.path.exists(f):
            a = float([l for l in open(f) if l.startswith("aexp")][0].split("=")[1])
            if best is None or abs(a - at) < abs(best[0] - at):
                best = (a, d)
    if best is None or abs(best[0] - at) > 0.05 * at:
        return None
    a, d = best
    inf = {l.split("=")[0].strip(): l.split("=")[1].strip() for l in open(f"{d}/info_{d[-5:]}.txt") if "=" in l}
    ul, ut = float(inf["unit_l"]), float(inf["unit_t"])
    c = rr.read_cells(d, rt=False)
    T = c["pressure"] / c["density"] * (ul / ut)**2 * MP * 1e3 / (KB * 1e7)
    dx = 0.5**c["level"]
    s = column(c["x"] * L, c["y"] * L, c["z"] * L, dx * L)
    rbar = np.sum(c["density"] * dx**3)
    return a, c["x"][s], c["density"][s] / rbar, c["velocity_x"][s] * ul / ut / 1e5, T[s], c["level"][s]


def load(name, at):
    s = (snap_dyablo if name.startswith("e_dy") else snap_ramses)(name, at)
    if s is None:
        return None
    a, x, rho, v, T, lev = s
    o = np.argsort(x)
    return dict(a=a, x=x[o], rho=rho[o], v=v[o], T=T[o], lev=lev[o])


Ti = {}
for code, name in (("RAMSES", "e_ra_o2"), ("dyablo", "e_dy_o2")):
    s = load(name, ai)
    Ti[code] = np.median(s["T"] / s["rho"]**(2 / 3)) if s else {"RAMSES": 1.356e-2 / ai**2, "dyablo": 317.5 * (zi / 151)**2}[code]
    print(f"{code}: T_i/mu = {Ti[code]:.2f} K", flush=True)

FIX = {"none": ("k", "no fix"),  # dyablo runs: 1st order beta fix without coarsening; entropy runs with the internal-energy remap
       "b05": ("C1", "pressure fix beta=0.5"), "ratio": ("C6", "Enzo ratio eta=1e-3"),
       "ent": ("C0", "entropy eta=0.1 (Tep et al.)")}
SCH = {"o1": ("1st order", "--", 4, "none"), "eu": ("Euler+slopes", ":", 2.5, None), "o2": ("2nd order", "-", 3.5, None)}
RUNS = {"RAMSES": [("e_ra_o1", "o1", "none"), ("e_ra_o1_pf", "o1", "b05"), ("e_ra_o2", "o2", "none"), ("e_ra_o2_pf", "o2", "b05")],
        "dyablo": [("e_dy_o1", "o1", "none"), ("e_dy_o1_pf_nc", "o1", "b05"),
                   ("e_dy_o2", "eu", "none"), ("e_dy_o2_ent_ei", "eu", "ent"),
                   ("e_dy_rk2_ei", "o2", "none"), ("e_dy_rk2_ent_ei", "o2", "ent")]}
REF = {"RAMSES": "e_ra_o2_ref", "dyablo": "e_dy_rk2_ent_ref_ei"}
summ = open(f"{H}/eds_summary.txt", "w")
YL = {"z2": dict(rho=(0.4, 8), T=(1e-2, 1e7), Tz=(1e-2, 1e7)), "z0": dict(rho=(0.2, 60), T=(1e-3, 3e8), Tz=(1e5, 3e8))}
for zt, at in (("z2", 1 / 3), ("z0", 1.0)):
    fig, ax = plt.subplots(6, 2, figsize=(14, 23), sharex="row", constrained_layout=True)
    for j, code in enumerate(("RAMSES", "dyablo")):
        X, Ra, Va, Ta = analytic(at, Ti[code])
        ok = ~np.isnan(X)
        col = ax[:, j]
        for i, A in enumerate((Ra, Va, Ta, Ta)):
            col[i].plot(X, A, color="orange", lw=6, alpha=0.5, zorder=1, label="analytical (Tep et al. B1-B4)" if i == 0 else None)
        col[4].axhline(1, color="orange", lw=6, alpha=0.5, zorder=1)
        # shocked region from the reference run (T > 1e4 K), strong-shock estimate T/mu = 3/16 m_p v_in^2 / k_B
        xs = 0.5
        r = load(REF[code], at)
        if r:
            for i, f in enumerate(("rho", "v", "T", "T")):
                col[i].plot(r["x"], r[f], color="0.3", lw=0.8, zorder=2, label=("RK2 + entropy + e_int remap, +2 levels (reference)" if code == "dyablo" else "MUSCL-Hancock no fix, +2 levels (reference)") if i == 0 else None)
            col[5].plot(r["x"], r["lev"], color="0.3", lw=0.8)
            hot = np.where((r["T"] > 1e6) & (r["x"] < 0.5))[0]
            if len(hot) and at > 0.5:
                xs = r["x"][hot[0]]
                vin = abs(np.interp(xs, X[ok][: ok.sum() // 2], Va[ok][: ok.sum() // 2]))
                Tsh = 3 / 16 * MP * (vin * 1e3)**2 / KB
                col[3].axhline(Tsh, color="C3", ls=":", lw=1.5, label=f"strong shock 3/16 m$_p$v$_{{in}}^2$/k = {Tsh:.1e} K (v$_{{in}}$ = {vin:.0f} km/s at x = {xs:.3f})")
                col[3].legend(fontsize=7, loc="lower center")
        for name, sch, fix in RUNS[code]:
            d = load(name, at)
            if d is None:
                continue
            c, lab = FIX[fix]
            sname, ls, ms, mfc = SCH[sch]
            if code == "dyablo" and sch == "o2":
                sname = "RK2"
            if code == "RAMSES" and sch == "o2":
                sname = "MUSCL-Hancock"
            lab = f"{sname}, {lab}"
            kw = dict(color=c, ls=ls, lw=1.2, marker="o", ms=ms, mfc=mfc or c, mew=0.8, zorder=3, label=lab)
            for i, f in enumerate(("rho", "v", "T", "T")):
                col[i].plot(d["x"], d[f], **(kw if i == 0 else {**kw, "label": None}))
            col[5].plot(d["x"], d["lev"], **{**kw, "label": None})
            # unshocked gas: T / T_analytic
            xf = np.where(d["x"] < 0.5, d["x"], 1 - d["x"])
            Xr, _, _, Tar = analytic(d["a"], Ti[code])      # analytical solution at the run's own output time
            okr = ~np.isnan(Xr); half = okr.sum() // 2
            ta = np.interp(xf, Xr[okr][:half], Tar[okr][:half])
            pre = xf < xs - 0.006
            col[4].plot(d["x"], np.where(pre, d["T"] / ta, np.nan), **{**kw, "label": None})
            far = xf < 0.2
            near = pre & (xf > xs - 0.06)
            Tin = d["T"][np.abs(d["x"] - 0.5) < 0.1]
            summ.write(f"{zt} {code:6s} {lab:42s} a={d['a']:.4f}  T/T_an: far {np.median(d['T'][far] / ta[far]):.3g}"
                       f"  just before shock {np.median(d['T'][near] / ta[near]) if near.any() else np.nan:.3g}"
                       f"  T_max {Tin.max():.3e} K  T(mid-plane) {d['T'][np.argmin(np.abs(d['x'] - 0.5))]:.3e} K  rho_max {d['rho'].max():.1f}\n")
        yl = YL[zt]
        col[0].set(yscale="log", ylabel=r"$\rho/\bar\rho$", title=f"{code}, z = {1 / at - 1:.0f}", ylim=yl["rho"])
        col[1].set(ylabel="$v_x$ [km/s]", ylim=(-2300, 2300) if at > 0.5 else (-1400, 1400))
        col[2].set(yscale="log", ylabel="T/$\\mu$ [K]", ylim=yl["T"])
        col[3].set(yscale="log", ylabel="T/$\\mu$ [K] (zoom on the shocked region)", xlim=(0.4, 0.6) if at > 0.5 else (0.3, 0.7), ylim=yl["Tz"])
        col[4].set(yscale="log", ylabel="T / T$_{analytic}$, unshocked gas", ylim=(0.1, 3e4))
        col[5].set(ylabel="level (cells: 6 = 64$^3$)", xlabel="x / L$_{box}$", ylim=(5.8, 8.2))
        col[0].legend(fontsize=7, loc="upper left")
    fig.suptitle(f"EdS gas-only Zel'dovich pancake (Tep et al. App. B setup: 64 Mpc/h, z_c = 1, z_i = 50, 64$^3$ + 2 AMR levels), z = {1 / at - 1:.0f}\n"
                 "line style = scheme (solid: 2nd order space+time, dotted: dyablo Euler+slopes, dashed/open: 1st order); colour = fix; thick orange = analytical (valid outside the shocks)", fontsize=12)
    fig.savefig(f"{H}/eds_{zt}.png", dpi=80)
    print(zt, "done", flush=True)
summ.close()
print(open(f"{H}/eds_summary.txt").read())
