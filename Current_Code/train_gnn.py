#!/usr/bin/env python3
"""
=============================================================================
train_gnn.py
ADNI GNN Training — Ablation across GCN, GAT, GraphSAGE

Loads dataset.pt, runs ablation across all three architectures with
identical splits/seeds, saves results and best model checkpoints.

Handles class imbalance via:
  1. Weighted cross-entropy loss (class weights from prepare_dataset.py)
  2. WeightedRandomSampler — oversamples AD in every training batch

Evaluation:
  - Stratified 80/10/10 split (same split for all models)
  - Per-class accuracy, macro F1, weighted F1, confusion matrix
  - Early stopping on val loss (patience=20)

Output:
  /mnt/e/adni_batch/models/
    {model}_best.pt          — best checkpoint per architecture
    {model}_results.json     — metrics per architecture
    ablation_summary.csv     — side-by-side comparison table
    training_curves.png      — loss/accuracy curves for all three

Usage:
  python3 train_gnn.py
  python3 train_gnn.py --model gcn          # run one model only
  python3 train_gnn.py --epochs 200 --lr 0.001
  python3 train_gnn.py --hidden 64 128      # hidden layer sizes

Requirements:
  pip install torch torch-geometric scikit-learn matplotlib
=============================================================================
"""

import argparse
import json
import csv
import random
import sys
import time
import numpy as np
from pathlib import Path
from collections import Counter

# =============================================================================
# CONFIGURATION
# =============================================================================
OUT_ROOT    = "/mnt/e/adni_batch"
DATASET_PT  = "/mnt/e/adni_batch/dataset.pt"
MODELS_DIR  = "/mnt/e/adni_batch/models"
N_CLASSES   = 3
SEED        = 42


# =============================================================================
# MODEL DEFINITIONS
# =============================================================================
def build_model(model_name: str, in_channels: int, hidden: list, n_classes: int,
                dropout: float):
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch_geometric.nn import GCNConv, GATConv, SAGEConv, global_mean_pool

    class GCN(nn.Module):
        def __init__(self):
            super().__init__()
            dims = [in_channels] + hidden
            self.convs = nn.ModuleList(
                [GCNConv(dims[i], dims[i+1]) for i in range(len(dims)-1)]
            )
            self.bn = nn.ModuleList(
                [nn.BatchNorm1d(d) for d in hidden]
            )
            self.head = nn.Linear(hidden[-1], n_classes)
            self.dropout = dropout

        def forward(self, x, edge_index, batch):
            for conv, bn in zip(self.convs, self.bn):
                x = conv(x, edge_index)
                x = bn(x)
                x = F.relu(x)
                x = F.dropout(x, p=self.dropout, training=self.training)
            x = global_mean_pool(x, batch)
            return self.head(x)

    class GAT(nn.Module):
        def __init__(self):
            super().__init__()
            heads = 4
            dims = [in_channels] + hidden
            self.convs = nn.ModuleList()
            self.bn    = nn.ModuleList()
            for i in range(len(dims)-1):
                in_ch  = dims[i] * (heads if i > 0 else 1)
                out_ch = dims[i+1]
                # Last layer: 1 head, average — intermediate: multi-head concat
                is_last = (i == len(dims)-2)
                h = 1 if is_last else heads
                concat = not is_last
                self.convs.append(GATConv(in_ch, out_ch, heads=h,
                                          concat=concat, dropout=dropout))
                self.bn.append(nn.BatchNorm1d(out_ch * h if concat else out_ch))
            self.head = nn.Linear(hidden[-1], n_classes)
            self.dropout = dropout

        def forward(self, x, edge_index, batch):
            for conv, bn in zip(self.convs, self.bn):
                x = conv(x, edge_index)
                x = bn(x)
                x = F.elu(x)
                x = F.dropout(x, p=self.dropout, training=self.training)
            x = global_mean_pool(x, batch)
            return self.head(x)

    class GraphSAGE(nn.Module):
        def __init__(self):
            super().__init__()
            dims = [in_channels] + hidden
            self.convs = nn.ModuleList(
                [SAGEConv(dims[i], dims[i+1]) for i in range(len(dims)-1)]
            )
            self.bn = nn.ModuleList(
                [nn.BatchNorm1d(d) for d in hidden]
            )
            self.head = nn.Linear(hidden[-1], n_classes)
            self.dropout = dropout

        def forward(self, x, edge_index, batch):
            for conv, bn in zip(self.convs, self.bn):
                x = conv(x, edge_index)
                x = bn(x)
                x = F.relu(x)
                x = F.dropout(x, p=self.dropout, training=self.training)
            x = global_mean_pool(x, batch)
            return self.head(x)

    models = {"gcn": GCN, "gat": GAT, "graphsage": GraphSAGE}
    if model_name not in models:
        raise ValueError(f"Unknown model: {model_name}. Choose from {list(models)}")
    return models[model_name]()


