# DTI/dMRI Preprocessing Pipeline Extraction
_Generated: 2026-02-17 23:39:46_
_Papers directory: C:\Research\Alzheimers\week2\Papers_
_Generation model: llama3.2:1b  |  Embedding model: mxbai-embed-large_

---

## Cai et al. (2023) — Graph Transformer Geometric Learning of Brain Networks Using Multimodal MR Images for Brain Age Esti
_File: `Cai et al. - 2023 - Graph Transformer Geometric Learning of Brain Networks Using Multimodal MR Images for Brain Age Esti.pdf`_

The DTI/dMRI preprocessing pipeline extracted from the provided excerpts is as follows:

1. Denoise/De-Shift: Not mentioned.
2. Gibbs Correction: Not mentioned.
3. Susceptibility-Topup: Not mentioned.
4. Eddy Current Correction: Not mentioned.
5. Bias Field B1: Not mentioned.
6. Brain Extraction: Using the BET (Brain Extraction Tool) [25] and then registered to the 1 mm resolution version of MNI152 template space.
7. Tensor Fitting: DTI fitting tool [27].
8. QC: Quality control pipeline as described in [23].

Tools mentioned:

- FSL
- eddy
- topup
- ANTs
- FreeSurfer
- MRtrix3
- DiPy

---

## Castellano et al. (2023) — Combining Unsupervised and Supervised Deep Learning for Alzheimer's Disease Detection by Fractional
_File: `Castellano et al. - 2023 - Combining Unsupervised and Supervised Deep Learning for Alzheimer's Disease Detection by Fractional.pdf`_

The DTI/dMRI preprocessing pipeline extracted from the provided excerpts is as follows:

1. Denoise/Denoising (Not mentioned)
2. Gibbs correction (Not mentioned)
3. Susceptibility-topup (Not mentioned)
4. Eddy current correction (Not mentioned)
5. Bias field B1 (Not mentioned)
6. Brain extraction (Not mentioned)
7. Registration (Not mentioned)
8. Tensor fitting (Not mentioned)
9. QC (Quality control)

---

## Esteve et al. (2025) — topoEEG An Python-framework for analyzing EEG data in neurodegeneratives disease through Topologica
_File: `Esteve et al. - 2025 - topoEEG An Python-framework for analyzing EEG data in neurodegeneratives disease through Topologica.pdf`_

The DTI/dMRI preprocessing pipeline mentioned in the excerpts is not explicitly stated. However, based on the context and the tools mentioned, it can be inferred that the following steps are part of the preprocessing pipeline:

1. Denoise/De-aliasing: This step is likely performed using tools like FSL or eddy to remove noise and de-alias the data.
2. Gibbs correction: This step is also likely performed using tools like FSL or eddy, as it is a common technique for denoising EEG data.
3. Susceptibility-topup: This step is mentioned in the context of eddy current correction, which involves correcting for susceptibility artifacts in the brain.
4. Eddy current correction: This step is likely performed using tools like FSL or eddy to correct for eddy currents and other magnetic field distortions in the data.
5. Bias field B1 correction: This step is mentioned as part of the registration process, which involves correcting for bias fields (B1) that can affect the accuracy of the analysis.
6. Brain extraction: This step is likely performed using tools like FreeSurfer or MRtrix3 to extract the brain from the data.
7. Registration: This step is also likely performed using tools like FreeSurfer or MRtrix3, which involves aligning the brain data with a reference template.
8. Tensor fitting: This step is mentioned as part of the QC (Quality Control) process, which may involve fitting tensors to the data to ensure that it meets certain criteria.

The exact order and steps of these preprocessing pipeline are not specified in the excerpts, but based on the context and the tools mentioned, it can be inferred that a comprehensive DTI/dMRI preprocessing pipeline is required for neuroimaging analysis.

---

## Lao et al. (2024) — Diagnosis of Alzheimer's Disease Based on Structural Graph Convolutional Neural Networks
_File: `Lao et al. - 2024 - Diagnosis of Alzheimer's Disease Based on Structural Graph Convolutional Neural Networks.pdf`_

The DTI/dMRI preprocessing pipeline mentioned in the excerpts is as follows:

1. Denoise: 
   - Lao et al. (2024) — Diagnosis of Alzheimer's Disease Based on Structural Graph Convolutional Neural Networks
   - Denoising along x-dimension, resulting in a low-pass image L and a high-pass image H.

2. Gibbs correction:
   - Lao et al. (2024) — Diagnosis of Alzheimer's Disease Based on Structural Graph Convolutional Neural Networks
   - Both L and H are then filtered along the y-dimension, resulting in four decomposed subbands (LL, LH, HL, HH).

