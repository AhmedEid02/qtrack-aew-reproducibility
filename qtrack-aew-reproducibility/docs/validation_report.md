# Validation report - 27 August 2026

## What was checked against QTrack v0.0.4 source/documentation

- required wind variables: `u` and `v`
- recommended pressure level: near 700 hPa
- recommended grid: 1 degree x 1 degree
- temporal sampling: 6-hourly
- recommended minimum input period: about 10 days
- workflow: `prep_data` -> curvature vorticity -> `run_tracking` -> `run_postprocessing`
- post-processed variables used by the custom diagnostics: `AEW_lon`, `AEW_lat`, and optional `AEW_strength`

## Local software-validation tests

Synthetic QTrack-contract dataset:

- dimensions: 41 time steps x 31 latitudes x 121 longitudes
- timestep: 6 h
- grid: 1 degree x 1 degree
- duration: 10.00 days
- input-contract result: **PASS**

Unit tests:

```text
2 passed
```

The track-summary and plotting CLIs were also executed on a synthetic QTrack-like post-processed NetCDF file. They produced:

- `outputs/synthetic_track_summary.csv`
- `figures/synthetic_aew_longitude_time.png`

## Important limitation

This environment cannot install QTrack's full meteorological dependency stack or download the official QTrack ERA5 example at runtime. Therefore, this report does **not** claim an end-to-end scientific QTrack reproduction. The repository contains a documented ERA5 10-day runner and a manually triggered GitHub Actions workflow to complete that step in a network-enabled environment.
