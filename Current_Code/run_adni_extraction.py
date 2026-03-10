#!/usr/bin/env python3
"""
=============================================================================
run_adni_extraction.py
ADNI FA Feature Extraction Pipeline

Extracts per-ROI mean FA for all 443 ADNI subjects that have a pre-computed
Native_Space_Fractional_Anisotropy_Image NIfTI file.

Pipeline per subject:
  1. Find FA .nii on F:\
  2. Repair NIfTI header if degenerate (nibabel)
  3. Register FA → FMRIB58_FA_1mm (flirt affine, in MNI space)
  4. Resample AAL116 atlas to match registered FA (identity xfm, nn interp)
  5. Extract mean FA per ROI (116 ROIs)
  6. Save node_features.csv
  7. Clean up all intermediates

Output per subject: /mnt/e/adni_batch/<subj_id>/
  node_features.csv        — 116 rows: roi_id, mean_fa
  roi_fa_stats.csv         — 116 rows: roi_id, mean_fa, voxel_count
  AAL_mni_resampled.nii.gz — atlas in registered space (kept for QC)

Usage:
  python3 run_adni_extraction.py
  python3 run_adni_extraction.py --jobs 4
  python3 run_adni_extraction.py --jobs 4 --list /path/to/subjects.txt

Requirements:
  pip install nibabel
  FSL installed, FSLDIR set (or edit FSL_HOME below)
=============================================================================
"""

import os
import sys
import csv
import shutil
import logging
import argparse
import subprocess
import traceback
import numpy as np
from pathlib import Path
from multiprocessing import Pool, cpu_count

# =============================================================================
# CONFIGURATION
# =============================================================================
ADNI_ROOT  = "/mnt/f/DTI_Brett6/ADNI/ADNI"
OUT_ROOT   = "/mnt/e/adni_batch"
AAL_ATLAS  = "/home/brett/atlases/AAL_MNI_2mm.nii.gz"
FSL_HOME   = "/home/brett/fsl"
SUBJ_LIST  = "/tmp/fa_subjects.txt"
N_ROIS     = 116
FA_FOLDER  = "Native_Space_Fractional_Anisotropy_Image"


# =============================================================================
# HELPERS
# =============================================================================
def fsl_env():
    env = os.environ.copy()
    if "FSLDIR" not in env:
        env["FSLDIR"] = FSL_HOME
    env["PATH"] = f"{env['FSLDIR']}/bin:{env.get('PATH','')}"
    env["FSLOUTPUTTYPE"] = "NIFTI_GZ"
    return env


