# DTI/dMRI Preprocessing Pipeline Extraction
_Generated: 2026-02-22 22:00:01_
_Papers: E:\adni-processing-pipeline\Week2\Papers1_
_Gen model: qwen3:8b  |  Embed model: qwen3-embedding:latest_
_Retrieval: 6 queries × top-4 chunks each_

---

## Cross-Paper Synthesis

### **Final Comparative Synthesis of Diffusion MRI Preprocessing**  

---

#### **1. Most Common Preprocessing Steps (Ranked by Frequency)**  
1. **Eddy Current and Motion Correction**  
   - **Frequency**: Nearly universal (all batches except a few exceptions).  
   - **Tools**: FSL (`eddy`), MRtrix3, Synb0disco, manual steps.  

2. **Tensor Fitting (FA/MD Calculation)**  
   - **Frequency**: High (all batches except Papers 1, 6, 8 in Batch 1; Papers 1, 2, 6, 8 in Batch 3).  
   - **Methods**: Least squares (OLS), NODDI, DTI.  

3. **Skull Stripping**  
   - **Frequency**: High (all batches except Batch 4).  
   - **Tools**: FSL-BET, BrainSuite, ROBEX, MNInu_correcttool.  

4. **Resampling to Isotropic Voxel Sizes**  
   - **Frequency**: Common (2–2.5 mm isotropic).  
   - **Examples**: 1 mm MNI (Batch 1), 2 mm (Batch 1), 2.5 mm (Batch 1).  

5. **Alignment to Standard Space**  
   - **Frequency**: High (MNI152, FMRIB58_FA, ENIGMA-DTI templates).  
   - **Tools**: FSL, ANTs, MRtrix3.  

6. **Fiber Tractography**  
   - **Frequency**: Moderate (deterministic/probabilistic methods).  
   - **Tools**: Dipy, MRtrix3, PANDA, Diffusion Toolkit.  

7. **Denoising**  
   - **Frequency**: Moderate (MP-PCA, PCA, Gibbs ringing correction).  
   - **Tools**: MRtrix3, Liou et al., Synb0disco.  

8. **ROI Extraction & Feature Selection**  
   - **Frequency**: Moderate (AAL, FMRIB58_FA, pyradiomics).  
   - **Tools**: pyradiomics, GRETNA, BrainSuite.  

9. **Cropping**  
   - **Frequency**: Moderate (e.g., 96×96×64px, 160×192×160).  

10. **Data Augmentation**  
    - **Frequency**: Low (GANs, CNNs for resizing).  

---

#### **2. Most Common Tools (Ranked by Frequency)**  
| **Tool**         | **Frequency** | **Key Use Cases**                                                                 |
|------------------|---------------|------------------------------------------------------------------------------------|
| **FSL**          | **High**      | Eddy correction, skull stripping, registration, FA/MD calculation.               |
| **MRtrix3**      | **High**      | Eddy correction, tensor fitting, denoising, tractography.                        |
| **PANDA**        | **High**      | DTI preprocessing, fiber tracking.                                                |
| **Dipy**         | **High**      | Tensor fitting, tractography.                                                     |
| **ANTs**         | **Medium**    | Nonlinear registration, segmentation.                                            |
| **pyradiomics**  | **Medium**    | Feature extraction from ROI.                                                     |
| **BrainSuite**   | **Medium**    | Registration, segmentation, tractography.                                        |
| **ROBEX**        | **Medium**    | Brain segmentation.                                                              |
| **MNInu_correcttool** | **Medium** | Intensity normalization.                                                         |
| **N3**           | **Low**       | Intensity inhomogeneity correction.                                              |
| **Kornia/TorchIO** | **Low**     | Data augmentation (GANs, CNNs).                                                  |

---

#### **3. Parameter Ranges and Disagreements**  
- **B-values**:  
  - **Common**: 1000–2000 s/mm² (Batch 1, 2, 3).  
  - **Disagreements**: Some papers report 500–1000 s/mm² (e.g., *Leveraging Swin Transformer*).  

- **Diffusion Directions**:  
  - **Common**: 32–127 non-collinear directions (Batch 1, 2, 3).  
  - **Disagreements**: Some papers use 100–127 directions (e.g., *Liou et al.*).  

