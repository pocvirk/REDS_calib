"""Negative-pressure fallback flavours on the idealised SN test (2026-11-17): runs/fbcomp setups (one SN, 1e51 erg, 10 Msun
ejecta, uniform medium, analytical primordial cooling, periodic, no gravity; units pc, Myr, Msun) rerun with the production
hydro (RK2, HydroIon policy, minmod, cfl 0.8) in three flavours:
  A floor   : p < 0 -> smallp (current dyablo)
  B adiabat : p < 0 -> p0 (rho/rho0)^gamma of the cell itself ([hydro] negative_p_fallback = adiabat)
  C pf0     : RAMSES pressure_fix with beta_fix = 0 (HydroUpdate_RK2_ion_pf, ramses mode)
The HydroIon policy needs rho_HII: uniform medium from the stromgren IC (non-cosmo: [stromgren] gas_density in code units,
[rad] temperature; p = rho k T / m_p, so T = 8197 K gives the fbcomp pressure 2.298 n) instead of blast."""
import re, glob, os
R = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(os.path.dirname(R), "fbcomp")
FLAV = {"A": ["update = HydroUpdate_RK2_ion"],
        "B": ["update = HydroUpdate_RK2_ion", "negative_p_fallback = adiabat"],
        "C": ["update = HydroUpdate_RK2_ion_pf", "dual_energy_mode = ramses", "beta_fix = 0.0"]}
for f in sorted(glob.glob(f"{SRC}/n*_*.ini")):
    base = os.path.basename(f)[:-4]
    s0 = open(f).read()
    n = float(re.search(r"density_in = ([0-9.e+-]+)", s0).group(1)) / 0.03252
    for fl, hyd in FLAV.items():
        run = f"{base}_{fl}"
        s = s0.replace("initial_conditions = blast,simple_particles", "initial_conditions = stromgren,simple_particles")
        s = re.sub(r"\[blast\]\n(?:[^\[]*\n)", f"[stromgren]\ngas_density = {0.03252 * n:g}\nxe_start = 1.2e-3\n[rad]\nupdate = none\ntemperature = 8197 K\n", s)
        s = s.replace("update = HydroUpdate_euler\n", "\n".join(hyd + ["slope_enabled = true", "slope_limiter = minmod"]) + "\n")
        s = s.replace("hydro_cfl = 0.5", "hydro_cfl = 0.8")
        s = s.replace(f"{SRC}/{base}", f"{R}/{run}").replace(f"outputprefix = {base}", f"outputprefix = {run}")
        s = s.replace("write_variables = rho,rho_vx,rho_vy,rho_vz,e_tot", "write_variables = rho,rho_vx,rho_vy,rho_vz,e_tot,rho_HII")
        s = f"# {run}: fallback flavour {fl} (see make_inis.py)\n" + s.split("\n", 1)[1]
        assert "stromgren" in s and "HydroUpdate_RK2_ion" in s and f"{R}/{run}" in s, run
        open(f"{R}/{run}.ini", "w").write(s); os.makedirs(f"{R}/{run}", exist_ok=True)
        print(run)
