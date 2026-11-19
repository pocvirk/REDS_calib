"""thermal vs mechanical SN feedback with cooling: radial momentum, kinetic / thermal energy vs time, and mid-plane
slices. Units pc, Myr, Msun. Momentum measured radially from the host-cell centre."""
import glob, re, sys, h5py, numpy as np
import matplotlib; matplotlib.use("agg"); import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
PCMYR = 3.085678e13 / 3.1536e13                 # pc/Myr in km/s (dyablo yr = 8760 h)
ERG = 1.9884e33 * 1e10 * PCMYR**2               # Msun (pc/Myr)^2 in erg
TK = 0.6 * 1.6726e-24 / 1.380649e-16 * 1e10 * PCMYR**2   # (pc/Myr)^2 -> K at mu = 0.6
G = 5 / 3
setups = {"n1_dx2": (1, 2), "n1_dx12": (1, 12.5), "n1_dx50": (1, 50), "n100_dx0.3": (100, 0.3125), "n100_dx50": (100, 50)}

def ini(run, key):
    return float([l.split("=")[1] for l in open(f"{run}.ini") if l.startswith(key)][0])

def load(f, keys=("rho", "rho_vx", "rho_vy", "rho_vz", "e_tot")):
    with h5py.File(f) as h:
        c = h["coordinates"][:][h["connectivity"][:]].mean(axis=1)
        return c, {k: h[k][:].astype(float) for k in keys}

def snaps(run):
    fs = sorted(glob.glob(f"{run}/{run}_iter*.h5"))
    ts = [float(re.search(r'Time TimeType="Single" Value="([^"]+)"', open(f[:-3] + ".xmf").read()).group(1)) for f in fs]
    return fs, np.array(ts)

def host_centre(run, dx):
    return (np.floor(np.array([ini(run, k) for k in ("px", "py", "pz")]) / dx) + 0.5) * dx

def history(run, dx):
    L = ini(run, "xmax"); hc = host_centre(run, dx); V = dx**3
    fs, ts = snaps(run)
    out = []
    for f in fs:
        c, d = load(f)
        dr = (c - hc + L / 2) % L - L / 2; r = np.linalg.norm(dr, axis=1)
        p = np.stack([d["rho_vx"], d["rho_vy"], d["rho_vz"]], 1)
        prad = (np.sum(p * dr, 1) / np.maximum(r, 1e-30)).sum() * V * PCMYR
        ek = 0.5 * np.sum(p**2, 1) / d["rho"]
        eth = d["e_tot"] - ek
        out.append((prad, ek.sum() * V * ERG, eth.sum() * V * ERG))
    out = np.array(out)
    out[:, 2] -= out[0, 2]                      # thermal energy relative to the initial ambient
    return ts, out

def slice_(run, dx, t):
    L = ini(run, "xmax"); hc = host_centre(run, dx)
    fs, ts = snaps(run); f = fs[np.argmin(abs(ts - t))]
    c, d = load(f, ("rho", "rho_vx", "rho_vy", "rho_vz", "e_tot"))
    s = np.abs(c[:, 2] - hc[2]) < dx / 2
    n = int(round(L / dx)); i = (c[s, 0] / dx).astype(int); j = (c[s, 1] / dx).astype(int)
    rho = np.zeros((n, n)); T = np.zeros((n, n))
    ek = 0.5 * (d["rho_vx"]**2 + d["rho_vy"]**2 + d["rho_vz"]**2) / d["rho"]
    rho[j, i] = d["rho"][s]; T[j, i] = ((G - 1) * (d["e_tot"] - ek) / d["rho"] * TK)[s]
    return rho / 0.03252 / 1.0, T, ts[np.argmin(abs(ts - t))], L   # rho in n_H [cm^-3] (rho_ref 0.03252 = n_H 1)

if __name__ == "__main__":
    H = {}
    for name, (n, dx) in setups.items():
        for fb in ("th", "mech"):
            try:
                H[name, fb] = history(f"{name}_{fb}", dx)
            except Exception as e:
                print(name, fb, "skipped:", e)
    np.save("histories.npy", {f"{k[0]}_{k[1]}": v for k, v in H.items()}, allow_pickle=True)
    # 1. radial momentum, kinetic, thermal energy vs time
    fig, ax = plt.subplots(2, 3, figsize=(15, 8.5), constrained_layout=True)
    for row, n in enumerate((1, 100)):
        names = [k for k, v in setups.items() if v[0] == n]
        for name, col in zip(names, ["k", "C0", "C3"]):
            for fb, ls in (("th", "--"), ("mech", "-")):
                if (name, fb) not in H: continue
                ts, o = H[name, fb]
                lab = f"dx={setups[name][1]:g} pc, {'thermal' if fb == 'th' else 'mechanical'}"
                for k in range(3):
                    ax[row, k].plot(ts, np.abs(o[:, k]) if k else o[:, k], ls, color=col, label=lab)
        psnow = 3e5 * n**(-2 / 17) * 0.01**(-0.14)     # Kimm+15 terminal momentum, Z' = 0.01
        ax[row, 0].axhline(psnow, color="0.5", lw=1, ls=":", label="Kimm+15 p_snow (Z'=0.01)")
        for k, yl in enumerate(["radial momentum [Msun km/s]", "kinetic energy [erg]", "|thermal energy - ambient| [erg]"]):
            a = ax[row, k]; a.set_yscale("log"); a.set_xlabel("t [Myr]"); a.set_ylabel(yl)
            a.set_title(f"n_H = {n} cm$^{{-3}}$"); a.grid(alpha=0.3, which="both")
        ax[row, 0].set_ylim(1e3, 3e6); ax[row, 1].set_ylim(1e46, 2e51); ax[row, 2].set_ylim(1e46, 2e51)
        ax[row, 0].legend(fontsize=7)
    fig.suptitle("one SN (1e51 erg, 10 Msun ejecta), uniform medium, analytical primordial cooling: thermal (dashed) vs mechanical (solid)")
    plt.savefig("fbcomp_history.png", dpi=110)
    # 2. slices at t = 0.1 and 1 Myr, dx = 12.5 pc and 50 pc at n=1, 50 pc at n=100
    cases = [("n1_dx2", 0.3), ("n1_dx12", 1.0), ("n1_dx50", 1.0), ("n100_dx50", 1.0)]
    fig, ax = plt.subplots(4, 4, figsize=(16, 15), constrained_layout=True)
    for i, (name, t) in enumerate(cases):
        for j, fb in enumerate(("th", "mech")):
            try:
                rho, T, tt, L = slice_(f"{name}_{fb}", setups[name][1], t)
            except Exception as e:
                print(e); continue
            n0 = setups[name][0]
            im = ax[i, 2 * j].imshow(rho, origin="lower", extent=[0, L, 0, L], norm=LogNorm(n0 / 30, n0 * 10), cmap="viridis")
            plt.colorbar(im, ax=ax[i, 2 * j], label="n_H [cm$^{-3}$]")
            im = ax[i, 2 * j + 1].imshow(T, origin="lower", extent=[0, L, 0, L], norm=LogNorm(5e3, 1e8), cmap="inferno")
            plt.colorbar(im, ax=ax[i, 2 * j + 1], label="T [K]")
            for a in ax[i, 2 * j:2 * j + 2]:
                a.set_title(f"{name} {'thermal' if fb == 'th' else 'mechanical'}, t={tt:.2f} Myr", fontsize=9)
    plt.savefig("fbcomp_slices.png", dpi=90)
