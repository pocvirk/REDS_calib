#!/bin/bash
#SBATCH -A AST031
#SBATCH -J fb_E
#SBATCH -o /lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/runs/fbcomp_fb/%x-%j.out
#SBATCH -t 01:00:00
#SBATCH -q debug
#SBATCH -N 3
# 2026-11-17 flavour E (entropy fallback only where e_int < 0, dual_energy_eta = 0): SN tests (10) and the pancake boost
# ladder (5 boosts), plus flavour B (adiabat fallback) on the ladder (5); build_fb (GPU), 1 GPU per run
R=/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/runs
D=/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/dyablo_mg
module purge
source $D/build_gpu/env_frontier_gpu.sh
export OMP_NUM_THREADS=7 OMP_PROC_BIND=true MPICH_GPU_SUPPORT_ENABLED=1 MPICH_GPU_IPC_ENABLED=0
for ini in $R/fbcomp_fb/n*_E.ini $R/pancake_eds/e_dy_rk2_eta0_ei*.ini $R/pancake_eds/e_dy_rk2_fbad_ei*.ini; do n=${ini%.ini}
  ( cd $n; srun --exact -N 1 -n 1 -c 7 --gpus-per-task=1 --gpu-bind=closest $D/build_fb/dyablo/bin/dyablo $ini > $n.log 2>&1; rc=$?
    echo "=== $(basename $n) EXIT_CODE=$rc $(date +%T)"; [ $rc = 0 ] && touch $n.done ) &
done
wait
