#!/usr/bin/env python3
"""
count_scalar_visits.py

Purpose
-------
Comprehensively analyze ADNI scalar availability across multiple roots, answering:

1) Subject-level availability:
   - Does a subject have FA / MD / RD / AD anywhere across all folders?
   - Exact and "at least" combination counts.

2) Visit-level availability (STRICT exact-date matching):
   - For a given subject and acquisition date, which scalars exist on that same date?
   - Exact and "at least" combination counts.
   - This is the main answer to:
       "Are the 4 scalars coming from the same appointment?"

3) Multi-visit longitudinal availability:
   - How many subjects have >= 1 valid 4-scalar visit?
   - How many subjects have >= 2 valid 4-scalar visits?
   - How many total valid visits exist?

4) Duplicate / ambiguity checks:
   - Multiple files for the same scalar on the same date
   - Dates that appear across multiple roots
   - Missing / malformed date folders

Outputs
-------
Writes several CSVs into OUTPUT_DIR:
- subject_level_presence.csv
- subject_level_combos.csv
- visit_level_presence.csv
- visit_level_combos.csv
- four_scalar_visits.csv
- subject_four_scalar_visit_counts.csv
- duplicate_scalar_same_date.csv
- malformed_entries.csv

Notes
-----
- "Visit-level" here is defined by exact date string parsed from the scalar date folder,
  e.g. 2017-06-21_13_48_54.0 -> 2017-06-21
- This is STRICT. It does NOT merge nearby dates.
- That makes it appropriate for answering whether all scalars are from the same appointment/date.

After this, if you want, the next step is to build the actual dataset using:
    (subject_id, visit_date)
as the sample key, and then split by GROUP=subject_id to avoid leakage.
"""

from __future__ import annotations

from pathlib import Path
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Optional
import itertools
import csv
import re

# =========================
# USER CONFIG
# =========================

ADNI_ROOTS = [
    Path("/mnt/f/DTI_Brett6/ADNI/ADNI"),
    Path("/mnt/e/DTI__Brett2/ADNI/ADNI"),
    Path("/mnt/e/DTI__Brett3/ADNI/ADNI"),
    Path("/mnt/f/DTI__Brett/ADNI/ADNI"),
    Path("/mnt/f/DTI_Brett4/ADNI/ADNI"),
    Path("/mnt/f/DTI_Brett5/ADNI/ADNI"),
    Path("/mnt/f/DTI_Brett7/ADNI/ADNI"),
    Path("/mnt/f/DTI_Brett8/ADNI/ADNI"),
    Path("/mnt/f/DTI_Brett9/ADNI/ADNI"),
]

SCALAR_DIRS = {
    "FA": "Native_Space_Fractional_Anisotropy_Image",
    "MD": "Native_Space_Mean_Diffusivity_Image",
    "RD": "Native_Space_Radial_Diffusivity_Image",
    "AD": "Native_Space_Axial_Diffusivity_Image",
}

OUTPUT_DIR = Path.home() / "scalar_visit_analysis"

# If True, recursively search deeply under each date folder for .nii/.nii.gz files
RECURSIVE_NIFTI_SEARCH = True

# =========================
# INTERNALS
# =========================

DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")

@dataclass
class ScalarFileRecord:
    subject_id: str
    scalar: str
    visit_date: str              # YYYY-MM-DD
    root: str
    subject_dir: str
    scalar_dir: str
    date_dir: str
    nifti_path: str

@dataclass
class MalformedRecord:
    subject_id: str
    scalar: str
    root: str
    scalar_dir: str
    problem: str
    path: str

def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def has_any_nifti(folder: Path) -> bool:
    if RECURSIVE_NIFTI_SEARCH:
        return any(folder.rglob("*.nii")) or any(folder.rglob("*.nii.gz"))
    return any(folder.glob("*.nii")) or any(folder.glob("*.nii.gz"))

def list_niftis(folder: Path) -> List[Path]:
    if RECURSIVE_NIFTI_SEARCH:
        return list(folder.rglob("*.nii")) + list(folder.rglob("*.nii.gz"))
    return list(folder.glob("*.nii")) + list(folder.glob("*.nii.gz"))

