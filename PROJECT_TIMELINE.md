# ADNI DTI × GNN — Project Timeline

> Alzheimer's Disease Classification using Diffusion Tensor Imaging and Graph Neural Networks  
> A record of progress, pivots, and corrections across three stages of development.

---

## At a Glance

```
Stage 1 ──────────────────────────────────────────────────────────────────────────── Stage 3
   │                              │                                                      │
Manual lit review          End-to-end pipeline vision                   Working GNN pipeline
FSL + PANDA setup          Multi-scalar + GNN design                    443 subjects trained
PANDA hits a wall          "Only 43 have all 4 scalars"      ◄── CORRECTED: data was spread
                                                                         across multiple folders
```

---

## Stage 1 — Literature Review & Preprocessing Foundation

### What was happening

The project began with a deep dive into the academic literature on DTI preprocessing for Alzheimer's research, combined with hands-on work building a preprocessing environment from scratch on a Linux VM.

**Ten papers were reviewed by hand**, extracting the preprocessing steps each used. Key takeaways from this manual review:

- Nearly every paper used **FSL** as the core toolchain
- **Eddy current correction** and **skull stripping (BET)** were near-universal
- Several papers layered **PANDA** on top of FSL for tractography
- Reporting quality varied widely — many papers omitted key parameters

**The environment built:**

| Tool | Role |
|---|---|
| `dcm2niix` | DICOM → NIfTI conversion |
| FSL | Eddy correction, BET, dtifit, registration |
| PANDA | Automated DTI pipeline including FA map generation |
| MATLAB | Required dependency for PANDA |

Raw ADNI data arrived as DICOM files, so the assumed workflow was: convert DICOM → run full preprocessing → generate FA maps → analyse. This turned out to be a wrong assumption (see correction in Stage 3).

### The blocker

**PANDA threw errors during FA map generation** and its documentation was sparse enough that debugging was impractical. Rather than spending more time fighting PANDA, the decision was made to expand the literature survey and look for alternative approaches.

### The `process_dti.sh` script

A standalone FSL shell script was written as a fallback to the full PANDA pipeline. It covered:

- DICOM → NIfTI via `dcm2niix`
- Skull stripping (`bet`, threshold 0.3)
- Eddy current + motion correction (`eddy --repol`)
- Tensor fitting + FA/MD map generation (`dtifit`)
- Registration to MNI152 1mm space (`flirt` + `fnirt`)
- Cropping to 160×192×160 (`fslroi`)

Known gaps at this stage: no denoising, no tractography, no ROI extraction.

---

## Stage 2 — Pipeline Vision & Expanded Literature Review

### What changed

With PANDA stalled, the scope of the literature review expanded from 10 to ~40 papers, now using an automated RAG pipeline (`paper_dti1.py`) built on a local Ollama instance (qwen3:8b + qwen3-embedding). The 10 hand-reviewed papers served as ground truth validation.

This wider survey crystallised the design for a full end-to-end graph learning pipeline:

```
ADNI DICOM DTI
      │
      ▼
DTI Preprocessing (FSL + MRtrix3)
      │
      ▼
Tractography + Atlas Alignment
      │
      ▼
ROI Scalar Feature Extraction (FA / MD / RD / AD)
      │
      ▼
Graph Construction (116 AAL nodes)
      │
      ▼
PyTorch Geometric Dataset
      │
      ▼
Graph Neural Network Training (GCN / GAT / GraphSAGE)
```

### Architecture decisions at this stage

Each brain visit would become one graph:
- **Nodes** — 116 AAL atlas brain regions
- **Node features** — per-ROI statistics (mean/std/min/max) for FA, MD, RD, AD, plus voxel count, centroid coordinates, demographics
- **Edges** — AAL spatial adjacency (with tractography-derived edges as planned future work)
- **Label** — CN / MCI / AD

Three GNN architectures were planned: **GCN**, **GAT**, and **GraphSAGE**.

### The scalar availability problem (later corrected)

At this stage, only one ADNI data folder was being examined (`DTI_Brett6`). Counting subjects with each scalar available showed:

| Scalar | Subjects Available |
|---|---|
| FA | 443 |
| MD | 441 |
| RD | 451 |
| AD | 471 |
| **All four scalars** | **43** |

