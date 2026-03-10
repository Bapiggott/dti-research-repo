#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import json
import numpy as np
import pandas as pd
import nibabel as nib
import torch
from torch_geometric.data import Data

SCALAR_ORDER = ["fa", "md", "rd", "ad"]


def compute_roi_centroids(atlas_path: str, n_rois: int = 116) -> np.ndarray:
    img = nib.load(atlas_path)
    atlas = img.get_fdata().astype(int)
    affine = img.affine

    centroids = []
    for roi_id in range(1, n_rois + 1):
        vox = np.argwhere(atlas == roi_id)
        if len(vox) == 0:
            centroids.append([0.0, 0.0, 0.0])
            continue
        c_vox = vox.mean(axis=0)
        c_mni = affine[:3, :3] @ c_vox + affine[:3, 3]
        centroids.append(c_mni.tolist())

    return np.asarray(centroids, dtype=np.float32)


def load_roi_csv(path: Path, roi_ids_expected):
    df = pd.read_csv(path).sort_values("roi_id").reset_index(drop=True)
    if list(df["roi_id"]) != list(roi_ids_expected):
        raise ValueError(f"ROI mismatch in {path}")
    return df


def build_knn_edges(centroids: np.ndarray, k: int = 8) -> torch.Tensor:
    n = centroids.shape[0]
    d = np.linalg.norm(centroids[:, None, :] - centroids[None, :, :], axis=2)
    edges = set()
    for i in range(n):
        nn = np.argsort(d[i])[1:k + 1]
        for j in nn:
            edges.add((i, j))
            edges.add((j, i))
    return torch.tensor(sorted(edges), dtype=torch.long).t().contiguous()


def build_fully_connected(n_nodes: int) -> torch.Tensor:
    edges = [(i, j) for i in range(n_nodes) for j in range(n_nodes) if i != j]
    return torch.tensor(edges, dtype=torch.long).t().contiguous()


def build_aal_spatial_from_resampled(aal_resampled_path: Path, n_rois: int = 116) -> torch.Tensor:
    """
    Simple 6-neighborhood face adjacency from a resampled atlas.
    Build once from a complete visit folder.
    """
    img = nib.load(str(aal_resampled_path))
    atlas = img.get_fdata().astype(int)
    edges = set()

    dx = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    sx, sy, sz = atlas.shape

    for x in range(sx):
        for y in range(sy):
            for z in range(sz):
                a = atlas[x, y, z]
                if a < 1 or a > n_rois:
                    continue
                for ox, oy, oz in dx:
                    nx, ny, nz = x + ox, y + oy, z + oz
                    if 0 <= nx < sx and 0 <= ny < sy and 0 <= nz < sz:
                        b = atlas[nx, ny, nz]
                        if b < 1 or b > n_rois or b == a:
                            continue
                        edges.add((a - 1, b - 1))
                        edges.add((b - 1, a - 1))

    return torch.tensor(sorted(edges), dtype=torch.long).t().contiguous()


def build_node_features(
    visit_dir: Path,
    metadata: dict,
    centroids: np.ndarray,
    include_stats: tuple[str, ...],
    include_voxel_count: bool,
    include_centroids: bool,
    include_demographics: bool,
) -> np.ndarray:
    roi_ids_expected = range(1, 117)
    feats = []

    for scalar in SCALAR_ORDER:
        csv_path = visit_dir / f"roi_{scalar}_stats.csv"
        df = load_roi_csv(csv_path, roi_ids_expected)

        for stat in include_stats:
            col = f"{stat}_{scalar}"
            if col not in df.columns:
                raise ValueError(f"Missing column '{col}' in {csv_path}")
            feats.append(df[col].to_numpy(dtype=np.float32).reshape(-1, 1))

        # only include voxel_count once (from FA)
        if include_voxel_count and scalar == "fa":
            if "voxel_count" not in df.columns:
                raise ValueError(f"Missing column 'voxel_count' in {csv_path}")
            feats.append(df["voxel_count"].to_numpy(dtype=np.float32).reshape(-1, 1))

    if include_centroids:
        feats.append(centroids.astype(np.float32))

    if include_demographics:
        age = float(metadata.get("age", 0) if str(metadata.get("age", "")).strip() != "" else 0)
        sex_raw = str(metadata.get("sex", "")).strip().upper()
        sex = 1.0 if sex_raw == "M" else 0.0
        apoe4 = float(metadata.get("apoe4", 0) if str(metadata.get("apoe4", "")).strip() != "" else 0)

        feats.append(np.full((116, 1), age, dtype=np.float32))
        feats.append(np.full((116, 1), sex, dtype=np.float32))
        feats.append(np.full((116, 1), apoe4, dtype=np.float32))

    x = np.concatenate(feats, axis=1)
    return x


