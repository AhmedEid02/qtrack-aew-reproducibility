import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from make_synthetic_winds import build_dataset
from check_input_contract import validate_dataset


def test_synthetic_dataset_matches_contract():
    ds = build_dataset(days=10)
    report = validate_dataset(ds)
    assert report.timestep_hours == 6.0
    assert report.lon_resolution_deg == 1.0
    assert report.lat_resolution_deg == 1.0
    assert report.duration_days >= 10.0
