"""Zel'dovich pancake ICs as in Tep, Aubert, Ocvirk & Marchal (Reionization powered by GPUs II, App. B):
Einstein-de Sitter, gas only (Omega_m = Omega_b = 1), H0 = 67 km/s/Mpc, L = 64 Mpc/h, z_c = 1, z_i = 50.
Exact Zel'dovich solution at z_i evaluated at the Eulerian cell centres (x -> q inverted), grafic format
(dyablo grafic_fields / RAMSES grafic; no DM files -> gas only).  usage: make_ic.py N [VY] -> ic_N/ (or ic_N_vyVY/: uniform transverse peculiar velocity VY km/s at z_i added to all gas,
Galilean-invariance test of the dual-energy switches; a uniform y velocity decays as 1/a, VY = 1e5 -> 2000 km/s at z = 0)"""
import sys, os
import numpy as np
from scipy.optimize import brentq
N = int(sys.argv[1]) if len(sys.argv) > 1 else 64
VY = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
H0, h = 67.0, 0.67
L = 64.0 / h                      # Mpc (comoving)
zc, zi = 1.0, 50.0
ai = 1 / (1 + zi)
k = 2 * np.pi / L
b = (1 + zc) / (1 + zi)           # D(a_i)/D(a_c) in EdS
dx = L / N
x = (np.arange(N) + 0.5) * dx
q = np.array([brentq(lambda qq: qq + b * np.sin(k * qq) / k - xx, xx - L / 2, xx + L / 2) for xx in x])
delta = 1 / (1 + b * np.cos(k * q)) - 1
vel = H0 * (1 + zc) / np.sqrt(1 + zi) * np.sin(k * q) / k        # proper peculiar km/s (Tep eq. B2)
def write(arr1, name, d):
    f = open(f"{d}/{name}", "wb")
    f.write(np.int32([44, N, N, N]).tobytes()); f.write(np.float32([dx, 0, 0, 0, ai, 1.0, 0.0, H0]).tobytes()); f.write(np.int32([44]).tobytes())
    plane = np.broadcast_to(arr1[None, :], (N, N)).astype(np.float32).ravel()
    for _ in range(N):
        f.write(np.int32([plane.size * 4]).tobytes()); f.write(plane.tobytes()); f.write(np.int32([plane.size * 4]).tobytes())
    f.close()
d = f"ic_{N}" + (f"_vy{VY:g}" if VY else ""); os.makedirs(d, exist_ok=True)
z0 = np.zeros(N)
for name, arr in [("ic_deltab", delta), ("ic_velbx", vel), ("ic_velby", z0 + VY), ("ic_velbz", z0)]:
    write(arr, name, d)
for c in "xyz":   # RAMSES init_time reads the grafic header from ic_velcx even without particles
    if not os.path.exists(f"{d}/ic_velc{c}"): os.symlink(f"ic_velb{c}", f"{d}/ic_velc{c}")
print(f"{d}: N={N}, L={L:.3f} Mpc, dx={dx*1e3:.1f} kpc, delta [{delta.min():.4f},{delta.max():.4f}], v max {vel.max():.2f} km/s")