# =============================================================================
# DATA SPLITTING
# =============================================================================
def stratified_split(dataset, train_ratio=0.8, val_ratio=0.1, seed=SEED):
    """
    Stratified 80/10/10 split — same class proportions in each split.
    Returns (train_idx, val_idx, test_idx).
    """
    from sklearn.model_selection import train_test_split

    labels = [d.y.item() for d in dataset]
    idx = list(range(len(dataset)))

    idx_trainval, idx_test = train_test_split(
        idx, test_size=0.1, stratify=labels, random_state=seed
    )
    labels_trainval = [labels[i] for i in idx_trainval]
    val_size = val_ratio / (train_ratio + val_ratio)
    idx_train, idx_val = train_test_split(
        idx_trainval, test_size=val_size,
        stratify=labels_trainval, random_state=seed
    )
    return idx_train, idx_val, idx_test


def make_sampler(dataset, indices):
    """
    WeightedRandomSampler — oversamples minority classes so each batch
    sees balanced class representation.
    """
    import torch
    labels = [dataset[i].y.item() for i in indices]
    counts = Counter(labels)
    total  = len(labels)
    # Weight per sample = inverse class frequency
    weights = [total / counts[dataset[i].y.item()] for i in indices]
    return torch.utils.data.WeightedRandomSampler(
        weights=weights,
        num_samples=len(indices),
        replacement=True
    )


