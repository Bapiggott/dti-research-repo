#!/usr/bin/env python3
"""
extract_labels.py

Extracts diagnosis labels and covariates for all ADNI subjects from the
loose XML files in the metadata root directory.

Files are named: ADNI_{subj_id}_*.xml
Each contains researchGroup, subjectSex, subjectAge, APOE alleles, dateAcquired.

For subjects with multiple XMLs (multiple visits/scans), picks the one whose
dateAcquired is closest to the FA scan date.

Label mapping:
  CN, SMC  → 0
  EMCI, MCI, LMCI → 1
  AD       → 2

Output: /mnt/e/adni_batch/labels.csv
"""

import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from collections import Counter

# =============================================================================
METADATA_ROOT = "/mnt/f/DTI_Brett_metadata/ADNI/ADNI"
DTI_ROOT      = "/mnt/f/DTI_Brett6/ADNI/ADNI"
SUBJ_LIST     = "/tmp/fa_subjects.txt"
OUT_CSV       = "/mnt/e/adni_batch/labels.csv"
FA_FOLDER     = "Native_Space_Fractional_Anisotropy_Image"

LABEL_MAP = {
    "CN": 0, "SMC": 0,
    "EMCI": 1, "MCI": 1, "LMCI": 1,
    "AD": 2,
}


def parse_xml(xml_path: Path) -> dict:
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        # Namespace is on <project>, not root — strip it
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
        for info in root.iter(f"{ns}subjectInfo"):
            item = info.get("item", "")
            if "APOE" in item and info.text:
                apoe[item] = info.text.strip()
        # Also try without namespace
        for info in root.iter("subjectInfo"):
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
    except Exception as e:
        return {}


def get_fa_scan_date(subj_id: str) -> datetime | None:
    """Get date from FA folder name e.g. 2017-06-21_13_48_54.0"""
    fa_dir = Path(DTI_ROOT) / subj_id / FA_FOLDER
    if not fa_dir.exists():
        return None
    date_folders = sorted(fa_dir.iterdir())
    if not date_folders:
        return None
    try:
        return datetime.strptime(date_folders[0].name.split("_")[0], "%Y-%m-%d")
    except ValueError:
        return None


def main():
    subjects = [l.strip() for l in Path(SUBJ_LIST).read_text().splitlines() if l.strip()]
    print(f"Processing {len(subjects)} subjects...")

    rows = []
    no_xml, no_dx, unknown_dx = [], [], []

    for subj_id in subjects:
        # Loose XMLs named ADNI_{subj_id}_*.xml in the root metadata dir
        xmls = sorted(Path(METADATA_ROOT).glob(f"ADNI_{subj_id}_*.xml"))

        if not xmls:
            no_xml.append(subj_id)
            continue

        parsed = [parse_xml(x) for x in xmls]
        parsed = [p for p in parsed if p.get("diagnosis")]

        if not parsed:
            no_dx.append(subj_id)
            continue

        # Pick XML closest to FA scan date
        fa_date = get_fa_scan_date(subj_id)
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

    # Write
    Path(OUT_CSV).parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["subject_id","diagnosis","label",
                                          "sex","age","apoe4","scan_date"])
        w.writeheader()
        w.writerows(rows)

    # Summary
    dx_counts    = Counter(r["diagnosis"] for r in rows)
    label_counts = Counter(r["label"] for r in rows)
    label_names  = {0: "CN/SMC", 1: "MCI", 2: "AD", -1: "UNKNOWN"}

    print(f"\n{'='*50}")
    print(f"  Labels written:  {len(rows)} / {len(subjects)}")
    print(f"  No XML found:    {len(no_xml)}")
    print(f"  No diagnosis:    {len(no_dx)}")
    print(f"  Unknown dx:      {len(unknown_dx)}")
    print(f"\n  Diagnosis breakdown:")
    for dx, count in sorted(dx_counts.items()):
        print(f"    {dx:6s} (label={LABEL_MAP.get(dx,-1)}): {count:>4} subjects")
    print(f"\n  Grouped:")
    for lbl in sorted(label_counts):
        print(f"    label={lbl} {label_names.get(lbl,'?'):8s}: {label_counts[lbl]:>4} subjects")
    if no_xml:
        print(f"\n  No XML: {no_xml[:5]}{'...' if len(no_xml)>5 else ''}")
    if unknown_dx:
        print(f"\n  Unknown dx: {unknown_dx}")
    print(f"\n  Output: {OUT_CSV}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