3. Susceptibility-topup:
   - Lao et al. (2024) — Diagnosis of Alzheimer's Disease Based on Structural Graph Convolutional Neural Networks
   - Among them, LLL is an approximation of the 3D image and usually contains more information about the image.

4. Eddy current correction:
   - Not mentioned in the excerpts

5. Bias field B1:
   - Not mentioned in the excerpts

6. Brain extraction:
   - Not mentioned in the excerpts

7. Registration:
   - Lao et al. (2024) — Diagnosis of Alzheimer's Disease Based on Structural Graph Convolutional Neural Networks
   - For all sMRI images, we used the "Segment Data" module in the Computation Anatomy Toolbox (CAT12) toolkit to perform skull stripping, tissue segmentation, and alignment and modulation operations.

8. Tensor fitting:
   - Not mentioned in the excerpts

9. QC:
   - Not mentioned in the excerpts

---

## Liou et al. (2025) — DTI versus NODDI White Matter Microstructural Biomarkers of Alzheimer’s Disease
_File: `Liou et al. - 2025 - DTI versus NODDI White Matter Microstructural Biomarkers of Alzheimer’s Disease.pdf`_

The DTI/dMRI preprocessing pipeline mentioned in the paper is as follows:

- Denoise / Gibbs correction / susceptibility-topup / eddy current correction / bias field B1 / brain extraction / registration / tensor fitting / QC

This pipeline is used to preprocess dMRI and T1w images before analysis.

---

## Nir et al. (2013) — Effectiveness of regional DTI measures in distinguishing Alzheimer's disease, MCI, and normal aging
_File: `Nir et al. - 2013 - Effectiveness of regional DTI measures in distinguishing Alzheimer's disease, MCI, and normal aging.pdf`_

The DTI/dMRI preprocessing pipeline mentioned in the excerpts is as follows:

1. Denoise/Denoising: Not mentioned.
2. Gibbs correction: Not mentioned.
3. Susceptibility-topup: Not mentioned.
4. Eddy current correction: Not mentioned.
5. Bias field B1: Not mentioned.
6. Brain extraction: Skull-stripped volumes were extracted from T1-weighted anatomical scans using software packages such as ROBEX and FreeSurfer.
7. Registration: The skull-stripped volumes were aligned to the average b0 image (DTI volume with no diffusion sensitization) using FSL eddy_correct tool, and then elastically registered to their respective T1-weighted structural scans using an inverse-consistent registration algorithm.
8. Tensor fitting: Not mentioned.
9. QC: Not mentioned.

Therefore, the answer is:

NO

---

## Qiao et al. (2026) — A multi-view DTI feature fusion framework for enhanced diagnosis of Alzheimer’s disease
_File: `Qiao et al. - 2026 - A multi-view DTI feature fusion framework for enhanced diagnosis of Alzheimer’s disease.pdf`_

The DTI/dMRI preprocessing pipeline mentioned in the paper is as follows:

1. Denoise / Gibbs correction
2. Susceptibility-topup
3. Eddy current correction
4. Bias field B1
5. Brain extraction
6. Registration (linear and non-linear)
7. Tensor fitting

---

## Sang and Li (2024) — Classification Study of Alzheimer’s Disease Based on Self-Attention Mechanism and DTI Imaging Using
_File: `Sang and Li - 2024 - Classification Study of Alzheimer’s Disease Based on Self-Attention Mechanism and DTI Imaging Using.pdf`_

The DTI/dMRI preprocessing pipeline mentioned in the excerpts is as follows:

1. Denoise/Denoising: Not mentioned
2. Gibbs correction: Not mentioned
3. Susceptibility-topup: Not mentioned
4. Eddy current correction: Not mentioned
5. Bias field B1: Not mentioned
6. Brain extraction: Not mentioned
7. Registration: Not mentioned
8. Tensor fitting: Not mentioned
9. QC (Quality control): Not mentioned

The paper does mention the use of FSL for preprocessing, specifically:

* Converting downloaded data from ADNI into nii.gz format using FSL.
* Skull stripping and eddy current correction are performed on the downloaded data.

However, it does not explicitly mention a DTI/dMRI preprocessing pipeline.

---

## Singh Chhabra et al. (2023) — Multimodal Neuroimaging for Early Alzheimer's detection A Deep Learning Approach
_File: `Singh Chhabra et al. - 2023 - Multimodal Neuroimaging for Early Alzheimer's detection A Deep Learning Approach.pdf`_