# =============================================================================
# TRAINING / EVALUATION
# =============================================================================
def train_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss = 0
    for batch in loader:
        batch = batch.to(device)
        optimizer.zero_grad()
        out  = model(batch.x, batch.edge_index, batch.batch)
        loss = criterion(out, batch.y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * batch.num_graphs
    return total_loss / len(loader.dataset)


@__import__('torch').no_grad()
def evaluate(model, loader, criterion, device):
    import torch
    model.eval()
    total_loss = 0
    all_preds, all_labels = [], []
    for batch in loader:
        batch  = batch.to(device)
        out    = model(batch.x, batch.edge_index, batch.batch)
        loss   = criterion(out, batch.y)
        total_loss += loss.item() * batch.num_graphs
        preds  = out.argmax(dim=1)
        all_preds.extend(preds.cpu().tolist())
        all_labels.extend(batch.y.cpu().tolist())
    avg_loss = total_loss / len(loader.dataset)
    return avg_loss, all_preds, all_labels


def compute_metrics(preds, labels, n_classes=N_CLASSES):
    from sklearn.metrics import (f1_score, confusion_matrix,
                                 classification_report, accuracy_score)
    acc       = accuracy_score(labels, preds)
    macro_f1  = f1_score(labels, preds, average="macro",    zero_division=0)
    weighted_f1 = f1_score(labels, preds, average="weighted", zero_division=0)
    per_class_f1 = f1_score(labels, preds, average=None,
                             labels=list(range(n_classes)), zero_division=0)
    cm        = confusion_matrix(labels, preds, labels=list(range(n_classes)))
    report    = classification_report(labels, preds,
                                      target_names=["CN/SMC","MCI","AD"],
                                      zero_division=0)
    return {
        "accuracy":       acc,
        "macro_f1":       macro_f1,
        "weighted_f1":    weighted_f1,
        "per_class_f1":   per_class_f1.tolist(),
        "confusion_matrix": cm.tolist(),
        "report":         report,
    }


# =============================================================================
# SINGLE MODEL TRAINING RUN
# =============================================================================
def run_model(model_name, dataset, idx_train, idx_val, idx_test,
              class_weights, args, device):
    import torch
    from torch_geometric.loader import DataLoader

    print(f"\n{'='*60}")
    print(f"  Training: {model_name.upper()}")
    print(f"{'='*60}")

    # Build loaders
    sampler = make_sampler(dataset, idx_train)
    train_loader = DataLoader(
        [dataset[i] for i in idx_train],
        batch_size=args.batch_size,
        sampler=sampler
    )
    val_loader = DataLoader(
        [dataset[i] for i in idx_val],
        batch_size=args.batch_size, shuffle=False
    )
    test_loader = DataLoader(
        [dataset[i] for i in idx_test],
        batch_size=args.batch_size, shuffle=False
    )

    in_channels = dataset[0].x.shape[1]
    model = build_model(model_name, in_channels, args.hidden,
                        N_CLASSES, args.dropout).to(device)

    n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"  Parameters: {n_params:,}")
    print(f"  Train: {len(idx_train)}  Val: {len(idx_val)}  Test: {len(idx_test)}")

    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr,
                                 weight_decay=args.weight_decay)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, patience=10, factor=0.5, min_lr=1e-5
    )
    criterion = torch.nn.CrossEntropyLoss(
        weight=class_weights.to(device)
    )

    # Training loop
    best_val_loss   = float("inf")
    best_val_f1     = 0.0
    patience_count  = 0
    history = {"train_loss": [], "val_loss": [], "val_acc": [], "val_macro_f1": []}

    models_dir = Path(MODELS_DIR)
    models_dir.mkdir(parents=True, exist_ok=True)
    ckpt_path = models_dir / f"{model_name}_best.pt"

    t0 = time.time()
    for epoch in range(1, args.epochs + 1):
        train_loss = train_epoch(model, train_loader, optimizer, criterion, device)
        val_loss, val_preds, val_labels = evaluate(model, val_loader, criterion, device)
        val_metrics = compute_metrics(val_preds, val_labels)

        scheduler.step(val_loss)

        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)
        history["val_acc"].append(val_metrics["accuracy"])
        history["val_macro_f1"].append(val_metrics["macro_f1"])

        # Save best by macro F1 (better than val_loss for imbalanced classes)
        if val_metrics["macro_f1"] > best_val_f1:
            best_val_f1  = val_metrics["macro_f1"]
            best_val_loss = val_loss
            patience_count = 0
            torch.save({
                "epoch":       epoch,
                "model_state": model.state_dict(),
                "val_macro_f1": best_val_f1,
                "val_loss":    best_val_loss,
                "args":        vars(args),
            }, ckpt_path)
        else:
            patience_count += 1

        if epoch % 10 == 0 or epoch == 1:
            print(f"  Epoch {epoch:>4}/{args.epochs}  "
                  f"train_loss={train_loss:.4f}  "
                  f"val_loss={val_loss:.4f}  "
                  f"val_acc={val_metrics['accuracy']:.3f}  "
                  f"val_macro_f1={val_metrics['macro_f1']:.3f}")

        if patience_count >= args.patience:
            print(f"  Early stopping at epoch {epoch} "
                  f"(no improvement for {args.patience} epochs)")
            break

    elapsed = time.time() - t0
    print(f"  Training time: {elapsed:.1f}s")

    # Load best and evaluate on test set
    ckpt = torch.load(ckpt_path, map_location=device)
    model.load_state_dict(ckpt["model_state"])
    _, test_preds, test_labels = evaluate(model, test_loader, criterion, device)
    test_metrics = compute_metrics(test_preds, test_labels)

    print(f"\n  ── Test Results ──────────────────────────")
    print(f"  Accuracy:    {test_metrics['accuracy']:.4f}")
    print(f"  Macro F1:    {test_metrics['macro_f1']:.4f}")
    print(f"  Weighted F1: {test_metrics['weighted_f1']:.4f}")
    print(f"  Per-class F1 [CN, MCI, AD]: "
          f"{[round(x,3) for x in test_metrics['per_class_f1']]}")
    print(f"\n  Classification Report:\n{test_metrics['report']}")
    print(f"  Confusion Matrix (rows=true, cols=pred):")
    for i, row in enumerate(test_metrics["confusion_matrix"]):
        print(f"    {['CN/SMC','MCI','AD'][i]:6s}: {row}")

    # Save full results
    results = {
        "model":        model_name,
        "n_params":     n_params,
        "best_epoch":   ckpt["epoch"],
        "best_val_f1":  best_val_f1,
        "test_metrics": test_metrics,
        "history":      history,
        "args":         vars(args),
        "train_time_s": elapsed,
    }
    with open(models_dir / f"{model_name}_results.json", "w") as f:
        json.dump(results, f, indent=2)

    return results


