# DTI Preprocessing Research — ADNI Alzheimer's Disease Project

## Overview

This repository documents the progress made in building a DTI (Diffusion Tensor Imaging) preprocessing pipeline for Alzheimer's disease research using the ADNI dataset. The work spans manual paper review, automated pipeline extraction using a local RAG system, and hands-on FSL preprocessing scripting.

---

## Repository Contents

| File | Description |
|------|-------------|
| `process_dti.sh` | FSL-based DTI preprocessing shell script (DICOM → FA map → MNI space) |
| `paper_dti1.py` | Local RAG pipeline (Ollama + qwen3) to extract DTI preprocessing steps from ~40 PDFs |
| `dti_pipeline_results1.md` | Auto-generated synthesis of preprocessing steps across ~40 papers |
| `manual_paper_notes.md` | Hand-reviewed notes from 10 papers used as ground truth |

---

## Progress Summary

### Phase 1 — Manual Literature Review (10 Papers)
Reviewed 10 Alzheimer's/DTI papers by hand and extracted preprocessing details. Key findings:
- Nearly all papers use **FSL** as the core toolchain
- **Eddy current correction** and **skull stripping (BET)** are near-universal
- Several papers use **PANDA** for tractography on top of FSL
- Reporting quality varies widely — many papers omit key parameters

### Phase 2 — FSL + PANDA Setup
Built a Linux VM environment and installed:
- **MATLAB** (required by PANDA)
- **FSL** (FMRIB Software Library)
- **PANDA** (Pipeline for Analyzing braiN Diffusion imAges)

Converted DICOM → NIfTI via `dcm2niix`, producing:
- `dwi.nii.gz` — 4D diffusion-weighted image
- `dwi.bval` — b-values per volume
- `dwi.bvec` — gradient direction vectors

**Current blocker:** PANDA errors out during FA (Fractional Anisotropy) map generation. PANDA has very limited documentation, making debugging difficult.

### Phase 3 — Automated Pipeline Extraction (~40 Papers)
Due to PANDA's limited docs, expanded the literature review to ~40 papers to survey alternative tools. Used a fully local RAG pipeline (`paper_dti1.py`) powered by Ollama (qwen3:8b + qwen3-embedding) to extract preprocessing steps automatically, using the 10 hand-reviewed papers as ground truth validation.

---

## Pipeline Comparison: `process_dti.sh` vs. Literature Common Steps

The table below compares what the current shell script implements against what the ~40-paper synthesis (`dti_pipeline_results1.md`) identifies as the most common steps in the literature.

| Step | `process_dti.sh` | Literature Frequency | Notes |
|------|-----------------|----------------------|-------|
| **DICOM → NIfTI conversion** | ✅ `dcm2niix` | Standard | `dcm2niix` is the de facto standard |
| **Skull stripping** | ✅ `bet` (threshold 0.3) | High — FSL-BET, ROBEX, BrainSuite | BET threshold of 0.3 matches reported norms |
| **Eddy current + motion correction** | ✅ `eddy --repol` | Nearly universal | `--repol` for outlier replacement is best practice |
| **Distortion correction (fieldmap)** | ⚠️ Partial — acqparams from JSON only | Common in recent papers | Script uses acqparams but lacks a paired reverse-PE b0 for full topup correction |
| **Tensor fitting → FA/MD maps** | ✅ `dtifit` | High — OLS/WLS methods | Script uses default linear LS via `dtifit` |
| **Registration to standard space** | ✅ `flirt` + `fnirt` (MNI152 1mm) | High — MNI152, FMRIB58_FA, ENIGMA-DTI | Both affine (FLIRT) and nonlinear (FNIRT) applied |
| **Cropping to fixed dimensions** | ✅ `fslroi` → 160×192×160 | Moderate | Matches dimensions used in graph transformer papers |
| **Denoising (MP-PCA / Gibbs)** | ❌ Not implemented | Moderate — MRtrix3 `dwidenoise`, `mrdegibbs` | Common in more recent pipelines |
| **Bias field / intensity correction** | ❌ Not implemented | Moderate — N3, ANTs | Often applied to sMRI; less common but present in DTI pipelines |
| **Fiber tractography** | ❌ Not implemented | Moderate — PANDA, MRtrix3, Dipy | Required for FN/LEN network features |
| **ROI extraction (AAL/atlas)** | ❌ Not implemented | Moderate — AAL, FMRIB58_FA | Needed for graph-based models |
| **Data augmentation** | ❌ Not implemented | Low — GANs, TorchIO | Optional, model-dependent |

### Key Gaps to Address
1. **Full distortion correction**: Consider `topup` with a reverse phase-encoding b0 for proper susceptibility distortion correction.
2. **Denoising**: Adding `dwidenoise` (MRtrix3) before eddy correction is increasingly standard.
3. **Tractography**: Required if building structural connectivity networks (FA/FN/LEN networks for GCN models).
4. **ROI extraction**: Needed for graph-based classification approaches using AAL or similar atlases.

---

## Tools Referenced Across Literature

| Tool | Frequency | Primary Use |
|------|-----------|-------------|
| FSL | High | Eddy, BET, FLIRT/FNIRT, dtifit |
| MRtrix3 | High | Denoising, tractography, tensor fitting |
| PANDA | High | DTI preprocessing + fiber tracking |
| Dipy | High | Tensor fitting, tractography |
| ANTs | Medium | Nonlinear registration |
| dcm2niix | Standard | DICOM → NIfTI |

---

## Environment Setup

```bash
# OS: Ubuntu (VM required on Windows due to FSL restrictions)
# Dependencies:
#   - FSL (https://fsl.fmrib.ox.ac.uk/)
#   - MATLAB (required for PANDA)
#   - PANDA (http://nmr.mgh.harvard.edu/~mschuber/PANDA.html)
#   - dcm2niix
#   - Python: pip install pypdf ollama numpy

# For paper_dti1.py (local RAG):
#   ollama pull qwen3:8b
#   ollama pull qwen3-embedding:latest
```

---

## Next Steps
- [ ] Debug PANDA FA generation error
- [ ] Add `topup` for full distortion correction
- [ ] Add MRtrix3 denoising step
- [ ] Evaluate alternative to PANDA (MRtrix3 or Dipy for tractography)
- [ ] Implement ROI extraction with AAL atlas