- **Voxel Sizes**:  
  - **Common**: 1.0–2.5 mm isotropic (Batch 1, 2, 3).  
  - **Disagreements**: 1 mm MNI (Batch 1) vs. 2 mm (Batch 1).  

- **FA Thresholds**:  
  - **Common**: 0.2–0.3 (Batch 1, 3, 4).  
  - **Disagreements**: Some papers use 0.2 (e.g., *Qiao et al.*), others omit thresholds.  

- **Registration Templates**:  
  - **Common**: MNI152, FMRIB58_FA, ENIGMA-DTI.  
  - **Disagreements**: Some papers use non-standard templates (e.g., *HemiHeter-GNN*).  

---

#### **4. Papers with Notably Different, Minimal, or Incomplete Pipeline Reporting**  
- **Minimal/Incomplete Reporting**:  
  - **Batch 1**:  
    - *Paper 1*: Missing b-values, directions, tensor fitting details.  
    - *Paper 6*: Focuses on GAN-based

---

## 1-s2.0-S2666459321000044-main
_File: `1-s2.0-S2666459321000044-main.pdf`_

1. **Yes**, diffusion MRI (DTI) was used in this paper. The text explicitly mentions "DTI images" and "diffusion measurements (FA, MD, RD, and AxD)".

2. **Processing steps** (in order):  
   - Conversion of DICOM-formed images to NIfTI-formed images.  
   - Use of `dtiInit` preprocessing pipeline in VISTASOFT for:  
     - Eddy current correction  
     - Head motion correction  
     - Rigid-body alignment to T1  
     - Resampling to 2-mm isotropic voxels  
     - Skull stripping  
     - Tensor model fitting with least squares.  
   - AFQ pipeline with three steps:  
     - Fiber tract identification (deterministic streamlines tracking, waypoint ROI segmentation, fiber tract probability refinement).  
     - Fiber cleaning.  
     - Quantification (resampling to 100 equally spaced nodes per tract).  

3. **Software/tools**:  
   - `dtiInit` (part of VISTASOFT).  
   - `AFQ` (version 1.2).  

4. **Parameters reported**:  
   - 2-mm isotropic voxels.  
   - 18 major white matter tracts.  
   - 100 points per tract.  
   - Metrics: FA, MD, RD, AxD.  
   - Fiber recognition rate threshold (14/18 = 78%).  
   - Dataset size: 825 subjects (276 NCs, 294 ADs, 255 MCIs).  
   - **Not reported**: B-values, number of diffusion directions, or specific gradient orientations.  

5. **Exact sentences**:  
   - "DICOM-formed images were transformed into Nifti-formed images."  
   - "dtiInit preprocessing pipeline in VISTASOFT for eddy current correction, head motion correction, rigid-body alignment to T1, resampling to 2-mm isotropic voxels, skull stripping, and tensor model fitting with least squares."  
   - "whole-brain fibers were tracked by using the deterministic streamlines tracking algorithm, after which fiber tracts were segmented based on the waypoint ROI procedure and refined via fiber tract probability maps."  
   - "resampling to 100 equally spaced nodes per tract."  

6. **Processing description completeness**:  
   The description is **complete as per the text** but **incomplete in terms of certain parameters** (e.g., b-values, number of diffusion directions). The excerpts detail the steps, software, and some parameters but omit others like gradient directions or b-values.

---

## ADAMAEX-Alzheimer-s-disease-classification-via-attent_2025_Egyptian-Informat
_File: `ADAMAEX-Alzheimer-s-disease-classification-via-attent_2025_Egyptian-Informat.pdf`_

1. **Was diffusion MRI (DTI, dMRI, DWI, or similar) used in this paper?**  
   **NO DIFFUSION MRI PROCESSING FOUND**  

2. **What processing steps were applied to the diffusion images?**  
   The excerpts describe structural MRI (sMRI) preprocessing steps, not diffusion MRI. The explicitly stated steps are:  
   - Resampling to 256 × 256 pixels  
   - Intensity normalization  
   - Contrast-Limited Adaptive Histogram Equalisation (CLAHE)  
   - Sharpening using the Unsharp Mask technique  

3. **What software or tools are explicitly named for processing?**  
   No specific software or tools are named for processing.  

