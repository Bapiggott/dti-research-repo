# ADNI DTI GNN Pipeline — Complete Documentation

> **Project:** Graph Neural Network for Alzheimer's Disease Classification  
> **Data:** ADNI (Alzheimer's Disease Neuroimaging Initiative) DTI scalar maps  
> **Goal:** Classify subjects as CN / MCI / AD using per-ROI FA features on a 116-node brain graph  
> **Date:** March 2026

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Data Inventory](#2-data-inventory)
3. [Literature Context](#3-literature-context)
4. [Key Architectural Decisions](#4-key-architectural-decisions)
5. [Pipeline Architecture](#5-pipeline-architecture)
6. [File & Directory Structure](#6-file--directory-structure)
7. [Scripts Reference](#7-scripts-reference)
8. [Registration Pipeline Deep-Dive](#8-registration-pipeline-deep-dive)
9. [Debugging History](#9-debugging-history)
10. [Label Extraction](#10-label-extraction)
11. [Dataset Preparation](#11-dataset-preparation)
12. [GNN Architecture](#12-gnn-architecture)
13. [Training Strategy](#13-training-strategy)
14. [Results (Initial Run)](#14-results-initial-run)
15. [Class Imbalance Strategy](#15-class-imbalance-strategy)
16. [Diagnosis Group Definitions](#16-diagnosis-group-definitions)
17. [Next Steps & Known Issues](#17-next-steps--known-issues)

---

## 1. Project Overview

This pipeline processes ADNI DTI data to build a Graph Neural Network (GNN) that classifies subjects as cognitively normal (CN), mild cognitive impairment (MCI), or Alzheimer's disease (AD).

The approach treats each subject's brain as a graph:
- **Nodes** = 116 anatomical brain regions (AAL116 atlas)
- **Node features** = per-ROI DTI scalar values + spatial + demographic features
- **Edges** = structural adjacency between ROIs (spatial face-adjacency in atlas space)
- **Graph label** = diagnosis (CN=0, MCI=1, AD=2)

The pipeline runs end-to-end on Windows Subsystem for Linux (WSL2) with data on an external F:\ drive and outputs to E:\.

---

## 2. Data Inventory

### Storage Layout

| Location | Contents |
|---|---|
| `F:\DTI_Brett6\ADNI\ADNI\` | Primary DTI scalar maps (1,214 subject folders) |
| `F:\DTI_Brett7\` through `F:\DTI_Brett9\` | Additional ADNI downloads (same structure) |
| `F:\DTI_Brett_metadata\ADNI\ADNI\` | XML metadata files per subject |
| `E:\adni_batch\` | All pipeline outputs |
| `C:\ADNIMERGE2\` | ADNIMERGE2 R package (clinical data, `.rda` format) |

### Subject Folder Structure

```
F:\DTI_Brett6\ADNI\ADNI\
└── 002_S_0413\
    ├── Native_Space_Fractional_Anisotropy_Image\
    │   └── 2017-06-21_13_48_54.0\
    │       └── I863064\
    │           └── ADNI_002_S_0413_20250514034509495.nii
    ├── Native_Space_Mean_Diffusivity_Image\
    ├── Native_Space_Radial_Diffusivity_Image\
    └── Native_Space_Axial_Diffusivity_Image\
```

The date folder (e.g. `2017-06-21_13_48_54.0`) encodes the scan acquisition date — used later to match the correct XML metadata to the right visit.

### Scalar Availability (out of 1,214 total subjects)

| Scalar | Subjects Available |
|---|---|
| FA (Fractional Anisotropy) | **443** |
| MD (Mean Diffusivity) | 441 |
| RD (Radial Diffusivity) | 451 |
| AD (Axial Diffusivity) | 471 |
| **All four scalars** | **43** |
| Raw DWI (tractography possible) | ~12 (Axial_MB_DTI_PA_MSV21_ series only) |

**Important:** ADNI pre-computed all scalar maps. No DICOM conversion or tensor fitting was required. The scalars are already in NIfTI format in native (subject) space.

### Metadata Structure

Two types of XML files exist in the metadata folder:

**Loose XMLs at root level** (contain clinical data):
```
F:\DTI_Brett_metadata\ADNI\ADNI\ADNI_002_S_0413_Axial_DTI_S574073_I863064.xml
```
Named: `ADNI_{subject_id}_{scan_type}_{series_id}_{image_id}.xml`

These contain: `researchGroup` (diagnosis), `subjectSex`, `subjectAge`, APOE alleles, `dateAcquired`, scanner info.

**Per-subject subfolder XMLs** (stub only — no clinical data):
```
F:\DTI_Brett_metadata\ADNI\ADNI\002_S_0413\Axial_DTI\...\S574073I863064.xml
```
These only contain image/series IDs. **Do not use for labels.**

---

## 3. Literature Context

Before building the pipeline, a multi-batch literature review of GNN-based AD classification from DTI was conducted. Key findings:

### Most Common Preprocessing Steps (by frequency)

1. Eddy current and motion correction (nearly universal)
2. Tensor fitting / FA/MD calculation (high)
3. Skull stripping (high — FSL-BET, ROBEX)
4. Resampling to isotropic voxel sizes (2–2.5mm common)
5. Alignment to standard space (high)
6. Fiber tractography (moderate)
7. Denoising — MP-PCA, Gibbs ringing correction (moderate)
8. ROI extraction / feature selection (moderate)

### Why Our Pipeline Skips Steps 1–3

ADNI pre-computed the scalar maps. Eddy correction, tensor fitting, and skull stripping were done upstream by ADNI's processing pipeline. **This must be explicitly noted in the methods section** — reviewers familiar with the literature will expect these steps and need to know they are accounted for.

### Template Choice: FMRIB58_FA_1mm

**Decision:** Use `FMRIB58_FA_1mm` (FSL's FA-specific template) rather than `MNI152_T1_1mm`.

**Rationale:** FA maps register better to an FA template than to a T1 anatomical template. Cross-modality registration (FA → T1 template) introduces systematic errors. The FA-specific template is the consensus choice in recent DTI papers.

FSL config path: `$FSLDIR/etc/flirtsch/FA_2_FMRIB58_1mm.cnf`  
FSL data path: `$FSLDIR/data/standard/FMRIB58_FA_1mm.nii.gz`

### Atlas Choice: AAL116

**Decision:** Use AAL116 (116 regions) rather than AAL90.

**Rationale:** AAL90 does not include cerebellar regions. AAL116 adds 26 cerebellar ROIs. Earlier testing with AAL90 caused an 85% streamline skip rate, because the cerebellum is implicated in AD progression. Most modern AD papers use AAL116 over AAL90. Using 90 ROIs when the atlas has 116 would mean silently ignoring an anatomically relevant part of the brain.

### FA Threshold

The literature commonly applies an FA threshold of 0.2–0.3 before ROI extraction to mask out non-white-matter voxels. This was **not implemented** in the current pipeline but should be considered for a revision.

---

## 4. Key Architectural Decisions

### Decision 1: FA-Only, 443 Subjects

**Options considered:**
- FA only (443 subjects, 1 scalar feature per ROI)
- FA + MD (167 subjects with both)
- All four scalars (43 subjects)

**Chosen:** FA only.

**Rationale:** Consistency across all subjects is essential for GNN training. Heterogeneous feature vectors (different subjects having different numbers of features) break most GNN implementations and introduce bias in ones that technically handle it. 443 subjects is competitive with published AD GNN papers. FA is the most clinically validated DTI metric for Alzheimer's disease (reduced white matter integrity is a well-established biomarker).

**Methodological justification for write-up:** Consistency across subjects was prioritized over feature richness. FA is the most widely validated DTI biomarker for AD. Dataset size (n=443) exceeds most published GNN studies on ADNI.

### Decision 2: Affine-Only Registration (No fnirt)

**Options considered:**
- flirt (affine, 12 DOF) only
- flirt + fnirt (nonlinear)

**Chosen:** flirt affine only.

**Rationale:** fnirt consistently failed with `inv(): matrix is singular` across 368/443 subjects regardless of parameter tuning. Root cause: many ADNI pre-computed FA images have degenerate NIfTI sform/qform headers (rank < 3, zero sform code, or non-finite affine values) — a known artifact of some DICOM-to-NIfTI conversion pipelines. For 116 large AAL ROIs, affine registration is standard in the literature and sufficient. Nonlinear registration adds precision for voxel-level analysis but is not critical for region-level averages.

**Methodological justification:** Affine registration was used due to the presence of degenerate image headers in ADNI pre-computed maps. NIfTI headers were repaired prior to registration using nibabel, reconstructing valid affines from pixdim values. For 116-ROI mean FA extraction, affine accuracy is sufficient.

### Decision 3: Atlas Applied in MNI Space (Not Subject Space)

**Options considered:**
- Register atlas to subject space (invwarp → applywarp)
- Register subject to MNI space and apply atlas there

**Chosen:** Register subject to MNI, apply atlas in MNI space.

**Rationale:** Applying the atlas in subject space required invwarp and applywarp — two additional FSL tools that both fail when the affine matrix is degenerate. Registering the subject to MNI and resampling the atlas to match the registered image eliminates these steps entirely. Only flirt + identity matrix resampling are required. This is architecturally simpler and avoids the inversion problem.

### Decision 4: 3-Class Labels (CN=0, MCI=1, AD=2)

**ADNI diagnosis groups present:**
- CN (Cognitively Normal): 183 subjects
- SMC (Subjective Memory Concern): 22 subjects
- EMCI (Early MCI): 66 subjects
- MCI: 100 subjects
- LMCI (Late MCI): 33 subjects
- AD (Alzheimer's Disease): 39 subjects

**Chosen:** 3-class collapse: CN+SMC=0, EMCI+MCI+LMCI=1, AD=2.

**Rationale:** With only 39 AD subjects, a 5-class model would be severely data-limited for the rarest classes. 3-class is the standard in GNN AD classification literature. SMC is treated as CN-like (subjective concern without objective impairment). All MCI subtypes share the same intermediate clinical status. A fine-grained 5-class model could be explored as an ablation once the base model works.

---

## 5. Pipeline Architecture

```
F:\DTI_Brett*\ADNI\ADNI\{subject}\
   Native_Space_Fractional_Anisotropy_Image\
   └── {date}\{id}\*.nii
         │
         ▼
[1] Discover subjects with FA data
         │
         ▼
[2] Copy FA .nii to E:\adni_batch\{subject}\FA_native.nii
         │
         ▼
[3] Repair NIfTI header (nibabel)
    - Check affine rank, sform code, pixdim
    - Rebuild affine from pixdim if degenerate
         │
         ▼
[4] flirt: FA_native → FMRIB58_FA_1mm
    - 12 DOF affine
    - Output: FA_MNI.nii.gz + native2mni.mat
    - Delete FA_native.nii after
         │
         ▼
[5] Resample AAL116 to FA_MNI grid
    - flirt -applyxfm with identity matrix
    - nearestneighbour interpolation
    - Output: AAL_mni_resampled.nii.gz
         │
         ▼
[6] Extract mean FA per ROI (116 ROIs)
    - fslmaths: threshold each ROI → binary mask
    - fslstats: mean FA within mask
    - Output: roi_fa_stats.csv
    - Delete FA_MNI.nii.gz after
         │
         ▼
[7] Write node_features.csv
    - roi_id, mean_fa (116 rows)
```

### Parallel Execution

The Python pipeline uses `multiprocessing.Pool` with `cpu_count()` workers (6 on this machine). Each subject is processed independently — no shared state. Processing time was approximately 2–3 hours for 443 subjects.

---

## 6. File & Directory Structure

### Output Per Subject: `E:\adni_batch\{subject_id}\`

| File | Contents | Kept? |
|---|---|---|
| `node_features.csv` | 116 rows: roi_id, mean_fa | ✅ Yes |
| `roi_fa_stats.csv` | 116 rows: roi_id, mean_fa, voxel_count | ✅ Yes |
| `AAL_mni_resampled.nii.gz` | AAL atlas resampled to FA_MNI space | ✅ Yes (QC) |
| `FA_native.nii` | Native space FA copy | ❌ Deleted after step 6 |
| `FA_MNI.nii.gz` | Registered FA in MNI space | ❌ Deleted after step 6 |
| `native2mni.mat` | Affine transform matrix | ❌ Deleted after step 4 |
| `identity.mat` | Identity matrix for atlas resampling | ❌ Deleted after step 5 |
| `_mask_{roi_id}.nii.gz` | Temporary ROI binary masks | ❌ Deleted per ROI |

### Root Output Directory: `E:\adni_batch\`

| File | Contents |
|---|---|
| `labels.csv` | 443 rows: subject_id, diagnosis, label, sex, age, apoe4, scan_date |
| `dataset.pt` | PyTorch Geometric dataset (443 Data objects) |
| `feat_mean.npy` | Per-ROI per-feature mean (116×8) for z-score normalisation |
| `feat_std.npy` | Per-ROI per-feature std (116×8) |
| `roi_centroids.npy` | MNI centroid coordinates per ROI (116×3) |
| `dataset_info.txt` | Summary stats, class distribution, class weights |
| `logs/pipeline_main.log` | Main run log |
| `logs/{subject_id}.log` | Per-subject FSL command log |
| `parallel_joblog.txt` | GNU parallel job log (from bash pipeline runs) |

### Models Directory: `E:\adni_batch\models\`

| File | Contents |
|---|---|
| `gcn_best.pt` | Best GCN checkpoint (by val macro F1) |
| `gat_best.pt` | Best GAT checkpoint |
| `graphsage_best.pt` | Best GraphSAGE checkpoint |
| `gcn_results.json` | Full metrics, history, args |
| `gat_results.json` | Full metrics, history, args |
| `graphsage_results.json` | Full metrics, history, args |
| `ablation_summary.csv` | Side-by-side comparison table |
| `training_curves.png` | Loss and F1 curves for all three models |

---

## 7. Scripts Reference

### `run_adni_extraction.py` — FA Extraction Pipeline

**Purpose:** Process all 443 subjects with FA data. Idempotent — already-done subjects skipped.

```bash
python3 ~/run_adni_extraction.py
python3 ~/run_adni_extraction.py --jobs 4
python3 ~/run_adni_extraction.py --list /tmp/custom_subjects.txt
```

**Key config variables at top of file:**
```python
ADNI_ROOT  = "/mnt/f/DTI_Brett6/ADNI/ADNI"
OUT_ROOT   = "/mnt/e/adni_batch"
AAL_ATLAS  = "/home/brett/atlases/AAL_MNI_2mm.nii.gz"
FSL_HOME   = "/home/brett/fsl"
SUBJ_LIST  = "/tmp/fa_subjects.txt"
N_ROIS     = 116
```

**Subject list generation (must regenerate after reboot — /tmp is cleared):**
```bash
for subj in /mnt/f/DTI_Brett6/ADNI/ADNI/*/; do
    subj_id=$(basename "$subj")
    if [ -d "${subj}/Native_Space_Fractional_Anisotropy_Image" ]; then
        echo "$subj_id"
    fi
done > /tmp/fa_subjects.txt
wc -l /tmp/fa_subjects.txt  # should be 443
```

**Monitor progress:**
```bash
tail -f /mnt/e/adni_batch/logs/pipeline_main.log
# or
ls /mnt/e/adni_batch/*/node_features.csv | wc -l
```

---

### `adni_pipeline.py` — Master Multi-Folder Pipeline

**Purpose:** Process subjects from any combination of DTI_Brett* folders. Handles discovery, FA extraction, and label extraction in one command. Merges results into the same output directory.

```bash
# Specific folders
python3 ~/adni_pipeline.py --folders DTI_Brett7 DTI_Brett8

# All folders at once
python3 ~/adni_pipeline.py --all

# Dry run (discover only, no processing)
python3 ~/adni_pipeline.py --folders DTI_Brett7 --dry-run

# Labels only (skip FA extraction, just update labels.csv)
python3 ~/adni_pipeline.py --folders DTI_Brett7 --labels-only

# Limit workers
python3 ~/adni_pipeline.py --folders DTI_Brett7 --jobs 4
```

**Key behaviors:**
- Already-processed subjects (have `node_features.csv`) are skipped automatically
- Subjects appearing in multiple folders: first found wins (no duplicates)
- Labels for new subjects are merged into existing `labels.csv`

---

### `extract_labels.py` — XML Label Extraction

**Purpose:** Parse loose XML files in the metadata root to extract diagnosis, age, sex, APOE4 for all 443 subjects.

```bash
python3 ~/extract_labels.py
```

**Logic:**
1. For each subject, glob `ADNI_{subject_id}_*.xml` in `METADATA_ROOT`
2. Parse all matching XMLs → extract researchGroup, age, sex, APOE alleles, dateAcquired
3. Match each XML's `dateAcquired` to the subject's FA scan date (from folder name)
4. Use the XML closest in date to the FA scan — ensures the label matches the imaging timepoint
5. Map diagnosis groups to integer labels

**Output columns:**
- `subject_id` — ADNI subject identifier (e.g. `002_S_0413`)
- `diagnosis` — raw string: CN, SMC, EMCI, MCI, LMCI, AD
- `label` — integer: 0=CN/SMC, 1=MCI variants, 2=AD, -1=unknown (excluded)
- `sex` — M or F
- `age` — age at scan (float, years)
- `apoe4` — 0 or 1 (1 if either allele is e4)
- `scan_date` — YYYY-MM-DD of matched XML

---

### `prepare_dataset.py` — PyG Dataset Builder

**Purpose:** Load all node features and labels, build graph structure, save a single `dataset.pt`. Run once before training. Training loads this file instantly.

```bash
python3 ~/prepare_dataset.py
python3 ~/prepare_dataset.py --edge-method fully_connected
python3 ~/prepare_dataset.py --edge-method threshold_r --corr-threshold 0.3
python3 ~/prepare_dataset.py --no-normalize
```

**Edge methods:**
- `aal_spatial` (default) — ROIs sharing a face in atlas voxel space (6-connectivity)
- `fully_connected` — all 116×116 pairs (ablation baseline)
- `threshold_r` — population-level FA correlation, thresholded at r > threshold

---

### `train_gnn.py` — GNN Training & Ablation

**Purpose:** Train GCN, GAT, GraphSAGE on the prepared dataset. Same split for all models (fair ablation). Saves checkpoints and results.

```bash
python3 ~/train_gnn.py                    # all three models
python3 ~/train_gnn.py --model gcn        # one model only
python3 ~/train_gnn.py --epochs 200 --lr 0.001
python3 ~/train_gnn.py --hidden 128 64    # change hidden layer sizes
```

**Key arguments:**
```
--model        gcn | gat | graphsage | all (default: all)
--epochs       int (default: 150)
--lr           float (default: 0.005)
--weight-decay float (default: 5e-4)
--batch-size   int (default: 32)
--dropout      float (default: 0.3)
--patience     int for early stopping (default: 25)
--hidden       list of ints e.g. 64 32 (default: 64 32)
--seed         int (default: 42)
```

---

## 8. Registration Pipeline Deep-Dive

### NIfTI Header Repair

The root cause of most pipeline failures was degenerate NIfTI affine matrices in ADNI pre-computed FA images. These are produced when DICOM-to-NIfTI conversion tools fail to properly populate the sform/qform fields.

**Symptoms:**
- `flirt` crashes with `inv(): matrix is singular`
- `fnirt` crashes with `inv(): matrix is singular` or `Mismatch between --subsamp and --applyrefmask`
- `convert_xfm` crashes with `Aborted (core dumped)`

**Detection (nibabel):**
```python
img = nib.load(path)
rank = np.linalg.matrix_rank(img.affine[:3, :3])
sform_code = int(img.header.get_sform(coded=True)[1])
zooms = np.array(img.header.get_zooms()[:3])

needs_repair = (
    rank < 3        # degenerate affine
    or sform_code == 0  # no spatial transform defined
    or np.any(zooms <= 0)  # invalid voxel sizes
    or np.any(~np.isfinite(img.affine))  # NaN/Inf in affine
)
```

**Repair:**
Rebuild the 4×4 affine from `pixdim` (voxel sizes), centering the image at the MNI origin. This loses absolute position information but gives FSL a valid matrix to initialize registration from.

```python
safe_zooms = np.where(zooms > 0, zooms, 2.0)
new_affine = np.diag(list(safe_zooms) + [1.0])
new_affine[:3, 3] = -(np.array(img.shape[:3]) * safe_zooms) / 2.0
```

**Note:** The repaired affine is only used for registration initialization. The registration itself finds the correct transform regardless.

### Registration Command

```bash
flirt \
  -in  FA_native.nii \
  -ref $FSLDIR/data/standard/FMRIB58_FA_1mm.nii.gz \
  -out FA_MNI.nii.gz \
  -omat native2mni.mat \
  -dof 12
```

12 DOF (degrees of freedom) = full affine (translation, rotation, scaling, shearing).

### Atlas Resampling Command

```bash
# Write identity.mat first:
echo "1 0 0 0
0 1 0 0
0 0 1 0
0 0 0 1" > identity.mat

flirt \
  -in      AAL_MNI_2mm.nii.gz \
  -ref     FA_MNI.nii.gz \
  -init    identity.mat \
  -applyxfm \
  -interp  nearestneighbour \
  -out     AAL_mni_resampled.nii.gz
```

`nearestneighbour` is mandatory for atlas resampling — linear or spline interpolation would blur ROI boundaries and create intermediate label values.

### Per-ROI Extraction

```bash
for roi_id in $(seq 1 116); do
    fslmaths AAL_mni_resampled.nii.gz \
        -thr $roi_id -uthr $roi_id -bin \
        mask_roi_${roi_id}.nii.gz
    
    voxel_count=$(fslstats mask_roi_${roi_id}.nii.gz -V | awk '{print $1}')
    mean_fa=$(fslstats FA_MNI.nii.gz -k mask_roi_${roi_id}.nii.gz -M)
    
    echo "${roi_id},${mean_fa},${voxel_count}"
    rm mask_roi_${roi_id}.nii.gz
done
```

---

## 9. Debugging History

A detailed record of what went wrong and why — useful for understanding pipeline design choices.

### Problem 1: fnirt "matrix is singular" (368/443 subjects)

**Error:** `Exception thrown with message: inv(): matrix is singular`

**Attempted fixes that did NOT work:**
1. Using `FA_2_FMRIB58_1mm.cnf` config → same error
2. Adding `--subsamp=4,2,1` → fixed the flag mismatch but not the singular matrix
3. Adding `--applyrefmask=1,1,1 --applyinmask=1,1,1` → `Mismatch` error resolved but singular matrix persisted
4. `fslreorient2std` before fnirt → only reorders axes, doesn't fix degenerate affine
5. Normalizing FA intensity range → FA range was 0–1.22 (normal), not the cause

**Root cause:** Degenerate NIfTI sform matrices in the images. The fix (header repair with nibabel) only worked once fnirt was dropped entirely.

**Final fix:** Drop fnirt entirely. Use flirt-only affine registration. Repair headers with nibabel before any FSL call.

### Problem 2: FSLDIR Not Set in Parallel Subshells

**Error:** FSL commands not found when running under `nohup` + GNU parallel.

**Cause:** `.bashrc` is not sourced in non-interactive subshells. FSL's `FSLDIR` and `PATH` modifications only apply in interactive shells.

**Fix:** Explicitly set FSL environment inside each parallel worker:
```bash
export FSLDIR="/home/brett/fsl"
source "${FSLDIR}/etc/fslconf/fsl.sh"
export PATH="${FSLDIR}/bin:$PATH"
export FSLOUTPUTTYPE=NIFTI_GZ
```

### Problem 3: AAL90 vs AAL116 Mismatch

**Error:** 85% streamline skip rate during a tractography test.

**Cause:** AAL90 excludes cerebellar regions. When subjects' streamlines were routed through cerebellum, no matching ROI was found, causing skips.

**Fix:** Switch to AAL116 atlas which includes 26 cerebellar ROIs.

### Problem 4: Parallel Temp File Collisions

**Error:** Random ROI extraction failures when running multiple subjects simultaneously.

**Cause:** All subjects were writing to the same temp mask filename (`roi_tmp_N.nii.gz`).

**Fix:** Namespace temp files by subject ID: `roi_tmp_{subject_id}_{roi_id}.nii.gz`.

### Problem 5: Subject List Lost After Reboot

**Cause:** `/tmp/fa_subjects.txt` is in tmpfs — cleared on reboot/WSL restart.

**Fix:** Always regenerate with the one-liner before running the pipeline:
```bash
for subj in /mnt/f/DTI_Brett6/ADNI/ADNI/*/; do
    [ -d "${subj}/Native_Space_Fractional_Anisotropy_Image" ] && basename "$subj"
done > /tmp/fa_subjects.txt
```

### Problem 6: XML Parser Finding No Diagnoses

**Error:** `extract_labels.py` reported `Labels written: 0 / 443` despite XMLs existing.

**Cause:** The script was looking inside per-subject subfolder XMLs (which are stubs with no clinical data) instead of the loose root-level XMLs named `ADNI_{subject_id}_*.xml`.

**Fix:** Change glob pattern to target only the loose files at the metadata root:
```python
# WRONG — subfolder XMLs are stubs
xmls = sorted(meta_dir.rglob("*.xml"))

# CORRECT — loose files have clinical data
xmls = sorted(Path(METADATA_ROOT).glob(f"ADNI_{subj_id}_*.xml"))
```

**Also:** The XML namespace is on `<project>` (a child element), not on the root `<idaxs>` element. The original parser was extracting namespace from `root.tag` which returned empty string, causing all `root.find()` calls to fail. Fix was to scan all elements for the first namespace.

---

## 10. Label Extraction

### Source

Loose XML files at `F:\DTI_Brett_metadata\ADNI\ADNI\`:
- Named: `ADNI_{subject_id}_{scan_description}_{series_id}_{image_id}.xml`
- There are 13,935 such files (multiple per subject — one per scan series)

### XML Structure

```xml
<idaxs xmlns="http://ida.loni.usc.edu">
  <project xmlns="">
    <subject>
      <subjectIdentifier>002_S_0413</subjectIdentifier>
      <researchGroup>CN</researchGroup>
      <subjectSex>F</subjectSex>
      <subjectInfo item="APOE A1">3</subjectInfo>
      <subjectInfo item="APOE A2">3</subjectInfo>
      <study>
        <subjectAge>87.47</subjectAge>
        <series>
          <dateAcquired>2017-06-21</dateAcquired>
        </series>
      </study>
    </subject>
  </project>
</idaxs>
```

**Namespace issue:** The namespace `xmlns="http://ida.loni.usc.edu"` is on `<idaxs>` but cleared on `<project>` with `xmlns=""`. This means some elements are namespaced and some aren't. The robust fix is to strip/search for namespace dynamically.

### Visit Matching

Each subject may have scans from multiple visits (longitudinal data). The pipeline selects the label from the visit closest in date to the FA scan:

```python
fa_date = datetime.strptime(fa_folder_name.split("_")[0], "%Y-%m-%d")
best = min(parsed_xmls_with_dates,
           key=lambda p: abs((p["date_obj"] - fa_date).days))
```

### Label Distribution (Final — 443 subjects)

| Diagnosis | Count | Label |
|---|---|---|
| CN | 183 | 0 |
| SMC | 22 | 0 |
| EMCI | 66 | 1 |
| MCI | 100 | 1 |
| LMCI | 33 | 1 |
| AD | 39 | 2 |
| **CN/SMC (total)** | **205** | **0** |
| **MCI all types (total)** | **199** | **1** |
| **AD (total)** | **39** | **2** |

### APOE4 Encoding

APOE is encoded as two alleles (A1, A2), each being 2, 3, or 4.
- APOE4 carrier = 1 if either allele is 4 (e4/e3 or e4/e4)
- APOE4 non-carrier = 0

---

## 11. Dataset Preparation

### Node Feature Matrix (per subject): shape (116, 8)

| Index | Feature | Source | Notes |
|---|---|---|---|
| 0 | `mean_fa` | `roi_fa_stats.csv` | Mean FA within ROI in MNI space |
| 1 | `voxel_count` | `roi_fa_stats.csv` | Number of voxels in registered ROI |
| 2 | `centroid_x` | AAL atlas (nibabel) | MNI x-coordinate / 90 (normalised to ~[-1,1]) |
| 3 | `centroid_y` | AAL atlas (nibabel) | MNI y-coordinate / 90 |
| 4 | `centroid_z` | AAL atlas (nibabel) | MNI z-coordinate / 90 |
| 5 | `age` | `labels.csv` | Repeated across all 116 nodes |
| 6 | `sex` | `labels.csv` | M=1, F=0, repeated across all 116 nodes |
| 7 | `apoe4` | `labels.csv` | 0/1, repeated across all 116 nodes |

**Why repeat demographics across all nodes?** This is standard practice in brain GNNs. It allows message passing layers to implicitly weight regions differently based on patient characteristics. Without demographics as node features, the GNN can only distinguish subjects by their FA patterns — it cannot learn, for example, that hippocampal FA reduction is more diagnostic in older APOE4 carriers.

**Why centroid coordinates?** Without spatial coordinates, every node looks identical to the GNN except for its FA value. The GNN has no way to distinguish the hippocampus from the motor cortex. With x/y/z coordinates, spatially consistent patterns of FA reduction (the actual neurobiological signature of AD) become learnable. This was the most critical feature addition.

**Centroid computation:**
```python
img = nib.load(atlas_path)
atlas = img.get_fdata().astype(int)
affine = img.affine

for roi_id in range(1, 117):
    voxels = np.argwhere(atlas == roi_id)    # voxel indices
    centroid_vox = voxels.mean(axis=0)       # mean voxel position
    centroid_mni = affine[:3,:3] @ centroid_vox + affine[:3,3]  # → mm
```

### Normalisation

Z-score normalisation applied per feature per ROI across all subjects:
```python
mean = all_x.mean(axis=0)  # shape (116, 8)
std  = all_x.std(axis=0)   # shape (116, 8)
std[std < 1e-8] = 1.0      # prevent division by zero
x_norm = (x - mean) / std
```

Stats saved to `feat_mean.npy` and `feat_std.npy` for applying to new data at inference.

### Edge Construction: AAL Spatial Adjacency

Two ROIs are connected if their voxels share a face (6-connectivity — no diagonals). The edge structure is computed once from the atlas and is identical for all 443 subjects.

**Result:** 898 directed edges = 449 undirected pairs ≈ 7–8 neighbours per node on average.

**Why shared edges?** Without tractography data, subject-specific connectivity cannot be computed. A population-level fixed prior (spatial adjacency) is the standard approach. An alternative would be downloading a published AAL structural connectivity template (e.g. from Hagmann et al. or PPMI), loadable via `--edge-method template`.

### PyG Data Object Structure

```python
Data(
    x          = FloatTensor (116, 8),   # node features
    edge_index = LongTensor  (2, 898),   # COO format edges
    y          = LongTensor  (1,),       # graph label 0/1/2
    subject_id = str,                    # for stratified splits
    diagnosis  = str,                    # raw diagnosis string
    age        = float,
    sex        = int,
    apoe4      = int,
)
```

---

## 12. GNN Architecture

Three architectures were trained in ablation. All share the same structure except the convolution type.

### Common Architecture

```
Input (116 nodes × 8 features)
       │
       ▼
Conv Layer 1 (8 → 64) + BatchNorm + ReLU/ELU + Dropout(0.3)
       │
       ▼
Conv Layer 2 (64 → 32) + BatchNorm + ReLU/ELU + Dropout(0.3)
       │
       ▼
global_mean_pool (116 nodes → 1 graph-level vector of size 32)
       │
       ▼
Linear (32 → 3)
       │
       ▼
Output (logits for CN, MCI, AD)
```

### GCN — Graph Convolutional Network

```python
GCNConv(in, out)
# Spectral convolution: aggregates neighbor features with normalized adjacency
# A_hat = D^{-1/2} A D^{-1/2}; H' = A_hat * H * W
```
Parameters: ~2,499

### GAT — Graph Attention Network

```python
GATConv(in, out, heads=4, concat=True)  # intermediate layers
GATConv(in, out, heads=1, concat=False)  # final layer
```
4 attention heads for intermediate layers, 1 head for final. Each head learns different attention weights over neighbours.
Parameters: ~9,987

### GraphSAGE — Graph Sample and Aggregate

```python
SAGEConv(in, out)
# Aggregates: h_v = W * concat(h_v, mean(h_u for u in N(v)))
```
Better generalisation for inductive settings (new subjects at test time).
Parameters: ~4,611

### Training Hyperparameters (defaults)

| Parameter | Value | Reason |
|---|---|---|
| Optimizer | Adam | Standard |
| Learning rate | 0.005 | Empirical starting point |
| Weight decay | 5e-4 | L2 regularisation |
| Batch size | 32 | Fits all subjects in ~11 batches |
| Dropout | 0.3 | Moderate regularisation for small dataset |
| Scheduler | ReduceLROnPlateau, patience=10, factor=0.5 | Adaptive LR |
| Early stopping patience | 25 epochs | On val macro F1 |
| Max epochs | 150 | |

---

## 13. Training Strategy

### Data Split

Stratified 80/10/10 split preserving class proportions in each set:
- Train: 353 subjects (CN=163, MCI=159, AD=31)
- Val: 45 subjects (CN=21, MCI=20, AD=4)
- Test: 45 subjects (CN=21, MCI=20, AD=4)

**Critical:** The same split is used for all three models. If each model got a different test set, the ablation comparison would be confounded.

### Imbalance Handling (Two-Pronged)

**1. Weighted Cross-Entropy Loss**

Class weights inversely proportional to class frequency:
```python
weight = [total / (n_classes * count_per_class)]
# CN/SMC: 0.72, MCI: 0.74, AD: 3.80
```
AD misclassifications are penalised ~5× more than CN/MCI misclassifications.

**2. WeightedRandomSampler (Oversampling)**

During training, samples are drawn with probability proportional to their class weight, so each batch sees approximately equal class representation. AD subjects appear ~5× more frequently than their natural proportion.

```python
weights = [total / counts[dataset[i].y.item()] for i in train_indices]
sampler = WeightedRandomSampler(weights, num_samples=len(train_indices), replacement=True)
```

### Early Stopping Metric: Macro F1

Early stopping monitors validation **macro F1**, not validation loss. This is intentional. With imbalanced classes, validation loss can keep improving while the model learns to ignore the AD class (since correct CN/MCI predictions dominate the loss). Macro F1 treats all three classes equally — a model that never predicts AD will have macro F1 = 0.33 regardless of how well it does on CN/MCI.

### Model Selection

Best checkpoint = epoch with highest val macro F1. Loaded for test evaluation.

---

## 14. Results (Initial Run)

### With 1 Feature Per Node (mean FA only)

All three models collapsed to predicting almost exclusively AD (ironically — overcompensated for the class weight). MCI F1 = 0 across all three.

**Confusion matrix example (GCN):**
```
            Predicted
            CN  MCI   AD
True CN  [  3,   0,  18 ]
True MCI [  3,   0,  17 ]
True AD  [  0,   0,   4 ]
```

**Root cause:** With `global_mean_pool` + 1 feature per node, the model reduces to computing a weighted scalar of 116 FA values. This is barely better than using whole-brain mean FA as a single feature. The GNN has no spatial context — it cannot distinguish "low FA in hippocampus" from "low FA in motor cortex."

### With 8 Features Per Node (current)

Training in progress at time of writing. Expected improvement due to:
- Centroid coordinates giving spatial identity to each node
- Voxel count providing ROI size information
- Demographics allowing patient-level conditioning

---

## 15. Class Imbalance Strategy

| Approach | What it does | Implemented |
|---|---|---|
| Weighted loss | Penalises minority class errors more | ✅ |
| Oversampling (WeightedRandomSampler) | AD appears more in each batch | ✅ |
| Macro F1 early stopping | Prevents model ignoring AD | ✅ |
| Stratified split | Equal class proportions in train/val/test | ✅ |
| Data augmentation | Generate synthetic AD graphs | ❌ Not yet |
| SMOTE | Oversample in feature space | ❌ Not yet |

---

## 16. Diagnosis Group Definitions

| Code | Full Name | ADNI Phase | Description | Label |
|---|---|---|---|---|
| CN | Cognitively Normal | All | No cognitive impairment | 0 |
| SMC | Subjective Memory Concern | ADNI3 | Self-reported memory issues, no objective impairment | 0 |
| EMCI | Early Mild Cognitive Impairment | ADNI2/GO | Very mild objective impairment, ADL intact | 1 |
| MCI | Mild Cognitive Impairment | ADNI1 | Objective impairment, no dementia | 1 |
| LMCI | Late Mild Cognitive Impairment | ADNI2/GO | More severe MCI, higher conversion risk | 1 |
| AD | Alzheimer's Disease | All | Dementia meeting NINCDS-ADRDA criteria | 2 |

The consolidation of MCI subtypes (EMCI/MCI/LMCI → label 1) reflects different naming conventions across ADNI phases, not clinically distinct groups. All three represent the intermediate MCI stage on the CN→AD progression spectrum.

---

## 17. Next Steps & Known Issues

### Immediate (before paper write-up)

- [ ] Evaluate 8-feature model — check if spatial features fix the collapse issue
- [ ] If still poor: try `--edge-method fully_connected` (allows all-pairs message passing)
- [ ] Consider FA threshold (0.2) to remove non-WM voxels before ROI extraction
- [ ] Process remaining DTI_Brett* folders (DTI_Brett through DTI_Brett9) with `adni_pipeline.py --all` to increase dataset size

### Model Improvements

- [ ] Add residual connections between GNN layers
- [ ] Try deeper networks (3–4 layers) with skip connections
- [ ] Experiment with `--hidden 128 64 32` 
- [ ] Add edge features (Euclidean distance between ROI centroids)
- [ ] Try a published AAL structural connectivity template as edge prior

### Evaluation Improvements

- [ ] Switch from single 80/10/10 split to 5-fold stratified cross-validation for more reliable estimates
- [ ] Report 95% confidence intervals across folds
- [ ] Add ROC-AUC per class
- [ ] Interpretability: GNNExplainer to identify which ROIs drive predictions

### Data Improvements

- [ ] Add FA threshold (0.2–0.3) to mask non-WM voxels — currently skipped
- [ ] Normalise centroid coordinates using actual MNI brain extent rather than hardcoded ±90mm
- [ ] For the 12 subjects with raw DWI: run full tractography pipeline and add as edge features

### Known Limitations for Methods Section

1. Pre-computed FA maps from ADNI — cannot verify upstream preprocessing parameters (b-value, diffusion directions, eddy correction method)
2. Affine-only registration (no nonlinear) — standard for ROI-level but not state-of-art for voxel-level
3. Fixed spatial adjacency edges — no subject-specific connectivity (no tractography)
4. Single timepoint per subject — ADNI is longitudinal but only baseline scan used
5. Small AD class (n=39) — limits statistical power for AD-specific findings

---

## Appendix: Environment & Dependencies

### System

- OS: Windows 11 with WSL2 (Ubuntu 24)
- CPU: 6 cores
- GPU: CUDA-capable (confirmed `Device: cuda` during training)
- FSL: installed at `/home/brett/fsl`

### Key Paths

```bash
FSL_HOME   = "/home/brett/fsl"
AAL_ATLAS  = "/home/brett/atlases/AAL_MNI_2mm.nii.gz"
REF_FA     = "/home/brett/fsl/data/standard/FMRIB58_FA_1mm.nii.gz"
ADNI_ROOT  = "/mnt/f/DTI_Brett6/ADNI/ADNI"
META_ROOT  = "/mnt/f/DTI_Brett_metadata/ADNI/ADNI"
OUT_ROOT   = "/mnt/e/adni_batch"
```

### Python Dependencies

```bash
pip install nibabel          # NIfTI I/O, header repair
pip install torch            # PyTorch
pip install torch-geometric  # PyG (GCN, GAT, SAGEConv, DataLoader)
pip install scikit-learn     # stratified splits, F1, confusion matrix
pip install matplotlib       # training curves plot
pip install numpy            # array operations
```

### Useful Commands

```bash
# Check FSL is available
which flirt && flirt -version

# Check nibabel
python3 -c "import nibabel; print(nibabel.__version__)"

# Check PyG
python3 -c "import torch_geometric; print(torch_geometric.__version__)"

# Count processed subjects
ls /mnt/e/adni_batch/*/node_features.csv | wc -l

# Kill a running pipeline
pkill -f run_adni_extraction; pkill -f parallel; pkill -f adni_pipeline

# Inspect a NIfTI header
fslinfo /path/to/image.nii | grep -E "^dim|^vox|^sform|^qform"

# Check FSL registration quality visually
fsleyes FA_MNI.nii.gz $FSLDIR/data/standard/FMRIB58_FA_1mm.nii.gz &
```
