#!/bin/bash
#SBATCH -A AST031
#SBATCH -J adi_fb
#SBATCH -o /lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/runs/reio_v2/%x-%j.out
#SBATCH -t 02:00:00
#SBATCH -q debug
#SBATCH -N 3
# 2026-11-17 negative-pressure fallback test on the adiabatic twin: build build_fb on a compute node, then
# A adi_fb_floor (smallp floor, noise floor vs adi_rk2), B adi_fb_adiabat (p0 (rho/rho0)^gamma), C adi_fb_pf0 (RAMSES pf beta_fix 0),
# one node each, concurrently.
R=/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/runs/reio_v2
D=/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/dyablo_mg
B=build_fb
if [ ! -x $D/$B/dyablo/bin/dyablo ]; then
  srun -N 1 -n 1 -c 56 bash $D/$B/build.sh > $D/$B/build.log 2>&1; rc=$?
  echo "build rc=$rc $(date +%T)"; [ $rc = 0 ] && [ -x $D/$B/dyablo/bin/dyablo ] || { tail -30 $D/$B/build.log; exit 1; }
fi
module purge
source $D/build_gpu/env_frontier_gpu.sh
export OMP_NUM_THREADS=7 OMP_PROC_BIND=true MPICH_GPU_SUPPORT_ENABLED=1 MPICH_GPU_IPC_ENABLED=0
for n in adi_fb_floor adi_fb_adiabat adi_fb_pf0; do
  ( [ -f $R/$n.done ] && exit 0
    cd $R/$n
    srun -N 1 -n 8 -c 7 --gpus-per-task=1 --gpu-bind=closest $D/$B/dyablo/bin/dyablo $R/$n.ini >> $R/$n.log 2>&1
    rc=$?; echo "$n EXIT_CODE=$rc $(date +%T)"; [ $rc = 0 ] && touch $R/$n.done ) &
done
wait