4. **What acquisition or processing parameters are explicitly reported?**  
   - Resampling to 256 × 256 pixels  
   - Intensity normalization  
   - CLAHE and Unsharp Masking techniques  

5. **Copy the exact sentences from the excerpts that describe the processing.**  
   - "We implement intensity normalisation to standardise pixel values, ensuring uniform intensity levels across images."  
   - "Resampling to 256 × 256 pixels guarantees consistent image dimensions for streamlined processing."  
   - "We utilise the Unsharp Masking technique to enhance image quality through sharpening."  
   - "CLAHE algorithm."  
   - "Pre-processing steps such as re-sampling, normalisation, Contrast-Limited Adaptive Histogram Equalisation (CLAHE), and sharpening using the Unsharp Mask technique."  

6. **Is the processing description complete, or does it appear incomplete/missing?**  
   The processing description is **complete** as per the excerpts, which detail all the steps explicitly stated in the paper. However, since the paper does not involve diffusion MRI, the description is not applicable to diffusion MRI techniques.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> esting the model’s accuracy and real-world applicability. 3.4. Image pre-processing
Image pre-processing is a pivotal component in our AD classification 
approach to enhance the quality of the images. We implement intensity 
normalisation to standardise pixel values, ensuring uniform intensity 
levels across images. Resampling to 256 × 256 pixels guarantees con-
sistent image dimensions for streamlined processing. Luft T, Colditz 
C, et al. conducted a study on Image Enhancement using Unsharp 
Masking, determining that the Unsharp Masking filter yielded the most 
effective sharpening results in comparison to other operators [39]. Based on this, we utilise the Unsharp Masking technique to enhance 
image quality through sharpening. [40] optimised the brain images 
in their study by employing the Contrast Limited Adaptive Histogram 
Equalisation (CLAHE) algorithm.

**Passage 2:**

> tics Journal 30 (2025) 100688 
4 
D. Bootun et al. Fig. 3. Original ADNI dataset distribution. Fig. 4. Data augmentation. Fig. 5, each serving a specific purpose during the model development 
process. Training Dataset : Used for training, allowing the model to learn pat-
terns and relationships in the data. 10,500 images of each class were 
allocated for training. Validation Dataset: Employed to fine-tune and optimise the model dur-
ing the training process. 1500 images of each class are reserved for 
validation and hyperparameter tuning. Testing Dataset: The remaining 3000 of the data for each class was used 
for testing the model’s accuracy and real-world applicability. 3.4. Image pre-processing
Image pre-processing is a pivotal component in our AD classification 
approach to enhance the quality of the images.

**Passage 3:**

> llenge of trustworthiness in clinical applications 
[34]. 3. Materials and methods
This section details the proposed methodology for the classification 
of brain scans. Fig. 2. Proposed workflow. 3.1. Proposed workflow and components
Fig. 2 illustrates the high-level architecture of the system. The sMRI 
Axial images of the 6 AD classes were obtained from ADNI and then 
converted from .nii to .png format. Data augmentation was applied 
to create a balanced dataset. Subsequently, pre-processing techniques 
were employed to enhance the images before feeding them into the 
models for training, aiming to achieve accurate image classification. 3.2. Datasets
The original dataset used in this study is sourced from the Alzhei-
mer’s Disease Neuroimaging Initiative (ADNI) database, available at 
https://adni.loni.usc.edu.

**Passage 4:**

> rning model, ADAMAEX, which is based on a convolutional autoencoder with four convolutions in the 
encoder part and a Squeeze and Excitation block for channel attention applied after each convolution. Additionally, we utilised fully connected layers (dense layers) for AD image classification. To conduct our study, 
we specifically chose axial brain scans acquired through sMRI in T2-weighted mode from the ADNI database, 
which were augmented using colour jitter, rotations, and flipping techniques. Before feeding the images to 
the model, we applied pre-processing steps such as re-sampling, normalisation, Contrast-Limited Adaptive 
Histogram Equalisation (CLAHE), and sharpening using the Unsharp Mask technique.

**Passage 5:**

