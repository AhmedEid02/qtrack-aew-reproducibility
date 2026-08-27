# Method note

This repository reproduces **QTrack v0.0.4** using the official `era5_2010_10day` example.

The verified sequence is:

1. Download the official ERA5 700-hPa zonal and meridional wind example.
2. Preprocess the fields with `qtrack.prep_data`.
3. Compute curvature vorticity with a 600-km spatial averaging radius.
4. Run QTrack's AEW tracker.
5. Post-process the detected systems.
6. Derive transparent diagnostics of duration, displacement, direct speed, longitude crossings, and maximum strength.
7. Generate a longitude–time track figure.

QTrack performs the tracking. The code added here provides reproducibility, version control, diagnostics, tests, and documentation; it does not modify or claim authorship of QTrack's tracking algorithm.
