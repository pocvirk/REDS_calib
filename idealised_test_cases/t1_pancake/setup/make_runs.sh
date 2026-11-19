#!/bin/bash
# EdS gas-only pancake (Tep et al. App. B setup): 64^3 coarse, mass AMR (refine when cell mass > mean coarse-cell mass), z=50 -> 0.
# NB 2026-11-16: dyablo mass_coarsen_factor must satisfy 2^ndim * coarsen < refine (absolute cell masses), else the mesh flickers
# (refine at parent mass > 1 m0, coarsen children at parent mass < 8*0.9 m0) and each coarsening averages e_tot -> spurious heating.
# dyablo: level_min 4 (bx=4 -> 64 cells), level_max 6 (+2, = Tep) or 8 (+4 reference). RAMSES: levelmin 6, levelmax 8 / 10.
R=/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/runs/pancake_eds
dy() { # name slope lmax update extra...
  n=$1 s=$2 lm=$3 up=$4; shift 4
  mkdir -p $R/$n
  cat > $R/$n.ini <<EOT
# $(date +%F) EdS gas-only pancake (Tep et al. App. B): slopes=$s level 4..$lm update=$up $*
[ini]
convert_units = true
[amr]
bx = 4
by = 4
bz = 4
level_min = 4
level_max = $lm
markers_kernel = RefineCondition_mass
nboctspergroup = 1024
use_block_data = true
loadbalance_coherent_levels = 3
enable_load_balance_during_init = false
load_balancing_frequency = 1
[hydro]
gamma0 = 1.66666666666666666666
riemann = hllc
smallp = 1e-43
smallr = 1e-50
slope_enabled = $s
slope_limiter = minmod
update = $up
$(for kv in "$@"; do echo "$kv"; done)
[cosmology]
active = true
da = 1.01
mass_coarsen_factor = 0.1
mass_refine_factor = 1
lookup_size = 262144
omegab = 1.0
save_expansion_table = false
[dt]
dt_kernel = Compute_dt_cosmology,Compute_dt_hydro
dt = 1.0e-4
hydro_cfl = 0.8
[gravity]
solver = GravitySolver_multigrid
MG_eps = 1e-3
[particles]
update_position = none
update_density = none
[rad]
update = none
xe_start = 1.2e-3
c_rad = 0.01 speedoflight
[grafic]
inputDir = $R/ic_64/
[mesh]
boundary_type_xmax = periodic
boundary_type_xmin = periodic
boundary_type_ymax = periodic
boundary_type_ymin = periodic
boundary_type_zmax = periodic
boundary_type_zmin = periodic
ndim = 3
xmin = 0
ymin = 0
zmin = 0
xmax = 95.522388059701493
ymax = 95.522388059701493
zmax = 95.522388059701493
[run]
enable_output = true
initial_conditions = grafic_fields
nstepmax = 1000000
t_end_var = aexp
tEnd = 1.0
output_frequency = 100000000
output_slice_var = aexp
output_timeslice = 0.083333333333333
checkpoint_frequency = 100000000
enable_checkpoint = false
nlog = 50
[output]
backend = IOManager_hdf5
checkpoint = IOManager_checkpoint
output_real_type = double
outputdir = $R/$n
outputprefix = $n
write_mesh_info = yes
write_variables = rho,rho_vx,rho_vy,rho_vz,e_tot,level
[units]
time = 1 Myr
length = 1 Mpc
density = 1 kg / m3
particle_density = 1 atom/m3
EOT
}
ra() { # name slope_type lmax pressure_fix
  n=$1 st=$2 lm=$3 pf=$4
  mkdir -p $R/$n; ln -sfn $R/ic_64 $R/$n/ic
  cat > $R/$n/$n.nml <<EOT
! $(date +%F) EdS gas-only pancake (Tep et al. App. B): slope_type=$st levels 6..$lm pressure_fix=$pf (beta 0.5)
&RUN_PARAMS
cosmo=.true.
pic=.false.
poisson=.true.
hydro=.true.
rt=.false.
nrestart=0
nremap=10
nsubcycle=1,1,2,2,2,2
ncontrol=10
verbose=.false.
/
&AMR_PARAMS
levelmin=6
levelmax=$lm
ngridmax=200000
nexpand=1
/
&INIT_PARAMS
filetype='grafic'
initfile(1)='ic'
omega_b=1.0
/
&OUTPUT_PARAMS
aout=0.33333333, 0.5, 0.66666667, 0.75, 0.83333333
aend=1.0
walltime_hrs=-1.
/
&POISSON_PARAMS
epsilon=1d-4
/
&HYDRO_PARAMS
gamma=1.6666667
courant_factor=0.8
scheme='muscl'
riemann='hllc'
slope_type=$st
pressure_fix=$pf
beta_fix=0.5
/
&REFINE_PARAMS
m_refine=10*1.
interpol_var=1
interpol_type=0
/
&COOLING_PARAMS
cooling=.false.
metal=.false.
/
EOT
}
dy e_dy_o1      false 6 HydroUpdate_euler_ion
dy e_dy_o2      true  6 HydroUpdate_euler_ion
dy e_dy_o1_pf   false 6 HydroUpdate_euler_ion_pf "beta_fix = 0.5"
dy e_dy_o2_pf   true  6 HydroUpdate_euler_ion_pf "beta_fix = 0.5"
dy e_dy_o2_de   true  6 HydroUpdate_euler_ion_pf "dual_energy_mode = ratio" "dual_energy_eta = 1e-3"
dy e_dy_o2_ref  true  8 HydroUpdate_euler_ion
ra e_ra_o1      0 8  .false.
ra e_ra_o2      1 8  .false.
ra e_ra_o1_pf   0 8  .true.
ra e_ra_o2_pf   1 8  .true.
ra e_ra_o2_ref  1 10 .false.
# entropy dual energy (Tep et al. eq. A.1), build_ent
dy e_dy_o2_ent  true  6 HydroUpdate_euler_ion_pf "dual_energy_mode = entropy" "dual_energy_eta = 0.1"
dy e_dy_o1_ent  false 6 HydroUpdate_euler_ion_pf "dual_energy_mode = entropy" "dual_energy_eta = 0.1"
dy e_dy_o2_ent_ref true 8 HydroUpdate_euler_ion_pf "dual_energy_mode = entropy" "dual_energy_eta = 0.1"
# proper 2nd order in time: SSP-RK2 + minmod (HydroUpdate_RK2_ion[_pf]); CPU build_cpu (login node) or build_ent
dy e_dy_rk2      true 6 HydroUpdate_RK2_ion
dy e_dy_rk2_ent  true 6 HydroUpdate_RK2_ion_pf "dual_energy_mode = entropy" "dual_energy_eta = 0.1"
dy e_dy_rk2_pf   true 6 HydroUpdate_RK2_ion_pf "beta_fix = 0.5"
dy e_dy_rk2_ref     true 8 HydroUpdate_RK2_ion
dy e_dy_rk2_ent_ref true 8 HydroUpdate_RK2_ion_pf "dual_energy_mode = entropy" "dual_energy_eta = 0.1"