def parse_visit_date_from_folder_name(name: str) -> Optional[str]:
    """
    Example:
        2017-06-21_13_48_54.0 -> 2017-06-21
    """
    m = DATE_RE.match(name)
    if not m:
        return None
    return m.group(1)

def exact_combo_tuple(present_map: Dict[str, bool]) -> Tuple[str, ...]:
    return tuple(sorted([k for k, v in present_map.items() if v]))

def write_csv(path: Path, rows: List[dict], fieldnames: List[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

def sorted_combo_counts(counter: Counter) -> List[Tuple[Tuple[str, ...], int]]:
    return sorted(counter.items(), key=lambda x: (-x[1], x[0]))

# =========================
# DISCOVERY
# =========================

def discover_subject_locations(adni_roots: List[Path]) -> Dict[str, List[Path]]:
    """
    Returns:
        subject_id -> list of subject directories across all roots
    """
    subjects = defaultdict(list)

    for root in adni_roots:
        if not root.exists():
            print(f"Skipping missing root: {root}")
            continue

        for subj_dir in root.iterdir():
            if not subj_dir.is_dir():
                continue
            subject_id = subj_dir.name
            subjects[subject_id].append(subj_dir)

    return subjects

def collect_scalar_file_records(
    subject_locations: Dict[str, List[Path]]
) -> Tuple[List[ScalarFileRecord], List[MalformedRecord]]:
    """
    Traverse all subjects, all roots, all scalar dirs, all date dirs.
    Produce one record per nifti file discovered with a valid parsed visit date.

    A single date folder may contain multiple nifti files; each file gets a record.
    """
    records: List[ScalarFileRecord] = []
    malformed: List[MalformedRecord] = []

    for subject_id, subj_dirs in subject_locations.items():
        for subj_dir in subj_dirs:
            for scalar, scalar_folder_name in SCALAR_DIRS.items():
                scalar_dir = subj_dir / scalar_folder_name
                if not scalar_dir.exists():
                    continue

                if not scalar_dir.is_dir():
                    malformed.append(MalformedRecord(
                        subject_id=subject_id,
                        scalar=scalar,
                        root=str(subj_dir.parent.parent.parent) if subj_dir.parent else "",
                        scalar_dir=str(scalar_dir),
                        problem="scalar_dir_exists_but_not_directory",
                        path=str(scalar_dir),
                    ))
                    continue

                date_dirs = [p for p in scalar_dir.iterdir() if p.is_dir()]
                if not date_dirs:
                    if has_any_nifti(scalar_dir):
                        malformed.append(MalformedRecord(
                            subject_id=subject_id,
                            scalar=scalar,
                            root=str(subj_dir.parent.parent.parent) if subj_dir.parent else "",
                            scalar_dir=str(scalar_dir),
                            problem="nifti_found_without_date_subdir",
                            path=str(scalar_dir),
                        ))
                    continue

                for date_dir in date_dirs:
                    visit_date = parse_visit_date_from_folder_name(date_dir.name)
                    if visit_date is None:
                        malformed.append(MalformedRecord(
                            subject_id=subject_id,
                            scalar=scalar,
                            root=str(subj_dir.parent.parent.parent) if subj_dir.parent else "",
                            scalar_dir=str(scalar_dir),
                            problem="could_not_parse_date_folder",
                            path=str(date_dir),
                        ))
                        continue

                    niftis = list_niftis(date_dir)
                    if not niftis:
                        malformed.append(MalformedRecord(
                            subject_id=subject_id,
                            scalar=scalar,
                            root=str(subj_dir.parent.parent.parent) if subj_dir.parent else "",
                            scalar_dir=str(scalar_dir),
                            problem="date_folder_has_no_nifti",
                            path=str(date_dir),
                        ))
                        continue

                    for nifti_path in niftis:
                        records.append(ScalarFileRecord(
                            subject_id=subject_id,
                            scalar=scalar,
                            visit_date=visit_date,
                            root=str(subj_dir.parents[2]) if len(subj_dir.parents) >= 3 else str(subj_dir),
                            subject_dir=str(subj_dir),
                            scalar_dir=str(scalar_dir),
                            date_dir=str(date_dir),
                            nifti_path=str(nifti_path),
                        ))

    return records, malformed

# =========================
# ANALYSIS BUILDERS
# =========================

def build_subject_level_presence(records: List[ScalarFileRecord]) -> Dict[str, Dict[str, bool]]:
    """
    subject_id -> {FA: bool, MD: bool, RD: bool, AD: bool}
    True if scalar exists anywhere for that subject.
    """
    presence = defaultdict(lambda: {s: False for s in SCALAR_DIRS})

    for rec in records:
        presence[rec.subject_id][rec.scalar] = True

    return dict(presence)

def build_visit_level_presence(records: List[ScalarFileRecord]) -> Dict[Tuple[str, str], Dict[str, bool]]:
    """
    (subject_id, visit_date) -> {FA: bool, MD: bool, RD: bool, AD: bool}
    True if scalar exists on that exact date for that subject.
    """
    presence = defaultdict(lambda: {s: False for s in SCALAR_DIRS})

    for rec in records:
        key = (rec.subject_id, rec.visit_date)
        presence[key][rec.scalar] = True

    return dict(presence)

def build_visit_level_file_lists(records: List[ScalarFileRecord]) -> Dict[Tuple[str, str, str], List[ScalarFileRecord]]:
    """
    (subject_id, visit_date, scalar) -> list of files
    Useful for duplicate detection.
    """
    groups = defaultdict(list)
    for rec in records:
        key = (rec.subject_id, rec.visit_date, rec.scalar)
        groups[key].append(rec)
    return dict(groups)

def combo_counter_from_presence_map(
    presence_map: Dict[object, Dict[str, bool]]
) -> Counter:
    c = Counter()
    for _, present in presence_map.items():
        c[exact_combo_tuple(present)] += 1
    return c

def at_least_combo_counts(
    presence_map: Dict[object, Dict[str, bool]]
) -> List[Tuple[str, int]]:
    scalar_names = list(SCALAR_DIRS.keys())
    out = []
    for r in range(1, len(scalar_names) + 1):
        for combo in itertools.combinations(scalar_names, r):
            count = sum(
                all(present[s] for s in combo)
                for present in presence_map.values()
            )
            out.append(("+".join(combo), count))
    return out

# =========================
# REPORT / CSV ROW BUILDERS
# =========================

def build_subject_presence_rows(subject_presence: Dict[str, Dict[str, bool]]) -> List[dict]:
    rows = []
    for subject_id, present in sorted(subject_presence.items()):
        row = {"subject_id": subject_id}
        row.update(present)
        row["exact_combo"] = "+".join(exact_combo_tuple(present)) if any(present.values()) else "NONE"
        rows.append(row)
    return rows

def build_visit_presence_rows(visit_presence: Dict[Tuple[str, str], Dict[str, bool]]) -> List[dict]:
    rows = []
    for (subject_id, visit_date), present in sorted(visit_presence.items()):
        row = {
            "subject_id": subject_id,
            "visit_date": visit_date,
        }
        row.update(present)
        row["exact_combo"] = "+".join(exact_combo_tuple(present)) if any(present.values()) else "NONE"
        rows.append(row)
    return rows

def build_combo_rows(counter: Counter, label: str) -> List[dict]:
    rows = []
    for combo, count in sorted_combo_counts(counter):
        rows.append({
            "level": label,
            "exact_combo": "+".join(combo) if combo else "NONE",
            "count": count,
        })
    return rows

def build_at_least_rows(at_least_counts: List[Tuple[str, int]], label: str) -> List[dict]:
    return [
        {
            "level": label,
            "combo": combo,
            "count": count,
        }
        for combo, count in at_least_counts
    ]

def build_duplicate_rows(file_groups: Dict[Tuple[str, str, str], List[ScalarFileRecord]]) -> List[dict]:
    rows = []
    for (subject_id, visit_date, scalar), recs in sorted(file_groups.items()):
        if len(recs) <= 1:
            continue

        roots = sorted(set(r.root for r in recs))
        date_dirs = sorted(set(r.date_dir for r in recs))
        nifti_paths = sorted(r.nifti_path for r in recs)

        rows.append({
            "subject_id": subject_id,
            "visit_date": visit_date,
            "scalar": scalar,
            "n_files": len(recs),
            "n_unique_roots": len(roots),
            "roots": " | ".join(roots),
            "date_dirs": " | ".join(date_dirs),
            "nifti_paths": " | ".join(nifti_paths),
        })
    return rows

def build_four_scalar_visit_rows(
    visit_presence: Dict[Tuple[str, str], Dict[str, bool]],
    file_groups: Dict[Tuple[str, str, str], List[ScalarFileRecord]]
) -> List[dict]:
    rows = []
    for (subject_id, visit_date), present in sorted(visit_presence.items()):
        if not all(present[s] for s in ["FA", "MD", "RD", "AD"]):
            continue

        row = {
            "subject_id": subject_id,
            "visit_date": visit_date,
        }
        for scalar in ["FA", "MD", "RD", "AD"]:
            recs = file_groups.get((subject_id, visit_date, scalar), [])
            row[f"{scalar.lower()}_n_files"] = len(recs)
            row[f"{scalar.lower()}_example_path"] = recs[0].nifti_path if recs else ""
        rows.append(row)

    return rows

def build_subject_four_scalar_visit_count_rows(
    visit_presence: Dict[Tuple[str, str], Dict[str, bool]]
) -> List[dict]:
    counts = Counter()
    for (subject_id, _visit_date), present in visit_presence.items():
        if all(present[s] for s in ["FA", "MD", "RD", "AD"]):
            counts[subject_id] += 1

    rows = []
    for subject_id, n_visits in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
        rows.append({
            "subject_id": subject_id,
            "n_four_scalar_visits": n_visits,
        })
    return rows

# =========================
# PRINT HELPERS
# =========================

def print_counter(title: str, counter: Counter) -> None:
    print(f"\n=== {title} ===")
    for combo, count in sorted_combo_counts(counter):
        print(f"{combo if combo else ('NONE',)}: {count}")

def print_at_least(title: str, presence_map: Dict[object, Dict[str, bool]]) -> None:
    print(f"\n=== {title} ===")
    for combo, count in at_least_combo_counts(presence_map):
        print(f"{combo}: {count}")

# =========================
# MAIN
# =========================

def main() -> None:
    ensure_output_dir(OUTPUT_DIR)

    print("Discovering subject locations...")
    subject_locations = discover_subject_locations(ADNI_ROOTS)

    n_subjects = len(subject_locations)
    n_multi_root_subjects = sum(1 for v in subject_locations.values() if len(v) > 1)

    print(f"Unique subjects discovered: {n_subjects}")
    print(f"Subjects appearing in multiple roots: {n_multi_root_subjects}")

    print("\nCollecting scalar file records...")
    records, malformed = collect_scalar_file_records(subject_locations)

    print(f"Total scalar nifti records found: {len(records)}")
    print(f"Malformed / suspicious entries: {len(malformed)}")

    # Build presence maps
    subject_presence = build_subject_level_presence(records)
    visit_presence = build_visit_level_presence(records)
    file_groups = build_visit_level_file_lists(records)

    n_visits = len(visit_presence)

    print(f"Unique visit keys (subject_id, visit_date): {n_visits}")

    # Subject-level reporting
    subject_counter = combo_counter_from_presence_map(subject_presence)
    print_counter("SUBJECT-LEVEL EXACT COMBINATIONS (scalar exists anywhere for subject)", subject_counter)
    print_at_least("SUBJECT-LEVEL AT-LEAST COMBINATIONS", subject_presence)

    # Visit-level reporting
    visit_counter = combo_counter_from_presence_map(visit_presence)
    print_counter("VISIT-LEVEL EXACT COMBINATIONS (same subject + same exact date)", visit_counter)
    print_at_least("VISIT-LEVEL AT-LEAST COMBINATIONS", visit_presence)

    # Four-scalar visit stats
    subject_four_scalar_visit_rows = build_subject_four_scalar_visit_count_rows(visit_presence)
    n_subjects_with_ge1_four_scalar_visit = sum(1 for r in subject_four_scalar_visit_rows if r["n_four_scalar_visits"] >= 1)
    n_subjects_with_ge2_four_scalar_visits = sum(1 for r in subject_four_scalar_visit_rows if r["n_four_scalar_visits"] >= 2)
    n_subjects_with_ge3_four_scalar_visits = sum(1 for r in subject_four_scalar_visit_rows if r["n_four_scalar_visits"] >= 3)
    total_four_scalar_visits = sum(r["n_four_scalar_visits"] for r in subject_four_scalar_visit_rows)

    print("\n=== LONGITUDINAL 4-SCALAR VISIT SUMMARY ===")
    print(f"Subjects with >=1 valid FA+MD+RD+AD same-date visit: {n_subjects_with_ge1_four_scalar_visit}")
    print(f"Subjects with >=2 valid FA+MD+RD+AD same-date visits: {n_subjects_with_ge2_four_scalar_visits}")
    print(f"Subjects with >=3 valid FA+MD+RD+AD same-date visits: {n_subjects_with_ge3_four_scalar_visits}")
    print(f"Total valid FA+MD+RD+AD same-date visits: {total_four_scalar_visits}")

    # Duplicate same-date same-scalar checks
    duplicate_rows = build_duplicate_rows(file_groups)
    print("\n=== DUPLICATE SAME-DATE SAME-SCALAR CHECK ===")
    print(f"(subject_id, visit_date, scalar) groups with >1 file: {len(duplicate_rows)}")

    # CSV outputs
    print(f"\nWriting CSVs to: {OUTPUT_DIR}")

    subject_presence_rows = build_subject_presence_rows(subject_presence)
    visit_presence_rows = build_visit_presence_rows(visit_presence)
    four_scalar_visit_rows = build_four_scalar_visit_rows(visit_presence, file_groups)

    write_csv(
        OUTPUT_DIR / "subject_level_presence.csv",
        subject_presence_rows,
        ["subject_id", "FA", "MD", "RD", "AD", "exact_combo"]
    )

    write_csv(
        OUTPUT_DIR / "subject_level_combos.csv",
        build_combo_rows(subject_counter, "subject"),
        ["level", "exact_combo", "count"]
    )

    write_csv(
        OUTPUT_DIR / "subject_level_at_least_combos.csv",
        build_at_least_rows(at_least_combo_counts(subject_presence), "subject"),
        ["level", "combo", "count"]
    )

    write_csv(
        OUTPUT_DIR / "visit_level_presence.csv",
        visit_presence_rows,
        ["subject_id", "visit_date", "FA", "MD", "RD", "AD", "exact_combo"]
    )

    write_csv(
        OUTPUT_DIR / "visit_level_combos.csv",
        build_combo_rows(visit_counter, "visit"),
        ["level", "exact_combo", "count"]
    )

    write_csv(
        OUTPUT_DIR / "visit_level_at_least_combos.csv",
        build_at_least_rows(at_least_combo_counts(visit_presence), "visit"),
        ["level", "combo", "count"]
    )

    write_csv(
        OUTPUT_DIR / "four_scalar_visits.csv",
        four_scalar_visit_rows,
        [
            "subject_id", "visit_date",
            "fa_n_files", "fa_example_path",
            "md_n_files", "md_example_path",
            "rd_n_files", "rd_example_path",
            "ad_n_files", "ad_example_path",
        ]
    )

    write_csv(
        OUTPUT_DIR / "subject_four_scalar_visit_counts.csv",
        subject_four_scalar_visit_rows,
        ["subject_id", "n_four_scalar_visits"]
    )

    write_csv(
        OUTPUT_DIR / "duplicate_scalar_same_date.csv",
        duplicate_rows,
        ["subject_id", "visit_date", "scalar", "n_files", "n_unique_roots", "roots", "date_dirs", "nifti_paths"]
    )

    malformed_rows = [asdict(x) for x in malformed]
    write_csv(
        OUTPUT_DIR / "malformed_entries.csv",
        malformed_rows,
        ["subject_id", "scalar", "root", "scalar_dir", "problem", "path"]
    )

    # Helpful end summary
    print("\n=== WHAT TO LOOK AT NEXT ===")
    print("1) visit_level_combos.csv")
    print("   -> tells you how many SAME-DATE visits have FA/MD/RD/AD combinations.")
    print("2) four_scalar_visits.csv")
    print("   -> exact subject-date rows you can use for a clean multi-scalar dataset.")
    print("3) subject_four_scalar_visit_counts.csv")
    print("   -> tells you whether multiple visits can be used per subject.")
    print("4) duplicate_scalar_same_date.csv")
    print("   -> inspect if multiple same-date files need disambiguation.")
    print("5) malformed_entries.csv")
    print("   -> catches weird folder/date issues.")

    print("\nDone.")

if __name__ == "__main__":
    main()
