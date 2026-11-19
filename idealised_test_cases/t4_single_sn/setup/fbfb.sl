#!/bin/bash
#SBATCH -A AST031
#SBATCH -J fbcomp_fb
#SBATCH -o /lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/runs/fbcomp_fb/%x-%j.out
#SBATCH -t 01:00:00
#SBATCH -q debug
#SBATCH -N 4
# 2026-11-17 negative-pressure fallback flavours (A floor, B adiabat, C RAMSES pf beta 0) on the fbcomp SN tests: 30 runs, 1 GPU each
R=/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/runs/fbcomp_fb
D=/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/dyablo_mg
module purge
source $D/build_gpu/env_frontier_gpu.sh
export OMP_NUM_THREADS=7 OMP_PROC_BIND=true MPICH_GPU_SUPPORT_ENABLED=1 MPICH_GPU_IPC_ENABLED=0
cd $R
for f in n*_*_[ABC].ini; do n=${f%.ini}
  ( cd $R/$n; srun --exact -N 1 -n 1 -c 7 --gpus-per-task=1 --gpu-bind=closest $D/build_fb/dyablo/bin/dyablo $R/$f > $R/$n.log 2>&1; echo "=== $n EXIT_CODE=$? $(date +%T)" ) &
done
wait
