"""z = 7 idealised discs (ICs/make_dice.py), 1e9 and 1e10 Msun haloes, reio resolution (dx_min = 195 pc), REDS physics.
Calibration path (PO 2026-11-13): which SF/FB recipe gives fesc(R200) ~ 50 % at 1e9 and 2-5 % at 1e10 (CoDa)?
Recipes: the four reio_v2 recipes + stronger-SN / denser-SF variants. Template = runs/disc/sfscan/sf_e0.3_n10_t3.ini
(mech FB, mass_star 1e4). Changes: ICs, box (25 kpc / 50 kpc, levels 3-5 / 4-6), IGM at the z = 7 mean baryon density
3e-6 Msun/pc^3 and 1e4 K, mass_refine scaled with the DM particle mass, tEnd 300 Myr, RT fluxes written (fesc).
usage: make_inis.py [1|2]  (scan 1 default, scan 2 = SN energy x t_SNII, + 3e9 halo) -> writes z7_<halo>_<recipe>.ini"""
import re
T = open("/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/runs/disc/sfscan/sf_e0.3_n10_t3.ini").read()
D = "/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/runs/disc_z7"
HALO = {"1e9": dict(L=25000, lmin=3, lmax=5, mref=2e4), "3e9": dict(L=25000, lmin=3, lmax=5, mref=6e4), "1e10": dict(L=50000, lmin=4, lmax=6, mref=2e5)}
#        name           FB      eps   n_th  t_SNII M_SNII   note
REC = [("th_e0.03_n0.1",  "th",   0.03, 0.1, 10, 10, "reio eps0.03"),
       ("mech_e0.03_n0.1", "mech", 0.03, 0.1, 10, 10, "reio eps0.03_mech"),
       ("mx2_e0.03_n0.1",  "mech", 0.03, 0.1, 10, 5,  "reio eps0.03_mech_snx2"),
       ("mech_e0.3_n10",   "mech", 0.3,  10,  3,  10, "reio eps0.3_mech_n10"),
       ("mx2_e0.3_n10",    "mech", 0.3,  10,  3,  5,  "2x SN"),
       ("mech_e0.1_n1",    "mech", 0.1,  1,   3,  10, ""),
       ("mx2_e0.1_n1",     "mech", 0.1,  1,   3,  5,  "2x SN"),
       ("mech_e0.3_n1",    "mech", 0.3,  1,   3,  10, "")]
# scan 2 (2026-11-13): mech, eps 0.03, n_th 0.1; SN energy boost via M_SNII (E per SN x b == M_SNII / b exactly in dyablo:
# only E_SNII/M_SNII enters), b = 1, 2, 4, 10, with t_SNII 10 and 3 Myr; eps 0.01 and 0.1 at b = 2, t_SNII 3
REC2 = [(f"mE{b}_e0.03_n0.1_t{t}", "mech", 0.03, 0.1, t, 10 / b, f"E x{b}") for t in (10, 3) for b in (1, 2, 4, 10)] + \
       [("mE2_e0.01_n0.1_t3", "mech", 0.01, 0.1, 3, 5, "E x2"), ("mE2_e0.1_n0.1_t3", "mech", 0.1, 0.1, 3, 5, "E x2")]
import sys
SCAN = sys.argv[1] if len(sys.argv) > 1 else "1"
if SCAN == "2":
    REC = REC2
FB = {"th": "ParticleUpdate_feedback", "mech": "ParticleUpdate_feedback_mechanical"}
def sub(pat, rep, s):
    s2, n = re.subn(pat, rep, s, flags=re.M); assert n == 1, pat; return s2
runs = []
for h, p in HALO.items():
    if SCAN == "1" and h == "3e9":
        continue
    for name, fb, eps, nth, tsn, msn, note in REC:
        run = f"z7_{h}_{name}"; runs.append(run)
        s = re.sub(r"^#.*\n", "", T, flags=re.M)
        s = f"# {run}: z = 7 disc, M200 = {h} Msun, {fb} FB, eps {eps}, n_th {nth} H/cc, t_SNII {tsn} Myr, M_SNII {msn} Msun ({note}) -- make_inis.py\n" + s
        s = sub(r"^tEnd = .*", "tEnd = 300", s)
        s = sub(r"^file = .*", f"file = {D}/ICs/z7_{h}.h5", s)
        s = sub(r"^IG_density = .*", "IG_density = 3e-6 solar_mass/pc**3", s)
        s = sub(r"^IG_T2 = .*", "IG_T2 = 1e4 K", s)
        s = sub(r"^level_min = .*", f"level_min = {p['lmin']}", s)
        s = sub(r"^level_max = .*", f"level_max = {p['lmax']}", s)
        s = sub(r"^mass_refine = .*", f"mass_refine = {p['mref']:g}", s)
        s = sub(r"^mass_coarsen = .*", f"mass_coarsen = {p['mref'] / 9:g}", s)
        for a in "xyz":
            s = sub(rf"^{a}max = .*", f"{a}max = {p['L']}", s)
        s = sub(r"^source_term = .*", f"source_term = ParticleUpdate_NGP_src_bpass,{FB[fb]}", s)
        s = sub(r"^density_threshold = .*", f"density_threshold = {nth:g} proton_mass/cm**3", s)
        s = sub(r"^epsilon_star = .*", f"epsilon_star = {eps:g}", s)
        s = sub(r"^M_SNII = .*", f"M_SNII = {msn:g} solar_mass", s)
        s = sub(r"^t_SNII = .*", f"t_SNII = {tsn} Myr", s)
        s = sub(r"^outputdir = .*", f"outputdir = {D}/{run}", s)
        s = sub(r"^outputprefix = .*", f"outputprefix = {run}", s)
        s = sub(r"^write_variables = .*", "write_variables = rho,rho_HII,rho_vx,rho_vy,rho_vz,e_tot,e_rad,fx_rad,fy_rad,fz_rad,src_ndot,level", s)
        open(f"{D}/{run}.ini", "w").write(s)
print(" ".join(runs))