def run(cmd, env, logf=None):
    r = subprocess.run(cmd, shell=True, env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if logf:
        logf.write(f"$ {cmd}\n{r.stdout}\n")
    if r.returncode != 0:
        raise RuntimeError(f"Command failed:\n{cmd}\n{r.stdout.strip()}")
    return r.stdout.strip()


def fslstats_scalar(cmd, env):
    r = subprocess.run(cmd, shell=True, env=env,
                       capture_output=True, text=True)
    val = r.stdout.strip()
    return float(val) if val else 0.0


def fslstats_int(cmd, env):
    r = subprocess.run(cmd, shell=True, env=env,
                       capture_output=True, text=True)
    val = r.stdout.strip().split()[0] if r.stdout.strip() else "0"
    try:
        return int(float(val))
    except ValueError:
        return 0


# =============================================================================
# HEADER REPAIR
# =============================================================================
def repair_header(nii_path: Path, logf) -> bool:
    """
    Check NIfTI sform/qform. If the affine is degenerate (rank < 3, zero
    sform code, or non-finite values), rebuild it from pixdim.
    This is the root cause of flirt/fnirt 'matrix is singular' errors on
    some ADNI DICOM-converted images.
    """
    import nibabel as nib

    img = nib.load(str(nii_path))
    hdr = img.header
    affine = img.affine
    sform_code = int(hdr.get_sform(coded=True)[1])
    rank = np.linalg.matrix_rank(affine[:3, :3])
    zooms = np.array(hdr.get_zooms()[:3], dtype=float)

    needs_repair = (
        rank < 3
        or sform_code == 0
        or np.any(zooms <= 0)
        or np.any(~np.isfinite(affine))
    )

    if not needs_repair:
        logf.write("    Header OK (rank=3, sform valid)\n")
        return False

    logf.write(f"    Header REPAIR needed: rank={rank}, sform_code={sform_code}, zooms={zooms}\n")

    safe_zooms = np.where(zooms > 0, zooms, 2.0)
    new_affine = np.diag(list(safe_zooms) + [1.0]).astype(float)
    # Center the image at MNI origin
    new_affine[:3, 3] = -(np.array(img.shape[:3]) * safe_zooms) / 2.0

    fixed = nib.Nifti1Image(np.asarray(img.dataobj), new_affine)
    fixed.header.set_sform(new_affine, code=1)
    fixed.header.set_qform(new_affine, code=1)
    fixed.header.set_zooms(safe_zooms)
    nib.save(fixed, str(nii_path))
    return True


# =============================================================================
# PER-SUBJECT PIPELINE
# =============================================================================
def process_subject(subj_id: str) -> dict:
    out_dir  = Path(OUT_ROOT) / subj_id
    log_path = Path(OUT_ROOT) / "logs" / f"{subj_id}.log"
    result   = {"subj": subj_id, "status": "unknown", "error": None}

    # Already done — skip
    if (out_dir / "node_features.csv").exists():
        result["status"] = "skipped"
        return result

    # Find FA NIfTI
    fa_matches = sorted(Path(ADNI_ROOT).glob(f"{subj_id}/{FA_FOLDER}/**/*.nii"))
    if not fa_matches:
        result["status"] = "skipped_no_fa"
        return result

    fa_src = fa_matches[0]
    out_dir.mkdir(parents=True, exist_ok=True)
    env = fsl_env()
    ref = Path(env["FSLDIR"]) / "data/standard/FMRIB58_FA_1mm.nii.gz"

    with open(log_path, "w") as logf:
        logf.write(f"=== {subj_id} ===\n")
        logf.write(f"FA source: {fa_src}\n\n")

        try:
            # ── STEP 1: Copy FA to working dir ────────────────────────────────
            fa_native = out_dir / "FA_native.nii"
            shutil.copy(fa_src, fa_native)

            # ── STEP 2: Repair NIfTI header ───────────────────────────────────
            repaired = repair_header(fa_native, logf)
            logf.write(f"    Header repaired: {repaired}\n\n")

            # ── STEP 3: Register FA → FMRIB58_FA (affine) ────────────────────
            fa_mni  = out_dir / "FA_MNI.nii.gz"
            xfm_mat = out_dir / "native2mni.mat"
            run(f"flirt -in {fa_native} -ref {ref} "
                f"-out {fa_mni} -omat {xfm_mat} -dof 12",
                env, logf)
            fa_native.unlink()  # delete native copy

            if not fa_mni.exists():
                raise RuntimeError("flirt failed — FA_MNI.nii.gz not created")
            xfm_mat.unlink()    # transform not needed further
            logf.write("    Registration done\n\n")

            # ── STEP 4: Resample AAL116 to match FA_MNI ───────────────────────
            # Both are now in MNI space — just resample to same grid
            ident = out_dir / "identity.mat"
            ident.write_text("1 0 0 0\n0 1 0 0\n0 0 1 0\n0 0 0 1\n")

            atlas_resampled = out_dir / "AAL_mni_resampled.nii.gz"
            run(f"flirt -in {AAL_ATLAS} -ref {fa_mni} "
                f"-init {ident} -applyxfm "
                f"-interp nearestneighbour -out {atlas_resampled}",
                env, logf)
            ident.unlink()

            if not atlas_resampled.exists():
                raise RuntimeError("Atlas resampling failed")
            logf.write("    Atlas resampled\n\n")

            # ── STEP 5: Per-ROI mean FA extraction ────────────────────────────
            logf.write("    Extracting ROI stats...\n")
            roi_rows = []

            for roi_id in range(1, N_ROIS + 1):
                mask = out_dir / f"_mask_{roi_id}.nii.gz"
                try:
                    run(f"fslmaths {atlas_resampled} "
                        f"-thr {roi_id} -uthr {roi_id} -bin {mask}",
                        env, logf)
                    vox = fslstats_int(
                        f"fslstats {mask} -V", env)
                    mean_fa = (
                        fslstats_scalar(
                            f"fslstats {fa_mni} -k {mask} -M", env)
                        if vox > 0 else 0.0
                    )
                except Exception as e:
                    mean_fa = 0.0
                    vox = 0
                    logf.write(f"      ROI {roi_id} failed: {e}\n")
                finally:
                    if mask.exists():
                        mask.unlink()

                roi_rows.append((roi_id, mean_fa, vox))

            # Delete registered FA — no longer needed
            fa_mni.unlink()

            # ── STEP 6: Write outputs ─────────────────────────────────────────
            with open(out_dir / "roi_fa_stats.csv", "w", newline="") as f:
                csv.writer(f).writerows(
                    [["roi_id", "mean_fa", "voxel_count"]] + list(roi_rows)
                )

            with open(out_dir / "node_features.csv", "w", newline="") as f:
                csv.writer(f).writerows(
                    [["roi_id", "mean_fa"]] +
                    [(r[0], r[1]) for r in roi_rows]
                )

            logf.write(f"\n    SUCCESS\n")
            result["status"] = "done"

        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            logf.write(f"\nFAILED: {e}\n{traceback.format_exc()}\n")
            # Clean up partial outputs so reruns start fresh
            for f in out_dir.glob("*.nii.gz"):
                f.unlink(missing_ok=True)
            for f in out_dir.glob("*_native.nii"):
                f.unlink(missing_ok=True)
            for f in out_dir.glob("*.mat"):
                f.unlink(missing_ok=True)

    return result


# =============================================================================
# MAIN
# =============================================================================
def main():
    parser = argparse.ArgumentParser(description="ADNI FA Extraction")
    parser.add_argument("--jobs", type=int, default=cpu_count(),
                        help="Parallel workers (default: all cores)")
    parser.add_argument("--list", type=str, default=SUBJ_LIST,
                        help="Subject list text file")
    args = parser.parse_args()

    # Logging
    log_dir = Path(OUT_ROOT) / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / "pipeline_main.log"),
        ],
    )
    log = logging.getLogger()

    # Check nibabel
    try:
        import nibabel
    except ImportError:
        log.error("nibabel not installed. Run:  pip install nibabel")
        sys.exit(1)

    # Load subject list
    subj_path = Path(args.list)
    if not subj_path.exists():
        log.error(f"Subject list not found: {subj_path}")
        sys.exit(1)

    subjects = [l.strip() for l in subj_path.read_text().splitlines() if l.strip()]
    total = len(subjects)
    already = sum(1 for s in subjects
                  if (Path(OUT_ROOT) / s / "node_features.csv").exists())

    log.info("=" * 55)
    log.info("  ADNI FA Extraction — FA only, consistent 116-node graphs")
    log.info(f"  Subjects:      {total}")
    log.info(f"  Already done:  {already}  (will be skipped)")
    log.info(f"  To process:    {total - already}")
    log.info(f"  Workers:       {args.jobs} / {cpu_count()} cores")
    log.info(f"  Registration:  flirt affine → FMRIB58_FA_1mm")
    log.info(f"  Atlas:         AAL116 in MNI space")
    log.info(f"  Output:        {OUT_ROOT}")
    log.info("=" * 55)

    counts = {"done": 0, "skipped": 0, "skipped_no_fa": 0, "failed": 0}

    with Pool(processes=args.jobs) as pool:
        for i, res in enumerate(pool.imap_unordered(process_subject, subjects), 1):
            s = res["status"]
            counts[s] = counts.get(s, 0) + 1
            n_done = sum(1 for _ in Path(OUT_ROOT).glob("*/node_features.csv"))

            if s == "done":
                log.info(f"[{i:>4}/{total}] DONE    {res['subj']}   total_done={n_done}")
            elif s == "failed":
                log.warning(f"[{i:>4}/{total}] FAILED  {res['subj']}   {str(res['error'])[:100]}")
            elif s == "skipped_no_fa":
                log.info(f"[{i:>4}/{total}] NO_FA   {res['subj']}")
            # skipped = already done, silent

    n_final = sum(1 for _ in Path(OUT_ROOT).glob("*/node_features.csv"))
    log.info("")
    log.info("=" * 55)
    log.info(f"  Done this run:   {counts.get('done',0)}")
    log.info(f"  Already done:    {counts.get('skipped',0)}")
    log.info(f"  No FA data:      {counts.get('skipped_no_fa',0)}")
    log.info(f"  Failed:          {counts.get('failed',0)}")
    log.info(f"  Total complete:  {n_final} / {total}")
    log.info("=" * 55)


if __name__ == "__main__":
    main()
