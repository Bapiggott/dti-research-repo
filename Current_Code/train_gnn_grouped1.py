#!/usr/bin/env python3
from __future__ import annotations

import argparse
import random
import numpy as np
import torch
import torch.nn.functional as F
from torch.nn import Linear, BatchNorm1d, Dropout, ModuleList
from torch.utils.data import WeightedRandomSampler
from torch_geometric.loader import DataLoader
from torch_geometric.nn import GCNConv, GATConv, SAGEConv, global_mean_pool
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from sklearn.model_selection import GroupShuffleSplit


def seed_everything(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


class GNN(torch.nn.Module):
    def __init__(self, model_type: str, in_dim: int, hidden_dims: list[int], out_dim: int, dropout: float):
        super().__init__()
        self.model_type = model_type

        convs = []
        bns = []
        dims = [in_dim] + hidden_dims

        for i in range(len(hidden_dims)):
            a, b = dims[i], dims[i + 1]

            if model_type == "gcn":
                conv = GCNConv(a, b)
                actual_out = b

            elif model_type == "gat":
                if i < len(hidden_dims) - 1:
                    out_per_head = max(1, b // 4)
                    conv = GATConv(a, out_per_head, heads=4, concat=True)
                    actual_out = out_per_head * 4
                else:
                    conv = GATConv(a, b, heads=1, concat=False)
                    actual_out = b

            elif model_type == "graphsage":
                conv = SAGEConv(a, b)
                actual_out = b

            else:
                raise ValueError(model_type)

            convs.append(conv)
            bns.append(BatchNorm1d(actual_out))
            dims[i + 1] = actual_out

        self.convs = ModuleList(convs)
        self.bns = ModuleList(bns)
        self.dropout = Dropout(dropout)
        self.fc = Linear(dims[-1], out_dim)

    def forward(self, x, edge_index, batch):
        for conv, bn in zip(self.convs, self.bns):
            x = conv(x, edge_index)
            x = bn(x)
            x = F.relu(x)
            x = self.dropout(x)
        x = global_mean_pool(x, batch)
        return self.fc(x)


def class_counts_from_indices(dataset, indices, n_classes=3):
    y = [int(dataset[i].y.item()) for i in indices]
    return np.bincount(y, minlength=n_classes)


def class_count_str(dataset, indices):
    counts = class_counts_from_indices(dataset, indices, n_classes=3)
    return f"CN={counts[0]} MCI={counts[1]} AD={counts[2]}"


def proportions(counts: np.ndarray) -> np.ndarray:
    total = counts.sum()
    if total == 0:
        return np.zeros_like(counts, dtype=float)
    return counts / total


def split_score(global_counts, train_counts, test_counts, test_size):
    """
    Lower is better.
    Penalizes:
      - deviation from global class proportions in train/test
      - missing classes in train/test
      - deviation from desired test size
    """
    global_p = proportions(global_counts)
    train_p = proportions(train_counts)
    test_p = proportions(test_counts)

    score = 0.0

    # Match class proportions
    score += np.abs(train_p - global_p).sum()
    score += np.abs(test_p - global_p).sum()

    # Penalize missing classes strongly, especially in test
    score += 2.0 * np.sum(train_counts == 0)
    score += 3.0 * np.sum(test_counts == 0)

    # Match test fraction
    total = global_counts.sum()
    actual_test_frac = test_counts.sum() / total if total > 0 else 0.0
    score += 2.0 * abs(actual_test_frac - test_size)

    return float(score)


def grouped_train_test_split_best(
    dataset,
    seed=42,
    test_size=0.2,
    n_trials=200,
):
    """
    Repeated grouped train/test split.
    Keeps all visits from a subject in one split.
    Chooses the split that best preserves class proportions.
    """
    groups = np.array([d.subject_id for d in dataset])
    labels = np.array([int(d.y.item()) for d in dataset])
    idx = np.arange(len(dataset))
    global_counts = np.bincount(labels, minlength=3)

    best = None
    best_score = float("inf")

    for trial in range(n_trials):
        rs = seed + trial
        gss = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=rs)
        train_idx, test_idx = next(gss.split(idx, labels, groups))

        train_counts = class_counts_from_indices(dataset, train_idx, n_classes=3)
        test_counts = class_counts_from_indices(dataset, test_idx, n_classes=3)

        score = split_score(global_counts, train_counts, test_counts, test_size)

        if score < best_score:
            best_score = score
            best = (train_idx, test_idx, train_counts, test_counts, rs)

    if best is None:
        raise RuntimeError("Could not create a grouped train/test split.")

    train_idx, test_idx, train_counts, test_counts, best_seed = best
    return train_idx, test_idx, train_counts, test_counts, best_seed, best_score


def make_loader(dataset, indices, batch_size, weighted=False):
    subset = [dataset[i] for i in indices]

    if not weighted:
        return DataLoader(subset, batch_size=batch_size, shuffle=True)

    y = np.array([int(d.y.item()) for d in subset])
    counts = np.bincount(y, minlength=3)

    sample_weights = []
    for c in y:
        if counts[c] > 0:
            sample_weights.append(len(y) / (3 * counts[c]))
        else:
            sample_weights.append(0.0)

    sample_weights = np.array(sample_weights, dtype=np.float32)
    sampler = WeightedRandomSampler(sample_weights, num_samples=len(sample_weights), replacement=True)
    return DataLoader(subset, batch_size=batch_size, sampler=sampler)


def evaluate(model, loader, device):
    model.eval()
    ys, preds = [], []
    total_loss = 0.0

    with torch.no_grad():
        for batch in loader:
            batch = batch.to(device)
            out = model(batch.x, batch.edge_index, batch.batch)
            loss = F.cross_entropy(out, batch.y)
            total_loss += loss.item() * batch.num_graphs
            pred = out.argmax(dim=1)
            ys.extend(batch.y.cpu().numpy().tolist())
            preds.extend(pred.cpu().numpy().tolist())

    if len(ys) == 0:
        return {
            "loss": float("inf"),
            "acc": 0.0,
            "macro_f1": 0.0,
            "weighted_f1": 0.0,
            "per_class_f1": np.array([0.0, 0.0, 0.0]),
            "report": "Empty evaluation set.",
            "cm": np.zeros((3, 3), dtype=int),
        }

    acc = accuracy_score(ys, preds)
    macro_f1 = f1_score(ys, preds, average="macro", zero_division=0)
    weighted_f1 = f1_score(ys, preds, average="weighted", zero_division=0)
    per_class_f1 = f1_score(ys, preds, average=None, labels=[0, 1, 2], zero_division=0)

    return {
        "loss": total_loss / len(ys),
        "acc": acc,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "per_class_f1": per_class_f1,
        "report": classification_report(
            ys,
            preds,
            labels=[0, 1, 2],
            target_names=["CN/SMC", "MCI", "AD"],
            zero_division=0,
        ),
        "cm": confusion_matrix(ys, preds, labels=[0, 1, 2]),
    }


def train_one(model_type, dataset, args, device):
    train_idx, test_idx, train_counts, test_counts, best_seed, best_score = grouped_train_test_split_best(
        dataset=dataset,
        seed=args.seed,
        test_size=args.test_size,
        n_trials=args.split_trials,
    )

    print(f"\nTraining {model_type.upper()}")
    print(f"Best grouped split seed: {best_seed}")
    print(f"Split score: {best_score:.4f}")
    print(f"Train={len(train_idx)} Test={len(test_idx)}")
    print(f"Train class counts: {class_count_str(dataset, train_idx)}")
    print(f"Test  class counts: {class_count_str(dataset, test_idx)}")

    train_loader = make_loader(dataset, train_idx, args.batch_size, weighted=True)
    test_loader = make_loader(dataset, test_idx, args.batch_size, weighted=False)

    model = GNN(model_type, dataset[0].x.shape[1], args.hidden, 3, args.dropout).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)

    y_train = np.array([int(dataset[i].y.item()) for i in train_idx])
    counts = np.bincount(y_train, minlength=3)
    class_weights = torch.tensor(
        [len(y_train) / (3 * c) if c > 0 else 0.0 for c in counts],
        dtype=torch.float32,
        device=device,
    )

    print(f"Class weights={class_weights.tolist()}")

    best_state = None
    best_train_loss = float("inf")
    patience_ctr = 0

    for epoch in range(1, args.epochs + 1):
        model.train()
        total_loss = 0.0

        for batch in train_loader:
            batch = batch.to(device)
            opt.zero_grad()
            out = model(batch.x, batch.edge_index, batch.batch)
            loss = F.cross_entropy(out, batch.y, weight=class_weights)
            loss.backward()
            opt.step()
            total_loss += loss.item() * batch.num_graphs

        train_loss = total_loss / len(train_idx)

        if epoch == 1 or epoch % 10 == 0:
            print(f"Epoch {epoch:3d}/{args.epochs} train_loss={train_loss:.4f}")

        # Early stopping on train loss only, since no validation split
        if train_loss < best_train_loss - 1e-6:
            best_train_loss = train_loss
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
            patience_ctr = 0
        else:
            patience_ctr += 1
            if patience_ctr >= args.patience:
                print(f"Early stopping at epoch {epoch}")
                break

    if best_state is not None:
        model.load_state_dict(best_state)

    test_metrics = evaluate(model, test_loader, device)

    print("\nTest Results")
    print(f"Accuracy:    {test_metrics['acc']:.4f}")
    print(f"Macro F1:    {test_metrics['macro_f1']:.4f}")
    print(f"Weighted F1: {test_metrics['weighted_f1']:.4f}")
    print(f"Per-class F1 [CN, MCI, AD]: {test_metrics['per_class_f1']}")
    print("\nClassification Report:")
    print(test_metrics["report"])
    print("Confusion Matrix:")
    print(test_metrics["cm"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="/mnt/e/adni_multiscalar_dataset.pt")
    parser.add_argument("--model", default="all", choices=["gcn", "gat", "graphsage", "all"])
    parser.add_argument("--epochs", type=int, default=150)
    parser.add_argument("--lr", type=float, default=0.005)
    parser.add_argument("--weight-decay", type=float, default=5e-4)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--dropout", type=float, default=0.3)
    parser.add_argument("--patience", type=int, default=25)
    parser.add_argument("--hidden", nargs="+", type=int, default=[64, 32])
    parser.add_argument("--seed", type=int, default=42)

    # new split args
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--split-trials", type=int, default=200)

    args = parser.parse_args()

    seed_everything(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    try:
        dataset = torch.load(args.dataset, weights_only=False)
    except TypeError:
        dataset = torch.load(args.dataset)

    print(f"Loaded graphs: {len(dataset)}")

    if len(dataset) == 0:
        raise RuntimeError("Dataset is empty.")

    global_counts = np.bincount([int(d.y.item()) for d in dataset], minlength=3)
    print(f"Global class counts: CN={global_counts[0]} MCI={global_counts[1]} AD={global_counts[2]}")

    models = ["gcn", "gat", "graphsage"] if args.model == "all" else [args.model]
    for m in models:
        train_one(m, dataset, args, device)


if __name__ == "__main__":
    main()
