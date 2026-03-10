#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional
import argparse
import csv
import re
import xml.etree.ElementTree as ET
import pandas as pd

DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")

ADNI_ROOTS_DEFAULT = [
    "/mnt/f/DTI_Brett6/ADNI/ADNI",
    "/mnt/e/DTI__Brett2/ADNI/ADNI",
    "/mnt/e/DTI__Brett3/ADNI/ADNI",
    "/mnt/f/DTI__Brett/ADNI/ADNI",
    "/mnt/f/DTI_Brett4/ADNI",
    "/mnt/f/DTI_Brett5/ADNI/ADNI",
    "/mnt/f/DTI_Brett7/ADNI/ADNI",
    "/mnt/f/DTI_Brett8/ADNI/ADNI",
    "/mnt/f/DTI_Brett9/ADNI/ADNI",
]

SCALAR_DIRS = {
    "FA": "Native_Space_Fractional_Anisotropy_Image",
    "MD": "Native_Space_Mean_Diffusivity_Image",
    "RD": "Native_Space_Radial_Diffusivity_Image",
    "AD": "Native_Space_Axial_Diffusivity_Image",
}

DIAG_TO_LABEL = {
    "CN": 0,
    "SMC": 0,
    "EMCI": 1,
    "MCI": 1,
    "LMCI": 1,
    "AD": 2,
}

@dataclass
class FileRec:
    subject_id: str
    visit_date: str
    scalar: str
    root: str
    nifti_path: str
    date_dir: str
    file_size: int

def parse_visit_date(name: str) -> Optional[str]:
    m = DATE_RE.match(name)
    return m.group(1) if m else None

def list_niftis(folder: Path):
    return list(folder.rglob("*.nii")) + list(folder.rglob("*.nii.gz"))

def choose_best_file(recs: list[FileRec], root_priority: list[str] | None = None) -> FileRec:
    priority_map = {}
    if root_priority:
        priority_map = {root: i for i, root in enumerate(root_priority)}

    def key(r: FileRec):
        root_rank = priority_map.get(r.root, 10**9)
        return (root_rank, -r.file_size, r.nifti_path)

    return sorted(recs, key=key)[0]

def discover_records(adni_roots: list[str]) -> list[FileRec]:
    records = []

    for root_str in adni_roots:
        root = Path(root_str)
        if not root.exists():
            print(f"Skipping missing root: {root}")
            continue

        for subj_dir in root.iterdir():
            if not subj_dir.is_dir():
                continue
            subject_id = subj_dir.name

            for scalar, scalar_dirname in SCALAR_DIRS.items():
                scalar_dir = subj_dir / scalar_dirname
                if not scalar_dir.exists() or not scalar_dir.is_dir():
                    continue

                for date_dir in scalar_dir.iterdir():
                    if not date_dir.is_dir():
                        continue
                    visit_date = parse_visit_date(date_dir.name)
                    if visit_date is None:
                        continue

                    niftis = list_niftis(date_dir)
                    for nifti in niftis:
                        try:
                            size = nifti.stat().st_size
                        except OSError:
                            size = 0

                        records.append(FileRec(
                            subject_id=subject_id,
                            visit_date=visit_date,
                            scalar=scalar,
                            root=str(root),
                            nifti_path=str(nifti),
                            date_dir=str(date_dir),
                            file_size=size,
                        ))
    return records

def safe_text(elem):
    return elem.text.strip() if elem is not None and elem.text else ""

def strip_ns(tag: str) -> str:
    return tag.split("}", 1)[-1]

def find_first_by_localname(root, localname):
    for elem in root.iter():
        if strip_ns(elem.tag) == localname:
            return elem
    return None

def find_all_by_localname(root, localname):
    out = []
    for elem in root.iter():
        if strip_ns(elem.tag) == localname:
            out.append(elem)
    return out

