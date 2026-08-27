import sys
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from summarize_tracks import summarize_dataset


def make_tracks():
    time = pd.date_range("2010-09-01", periods=9, freq="6h")
    lon = np.array([[10, 5, 0, -5, -10, -15, -20, -25, -30], [np.nan, 25, 20, 15, 10, 5, 0, -5, np.nan]], dtype=float)
    lat = np.array([[12, 12, 13, 13, 14, 14, 15, 15, 16], [np.nan, 10, 10, 11, 11, 12, 12, 13, np.nan]], dtype=float)
    strength = np.where(np.isfinite(lon), 3e-6, np.nan)
    return xr.Dataset(
        {
            "AEW_lon": (("system", "time"), lon),
            "AEW_lat": (("system", "time"), lat),
            "AEW_strength": (("system", "time"), strength),
        },
        coords={"system": [1, 2], "time": time},
    )


def test_summary_metrics():
    df = summarize_dataset(make_tracks())
    assert len(df) == 2
    assert bool(df.loc[0, "crosses_0E"])
    assert bool(df.loc[0, "crosses_20W"])
    assert df.loc[0, "westward_displacement_deg"] == 40
    assert df.loc[0, "duration_days"] == 2.0
    assert np.isclose(df.loc[0, "max_strength_s-1"], 3e-6)
