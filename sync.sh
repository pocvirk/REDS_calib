#!/bin/bash
# Copy figures, configs, tables and analysis scripts from the Frontier run directories into this repo (idempotent).
# usage: ./sync.sh   then   git add -A && git commit -m "..." && git push
# PNG only for figures (vector PDFs stay on Frontier, except each comparison's multi-page dashboard_compare.pdf).
set -e
B=/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026
R=$B/runs; V=$R/reio_v2; H=$(cd "$(dirname "$0")" && pwd)
cp_png() { mkdir -p "$2"; for f in "$1"/*.png; do [ -e "$f" ] && cp -u "$f" "$2/"; done; return 0; }

# per-run dashboards (dyablo_tools run_dashboard.py) + IGM history tables
for d in $V/*/dashboard/PDFs; do r=$(basename $(dirname $(dirname $d)))
  cp_png $d $H/dashboards/$r
  [ -f $V/$r/dashboard/averages.txt ] && mkdir -p $H/tables/averages && cp -u $V/$r/dashboard/averages.txt $H/tables/averages/$r.txt
done
for d in $R/ramses_box/*/dashboard/PDFs; do r=$(basename $(dirname $(dirname $d)))
  cp_png $d $H/dashboards/RAMSES_$r
  [ -f $R/ramses_box/$r/dashboard/averages.txt ] && cp -u $R/ramses_box/$r/dashboard/averages.txt $H/tables/averages/RAMSES_$r.txt
done

# multi-run comparisons (dyablo_tools compare_dashboard.py)
for d in $V/compare_*/ $R/ramses_box/compare_*/; do s=$(basename $d); [ ${d#$R/ramses_box} != $d ] && s=ramses_box_$s
  cp_png $d $H/comparisons/$s
  [ -f $d/dashboard_compare.pdf ] && cp -u $d/dashboard_compare.pdf $H/comparisons/$s/
done
[ -f $V/compare_z8.png ] && cp -u $V/compare_z8.png $H/comparisons/compare_z8.09/compare_z8_custom.png

# FB-strength campaign trend tables (runs/reio_v2/fbtrend.py via auto_fbw.sh)
[ -d $V/fbw_trend ] && { cp_png $V/fbw_trend $H/comparisons/fbw_trend; cp -u $V/fbw_trend/*.txt $H/comparisons/fbw_trend/ 2>/dev/null || true; }

# fiducial vs twins (thermal FB, constant eps, c_rad 0.1c): f_esc budget by Mh + UV LF (runs/reio_v2/twins/twins_dash.sh), 2026-11-25
[ -d $V/twins ] && { cp_png $V/twins $H/comparisons/fiducial_twins; cp -u $V/twins/budget_twins_*.txt $H/comparisons/fiducial_twins/ 2>/dev/null || true; }

# boxC (8 cMpc/h) UV LF: latest LF figure; LF post-processing (aperture / metallicity / dust) and mock JWST photometry
# (runs/reio_v2/boxsize/lfpp: extract.py, lfpp.py, mock_phot.py, mock_plots.py, mock_simcomp.py), 2026-11-26
[ -f $V/boxsize/uvlf_boxC_latest.png ] && { mkdir -p $H/comparisons/box_size_4_vs_8mpc; cp -u $V/boxsize/uvlf_boxC_latest.png $H/comparisons/box_size_4_vs_8mpc/; }
if [ -d $V/boxsize/lfpp ]; then L=$H/comparisons/boxC_lf_postproc; mkdir -p $L/scripts
  cp_png $V/boxsize/lfpp $L; cp -u $V/boxsize/lfpp/boxC_lfpp.txt $L/ 2>/dev/null || true
  cp_png $V/boxsize/lfpp/mock $L/mock_photometry; cp -u $V/boxsize/lfpp/mock/boxC_mock*.txt $L/mock_photometry/ 2>/dev/null || true
  cp_png $V/boxsize/lfpp/maps $L/halo_maps
  cp -u $V/boxsize/lfpp/*.py $V/boxsize/lfpp/mock/run_iter.sh $L/scripts/ 2>/dev/null || true
fi

# halo maps
cp_png $V/porosity_z9 $H/maps/porosity_z9; cp -u $V/porosity_z9/halo_porosity_summary.txt $H/maps/porosity_z9/ 2>/dev/null || true

# isolated z=7 disc scans
cp_png $R/disc_z7 $H/discs_z7

# idealised hydro tests (non-regression suite, KB research/dyablo/hydro_regression): figures + configs/scripts
K=$B/knowledge_base/research/dyablo/hydro_regression; T=$H/idealised_test_cases; F=$R/sf_halo_diag/figures
mkdir -p $T/t1_pancake $T/t2_pancake_galilean $T/t3_adiabatic_cosmo $T/t4_single_sn
cp -u $R/pancake_eds/eds_z0.png $R/pancake_eds/eds_z2.png $R/pancake_eds/eds_scan_z0.png $R/pancake_eds/eds_scan_z2.png \
      $R/pancake_eds/eds_mesh_z0.png $T/t1_pancake/
cp -u $R/pancake_eds/ladder_T.png $R/pancake_eds/boost_rho.png $R/pancake_eds/boost_T.png $T/t2_pancake_galilean/
cp -u $F/adiabatic_halos_a0.100_fb_rc.png $F/adiabatic_phase_a0.100_fb_rc.png $F/fix_profiles_a0.100.png $F/fix_maps_*_a0.100.png \
      $F/adiabatic_halos_a0.100.png $F/adiabatic_phase_a0.100.png $T/t3_adiabatic_cosmo/
cp -u $R/fbcomp_fb/fb_history.png $R/fbcomp_fb/fb_slices.png $T/t4_single_sn/
for t in t1_t2_pancake:t1_pancake t3_adiabatic:t3_adiabatic_cosmo t4_sn:t4_single_sn; do
  mkdir -p $T/${t#*:}/setup; find $K/${t%%:*} -maxdepth 1 -type f ! -name "*.png" -exec cp -u {} $T/${t#*:}/setup/ \;; done

# reports (short LaTeX PDFs)
mkdir -p $H/reports; cp -u $R/sf_halo_diag/report_2026-11-17/report.pdf $H/reports/2026-11-17_hydro_validation.pdf

# configs: dyablo inis of the cosmological boxes, RAMSES twins, disc templates
mkdir -p $H/inis/boxB $H/inis/ramses_box $H/inis/disc_z7
cp -u $V/*.ini $H/inis/boxB/
# stellar emission tables (dyablo [rad] emissivity_file, dashboard UV magnitudes)
mkdir -p $H/src_files && cp -u /lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/REDS_src_files/* $H/src_files/
for n in $R/ramses_box/*/*.nml; do [ "$(basename $n)" = run.nml ] || cp -u $n $H/inis/ramses_box/; done
cp -u $R/disc_z7/z7_1e10_mE1_e0.03_n0.1_t10.ini $R/disc_z7/z7_1e10_mE1_e0.03_n0.1_t3.ini $R/disc_z7/make_inis.py $H/inis/disc_z7/

# analysis / job scripts not in dyablo_tools
mkdir -p $H/scripts
cp -u $V/halo_porosity_maps.py $V/snap_at.py $V/auto_h2z.sh $V/h2one.sl $V/chain_h2one.sh $V/porosity_z9/porosity.sl \
      $V/fbtrend.py $V/auto_fbw.sh $V/avgone.sl $V/chain_avgone.sh $V/dash_fbw.sl $R/disc_z7/plot_z7_tsn.py $R/disc_z7/analyse_z7.py $R/disc_z7/raytrace_z7.py $H/scripts/
cp -u $B/knowledge_base/research/dyablo/reio_runs_naming.md $H/scripts/.kb_naming_snapshot.md 2>/dev/null || true
echo "synced into $H ($(du -sh --exclude=.git $H | cut -f1))"
