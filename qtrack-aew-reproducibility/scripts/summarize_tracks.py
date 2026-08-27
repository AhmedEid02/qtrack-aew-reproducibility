#!/usr/bin/env python
"""Summarize post-processed QTrack AEW tracks into analysis-ready metrics."""
from __future__ import annotations

from pathlib import Path
import argparse
import math
import numpy as np
import pandas as pd
import xarray as xr

EARTH_RADIUS_KM = 6371.0


def haversine_km(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    dp = math.radians(lat2 - lat1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


def _time_index(ds: xr.Dataset) -> pd.DatetimeIndex | None:
    try:
        idx = pd.DatetimeIndex(pd.to_datetime(ds["time"].values))
        if idx.isna().any():
            return None
        return idx
    except Exception:
        return None


def summarize_dataset(ds: xr.Dataset, default_timestep_hours: float = 6.0) -> pd.DataFrame:
    required = {"AEW_lon", "AEW_lat"}
    missing = required - set(ds.data_vars)
    if missing:
        raise ValueError(f"Missing QTrack output variables: {sorted(missing)}")

    lon = np.asarray(ds["AEW_lon"].values, dtype=float)
    lat = np.asarray(ds["AEW_lat"].values, dtype=float)
    if lon.ndim != 2 or lat.shape != lon.shape:
        raise ValueError("Expected AEW_lon and AEW_lat with shape (system, time)")

    strength = np.asarray(ds["AEW_strength"].values, dtype=float) if "AEW_strength" in ds else None
    times = _time_index(ds)
    records: list[dict] = []

    for i in range(lon.shape[0]):
        valid = np.isfinite(lon[i]) & np.isfinite(lat[i])
        idx = np.flatnonzero(valid)
        if not len(idx):
            continue
        first, last = int(idx[0]), int(idx[-1])
        n_steps = len(idx)

        if times is not None:
            duration_hours = max((times[last] - times[first]).total_seconds() / 3600.0, 0.0)
        else:
            duration_hours = max((last - first) * default_timestep_hours, 0.0)

        start_lon, start_lat = float(lon[i, first]), float(lat[i, first])
        end_lon, end_lat = float(lon[i, last]), float(lat[i, last])
        direct_km = haversine_km(start_lon, start_lat, end_lon, end_lat)
        westward_deg = start_lon - end_lon
        speed_ms = (direct_km * 1000 / (duration_hours * 3600)) if duration_hours > 0 else np.nan

        rec = {
            "system": i + 1,
            "n_valid_steps": n_steps,
            "duration_days": duration_hours / 24.0,
            "start_lon": start_lon,
            "start_lat": start_lat,
            "end_lon": end_lon,
            "end_lat": end_lat,
            "westward_displacement_deg": westward_deg,
            "direct_displacement_km": direct_km,
            "mean_direct_speed_ms": speed_ms,
            "crosses_0E": bool(np.nanmin(lon[i, valid]) <= 0 <= np.nanmax(lon[i, valid])),
            "crosses_20W": bool(np.nanmin(lon[i, valid]) <= -20 <= np.nanmax(lon[i, valid])),
        }
        if strength is not None and strength.shape == lon.shape:
            vals = strength[i, valid]
            rec["max_strength_s-1"] = float(np.nanmax(vals)) if np.isfinite(vals).any() else np.nan
        records.append(rec)

    return pd.DataFrame.from_records(records)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--csv", default="outputs/aew_track_summary.csv")
    args = parser.parse_args()

    with xr.open_dataset(args.path) as ds:
        summary = summarize_dataset(ds)
    out = Path(args.csv)
    out.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(out, index=False)
    print(summary.to_string(index=False))
    print(f"\nSaved {out}")


if __name__ == "__main__":
    main()