> fi-
cantly more training data than others. Consequently, this imbalance can 
Egyptian Informatics Journal 30 (2025) 100688 
3 
D. Bootun et al. Table 1
Summary of recent studies carried by researches. References Scan type Dataset Data augmentation/Pre-
processing
Method  
 [22] MRI Kaggle Horizontal rendering of 
images and displays 
RGB pixel values 
Principal Component 
Analysis (PCA)
Pretrained-CNN 
VGG 
ResNet 
Modified AlexNet
 
 [23] MRI Kaggle Random flip 
Random zoom 
Rescaling of images in 
tensors with values 
between 0 and 1
CNN 
VGG-16 
VGG-19
 
 [24] MRI ADNI Adaptive thresholding 
Cropping 
Filtration 
Resize images to (128,128) 
and (64,64) 
Horizontal flipping 
Shearing 
Shifting 
Rotating 
Zooming
CNN with 3 
convolutional layers 
and max pooling 
after each 
convolutional layer
 
 [25] MRI Kaggle Rescaling 
Brightness 
Zooming 
Filling 
Flipping
Series of Conv2D 
and MaxPooling2D 
layers 
2 dense layers
 
 [26] MRI ADNI Skull-stripping Hybrid DNN 
architecture: LeNet 
and AlexNet in 
parallel 
Filters (1 × 1, 3 ×
3, 5 × 5)
 
 [28] MRI ADNI Rotation 
Scaling 
Shearing 
Flipping
CAE for feature 
extraction 
Deep parallel 
ensemble for 
classification
 
 [29] PET/ CT data from 
Dong-A 
University
Horizontal flip 
Width shift 
Height shift
stacked CAE  
 [32] MRI ADNI Correct intensity 
inhomogeneity 
Intensity normalisation 
step 
Remove skull 
Aligned to the standard 
space using FLIRT 
Resampled to the size of 
182 × 218 × 182 
3D connection-wise-
attention model 
based densely 
connected
 
 [33] MRI ADNI Rotation 
Flipping 
Scaling
3D Convolutional 
Neural Network 
Multilayer 
Perceptron which 
uses attention 
mechanism
 
negatively impact the model’s overall performance and its capacity to 
generalise effectively on unseen data.

**Passage 6:**

> s. Int J Mol Sci 2022;23(11):6079.
[18] Maharana K, Mondal S, Nemade B. A review: Data pre-processing and data 
augmentation techniques. Glob Transit Proc 2022;3(1):91–9.
[19] Varuna Shree N, Kumar T. Identification and classification of Brain Tumor MRI 
images with feature extraction using DWT and probabilistic neural network. Brain Inform 2018;5(1):23–30.
[20] Khalid S, Khalil T, Nasreen S. A survey of feature selection and feature extraction 
techniques in machine learning. In: 2014 Science and information conference. IEEE; 2014, p. 372–8.
[21] Atitallah SB, Driss M, Boulila W, Koubaa A. Enhancing early Alzheimer’s disease 
detection through big data and ensemble few-shot learning. IEEE J Biomed Heal 
Inform. 2024.
[22] Acharya H, Mehta R, Singh DK. Alzheimer disease classification using transfer 
learning.

**Passage 7:**

> r’s disease and mild cognitive impairment using a single 
MRI and deep neural networks. NeuroImage: Clin 2019;21:101645.
[14] Krishnan G, Singh S, Pathania M, Gosavi S, Abhishek S, Parchani A, et 
al. Artificial intelligence in clinical medicine: catalyzing a sustainable global 
healthcare paradigm. Front Artif Intell 2023;6.
[15] Angermueller C, Pärnamaa T, Parts L, Stegle O. Deep learning for computational 
biology. Mol Syst Biol 2016;12(7):878.
[16] Li M, Jiang Y, Zhang Y, Zhu H. Medical image analysis using deep learning 
algorithms. Front Public Heal 2023;11:1273253.
[17] Kim J, Jeong M, Stiles WR, Choi HS. Neuroimaging modalities in Alzheimer’s 
disease: diagnosis and clinical features. Int J Mol Sci 2022;23(11):6079.
[18] Maharana K, Mondal S, Nemade B. A review: Data pre-processing and data 
augmentation techniques. Glob Transit Proc 2022;3(1):91–9.
[19] Varuna Shree N, Kumar T.

**Passage 8:**

