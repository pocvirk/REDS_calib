"""Adiabatic twin diagnostics (2026-11-17): DM + gas, no cooling/chemistry/RT/SF, same ICs in RAMSES and dyablo.
(1) halo temperature: gas-mass-weighted T/mu inside R200 over T200/mu = m_p G M200/(2 k R200) (catalogue M, R; the
    Barkana & Loeb T_vir formula is 1.48x higher here)
(2) halo baryon fraction: M_gas(<R200) / M_tot(<R200) / (Omega_b/Omega_m)
(3) T-delta phase diagram vs each code's own analytic adiabat T0(a) (1+delta)^(2/3), T0 from its a = 0.02 output
    scaled as a^-2 (no Compton): mass fractions below 0.8x (numerical cooling), within, and above 1.25x (shocks/heating)
(4) entropy profiles K = (T/mu) / n_H^(2/3) of the 5 most massive halos
Halos: RAMSES eps0.01 FoF catalogue at z = 9 (same ICs -> same halos); valid at a ~ 0.1 only.
usage: adiabatic.py AEXP LABEL=ramses:<dir>|dyablo:<dir> ... -> adiabatic_a<AEXP>.txt, figures/adiabatic_*_a<AEXP>.png"""
import sys, os, glob
import numpy as np, h5py
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
H = os.path.dirname(os.path.abspath(__file__))
TOOLS = "/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/analysis/dyablo_tools/dashboard_dyablo_reio"
sys.path.insert(0, TOOLS)
from dashboard_reio_dyablo import ramses_reader as rr
from dashboard_reio_dyablo.run import DyabloRun
R = "/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/runs"
MP, KB, MPC, MYR = 1.67262192e-27, 1.380649e-23, 3.0856775814913673e22, 3.15576e13
L, HUB, OMB = 5.9603633880615234, 0.6711, 0.049
AT = float(sys.argv[1])
specs = [a.split("=", 1) for a in sys.argv[2:]]
TAG = os.environ.get("ADI_TAG", "")   # output suffix (e.g. _fb for the negative-pressure fallback test)
RECENTRE = os.environ.get("ADI_RECENTRE", "1") == "1"   # per-run DM shrinking-sphere centres (default since 2026-11-17)


def info(path):
    return {l.split("=")[0].strip(): l.split("=")[1].strip() for l in open(path) if "=" in l}


def ramses(d, at):
    outs = [o for o in sorted(glob.glob(f"{d}/output_*")) if os.path.exists(f"{o}/info_{o[-5:]}.txt")]
    o = min(outs, key=lambda o: abs(float(info(f"{o}/info_{o[-5:]}.txt")["aexp"]) - at))
    inf = info(f"{o}/info_{o[-5:]}.txt"); a = float(inf["aexp"]); ud, ul, ut = (float(inf[k]) for k in ("unit_d", "unit_l", "unit_t"))
    c = rr.read_cells(o, rt=False)
    dxc = 0.5**c["level"].astype(float)
    g = dict(n=c["density"] * ud / (MP * 1e3), T=c["pressure"] / c["density"] * (ul / ut)**2 * MP * 1e3 / (KB * 1e7),
             m=c["density"] * dxc**3, pos=np.stack([c["x"], c["y"], c["z"]], 1) * L % L)
    p = rr.read_particles(o)
    dm = p["family"].astype(int) == 1
    return a, os.path.basename(o), g, np.stack([p["position_x"], p["position_y"], p["position_z"]], 1)[dm] * L % L, p["mass"][dm], float(inf["omega_m"])


