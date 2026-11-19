#!/bin/bash
#SBATCH -A AST031
#SBATCH -J eds_ladder
#SBATCH -o /lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/runs/pancake_eds/%x-%j.out
#SBATCH -t 01:30:00
#SBATCH -q debug
#SBATCH -p batch
#SBATCH -N 1
# Galilean test with realistic boosts (2026-11-17): v_y at z_i = 1.5e4, 3e4, 6e4 km/s -> 504, 1009, 2018 km/s at a = 0.58
# (294, 588, 1176 km/s at z = 0). dyablo 6 x 5 threads + RAMSES 24 ranks (incl. the unboosted _v0 twins with aout 0.5833).
R=/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/runs/pancake_eds
D=$R/../../dyablo_mg/build_cpu3
( source $D/env_cpu.sh > /dev/null 2>&1; export OMP_NUM_THREADS=5
  for n in e_dy_rk2_ent_ei_vy15k e_dy_rk2_ent_ei_vy30k e_dy_rk2_ent_ei_vy60k e_dy_rk2_ei_vy15k e_dy_rk2_ei_vy30k e_dy_rk2_ei_vy60k; do
    [ -f $R/$n.done ] && continue
    ( cd $R/$n; echo "$n start $(date +%T)"; srun -N 1 -n 1 -c 5 --exact $D/dyablo/bin/dyablo $R/$n.ini > $R/$n.log 2>&1
      rc=$?; echo "$n rc=$rc $(date +%T)"; [ $rc = 0 ] && touch $R/$n.done ) &
  done; wait ) &
( module load PrgEnv-gnu > /dev/null 2>&1
  for n in e_ra_o2_pf_vy15k e_ra_o2_pf_vy30k e_ra_o2_pf_vy60k e_ra_o2_vy15k e_ra_o2_vy30k e_ra_o2_vy60k e_ra_o2_pf_v0 e_ra_o2_v0 e_ra_o1_pf_v0; do
    [ -f $R/$n/done ] && continue
    cd $R/$n; echo "$n start $(date +%T)"
    srun -N 1 -n 24 -c 1 --exact $R/../../ramses/bin/ramses_rt13d $n.nml > run.log 2>&1
    rc=$?; echo "$n rc=$rc $(date +%T)"; grep -q "Run completed" run.log && touch done
  done ) &
wait
