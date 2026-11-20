# REDS_src_files: stellar emission tables for REDS runs (dyablo [rad] emissivity_file and dashboard UV magnitudes)

Layout (comma separated, `#` comments): n_age (51), n_Z (13), ages [Myr] (1 to 1e5, 0.1 dex), Z (absolute, 0.02 = Zsun),
then 5 blocks of n_Z rows vs age: ionizing emissivity [photons/s per Msun of initial stellar mass], M_AB1600 (per Msun),
continuum at 1500 A, continuum at 2500 A, UV slope beta. dyablo (ParticleUpdate_NGP_src_bpass) reads block 1;
dyablo_tools dashboard_dyablo_reio reads block 2 for the UV magnitudes (LF, SMHM) when the run's emissivity_file is in this dir.

| file | model | added |
|---|---|---|
| `SSP_BPASSv2.2.1_kroupa_binary_MMax100_pseudo-f1_pf_width200Angstrom_emissivites_mags_betas.txt` | BPASS v2.2.1 binary, imf135_100 (Kroupa-like, M_max 100 Msun), single burst (SSP) | 2026-11-20, PO (remade); identical to dashboard_rc `Emissivity_MAB1600_BPASSv2.2.1_kroupa_binary_MMax=100.txt` |
| `SSP_BPASSv2.2.1_kroupa_binary_MMax300_pseudo-f1_pf_width200Angstrom_emissivites_mags_betas.txt` | same, imf135_300 (M_max 300 Msun, as MEGATRON) | 2026-11-20, PO |
| `cstSFR_5Myr_BPASSv2.2.1_kroupa_binary_MMax=100_emissivites_mags_betas.txt` | imf135_100, particle formed at constant rate over 5 Myr (CoDa III table; all REDS runs before 2026-11-20) | copy of dyablo_mg/settings/stellar_emissivity |

At Z = 0.001, photons per Msun of initial mass (dyablo interpolation, Q held at its 1 Myr value below 1 Myr):

| table | Q(1 Myr) | Q(5 Myr) | N(<10 Myr) | N(<200 Myr) |
|---|---|---|---|---|
| SSP MMax100 | 4.0e46 | 2.2e46 | 8.2e60 | 8.9e60 |
| SSP MMax300 | 7.8e46 | 2.3e46 | 1.17e61 | 1.23e61 (+38%) |
| cstSFR 5 Myr MMax100 | 7.0e45 | 3.7e46 | 6.8e60 | 7.9e60 |
