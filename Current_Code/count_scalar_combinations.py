from pathlib import Path
from collections import Counter, defaultdict
import itertools

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

def has_any_nifti(folder: Path) -> bool:
    return any(folder.rglob("*.nii")) or any(folder.rglob("*.nii.gz"))

def discover_subject_locations(adni_roots):
    """
    Returns:
        dict[str, list[Path]]
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
            subj_id = subj_dir.name
            subjects[subj_id].append(subj_dir)

    return subjects

def get_subject_scalar_presence(subject_dirs):
    """
    subject_dirs: list[Path] for the same subject across multiple roots
    A scalar is marked present if it exists in ANY of those folders.
    """
    present = {scalar: False for scalar in SCALAR_DIRS}

    for subj_dir in subject_dirs:
        for scalar, dirname in SCALAR_DIRS.items():
            scalar_path = subj_dir / dirname
            if scalar_path.exists() and has_any_nifti(scalar_path):
                present[scalar] = True

    return present

def main():
    subject_locations = discover_subject_locations(ADNI_ROOTS)
    print(f"Unique subjects discovered: {len(subject_locations)}")

    combo_counter = Counter()
    scalar_presence_map = {}

    # Optional: see how many duplicate subject IDs occur across roots
    multi_location_subjects = sum(1 for v in subject_locations.values() if len(v) > 1)
    print(f"Subjects appearing in multiple roots: {multi_location_subjects}")

    for subj_id, subj_dirs in subject_locations.items():
        present = get_subject_scalar_presence(subj_dirs)
        scalar_presence_map[subj_id] = present

        combo = tuple(sorted([k for k, v in present.items() if v]))
        combo_counter[combo] += 1

    print("\n=== Exact combinations present ===")
    for combo, count in sorted(combo_counter.items(), key=lambda x: (-x[1], x[0])):
        print(f"{combo if combo else ('NONE',)}: {count}")

    print("\n=== At least these combinations ===")
    scalar_names = list(SCALAR_DIRS.keys())
    for r in range(1, len(scalar_names) + 1):
        for combo in itertools.combinations(scalar_names, r):
            count = sum(
                all(scalar_presence_map[subj_id][x] for x in combo)
                for subj_id in scalar_presence_map
            )
            print(f"{'+'.join(combo)}: {count}")

if __name__ == "__main__":
    main()
