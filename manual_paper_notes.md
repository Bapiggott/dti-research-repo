# Manual DTI Preprocessing Notes — 10 Paper Ground Truth

These notes were hand-reviewed and serve as the ground truth for validating the automated RAG extraction pipeline (`paper_dti1.py`).

---

## Paper 1 — A Multi-View DTI Feature Fusion Framework for Enhanced Diagnosis of Alzheimer's Disease

**Tool:** FSL (FDT)  
**Data format:** NIfTI DTI  
**Steps:**
- Estimated fieldmap for distortion correction using phase info from dual spin-echo images
- Used distortion-corrected b0 (b=0) as reference
- Skull stripping with BET (intensity threshold = 0.3) to generate brain mask
- Eddy current + subject motion correction simultaneously using estimated fieldmap
- Aligned and undistorted all diffusion images
- Tensor fitting via linear least squares → FA and MD maps

---

## Paper 2 — Classification Study of Alzheimer's Disease Based on Self-Attention Mechanism and DTI Imaging Using GCN

**Tools:** FSL, PANDA  
**Steps:**
- Converted ADNI diffusion data to NIfTI (.nii.gz) using FSL
- Skull stripping + eddy-current correction via FSL/PANDA
- Computed FA and MD maps using FSL
- Deterministic tractography in PANDA → whole-brain white matter fiber bundles
- Applied AAL atlas → 90 ROIs, each as a graph node

**Three structural brain networks constructed:**
- FA network: edge weight = average FA between ROI pairs
- FN network: edge weight = fiber count between ROIs
- LEN network: edge weight = average fiber length between ROIs

**Node features:**
- ROIS (ROISurfaceSize): voxels traversed by fibers within each ROI
- ROIV (ROIVoxelSize): total voxels in each ROI

---

## Paper 3 — Alzheimer's Disease Prediction via Brain Structural-Functional Deep Fusing Network

No preprocessing details reported.

---

## Paper 4 — Diagnosis of Alzheimer's Disease Based on Structural Graph Convolutional Neural Networks

No DTI preprocessing details. Notes FSL FLIRT used for FDG-PET registration.

---

## Paper 5 — DTI versus NODDI White Matter Microstructural Biomarkers of Alzheimer's Disease

**Tool:** FSL  
**Method:** Weighted least squares for DTI computation

---

## Paper 6 — Enhancing Alzheimer's Disease Diagnosis: A Novel Low-HRNet Approach

**Note:** Does not actually use DTI — uses fMRI only. Mentioned wanting to include DTI in future work. No preprocessing details relevant to DTI.

---

## Paper 7 — Graph Transformer Geometric Learning of Brain Networks Using Multimodal MR Images for Brain Age Estimation

**Tools:** FSL, PANDA (suite 1.2.4)  
**Steps:**
- N3 algorithm for initial bias field correction (sMRI)
- Distortion correction, FOV reduction, brain extraction, registration via FSL
- Brain extraction with FSL BET → registered to MNI152 1mm via FNIRT
- Eddy-current + head motion correction (method from referenced paper)
- PANDA 1.2.4 for eddy-current-induced distortion + simple head-motion correction
- DTI fitting → FA maps
- Image alignment and cropping to match sMRI volumes
- Final crop: 160 × 192 × 160

---

## Paper 8 — Harnessing Machine Learning for Early Detection of Alzheimer's Disease

No preprocessing pipeline details.  
Notes: FA values extracted from ROIs using standard anatomical templates; ROIs chosen based on prior AD vulnerability studies.

---

## Paper 9 — Multimodal Neuroimaging for Early Alzheimer's Detection: A Deep Learning Approach

No preprocessing pipeline details.  
Notes: Mentions tailored preprocessing pipelines for each modality (sMRI, fMRI, DTI) but provides no specifics.

---

## Paper 10 — PreQual: An Automated Pipeline for Integrated Preprocessing and Quality Assurance of Diffusion Weighted MRI Images

*(Specifically searched for as a preprocessing methodology reference)*  
Full pipeline tool covering integrated preprocessing + QA for DWI.
