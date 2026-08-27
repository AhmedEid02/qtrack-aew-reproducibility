# Reproducible African Easterly Wave Tracking with QTrack

**A compact atmospheric-science reproducibility project built around Quinton A. Lawton's QTrack package.**

This repository demonstrates a transparent transition from climate-data analysis into tropical meteorology, atmospheric-wave diagnostics, and reproducible scientific computing. It uses **QTrack v0.0.4** as an external dependency; QTrack source code is not copied into this repository.

## Scientific question

Can a reproducible workflow recover African Easterly Wave (AEW) tracks from 700-hPa wind fields and summarize how those waves initiate over Africa and propagate westward toward the Atlantic?

## Why QTrack?

QTrack is an open-source Python AEW tracker developed by Quinton A. Lawton and collaborators. The current package documentation specifies 700-hPa zonal and meridional winds, ideally on a 1-degree grid at 6-hourly resolution. QTrack prepares the wind data, computes a curvature-vorticity field smoothed over a 600-km radius, tracks coherent AEW centers, and post-processes the tracks into analysis-ready outputs.

**Method reference**

Lawton, Q. A., Majumdar, S. J., Dotterer, K., Thorncroft, C., & Schreck, C. J. (2022). *The Influence of Convectively Coupled Kelvin Waves on African Easterly Waves in a Wave-Following Framework*. Monthly Weather Review, 150(8), 2055-2072. https://doi.org/10.1175/MWR-D-21-0321.1

QTrack: https://github.com/qlawton/QTrack

## What this repository adds

After QTrack generates post-processed tracks, this project derives a compact set of interpretable diagnostics:

- AEW count and track duration
- initiation and terminal longitude/latitude
- westward displacement
- approximate propagation speed
- maximum curvature-vorticity strength, when available
- whether a track crosses 0 degrees and 20 degrees W
- CSV summary for reproducible comparison across cases
- longitude-time diagnostic of tracked waves
- input-contract checks and lightweight unit tests

The goal is not to modify QTrack, but to show that its outputs can be reproduced, checked, summarized, and interpreted transparently.

## Workflow

```text
Official QTrack wind example (ERA5 / GFS / MPAS-A)
        |
        v
Input-contract validation
(u, v; 700 hPa; ~1 degree; 6-hourly)
        |
        v
qtrack.prep_data
        |
        v
Curvature vorticity + 600-km smoothing
        |
        v
AEW tracking
        |
        v
Post-processing
        |
        +--> QTrack Hovmoller diagnostic
        |
        v
Track metrics + CSV + longitude-time figure
```

## Repository structure

```text
.
├── .github/workflows/
│   ├── ci.yml
│   └── qtrack-end-to-end.yml
├── data/
├── docs/
│   └── method_note.md
├── figures/
├── notebooks/
│   └── qtrack_aew_proof_of_fit.ipynb
├── outputs/
├── scripts/
│   ├── check_input_contract.py
│   ├── make_synthetic_winds.py
│   ├── run_qtrack_demo.py
│   ├── summarize_tracks.py
│   └── plot_tracks.py
├── tests/
│   ├── test_input_contract.py
│   └── test_track_summary.py
├── CITATION.cff
├── LICENSE
├── environment.yml
└── requirements.txt
```

## Quick start

### 1. Create an environment

Using conda/mamba:

```bash
conda env create -f environment.yml
conda activate aew-qtrack
```

Or with pip:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

### 2. Validate the repository without downloading large meteorological data

```bash
python scripts/make_synthetic_winds.py
python scripts/check_input_contract.py data/synthetic_700hpa_winds.nc
pytest -q
```

The synthetic dataset validates **software plumbing and QTrack's input contract only**. It is not presented as a real or detected AEW.

### 3. Run QTrack's official short ERA5 example

```bash
python scripts/run_qtrack_demo.py --case era5_2010_10day --jobs 2
```

The runner follows QTrack's documented sequence:

1. `qtrack.prep_data`
2. `qtrack.curvvort.compute_curvvort`
3. `qtrack.tracking.run_tracking`
4. `qtrack.tracking.run_postprocessing`

### 4. Summarize and visualize the tracks

```bash
python scripts/summarize_tracks.py outputs/AEW_tracks_post_processed.nc \
  --csv outputs/aew_track_summary.csv

python scripts/plot_tracks.py outputs/AEW_tracks_post_processed.nc \
  --out figures/aew_longitude_time.png
```

## Validation status

- Custom repository scripts: syntax-checked and unit-tested with synthetic NetCDF datasets.
- QTrack API, required wind fields, recommended resolution, workflow sequence, and output variable names: checked against QTrack v0.0.4 source/documentation.
- Official ERA5 end-to-end run: configured in `scripts/run_qtrack_demo.py` and in the manual GitHub Actions workflow. It requires QTrack and its meteorological dependencies plus runtime access to the official example dataset.

## Scientific caution

The tracker is sensitive to data resolution, domain, temporal sampling, curvature-vorticity thresholds, and post-processing choices. A successful software run is not by itself scientific validation. Any research use should document sensitivity tests and compare tracks with established datasets or independent diagnostics.

## Author

**Ahmed Hussein Ismail**  
Climate & atmospheric-data researcher | Agro-meteorology | Python/R | Reanalysis  
GitHub: https://github.com/AhmedEid02  
ORCID: https://orcid.org/0009-0001-4542-7150

## Attribution

QTrack is developed and maintained by Quinton A. Lawton and collaborators and is distributed under its own MIT license. This repository depends on QTrack and cites the underlying method; it does not redistribute QTrack source code.
