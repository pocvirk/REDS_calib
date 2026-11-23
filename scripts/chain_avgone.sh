#!/bin/bash
# usage: chain_avgone.sh <run>: resubmit avgone.sl (1 node, 2 h) until <run>.done, max 40 jobs. Log: chain_<run>.log
cd /lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/runs/reio_v2
RUNS=$1
j0=""
for k in $(seq 1 40); do
  left=0; for n in $RUNS; do [ -f $n.done ] || left=1; done; [ $left = 0 ] && { echo "ALL DONE"; exit 0; }
  if [ -n "$j0" ]; then j=$j0; j0=""; else j=$(sbatch --parsable avgone.sl $RUNS) || { echo "sbatch failed"; exit 1; }; fi
  echo "job $k: $j submitted $(date +%m-%d_%H:%M)"
  while squeue -h -j $j 2>/dev/null | grep -q .; do sleep 120; done
  echo "job $k: $j $(sacct -j $j -X -n -o State,Elapsed | xargs)"
  for n in $RUNS; do echo "   $n $(grep -o 'aexp=[0-9.]*' $n.log | tail -1) $(grep -o 'star_formed=[0-9]*' $n.log | tail -1) $(grep -o 'xion_mean=[0-9.e-]*' $n.log | tail -1)"; done
  grep -q "build rc=[1-9]" reio_avgone-$j.out 2>/dev/null && { echo "build failed in $j: stopping"; exit 1; }
  # a run that exits non-zero well before the 2 h walltime crashed: stop the chain
  el=$(sacct -j $j -X -n -o ElapsedRaw | xargs)
  if grep -q "EXIT_CODE=[1-9]" reio_avgone-$j.out && [ "${el:-0}" -lt 6600 ]; then echo "a run failed in $j: stopping"; grep EXIT_CODE reio_avgone-$j.out; exit 1; fi
done
