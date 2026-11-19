#!/bin/bash
#SBATCH -A AST031
#SBATCH -J fbcomp_fb2
#SBATCH -o /lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/runs/fbcomp_fb/%x-%j.out
#SBATCH -t 01:30:00
#SBATCH -q debug
#SBATCH -N 5
# 2026-11-17 follow-up: rebuild build_fb (per-RK2-stage negative-pressure counts), then
# - flavour D (Tep entropy eta 0.1) on all 10 setups, cfl 0.8
# - resolved cases (n1_dx2, n100_dx0.3; th, mech): A, B, C rerun at cfl 0.8 (stage counts), A at cfl 0.2 and 0.1, B at cfl 0.2
R=/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/runs/fbcomp_fb
D=/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/dyablo_mg
srun -N 1 -n 1 -c 56 bash $D/build_fb/build.sh > $D/build_fb/build2.log 2>&1; rc=$?
echo "build rc=$rc $(date +%T)"; [ $rc = 0 ] || { tail -30 $D/build_fb/build2.log; exit 1; }
module purge
source $D/build_gpu/env_frontier_gpu.sh
export OMP_NUM_THREADS=7 OMP_PROC_BIND=true MPICH_GPU_SUPPORT_ENABLED=1 MPICH_GPU_IPC_ENABLED=0
cd $R
runs="$(ls n*_D.ini n*_c0[12].ini) $(for b in n1_dx2_th n1_dx2_mech n100_dx0.3_th n100_dx0.3_mech; do echo $b"_A.ini" $b"_B.ini" $b"_C.ini"; done)"
for f in $runs; do n=${f%.ini}
  ( cd $R/$n; srun --exact -N 1 -n 1 -c 7 --gpus-per-task=1 --gpu-bind=closest $D/build_fb/dyablo/bin/dyablo $R/$f > $R/$n.log 2>&1; echo "=== $n EXIT_CODE=$? $(date +%T)" ) &
done
wait