# =============================================================================
# PLOTTING
# =============================================================================
def plot_curves(all_results, out_path):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("  matplotlib not installed — skipping plots")
        return

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    colors = {"gcn": "#2196F3", "gat": "#FF5722", "graphsage": "#4CAF50"}

    for res in all_results:
        name = res["model"]
        col  = colors.get(name, "gray")
        h    = res["history"]
        epochs = range(1, len(h["train_loss"]) + 1)
        axes[0].plot(epochs, h["train_loss"], "--", color=col, alpha=0.6,
                     label=f"{name.upper()} train")
        axes[0].plot(epochs, h["val_loss"],   "-",  color=col,
                     label=f"{name.upper()} val")
        axes[1].plot(epochs, h["val_macro_f1"], "-", color=col,
                     label=f"{name.upper()} val macro-F1")

    axes[0].set_title("Loss")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Cross-Entropy Loss")
    axes[0].legend(fontsize=8)
    axes[0].grid(True, alpha=0.3)

    axes[1].set_title("Validation Macro F1")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Macro F1")
    axes[1].legend(fontsize=8)
    axes[1].grid(True, alpha=0.3)

    plt.suptitle("ADNI GNN Ablation — GCN vs GAT vs GraphSAGE", fontsize=13)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"  Training curves → {out_path}")


