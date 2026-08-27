# QTrack African Easterly Wave Reproducibility

[![QTrack ERA5 workflow](https://github.com/AhmedEid02/qtrack-aew-reproducibility/actions/workflows/qtrack-end-to-end.yml/badge.svg)](https://github.com/AhmedEid02/qtrack-aew-reproducibility/actions/workflows/qtrack-end-to-end.yml)

**An end-to-end reproducible implementation of African Easterly Wave (AEW) tracking using QTrack v0.0.4 and the official `era5_2010_10day` ERA5 example.**

> **Reproduction status: PASS ✅**  
> Official ERA5 example downloaded and processed successfully in GitHub Actions on 27 August 2026.  
> Successful run: https://github.com/AhmedEid02/qtrack-aew-reproducibility/actions/runs/33070652829

## Verified experiment

| Component | Configuration |
|---|---|
| Tracker | QTrack v0.0.4 |
| Example | `era5_2010_10day` |
| Input | ERA5 700-hPa zonal and meridional winds |
| Sampling | 6-hourly |
| Grid | 1° × 1° |
| Curvature-vorticity averaging radius | 600 km |
| Runtime | Ubuntu 24.04, Python 3.11 |
| NumPy | 1.26.4 |
| Status | Successful end-to-end run |

## Results

**Six AEW systems were returned by the official short ERA5 experiment.** All six showed net westward displacement.

| AEW | Duration (days) | Start lon | End lon | Westward displacement | Distance | Mean speed | Max strength |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 6.50 | 32.9°W | 58.8°W | 25.9° | 3,053 km | 5.44 m s⁻¹ | 1.59×10⁻⁵ s⁻¹ |
| 2 | **8.75** | **4.6°E** | **45.3°W** | **49.9°** | **5,387 km** | 7.13 m s⁻¹ | 1.94×10⁻⁵ s⁻¹ |
| 3 | 6.25 | 21.7°E | 11.1°W | 32.8° | 3,679 km | 6.81 m s⁻¹ | 1.53×10⁻⁵ s⁻¹ |
| 4 | 6.75 | 5.4°E | 25.5°W | 30.9° | 3,463 km | 5.94 m s⁻¹ | **2.61×10⁻⁵ s⁻¹** |
| 5 | 3.75 | 17.8°E | 5.2°W | 23.0° | 2,537 km | 7.83 m s⁻¹ | 1.57×10⁻⁵ s⁻¹ |
| 6 | 2.00 | 38.0°E | 23.8°E | 14.3° | 1,582 km | 9.16 m s⁻¹ | 0.76×10⁻⁵ s⁻¹ |

AEW 2 is the clearest long-track example: approximately 4.6°E to 45.3°W, crossing both 0° and 20°W and covering about 5,387 km. AEW 4 had the largest maximum 700-hPa curvature-vorticity strength among the six returned tracks.

Machine-readable results: [`outputs/aew_track_summary.csv`](outputs/aew_track_summary.csv).

## Workflow

```text
Official QTrack ERA5 700-hPa winds
                ↓
         qtrack.prep_data
                ↓
 curvature vorticity + 600-km averaging
                ↓
       qtrack.run_tracking
                ↓
      qtrack.run_postprocessing
                ↓
 transparent track diagnostics
```

## What this repository adds

QTrack performs the AEW detection and tracking. This repository adds:

- automated execution of an official QTrack ERA5 example;
- a versioned reproducible environment;
- quantitative summaries of track duration, displacement, speed, longitude crossings, and maximum strength;
- GitHub Actions as an independent execution record;
- clear separation between QTrack's method and this reproduction layer.

## Reproduce

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

python scripts/run_qtrack_demo.py --case era5_2010_10day --jobs 2

python scripts/summarize_tracks.py   outputs/qtrack_run/AEW_tracks_post_processed.nc   --csv outputs/aew_track_summary.csv
```

Or use **Actions → qtrack-official-example → Run workflow**.

## Compatibility note

The first CI attempt used NumPy 2.4.6 and reached QTrack's tracking stage before a scalar-conversion incompatibility. Pinning **NumPy 1.26.4** produced a successful end-to-end QTrack v0.0.4 run, so the compatibility pin is retained deliberately.

## Scientific scope

This is a **reproducibility and methods-learning project**, not a new AEW tracking algorithm or a climatological analysis. The short official example demonstrates the workflow; scientific inference would require longer records, sensitivity tests, and independent validation.

## Attribution

QTrack was developed by **Quinton A. Lawton and collaborators**.

Lawton, Q. A., Majumdar, S. J., Dotterer, K., Thorncroft, C., & Schreck, C. J. (2022). *The Influence of Convectively Coupled Kelvin Waves on African Easterly Waves in a Wave-Following Framework*. **Monthly Weather Review, 150**(8), 2055–2072. https://doi.org/10.1175/MWR-D-21-0321.1

QTrack source: https://github.com/qlawton/QTrack

## Author

**Ahmed Hussein Ismail**  
Climate & atmospheric-data researcher · Agro-meteorology · Python/R · Reanalysis  
GitHub: https://github.com/AhmedEid02  
ORCID: https://orcid.org/0009-0001-4542-7150
