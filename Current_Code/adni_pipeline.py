#!/usr/bin/env python3
"""
=============================================================================
adni_pipeline.py
Master ADNI DTI Processing Pipeline

Discovers subjects across one or more DTI_Brett* folders, extracts FA-based
node features, and pulls diagnosis labels from XML metadata.

Usage:
  # Process specific folders
  python3 adni_pipeline.py --folders DTI_Brett6 DTI_Brett7

  # Process multiple folders
  python3 adni_pipeline.py --folders DTI_Brett DTI_Brett1 DTI_Brett2

  # Process all DTI_Brett* folders on F:\
  python3 adni_pipeline.py --all

  # Just discover subjects without processing (dry run)
  python3 adni_pipeline.py --folders DTI_Brett7 --dry-run

  # Limit parallel workers
  python3 adni_pipeline.py --folders DTI_Brett7 --jobs 4

Output goes to E:\adni_batch (same folder as before — already-processed
subjects are skipped automatically, so safe to add new folders incrementally)

Requirements:
  pip install nibabel
  FSL installed
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
import xml.etree.ElementTree as ET
import numpy as np
from pathlib import Path
from multiprocessing import Pool, cpu_count
from datetime import datetime
from collections import Counter

# =============================================================================
# CONFIGURATION — edit these if your paths differ
# =============================================================================
F_DRIVE        = "/mnt/f"
METADATA_ROOT  = "/mnt/f/DTI_Brett_metadata/ADNI/ADNI"
OUT_ROOT       = "/mnt/e/adni_batch"
AAL_ATLAS      = "/home/brett/atlases/AAL_MNI_2mm.nii.gz"
FSL_HOME       = "/home/brett/fsl"
N_ROIS         = 116
FA_FOLDER      = "Native_Space_Fractional_Anisotropy_Image"

LABEL_MAP = {
    "CN":   0,
    "SMC":  0,
    "EMCI": 1,
    "MCI":  1,
    "LMCI": 1,
    "AD":   2,
}


# =============================================================================
# DISCOVERY
# =============================================================================
def discover_subjects(folders: list[str]) -> dict:
    """
    Scan specified DTI_Brett* folders for subjects with FA data.
    Returns dict: subject_id -> fa_nii_path
    Handles subjects appearing in multiple folders (keeps first found).
    """
    found = {}
    skipped_dup = []

    for folder_name in folders:
        # Support both "DTI_Brett6" and full paths
        if folder_name.startswith("/"):
            adni_root = Path(folder_name) / "ADNI" / "ADNI"
        else:
            adni_root = Path(F_DRIVE) / folder_name / "ADNI" / "ADNI"

        if not adni_root.exists():
            logging.warning(f"  Folder not found: {adni_root}")
            continue

        subj_dirs = [d for d in adni_root.iterdir() if d.is_dir()]
        folder_count = 0

        for subj_dir in subj_dirs:
            subj_id = subj_dir.name
            fa_matches = sorted((subj_dir / FA_FOLDER).glob("**/*.nii")
                                if (subj_dir / FA_FOLDER).exists() else [])
            if not fa_matches:
                continue

            if subj_id in found:
                skipped_dup.append(subj_id)
                continue

            found[subj_id] = fa_matches[0]
            folder_count += 1

        logging.info(f"  {folder_name}: {folder_count} new subjects with FA")

    if skipped_dup:
        logging.info(f"  Skipped {len(skipped_dup)} duplicates across folders")

    return found


# =============================================================================
# FSL / NIBABEL HELPERS  (same as run_adni_extraction.py)
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
    r = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True)
    val = r.stdout.strip()
    return float(val) if val else 0.0


def fslstats_int(cmd, env):
    r = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True)
    val = r.stdout.strip().split()[0] if r.stdout.strip() else "0"
    try:
        return int(float(val))
    except ValueError:
        return 0


def repair_header(nii_path: Path, logf) -> bool:
    import nibabel as nib
    img = nib.load(str(nii_path))
    hdr = img.header
    affine = img.affine
    sform_code = int(hdr.get_sform(coded=True)[1])
    rank = np.linalg.matrix_rank(affine[:3, :3])
    zooms = np.array(hdr.get_zooms()[:3], dtype=float)

    needs_repair = (
        rank < 3 or sform_code == 0
        or np.any(zooms <= 0) or np.any(~np.isfinite(affine))
    )
    if not needs_repair:
        return False

    safe_zooms = np.where(zooms > 0, zooms, 2.0)
    new_affine = np.diag(list(safe_zooms) + [1.0]).astype(float)
    new_affine[:3, 3] = -(np.array(img.shape[:3]) * safe_zooms) / 2.0
    fixed = nib.Nifti1Image(np.asarray(img.dataobj), new_affine)
    fixed.header.set_sform(new_affine, code=1)
    fixed.header.set_qform(new_affine, code=1)
    fixed.header.set_zooms(safe_zooms)
    nib.save(fixed, str(nii_path))
    logf.write(f"    Header repaired (rank was {rank})\n")
    return True


# =============================================================================
# FA EXTRACTION  (same logic as run_adni_extraction.py)
# =============================================================================
def process_subject(args: tuple) -> dict:
    subj_id, fa_src_str = args
    fa_src   = Path(fa_src_str)
    out_dir  = Path(OUT_ROOT) / subj_id
    log_path = Path(OUT_ROOT) / "logs" / f"{subj_id}.log"
    result   = {"subj": subj_id, "status": "unknown", "error": None}

    if (out_dir / "node_features.csv").exists():
        result["status"] = "skipped"
        return result

    out_dir.mkdir(parents=True, exist_ok=True)
    env = fsl_env()
    ref = Path(env["FSLDIR"]) / "data/standard/FMRIB58_FA_1mm.nii.gz"

    with open(log_path, "w") as logf:
        logf.write(f"=== {subj_id} ===\n")
        logf.write(f"FA source: {fa_src}\n\n")
        try:
            # Copy + repair header
            fa_native = out_dir / "FA_native.nii"
            shutil.copy(fa_src, fa_native)
            repair_header(fa_native, logf)

            # Register FA → FMRIB58_FA
            fa_mni  = out_dir / "FA_MNI.nii.gz"
            xfm_mat = out_dir / "native2mni.mat"
            run(f"flirt -in {fa_native} -ref {ref} "
                f"-out {fa_mni} -omat {xfm_mat} -dof 12", env, logf)
            fa_native.unlink()
            if not fa_mni.exists():
                raise RuntimeError("flirt failed")
            xfm_mat.unlink()

            # Resample AAL to FA_MNI grid
            ident = out_dir / "identity.mat"
            ident.write_text("1 0 0 0\n0 1 0 0\n0 0 1 0\n0 0 0 1\n")
            atlas_resampled = out_dir / "AAL_mni_resampled.nii.gz"
            run(f"flirt -in {AAL_ATLAS} -ref {fa_mni} "
                f"-init {ident} -applyxfm "
                f"-interp nearestneighbour -out {atlas_resampled}", env, logf)
            ident.unlink()
            if not atlas_resampled.exists():
                raise RuntimeError("Atlas resampling failed")

            # Per-ROI extraction
            roi_rows = []
            for roi_id in range(1, N_ROIS + 1):
                mask = out_dir / f"_mask_{roi_id}.nii.gz"
                try:
                    run(f"fslmaths {atlas_resampled} "
                        f"-thr {roi_id} -uthr {roi_id} -bin {mask}", env, logf)
                    vox = fslstats_int(f"fslstats {mask} -V", env)
                    mean_fa = (fslstats_scalar(
                        f"fslstats {fa_mni} -k {mask} -M", env)
                        if vox > 0 else 0.0)
                except Exception:
                    mean_fa, vox = 0.0, 0
                finally:
                    if mask.exists():
                        mask.unlink()
                roi_rows.append((roi_id, mean_fa, vox))

            fa_mni.unlink()

            # Write outputs
            with open(out_dir / "roi_fa_stats.csv", "w", newline="") as f:
                csv.writer(f).writerows(
                    [["roi_id", "mean_fa", "voxel_count"]] + list(roi_rows))

            with open(out_dir / "node_features.csv", "w", newline="") as f:
                csv.writer(f).writerows(
                    [["roi_id", "mean_fa"]] + [(r[0], r[1]) for r in roi_rows])

            logf.write("\n    SUCCESS\n")
            result["status"] = "done"

        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            logf.write(f"\nFAILED: {e}\n{traceback.format_exc()}\n")
            for f in out_dir.glob("*.nii.gz"):
                f.unlink(missing_ok=True)
            for f in out_dir.glob("*_native.nii"):
                f.unlink(missing_ok=True)
            for f in out_dir.glob("*.mat"):
                f.unlink(missing_ok=True)

    return result


# =============================================================================
# LABEL EXTRACTION
# =============================================================================
def parse_xml(xml_path: Path) -> dict:
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        # Namespace sits on <project> child, not root — scan all elements
        ns = ""
        for el in root.iter():
            if el.tag.startswith("{"):
                ns = el.tag.split("}")[0] + "}"
                break

        def find(tag):
            el = root.find(f".//{ns}{tag}")
            if el is None:
                el = root.find(f".//{tag}")
            return el.text.strip() if el is not None and el.text else None

        apoe = {}
        for info in list(root.iter(f"{ns}subjectInfo")) + list(root.iter("subjectInfo")):
            item = info.get("item", "")
            if "APOE" in item and info.text:
                apoe[item] = info.text.strip()

        a1, a2 = apoe.get("APOE A1", ""), apoe.get("APOE A2", "")
        apoe4 = 1 if ("4" in a1 or "4" in a2) else 0

        date_str = find("dateAcquired")
        date_obj = None
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                pass

        return {
            "diagnosis": find("researchGroup"),
            "sex":       find("subjectSex"),
            "age":       find("subjectAge"),
            "apoe4":     apoe4,
            "scan_date": date_str,
            "date_obj":  date_obj,
        }
    except Exception:
        return {}


def get_fa_scan_date(subj_id: str, fa_src: Path) -> datetime | None:
    # FA path: .../Native_Space_FA/<date>_HH_MM_SS.0/<ID>/<file>.nii
    try:
        date_str = fa_src.parts[-3].split("_")[0]
        return datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, IndexError):
        return None


def extract_labels(subjects: dict) -> list:
    """Extract labels for all subjects from loose XMLs in METADATA_ROOT.
    Note: per-subject subfolder XMLs are stubs with no clinical data.
    The real data is in loose files named ADNI_{subj_id}_*.xml at root level.
    """
    rows = []
    no_dx, unknown_dx = [], []

    for subj_id, fa_src in subjects.items():
        # Only look at loose XMLs — subfolder ones have no diagnosis
        xmls = sorted(Path(METADATA_ROOT).glob(f"ADNI_{subj_id}_*.xml"))

        if not xmls:
            no_dx.append(subj_id)
            continue

        parsed = [parse_xml(x) for x in xmls]
        parsed = [p for p in parsed if p.get("diagnosis")]
        if not parsed:
            no_dx.append(subj_id)
            continue

        fa_date = get_fa_scan_date(subj_id, fa_src)
        if fa_date:
            with_date = [p for p in parsed if p.get("date_obj")]
            best = (min(with_date,
                        key=lambda p: abs((p["date_obj"] - fa_date).days))
                    if with_date else parsed[-1])
        else:
            best = parsed[-1]

        dx = best["diagnosis"].upper().strip()
        label = LABEL_MAP.get(dx)
        if label is None:
            unknown_dx.append((subj_id, dx))
            label = -1

        rows.append({
            "subject_id": subj_id,
            "diagnosis":  dx,
            "label":      label,
            "sex":        best.get("sex", ""),
            "age":        best.get("age", ""),
            "apoe4":      best.get("apoe4", ""),
            "scan_date":  best.get("scan_date", ""),
        })

    if no_dx:
        logging.warning(f"  No diagnosis found for {len(no_dx)} subjects: "
                        f"{no_dx[:3]}{'...' if len(no_dx)>3 else ''}")
    if unknown_dx:
        logging.warning(f"  Unknown diagnosis codes: {unknown_dx[:5]}")

    return rows


# =============================================================================
# MAIN
# =============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="ADNI DTI Pipeline — discover, extract FA, get labels",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 adni_pipeline.py --folders DTI_Brett6 DTI_Brett7
  python3 adni_pipeline.py --all
  python3 adni_pipeline.py --folders DTI_Brett7 --dry-run
  python3 adni_pipeline.py --folders DTI_Brett7 --jobs 4
        """
    )
    parser.add_argument("--folders", nargs="+",
                        help="DTI_Brett* folder names to process (e.g. DTI_Brett6 DTI_Brett7)")
    parser.add_argument("--all", action="store_true",
                        help="Process all DTI_Brett* folders on F:\\")
    parser.add_argument("--jobs", type=int, default=cpu_count(),
                        help="Parallel workers (default: all cores)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Discover subjects only, do not process")
    parser.add_argument("--labels-only", action="store_true",
                        help="Skip FA extraction, only update labels.csv")
    args = parser.parse_args()

    if not args.folders and not args.all:
        parser.error("Specify --folders or --all")

    # Setup logging
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
        log.error("nibabel not installed. Run: pip install nibabel")
        sys.exit(1)

    # Determine folders to process
    if args.all:
        folders = sorted(
            d.name for d in Path(F_DRIVE).iterdir()
            if d.is_dir() and d.name.startswith("DTI_Brett")
            and "metadata" not in d.name.lower()
        )
        log.info(f"Found DTI_Brett folders: {folders}")
    else:
        folders = args.folders

    log.info("=" * 60)
    log.info("  ADNI DTI Pipeline")
    log.info(f"  Folders:  {folders}")
    log.info(f"  Workers:  {args.jobs} / {cpu_count()} cores")
    log.info(f"  Output:   {OUT_ROOT}")
    log.info("=" * 60)

    # Discover subjects
    log.info("Discovering subjects...")
    subjects = discover_subjects(folders)
    total = len(subjects)

    already_done = sum(
        1 for s in subjects
        if (Path(OUT_ROOT) / s / "node_features.csv").exists()
    )
    to_process = total - already_done

    log.info(f"  Found:         {total} subjects with FA data")
    log.info(f"  Already done:  {already_done} (will skip)")
    log.info(f"  To process:    {to_process}")

    if args.dry_run:
        log.info("\nDry run — subject list:")
        for s in sorted(subjects.keys()):
            status = "DONE" if (Path(OUT_ROOT) / s / "node_features.csv").exists() else "TODO"
            log.info(f"  [{status}] {s}")
        return

    # FA extraction
    if not args.labels_only and to_process > 0:
        log.info(f"\nRunning FA extraction on {to_process} subjects...")
        args_list = [(s, str(p)) for s, p in subjects.items()]
        counts = Counter()

        with Pool(processes=args.jobs) as pool:
            for i, res in enumerate(
                pool.imap_unordered(process_subject, args_list), 1
            ):
                s = res["status"]
                counts[s] += 1
                n_done = sum(1 for _ in Path(OUT_ROOT).glob("*/node_features.csv"))

                if s == "done":
                    log.info(f"[{i:>4}/{total}] DONE    {res['subj']}  "
                             f"total_done={n_done}")
                elif s == "failed":
                    log.warning(f"[{i:>4}/{total}] FAILED  {res['subj']}  "
                                f"{str(res['error'])[:80]}")

        log.info(f"\n  Done: {counts['done']}  "
                 f"Skipped: {counts['skipped']}  "
                 f"Failed: {counts['failed']}")
    elif to_process == 0:
        log.info("  All subjects already processed — skipping extraction")

    # Label extraction
    log.info("\nExtracting labels from XML metadata...")

    # Merge with any existing labels
    labels_path = Path(OUT_ROOT) / "labels.csv"
    existing_labels = {}
    if labels_path.exists():
        with open(labels_path) as f:
            for row in csv.DictReader(f):
                existing_labels[row["subject_id"]] = row

    new_labels = extract_labels(subjects)
    new_labels_dict = {r["subject_id"]: r for r in new_labels}

    # Merge: new labels override existing for same subject
    merged = {**existing_labels, **new_labels_dict}

    fieldnames = ["subject_id", "diagnosis", "label", "sex", "age",
                  "apoe4", "scan_date"]
    with open(labels_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(merged.values())

    # Final summary
    label_counts = Counter(r["label"] for r in merged.values())
    dx_counts    = Counter(r["diagnosis"] for r in merged.values())
    n_final = sum(1 for _ in Path(OUT_ROOT).glob("*/node_features.csv"))

    log.info(f"\n{'='*60}")
    log.info(f"  Pipeline complete")
    log.info(f"  Subjects with node_features.csv: {n_final}")
    log.info(f"  Subjects with labels:            {len(merged)}")
    log.info(f"\n  Diagnosis breakdown:")
    for dx, count in sorted(dx_counts.items()):
        lbl = LABEL_MAP.get(dx, -1)
        log.info(f"    {dx:6s} (label={lbl}): {count:>4}")
    log.info(f"\n  Grouped labels:")
    label_names = {0: "CN/SMC", 1: "MCI", 2: "AD", -1: "UNKNOWN"}
    for lbl in sorted(label_counts):
        log.info(f"    label={lbl} {label_names.get(lbl,'?'):8s}: "
                 f"{label_counts[lbl]:>4}")
    log.info(f"\n  labels.csv → {labels_path}")
    log.info(f"{'='*60}")


if __name__ == "__main__":
    main()