> image classification. 3.2. Datasets
The original dataset used in this study is sourced from the Alzhei-
mer’s Disease Neuroimaging Initiative (ADNI) database, available at 
https://adni.loni.usc.edu. Established in 2003, ADNI is a collaborative 
effort led by Principal Investigator Michael W. Weiner, MD, aimed at 
evaluating the utility of various tools such as serial magnetic resonance 
imaging (MRI), positron emission tomography (PET), biological mark-
ers, and clinical and neuropsychological assessments in tracking the 
progression of mild cognitive impairment (MCI) and early Alzheimer’s 
disease (AD). The ADNI database was chosen for its benchmark sta-
tus in AD research, providing standardised imaging data for model 
evaluation. However, its limited demographic diversity and imaging 
modalities could affect generalisability.

**Passage 9:**

> work reported in this paper. Acknowledgements
The authors would like to acknowledge Prince Sultan University, 
Riyadh Saudi Arabia for supporting Article Processing Charges (APC) 
of this publication. Dataset for this project was obtained from the Alzheimer’s Disease 
Neuroimaging Initiative (ADNI) (National Institutes of Health Grant 
U01 AG024904) and DOD ADNI (Department of Defense award number 
W81XWH-12-2-0012). ADNI is funded by the National Institute on 
Aging, United States, the National Institute of Biomedical Imaging 
and Bioengineering, United States, and through generous contribu-
tions from the following: AbbVie, Alzheimer’s Association; Alzheimer’s 
Drug Discovery Foundation; Araclon Biotech; BioClinica, Inc.; Biogen; 
Bristol–Myers Squibb Company; CereSpir, Inc.; Cogstate; Eisai Inc.; 
Elan Pharmaceuticals, Inc.; Eli Lilly and Company; EuroImmun; F.

**Passage 10:**

> r Inc.; Piramal 
Imaging; Servier; Takeda Pharmaceutical Company; and Transition 
Therapeutics. The Canadian Institutes of Health Research is providing 
funds to support ADNI clinical sites in Canada. Private sector contri-
butions are facilitated by the Foundation for the National Institutes 
of Health (www.fnih.org). The grantee organisation is the Northern 
California Institute for Research and Education, and the study is co-
ordinated by the Alzheimer’s Therapeutic Research Institute at the 
University of Southern California. ADNI data are disseminated by the 
Laboratory for Neuro Imaging at the University of Southern California. Data availability
Due to the confidentiality of the data, the dataset has not been made 
publicly available. References
[1] Bharathi A, Arunachalam A. Pre-processing on Alzheimer MRI images. Ann Rom 
Soc Cell Biol 2021;4433–41.
[2] DeTure MA, Dickson DW.

**Passage 11:**

> Discovery Foundation; Araclon Biotech; BioClinica, Inc.; Biogen; 
Bristol–Myers Squibb Company; CereSpir, Inc.; Cogstate; Eisai Inc.; 
Elan Pharmaceuticals, Inc.; Eli Lilly and Company; EuroImmun; F. Hoffmann-La Roche Ltd and its affiliated company Genentech, Inc.; 
Fujirebio; GE Healthcare; IXICO Ltd.;Janssen Alzheimer Immunother-
apy Research & Development, LLC.; Johnson & Johnson Pharmaceutical 
Research & Development LLC.; Lumosity; Lundbeck; Merck & Co., Inc.; 
Meso Scale Diagnostics, LLC.; NeuroRx Research; Neurotrack Tech-
nologies; Novartis Pharmaceuticals Corporation; Pfizer Inc.; Piramal 
Imaging; Servier; Takeda Pharmaceutical Company; and Transition 
Therapeutics. The Canadian Institutes of Health Research is providing 
funds to support ADNI clinical sites in Canada.

**Passage 12:**

