#!/bin/bash
#SBATCH -A AST031
#SBATCH -J dash_fbw
#SBATCH -o /lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/runs/reio_v2/dash_fbw-%j.out
#SBATCH -t 02:00:00
#SBATCH -p batch
#SBATCH -N 1
# 2026-11-20: copy of dyablo_tools run_dashboard_multi.sl on the normal batch QOS (no -q debug), for the weekend watcher auto_fbw.sh, so that it never competes with auto_tsn.sh for the 1 debug job. Was: dashboards of several reio runs in parallel on one node (2026-11-17). usage: sbatch run_dashboard_multi.sl <rundir>[:iter,iter...] ...
# (2026-11-18) optional :iter list -> run_dashboard.py --snap (galaxy analysis at those iterations; default last snapshot)
HERE=/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/analysis/dyablo_tools/dashboard_dyablo_reio
PYENV=/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/analysis/pyenv
export FOF_DYABLO=/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/analysis/dyablo_tools/dyablo_fof/fof
module load cray-python/3.11.7 PrgEnv-gnu cray-hdf5-parallel
. $PYENV/bin/activate
c=$(( 56 / $# ))
for a in "$@"; do
  d=${a%%:*}; sn=""; [ "$a" != "$d" ] && sn="--snap ${a#*:}" && sn=${sn//,/ }
  ( srun --exact -N 1 -n 1 -c $c python -I -W ignore $HERE/run_dashboard.py $d $sn > $d/dashboard_$SLURM_JOB_ID.log 2>&1; echo "$(basename $d) rc=$? $(date +%T)" ) &
done
wait
