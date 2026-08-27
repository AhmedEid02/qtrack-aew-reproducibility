# Validation report — 27 August 2026

## End-to-end reproduction status

**PASS.** The official QTrack `era5_2010_10day` example was successfully executed in GitHub Actions using QTrack v0.0.4, Python 3.11, and NumPy 1.26.4.

Successful reference run: https://github.com/AhmedEid02/qtrack-aew-reproducibility/actions/runs/33085165852

## Verified workflow

1. Download official ERA5 700-hPa wind example.
2. Run `qtrack.prep_data`.
3. Compute curvature vorticity using a 600-km averaging radius.
4. Run automated AEW tracking.
5. Run QTrack post-processing.
6. Summarize returned tracks and generate longitude–time diagnostics.

## Verified output

The short ERA5 experiment returned **six AEW systems**, all with net westward displacement during their valid tracked periods. AEW 2 had the longest track (8.75 days) and propagated from approximately 4.6°E to 45.3°W. AEW 4 had the largest maximum curvature-vorticity strength among the returned tracks (~2.61 × 10⁻⁵ s⁻¹).

Included reproducibility outputs:

- `outputs/aew_track_summary.csv`
- `outputs/AEW_tracks_post_processed.nc`
- `figures/aew_longitude_time.png`
- `figures/final_hovmoller.png`

## Compatibility finding

The first workflow attempt installed NumPy 2.4.6 and reached QTrack's tracking stage before a scalar-conversion incompatibility. Pinning **NumPy 1.26.4** resolved that incompatibility and produced the successful end-to-end run. The pin is therefore retained deliberately.

## Scope

This validates execution and reproduction of QTrack's official short example. It is not a climatological AEW study and does not independently validate the tracking algorithm. Longer records, sensitivity tests, and independent track comparisons would be required for substantive scientific inference.
