# Method note: QTrack proof-of-fit workflow

## Purpose

This mini-project is a reproducibility exercise, not a claim of new AEW science. It demonstrates that a climate-data researcher can understand, configure, validate, and interpret a published atmospheric-tracking workflow.

## QTrack v0.0.4 assumptions checked

The QTrack documentation and source were reviewed for the following main requirements:

- zonal (`u`) and meridional (`v`) wind components
- pressure level at or near 700 hPa
- 6-hourly temporal resolution
- 1 degree by 1 degree grid recommended/tested in the published configuration
- at least about 10 days of input data recommended to provide tracking context/spin-up
- curvature-vorticity calculation followed by 600-km radial smoothing
- AEW tracking followed by post-processing into NetCDF and optional pickle/Hovmoller outputs

## Added diagnostics

The custom summary code deliberately uses simple, transparent metrics:

- start/end positions
- duration
- direct great-circle displacement
- westward longitude displacement
- approximate direct propagation speed
- crossing of 0 degrees and 20 degrees W
- maximum QTrack-provided AEW strength when available

These are diagnostics of the produced track geometry; they are not substitutes for dynamical analysis.

## Reproducibility boundary

The lightweight unit tests use synthetic NetCDF data only to validate file structure, time/grid assumptions, and custom summary functions. A real QTrack run should use the official QTrack example data or independently prepared atmospheric data and should document environment versions and tracking parameters.

## Scientific next step

A stronger follow-on study could compare QTrack ERA5 tracks with rainfall/convection fields, or compare ERA5 with an AI/NWP forecast system to diagnose when propagating tropical disturbances are well or poorly represented. That extension should only be undertaken after the baseline QTrack reproduction has been run and checked.