def dyablo(d, at):
    run = DyabloRun(d)
    snaps = [(run.snapshot_aexp(g), g, pf) for _, g, pf in run.snapshots() if pf]
    a, gf, pf = min(snaps, key=lambda s: abs(s[0] - at))
    with h5py.File(gf) as h:
        rho, e = h["rho"][()], h["e_tot"][()]
        ek = 0.5 * (h["rho_vx"][()]**2 + h["rho_vy"][()]**2 + h["rho_vz"][()]**2) / rho
        lev = h["level"][()].astype(int)
    dx = run.lbox_mpc / (run.bx * 2.0**lev)
    g = dict(n=rho / a**3 / MP * 1e-6, T=(2 / 3) * (e - ek) / rho * (MPC / MYR)**2 / a**2 * MP / KB, m=rho * dx**3, pos=run.cell_centers(gf))
    with h5py.File(pf, "r") as f:       # adiabatic outputs have no birth_time: all particles are DM
        pos = (f["coordinates"][()] * run.l_unit / MPC) % run.lbox_mpc; m = f["mass"][()]
    return a, os.path.basename(gf), g, pos, m, run.om


def load(code, d, at):
    return (ramses if code == "ramses" else dyablo)(d, at)


def recentre(td, dpos, c0, r200, f=0.85, rmin=0.1, nmin=30):
    """Shrinking-sphere centre of the DM particles (Power et al. 2003), starting from the catalogue centre c0 with radius
    R200; each code's halo can sit slightly away from the RAMSES FoF position. td: periodic cKDTree of dpos."""
    c, r = np.array(c0, float), r200
    while r > rmin * r200:
        idx = td.query_ball_point(c, r)
        if len(idx) < nmin:
            break
        dr = (dpos[idx] - c + 0.5 * L) % L - 0.5 * L
        c = (c + dr.mean(0)) % L; r *= f
    return c


ref = np.loadtxt(f"{R}/ramses_box/eps0.01/dashboard/halos_iter0000012.txt")
Ph, Mh, Rh = ref[:, 1:4], ref[:, 4], ref[:, 5]
big = np.argsort(Mh)[::-1][:5]
sel = np.where(Mh >= 3e7)[0]
MB = np.array([3e7, 1e8, 3e8, 1e9, 1e10]); MC = np.sqrt(MB[1:] * MB[:-1])
KED = np.logspace(np.log10(0.05), np.log10(2), 11); KC = np.sqrt(KED[1:] * KED[:-1])
z = 1 / AT - 1
out = open(f"{H}/adiabatic_a{AT:.3f}{TAG}.txt", "w")
def say(s):
    print(s, flush=True); out.write(s + "\n")
