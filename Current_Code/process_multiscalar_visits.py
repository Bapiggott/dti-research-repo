#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import csv
import json
import os
import shutil
import subprocess
import numpy as np
import nibabel as nib
import pandas as pd

FSLDIR_DEFAULT = "/home/brett/fsl"
REF_FA_DEFAULT = "/home/brett/fsl/data/standard/FMRIB58_FA_1mm.nii.gz"
AAL_ATLAS_DEFAULT = "/home/brett/atlases/AAL_MNI_2mm.nii.gz"

def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout.strip()

def ensure_fsl_env(fsldir: str):
    env = os.environ.copy()
    env["FSLDIR"] = fsldir
    env["FSLOUTPUTTYPE"] = "NIFTI_GZ"
    env["PATH"] = f"{fsldir}/bin:" + env.get("PATH", "")
    return env

def run_env(cmd: list[str], env: dict) -> str:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True, env=env)
    return result.stdout.strip()

def repair_nifti_if_needed(in_path: str, out_path: str):
    img = nib.load(in_path)
    aff = img.affine
    hdr = img.header
    zooms = np.array(hdr.get_zooms()[:3], dtype=float)

    needs_repair = (
        np.linalg.matrix_rank(aff[:3, :3]) < 3
        or np.any(~np.isfinite(aff))
        or np.any(zooms <= 0)
    )

    if not needs_repair:
        shutil.copy2(in_path, out_path)
        return False

    safe_zooms = np.where(zooms > 0, zooms, 2.0)
    new_aff = np.diag([safe_zooms[0], safe_zooms[1], safe_zooms[2], 1.0])
    new_aff[:3, 3] = -(np.array(img.shape[:3]) * safe_zooms) / 2.0

    repaired = nib.Nifti1Image(img.get_fdata(dtype=np.float32), new_aff, header=hdr)
    nib.save(repaired, out_path)
    return True

def write_identity_mat(path: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write("1 0 0 0\n0 1 0 0\n0 0 1 0\n0 0 0 1\n")

def register_to_mni(in_path: str, ref_path: str, out_path: str, mat_path: str, env: dict):
    run_env([
        "flirt",
        "-in", in_path,
        "-ref", ref_path,
        "-out", out_path,
        "-omat", mat_path,
        "-dof", "12",
    ], env)

def resample_atlas_to_grid(aal_atlas: str, ref_img: str, out_atlas: str, env: dict):
    identity_mat = str(Path(out_atlas).parent / "identity.mat")
    write_identity_mat(identity_mat)
    run_env([
        "flirt",
        "-in", aal_atlas,
        "-ref", ref_img,
        "-init", identity_mat,
        "-applyxfm",
        "-interp", "nearestneighbour",
        "-out", out_atlas,
    ], env)

def extract_roi_stats(scalar_mni: str, atlas_resampled: str, out_csv: str, scalar_name: str, n_rois: int, env: dict):
    out_dir = Path(out_csv).parent
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "roi_id",
            f"mean_{scalar_name}",
            f"std_{scalar_name}",
            f"min_{scalar_name}",
            f"max_{scalar_name}",
            "voxel_count",
        ])

        for roi_id in range(1, n_rois + 1):
            mask = out_dir / f"_mask_{scalar_name}_{roi_id}.nii.gz"

            subprocess.run([
                "fslmaths",
                atlas_resampled,
                "-thr", str(roi_id),
                "-uthr", str(roi_id),
                "-bin",
                str(mask),
            ], check=True, env=env)

            vox = run_env(["fslstats", str(mask), "-V"], env).split()
            voxel_count = int(float(vox[0])) if len(vox) > 0 else 0

            if voxel_count == 0:
                row = [roi_id, 0.0, 0.0, 0.0, 0.0, 0]
            else:
                mean_val = float(run_env(["fslstats", scalar_mni, "-k", str(mask), "-M"], env) or 0.0)
                std_val  = float(run_env(["fslstats", scalar_mni, "-k", str(mask), "-S"], env) or 0.0)
                minmax   = run_env(["fslstats", scalar_mni, "-k", str(mask), "-R"], env).split()
                min_val  = float(minmax[0]) if len(minmax) >= 2 else 0.0
                max_val  = float(minmax[1]) if len(minmax) >= 2 else 0.0
                row = [roi_id, mean_val, std_val, min_val, max_val, voxel_count]

            w.writerow(row)
            if mask.exists():
                mask.unlink()

def process_visit(row: pd.Series, out_root: Path, ref_fa: str, aal_atlas: str, env: dict, n_rois: int):
    subject_id = row["subject_id"]
    visit_date = row["visit_date"]
    visit_id = f"{subject_id}_{visit_date}"
    visit_dir = out_root / visit_id
    visit_dir.mkdir(parents=True, exist_ok=True)

    metadata = {
        "subject_id": subject_id,
        "visit_date": visit_date,
        "diagnosis": row.get("diagnosis", ""),
        "label": row.get("label", ""),
        "sex": row.get("sex", ""),
        "age": row.get("age", ""),
        "apoe4": row.get("apoe4", ""),
        "scan_date": row.get("scan_date", ""),
        "label_match_type": row.get("label_match_type", ""),
        "files": {},
    }

    scalar_paths = {
        "fa": row["fa_path"],
        "md": row["md_path"],
        "rd": row["rd_path"],
        "ad": row["ad_path"],
    }

    atlas_done = False
    atlas_resampled = visit_dir / "AAL_resampled.nii.gz"

    for scalar_name, src in scalar_paths.items():
        repaired = visit_dir / f"{scalar_name}_native_repaired.nii.gz"
        mni = visit_dir / f"{scalar_name}_mni.nii.gz"
        mat = visit_dir / f"{scalar_name}_native2mni.mat"
        out_csv = visit_dir / f"roi_{scalar_name}_stats.csv"

        was_repaired = repair_nifti_if_needed(src, str(repaired))
        register_to_mni(str(repaired), ref_fa, str(mni), str(mat), env)

        if not atlas_done:
            resample_atlas_to_grid(aal_atlas, str(mni), str(atlas_resampled), env)
            atlas_done = True

        extract_roi_stats(str(mni), str(atlas_resampled), str(out_csv), scalar_name, n_rois, env)

        metadata["files"][scalar_name] = {
            "src": src,
            "repaired": str(repaired),
            "mni": str(mni),
            "mat": str(mat),
            "roi_csv": str(out_csv),
            "was_repaired": was_repaired,
        }

    with open(visit_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-csv", required=True)
    parser.add_argument("--out-root", default="/mnt/e/adni_multiscalar_visits")
    parser.add_argument("--fsldir", default=FSLDIR_DEFAULT)
    parser.add_argument("--ref-fa", default=REF_FA_DEFAULT)
    parser.add_argument("--aal-atlas", default=AAL_ATLAS_DEFAULT)
    parser.add_argument("--n-rois", type=int, default=116)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    env = ensure_fsl_env(args.fsldir)
    out_root = Path(args.out_root)
    out_root.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.manifest_csv)
    if args.limit > 0:
        df = df.head(args.limit)

    print(f"Visits to process: {len(df)}")

    for i, row in df.iterrows():
        print(f"[{i+1}/{len(df)}] {row['subject_id']} {row['visit_date']}")
        process_visit(row, out_root, args.ref_fa, args.aal_atlas, env, args.n_rois)

    print("Done.")

if __name__ == "__main__":
    main()
