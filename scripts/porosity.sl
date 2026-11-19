#!/bin/bash
#SBATCH -A AST031
#SBATCH -J porosity
#SBATCH -o /lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026/runs/reio_v2/porosity_z9/porosity-%j.out
#SBATCH -t 01:00:00
#SBATCH -p batch
#SBATCH -q debug
#SBATCH -N 1
# 2026-11-19: halo porosity maps, 1st order vs h2, z=9 (halo_porosity_maps.py)
B=/lustre/orion/ast031/proj-shared/pocvirk/CoDaIII/prod_sr/pocvirk/dyablo/28102026; R=$B/runs/reio_v2; cd $R/porosity_z9
module load cray-python/3.11.7 PrgEnv-gnu cray-hdf5-parallel; . $B/analysis/pyenv/bin/activate; export OMP_NUM_THREADS=8
L="epsn0.03c0.1_chemfix:eps0.03n0.5c0.1_th_t10_1st_order h2_epsn0.03c0.1:eps0.03n0.5c0.1_th_t10_h2
cf_eps0.03_mech_snx2:eps0.03_mech_snx2_t10_1st_order h2_eps0.03_mech_snx2:eps0.03_mech_snx2_t10_h2
cf_eps0.3_mech_n10_snx2:eps0.3_mech_n10_snx2_t3_1st_order h2_eps0.3_mech_n10_snx2:eps0.3_mech_n10_snx2_t3_h2"
F=""
for x in $L; do d=${x%%:*}; l=${x#*:}; F="$F $l.npy"
  srun --exact -N 1 -n 1 -c 8 python -I -W ignore $R/halo_porosity_maps.py compute $R/$d $l $l.npy > $l.log 2>&1 &
done; wait
grep -h "halo" *.log
python -I -W ignore $R/halo_porosity_maps.py plot $F