say(f"# adiabatic twin, a = {AT}: same halos (RAMSES eps0.01 FoF z=9, {len(sel)} halos > 3e7 Msun)")
res = {}
for lab, spec in specs:
    code, d = spec.split(":", 1)
    a0, _, g0, *_ = load(code, d, 0.02)
    m0 = g0["m"]; dl0 = g0["n"] / (np.sum(g0["n"] * m0 / g0["n"]) / np.sum(m0 / g0["n"]))
    s0 = np.abs(dl0 - 1) < 0.05; T00 = np.median(g0["T"][s0])
    a, snap, g, dpos, dmass, om = load(code, d, AT)
    vol = g["m"] / g["n"]; nbar = g["m"].sum() / vol.sum(); delta = g["n"] / nbar
    Tad = T00 * (a0 / a)**2 * delta**(2 / 3)
    w = g["m"] / g["m"].sum(); q = g["T"] / Tad
    fb_lo, fb_ok, fb_hi = w[q < 0.8].sum(), w[(q >= 0.8) & (q <= 1.25)].sum(), w[q > 1.25].sum()
    vo = (delta < 1); fv_lo = w[vo & (q < 0.8)].sum() / w[vo].sum()
    say(f"\n{lab}: {snap} a = {a:.4f}; T0(a=0.02) = {T00:.1f} K -> adiabat at mean density {T00 * (a0 / a)**2:.2f} K")
    say(f"  gas mass vs own adiabat: below 0.8x {fb_lo:.4f} | 0.8-1.25x {fb_ok:.3f} | above 1.25x {fb_hi:.3f}; voids (delta<1) below 0.8x: {fv_lo:.4f}")
    # gas and DM masses come in different code units: rescale gas so that the box baryon fraction is Omega_b/Omega_m
    fc = OMB / om; scale = fc / (1 - fc) * dmass.sum() / g["m"].sum(); g["m"] = g["m"] * scale
    say(f"  gas-mass unit rescale {scale:.4g} (box baryon fraction set to Omega_b/Omega_m = {fc:.4f}); {len(dmass)} DM particles")
    tg = cKDTree(g["pos"], boxsize=L * (1 + 1e-9)); td = cKDTree(dpos, boxsize=L * (1 + 1e-9))
    beta, fbar = np.full(len(sel), np.nan), np.full(len(sel), np.nan)
    cen = Ph.copy()
    if RECENTRE:
        for i in sel:
            cen[i] = recentre(td, dpos, Ph[i], Rh[i])
    off = np.sqrt(((((cen - Ph) + 0.5 * L) % L - 0.5 * L)**2).sum(1)) / Rh
    if RECENTRE:
        say(f"  recentred on DM shrinking sphere: offset from RAMSES-FoF centre median {np.median(off[sel]):.2f} R200, 90th pct {np.percentile(off[sel], 90):.2f} R200")
    for k, i in enumerate(sel):
        ig = np.array(tg.query_ball_point(cen[i], Rh[i]), int); idm = np.array(td.query_ball_point(cen[i], Rh[i]), int)
        if len(ig) == 0:
            continue
        mg = g["m"][ig]; md = dmass[idm].sum() if len(idm) else 0.0
        tvir = MP * 6.674e-11 * Mh[i] * 1.989e30 / (2 * KB * Rh[i] * MPC * AT)   # T200/mu = m_p G M200 / (2 k R200), catalogue M, R
        beta[k] = np.sum(mg * g["T"][ig]) / mg.sum() / tvir
        fbar[k] = mg.sum() / (mg.sum() + md) / (OMB / om)
    prof = []
    for i in big:
        idx = np.array(tg.query_ball_point(cen[i], 2 * Rh[i]), int)
        dr = (g["pos"][idx] - cen[i] + 0.5 * L) % L - 0.5 * L; r = np.sqrt((dr**2).sum(1)) / Rh[i]
        K = g["T"][idx] / g["n"][idx]**(2 / 3); kb = np.digitize(r, KED) - 1
        prof.append([np.median(K[kb == j]) if np.any(kb == j) else np.nan for j in range(len(KC))])
    res[lab] = dict(code=code, beta=beta, fbar=fbar, prof=np.array(prof), delta=delta, T=g["T"], w=w, Tad0=T00 * (a0 / a)**2)
    for b in range(len(MC)):
        s = (Mh[sel] >= MB[b]) & (Mh[sel] < MB[b + 1])
        say(f"  M {MB[b]:.0e}-{MB[b + 1]:.0e} ({s.sum():4d} halos): T/T_vir median {np.nanmedian(beta[s]):.2f} "
            f"[{np.nanpercentile(beta[s], 16):.2f}-{np.nanpercentile(beta[s], 84):.2f}] | f_gas/(Ob/Om) median {np.nanmedian(fbar[s]):.2f}")
out.close()
# figures
C = {"ramses": "#2a6fdb"}; CD = ["#1aa39a", "#e8590c", "#7048e8", "#c2255c", "#495057"]
cols = {}; k = 0
for lab, r in res.items():
    if r["code"] == "ramses":
        cols[lab] = (C["ramses"], "--")
    else:
        cols[lab] = (CD[k], "-"); k += 1