def is_complete_visit_dir(visit_dir: Path) -> tuple[bool, list[str]]:
    """
    A complete visit must contain:
      - metadata.json
      - roi_fa_stats.csv
      - roi_md_stats.csv
      - roi_rd_stats.csv
      - roi_ad_stats.csv
      - AAL_resampled.nii.gz (needed for aal_spatial)
    """
    required = [
        "metadata.json",
        "roi_fa_stats.csv",
        "roi_md_stats.csv",
        "roi_rd_stats.csv",
        "roi_ad_stats.csv",
        "AAL_resampled.nii.gz",
    ]
    missing = [name for name in required if not (visit_dir / name).exists()]
    return (len(missing) == 0, missing)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--visits-root", default="/mnt/e/adni_multiscalar_visits")
    parser.add_argument("--atlas", default="/home/brett/atlases/AAL_MNI_2mm.nii.gz")
    parser.add_argument("--out-dataset", default="/mnt/e/adni_multiscalar_dataset.pt")
    parser.add_argument("--out-info", default="/mnt/e/adni_multiscalar_dataset_info.txt")
    parser.add_argument("--include-stats", nargs="+", default=["mean", "std"],
                        choices=["mean", "std", "min", "max"])
    parser.add_argument("--include-voxel-count", action="store_true")
    parser.add_argument("--include-centroids", action="store_true")
    parser.add_argument("--include-demographics", action="store_true")
    parser.add_argument("--edge-method", default="aal_spatial",
                        choices=["aal_spatial", "fully_connected", "knn"])
    parser.add_argument("--k", type=int, default=8)
    parser.add_argument("--normalize", action="store_true")
    args = parser.parse_args()

    visits_root = Path(args.visits_root)
    all_visit_dirs = sorted([p for p in visits_root.iterdir() if p.is_dir()])
    print(f"Found visit folders: {len(all_visit_dirs)}")

    complete_visit_dirs = []
    incomplete_rows = []

    for visit_dir in all_visit_dirs:
        ok, missing = is_complete_visit_dir(visit_dir)
        if ok:
            complete_visit_dirs.append(visit_dir)
        else:
            incomplete_rows.append((visit_dir.name, missing))

    print(f"Complete 4-scalar visit folders: {len(complete_visit_dirs)}")
    print(f"Incomplete/skipped visit folders: {len(incomplete_rows)}")

    if len(complete_visit_dirs) == 0:
        raise RuntimeError("No complete visit folders found with all 4 scalar CSVs and metadata.")

    centroids = compute_roi_centroids(args.atlas, n_rois=116)

    # build shared edge_index
    if args.edge_method == "fully_connected":
        edge_index = build_fully_connected(116)
    elif args.edge_method == "knn":
        edge_index = build_knn_edges(centroids, k=args.k)
    else:
        # Use first COMPLETE folder, not first raw folder
        first_aal = complete_visit_dirs[0] / "AAL_resampled.nii.gz"
        edge_index = build_aal_spatial_from_resampled(first_aal, n_rois=116)

    dataset = []
    skipped_unlabeled = 0
    skipped_feature_errors = 0

    for visit_dir in complete_visit_dirs:
        meta_path = visit_dir / "metadata.json"

        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        label_raw = meta.get("label", "")

        # Robust missing-label handling
        if label_raw is None:
            skipped_unlabeled += 1
            continue

        if isinstance(label_raw, float) and np.isnan(label_raw):
            skipped_unlabeled += 1
            continue

        label_str = str(label_raw).strip().lower()
        if label_str in {"", "nan", "none", "-1"}:
            skipped_unlabeled += 1
            continue

        try:
            x = build_node_features(
                visit_dir=visit_dir,
                metadata=meta,
                centroids=centroids,
                include_stats=tuple(args.include_stats),
                include_voxel_count=args.include_voxel_count,
                include_centroids=args.include_centroids,
                include_demographics=args.include_demographics,
            )
        except Exception as e:
            print(f"Skipping {visit_dir.name} due to feature error: {e}")
            skipped_feature_errors += 1
            continue

        dataset.append({
            "visit_dir": visit_dir,
            "meta": meta,
            "x": x,
        })

    print(f"Usable labeled complete visits: {len(dataset)}")
    print(f"Skipped unlabeled visits: {skipped_unlabeled}")
    print(f"Skipped feature-error visits: {skipped_feature_errors}")

    if len(dataset) == 0:
        raise RuntimeError("No usable labeled complete visits found.")

    if args.normalize:
        X = np.stack([d["x"] for d in dataset], axis=0)  # [N, 116, F]
        mean = X.mean(axis=0)
        std = X.std(axis=0)
        std[std < 1e-8] = 1.0
    else:
        mean = None
        std = None

    pyg_dataset = []
    for item in dataset:
        x = item["x"]
        if args.normalize:
            x = (x - mean) / std

        meta = item["meta"]
        y = int(float(meta["label"]))

        data = Data(
            x=torch.tensor(x, dtype=torch.float32),
            edge_index=edge_index,
            y=torch.tensor(y, dtype=torch.long),
        )
        data.subject_id = str(meta["subject_id"])
        data.visit_date = str(meta["visit_date"])
        data.diagnosis = str(meta.get("diagnosis", ""))
        data.age = float(meta.get("age", 0) or 0)
        data.sex = str(meta.get("sex", ""))
        data.apoe4 = int(float(meta.get("apoe4", 0) or 0))
        pyg_dataset.append(data)

    torch.save(pyg_dataset, args.out_dataset)

    with open(args.out_info, "w", encoding="utf-8") as f:
        f.write(f"n_visit_folders_found: {len(all_visit_dirs)}\n")
        f.write(f"n_complete_visit_folders: {len(complete_visit_dirs)}\n")
        f.write(f"n_graphs: {len(pyg_dataset)}\n")
        f.write(f"n_nodes: 116\n")
        f.write(f"n_features: {pyg_dataset[0].x.shape[1] if pyg_dataset else 0}\n")
        f.write(f"edge_method: {args.edge_method}\n")
        f.write(f"n_edges: {edge_index.shape[1]}\n")
        f.write(f"include_stats: {args.include_stats}\n")
        f.write(f"include_voxel_count: {args.include_voxel_count}\n")
        f.write(f"include_centroids: {args.include_centroids}\n")
        f.write(f"include_demographics: {args.include_demographics}\n")
        f.write(f"normalized: {args.normalize}\n")
        f.write(f"skipped_incomplete_visit_folders: {len(incomplete_rows)}\n")
        f.write(f"skipped_unlabeled_visits: {skipped_unlabeled}\n")
        f.write(f"skipped_feature_error_visits: {skipped_feature_errors}\n")

        if incomplete_rows:
            f.write("\n# Incomplete visit folders\n")
            for visit_name, missing in incomplete_rows[:200]:
                f.write(f"{visit_name}: missing {missing}\n")

    print(f"Saved dataset: {args.out_dataset}")
    print(f"Saved info:    {args.out_info}")


if __name__ == "__main__":
    main()