# =============================================================================
# MAIN
# =============================================================================
def main():
    parser = argparse.ArgumentParser(description="ADNI GNN Training")
    parser.add_argument("--model", default="all",
                        choices=["all","gcn","gat","graphsage"],
                        help="Which model(s) to train")
    parser.add_argument("--epochs",       type=int,   default=150)
    parser.add_argument("--lr",           type=float, default=0.005)
    parser.add_argument("--weight-decay", type=float, default=5e-4)
    parser.add_argument("--batch-size",   type=int,   default=32)
    parser.add_argument("--dropout",      type=float, default=0.3)
    parser.add_argument("--patience",     type=int,   default=25)
    parser.add_argument("--hidden",       type=int,   nargs="+",
                        default=[64, 32],
                        help="Hidden layer sizes e.g. --hidden 64 32")
    parser.add_argument("--seed",         type=int,   default=SEED)
    args = parser.parse_args()

    # Reproducibility
    random.seed(args.seed)
    np.random.seed(args.seed)

    try:
        import torch
        from torch_geometric.loader import DataLoader
        from sklearn.metrics import f1_score
    except ImportError as e:
        print(f"ERROR: {e}")
        print("Run: pip install torch torch-geometric scikit-learn matplotlib")
        sys.exit(1)

    torch.manual_seed(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\nDevice: {device}")

    # Load dataset
    print(f"Loading dataset from {DATASET_PT}...")
    dataset = torch.load(DATASET_PT, weights_only=False)
    print(f"  {len(dataset)} graphs loaded")

    # Splits — computed once, used for ALL models
    idx_train, idx_val, idx_test = stratified_split(dataset, seed=args.seed)
    print(f"  Split — train: {len(idx_train)}  val: {len(idx_val)}  "
          f"test: {len(idx_test)}")

    # Verify stratification
    for name, idxs in [("train",idx_train),("val",idx_val),("test",idx_test)]:
        c = Counter(dataset[i].y.item() for i in idxs)
        print(f"    {name}: CN={c[0]} MCI={c[1]} AD={c[2]}")

    # Class weights from prepare_dataset stats
    label_counts = Counter(dataset[i].y.item() for i in idx_train)
    total = len(idx_train)
    class_weights = torch.tensor(
        [total / (N_CLASSES * label_counts[i]) for i in range(N_CLASSES)],
        dtype=torch.float
    )
    print(f"  Class weights: {class_weights.tolist()}")

    # Models to run
    models_to_run = (
        ["gcn", "gat", "graphsage"] if args.model == "all"
        else [args.model]
    )

    print(f"\nRunning ablation: {models_to_run}")
    print(f"Epochs: {args.epochs}  LR: {args.lr}  "
          f"Hidden: {args.hidden}  Dropout: {args.dropout}")

    all_results = []
    for model_name in models_to_run:
        res = run_model(
            model_name, dataset,
            idx_train, idx_val, idx_test,
            class_weights, args, device
        )
        all_results.append(res)

    # Ablation summary table
    models_dir = Path(MODELS_DIR)
    summary_path = models_dir / "ablation_summary.csv"
    fieldnames = ["model", "n_params", "best_epoch",
                  "test_accuracy", "test_macro_f1", "test_weighted_f1",
                  "f1_cn", "f1_mci", "f1_ad", "train_time_s"]
    rows = []
    for res in all_results:
        tm = res["test_metrics"]
        rows.append({
            "model":           res["model"].upper(),
            "n_params":        res["n_params"],
            "best_epoch":      res["best_epoch"],
            "test_accuracy":   round(tm["accuracy"], 4),
            "test_macro_f1":   round(tm["macro_f1"], 4),
            "test_weighted_f1": round(tm["weighted_f1"], 4),
            "f1_cn":           round(tm["per_class_f1"][0], 4),
            "f1_mci":          round(tm["per_class_f1"][1], 4),
            "f1_ad":           round(tm["per_class_f1"][2], 4),
            "train_time_s":    round(res["train_time_s"], 1),
        })

    with open(summary_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    print(f"\n{'='*60}")
    print("  ABLATION SUMMARY")
    print(f"{'='*60}")
    print(f"  {'Model':<12} {'Acc':>6} {'MacroF1':>8} {'F1-CN':>7} "
          f"{'F1-MCI':>7} {'F1-AD':>7}")
    print(f"  {'-'*50}")
    for row in rows:
        print(f"  {row['model']:<12} {row['test_accuracy']:>6.4f} "
              f"{row['test_macro_f1']:>8.4f} {row['f1_cn']:>7.4f} "
              f"{row['f1_mci']:>7.4f} {row['f1_ad']:>7.4f}")
    print(f"\n  Full results → {models_dir}")
    print(f"  Summary CSV  → {summary_path}")

    # Plot
    if len(all_results) > 0:
        plot_curves(all_results, models_dir / "training_curves.png")

    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
