#!/bin/bash
#SBATCH -A AST031
#SBATCH -J reio_avgone
#SBATCH -o /lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/runs/reio_v2/%x-%j.out
#SBATCH -t 02:00:00
#SBATCH -p batch
#SBATCH -N 1
# 2026-11-20: h2one.sl with build_avg (build_h2 + AveragesLogger, [run] dump_averages; physics identical), for new runs only (usage: sbatch avgone.sl <run>). Was: 2026-11-18 single-run version of h2.sl. 2026-11-17: calibration candidates with the validated production hydro (build_h2, REDS_hydro 7b0f0215), normal QOS, one node per run,
# each from its ICs or its latest checkpoint; a run with EXIT_CODE=0 (aexp 1/6) is marked .done and skipped. Chain: chain_avgone.sh
R=/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/runs/reio_v2
D=/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/dyablo_mg
if [ ! -x $D/build_avg/dyablo/bin/dyablo ]; then
  srun -N 1 -n 1 -c 56 bash $D/build_avg/build.sh > $D/build_avg/build.log 2>&1; rc=$?
  echo "build rc=$rc $(date +%T)"; [ $rc = 0 ] && [ -x $D/build_avg/dyablo/bin/dyablo ] || { tail -30 $D/build_avg/build.log; exit 1; }
fi
module purge
source $D/build_gpu/env_frontier_gpu.sh
export OMP_NUM_THREADS=7 OMP_PROC_BIND=true MPICH_GPU_SUPPORT_ENABLED=1 MPICH_GPU_IPC_ENABLED=0
date
for n in $1; do
  [ -f $R/$n.done ] && { echo "$n done"; continue; }
  cd $R/$n
  last=$(ls restart_${n}_*.ini 2>/dev/null | sed 's/.*_\([0-9]*\)\.ini/\1/' | sort -n | tail -1)
  if [ -z "$last" ]; then ini=$R/$n.ini; else ini=$PWD/restart_run_${last}.ini; cp restart_${n}_${last}.ini $ini; fi
  echo "$n: $ini"
  ( srun -N 1 -n 8 -c 7 --gpus-per-task=1 --gpu-bind=closest --exact $D/build_avg/dyablo/bin/dyablo $ini >> $R/$n.log 2>&1
    rc=$?; echo "$n EXIT_CODE=$rc $(date +%T)"; [ $rc = 0 ] && touch $R/$n.done ) &
done
wait
date
