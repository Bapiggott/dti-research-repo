#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import json
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime

META_ROOT_DEFAULT = "/mnt/f/DTI_Brett_metadata/ADNI/ADNI"
VISITS_ROOT_DEFAULT = "/mnt/e/adni_multiscalar_visits"
OUT_CSV_DEFAULT = "/mnt/e/missing_visit_label_diagnosis.csv"

DIAG_TO_LABEL = {
    "CN": 0,
    "SMC": 0,
    "EMCI": 1,
    "MCI": 1,
    "LMCI": 1,
    "AD": 2,
}

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

def load_unlabeled_complete_visits(visits_root: Path):
    rows = []
    for visit_dir in sorted(visits_root.iterdir()):
        if not visit_dir.is_dir():
            continue

        required = [
            visit_dir / "metadata.json",
            visit_dir / "roi_fa_stats.csv",
            visit_dir / "roi_md_stats.csv",
            visit_dir / "roi_rd_stats.csv",
            visit_dir / "roi_ad_stats.csv",
        ]
        if not all(p.exists() for p in required):
            continue

        with open(visit_dir / "metadata.json", "r", encoding="utf-8") as f:
            meta = json.load(f)

        label_raw = meta.get("label", "")
        bad = False
        if label_raw is None:
            bad = True
        elif isinstance(label_raw, float) and pd.isna(label_raw):
            bad = True
        elif str(label_raw).strip().lower() in {"", "nan", "none", "-1"}:
            bad = True

        if bad:
            rows.append({
                "visit_dir": str(visit_dir),
                "subject_id": str(meta.get("subject_id", "")),
                "visit_date": str(meta.get("visit_date", "")),
            })

    return pd.DataFrame(rows)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--meta-root", default=META_ROOT_DEFAULT)
    parser.add_argument("--visits-root", default=VISITS_ROOT_DEFAULT)
    parser.add_argument("--out-csv", default=OUT_CSV_DEFAULT)
    parser.add_argument("--max-days", type=int, default=365)
    args = parser.parse_args()

    meta_root = Path(args.meta_root)
    visits_root = Path(args.visits_root)

    df_missing = load_unlabeled_complete_visits(visits_root)
    print(f"Unlabeled complete visits found: {len(df_missing)}")

    out_rows = []

    for i, row in df_missing.iterrows():
        subject_id = row["subject_id"]
        visit_date = row["visit_date"]

        try:
            visit_dt = pd.to_datetime(visit_date)
        except Exception:
            continue

        xmls = sorted(meta_root.glob(f"ADNI_{subject_id}_*.xml"))
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
            info["day_diff"] = abs((scan_dt - visit_dt).days)
            parsed.append(info)

        if not parsed:
            out_rows.append({
                "subject_id": subject_id,
                "visit_date": visit_date,
                "n_candidate_xmls": 0,
                "best_scan_date": "",
                "best_day_diff": "",
                "best_diagnosis": "",
                "best_label": "",
                "best_xml_path": "",
                "status": "no_xml_found",
            })
            continue

        parsed = sorted(parsed, key=lambda x: x["day_diff"])
        best = parsed[0]

        status = "good_match" if best["day_diff"] <= args.max_days else "far_match"

        out_rows.append({
            "subject_id": subject_id,
            "visit_date": visit_date,
            "n_candidate_xmls": len(parsed),
            "best_scan_date": best["scan_date"],
            "best_day_diff": best["day_diff"],
            "best_diagnosis": best["diagnosis"],
            "best_label": best["label"],
            "best_xml_path": best["xml_path"],
            "status": status,
        })

        if (i + 1) % 10 == 0:
            print(f"[{i+1}/{len(df_missing)}] checked")

    out_df = pd.DataFrame(out_rows)
    out_df.to_csv(args.out_csv, index=False)
    print(f"Saved: {args.out_csv}")

    if len(out_df) > 0:
        print("\nSummary:")
        print(out_df["status"].value_counts(dropna=False))

if __name__ == "__main__":
    main()
