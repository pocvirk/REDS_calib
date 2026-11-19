"""Negative-pressure fallback flavours on the adiabatic twin (2026-11-17): gas density and temperature profiles, and maps,
for a small, a medium and a massive halo at z = 9 (RAMSES eps0.01 FoF catalogue, same ICs in every run).
Profiles: volume-weighted gas density (1+delta) and mass-weighted T/mu in spherical shells vs r/R200.
Centres: each run's own DM shrinking-sphere centre (recentre(), adiabatic.py), starting at the RAMSES FoF position.
Maps: projection through a slab of thickness 2 R200 centred on the halo, sampled on a regular grid (nearest cell centre):
mean gas overdensity, and density-weighted T/mu. Circle: R200.
usage: halo_fix_maps.py [AEXP] -> figures/fix_profiles_a<AEXP>.png, figures/fix_maps_<halo>_a<AEXP>.png, fix_profiles_a<AEXP>.txt"""
import sys, os
import numpy as np
from scipy.spatial import cKDTree
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
H = os.path.dirname(os.path.abspath(__file__))
AT = float(sys.argv[1]) if len(sys.argv) > 1 else 0.1
_argv = sys.argv; sys.argv = [_argv[0], str(AT)]
src = open(f"{H}/adiabatic.py").read()
exec(src[: src.index("ref = np.loadtxt")])          # constants, ramses(), dyablo(), load(), recentre()
sys.argv = _argv
RV = f"{R}/reio_v2"
RUNS = [  # label, code, dir, colour, linestyle, in maps
    ("RAMSES (pf beta 0)", "ramses", f"{R}/ramses_box/adi_s1", "#2a6fdb", "--", True),
    ("dyablo A: floor (adi_rk2)", "dyablo", f"{RV}/adi_rk2", "#1aa39a", "-", True),
    ("dyablo A': floor rerun (noise)", "dyablo", f"{RV}/adi_fb_floor", "#1aa39a", ":", False),
    ("dyablo B: adiabat fallback", "dyablo", f"{RV}/adi_fb_adiabat", "#7048e8", "-", True),
    ("dyablo C: RAMSES-like pf beta 0", "dyablo", f"{RV}/adi_fb_pf0", "#c2255c", "-", True),
    ("dyablo + entropy (Tep)", "dyablo", f"{RV}/adi_rk2_ent", "#e8590c", "-", True),
]
ref = np.loadtxt(f"{R}/ramses_box/eps0.01/dashboard/halos_iter0000012.txt")
Ph, Mh, Rh = ref[:, 1:4], ref[:, 4], ref[:, 5]
HALOS = {}
for name, target in (("small", 5.5e7), ("medium", 5.5e8)):
    HALOS[name] = int(np.argmin(np.abs(np.log(Mh / target))))
HALOS["massive"] = int(np.argmax(Mh))
REDGE = np.logspace(np.log10(0.05), np.log10(3.0), 13); RC = np.sqrt(REDGE[1:] * REDGE[:-1])
NPIX, NZ, EXT = 120, 24, 3.0        # pixels, samples through the slab, half-width in R200

prof, maps, used, offs = {}, {}, [], {}
for lab, code, d, c, ls, inmap in RUNS:
    try:
        a, snap, g, dpos, dmass, _ = load(code, d, AT)
    except Exception as e:          # run missing / not finished
        print(f"skip {lab}: {e}", flush=True); continue
    used.append((lab, c, ls, inmap))
    vol = g["m"] / g["n"]; nbar = g["m"].sum() / vol.sum()
    tree = cKDTree(g["pos"], boxsize=L * (1 + 1e-9)); td = cKDTree(dpos, boxsize=L * (1 + 1e-9))
    print(f"{lab}: {snap} a = {a:.4f}", flush=True)
    for hn, i in HALOS.items():
        r200 = Rh[i]
        c = recentre(td, dpos, Ph[i], r200)          # this run's own DM shrinking-sphere centre
        offs[(lab, hn)] = (((c - Ph[i]) + 0.5 * L) % L - 0.5 * L) / r200
        idx = np.array(tree.query_ball_point(c, REDGE[-1] * r200), int)
        dr = (g["pos"][idx] - c + 0.5 * L) % L - 0.5 * L; r = np.sqrt((dr**2).sum(1)) / r200
        b = np.digitize(r, REDGE) - 1; ok = (b >= 0) & (b < len(RC))
        rho, T = np.full(len(RC), np.nan), np.full(len(RC), np.nan)
        for j in range(len(RC)):
            s = idx[ok & (b == j)]
            if len(s):
                rho[j] = g["m"][s].sum() / vol[s].sum() / nbar; T[j] = np.sum(g["m"][s] * g["T"][s]) / g["m"][s].sum()
        prof[(lab, hn)] = (rho, T)
        if inmap:
            u = np.linspace(-EXT, EXT, NPIX) * r200; w = np.linspace(-1, 1, NZ) * r200
            X, Y, Z = np.meshgrid(u, u, w, indexing="ij")
            pts = (np.stack([X, Y, Z], -1).reshape(-1, 3) + c) % L
            _, k = tree.query(pts)
            n = g["n"][k].reshape(NPIX, NPIX, NZ)
            maps[(lab, hn)] = ((n / nbar).mean(2), (n * g["T"][k].reshape(NPIX, NPIX, NZ)).sum(2) / n.sum(2))
    del g, tree, vol, td, dpos, dmass