The conclusion drawn was that multi-scalar training would be impossible at scale due to insufficient overlap. The pipeline design at this stage still planned for multi-scalar features but flagged it as a constraint.

> ⚠️ **This was incorrect.** See the correction in Stage 3.

---

## Stage 3 — Working Pipeline, Key Corrections & GNN Training

### The biggest discovery: ADNI pre-computed the scalars

The most impactful realisation of the entire project: **ADNI had already computed all four scalar maps (FA, MD, RD, AD) and delivered them as NIfTI files in native subject space.** No DICOM conversion, no tensor fitting, no eddy correction — all of that had been done upstream by ADNI's own processing pipeline.

The full PANDA and `process_dti.sh` work from Stage 1 was not wasted (it built a real understanding of the preprocessing steps that must be acknowledged in a methods section), but it was not required for this dataset. The pipeline was refocused entirely on:

1. Registering the pre-computed NIfTI scalars to MNI space
2. Extracting per-ROI statistics using the AAL atlas
3. Building and training a GNN

This must be **explicitly noted in any methods section** — reviewers familiar with DTI pipelines will expect to see eddy correction and tensor fitting and need to know these were handled upstream by ADNI.

---

### Correction: the "43 subjects" scalar overlap was a folder-scope error

The earlier count showing only 43 subjects with all four scalars was based on examining `DTI_Brett6` in isolation. In reality, the ADNI data had been downloaded across **four separate folders**:

```
F:\DTI_Brett6\ADNI\ADNI\   ← 1,214 subject folders (the only one examined before)
F:\DTI_Brett7\
F:\DTI_Brett8\
F:\DTI_Brett9\
```

Subject data is distributed across all four. The pipeline was updated (`adni_pipeline.py --all`) to discover and merge subjects from all folders, making multi-scalar training feasible.

---

### Pipeline architecture (final)

```
F:\DTI_Brett*\ADNI\ADNI\{subject}\
   Native_Space_Fractional_Anisotropy_Image\
   └── {date}\{id}\*.nii
         │
         ▼
[1] Discover subjects with FA data across all DTI_Brett* folders
         │
         ▼
[2] Copy FA .nii to E:\adni_batch\{subject}\FA_native.nii
         │
         ▼
[3] Repair NIfTI header (nibabel)
    Many ADNI pre-computed maps have degenerate sform/qform headers —
    affine is rebuilt from pixdim values if rank < 3
         │
         ▼
[4] flirt: FA_native → FMRIB58_FA_1mm  (affine only, 12 DOF)
         │
         ▼
[5] Resample AAL116 atlas to FA_MNI grid (nearest-neighbour)
         │
         ▼
[6] Extract mean FA per ROI (116 ROIs via fslmaths + fslstats)
         │
         ▼
[7] Write node_features.csv (116 rows: roi_id, mean_fa)
```

---

### Key decisions made (with rationale)

**FA-only, 443 subjects — not multi-scalar**

Even after discovering the multi-folder data, the decision was made to use FA only for the initial trained model. Mixed feature vectors (different subjects having different scalars available) break most GNN implementations. FA is the most clinically validated DTI biomarker for AD, and 443 subjects exceeds the dataset size of most published GNN AD studies. Multi-scalar remains a planned extension.

**Template: FMRIB58_FA — not MNI152 T1**

Early plans used `MNI152_T1_1mm` as the registration target. This was changed to `FMRIB58_FA_1mm` — FSL's FA-specific template. FA maps register significantly better to an FA template than to a T1 anatomical template. Cross-modality registration introduces systematic errors and is not standard practice in DTI literature.

**Registration: affine-only (flirt) — not affine + nonlinear (flirt + fnirt)**

The Stage 1 `process_dti.sh` script used both FLIRT and FNIRT. In the final pipeline, FNIRT was dropped. Root cause: 368 of 443 ADNI subjects had degenerate NIfTI headers (rank < 3 affines, zero sform codes) that caused `fnirt` to fail with `inv(): matrix is singular` regardless of parameter tuning. For 116 large AAL ROIs, affine registration is standard in the literature and sufficient — nonlinear registration primarily matters for voxel-level analyses, not region-level averages. NIfTI headers were repaired via nibabel before running FLIRT.

**Atlas: AAL116 — not AAL90**