def parse_xml_label(xml_path: Path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except Exception:
        return None

    subj_elem = find_first_by_localname(root, "subjectIdentifier")
    diag_elem = find_first_by_localname(root, "researchGroup")
    sex_elem = find_first_by_localname(root, "subjectSex")
    age_elem = find_first_by_localname(root, "subjectAge")
    date_elem = find_first_by_localname(root, "dateAcquired")

    apoe_vals = []
    for elem in find_all_by_localname(root, "subjectInfo"):
        item = elem.attrib.get("item", "").strip().upper()
        if item in {"APOE A1", "APOE A2"}:
            apoe_vals.append(safe_text(elem))

    subject_id = safe_text(subj_elem)
    diagnosis = safe_text(diag_elem).upper()
    sex = safe_text(sex_elem).upper()
    age = safe_text(age_elem)
    scan_date = safe_text(date_elem)

    if not subject_id or not diagnosis or not scan_date:
        return None

    apoe4 = 1 if "4" in apoe_vals else 0
    label = DIAG_TO_LABEL.get(diagnosis, -1)

    return {
        "subject_id": subject_id,
        "diagnosis": diagnosis,
        "label": label,
        "sex": sex,
        "age": age,
        "apoe4": apoe4,
        "scan_date": scan_date,
        "xml_path": str(xml_path),
    }

def match_label_from_raw_xml(meta_root: Path, subject_id: str, visit_date: str, max_days: int = 365):
    xmls = sorted(meta_root.glob(f"ADNI_{subject_id}_*.xml"))
    if not xmls:
        return None

    try:
        visit_dt = pd.to_datetime(visit_date)
    except Exception:
        return None

    parsed = []
    for xml_path in xmls:
        info = parse_xml_label(xml_path)
        if info is None:
            continue
        if info["subject_id"] != subject_id:
            continue
        try:
            scan_dt = pd.to_datetime(info["scan_date"])
        except Exception:
            continue
        info["label_day_diff"] = abs((scan_dt - visit_dt).days)
        parsed.append(info)

    if not parsed:
        return None

    parsed = sorted(parsed, key=lambda x: x["label_day_diff"])
    best = parsed[0]

    if best["label_day_diff"] > max_days:
        return None

    return {
        "diagnosis": best["diagnosis"],
        "label": best["label"],
        "sex": best["sex"],
        "age": best["age"],
        "apoe4": best["apoe4"],
        "scan_date": best["scan_date"],
        "label_match_type": "raw_xml_nearest" if best["label_day_diff"] > 0 else "raw_xml_exact",
        "label_day_diff": best["label_day_diff"],
        "xml_path": best["xml_path"],
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--roots", nargs="*", default=ADNI_ROOTS_DEFAULT)
    parser.add_argument("--meta-root", default="/mnt/f/DTI_Brett_metadata/ADNI/ADNI")
    parser.add_argument("--out-csv", default="/mnt/e/adni_visit_manifest.csv")
    parser.add_argument("--require-scalars", nargs="+", default=["FA", "MD", "RD", "AD"],
                        choices=["FA", "MD", "RD", "AD"])
    parser.add_argument("--max-label-days", type=int, default=365)
    args = parser.parse_args()

    meta_root = Path(args.meta_root)
    root_priority = args.roots[:]
    records = discover_records(args.roots)
    print(f"Discovered raw scalar file records: {len(records)}")

    grouped = defaultdict(list)
    for r in records:
        grouped[(r.subject_id, r.visit_date, r.scalar)].append(r)

    chosen = {}
    duplicate_rows = []
    for key, recs in grouped.items():
        best = choose_best_file(recs, root_priority=root_priority)
        chosen[key] = best
        if len(recs) > 1:
            duplicate_rows.append({
                "subject_id": key[0],
                "visit_date": key[1],
                "scalar": key[2],
                "n_candidates": len(recs),
                "chosen_path": best.nifti_path,
                "all_paths": " | ".join(sorted(r.nifti_path for r in recs)),
            })

    visit_scalars = defaultdict(dict)
    for (subject_id, visit_date, scalar), rec in chosen.items():
        visit_scalars[(subject_id, visit_date)][scalar] = rec

    manifest_rows = []
    n_labeled = 0
    n_unlabeled = 0

    for (subject_id, visit_date), scalars in sorted(visit_scalars.items()):
        if not all(s in scalars for s in args.require_scalars):
            continue

        row = {
            "subject_id": subject_id,
            "visit_date": visit_date,
            "fa_path": scalars["FA"].nifti_path if "FA" in scalars else "",
            "md_path": scalars["MD"].nifti_path if "MD" in scalars else "",
            "rd_path": scalars["RD"].nifti_path if "RD" in scalars else "",
            "ad_path": scalars["AD"].nifti_path if "AD" in scalars else "",
        }

        label_info = match_label_from_raw_xml(
            meta_root=meta_root,
            subject_id=subject_id,
            visit_date=visit_date,
            max_days=args.max_label_days,
        )

        if label_info is not None:
            row.update(label_info)
            n_labeled += 1
        else:
            row.update({
                "diagnosis": "",
                "label": "",
                "sex": "",
                "age": "",
                "apoe4": "",
                "scan_date": "",
                "label_match_type": "missing",
                "label_day_diff": "",
                "xml_path": "",
            })
            n_unlabeled += 1

        manifest_rows.append(row)

    out_csv = Path(args.out_csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "subject_id", "visit_date",
        "fa_path", "md_path", "rd_path", "ad_path",
        "diagnosis", "label", "sex", "age", "apoe4",
        "scan_date", "label_match_type", "label_day_diff", "xml_path"
    ]

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in manifest_rows:
            w.writerow(row)

    dup_csv = out_csv.with_name(out_csv.stem + "_duplicates.csv")
    if duplicate_rows:
        with open(dup_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(duplicate_rows[0].keys()))
            w.writeheader()
            w.writerows(duplicate_rows)

    print(f"Manifest written: {out_csv}")
    print(f"Valid visits with required scalars: {len(manifest_rows)}")
    print(f"Labeled visits: {n_labeled}")
    print(f"Unlabeled visits: {n_unlabeled}")
    print(f"Duplicate-resolution report: {dup_csv}")

if __name__ == "__main__":
    main()
