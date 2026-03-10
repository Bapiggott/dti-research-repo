#!/usr/bin/env python3
"""
=============================================================================
prepare_dataset.py
ADNI GNN Dataset Preparation — Run Once

Node features per ROI (8 total):
  1. mean_fa        — mean FA in this ROI (from node_features.csv)
  2. voxel_count    — number of voxels in this ROI (from roi_fa_stats.csv)
  3. centroid_x     — MNI x coordinate of ROI centroid (from AAL atlas)
  4. centroid_y     — MNI y coordinate of ROI centroid
  5. centroid_z     — MNI z coordinate of ROI centroid
  6. age            — subject age (repeated across all nodes)
  7. sex            — subject sex, M=1 F=0 (repeated across all nodes)
  8. apoe4          — APOE4 carrier 0/1 (repeated across all nodes)

Edge method options (set --edge-method):
  aal_spatial       — ROIs sharing a face in atlas space (default)
  fully_connected   — all pairs (baseline ablation)
  threshold_r       — population FA correlation, thresholded at r > threshold

Output:
  /mnt/e/adni_batch/dataset.pt
  /mnt/e/adni_batch/feat_mean.npy, feat_std.npy  (normalisation stats)
  /mnt/e/adni_batch/roi_centroids.npy            (116x3, MNI coords)
  /mnt/e/adni_batch/dataset_info.txt

Usage:
  python3 prepare_dataset.py
  python3 prepare_dataset.py --edge-method fully_connected
  python3 prepare_dataset.py --edge-method threshold_r --corr-threshold 0.3
=============================================================================
"""

import argparse
import csv
import sys
import numpy as np
from pathlib import Path
from collections import Counter

OUT_ROOT        = "/mnt/e/adni_batch"
AAL_ATLAS       = "/home/brett/atlases/AAL_MNI_2mm.nii.gz"
LABELS_CSV      = "/mnt/e/adni_batch/labels.csv"
N_ROIS          = 116
EDGE_METHOD     = "aal_spatial"
CORR_THRESHOLD  = 0.3


# =============================================================================
# ROI CENTROIDS FROM ATLAS
# =============================================================================
def compute_roi_centroids(atlas_path: str, n_rois: int) -> np.ndarray:
    """
    Compute MNI centroid (x,y,z) for each AAL ROI.
    Returns float32 array of shape (n_rois, 3), 0-indexed (roi 1 → row 0).
    """
    import nibabel as nib
    print("  Computing ROI centroids from AAL atlas...")
    img    = nib.load(atlas_path)
    atlas  = img.get_fdata().astype(int)
    affine = img.affine
    centroids = np.zeros((n_rois, 3), dtype=np.float32)

    for roi_id in range(1, n_rois + 1):
        voxels = np.argwhere(atlas == roi_id)  # (N, 3) voxel coords
        if len(voxels) == 0:
            continue
        centroid_vox = voxels.mean(axis=0)     # mean voxel coordinate
        # Convert to MNI mm space
        centroid_mni = affine[:3, :3] @ centroid_vox + affine[:3, 3]
        centroids[roi_id - 1] = centroid_mni.astype(np.float32)

    print(f"  Centroids computed: shape {centroids.shape}")
    return centroids


# =============================================================================
# LOAD LABELS
# =============================================================================
def load_labels(labels_csv: str) -> dict:
    labels = {}
    with open(labels_csv) as f:
        for row in csv.DictReader(f):
            lbl = int(row["label"])
            if lbl == -1:
                continue
            labels[row["subject_id"]] = {
                "label": lbl,
                "diagnosis": row["diagnosis"],
                "age":   float(row["age"]) if row["age"] else 0.0,
                "sex":   1.0 if row.get("sex", "M") == "M" else 0.0,
                "apoe4": float(row["apoe4"]) if row["apoe4"] else 0.0,
            }
    return labels