Initial testing used AAL90. This was changed to AAL116 after an 85% streamline skip rate was observed — the 26 cerebellar regions in AAL116 are missing from AAL90, and the cerebellum is implicated in AD progression. Most modern AD papers use AAL116.

**3-class labels: CN / MCI / AD**

ADNI uses five diagnosis codes (CN, SMC, EMCI, MCI, LMCI, AD). These were collapsed into three: CN+SMC=0, all MCI variants=1, AD=2. With only 39 AD subjects, a 5-class model would be severely data-limited.

---

### GNN training and initial results

Three models were implemented and trained with subject-grouped splits (no subject appears in both train and test across their visits):

| Model | Architecture |
|---|---|
| GCN | Graph Convolutional Network |
| GAT | Graph Attention Network |
| GraphSAGE | Aggregation-based GNN |

Class imbalance (CN: 205, MCI: 199, AD: 39) was handled with weighted cross-entropy loss, `WeightedRandomSampler` oversampling, and macro F1 early stopping.

**Initial results (1 feature per node — mean FA only):** All three models collapsed to predicting almost exclusively AD — an overcorrection from the class weighting. Root cause: with `global_mean_pool` and only 1 feature per node, the GNN effectively reduces to computing a weighted scalar across 116 FA values, which is barely better than using whole-brain mean FA as a single number. The model had no spatial context to distinguish "low FA in hippocampus" from "low FA in motor cortex."

**Response:** Node features were expanded from 1 to 8 per node:
- mean FA
- voxel count (ROI size)
- MNI centroid coordinates (x, y, z — spatial identity for each ROI)
- age, sex, APOE4 (demographics as patient-level context)

Training on 8-feature nodes was in progress at time of writing.

---

## Corrections Summary

| Stage | Original Assumption | Correction Made |
|---|---|---|
| Stage 1 | Raw DICOM needed full preprocessing (PANDA/FSL pipeline) | ADNI pre-computed all scalar maps — no DICOM or tensor fitting needed |
| Stage 2 | Only 43 subjects had all 4 scalars → multi-scalar impractical | Data was spread across 4 folders; combining them gives far more subjects with full scalar coverage |
| Stage 2 | MNI152 T1 template for FA registration | Changed to FMRIB58_FA — FA-specific template, standard in DTI literature |
| Stage 2 | FLIRT + FNIRT (affine + nonlinear registration) | Affine-only — ADNI headers are frequently degenerate, causing FNIRT to fail on 83% of subjects |
| Stage 2 | AAL90 atlas | Changed to AAL116 — AAL90 silently omits the cerebellum |
| Stage 3 | 1 feature per node (mean FA) sufficient for GNN | Model collapsed — 8 features per node (FA + spatial + demographics) required for meaningful learning |

---

## What Each Stage Built Toward

**Stage 1** built real working knowledge of the DTI preprocessing stack (FSL, eddy correction, BET, dtifit, registration). Even though the DICOM pipeline was ultimately not needed for this dataset, understanding those steps is essential for correctly framing the methods section and knowing what ADNI's preprocessing pipeline did on our behalf.

**Stage 2** designed the full architecture of the graph learning system — ROI extraction, graph construction, GNN model selection, training strategy. The multi-scalar limitation discovered here turned out to be a data-scoping error, but the broader architecture design held up through Stage 3.

**Stage 3** produced a working, trained pipeline: 443 subjects processed, brain graphs constructed, three GNN models trained. The remaining open questions are around expanding to multi-scalar features across all `DTI_Brett*` folders, improving registration quality, and refining the GNN with spatial node features.

---

## Current State & Next Steps

| Task | Status |
|---|---|
| FA extraction, 443 subjects (DTI_Brett6) | ✅ Complete |
| Label extraction from ADNI XML metadata | ✅ Complete |
| GNN training with FA-only (1 feature/node) | ✅ Complete (model collapsed) |
| 8-feature node model training | 🔄 In progress |
| Process remaining DTI_Brett7–9 folders | 📋 Planned |
| Multi-scalar (FA + MD + RD + AD) dataset | 📋 Planned |
| MRtrix3 denoising + Gibbs correction | 📋 Planned improvement |
| Tractography-derived graph edges | 📋 Future work |
| Cross-validation (5-fold) | 📋 Planned |
| GNNExplainer interpretability | 📋 Future work |
