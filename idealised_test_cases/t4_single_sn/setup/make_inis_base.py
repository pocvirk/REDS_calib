"""thermal vs mechanical SN feedback, one SN (10 Msun ejecta, 1e51 erg) in a uniform medium with cooling
(analytical primordial table, settings/cooling), no gravity. Units pc, Myr, Msun."""
setups = {  # name: (n_H, box pc, level)  -> dx = box / (4 2^level)
    "n1_dx2":    (1,   128,  4),
    "n1_dx12":   (1,   800,  4),
    "n1_dx50":   (1,   1600, 3),
    "n100_dx0.3": (100, 40,  5),
    "n100_dx50": (100, 1600, 3),
}
R = "/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/runs/fbcomp"
for name, (n, L, lev) in setups.items():
    rho, p = 0.03252 * n, 2.298 * n                     # n_H = n, T ~ 1e4 K (mu = 1.22)
    dx = L / (4 * 2**lev)
    for fb, kernel in [("th", "ParticleUpdate_feedback"), ("mech", "ParticleUpdate_feedback_mechanical")]:
        run = f"{name}_{fb}"
        open(f"{R}/{run}.ini", "w").write(f"""# {run}: n_H = {n}, dx = {dx:g} pc, {kernel}, analytical cooling
[units]
time = 1 Myr
length = 1 pc
mass = 1 solar_mass
[run]
initial_conditions = blast,simple_particles
tEnd = 1.0
nstepmax = 200000
output_timeslice = 0.025
[dt]
hydro_cfl = 0.5
dt_kernel = Compute_dt_hydro,Compute_dt_max
dt_max = 0.005
[amr]
level_min = {lev}
level_max = {lev}
markers_kernel = RefineCondition_pseudo_gradient
bx = 4
by = 4
bz = 4
load_balancing_frequency = 1000
[mesh]
ndim = 3
xmin = 0
xmax = {L}
ymin = 0
ymax = {L}
zmin = 0
zmax = {L}
boundary_type_xmin = periodic
boundary_type_xmax = periodic
boundary_type_ymin = periodic
boundary_type_ymax = periodic
boundary_type_zmin = periodic
boundary_type_zmax = periodic
[hydro]
gamma0 = 1.6666666666666667
riemann = hllc
update = HydroUpdate_euler
smallr = 1e-20
smallp = 1e-20
[source_terms]
updates = SourceUpdate_cooling_grackle_table_hydro
[cooling]
grackle_table = {R}/analytical_cooling_table.h5
[blast]
density_in = {rho:g}
density_out = {rho:g}
pressure_in = {p:g}
pressure_out = {p:g}
[simple_particles]
npart = 1
px = {L/2 + 0.13*dx:g}
py = {L/2 + 0.21*dx:g}
pz = {L/2 + 0.07*dx:g}
attributes = vx,vy,vz,mass,birth_time
vx = 0
vy = 0
vz = 0
mass = 50
birth_time = 0
[particles]
update_position = none
source_term = {kernel}
[star_feedback]
eta_SNII = 0.2
M_SNII = 10 solar_mass
E_SNII = 1e51 erg
t_SNII = 1e-6 Myr
[output]
outputdir = {R}/{run}
outputprefix = {run}
write_variables = rho,rho_vx,rho_vy,rho_vz,e_tot
""")
        print(run, dx)
