#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import json
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-csv", required=True)
    parser.add_argument("--visits-root", default="/mnt/e/adni_multiscalar_visits")
    args = parser.parse_args()

    df = pd.read_csv(args.manifest_csv)
    visits_root = Path(args.visits_root)

    updated = 0
    missing = 0

    for _, row in df.iterrows():
        visit_dir = visits_root / f"{row['subject_id']}_{row['visit_date']}"
        meta_path = visit_dir / "metadata.json"

        if not meta_path.exists():
            missing += 1
            continue

        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        meta["diagnosis"] = row.get("diagnosis", "")
        meta["label"] = row.get("label", "")
        meta["sex"] = row.get("sex", "")
        meta["age"] = row.get("age", "")
        meta["apoe4"] = row.get("apoe4", "")
        meta["scan_date"] = row.get("scan_date", "")
        meta["label_match_type"] = row.get("label_match_type", "")
        meta["label_day_diff"] = row.get("label_day_diff", "")
        meta["xml_path"] = row.get("xml_path", "")

        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        updated += 1

    print(f"Updated metadata.json files: {updated}")
    print(f"Missing visit folders: {missing}")

if __name__ == "__main__":
    main()