> ng 
functional MRI. J Heal Eng 2023;2023(1):6961346.
[38] Arafa DA, Moustafa HE-D, Ali HA, Ali-Eldin AM, Saraya SF. A deep learning 
framework for early diagnosis of Alzheimer’s disease on MRI images. Multimedia 
Tools Appl 2024;83(2):3767–99.
[39] Gunawardena K, Rajapakse R, Kodikara ND. Applying convolutional neural 
networks for pre-detection of Alzheimer’s disease from structural MRI data. In: 2017 24th international conference on mechatronics and machine vision in 
practice. IEEE; 2017, p. 1–7.
[40] AbdulAmeer AT, Ali SH. Classification of medical images of Alzheimer’s disease 
using deep learning techniques.
[41] Hung C-L. Deep learning in biomedical informatics. In: Intell nanotechnology. Elsevier; 2023, p. 307–29.
[42] Zhang Y. A better autoencoder for image: Convolutional autoencoder. 2018, 
ICONIP17-DCEC.

**Passage 13:**

> he images to 
the model, we applied pre-processing steps such as re-sampling, normalisation, Contrast-Limited Adaptive 
Histogram Equalisation (CLAHE), and sharpening using the Unsharp Mask technique. For visualisation, we 
integrated Grad-CAM, an Explainable AI (XAI) technique, to highlight the brain regions responsible for the 
model’s classification decisions, a method underutilised by other authors in the context of AD classification. This model achieved an impressive accuracy of 96.2% and shows great promise for adoption in the medical 
sector, providing valuable assistance to doctors in validating their predictions based on brain scans. 1. Introduction
The brain, a vital organ crucial for human functions [1], was 
the subject of Alois Alzheimer’s groundbreaking work over a century 
ago. He first described the neurodegenerative condition that would 
eventually bear his name [2].

**Passage 14:**

> d CLAHE, improves the robust-
ness and feature sensitivity of the model. These enhancements are 
Egyptian Informatics Journal 30 (2025) 100688 
13 
D. Bootun et al. Table 3
Summary of carried studies. References Scan type Dataset Data augmentation/Pre-processing Method Accuracy Limitations  
 [22] MRI Kaggle Produced horizontal rendering of 
images and displays 
Performed RGB pixel values and 
Principal Component Analysis 
(PCA) to reverse the strength of 
RGB channels
Pretrained-CNN 
VGG 
ResNet 
Modified AlexNet
CNN:88.89% 
VGG-16:85.07% 
ResNet50: 75.25% 
Modified AlexNet: 
95.70%
Limited to only 4 stages 
No implementation of XAI
 
 [23] MRI Kaggle Random flip 
Random zoom 
Rescaling of images in tensors 
with values between 0 and 1
CNN 
VGG-16 
VGG-19
CNN:0.7102 
VGG-16: 0.7704 
VGG-19: 0.7766
Limited to only 4 stages 
High computational time 
No implementation of XAI
 
 [24] MRI ADNI Adaptive thresholding 
Cropping 
Filtration 
Resize images to (128,128) and 
(64,64) 
Horizontal flipping 
Shearing 
shifting 
Rotating 
Zooming
CNN with 3 
convolutional layers 
and max pooling after 
each convolutional 
layer
Multi-classification: 
97.5%
No implementation of XAI  
 [25] MRI Kaggle Rescaling 
Brightness 
Zooming 
Filling 
Flipping
Series of Conv2D and 
MaxPooling2D layers 
2 dense layers 
Multi-classification: 
95.96%
Relatively small dataset 
Limited to only 4 stages 
No implementation of XAI
 
 [26] MRI ADNI Skull-stripping Hybrid DNN 
architecture: LeNet and 
AlexNet in parallel 
Used small filters (1 
×1, 3 ×3, 5 ×5)
93.58% Limited to only 3 stages 
No implementation of XAI
 
 [28] MRI ADNI Rotation 
Scaling 
Shearing 
Flipping
CAE for feature 
extraction 
Deep parallel ensemble 
for classification 
86.57% No implementation of XAI  
 [29] PET/ 
CT
data from 
Dong-A 
University
Horizontal flip 
Width shift 
Height shift
stacked CAE 98.54% Limited to only 3 stages 
No implementation of XAI
 
 [32] MRI ADNI Correct intensity inhomogeneity 
Intensity normalisation step 
Remove skull 
Aligned to the standard space 
using FLIRT 
Resampled to the size of 182 ×
218 × 182
3D connection-wise-
attention model based 
densely connected
AD vs. healthy control: 
97.35% 
MCI converters vs. 
healthy control: 
87.82% 
MCI converters vs. 
non-converters: 78.79% 
No implementation of XAI  
 [33] MRI ADNI Rotation 
