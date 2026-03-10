# ADNI DTI Graph Learning Pipeline
### Alzheimer's Disease Classification using Diffusion MRI and Graph Neural Networks

---

# Overview

This repository implements a **full end-to-end research pipeline** for studying Alzheimer's disease using **Diffusion Tensor Imaging (DTI)** from the **ADNI dataset**.

The pipeline converts diffusion MRI scans into **ROI-level brain graphs** and trains **Graph Neural Networks** to classify disease stages:

- **CN / SMC** — Cognitively Normal
- **MCI** — Mild Cognitive Impairment
- **AD** — Alzheimer's Disease

The project includes:

1. Automated **DTI preprocessing**
2. **Tractography-based structural connectivity**
3. **ROI feature extraction** across multiple diffusion scalars
4. Construction of **graph datasets**
5. Training and evaluation of **graph neural networks**

---

# Pipeline Overview

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
ROI Scalar Feature Extraction
      │
      ▼
Graph Construction (116 AAL nodes)
      │
      ▼
PyTorch Geometric Dataset
      │
      ▼
Graph Neural Network Training
```

Each **visit becomes one graph sample**.

---

# Diffusion Scalars Used

The pipeline extracts four standard DTI scalar measures.

| Scalar | Meaning |
|------|------|
| **FA** | Fractional Anisotropy |
| **MD** | Mean Diffusivity |
| **RD** | Radial Diffusivity |
| **AD** | Axial Diffusivity |

For each scalar and each ROI we compute:

- mean
- standard deviation
- min
- max

These capture **microstructural changes in white matter** associated with neurodegeneration.

---

# Graph Representation

Each visit is represented as a graph.

**Nodes**

- 116 brain regions (AAL atlas)

**Node Features**

- FA mean / std
- MD mean / std
- RD mean / std
- AD mean / std
- voxel count
- ROI centroid
- demographics (age, sex, APOE4)

**Edges**

Primary approach:

- **AAL spatial adjacency**

Alternative graph construction options:

- **k-nearest neighbor graphs**
- **fully connected graphs**
- **tractography-derived connectivity (future work)**

---

# Repository Structure

| File | Description |
|-----|-------------|
| `process_multiscalar_visits.py` | Full DTI preprocessing + ROI scalar extraction |
| `build_graph.py` | Builds ROI adjacency matrices |
| `prepare_multiscalar_dataset.py` | Converts visits into PyTorch Geometric graphs |
| `train_gnn_grouped.py` | Trains GCN / GAT / GraphSAGE models |
| `diagnose_missing_visit_labels.py` | Diagnoses metadata mismatches |
| `build_visit_manifest.py` | Builds global ADNI visit manifest |
| `refresh_visit_metadata.py` | Injects metadata labels into visits |

---

# Dataset Format

Processed visits are stored as:

```
adni_multiscalar_visits/

    subject_visit/
        roi_fa_stats.csv
        roi_md_stats.csv
        roi_rd_stats.csv
        roi_ad_stats.csv

        AAL_resampled.nii.gz
        metadata.json
```

Each visit folder contains:

- ROI diffusion statistics
- atlas alignment
- demographic metadata
- diagnosis label

---

# Dataset Creation

Graphs are generated using:

```bash
python3 prepare_multiscalar_dataset.py \
  --visits-root /mnt/e/adni_multiscalar_visits \
  --out-dataset /mnt/e/adni_multiscalar_dataset.pt \
  --include-stats mean std \
  --include-voxel-count \
  --include-centroids \
  --include-demographics \
  --edge-method aal_spatial \
  --normalize
```

Output:

```
adni_multiscalar_dataset.pt
```

A **PyTorch Geometric dataset** of brain graphs.

---

# Graph Neural Network Training

Implemented models:

| Model | Description |
|------|------|
| **GCN** | Graph Convolutional Network |
| **GAT** | Graph Attention Network |
| **GraphSAGE** | Aggregation-based GNN |

Training uses **subject-grouped splits** to avoid leakage across visits.

Example:

```bash
python3 train_gnn_grouped.py \
  --dataset /mnt/e/adni_multiscalar_dataset.pt \
  --model all \
  --test-size 0.2
```

Evaluation outputs:

- Accuracy
- Macro F1
- Per-class F1
- Confusion matrix

---

# Example Dataset Statistics

Example partial dataset:

```
Graphs: 100 visits

Class distribution:
CN / SMC : 53
MCI      : 40
AD       : 7
```

Grouped split example:

```
Train
CN : 42
MCI: 32
AD : 6

