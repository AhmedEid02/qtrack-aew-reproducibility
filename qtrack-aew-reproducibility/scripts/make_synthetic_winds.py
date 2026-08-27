#!/usr/bin/env python
"""Create a small synthetic 700-hPa wind dataset matching QTrack's input contract.

The data are intentionally synthetic and are only for validating repository plumbing.
They must not be interpreted as an observed or simulated African Easterly Wave.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import xarray as xr


def build_dataset(days: int = 10) -> xr.Dataset:
    time = pd.date_range("2010-09-01", periods=days * 4 + 1, freq="6h")
    lat = np.arange(30.0, -1.0, -1.0)      # descending, consistent with many reanalysis files
    lon = np.arange(-80.0, 41.0, 1.0)

    tt = np.arange(len(time), dtype=float)[:, None, None]
    yy = lat[None, :, None]
    xx = lon[None, None, :]

    # A weak westward-moving perturbation superimposed on a simple easterly jet-like flow.
    center_lon = 20.0 - 1.7 * tt
    center_lat = 12.0 + 1.5 * np.sin(tt / 8.0)
    r2 = ((xx - center_lon) / 8.0) ** 2 + ((yy - center_lat) / 4.0) ** 2
    perturb = np.exp(-0.5 * r2)

    u = -8.0 - 3.0 * np.exp(-0.5 * ((yy - 14.0) / 5.0) ** 2) + 1.2 * perturb
    v = 2.0 * ((yy - center_lat) / 4.0) * perturb

    # Broadcast both fields to identical (time, latitude, longitude) dimensions.
    u = np.broadcast_to(u, (len(time), len(lat), len(lon))).copy()
    v = np.broadcast_to(v, (len(time), len(lat), len(lon))).copy()

    ds = xr.Dataset(
        data_vars={
            "u": (("time", "latitude", "longitude"), u.astype("float32"), {"units": "m s-1", "long_name": "zonal wind at 700 hPa"}),
            "v": (("time", "latitude", "longitude"), v.astype("float32"), {"units": "m s-1", "long_name": "meridional wind at 700 hPa"}),
        },
        coords={"time": time, "latitude": lat, "longitude": lon},
        attrs={
            "title": "Synthetic 700-hPa wind field for QTrack input-contract testing",
            "warning": "Synthetic software-validation data only; not meteorological evidence.",
            "pressure_level_hpa": 700,
        },
    )
    return ds


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="data/synthetic_700hpa_winds.nc")
    parser.add_argument("--days", type=int, default=10)
    args = parser.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    ds = build_dataset(args.days)
    # scipy backend writes NetCDF3 and keeps the lightweight test environment dependency-free.
    ds.to_netcdf(out, engine="scipy")
    print(f"Wrote {out} | dims={dict(ds.sizes)}")


if __name__ == "__main__":
    main()