Flipping 
Scaling
3D Convolutional 
Neural Network 
Multilayer Perceptron 
which uses attention 
mechanism
AD and NC: 91.27%, 
MCI and NC: 80.85%, 
and AD and MCI: 
87.34%
Computationally expensive 
for training 
No implementation of XAI
 
 Our proposed 
model
sMRI ADNI Data Augmentation: 
Colour jitter 
90◦ rotation 
180◦ rotation 
Vertical flipping 
Pre-processing: 
Resampling 256*256 
Sharpening using Unsharp Mask 
Technique 
CLAHE
Convolutional 
autoencoder with 
Squeeze and Excitation 
block after each 
convolutional layer for 
feature extraction.

**Passage 15:**

> rp Masking technique to enhance 
image quality through sharpening. [40] optimised the brain images 
in their study by employing the Contrast Limited Adaptive Histogram 
Equalisation (CLAHE) algorithm. This method proves particularly ben-
eficial in scenarios where high brightness requirements are essential, 
thereby enhancing the visibility of hidden image features. In alignment 
with this approach, our study also implemented the CLAHE technique 
to enhance image quality. Fig. 6 depicts a comparison between the 
original image and the same image after undergoing the pre-processing 
steps mentioned above. 3.5. Models development
3.5.1. Autoecoder (AE)
AEs are neural networks designed to learn compressed representa-
tions of input data by reducing the amount of distortion between the 
input and the output.

**Passage 16:**

> incorpo-
rating colour jitter, multiple rotation angles (90◦, 180◦), and vertical 
flipping. These variations provide additional robustness, particularly 
when addressing small or imbalanced datasets. Several studies also incorporated pre-processing techniques, such as 
rescaling, skull-stripping, intensity normalisation, and adaptive thresh-
olding. In contrast, our model introduces advanced pre-processing 
methods, including sharpening via the Unsharp Mask and Contrast 
Limited Adaptive Histogram Equalisation (CLAHE). These techniques 
are particularly valuable in medical imaging, where enhancing image 
contrast and highlighting critical features are essential, as subtle image 
details may hold clinical significance. The models used across the studies ranged from convolutional 
neural networks (CNNs) to hybrid architectures and more advanced 
deep learning methods.

**Passage 17:**

> for its benchmark sta-
tus in AD research, providing standardised imaging data for model 
evaluation. However, its limited demographic diversity and imaging 
modalities could affect generalisability. Future work will expand the 
dataset to include more diverse patient data and imaging techniques to 
improve robustness and applicability. In the process of image acquisi-
tion for this study, we specifically chose axial brain scans for the six 
classes of AD acquired through sMRI in T2-weighted mode. The class 
distribution of the original ADNI dataset is illustrated in Fig. 3. 3.3. Data augmentation
We observe a class imbalance as shown in Fig. 3. This disparity 
becomes more pronounced during the dataset’s division into training, 
testing, and validation sets, leading to certain classes having signifi-
cantly more training data than others.

**Passage 18:**

> ipping, horizontal or vertical flipping, random scaling, and 
colour jittering [36], have been widely utilised. [37] extended these 
methods by incorporating 90◦, 180◦, and 270◦ rotation and flipping. Similarly, [38] employed rotation, up-down flipping, and mirroring 
techniques in their study on early diagnosis of AD on MRI images. In our study, we aim to achieve a target of 15,000 images per class, 
initially. To strike a balance between adding variation and preserving 
data integrity we employ vertical and horizontal flipping, 90◦ and 180◦
rotation, and slight colour jitter as depicted in Fig. 4. The original colour-jittered image undergoes the same augmenta-
tion steps as the original image, resulting in the generation of 14 
images from a single original image.

**Passage 19:**

> ployment of an explainable AI approach to highlight the brain 
scan features contributing to classification. 4. Comparative evaluation of the proposed automated system with 
existing methodologies. 2. Related works
AD diagnosis includes cognitive evaluations and brain imaging to 
detect the disease early and classify patients into different stages before 
neurodegeneration onset. Various clinical brain imaging techniques 
show promise in investigating the disease but differ in accuracy for 
disease identification and distinguishing AD-related groups [17]. AD medical imaging datasets can be limited due to privacy con-
cerns, affecting machine learning and deep learning algorithms accu-
racy. Data augmentation helps by creating additional data with diverse 
orientations, serving two purposes: generating more data from a limited 
dataset and reducing overfitting risk [18].

