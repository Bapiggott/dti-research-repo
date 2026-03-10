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
        self.dropout_p = dropout

        convs = []
        bns = []
        dims = [in_dim] + hidden_dims

        for i in range(len(hidden_dims)):
            a, b = dims[i], dims[i + 1]
            if model_type == "gcn":
                conv = GCNConv(a, b)
            elif model_type == "gat":
                if i < len(hidden_dims) - 1:
                    out_per_head = max(1, b // 4)
                    conv = GATConv(a, out_per_head, heads=4, concat=True)
                    actual_out = out_per_head * 4
                    bns.append(BatchNorm1d(actual_out))
                    convs.append(conv)
                    dims[i + 1] = actual_out
                    continue
                else:
                    conv = GATConv(a, b, heads=1, concat=False)
            elif model_type == "graphsage":
                conv = SAGEConv(a, b)
            else:
                raise ValueError(model_type)

            convs.append(conv)
            bns.append(BatchNorm1d(b))

        self.convs = ModuleList(convs)
        self.bns = ModuleList(bns)
        self.fc = Linear(dims[-1], out_dim)
        self.dropout = Dropout(dropout)

    def forward(self, x, edge_index, batch):
        for conv, bn in zip(self.convs, self.bns):
            x = conv(x, edge_index)
            x = bn(x)
            x = F.relu(x)
            x = self.dropout(x)
        x = global_mean_pool(x, batch)
        return self.fc(x)


def grouped_split(dataset, seed=42, val_size=0.1, test_size=0.1):
    groups = np.array([d.subject_id for d in dataset])
    labels = np.array([int(d.y.item()) for d in dataset])
    idx = np.arange(len(dataset))

    gss1 = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=seed)
    trainval_idx, test_idx = next(gss1.split(idx, labels, groups))

    groups_trainval = groups[trainval_idx]
    labels_trainval = labels[trainval_idx]
    relative_idx = np.arange(len(trainval_idx))

    val_fraction_of_trainval = val_size / (1.0 - test_size)
    gss2 = GroupShuffleSplit(n_splits=1, test_size=val_fraction_of_trainval, random_state=seed)
    train_rel, val_rel = next(gss2.split(relative_idx, labels_trainval, groups_trainval))

    train_idx = trainval_idx[train_rel]
    val_idx = trainval_idx[val_rel]

    return train_idx, val_idx, test_idx


def class_count_str(dataset, indices):
    y = [int(dataset[i].y.item()) for i in indices]
    counts = np.bincount(y, minlength=3)
    return f"CN={counts[0]} MCI={counts[1]} AD={counts[2]}"


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
    train_idx, val_idx, test_idx = grouped_split(dataset, seed=args.seed, val_size=0.1, test_size=0.1)

    print(f"\nTraining {model_type.upper()}")
    print(f"Train={len(train_idx)} Val={len(val_idx)} Test={len(test_idx)}")
    print(f"Train class counts: {class_count_str(dataset, train_idx)}")
    print(f"Val   class counts: {class_count_str(dataset, val_idx)}")
    print(f"Test  class counts: {class_count_str(dataset, test_idx)}")

    train_loader = make_loader(dataset, train_idx, args.batch_size, weighted=True)
    val_loader = make_loader(dataset, val_idx, args.batch_size, weighted=False)
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
    best_val_f1 = -1.0
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
        val_metrics = evaluate(model, val_loader, device)

        if epoch == 1 or epoch % 10 == 0:
            print(
                f"Epoch {epoch:3d}/{args.epochs} "
                f"train_loss={train_loss:.4f} "
                f"val_loss={val_metrics['loss']:.4f} "
                f"val_acc={val_metrics['acc']:.3f} "
                f"val_macro_f1={val_metrics['macro_f1']:.3f}"
            )

        if val_metrics["macro_f1"] > best_val_f1:
            best_val_f1 = val_metrics["macro_f1"]
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

    models = ["gcn", "gat", "graphsage"] if args.model == "all" else [args.model]
    for m in models:
        train_one(m, dataset, args, device)


if __name__ == "__main__":
    main()