Test
CN : 11
MCI: 8
AD : 1
```

---

# Literature Study of DTI Preprocessing Pipelines

To design the preprocessing pipeline, a **large literature review of diffusion MRI pipelines** was conducted across multiple research papers.

The goal was to identify **common preprocessing steps, tools, and parameter ranges** used in Alzheimer's disease DTI studies.

---

# Cross-Paper Synthesis

## Most Common Preprocessing Steps (Ranked by Frequency)

| Rank | Step | Frequency | Tools |
|----|----|----|----|
| 1 | Eddy current & motion correction | Nearly universal | FSL `eddy`, MRtrix3 |
| 2 | Tensor fitting (FA/MD) | High | FSL `dtifit`, Dipy |
| 3 | Skull stripping | High | FSL BET, ROBEX, BrainSuite |
| 4 | Resampling to isotropic voxels | Common | FSL, ANTs |
| 5 | Registration to standard space | High | FSL FLIRT/FNIRT, ANTs |
| 6 | Fiber tractography | Moderate | MRtrix3, Dipy, PANDA |
| 7 | Denoising | Moderate | MRtrix3 MP-PCA |
| 8 | ROI extraction | Moderate | AAL, FMRIB58_FA |
| 9 | Cropping volumes | Moderate | FSL `fslroi` |
| 10 | Data augmentation | Low | TorchIO, GANs |

---

# Most Common Tools in the Literature

| Tool | Frequency | Main Use |
|------|------|------|
| **FSL** | High | Eddy correction, skull stripping, registration |
| **MRtrix3** | High | Denoising, tractography |
| **PANDA** | High | Automated DTI pipeline |
| **Dipy** | High | Tensor fitting, tractography |
| **ANTs** | Medium | Nonlinear registration |
| **pyradiomics** | Medium | ROI feature extraction |
| **BrainSuite** | Medium | Brain segmentation |
| **ROBEX** | Medium | Skull stripping |
| **MNInu_correcttool** | Medium | Intensity normalization |
| **N3** | Low | Bias field correction |
| **TorchIO / Kornia** | Low | Data augmentation |

---

# Parameter Ranges Observed Across Papers

| Parameter | Common Range | Notes |
|------|------|------|
| **b-values** | 1000–2000 s/mm² | Some studies use 500–1000 |
| **diffusion directions** | 32–127 | High-end studies use ~100 |
| **voxel size** | 1–2.5 mm isotropic | Depends on scanner protocol |
| **FA threshold** | 0.2–0.3 | Used for tractography |
| **templates** | MNI152, FMRIB58_FA | Some use ENIGMA-DTI |

---

# Comparison With Literature DTI Pipelines

To ensure the preprocessing pipeline follows accepted practices, a study of multiple diffusion MRI papers was conducted.  
The table below compares **common steps reported in the literature** with **what this pipeline currently implements**.

---

## Preprocessing Pipeline Comparison

| Preprocessing Step | Literature Frequency | Tools Used in Papers | Implemented in This Pipeline | Implementation Details |
|--------------------|---------------------|----------------------|-------------------------------|------------------------|
| **DICOM → NIfTI Conversion** | Standard | `dcm2niix` | ✅ Yes | `dcm2niix` used for ADNI conversion |
| **Eddy Current Correction** | Nearly universal | FSL `eddy`, MRtrix3 | ✅ Yes | FSL `eddy` |
| **Motion Correction** | Nearly universal | FSL `eddy` | ✅ Yes | Handled by `eddy` |
| **Distortion Correction (Topup / Fieldmap)** | Common in newer studies | FSL `topup`, Synb0-DisCo | ⚠ Partial | Acquisition parameters used but full reverse phase-encoding correction not always available |
| **Tensor Fitting** | High | FSL `dtifit`, Dipy | ✅ Yes | FSL `dtifit` |
| **FA / MD / RD / AD Scalar Maps** | High | FSL, MRtrix3, Dipy | ✅ Yes | All four scalars extracted |
| **Skull Stripping** | High | FSL BET, ROBEX, BrainSuite | ✅ Yes | FSL BET |
| **Denoising** | Moderate | MRtrix3 `dwidenoise` | ❌ Not yet | Planned improvement |
| **Gibbs Ringing Correction** | Moderate | MRtrix3 `mrdegibbs` | ❌ Not yet | Planned improvement |
| **Bias Field Correction** | Moderate | ANTs N4, N3 | ❌ Not yet | Could be added later |
| **Resampling to Isotropic Voxels** | Common | FSL, ANTs | ✅ Yes | Resampled during preprocessing |
| **Registration to Standard Space** | High | FSL FLIRT/FNIRT, ANTs | ✅ Yes | FSL FLIRT + FNIRT to MNI space |
| **Cropping / Volume Normalization** | Moderate | FSL `fslroi` | ⚠ Partial | Some cropping performed |
| **Fiber Tractography** | Moderate | MRtrix3, Dipy, PANDA | ⚠ Partial | Streamlines generated but not always used for graph edges |
| **ROI Extraction** | Moderate | AAL, FMRIB58_FA | ✅ Yes | AAL atlas with 116 regions |
| **Radiomics Feature Extraction** | Moderate | `pyradiomics` | ❌ No | Instead ROI statistical summaries used |
| **Graph Construction** | Moderate | Structural connectivity networks | ✅ Yes | Graph built from AAL spatial adjacency |
| **Data Augmentation** | Low | TorchIO, GANs | ❌ No | Not used |

---

# Feature Extraction Comparison

Many studies extract **radiomics features or connectivity metrics**.  
This pipeline instead focuses on **diffusion scalar statistics per ROI**.

| Feature Type | Used in Literature | Used in This Pipeline | Notes |
|--------------|------------------|----------------------|------|
| FA mean | Yes | ✅ Yes | Standard biomarker |
| FA variance/std | Sometimes | ✅ Yes | Captures heterogeneity |
| MD statistics | Yes | ✅ Yes | Diffusivity indicator |
| RD statistics | Yes | ✅ Yes | Demyelination indicator |
| AD statistics | Yes | ✅ Yes | Axonal damage indicator |
| Radiomics features | Moderate | ❌ No | Could be added later |
| Connectivity strength | Moderate | ⚠ Planned | Requires tractography edges |
| Demographics | Rare | ✅ Yes | Age, sex, APOE4 |

---

# Graph Construction Comparison

| Graph Method | Used in Literature | Used Here | Notes |
|--------------|-------------------|----------|------|
| Structural connectivity graphs | Common | ⚠ Planned | Requires tractography connectivity matrix |
| Atlas adjacency graphs | Rare | ✅ Yes | Current implementation |
| Fully connected graphs | Rare | ⚠ Experimental | Available option |
| kNN graphs | Rare | ⚠ Experimental | Available option |

Current default:

```
AAL spatial adjacency graph
116 nodes
ROI scalar features
```

---

# Parameter Comparison

| Parameter | Literature Range | This Pipeline |
|----------|-----------------|---------------|
| b-values | 1000–2000 s/mm² | ADNI acquisition protocol |
| diffusion directions | 32–127 | ADNI acquisition protocol |
| voxel size | 1–2.5 mm isotropic | Resampled to standard grid |
| FA threshold | 0.2–0.3 | Not required (no tract filtering yet) |
| atlas | AAL / FMRIB58_FA | AAL (116 ROIs) |

---

# Key Differences From Typical Literature Pipelines

### 1. Graph Learning Focus
Most studies perform **voxel-based classification**.  
This project instead uses **brain graph representations with GNNs**.

### 2. Multi-Scalar Node Features
Instead of using only FA:

```
FA
MD
RD
AD
```

All four scalars are used.

### 3. ROI Statistical Features
Instead of radiomics feature sets, this pipeline uses:

```
mean
std
min
max
```

per scalar per ROI.

### 4. Demographic Feature Integration
Demographic metadata is integrated directly into graph node features.

---

# Potential Future Improvements

Based on the literature review, the following steps could improve the pipeline:

| Improvement | Benefit |
|-------------|--------|
| MRtrix3 denoising | Improved signal quality |
| Gibbs ringing removal | Cleaner diffusion signal |
| ANTs N4 bias correction | Better intensity normalization |
| Tractography connectivity graphs | More biologically meaningful graph edges |
| Radiomics features | Richer ROI feature sets |
| Graph Transformers | Potentially stronger performance |

---

# Summary

The current pipeline implements **most core diffusion preprocessing steps used in the literature**, while introducing several **novel aspects**:

- multi-scalar ROI features
- graph neural network models
- subject-grouped training splits
- automated dataset construction

The system is designed to be **extensible**, allowing future improvements such as tractography-based connectivity graphs and radiomics features.

# Key Challenges

### Small datasets
DTI preprocessing is computationally expensive.

### Label synchronization
ADNI metadata must be matched with imaging visit dates.

### Class imbalance
AD cases are often under-represented.

### CN vs MCI overlap
Structural diffusion changes are subtle.

---

# Environment Setup

Python dependencies:

```bash
pip install torch torch-geometric nibabel numpy pandas scikit-learn
```

Neuroimaging dependencies:

```
FSL
MRtrix3
```

---

# Future Work

Planned improvements include:

- larger ADNI dataset processing
- tractography-derived graph edges
- multimodal fusion (MRI + DTI)
- Graph Transformer models
- longitudinal modeling across visits

---

# Research Goal

The long-term goal is to determine whether **multi-scalar diffusion brain graphs combined with graph neural networks** can improve early detection of **Alzheimer's disease progression**.