**Passage 20:**

> e-processing steps. The table also highlights the methods used, 
classification accuracies achieved, and the limitations of each model. Most studies utilised publicly available datasets, such as ADNI. The 
augmentation techniques commonly employed included horizontal and 
vertical flipping, rotations, scaling, zooming, and other affine transfor-
mations. These standard procedures aim to enhance the diversity of the 
training data and mitigate the risk of overfitting. Notably, our proposed 
model employs a more comprehensive augmentation strategy, incorpo-
rating colour jitter, multiple rotation angles (90◦, 180◦), and vertical 
flipping. These variations provide additional robustness, particularly 
when addressing small or imbalanced datasets.

**Passage 21:**

> formatics Journal 30 (2025) 100688 
14 
D. Bootun et al.
new contribution in this area. The results of our model were highly 
promising, and we believe it will be of great value to the medical 
field. Medical professionals can utilise our ADAMAEX to aid in visual 
classification, confirming their diagnostic results, and offering timely 
and appropriate healthcare assistance. CRediT authorship contribution statement
Doorgeshwaree Bootun: Writing – review & editing, Writing 
– original draft, Methodology, Formal analysis, Conceptualiza-
tion. Muhammad Muzzammil Auzine: Visualization, Software, 
Methodology, Investigation, Formal analysis, Data curation. Noor 
Ayesha: Visualization, Validation, Formal analysis, Data curation, 
Conceptualization. Salma Idris: Writing – review & editing, Soft-
ware, Resources, Funding acquisition, Data curation.

**Passage 22:**

> ration. Noor 
Ayesha: Visualization, Validation, Formal analysis, Data curation, 
Conceptualization. Salma Idris: Writing – review & editing, Soft-
ware, Resources, Funding acquisition, Data curation. Tanzila Saba: 
Writing – review & editing, Writing – original draft, Visualization, 
Methodology, Data curation, Conceptualization. Maleika Heenaye-
Mamode Khan: Writing – original draft, Software, Resources, 
Project administration, Methodology, Formal analysis. Declaration of competing interest
The authors declare that they have no known competing finan-
cial interests or personal relationships that could have appeared to 
influence the work reported in this paper. Acknowledgements
The authors would like to acknowledge Prince Sultan University, 
Riyadh Saudi Arabia for supporting Article Processing Charges (APC) 
of this publication.

**Passage 23:**

> potential of attention mechanisms in 
elevating the accuracy and interpretability of AD classification models. Table  1 shows a summary of recent studies carried out by research 
on AD classification. After analysing various studies, it can be inferred 
that autoencoders and attention mechanisms have played a role in 
AD classification, although only a few attention models have been 
explored and applied in AD applications. Additionally, research on the 
combination of autoencoders and attention models is limited. Further-
more, many studies lack implementation of explainable AI, a promising 
approach to enhance transparency and interpretability of AI models, 
addressing the challenge of trustworthiness in clinical applications 
[34]. 3. Materials and methods
This section details the proposed methodology for the classification 
of brain scans. Fig. 2. Proposed workflow. 3.1.

**Passage 24:**

> processing: 
Resampling 256*256 
Sharpening using Unsharp Mask 
Technique 
CLAHE
Convolutional 
autoencoder with 
Squeeze and Excitation 
block after each 
convolutional layer for 
feature extraction. Dense layers as 
classifier. XAI: Grad 
CAM
96.2%  
crucial for medical imaging tasks, where subtle details can have sig-
nificant clinical implications. Finally, the use of SE blocks in our archi-
tecture improves feature extraction efficiency, making the model more 
suitable for complex classification tasks without imposing excessive 
computational burdens. 5. Conclusion
Our autoencoder model with convolutional layers and Squeeze and 
Excitation block performs competitively compared to the other state-of-
the-art models. It achieves a high accuracy of 96.2% in classifying ADNI 
data, demonstrating its effectiveness in the task of AD classification.

</details>

---