# =============================================================================
# LOAD NODE FEATURES
# =============================================================================
def load_node_features(subj_id: str) -> tuple | None:
    """
    Load mean_fa and voxel_count per ROI.
    Returns (fa_array, voxel_array) each shape (N_ROIS,), or None if missing.
    """
    csv_path = Path(OUT_ROOT) / subj_id / "roi_fa_stats.csv"
    if not csv_path.exists():
        # Fall back to node_features.csv (no voxel count)
        csv_path = Path(OUT_ROOT) / subj_id / "node_features.csv"
        if not csv_path.exists():
            return None

    fa_vals  = []
    vox_vals = []
    try:
        with open(csv_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                fa_vals.append(float(row.get("mean_fa", 0.0)))
                vox_vals.append(float(row.get("voxel_count", 0.0)))
        if len(fa_vals) != N_ROIS:
            return None
        return (
            np.array(fa_vals,  dtype=np.float32),
            np.array(vox_vals, dtype=np.float32),
        )
    except Exception:
        return None


# =============================================================================
# EDGE CONSTRUCTION
# =============================================================================
def build_edges_aal_spatial(atlas_path: str, n_rois: int) -> np.ndarray:
    import nibabel as nib
    print("  Building spatial adjacency from AAL atlas...")
    atlas = nib.load(atlas_path).get_fdata().astype(int)
    adj   = np.zeros((n_rois + 1, n_rois + 1), dtype=bool)
    x_max, y_max, z_max = atlas.shape

    for dx, dy, dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
        sx = slice(max(0,-dx), x_max + min(0,-dx))
        sy = slice(max(0,-dy), y_max + min(0,-dy))
        sz = slice(max(0,-dz), z_max + min(0,-dz))
        tx = slice(max(0, dx), x_max + min(0, dx))
        ty = slice(max(0, dy), y_max + min(0, dy))
        tz = slice(max(0, dz), z_max + min(0, dz))

        src_roi  = atlas[sx, sy, sz]
        dest_roi = atlas[tx, ty, tz]
        mask     = (src_roi > 0) & (dest_roi > 0) & (src_roi != dest_roi)
        s, d     = src_roi[mask], dest_roi[mask]
        valid    = (s <= n_rois) & (d <= n_rois)
        adj[s[valid], d[valid]] = True

    np.fill_diagonal(adj, False)
    adj  = adj[1:n_rois+1, 1:n_rois+1]
    adj  = adj | adj.T
    src, dst = np.where(adj)
    edge_index = np.stack([src, dst], axis=0)
    print(f"  Spatial adjacency: {edge_index.shape[1]} edges "
          f"({edge_index.shape[1]//2} undirected pairs)")
    return edge_index.astype(np.int64)


def build_edges_fully_connected(n_rois: int) -> np.ndarray:
    src, dst = np.meshgrid(np.arange(n_rois), np.arange(n_rois))
    mask = src != dst
    edge_index = np.stack([src[mask], dst[mask]], axis=0)
    print(f"  Fully connected: {edge_index.shape[1]} edges")
    return edge_index.astype(np.int64)


def build_edges_correlation(all_fa: np.ndarray, threshold: float,
                             n_rois: int) -> np.ndarray:
    print(f"  Computing population FA correlation (threshold r>{threshold})...")
    corr = np.corrcoef(all_fa.T)
    adj  = (corr > threshold)
    np.fill_diagonal(adj, False)
    adj  = adj | adj.T
    src, dst = np.where(adj)
    edge_index = np.stack([src, dst], axis=0)
    print(f"  Correlation edges: {edge_index.shape[1]}")
    return edge_index.astype(np.int64)


# =============================================================================
# NORMALISATION
# =============================================================================
def normalise(data_list: list) -> tuple:
    """
    Z-score normalise each of the 8 features across all subjects.
    Saves mean/std so the same transform can be applied at inference.
    """
    all_x = np.stack([d["x"] for d in data_list], axis=0)  # (N, 116, 8)
    mean  = all_x.mean(axis=0)   # (116, 8)
    std   = all_x.std(axis=0)    # (116, 8)
    std[std < 1e-8] = 1.0        # no division by zero for constant features

    for d in data_list:
        d["x"] = (d["x"] - mean) / std

    return data_list, mean, std


# =============================================================================
# MAIN
# =============================================================================
def main():
    parser = argparse.ArgumentParser(description="Prepare ADNI GNN dataset")
    parser.add_argument("--edge-method", default=EDGE_METHOD,
                        choices=["aal_spatial","fully_connected","threshold_r"])
    parser.add_argument("--corr-threshold", type=float, default=CORR_THRESHOLD)
    parser.add_argument("--no-normalize", action="store_true")
    args = parser.parse_args()

    try:
        import torch
        from torch_geometric.data import Data
        import nibabel
    except ImportError as e:
        print(f"ERROR: {e}\nRun: pip install torch torch-geometric nibabel")
        sys.exit(1)

    print("=" * 60)
    print("  ADNI GNN Dataset Preparation")
    print(f"  Node features:  8 per ROI")
    print(f"  Edge method:    {args.edge_method}")
    print(f"  Output:         {OUT_ROOT}/dataset.pt")
    print("=" * 60)

    # ── ROI centroids (computed once from atlas) ──────────────────────────────
    centroids_path = Path(OUT_ROOT) / "roi_centroids.npy"
    if centroids_path.exists():
        print("\nLoading cached ROI centroids...")
        centroids = np.load(centroids_path)
    else:
        print("\nComputing ROI centroids...")
        centroids = compute_roi_centroids(AAL_ATLAS, N_ROIS)
        np.save(centroids_path, centroids)
        print(f"  Saved → {centroids_path}")

    # Normalise centroids to ~[-1, 1] range (MNI coords are ~[-90, 90] mm)
    centroids_norm = centroids / 90.0

    # ── Labels ────────────────────────────────────────────────────────────────
    print("\nLoading labels...")
    labels = load_labels(LABELS_CSV)
    lbl_counts = Counter(v["label"] for v in labels.values())
    print(f"  {len(labels)} subjects  "
          f"CN/SMC={lbl_counts[0]}  MCI={lbl_counts[1]}  AD={lbl_counts[2]}")

    # ── Node features ─────────────────────────────────────────────────────────
    print("\nLoading node features...")
    raw = []
    missing = []

    for subj_id, meta in labels.items():
        result = load_node_features(subj_id)
        if result is None:
            missing.append(subj_id)
            continue

        fa_vals, vox_vals = result

        # Stack all 8 features: (116, 8)
        # Demographics broadcast across all 116 nodes
        age_col   = np.full(N_ROIS, meta["age"],   dtype=np.float32)
        sex_col   = np.full(N_ROIS, meta["sex"],   dtype=np.float32)
        apoe4_col = np.full(N_ROIS, meta["apoe4"], dtype=np.float32)

        x = np.stack([
            fa_vals,              # feature 0: mean FA
            vox_vals,             # feature 1: voxel count
            centroids_norm[:, 0], # feature 2: centroid x (MNI)
            centroids_norm[:, 1], # feature 3: centroid y (MNI)
            centroids_norm[:, 2], # feature 4: centroid z (MNI)
            age_col,              # feature 5: age
            sex_col,              # feature 6: sex
            apoe4_col,            # feature 7: APOE4
        ], axis=1).astype(np.float32)  # shape: (116, 8)

        raw.append({
            "subject_id": subj_id,
            "x":          x,
            "label":      meta["label"],
            "diagnosis":  meta["diagnosis"],
            "age":        meta["age"],
            "sex":        meta["sex"],
            "apoe4":      meta["apoe4"],
        })

    print(f"  Loaded: {len(raw)} subjects")
    if missing:
        print(f"  Missing data: {len(missing)} subjects skipped")

    # ── Edges ─────────────────────────────────────────────────────────────────
    print(f"\nBuilding edges ({args.edge_method})...")
    if args.edge_method == "aal_spatial":
        edge_index_np = build_edges_aal_spatial(AAL_ATLAS, N_ROIS)
    elif args.edge_method == "fully_connected":
        edge_index_np = build_edges_fully_connected(N_ROIS)
    elif args.edge_method == "threshold_r":
        all_fa = np.stack([d["x"][:, 0] for d in raw], axis=0)
        edge_index_np = build_edges_correlation(
            all_fa, args.corr_threshold, N_ROIS)

    edge_index = torch.tensor(edge_index_np, dtype=torch.long)

    # ── Normalise ─────────────────────────────────────────────────────────────
    if not args.no_normalize:
        print("\nNormalising features (z-score per feature per ROI)...")
        raw, feat_mean, feat_std = normalise(raw)
        np.save(Path(OUT_ROOT) / "feat_mean.npy", feat_mean)
        np.save(Path(OUT_ROOT) / "feat_std.npy",  feat_std)
        print(f"  Stats saved → feat_mean.npy, feat_std.npy")

    # ── Build PyG Data objects ────────────────────────────────────────────────
    print("\nBuilding PyG Data objects...")
    dataset = []
    for d in raw:
        data = Data(
            x          = torch.tensor(d["x"], dtype=torch.float),
            edge_index = edge_index,
            y          = torch.tensor(d["label"], dtype=torch.long),
        )
        data.subject_id = d["subject_id"]
        data.diagnosis  = d["diagnosis"]
        data.age        = d["age"]
        data.sex        = d["sex"]
        data.apoe4      = d["apoe4"]
        dataset.append(data)

    # ── Save ──────────────────────────────────────────────────────────────────
    out_path = Path(OUT_ROOT) / "dataset.pt"
    torch.save(dataset, out_path)

    # ── Summary ───────────────────────────────────────────────────────────────
    lbl_final    = Counter(d.y.item() for d in dataset)
    label_names  = {0: "CN/SMC", 1: "MCI", 2: "AD"}
    total        = len(dataset)

    summary = []
    summary.append("=" * 60)
    summary.append("  ADNI GNN Dataset Summary")
    summary.append(f"  Total graphs:      {total}")
    summary.append(f"  Nodes per graph:   {N_ROIS}")
    summary.append(f"  Features per node: 8")
    summary.append(f"    0: mean_fa")
    summary.append(f"    1: voxel_count")
    summary.append(f"    2: centroid_x (MNI)")
    summary.append(f"    3: centroid_y (MNI)")
    summary.append(f"    4: centroid_z (MNI)")
    summary.append(f"    5: age")
    summary.append(f"    6: sex")
    summary.append(f"    7: apoe4")
    summary.append(f"  Edges per graph:   {edge_index.shape[1]}")
    summary.append(f"  Edge method:       {args.edge_method}")
    summary.append(f"  Normalised:        {not args.no_normalize}")
    summary.append("")
    summary.append("  Class distribution:")
    for lbl in sorted(lbl_final):
        pct = 100 * lbl_final[lbl] / total
        summary.append(f"    {label_names[lbl]:8s} (y={lbl}): "
                       f"{lbl_final[lbl]:>4} ({pct:.1f}%)")
    summary.append("")
    summary.append("  Suggested class weights for weighted loss:")
    for lbl in sorted(lbl_final):
        w = total / (3 * lbl_final[lbl])
        summary.append(f"    class {lbl}: {w:.4f}")
    summary.append("")
    summary.append(f"  dataset.pt → {out_path}")
    summary.append("=" * 60)

    info_text = "\n".join(summary)
    print("\n" + info_text)
    with open(Path(OUT_ROOT) / "dataset_info.txt", "w") as f:
        f.write(info_text + "\n")

    print(f"\n  Load with:")
    print(f"    import torch")
    print(f"    dataset = torch.load('{out_path}')")
    print(f"    print(dataset[0])  # Data(x=[116, 8], edge_index=[2, 898], y=0)")


if __name__ == "__main__":
    main()
