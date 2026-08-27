#!/usr/bin/env python
"""Validate the main input assumptions documented by QTrack v0.0.4."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import xarray as xr


@dataclass
class ContractReport:
    timestep_hours: float
    lon_resolution_deg: float
    lat_resolution_deg: float
    duration_days: float


def _coord_name(ds: xr.Dataset, candidates: tuple[str, ...]) -> str:
    hits = [c for c in candidates if c in ds.coords or c in ds.dims]
    if len(hits) != 1:
        raise ValueError(f"Expected exactly one coordinate from {candidates}; found {hits}")
    return hits[0]


def validate_dataset(ds: xr.Dataset, require_ten_days: bool = True) -> ContractReport:
    for var in ("u", "v"):
        if var not in ds.data_vars:
            raise ValueError(f"Missing required wind component: {var}")

    lon_name = _coord_name(ds, ("longitude", "lon", "lons"))
    lat_name = _coord_name(ds, ("latitude", "lat", "lats"))
    if "time" not in ds.coords:
        raise ValueError("Missing time coordinate")

    times = pd.DatetimeIndex(pd.to_datetime(ds["time"].values))
    if len(times) < 2:
        raise ValueError("At least two time steps are required")
    dt_hours = np.diff(times.asi8) / 3.6e12
    if not np.allclose(dt_hours, 6.0):
        raise ValueError(f"QTrack is documented for 6-hourly data; found {np.unique(dt_hours)} h")

    lon = np.asarray(ds[lon_name].values, dtype=float)
    lat = np.asarray(ds[lat_name].values, dtype=float)
    if len(lon) < 2 or len(lat) < 2:
        raise ValueError("Latitude and longitude require multiple grid points")
    lon_res = float(np.nanmedian(np.abs(np.diff(lon))))
    lat_res = float(np.nanmedian(np.abs(np.diff(lat))))
    if not np.isclose(lon_res, 1.0, atol=1e-6) or not np.isclose(lat_res, 1.0, atol=1e-6):
        raise ValueError(f"Recommended QTrack grid is 1 degree; found lon={lon_res:g}, lat={lat_res:g}")

    duration_days = (times[-1] - times[0]).total_seconds() / 86400.0
    if require_ten_days and duration_days < 10.0:
        raise ValueError(f"QTrack recommends at least ~10 days; dataset covers {duration_days:.2f} days")

    return ContractReport(6.0, lon_res, lat_res, duration_days)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--allow-short", action="store_true")
    args = parser.parse_args()

    path = Path(args.path)
    with xr.open_dataset(path) as ds:
        report = validate_dataset(ds, require_ten_days=not args.allow_short)
    print("QTrack input-contract check: PASS")
    print(f"  timestep: {report.timestep_hours:g} h")
    print(f"  grid: {report.lat_resolution_deg:g} x {report.lon_resolution_deg:g} degrees")
    print(f"  duration: {report.duration_days:.2f} days")


if __name__ == "__main__":
    main()
