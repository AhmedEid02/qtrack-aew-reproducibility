#!/usr/bin/env python
"""Run the documented QTrack v0.0.4 pipeline on an official example case."""
from __future__ import annotations

from pathlib import Path
import argparse
import os

CASES = {
    "era5_2010_10day": ("era5_700_wind_global_2010_10day.nc", 2010),
    "era5_2010": ("era5_700_wind_global_2010.nc", 2010),
    "gfs_2024062612": ("analysis_and_forecast_GFS_2024062612.nc", "none"),
    "mpas_2021092400": ("mpas_30km_run_2021092400.nc", "none"),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=CASES, default="era5_2010_10day")
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--workdir", default="outputs/qtrack_run")
    args = parser.parse_args()

    try:
        import qtrack
        from qtrack.curvvort import compute_curvvort
        from qtrack.tracking import run_postprocessing, run_tracking
    except ImportError as exc:
        raise SystemExit("QTrack is not installed. Create the environment first: pip install -r requirements.txt") from exc

    work = Path(args.workdir).resolve()
    work.mkdir(parents=True, exist_ok=True)
    old_cwd = Path.cwd()
    os.chdir(work)
    try:
        input_name, real_year = CASES[args.case]
        print(f"Downloading official QTrack example: {args.case}")
        qtrack.download_examples(args.case, "")

        prepped = "adjusted_data.nc"
        curv = "curv_vort.nc"
        raw = "AEW_tracks_raw.nc"
        final_nc = "AEW_tracks_post_processed.nc"
        final_pkl = "AEW_tracks_post_processed.pkl"
        hov = "final_hovmoller.png"

        qtrack.prep_data(data_in=input_name, data_out=prepped, cut_lev_val=700)
        compute_curvvort(
            prepped,
            curv,
            radius_of_avg=600,
            data_resolution=1,
            njobs_in=args.jobs,
            nondiv_wind=False,
            run_animation=False,
        )
        run_tracking(input_file=curv, save_file=raw, run_animation=False)
        run_postprocessing(
            input_file=raw,
            curv_data_file=curv,
            real_year_used=real_year,
            TC_pairing=False,
            hovmoller_save=True,
            object_data_save=True,
            netcdf_data_save=True,
            save_obj_file=final_pkl,
            save_nc_file=final_nc,
            hov_save_file=hov,
        )
        print(f"QTrack run complete: {work / final_nc}")
    finally:
        os.chdir(old_cwd)


if __name__ == "__main__":
    main()
