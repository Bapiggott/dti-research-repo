import argparse
import os
import sys
import csv
import time

import numpy as np
import nibabel as nib

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--tck",     required=True)
    p.add_argument("--aal",     required=True)
    p.add_argument("--fa",      required=True)
    p.add_argument("--roi_csv", required=True)
    p.add_argument("--out_dir", required=True)
    p.add_argument("--n_rois",  type=int, default=90)
    return p.parse_args()

def load_tck(tck_path, ref_img):
    from dipy.io.streamline import load_tractogram
    print(f"    Loading tractogram: {tck_path}")
    t0 = time.time()
    sft = load_tractogram(tck_path, ref_img, bbox_valid_check=False)
    sft.to_vox()
    sft.to_corner()
    streamlines = list(sft.streamlines)
    print(f"    Loaded {len(streamlines):,} streamlines in {time.time()-t0:.1f}s")
    return streamlines

def get_roi(point, aal_data):
    shape = aal_data.shape
    x, y, z = int(round(point[0])), int(round(point[1])), int(round(point[2]))
    x = max(0, min(x, shape[0]-1))
    y = max(0, min(y, shape[1]-1))
    z = max(0, min(z, shape[2]-1))
    return int(aal_data[x, y, z])

def sample_fa(streamline, fa_data):
    vals = []
    shape = fa_data.shape
    for pt in streamline:
        x, y, z = int(round(pt[0])), int(round(pt[1])), int(round(pt[2]))
        x = max(0, min(x, shape[0]-1))
        y = max(0, min(y, shape[1]-1))
        z = max(0, min(z, shape[2]-1))
        vals.append(fa_data[x, y, z])
    return np.array(vals)

def sl_length(sl, voxel_sizes):
    diffs = np.diff(sl, axis=0) * voxel_sizes
    return np.sqrt((diffs**2).sum(axis=1)).sum()

def build_graphs(streamlines, aal_data, fa_data, voxel_sizes, n_rois):
    FN  = np.zeros((n_rois, n_rois), dtype=np.float32)
    FAs = np.zeros((n_rois, n_rois), dtype=np.float32)
    LEN = np.zeros((n_rois, n_rois), dtype=np.float32)
    fiber_voxels = np.zeros(n_rois, dtype=np.int32)

    total = len(streamlines)
    skipped = 0
    checkpoint = max(1, total // 20)
    t0 = time.time()

    print(f"    Processing {total:,} streamlines...")
    for i, sl in enumerate(streamlines):
        if i % checkpoint == 0:
            pct = 100 * i / total
            eta = ((time.time()-t0) / max(i,1)) * (total-i)
            print(f"    {pct:5.1f}%  ({i:,}/{total:,})  ETA: {eta:.0f}s", end="\r")

        if len(sl) < 2:
            skipped += 1
            continue

        a = get_roi(sl[0],  aal_data)
        b = get_roi(sl[-1], aal_data)

        if a == 0 or b == 0 or a == b or a > n_rois or b > n_rois:
            skipped += 1
            continue

        a -= 1
        b -= 1

        fa_vals = sample_fa(sl, fa_data)
        mean_fa = float(np.mean(fa_vals[fa_vals > 0])) if np.any(fa_vals > 0) else 0.0
        length  = sl_length(sl, voxel_sizes)

        FN[a,b]  += 1;  FN[b,a]  += 1
        FAs[a,b] += mean_fa; FAs[b,a] += mean_fa
        LEN[a,b] += length;  LEN[b,a] += length

        for pt in sl:
            r = get_roi(pt, aal_data)
            if 1 <= r <= n_rois:
                fiber_voxels[r-1] += 1

    print(f"\n    Done. Skipped {skipped:,} streamlines.")

    with np.errstate(divide="ignore", invalid="ignore"):
        FA_net  = np.where(FN > 0, FAs / FN, 0.0)
        LEN_net = np.where(FN > 0, LEN / FN, 0.0)

    return FN, FA_net, LEN_net, fiber_voxels

def save_matrix(matrix, name, out_dir):
    np.save(os.path.join(out_dir, f"{name}.npy"), matrix)
    np.savetxt(os.path.join(out_dir, f"{name}.csv"), matrix, delimiter=",", fmt="%.6f")
    print(f"    Saved: {name}.npy / .csv")

def build_node_features(roi_csv_path, fiber_voxels, n_rois, out_dir):
    roi_data = {}
    with open(roi_csv_path) as f:
        for row in csv.DictReader(f):
            roi_data[int(row["roi_id"])] = {
                "mean_fa": float(row["mean_fa"]),
                "voxel_count": int(row["voxel_count"])
            }
    with open(os.path.join(out_dir, "node_features.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["roi_id","mean_fa","ROIV_voxel_count","ROIS_fiber_voxels"])
        for roi_id in range(1, n_rois+1):
            d = roi_data.get(roi_id, {"mean_fa": 0.0, "voxel_count": 0})
            w.writerow([roi_id, f"{d['mean_fa']:.6f}", d["voxel_count"], int(fiber_voxels[roi_id-1])])
    print("    Saved: node_features.csv")

def main():
    args = parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    print("\n    Loading AAL atlas...")
    aal_img  = nib.load(args.aal)
    aal_data = np.asarray(aal_img.dataobj, dtype=np.int32)

    print("    Loading FA map...")
    fa_img   = nib.load(args.fa)
    fa_data  = np.asarray(fa_img.dataobj, dtype=np.float32)
    voxel_sizes = np.array(fa_img.header.get_zooms()[:3], dtype=np.float32)
    print(f"    Voxel size: {voxel_sizes} mm")

    if aal_data.shape != fa_data.shape:
        print(f"    WARNING: AAL shape {aal_data.shape} != FA shape {fa_data.shape}")

    unique_rois = np.unique(aal_data[aal_data > 0])
    print(f"    AAL: {len(unique_rois)} unique ROIs (expected {args.n_rois})")

    streamlines = load_tck(args.tck, fa_img)

    print("\n    Building adjacency matrices...")
    FN, FA_net, LEN_net, fiber_voxels = build_graphs(
        streamlines, aal_data, fa_data, voxel_sizes, args.n_rois)

    print("\n    Saving matrices...")
    save_matrix(FN,      "FN_network",  args.out_dir)
    save_matrix(FA_net,  "FA_network",  args.out_dir)
    save_matrix(LEN_net, "LEN_network", args.out_dir)

    build_node_features(args.roi_csv, fiber_voxels, args.n_rois, args.out_dir)

    n_conn = int(np.sum(FN > 0) / 2)
    print(f"\n    Connected ROI pairs: {n_conn} / {args.n_rois*(args.n_rois-1)//2}")
    print(f"    Mean FA (connections): {float(np.mean(FA_net[FA_net>0])):.4f}")
    print(f"    Mean length (mm): {float(np.mean(LEN_net[LEN_net>0])):.1f}")
    print(f"\n    All outputs saved to: {args.out_dir}")

if __name__ == "__main__":
    main()