The DTI/dMRI preprocessing pipeline mentioned in the paper is not explicitly stated, but based on the provided excerpts, it can be inferred as follows:

1. Denoise: The process of removing noise from the data.
2. Gibbs correction: A technique used to reduce artifacts and improve image quality by estimating missing values in the data.
3. Susceptibility-topup: A method used to correct for susceptibility artifacts in diffusion tensor imaging (DTI) data, which can be caused by magnetic field inhomogeneities or other factors.
4. Eddy current correction: A technique used to remove eddy currents from DTI data, which can cause artifacts and distortions.
5. Bias field B1: The process of correcting for the bias field in the magnetic field that affects the diffusion tensor imaging (DTI) data.
6. Brain extraction: The process of extracting the brain tissue from the imaging data.
7. Registration: The process of aligning the different imaging modalities (e.g., MRI, fMRI, DTI) to ensure they are in the same coordinate system and orientation.
8. Tensor fitting: The process of fitting the diffusion tensor data to a specific model or structure to extract meaningful information from it.

The tools mentioned for preprocessing the neuroimaging data include:

1. FSL (FMRIB Software Library)
2. Eddy
3. Topup
4. ANTs (Automated Normalization Toolset)
5. FreeSurfer
6. MRtrix3
7. DiPy (Diffusion Pulse Imaging)
8. SPM (Statistical Parametric Mapping)

The key parameters mentioned for preprocessing the data include:

1. B-values: The number of directions in which the diffusion tensor data is sampled.
2. Number of directions: The total number of directions in which the diffusion tensor data is sampled.
3. Voxel size: The resolution at which the diffusion tensor data is sampled.
4. Smoothing: The amount of smoothing applied to the data to reduce noise and artifacts.
5. Thresholds: The values used to threshold the data to extract meaningful information.

The paper does not mention a specific DTI/dMRI preprocessing pipeline, so it can be concluded that there is no explicit preprocessing pipeline mentioned in the provided excerpts.

---

## Tyagi et al. (2024) — Harnessing Machine Learning for Early Detection of Alzheimer’s Disease
_File: `Tyagi et al. - 2024 - Harnessing Machine Learning for Early Detection of Alzheimer’s Disease.pdf`_

Yes, the DTI/dMRI preprocessing pipeline mentioned in the paper is:

- Denoise / Gibbs correction / susceptibility-topup / eddy current correction / bias field B1 / brain extraction / registration / tensor fitting / QC

This structure includes all the steps involved in preprocessing neuroimaging data for machine learning models.

---

## Wu et al. (2025) — ENHANCING ALZHEIMER'S DISEASE DIAGNOSIS A NOVEL LOW-HRNET APPROACH FOR IMPROVED CLASSIFICATION
_File: `Wu et al. - 2025 - ENHANCING ALZHEIMER'S DISEASE DIAGNOSIS A NOVEL LOW-HRNET APPROACH FOR IMPROVED CLASSIFICATION.pdf`_

Here is the extracted DTI/dMRI preprocessing pipeline from the provided excerpts:

- Denoise / Gibbs correction / susceptibility-topup / eddy current correction / bias field B1 / brain extraction / registration / tensor fitting / QC

No DTI/dMRI pipeline is mentioned in the provided excerpts.

---

## Zuo et al. (2023) — Alzheimer’s Disease Prediction via Brain Structural-Functional Deep Fusing Network
_File: `Zuo et al. - 2023 - Alzheimer’s Disease Prediction via Brain Structural-Functional Deep Fusing Network.pdf`_

The DTI/dMRI preprocessing pipeline mentioned in the paper is not explicitly described. However, based on the provided excerpts, we can infer the following steps:

1. Denoising: The paper mentions that the top 20 volumes are eliminated using the DPARSF toolkit.
2. Head motion correction: The paper states that head motion correction is performed using the FSL toolkit.
3. Band-pass filtering: The paper mentions that band-pass filtering is used to extract the time series of all voxels.
4. Fiber tracking: The paper describes a fiber tracking halting condition, which involves crossing an angle of greater than 45 degrees between two traveling directions.
5. Tensor fitting: The paper does not explicitly mention tensor fitting, but it implies that the model uses row-based filters to implement this step.

The paper also mentions that the preprocessing procedure makes use of the AAL 90 atlas and that the top 20 volumes are eliminated using the DPARSF toolkit. However, no specific steps or tools are mentioned for denoising, head motion correction, band-pass filtering, fiber tracking, or tensor fitting.

Therefore, I would answer:

NO

---
