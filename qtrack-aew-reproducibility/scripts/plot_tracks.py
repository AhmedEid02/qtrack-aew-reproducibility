#!/usr/bin/env python
"""Create a compact longitude-time plot from QTrack post-processed tracks."""
from __future__ import annotations

from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--out", default="figures/aew_longitude_time.png")
    args = parser.parse_args()

    with xr.open_dataset(args.path) as ds:
        lon = np.asarray(ds["AEW_lon"].values, dtype=float)
        if "time" in ds.coords:
            try:
                y = pd.to_datetime(ds["time"].values)
                ylabel = "Time"
            except Exception:
                y = np.arange(lon.shape[1])
                ylabel = "Time index"
        else:
            y = np.arange(lon.shape[1])
            ylabel = "Time index"

    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    for i in range(lon.shape[0]):
        valid = np.isfinite(lon[i])
        if valid.any():
            ax.plot(lon[i, valid], np.asarray(y)[valid], marker="o", markersize=2, linewidth=1, label=f"AEW {i+1}")
    ax.axvline(0, linewidth=0.7)
    ax.axvline(-20, linewidth=0.7, linestyle="--")
    ax.set_xlabel("Longitude (degrees east)")
    ax.set_ylabel(ylabel)
    ax.set_title("African Easterly Wave tracks: longitude-time diagnostic")
    ax.grid(True, alpha=0.25)
    if lon.shape[0] <= 12:
        ax.legend(fontsize=7, ncol=2, loc="best")
    fig.tight_layout()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=220, bbox_inches="tight")
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