tag = f"a{AT:.3f}"
with open(f"{H}/fix_profiles_{tag}.txt", "w") as f:
    f.write(f"# gas profiles at a = {AT}: r/R200 bin centres, then per run 1+delta (volume-weighted) and T/mu [K] (mass-weighted)\n")
    for hn, i in HALOS.items():
        f.write(f"\n# {hn} halo: M200 = {Mh[i]:.3g} Msun, R200 = {Rh[i] * 1e3:.1f} ckpc (max-level cell {L / 4096 * 1e3:.1f} ckpc)\n")
        f.write("r/R200      " + " ".join(f"{x:8.3f}" for x in RC) + "\n")
        f.write("# centre offset of each run (DM shrinking sphere) from the RAMSES FoF centre, in R200 (dx, dy, dz): "
                + "; ".join(f"{lab[:14]} ({o[0]:+.2f},{o[1]:+.2f},{o[2]:+.2f})" for (lab, h), o in offs.items() if h == hn) + "\n")
        for lab, *_ in used:
            rho, T = prof[(lab, hn)]
            f.write(f"{lab[:30]:30s} rho " + " ".join(f"{x:8.3g}" for x in rho) + "\n")
            f.write(f"{lab[:30]:30s} T   " + " ".join(f"{x:8.3g}" for x in T) + "\n")

# profiles: rows rho, T; columns small/medium/massive
fig, ax = plt.subplots(2, 3, figsize=(15, 8), sharex=True, constrained_layout=True)
for j, (hn, i) in enumerate(HALOS.items()):
    tvir = MP * 6.674e-11 * Mh[i] * 1.989e30 / (2 * KB * Rh[i] * MPC * AT)
    for lab, c, ls, _ in used:
        rho, T = prof[(lab, hn)]
        ax[0, j].plot(RC, rho, ls, color=c, marker="o", ms=3, lw=1.6, label=lab)
        ax[1, j].plot(RC, T, ls, color=c, marker="o", ms=3, lw=1.6)
    ax[1, j].axhline(tvir, color="0.4", lw=1, ls=":"); ax[1, j].text(0.06, tvir * 1.15, "T$_{200}$", fontsize=8, color="0.3")
    dxr = L / 4096 / Rh[i]
    for k in (0, 1):
        ax[k, j].axvline(1, color="0.7", lw=0.8); ax[k, j].axvspan(0.05, dxr, color="0.9", zorder=0)
        ax[k, j].set(xscale="log", yscale="log"); ax[k, j].grid(alpha=0.25, lw=0.5)
    ax[0, j].set_title(f"{hn} halo: M$_{{200}}$ = {Mh[i]:.2g} M$_\\odot$, R$_{{200}}$ = {Rh[i] * 1e3:.0f} ckpc")
    ax[1, j].set_xlabel("r / R$_{200}$")
ax[0, 0].set_ylabel("gas 1+$\\delta$ (shell, volume-weighted)"); ax[1, 0].set_ylabel("T/$\\mu$ [K] (shell, mass-weighted)")
ax[0, 0].legend(fontsize=7.5, loc="lower left")
fig.suptitle(f"Adiabatic twin, z = {1 / AT - 1:.0f}: negative-pressure fallback flavours (grey band: inside one max-level cell)", fontsize=10)
fig.savefig(f"{H}/figures/fix_profiles_{tag}.png", dpi=100)

# maps: one figure per halo; rows density / T, columns runs
mlabs = [(lab, c) for lab, c, ls, inmap in used if inmap]
for hn, i in HALOS.items():
    fig, ax = plt.subplots(2, len(mlabs), figsize=(3.3 * len(mlabs), 6.6), constrained_layout=True, squeeze=False)
    dmaps = [maps[(lab, hn)][0] for lab, _ in mlabs]; tmaps = [maps[(lab, hn)][1] for lab, _ in mlabs]
    dn = LogNorm(*np.nanpercentile(np.concatenate([m.ravel() for m in dmaps]), [1, 99.8]))
    tn = LogNorm(*np.nanpercentile(np.concatenate([m.ravel() for m in tmaps]), [1, 99.8]))
    for j, (lab, c) in enumerate(mlabs):
        for k, (m, nrm, cm) in enumerate(((dmaps[j], dn, "viridis"), (tmaps[j], tn, "inferno"))):
            im = ax[k, j].imshow(m.T, origin="lower", extent=(-EXT, EXT, -EXT, EXT), norm=nrm, cmap=cm, interpolation="nearest")
            ax[k, j].add_patch(plt.Circle((0, 0), 1, fill=False, color="w", lw=0.8, ls="--"))
            ax[k, j].set(xticks=[-2, 0, 2], yticks=[-2, 0, 2])
        ax[0, j].set_title(lab, fontsize=8.5, color=c)
    fig.colorbar(ax[0, -1].images[0], ax=ax[0, :], shrink=0.85, label="gas 1+$\\delta$ (slab mean)")
    fig.colorbar(ax[1, -1].images[0], ax=ax[1, :], shrink=0.85, label="T/$\\mu$ [K] (density-weighted)")
    ax[1, 0].set_xlabel("x / R$_{200}$"); ax[1, 0].set_ylabel("y / R$_{200}$")
    fig.suptitle(f"{hn} halo, z = {1 / AT - 1:.0f}: M$_{{200}}$ = {Mh[i]:.2g} M$_\\odot$, R$_{{200}}$ = {Rh[i] * 1e3:.0f} ckpc "
                 f"(max-level cell = {L / 4096 / Rh[i]:.2f} R$_{{200}}$); slab 2 R$_{{200}}$ thick", fontsize=10)
    fig.savefig(f"{H}/figures/fix_maps_{hn}_{tag}.png", dpi=100)
print(open(f"{H}/fix_profiles_{tag}.txt").read())