fig, ax = plt.subplots(1, 3, figsize=(16, 4.6), constrained_layout=True)
for lab, r in res.items():
    c, ls = cols[lab]
    for j, (key, axx) in enumerate((("beta", ax[0]), ("fbar", ax[1]))):
        med = [np.nanmedian(r[key][(Mh[sel] >= MB[b]) & (Mh[sel] < MB[b + 1])]) for b in range(len(MC))]
        lo = [np.nanpercentile(r[key][(Mh[sel] >= MB[b]) & (Mh[sel] < MB[b + 1])], 16) for b in range(len(MC))]
        hi = [np.nanpercentile(r[key][(Mh[sel] >= MB[b]) & (Mh[sel] < MB[b + 1])], 84) for b in range(len(MC))]
        axx.plot(MC, med, ls, color=c, marker="o", lw=2, label=lab); axx.fill_between(MC, lo, hi, color=c, alpha=0.12)
    for p in r["prof"]:
        ax[2].plot(KC, p, ls, color=c, lw=1, alpha=0.8)
    ax[2].plot([], [], ls, color=c, label=lab)
ax[0].axhline(1, color="0.5", lw=1, ls=":"); ax[1].axhline(1, color="0.5", lw=1, ls=":")
ax[0].set(xscale="log", xlabel="halo mass [M$_\\odot$]", ylabel="T$_{gas}$(<R$_{200}$) / T$_{200}$ (mass-weighted)", title=f"halo temperature, z = {z:.0f}", ylim=(0, 2))
ax[1].set(xscale="log", xlabel="halo mass [M$_\\odot$]", ylabel="f$_{gas}$(<R$_{200}$) / ($\\Omega_b/\\Omega_m$)", title="halo baryon fraction", ylim=(0, 1.3))
ax[2].set(xscale="log", yscale="log", xlabel="r / R$_{200}$", ylabel="K = (T/$\\mu$) / n$_H^{2/3}$ [K cm$^2$]", title="entropy profiles, 5 most massive halos")
for x in ax:
    x.grid(alpha=0.25, lw=0.5); x.legend(fontsize=8, frameon=False)
ax[0].text(0.02, 0.03, "bands: 16-84th percentile", transform=ax[0].transAxes, fontsize=7, color="0.4")
os.makedirs(f"{H}/figures", exist_ok=True); fig.savefig(f"{H}/figures/adiabatic_halos_a{AT:.3f}{TAG}.png", dpi=110)
fig, ax = plt.subplots(1, len(res), figsize=(5.2 * len(res), 4.6), constrained_layout=True, squeeze=False)
xe, ye = np.linspace(-1.5, 3, 160), np.linspace(-2, 6, 200)
for axx, (lab, r) in zip(ax[0], res.items()):
    hh, _, _ = np.histogram2d(np.log10(r["delta"]), np.log10(np.maximum(r["T"], 1e-3)), bins=(xe, ye), weights=r["w"])
    axx.pcolormesh(xe, ye, np.log10(np.maximum(hh.T, 1e-9)), vmin=-7, vmax=-1, cmap="Greys", shading="auto")
    xx = np.linspace(-1.5, 3, 50)
    axx.plot(xx, np.log10(r["Tad0"]) + 2 / 3 * xx, color="#e8590c", lw=1.5, label="own adiabat T$_0$(a)(1+$\\delta$)$^{2/3}$")
    axx.plot(xx, np.log10(0.8 * r["Tad0"]) + 2 / 3 * xx, color="#e8590c", lw=0.8, ls=":", label="0.8x adiabat")
    axx.set(xlabel="log$_{10}$(1+$\\delta$)", ylabel="log$_{10}$ T/$\\mu$ [K]", title=lab)
    axx.legend(fontsize=7, frameon=False, loc="upper left")
fig.suptitle(f"adiabatic twin: gas mass in the temperature-density plane, z = {z:.0f} (grey scale: log mass fraction per pixel)", fontsize=10)
fig.savefig(f"{H}/figures/adiabatic_phase_a{AT:.3f}{TAG}.png", dpi=110)
print("ok")
