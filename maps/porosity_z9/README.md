# porosity_z9

z = 9 (a = 0.100). The 3 most massive halos (2-3.3e9 Msun) of the box, matched by position in the 1st-order and h2
(production hydro) versions of 3 recipes. One figure per halo (`halo_porosity_<k>.png`), rows = runs, columns:
N_H and N_HI columns through the slab |z| < R200, mass-weighted T in the same slab (maps 4 R200 wide, dashed circle R200,
cyan dots = stars < 10 Myr), and the sky map of the photon-weighted transmission exp(-sigma N_HI) from all stars to
1728 HEALPix points on the R200 sphere (its mean = the dashboard ray-traced f_esc; checked).
`halo_porosity_summary.txt`: per halo and run, M_h, M*, f_esc, open-sky fraction, gas mass and diffuse volume fraction in R200.
Script: `scripts/halo_porosity_maps.py` (+ `scripts/porosity.sl`).
