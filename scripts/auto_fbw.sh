#!/bin/bash
# 2026-11-20: weekend FB-strength campaign watcher (KB reds_feedback_sf.md 'Calibration levers'; REDS_calib JOURNAL 2026-11-20).
# For each run and each target a (0.090 ... 0.130): once the run is past a+0.001, dashboard of its snapshot at a
# (dash_fbw.sl = run_dashboard_multi.sl on the normal batch QOS: never competes with auto_tsn.sh for the debug job),
# one snapshot per run per job, one job at a time. After each job, for every target that got new results:
# compare_dashboard.py per series (A: smooth SF t10 snx2/4/10; B: bursty n10 t3 snx2/5/10; M: M_max 100 vs 300) with only
# the runs analysed at that target, and fbtrend.py on all of them. State: fbw_state/<run>@<a>.{done,fail1,fail2}. Log auto_fbw.log
B=/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026; R=$B/runs/reio_v2; H=$B/analysis/dyablo_tools/dashboard_dyablo_reio
cd $R || exit 1
module load cray-python/3.11.7 >/dev/null 2>&1; . $B/analysis/pyenv/bin/activate; export OMP_NUM_THREADS=1
LOG=$R/auto_fbw.log; ST=$R/fbw_state; mkdir -p $ST
SPEC="h2_eps0.03n0.5c0.1_mech_snx2_ssp300:eps0.03n0.5c0.1_mech_snx2_t10_ssp300_h2:A
h2_eps0.03n0.5c0.1_mech_snx4_ssp300:eps0.03n0.5c0.1_mech_snx4_t10_ssp300_h2:A
h2_eps0.03n0.5c0.1_mech_snx10_ssp300:eps0.03n0.5c0.1_mech_snx10_t10_ssp300_h2:A
h2_eps0.3_mech_n10_snx2_t3_ssp300:eps0.3_n10_mech_snx2_t3_ssp300_h2:B
h2_eps0.3_mech_n10_snx5_t3_ssp300:eps0.3_n10_mech_snx5_t3_ssp300_h2:B
h2_eps0.3_mech_n10_snx10_t3_ssp300:eps0.3_n10_mech_snx10_t3_ssp300_h2:B
h2_eps0.03n0.5c0.1_mech_snx4_ssp100:eps0.03n0.5c0.1_mech_snx4_t10_ssp100_h2:M"
TARGETS="0.090 0.100 0.110 0.120 0.130"
say() { echo "$(date +%F_%T) $*" >> $LOG; }
aexp_of() { grep -oE "aexp=[0-9.e-]+" $R/$1.log 2>/dev/null | tail -1 | cut -d= -f2; }
past() { local x; x=$(aexp_of $1); [ -n "$x" ] && awk -v a=$2 -v x=$x 'BEGIN{exit !(x > a+0.001)}'; }
zof() { awk -v a=$1 'BEGIN{printf "%.2f", 1/a-1}'; }
say "start (pid $$)"
for loop in $(seq 1 1000); do
  args=""; todo=""
  for s in $SPEC; do
    n=${s%%:*}
    for a in $TARGETS; do
      { [ -f $ST/$n@$a.done ] || [ -f $ST/$n@$a.fail2 ]; } && continue
      past $n $a || break
      it=$(python -I snap_at.py $R/$n $a 2>/dev/null)
      if [ -z "$it" ]; then
        if [ -f $ST/$n@$a.nosnap ]; then say "$n: no snapshot at a=$a (twice), skipped"; touch $ST/$n@$a.fail2
        else say "$n: no snapshot at a=$a yet, retry next loop"; touch $ST/$n@$a.nosnap; fi; break
      fi
      args="$args $R/$n:$it"; todo="$todo $n@$a@$it"; break
    done
  done
  changed=""
  if [ -n "$args" ] && ! squeue -h -u $USER -n dash_fbw 2>/dev/null | grep -q .; then
    j=$(sbatch --parsable dash_fbw.sl $args 2>>$LOG)
    if [ -n "$j" ]; then
      say "dashboards job $j:$args"
      while squeue -h -j $j 2>/dev/null | grep -q .; do sleep 120; done
      say "job $j $(sacct -j $j -X -n -o State,Elapsed | xargs) | $(grep rc= dash_fbw-$j.out | xargs)"
      for t in $todo; do
        n=${t%%@*}; r=${t#*@}; a=${r%%@*}; it=${r#*@}
        if [ -f $R/$n/dashboard/halos_iter$(printf %07d $it).txt ]; then touch $ST/$n@$a.done; changed="$changed $a"
        elif [ -f $ST/$n@$a.fail1 ]; then touch $ST/$n@$a.fail2; say "$n a=$a: dashboard failed twice, skipped"
        else touch $ST/$n@$a.fail1; say "$n a=$a: dashboard failed once, will retry"; fi
      done
    else
      say "sbatch failed, retry next loop"
    fi
  fi
  for a in $(echo $changed | tr ' ' '\n' | sort -u); do
    z=$(zof $a); all=""
    for ser in A B M; do
      L=""; k=0
      for s in $SPEC; do
        n=${s%%:*}; r=${s#*:}; lab=${r%%:*}; sr=${r#*:}
        [ -f $ST/$n@$a.done ] || continue
        all="$all $R/$n:$lab:$sr"
        { [ $sr = $ser ] || { [ $ser = M ] && [ $n = h2_eps0.03n0.5c0.1_mech_snx4_ssp300 ]; }; } && { L="$L $R/$n:$lab"; k=$((k+1)); }
      done
      if [ $k -ge 2 ]; then
        python -I $H/compare_dashboard.py --out $R/compare_fbw_${ser}_z$z --z $z $L > $R/compare_fbw_${ser}_z$z.log 2>&1
        say "compare $ser z=$z rc=$? ($k runs) -> compare_fbw_${ser}_z$z"
      fi
    done
    all=$(echo $all | tr ' ' '\n' | sort -u | xargs)
    python -I $R/fbtrend.py --a $a --out $R/fbw_trend $all > $R/fbw_trend_a$a.log 2>&1
    say "fbtrend a=$a rc=$? -> fbw_trend/fbtrend_a$a.{txt,png}"
  done
  left=0
  for s in $SPEC; do n=${s%%:*}; for a in $TARGETS; do { [ -f $ST/$n@$a.done ] || [ -f $ST/$n@$a.fail2 ]; } || left=1; done; done
  [ $left = 0 ] && { say "all targets done"; exit 0; }
  sleep 600
done
say "loop limit reached"
