"""t_SNII 3 vs 10 Myr in the z = 7 disc scan 2 (mech FB, eps 0.03, n_th 0.1, SN energy boost b = 1,2,4,10 via M_SNII = 10/b):
stellar mass formed in 300 Myr, photon-weighted fesc(R200) (M1 flux, t >= 50 Myr; ray-traced HEALPix) vs b, per halo.
Reads analyse_z7_scan2.log and raytrace_z7_scan2.log -> z7_tsn.png (2026-11-18)"""
import re, numpy as np, matplotlib; matplotlib.use("agg"); import matplotlib.pyplot as plt
A, RT = {}, {}
for l in open("analyse_z7_scan2.log"):
    m = re.match(r"(z7_\S+)\s+300\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)", l)
    if m: A[m.group(1)] = [float(x) for x in m.groups()[1:]]
for l in open("raytrace_z7_scan2.log"):
    m = re.match(r"(z7_\S+)\s+photon-weighted fesc_RT\(R200\) = (\S+)", l)
    if m: RT[m.group(1)] = float(m.group(2))
B = [1, 2, 4, 10]; COL = {10: "#c2255c", 3: "#1c7ed6"}
fig, ax = plt.subplots(2, 3, figsize=(13, 7), constrained_layout=True, sharex=True)
for j, h in enumerate(["1e9", "3e9", "1e10"]):
    for t in (10, 3):
        rs = [f"z7_{h}_mE{b}_e0.03_n0.1_t{t}" for b in B]
        ax[0, j].loglog(B, [A[r][0] for r in rs], "-o", color=COL[t], lw=2, ms=6, label=f"t_SNII = {t} Myr")
        ax[1, j].loglog(B, [min(A[r][3], 1.0) for r in rs], "-o", color=COL[t], lw=2, ms=6, label=f"t_SNII = {t} Myr, M1 flux")
        ax[1, j].loglog(B, [RT[r] for r in rs], "--s", color=COL[t], lw=1.2, ms=5, label=f"t_SNII = {t} Myr, ray-traced")
        q = [r for r in rs if A[r][1] == 0]
        ax[0, j].plot([B[rs.index(r)] for r in q], [A[r][0] for r in q], "x", color="k", ms=10, mew=2)
    ax[0, j].set_title(f"z = 7 disc, M$_{{200}}$ = {h} M$_\\odot$")
    ax[1, j].set_xlabel("SN energy boost b (E per M$_\\star$ x b)"); ax[1, j].set_xticks(B, [str(b) for b in B])
    for a in ax[:, j]: a.grid(alpha=0.3, which="both")
ax[0, 0].set_ylabel("stellar mass formed in 300 Myr [M$_\\odot$]"); ax[1, 0].set_ylabel("photon-weighted f$_{esc}$(R$_{200}$)  (M1 capped at 1)")
ax[0, 0].legend(fontsize=8); ax[1, 0].legend(fontsize=7.5)
fig.suptitle("Isolated z = 7 discs, 195 pc, mech FB, eps 0.03, n$_{th}$ 0.1 (1st-order hydro): t$_{SNII}$ 3 vs 10 Myr.  x = SF quenched by 300 Myr", fontsize=10)
fig.savefig("z7_tsn.png", dpi=110)
