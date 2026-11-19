#!/bin/bash
# 2026-11-19: z=9 then z=8.09 comparison of the 3 h2 calibration runs (production hydro) vs their 1st-order counterparts,
# whose dashboards at a=0.100 / 0.110 exist (debug job 5946780). Per target a: wait until all 3 h2 runs are past it (log aexp > a+0.001),
# one debug dashboard job for the 3 runs at that snapshot, then compare_dashboard.py. Labels from the inis (FB type + t_SNII). Log auto_h2z.log
B=/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026; R=$B/runs/reio_v2; H=$B/analysis/dyablo_tools/dashboard_dyablo_reio; cd $R
module load cray-python/3.11.7 >/dev/null 2>&1; . $B/analysis/pyenv/bin/activate; export OMP_NUM_THREADS=1
N="h2_epsn0.03c0.1 h2_eps0.03_mech_snx2 h2_eps0.3_mech_n10_snx2"
L="$R/epsn0.03c0.1_chemfix:eps0.03n0.5c0.1_th_t10_1st_order $R/cf_eps0.03_mech_snx2:eps0.03_mech_snx2_t10_1st_order $R/cf_eps0.3_mech_n10_snx2:eps0.3_mech_n10_snx2_t3_1st_order
   $R/h2_epsn0.03c0.1:eps0.03n0.5c0.1_th_t10_h2 $R/h2_eps0.03_mech_snx2:eps0.03_mech_snx2_t10_h2 $R/h2_eps0.3_mech_n10_snx2:eps0.3_mech_n10_snx2_t3_h2"
past() { for n in $N; do awk -v a=$1 -v x=$(grep -oE "aexp=[0-9.e-]+" $n.log | tail -1 | cut -d= -f2) 'BEGIN{exit !(x > a+0.001)}' || return 1; done; }
for az in 0.100:9 0.110:8.09; do
  a=${az%%:*}; z=${az#*:}
  until past $a; do sleep 300; done
  args=""; for n in $N; do it=$(python -I snap_at.py $n $a 2>/dev/null); [ -z "$it" ] && { echo "$(date +%F_%T) $n: no snapshot at a=$a" >> auto_h2z.log; continue 2; }; args="$args $R/$n:$it"; done
  until ! squeue -h -u $USER -q debug | grep -q .; do sleep 120; done   # debug QOS: 1 job per user
  j=$(sbatch --parsable $H/run_dashboard_multi.sl $args); echo "$(date +%F_%T) a=$a dashboards job $j:$args" >> auto_h2z.log
  while squeue -h -j $j 2>/dev/null | grep -q .; do sleep 60; done; tail -3 dash_multi-$j.out >> auto_h2z.log
  python -I $H/compare_dashboard.py --out $R/compare_h2_z$z --z $z $L > compare_h2_z$z.log 2>&1
  echo "$(date +%F_%T) compare rc=$? -> compare_h2_z$z" >> auto_h2z.log
done
