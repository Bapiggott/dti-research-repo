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

## Alzheimer-s Disease Prediction via Brain Structural-Functional Deep Fusing Network
_File: `Alzheimer-s Disease Prediction via Brain Structural-Functional Deep Fusing Network.pdf`_



<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> tings
The ADNI (Alzheimer’s Disease Neuroimaging Initiative)
public dataset is used to test our CT-GAN model. Table I
contains full information about the 268 patients whose data
we used in this study. Each patient was scanned with both
DTI and fMRI. The preprocessing procedure makes use of the
AAL 90 atlas. Using the DPARSF toolkit, the top 20 volumes
are eliminated, followed by head motion correction, band-
pass filtering, Gaussian smoothing, and extracting the time
series of all voxels. By following fiber bundles between ROIs,
4606 IEEE TRANSACTIONS ON NEURAL SYSTEMS AND REHABILITATION ENGINEERING, VOL. 31, 2023
Fig. 4. Examples of two multimodal connectivity matrices at different
stages of cognitive disease (a) NC; (b) AD. Fig. 5. The ten most important brain regions between NC and EMCI
groups.
the structural connection is computed.

**Passage 2:**

> taining magnetic resonance imaging (MRI) brain scan data
from more than 500,000 UK participants. This large sample
data can be suitable to study neurodegenerative diseases (e.g.,
Alzheimer’s disease). Due to the huge size of the dataset,
downloading and preprocessing of brain imaging data is very
time-consuming, and we are still in the collection stage of the
brain imaging data set. We will validate our model on the UK
biobank data in future work. V. C ONCLUSION
In this paper, we propose a novel CT-GAN model to fuse
fMRI and DTI and generate multimodal connectivity from
fMRI and DTI in an efficient end-to-end manner. The key idea
of this work is that mutual conversion between structural and
functional information is accomplished using a cross-modal
swapping bi-attention mechanism.

**Passage 3:**

> in images are based on two steps: the first step
is to preprocess the brain structural and functional images
ZUO et al.: AD PREDICTION VIA BRAIN STRUCTURAL-FUNCTIONAL DEEP FUSING NETWORK 4611
Fig. 14. Comparison of classification performance using single-modal and bimodal images.
to obtain structural and functional features by the software
toolbox; the second step is to use the preprocessed structural
and functional features to build deep learning models for
fusion. The novelty of our model is constructing an end-to-
end framework to fuse structural brain imaging (DTI) and
functional brain imaging (fMRI) for AD analysis.

**Passage 4:**

> successive convolutional filters on
the DTI. Specifically, we first design four down-sampling
convolutional operations with a kernel size of 3 × 3 × 3 and a
stride of 2 to extract local feature maps. The extracted feature
maps are then passed through 1 ×1×1 filters to fix the channel
at N. Finally, each channel map is combined with the brain
anatomical information ( x, y, z, v) to align the features for
each brain region [43]. Similar operations are conducted on
the fMRI. The output embeddings S and F are given below:
S = S E(DT I , x, y, z, v), F = F E( f M R I, x, y, z, v) (1)
where S ∈ RN ×q, F ∈ RN ×q. 2) Swapping Bi-Attention Mechanism: The proposed model
aims to leverage the transformer’s bi-attention mechanism to
explore complementary information between structural and
functional images.

**Passage 5:**

> 23
[13] S. Wang, Y . Shen, W. Chen, T. Xiao, and J. Hu, “Automatic recogni-
tion of mild cognitive impairment from MRI images using expedited
convolutional neural networks,” in Proc. Int. Conf. Artif. Neural Netw.,
Oct. 2017, pp. 373–380.
[14] G. L. Colclough, M. W. Woolrich, S. J. Harrison, P. A. Rojas López,
P. A. Valdes-Sosa, and S. M. Smith, “Multi-subject hierarchical inverse
covariance modelling improves estimation of functional brain networks,”
NeuroImage, vol. 178, pp. 370–384, Sep. 2018.
[15] R. Yu, L. Qiao, M. Chen, S.-W. Lee, X. Fei, and D. Shen, “Weighted
graph regularized sparse brain network construction for MCI identifica-
tion,” Pattern Recognit., vol. 90, pp. 220–231, Jun. 2019.
[16] Y . Li, H. Yang, B. Lei, J. Liu, and C.-Y .

**Passage 6:**

> Song, Z. Wen, and J. Qin, “Feature masking on
non-overlapping regions for detecting dense cells in blood smear image,”
IEEE Trans. Med. Imag., vol. 42, no. 6, pp. 1668–1680, Jun. 2023.
[35] H. Wu, X. Huang, X. Guo, Z. Wen, and J. Qin, “Cross-image depen-
dency modeling for breast ultrasound segmentation,” IEEE Trans. Med. Imag., vol. 42, no. 6, pp. 1619–1631, Jun. 2023.
[36] W. Yu, B. Lei, M. K. Ng, A. C. Cheung, Y . Shen, and S. Wang,
“Tensorizing GAN with high-order pooling for Alzheimer’s disease
assessment,” IEEE Trans. Neural Netw. Learn. Syst., vol. 33, no. 9,
pp. 4945–4959, Sep. 2022.
[37] S. Hu, B. Lei, S. Wang, Y . Wang, Z. Feng, and Y . Shen, “Bidi-
rectional mapping generative adversarial networks for brain MR to
PET synthesis,” IEEE Trans. Med. Imag. , vol. 41, no. 1, pp. 145–157,
Jan. 2022.
[38] W.

**Passage 7:**

> Wu, and J. Wang, “Enhancing the feature
representation of multi-modal MRI data by combining multi-view infor-
mation for MCI classification,” Neurocomputing, vol. 400, pp. 322–332,
Aug. 2020.
[56] X. Song et al., “Graph convolution network with similarity awareness
and adaptive calibration for disease-induced deterioration prediction,”
Med. Image Anal., vol. 69, Apr. 2021, Art. no. 101947.

**Passage 8:**

> 990, Apr. 2015.
[31] B. Lei et al., “Self-calibrated brain network estimation and joint
non-convex multi-task learning for identification of early Alzheimer’s
disease,” Med. Image Anal., vol. 61, Apr. 2020, Art. no. 101652.
[32] P. Cao et al., “Generalized fused group lasso regularized multi-task fea-
ture learning for predicting cognitive outcomes in Alzheimers disease,”
Comput. Methods Programs Biomed., vol. 162, pp. 19–45, Aug. 2018.
[33] S. Wang, Z. Chen, S. You, B. Wang, Y . Shen, and B. Lei, “Brain stroke
lesion segmentation using consistent perception generative adversarial
network,” Neural Comput. Appl., vol. 34, no. 11, pp. 8657–8669,
Jun. 2022.
[34] H. Wu, C. Lin, J. Liu, Y . Song, Z. Wen, and J. Qin, “Feature masking on
non-overlapping regions for detecting dense cells in blood smear image,”
IEEE Trans. Med. Imag., vol. 42, no. 6, pp. 1668–1680, Jun. 2023.
[35] H. Wu, X.

**Passage 9:**

> pping six ROIs in the prediction results. The index indicates the
corresponding ROI in the AAL90 atlas. The red color represents decreased connections; the blue color represents increased connections. The
gray dotted lines divide the six ROIs into five brain lobes. Fig. 13. Influence of different modules in CT -GAN on the prediction
performance.
experiments. First, we individually computed the classifica-
tion performance using functional brain imaging (fMRI) (as
shown by the red color in Figure 14). Then, we individually
computed the classification performance using structural brain
imaging (DTI) (as shown by the blue color in Figure 14). Finally, we fused functional and structural brain imaging and
presented the classification results in green color in Figure 14.

**Passage 10:**

> IEEE TRANSACTIONS ON NEURAL SYSTEMS AND REHABILITATION ENGINEERING, VOL. 31, 2023 4601
Alzheimer’s Disease Prediction via Brain
Structural-Functional Deep Fusing Network
Qiankun Zuo, Y anyan Shen
 , Member, IEEE, Ning Zhong, C. L. Philip Chen,
Baiying Lei
 , Senior Member, IEEE, and Shuqiang Wang
 , Senior Member, IEEE
Abstract— Fusing structural-functional images of the
brain has shown great potential to analyze the deterio-
ration of Alzheimer’s disease (AD). However, it is a big
challenge to effectively fuse the correlated and comple-
mentary information from multimodal neuroimages. In this
work, a novel model termed cross-modal transformer
generative adversarial network (CT-GAN) is proposed to
effectively fuse the functional and structural information
contained in functional magnetic resonance imaging (fMRI)
and diffusion tensor imaging (DTI).

**Passage 11:**

> vol. 181, pp. 734–747, Nov. 2018.
[25] O. Dekhil et al., “A personalized autism diagnosis CAD system using
a fusion of structural MRI and resting-state functional MRI data,”
Frontiers Psychiatry, vol. 10, p. 392, Jul. 2019.
[26] D. Hirjak et al., “Multimodal magnetic resonance imaging data fusion
reveals distinct patterns of abnormal brain structure and function in
catatonia,” Schizophrenia Bull., vol. 46, no. 1, pp. 202–210, Jan. 2020.
[27] C. J. Honey et al., “Predicting human resting-state functional connectiv-
ity from structural connectivity,” Proc. Nat. Acad. Sci. USA, vol. 106,
no. 6, pp. 2035–2040, Feb. 2009.
[28] K. Li, L. Guo, D. Zhu, X. Hu, J. Han, and T. Liu, “Individual
functional ROI optimization via maximization of group-wise consistency
of structural and functional profiles,” Neuroinformatics, vol. 10, no. 3,
pp. 225–242, Jul. 2012.
[29] Q. Zuo, B. Lei, Y . Shen, Y .

**Passage 12:**

> d D. Shen, “Weighted
graph regularized sparse brain network construction for MCI identifica-
tion,” Pattern Recognit., vol. 90, pp. 220–231, Jun. 2019.
[16] Y . Li, H. Yang, B. Lei, J. Liu, and C.-Y . Wee, “Novel effective
connectivity inference using ultra-group constrained orthogonal forward
regression and elastic multilayer perceptron classifier for MCI identifica-
tion,” IEEE Trans. Med. Imag., vol. 38, no. 5, pp. 1227–1239, May 2019.
[17] L. Xiao et al., “Multi-hypergraph learning-based brain functional con-
nectivity analysis in fMRI data,” IEEE Trans. Med. Imag., vol. 39, no. 5,
pp. 1746–1758, May 2020.
[18] B. Lei et al., “Diagnosis of early Alzheimer’s disease based on dynamic
high order networks,” Brain Imag. Behav., vol. 15, no. 1, pp. 276–287,
2021.
[19] M. Yu, O. Sporns, and A. J.

**Passage 13:**

> Process. Syst., vol. 30, 2017.
[41] D. A. Hudson and L. Zitnick, “Generative adversarial transformers,” in
Proc. Int. Conf. Mach. Learn., 2021, pp. 4487–4499.
[42] H. Wu, J. Pan, Z. Li, Z. Wen, and J. Qin, “Automated skin lesion
segmentation via an adaptive dual attention module,” IEEE Trans. Med. Imag., vol. 40, no. 1, pp. 357–370, Jan. 2021.
[43] Q. Zuo, L. Lu, L. Wang, J. Zuo, and T. Ouyang, “Constructing
brain functional network by adversarial temporal-spatial aligned trans-
former for early AD analysis,” Frontiers Neurosci., vol. 16, Nov. 2022,
Art. no. 1087176.
[44] L. Zhang, L. Wang, and D. Zhu, “Predicting brain structural network
using functional connectivity,” Med. Image Anal., vol. 79, Jul. 2022,
Art. no. 102463.
[45] L. Liu, Y .-P. Wang, Y . Wang, P. Zhang, and S. Xiong, “An enhanced
multi-modal brain graph network for classifying neuropsychiatric disor-
ders,” Med.

**Passage 14:**

> Wang, Y . Wang, Z. Feng, and Y . Shen, “Bidi-
rectional mapping generative adversarial networks for brain MR to
PET synthesis,” IEEE Trans. Med. Imag. , vol. 41, no. 1, pp. 145–157,
Jan. 2022.
[38] W. Yu et al., “Morphological feature visualization of Alzheimer’s disease
via multidirectional perception GAN,” IEEE Trans. Neural Netw. Learn. Syst., vol. 34, no. 8, pp. 4401–4415, Aug. 2023.
[39] C. Gong et al., “Generative AI for brain image computing and brain
network computing: A review,” Frontiers Neurosci., vol. 17, Jun. 2023,
Art. no. 1203104.
[40] A. Vaswani et al., “Attention is all you need,” in Proc. Adv. Neural Inf. Process. Syst., vol. 30, 2017.
[41] D. A. Hudson and L. Zitnick, “Generative adversarial transformers,” in
Proc. Int. Conf. Mach. Learn., 2021, pp. 4487–4499.
[42] H. Wu, J. Pan, Z. Li, Z. Wen, and J.

**Passage 15:**

> Channel Separator
The MC contains both structural and functional connectivity
information. To stabilize the learning process, we design the
dual-channel separator to recover the SC and FC from the MC. As shown in Figure 2, the dual-channel separator projects the
MC back to two modality-specific connectivities. Considering
the topological properties of the human brain, we adopt the
cross-weighting scheme to extract global connectivity informa-
tion for better detachment between structural and functional
connectivity. It consists of two branches, which share the
first layer and have different weighting parameters in the
second and third layers, respectively. The filter is a cross-shape
parameter with step size 1. The input and the output for each
layer have the same size, except for different channels. Finally,
the third layer outputs the reconstructed SC and FC. C.

**Passage 16:**

> ctional ROI optimization via maximization of group-wise consistency
of structural and functional profiles,” Neuroinformatics, vol. 10, no. 3,
pp. 225–242, Jul. 2012.
[29] Q. Zuo, B. Lei, Y . Shen, Y . Liu, Z. Feng, and S. Wang, “Multimodal
representations learning and adversarial hypergraph fusion for early
Alzheimer’s disease prediction,” in Proc. Chin. Conf. Pattern Recognit. Comput. Vis. (PRCV), Beijing, China, Nov. 2021, pp. 479–490.
[30] S. M. Daselaar, V . Iyengar, S. W. Davis, K. Eklund, S. M. Hayes, and
R. E. Cabeza, “Less wiring, more firing: Low-performing older adults
compensate for impaired white matter with greater neural activity,”
Cerebral Cortex, vol. 25, no. 4, pp. 983–990, Apr. 2015.
[31] B. Lei et al., “Self-calibrated brain network estimation and joint
non-convex multi-task learning for identification of early Alzheimer’s
disease,” Med. Image Anal., vol. 61, Apr.

**Passage 17:**

> obtained by applying the trained generator
to DTI and fMRI. The visualization of averaged multimodal
connectivity matrices and the change in connectivity with
various thresholds are shown in Figure 8. The three rows
correspond to the altered connections from NC to EMCI, from
EMCI to LMCI, and from LMCI to AD, respectively. The
values between −0.1 ∼ 0.1 are ignored during the analysis. Two threshold values are set for viewing the important con-
nections. The first threshold is 50% quantile values, which are
estimated from the positive and negative connectivities. The
same operation is implemented on the second 75% threshold
value. The more important connections with the 75% threshold
value are shown in Figure 9. It can be seen that the decreased
connections are greater than the increased connections at the
stages of EMCI and AD, while the phenomenon is reversed
at the LMCI stage.

**Passage 18:**

> ∈ RN ×q. 2) Swapping Bi-Attention Mechanism: The proposed model
aims to leverage the transformer’s bi-attention mechanism to
explore complementary information between structural and
functional images. Traditional transformers haven’t been thor-
oughly studied in the context of brain network computing, and
they just model relationships between brain regions within
a single modality, which fails to effectively explore the
complementary information between modalities. To mine the
complementary information between fMRI and DTI, we devise
the swapping bi-attention mechanism (SBM) to proficiently
align functional features with microstructural information. It can facilitate the synergistic exchange of information
between bimodal images. In this section, we first introduce
4604 IEEE TRANSACTIONS ON NEURAL SYSTEMS AND REHABILITATION ENGINEERING, VOL.

**Passage 19:**

> ontributions to this work are as follows:
• The proposed CT-GAN is proposed to transform the fMRI
and DTI into multimodal connectivity for AD analysis by
combining the generative adversarial strategy. It not only
learns the topological characteristics of non-Euclidean
space but also deeply fuses complementary information
in an efficient end-to-end manner.
• The swapping bi-attention mechanism (SBM) is devel-
oped to effectively align functional information with
microstructural information and enhance the complemen-
tary information between bimodal images.
• The dual-channel separator with cross-weighting scheme
is devised to decompose multimodal connectivity into
functional and structural connectivities, which preserve
global topological information and ensure the high quality
and diversity of the generated connectivities.

**Passage 20:**

> efine functional
connectivity. The neural fiber connection strength between
brain regions is defined as SC. It makes use of diffusion
tensor imaging (DTI) to measure water molecular dispersion
motion. The structural and functional connectivity can describe
AD patients’ pathological features from different perspec-
tives. AD patients exhibit damage to their structural con-
nections [10], which affects information transmission and
© 2023 The Authors. This work is licensed under a Creative Commons Attribution 4.0 License. For more information, see https://creativecommons.org/licenses/by/4.0/
4602 IEEE TRANSACTIONS ON NEURAL SYSTEMS AND REHABILITATION ENGINEERING, VOL. 31, 2023
processing and results in cognitive dysfunction. Besides, early-
stage AD patients show weakened and enhanced changes in
the functional connectivity strength [11].

**Passage 21:**

> ultimodal connectivity matrices at different
stages of cognitive disease (a) NC; (b) AD. Fig. 5. The ten most important brain regions between NC and EMCI
groups.
the structural connection is computed. The requirements are
configured in PANDA as the fiber tracking halting conditions:
a crossing angle of greater than 45 degrees between two
traveling directions. The predictor is implemented by the row-based filters in the
work [47]. The embedding dimension in the generator G is
set at 128. L = 5 layers of transformer are utilized to fuse
structural and functional embeddings. The heads in the trans-
former block are 8. The model’s parameters will be updated
during the training process using the Adam algorithm. The
learning rate is set to 0.001. The weight decay is set to 0.01.

**Passage 22:**

> tivity matrices, with the threshold
values set at 50% and 75% respectively. The second and fourth columns are the increased connectivity matrices with the threshold values at 50%
and 75% respectively. TABLE II
PREDICTION OF PERFORMANCE UNDER DIFFERENT MODELS AND CLASSIFIERS BY FUSING F MRI AND DTI(%)
proposed CT-GAN has the benefit of being more accurate than
previous multimodal fusion models in predicting the phases
of AD. To evaluate the AD-related ROIs in the classification tasks,
we utilized the LOOCV method [6] to compute the impor-
tant score for each ROI. To calculate the importance score
for each ROI, we first began to remove one row and one
column corresponding to one particular ROI in the generated
multimodal connectivity matrix. We then computed the mean
classification accuracy of the removed connectivity matrices.

**Passage 23:**

> luding the normal
control (NC), early mild cognitive impairment (EMCI), late
mild cognitive impairment (LMCI), and AD. p(Y |C(G(x, y)))
is the probability that the subject is predicted to be stage Y . Pair-wise Connectivity Reconstruction Loss. To impose
an additional topological constraint on the cross-modal trans-
former generator, we add the L1 pair-wise connectivity
reconstruction loss in the model’s optimization process. The
overall pair-wise connection gap between empirical FC/SC
matrices and FC/SC matrices are minimized by the following
formula:
LFC
pcr = ∥FC − FC′∥1, (19)
LSC
pcr = ∥SC − SC′∥1. (20)
III. E XPERIMENTS
A. Preprocessing and Settings
The ADNI (Alzheimer’s Disease Neuroimaging Initiative)
public dataset is used to test our CT-GAN model. Table I
contains full information about the 268 patients whose data
we used in this study.

**Passage 24:**

> ive adversarial network (CT-GAN) is proposed to
effectively fuse the functional and structural information
contained in functional magnetic resonance imaging (fMRI)
and diffusion tensor imaging (DTI). The CT-GAN can learn
topological features and generate multimodal connectivity
from multimodal imaging data in an efficient end-to-end
manner. Moreover, the swapping bi-attention mechanism
is designed to gradually align common features and
effectively enhance the complementary features between
modalities. By analyzing the generated connectivity fea-
tures, the proposed model can identify AD-related brain
connections. Evaluations on the public ADNI dataset show
that the proposed CT-GAN can dramatically improve pre-
diction performance and detect AD-related brain regions
effectively. The proposed model also provides new insights
into detecting AD-related abnormal neural circuits.

</details>

---

## Brain-Tissue-Segmentation-from-MRI-Scans-using-Digit_2025_Procedia-Computer-
_File: `Brain-Tissue-Segmentation-from-MRI-Scans-using-Digit_2025_Procedia-Computer-.pdf`_

1. **Was diffusion MRI (DTI, dMRI, DWI, or similar) used in this paper?**  
   **NO DIFFUSION MRI PROCESSING FOUND**  
   The paper explicitly mentions "Diffusion tensor imaging (DTI)" as one of several imaging technologies (e.g., MRI, PET, CT) but does not describe any processing steps or parameters specific to diffusion MRI. All processing steps described are for structural MRI (sMRI), not diffusion MRI.

---

2. **What processing steps were applied to the diffusion images?**  
   **Not reported in available text.**  
   The paper does not describe any processing steps for diffusion MRI. All processing steps (e.g., skull stripping, CLAHE, Otsu thresholding) are explicitly for structural MRI (sMRI).

---

3. **What software or tools are explicitly named for processing?**  
   **Not reported in available text.**  
   No specific software or tools (e.g., FSL, MRtrix, etc.) are explicitly named for diffusion MRI processing. The paper references general techniques like "CLAHE" and "Otsu thresholding" but does not link them to diffusion MRI.

---

4. **What acquisition or processing parameters are explicitly reported?**  
   **Not reported in available text.**  
   The paper reports parameters for structural MRI (e.g., 3D image size: 256x256x170 pixels, random selection of 2D slices), but no diffusion MRI-specific parameters (e.g., b-values, diffusion directions) are mentioned.

---

5. **Copy the exact sentences from the excerpts that describe the processing.**  
   - "The size of each of these images in 3 Dimensions is 256x256x170 pixels."  
   - "CLAHE Equalized scan" (referenced in a figure caption).  
   - "The brain is the fundamental seat of learning... skull stripping plays an important role in detecting pathology and multi-modality brain image registration."  
   - "The segmentation method used in this study mainly depends on the Largest Connected component..."  
   - "The preprocessing step involves contrast enhancement using CLAHE, binarization of the scan using Otsu thresholding, and de-blurring..."  

   These sentences describe structural MRI preprocessing, not diffusion MRI.

---

6. **Is the processing description complete, or does it appear incomplete/missing?**  
   **Incomplete.**  
   The paper describes preprocessing steps for structural MRI (sMRI) but does not mention diffusion MRI (DTI, dMRI, etc.) at all. The processing description is limited to sMRI techniques and does not address diffusion MRI.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> nd the natural aging process, and the doctors also have limited knowledge of the disease. However, deep learning techniques can address these issues that a conventional diagnosis system nearly misses. The
presented study encompasses the pre-processing of sMRI scans which involves acquiring data, converting it into
structured format, applying pre-processing steps, and preparing the data for further suitable classification process. 3. REVIEW OF RELA TED WORK
In their attempt to address the issue of extracting the brain from the cranium in multiple T1-Weighted MRI imaging
slices Duarte et al.[18] have used Digital image Processing techniques to strip the skull from the brain MRI scan as
it is not a ffected from Alzheimer’s Disease and is not required for this particular study.

**Passage 2:**

> necessary to further segment
the brain tissues and identify the region of interest. Also, skull stripping plays an important role in detecting pathology
and multi-modality brain image registration. 5. Discussion and Comparative Analysis
The previous section demonstrates the preprocessing of MRI scans so as to extract the Region of interest which
in this case is the brain tissue. The preprocessing of sMRI is beneficial for further classification of the scans into
three main classes. The Region of Interest is well-marked after the segmentation of the brain scan is done. The brain
mask along with the segmented brain structure is shown in Fig 4. The segmentation method used in this study mainly
depends on the Largest Connected component which is one of the most fundamental operations in Computer vision.

**Passage 3:**

> ybrid approach to the skull stripping problem in mri,”
NeuroImage, vol. 22, no. 3, pp. 1060– 1075, 2004.
[26] K. Tartarotti Nepomuceno Duarte, M. Andrade Nascimento Moura, P . Sergio Martins and M. A. Garcia de Carvalho, ”Brain Extraction in Mul-
tiple T1-weighted Magnetic Resonance Imaging slices using Digital Image Processing techniques,” in IEEE Latin America Transactions, vol. 20, no. 5, pp. 831-838, May 2022, doi: 10.1109 /TLA.2022.9693568. keywords: Brain;Magnetic resonance imaging;Histograms;Software algo-
rithms;Data mining;Image edge detection;Diseases;Image Processing;Skull Stripping;Brain Extraction;Image Segmentation;Medical Imaging,

**Passage 4:**

> rea) and bright intensity fat
areas become the basis of this work. After identifying this idea, we proposed the step-by-step illustration of this work
with the help of a flow diagram in (Fig 2.). 4.1. Image Acquisition
1)Acquiring dataset for analysis: MRI scans are obtained using ADNI which provides MRI scans in the nifty
or nii format. These files initially are converted into 2D slices of 682 images each. These images are then selected
36 Sushmita Chauhan  et al. / Procedia Computer Science 260 (2025) 32–39
Fig. 3. CLAHE Equalized scan
randomly for further pre-processing and finally for brain extraction from the skull. The size of each of these images
in 3 Dimensions is 256x256x170 pixels. A batch file is used to read and convert all of the MRI scans into 2D images. 4.2.

**Passage 5:**

> ScienceDirect
Available online at www.sciencedirect.com
Procedia Computer Science 260 (2025) 32–39
1877-0509 © 2025 The Authors. Published by Elsevier B.V . This is an open access article under the CC BY-NC-ND license ( https://creativecommons.org/licenses/by-nc-nd/4.0 )
Peer-review under responsibility of the scientific committee of the Seventh International Conference on Recent Trends 
in Image Processing and Pattern Recognition. 10.1016/j.procs.2025.03.174
Keywords: Alzheimer’s Disease; Digital Image Processing; Magnetic Resonance Imaging; Brain Extraction. 1. Introduction
In this age of progress and innovation, the potential technological advancements, especially in the field of health-
care, have resulted in an increased life expectancy. However, the rate of age-related diseases has also accelerated with
time.

**Passage 6:**

> . 33, no. 20, pp. 13587–13599, 2021,
doi: 10.1007/s00521-021-05983-y.
[22] “Analysis of functional neuroimages.” http: //afni.nimh.nih.gov.
[23] A. Mikheev, G. Nevsky, S. Govindan, R. Grossman, and H. Rusinek, “Fully automatic segmentation of the brain from t1-weighted MRI using
bridge burner algorithm,” Journal of Magnetic Resonance Imaging, vol. 27, pp. 1235–1241, May 2008.
[24] S. A. Sadananthan, W. Zheng, M. W. Chee, and V . Zagorodnov, “Skull stripping using graph cuts,” NeuroImage, vol. 49, pp. 225–239, Jan. 2010.
[25] F. S ´egonne, A. Dale, E. Busa, M. Glessner, D. Salat, H. Hahn, and B. Fischl, “A hybrid approach to the skull stripping problem in mri,”
NeuroImage, vol. 22, no. 3, pp. 1060– 1075, 2004.
[26] K. Tartarotti Nepomuceno Duarte, M. Andrade Nascimento Moura, P . Sergio Martins and M. A.

**Passage 7:**

> uarte et al.[18] have used Digital image Processing techniques to strip the skull from the brain MRI scan as
it is not a ffected from Alzheimer’s Disease and is not required for this particular study. In their attempt to extract the
brain from the skull, the authors have proposed an approach in which T1 weighted approach plays a key role which
states that the dark intensity area refers to the skull and the bright intensity refers to the fat part of the brain which is
affected by Alzheimer’s disease. It is noteworthy to state that only the Axial plane also known as the horizontal plane
has been incorporated in their study. The quantitative metrics used to evaluate their results included Specificity and
Precision which was about 90 percent, F-Measure as well as Accuracy surpassed 80 % and Recall achieved in their
experiments was better than 70%.

**Passage 8:**

> .6% 98.8%
GCUT [24] 95.2% 94.0%
FreeSurfer [25] 94.8% 94.0%
Contouring Method [26] 91.2% 96.9%
38 Sushmita Chauhan  et al. / Procedia Computer Science 260 (2025) 32–39
Fig. 4. Brain mask generation
6. Conclusion
With the alarming rate at which memory-related problems along with Alzheimer’s Disease have increased over the
years, it becomes all the more necessary to study and analyze the human brain and its complexities. The presented work
becomes one of the most basic yet important steps for brain extraction from the skull. Additionally, e fficient digital
image processing techniques have been discussed so that any distortion that might have occurred during scanning can
be removed. Further, image preprocessing helps in better and more e ffective analysis of scans so that the points or
regions of interest can be projected and studied easily as well as extensively.

**Passage 9:**

> di fferent modes of imaging technologies are in use viz magnetic resonance imaging (MRI), positron emission
tomography (PET), Diffusion tensor imaging (DTI) and computerized tomography (CT) scans[16]. Atrophy or shrinkage of the brain’s hippocampus area is one of the most important biomarkers. Structurally, MRI
forms the basis of computer-aided diagnosis (CAD) for early detection of AD as well as MCI. sMRI-based CAD
methods are one of the basic and the most commonly used tests in neuroscience and neurosurgery. It provides a
detailed image of the brain in three dimensions i.e., axial (from top to down), sagittal (from side to side), and coronal
(from front to back) as shown in Fig. 1.

**Passage 10:**

> . 371–386, 2021, doi: 10.14283 /jpad.2021.23.
[16] Z. Xia, T. Zhou, S. Mamoon, and J. Lu, “Recognition of Dementia Biomarkers with Deep Finer-DBN,” IEEE Trans. Neural Syst. Rehabil. Eng., vol. 29, pp. 1926–1935, 2021, doi: 10.1109 /TNSRE.2021.3111989.
[17] “Initiative, Alzheimer’s Disease Neuroimaging.” [Online]. Available: https: //adni.loni.usc.edu/
[18] Duarte, K. T. N., Moura, M. A. N., Martins, P . S., and de arvalho, M. A. G. (2022). Brain Extraction in Multiple T1-weighted Magnetic
Resonance Imaging slices using Digital Image Processing techniques. IEEE Latin America Transactions, 20(5), 831-838.
[19] L. Alzubaidi et al., Review of deep learning: concepts, CNN architectures, challenges, applications, future directions, vol. 8, no. 1. Springer
International Publishing, 2021. doi: 10.1186 /s40537-021-00444-8.
[20] C. Lian, M. Liu, J. Zhang, and D.

**Passage 11:**

> finally for brain extraction from the skull. The size of each of these images
in 3 Dimensions is 256x256x170 pixels. A batch file is used to read and convert all of the MRI scans into 2D images. 4.2. Preprocessing
1) Selecting 2D slices for analysis : In this section, we discuss the random selection of 2D images in the three
different planes for analysis i.e. Axial, Coronal and-Sagittal. The dataset is sliced into 3 Dimensions as mentioned
above. Axial and Coronal images are 256 in number each and Sagittal are 170 in number.Our study focuses on the
Sagittal and coronal dimensions of the scan. The sagittal dimension provides the side view of the brain as shown in
Fig 1 and the coronal section provides a detailed cross-sectional view which is indicative of the hippocampus and the
entorhinal cortex which are the parts of the brain that are mainly a ffected by Alzheimer’s disease.

**Passage 12:**

> nted brain structure is shown in Fig 4. The segmentation method used in this study mainly
depends on the Largest Connected component which is one of the most fundamental operations in Computer vision. Computationally this method is light as it does not require much resources as compared to 3D data. Also, it helps
in boundary detection, shape analysis, Region isolation, and most important segmentation.A tabulated study on the
comparative analysis of various methods used for Brain Extraction has been shown in Table 1. Comparative Analysis according to Sensitivity and Specificity:
Method Sensitivity Specificity
3D Skull Strip[22] 90.6% 96.2%
BB [23] 80.6% 98.8%
GCUT [24] 95.2% 94.0%
FreeSurfer [25] 94.8% 94.0%
Contouring Method [26] 91.2% 96.9%
38 Sushmita Chauhan  et al. / Procedia Computer Science 260 (2025) 32–39
Fig. 4. Brain mask generation
6.

**Passage 13:**

> (t) (5)
σ 2
1(t) =
t∑
i=1
[i − µ1(t)]2 P(i)/w1(t) (6)
and σ 2
2(t) =
I∑
i=t+1
[i − µ2(t)]2 P(i)/w2(t) (7)
The in-class variance is calculated by substituting the values of µ and σ in equation (1)
4.3. Brain Extraction
The brain is the fundamental seat of learning, thinking, and doing day-to-day jobs; therefore, it becomes vital that
it is studied precisely without taking into consideration the outer cranial structure, which otherwise is present in all
MRI scans. In the present study, the skull is separated from the brain structure which is necessary to further segment
the brain tissues and identify the region of interest. Also, skull stripping plays an important role in detecting pathology
and multi-modality brain image registration. 5.

**Passage 14:**

> 181 subjects of the ADNI dataset with
an accuracy of 86.74%. 4. PROPOSED APPROACH
In this section the approach followed for the extraction of the brain from the skull in MRI scans has been discussed. The basis of this approach is the fact that brain MRI scans have di fferent intensities of gray areas which di ffers from
region to region. Also, there is variation in the T1 intensity in accordance with the water-filled areas of the brain
which makes it di fficult for using conventional thresholding techniques. The largest connected component which is
considered in this work is the brain and the intensity di fferences between the skull (dark area) and bright intensity fat
areas become the basis of this work. After identifying this idea, we proposed the step-by-step illustration of this work
with the help of a flow diagram in (Fig 2.). 4.1.

**Passage 15:**

> method-
ology used for the extraction of the brain area from the skull and other non-required parts of the scan. Also, metrics
used to evaluate the proposed methodology have been discussed in detail. Section 4 involves the experimentation used
for extracting the brain from the skull and finally, section 5 involves the Conclusion of our work. 34 Sushmita Chauhan  et al. / Procedia Computer Science 260 (2025) 32–39
Fig. 1. Axial, Coronal and Sagittal dimensions of the brain
2. Motivation
The presented work is based on Alzheimer’s Disease which is an incurable neurodegenerative disease that a ffects
the elderly population and is increasing at an alarming rate due to the current lifestyle which is full of stress, anxiety,
and other environmental factors.

**Passage 16:**

> diction of age-related diseases like Alzheimer’s
disease. Nowadays With the increase in life expectancy and the extravagant use of technology, it is evident that neurological
diseases are on the rise. Therefore, it becomes essential that such diseases can be diagnosed at an early stage of their occurrence. The proposed work presents brain extraction from the skull with the help of three basic steps, data acquisition, pre-processing, and
largest connected component extraction using contours . The data acquired is using the ADNI data repository. The preprocessing
step involves contrast enhancement using CLAHE, binarization of the scan using Otsu thresholding, and de-blurring so that the
noise that might be there in the scans can be removed and a clear image of the brain is available for further processing and
classification of Alzheimer’s disease.
© 2025 The Authors.

**Passage 17:**

> harp edges and
fine details get smeared, which make the identification of di fferent regions of the brain, di fficult. Intentional blurring
is done by adjusting the kernel size of the Gaussian Filter. 4)Binarization: The original brain scans are subjected to a two-step process, the first being grayscale conversion
and the second is Otsu thresholding which is a global binarization method in which the grayscale image is assumed to
consist of only two types of pixels one foreground and the other background pixels. It is a variance-based binarization
technique where the pixels are divided into two clusters which minimises the intra-cluster variation by increasing the
inter-cluster variance.

**Passage 18:**

> ience and neurosurgery. It provides a
detailed image of the brain in three dimensions i.e., axial (from top to down), sagittal (from side to side), and coronal
(from front to back) as shown in Fig. 1. The Dataset used for this study has been taken from Alzheimer’s Disease Neuroimaging Initiative (ADNI)[17]
which is an open-source repository maintained by USC.In order to track and detect the early stage of AD, the ADNI is
a longitudinal cohort of clinical, imaging, genetic and biochemical biomarkers. This article has been organized in the
following manner and Section 2, presents a brief review of the literature. Section 3, describes the proposed method-
ology used for the extraction of the brain area from the skull and other non-required parts of the scan. Also, metrics
used to evaluate the proposed methodology have been discussed in detail.

**Passage 19:**

> ive neurode-
generative disease that slowly destroys memory, the capability to think and reason out, and eventually to carry out
∗ Corresponding author. Tel.: + 0-000-000-0000 ; fax: + 0-000-000-0000. E-mail address: poonamsaini@pec.edu.in
7th International Conference on Recent Trends in Image Processing and Pattern Recognition
(RTIP2R-2024)
Brain Tissue Segmentation from MRI Scans using Digital Image
Processing
Sushmita Chauhana, Poonam Sainia,∗, Sanjeev Sofata
a Department of Computer Science and Engineering, Punjab Engineering College (Deemed to be university), Sector 12 Chandigarh, 160012. Abstract
The brain is one of the most unexplored parts of the human body and its complex and delicate structure has scientists worldwide
looking for answers about its intricacies.

**Passage 20:**

> nal section provides a detailed cross-sectional view which is indicative of the hippocampus and the
entorhinal cortex which are the parts of the brain that are mainly a ffected by Alzheimer’s disease. 2) Contrast limited adaptive histogram equalization : This particular method deals with the dispersion of intensity
values in order to produce an improved image in terms of contrast. This particular method is di fferent from Histogram
Equalization in terms of a number of histograms each belonging to a segment of a di fferent segment of the image
and utilizes them for redistribution of the lightness value of the image.CLAHE functions in a way that divides the
entire image into tiles. Blending of the boundaries of these tiles is done using bilinear interpolation which removes
the false boundaries and improves the overall contrast of the image.

**Passage 21:**

> ated. Fan et al. [21] have performed a Unet-based analysis of MRI data for AD diagnosis. The method so implemented
by the authors is a combination of encoding and decoding along with skip connections. The skip connections combine
the high-level semantics and the low-level fine-grained surface representation, which results in more information
utilization from the images for further classification. The region of interest for the model is explored by the 3D Grad
CAM method which is implemented after preprocessing steps like clipping and sampling of images, normalization of
intensity, and finally brain extraction. The proposed Unet model is applied to 181 subjects of the ADNI dataset with
an accuracy of 86.74%. 4. PROPOSED APPROACH
In this section the approach followed for the extraction of the brain from the skull in MRI scans has been discussed.

**Passage 22:**

> rm joint atrophy localization and AD classification at every level be it patch, region, or subject level. The proposed method was evaluated in terms of AD classification and MCI conversion prediction. AD classification
between AD vs NC reached an accuracy of 0.90 along with sensitivity and specificity of 0.82, and 0.97 respectively,

Sushmita Chauhan  et al. / Procedia Computer Science 260 (2025) 32–39 35
Fig. 2. Workflow
and AUC of 0.95, while MCI conversion between pMCI vs sMCI the model reached an accuracy of 0.81, sensitivity
of 0.53, specificity of 0.85 and AUC of 0.78 was evaluated. Fan et al. [21] have performed a Unet-based analysis of MRI data for AD diagnosis. The method so implemented
by the authors is a combination of encoding and decoding along with skip connections.

**Passage 23:**

> ncepts, CNN architectures, challenges, applications, future directions, vol. 8, no. 1. Springer
International Publishing, 2021. doi: 10.1186 /s40537-021-00444-8.
[20] C. Lian, M. Liu, J. Zhang, and D. Shen, “Hierarchical fully convolutional network for joint atrophy localization and Alzheimer’s disease diag-
nosis using structural MRI,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 42, no. 4, pp. 880–893, 2020, doi: 10.1109 /TPAMI.2018.2889096.
[21] Z. Fan et al., “U-net based analysis of MRI for Alzheimer’s disease diagnosis,” Neural Comput. Appl., vol. 33, no. 20, pp. 13587–13599, 2021,
doi: 10.1007/s00521-021-05983-y.
[22] “Analysis of functional neuroimages.” http: //afni.nimh.nih.gov.
[23] A. Mikheev, G. Nevsky, S. Govindan, R. Grossman, and H.

**Passage 24:**

> can
be removed. Further, image preprocessing helps in better and more e ffective analysis of scans so that the points or
regions of interest can be projected and studied easily as well as extensively. The mask generated after segmentation
of the brain MRI scan clearly is indicative of the volume of the brain which can be further studied for classifying
whether the scan belongs to a patient su ffering from AD or not. References
[1] J. Ouyang, Q. Zhao, E. Adeli, G. Zaharchuk, and K. M. Pohl, “Disentangling Normal Aging From Severity of Disease via Weak Supervision
on Longitudinal MRI,” IEEE Trans. Med. Imaging, vol. 41, no. 10, pp. 2558–2569, 2022, doi: 10.1109 /TMI.2022.3166131.
[2] “ARDSI.” https: //ardsi.org/
[3] “2023 Alzheimer’s disease facts and figures,” Alzheimer’s Dement., vol. 19, no. 4, pp. 1598–1695, 2023, doi: 10.1002 /alz.13016.
[4] W. Is, A. S. Disease, W. H. O. Gets, and A.

</details>

---

## Cai et al. (2023) — Graph Transformer Geometric Learning of Brain Networks Using Multimodal MR Images for Brain Age Esti
_File: `Cai et al. - 2023 - Graph Transformer Geometric Learning of Brain Networks Using Multimodal MR Images for Brain Age Esti.pdf`_

1. **Yes**, diffusion MRI (DTI) was used in this paper.  
   - Excerpt: "The DTI data is preprocessed as below by using P ANDA suite 1.2.4 [...] The DTI data were corrected by eddy currents and head motion and then the fractional anisotropy (FA) images were generated by the DTI ﬁtting tool [27]."  

2. **Processing steps applied to diffusion images (in order):**  
   - Correction of eddy-current-induced distortion and simple head-motion.  
   - Extraction of FA images using DTI fitting tool.  
   - Alignment of FA images to the MNI152_T1_1mm template.  
   - Cropping of FA images to match sMRI data.  
   - Use of PANDA suite for preprocessing DTI data.  
   - Brain extraction using BET (FSL tool).  
   - Registration to MNI152_T1_1mm using FNIRT (FSL tool).  

3. **Software/tools explicitly named:**  
   - **PANDA suite 1.2.4** [29].  
   - **FSL tools** (including BET [25], FNIRT [26]).  
   - **DTI fitting tool** [27].  

4. **Acquisition/processing parameters explicitly reported:**  
   - **Resolution**: "1 mm resolution version of MNI152 template" (MNI152_T1_1mm).  
   - **Cropping**: "cropped to the size of 160 × 192 × 160" (based on a mask).  
   - **No explicit mention of b-values, number of directions, or voxel size.**  

5. **Exact sentences from excerpts describing processing:**  
   - "Similarly, after correction of eddy-current-induced distortion and simple head-motion, the FA images are extracted using DTI ﬁtting tool [27]."  
   - "The DTI data were corrected by eddy currents and head motion and then the fractional anisotropy (FA) images were generated by the DTI ﬁtting tool [27]."  
   - "They are aligned and cropped to match with the sMRI data."  
   - "The DTI data is preprocessed as below by using P ANDA suite 1.2.4 [...] after correction of eddy-current-induced distortion and simple head-motion, the FA images are extracted using DTI ﬁtting tool [27]."  

6. **Processing description completeness:**  
   - **Incomplete**. The steps are described but lack details on specific parameters (e.g., b-values, number of diffusion directions, voxel size) and some steps (e.g., exact PANDA workflow) are only partially outlined.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> re preprocessed by intensity correction with the N3 algo-
rithm [28]. We further process these data following the similar
pipeline as that in UKB dataset using the FSL tools and
MNI152 template space. Similarly, the BET [25] is used for
stripping the non-brain tissues from the source image space,
followed by image registration to the MNI152_T1_1mm. The
DTI data is preprocessed as below by using P ANDA suite
1.2.4 (https://www.nitrc.org/projects/panda/) [29]. Similarly,
after correction of eddy-current-induced distortion and simple
head-motion, the FA images are extracted using DTI ﬁtting
tool [27]. They are aligned and cropped to match with the
sMRI data.

**Passage 2:**

> and DTI data
from the UKB dataset with the preprocessing and qual-
ity control pipeline as described in [23]. These data are
fully preprocessed and available to all researchers granted
access to UKB. This pipeline includes the distortion correc-
tion, cutting down the ﬁeld of view, brain extraction and
registration by using the FMRIB Software Library (FSL,
https://fsl.fmrib.ox.ac.uk/) [24]. The MNI152 standard tem-
plate space was used as the reference space in the data
processing. The image data was processed for brain extraction
using the BET (Brain Extraction Tool) [25] and then regis-
tered to the 1 mm resolution version of MNI152 template
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 15,2026 at 22:48:26 UTC from IEEE Xplore. Restrictions apply.

**Passage 3:**

> is-
tered to the 1 mm resolution version of MNI152 template
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 15,2026 at 22:48:26 UTC from IEEE Xplore. Restrictions apply. CAI et al.: GRAPH TRANSFORMER GEOMETRIC LEARNING OF BRAIN NETWORKS USING MUL TIMODAL MR IMAGES 459
(MNI152_T1_1mm) using the FNIRT (FMRIB’s Nonlinear
Image Registration Tool) [26]. The DTI data were corrected
by eddy currents and head motion and then the fractional
anisotropy (FA) images were generated by the DTI ﬁt-
ting tool [27]. The FA images were also aligned to the
MNI152_T1_1mm as the sMRI. All sMRI and DTI data downloaded from ADNI dataset
were preprocessed by intensity correction with the N3 algo-
rithm [28]. We further process these data following the similar
pipeline as that in UKB dataset using the FSL tools and
MNI152 template space.

**Passage 4:**

> Similarly,
after correction of eddy-current-induced distortion and simple
head-motion, the FA images are extracted using DTI ﬁtting
tool [27]. They are aligned and cropped to match with the
sMRI data. To ensure that the inputs of proposed method from dif-
ferent datasets and modalities have the same size, all pre-
processed sMRI and FA images are cropped to the size of
160 × 192 × 160 based on a mask generated to remove
the uninformative zero-value pixels on the background. The
overall data preprocessing pipelines are consistent in the ADNI
and UKB datasets, but some details may not be exactly same
and subsequent ﬁne-tuning process can solve the minor data
gap problem. III. P
ROPOSED METHOD
This paper proposes a graph transformer geometric deep
learning framework to construct and combine the multimodal
brain networks from sMRI and DTI data for brain age esti-
mation, as shown in Fig.1.

**Passage 5:**

> teps in these
1558-254X © 2022 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission. See https://www.ieee.org/publications/rights/index.html for more information. Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 15,2026 at 22:48:26 UTC from IEEE Xplore. Restrictions apply. CAI et al.: GRAPH TRANSFORMER GEOMETRIC LEARNING OF BRAIN NETWORKS USING MUL TIMODAL MR IMAGES 457
methods: data preprocessing, feature extraction and age regres-
sion. For different imaging modalities, different pipelines are
used for preprocessing of raw imaging data [6], [7]. After data
preprocessing, variant measur ements are computed to charac-
terize the patterns related to brain aging.

**Passage 6:**

> oImage, vol. 62, no. 2, pp. 782–790, 2012.
[25] S. M. Smith, “Fast robust automated brain extraction,” Hum. Brain
Mapping, vol. 17, no. 3, pp. 143–155, 2002.
[26] J. L. Andersson, M. Jenkinson, and S. Smith, “Non-linear registration,
aka Spatial normalisation FMRIB technical report TR07JA2,” FMRIB
Anal. Group Univ. Oxford , vol. 2, no. 1, p. e21, 2007.
[27] C. Pierpaoli and P . J. Basser, “Toward a quantitative assessment of
diffusion anisotropy,” Magn. Reson. Med. , vol. 36, no. 6, pp. 893–906,
1996.
[28] J. G. Sled, A. P . Zijdenbos, and A. C. Evans, “A nonparametric method
for automatic correction of intensity nonuniformity in MRI data,” IEEE
Trans. Med. Imag. , vol. 17, no. 1, pp. 87–97, Feb. 1998.
[29] Z. Cui, S. Zhong, P . Xu, Y . He, and G. Gong, “PANDA: A pipeline
toolbox for analyzing brain diffusion images,” Frontiers Hum. Neurosci.,
vol. 7, p. 42, Feb. 2013.
[30] Y . LeCun, L.

**Passage 7:**

> ow et al., “U.K. biobank: An open access resource for identifying
the causes of a wide range of complex diseases of middle and old age,”
PLoS Med. , vol. 12, no. 3, 2015, Art. no. e1001779.
[22] C. R. Jack et al., “The Alzheimer’s disease neuroimaging initiative
(ADNI): MRI methods,” J. Magn. Reson. Imag., Off. J. Int. Soc. Magn. Reson. Med. , vol. 27, no. 4, pp. 685–691, 2008.
[23] F. Alfaro-Almagro et al., “Image processing and quality control for the
ﬁrst 10,000 brain imaging datasets from U.K. Biobank,” NeuroImage,
vol. 166, pp. 400–424, Feb. 2018.
[24] M. Jenkinson, C. F. Beckmann, T. E. Behrens, M. W. Woolrich, and
S. M. Smith, “FSL,” NeuroImage, vol. 62, no. 2, pp. 782–790, 2012.
[25] S. M. Smith, “Fast robust automated brain extraction,” Hum. Brain
Mapping, vol. 17, no. 3, pp. 143–155, 2002.
[26] J. L. Andersson, M. Jenkinson, and S.

**Passage 8:**

> lities, different pipelines are
used for preprocessing of raw imaging data [6], [7]. After data
preprocessing, variant measur ements are computed to charac-
terize the patterns related to brain aging. As for 3D sMRI data,
the morphological features such as tissue intensities, volumes
of ROIs (regions of interest), cortical thickness are extracted
for brain age estimation [3], [6]. As for DTI data, fractional
anisotropy (FA) map is obtained after data preprocessing,
and the ﬁber tract-tracing algorithm is used to generate a
connectivity matrix of brain ROIs as the features [4], [7]. Based on the features from MR images, brain age is estimated
by multivariate regression models such as relevance vector
regression [5], support vector regression (SVR) with random
forest (RF) [6] and backpropagation neural network [7], etc.

**Passage 9:**

> . Fu, G. Chen, J. Shen, and L. Shao, “Hi-Net: Hybrid-fusion
network for multi-modal MR image synthesis,” IEEE Trans. Med. Imag.,
vol. 39, no. 9, pp. 2772–2781, Sep. 2020.
[43] M. Xia, J. Wang, and Y . He, “BrainNet viewer: A network visualization
tool for human brain connectomics,” PLoS ONE, vol. 8, no. 7, Jul. 2013,
Art. no. e68910. Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 15,2026 at 22:48:26 UTC from IEEE Xplore. Restrictions apply.

**Passage 10:**

> Feb. 1998.
[29] Z. Cui, S. Zhong, P . Xu, Y . He, and G. Gong, “PANDA: A pipeline
toolbox for analyzing brain diffusion images,” Frontiers Hum. Neurosci.,
vol. 7, p. 42, Feb. 2013.
[30] Y . LeCun, L. Bottou, Y . Bengio, and P . Haffner, “Gradient-based
learning applied to document recognition,” Proc. IEEE , vol. 86, no. 11,
pp. 2278–2324, Nov. 1998.
[31] X. Glorot, A. Bordes, and Y . Bengio, “Deep sparse rectiﬁer neural net-
works,” in Proc. 14th Int. Conf. Artif. Intell. Statist. , 2011, pp. 315–323.
[32] S. Ioffe and C. Szegedy, “Batch normalization: Accelerating deep
network training by reducing internal covariate shift,” in Proc. 32nd
Int. Conf. Mach. Learn. , 2015, pp. 448–456.
[33] N. Tzourio-Mazoyer et al., “Automated anatomical labeling of activa-
tions in SPM using a macroscopic anatomical parcellation of the MNI
MRI single-subject brain,” NeuroImage, vol. 15, no. 1, pp.

**Passage 11:**

> rain age
estimation. A multimodal brain age estimation model was proposed to
combine the T1-weighted MRI, T2-FLAIR, T2*, diffusion-
MRI, task fMRI, and resting-state fMRI with a LASSO
regression [19]. The hand-crafted features are extracted using
complex data preprocessing with prior knowledge, which are
not jointly optimized with brain age regression. Recently, the
SFCN with linear regression (LR) was employed to com-
bine sMRI and time-of-ﬂight magnetic resonance angiography
(TOF MRA) for brain age estimation [20]. Although the CNN
architecture has powerful ability to learn the features of MR
images, the multimodal features are concatenated for ﬁnal
decision, ignoring the interactions between sMRI and DTI. The sMRI can capture the variations of brain anatomy
and morphometric atrophy while DTI captures information
about the microstructural integrity of white matter [18].

**Passage 12:**

> ils
The proposed method is implemented on a single GPU
(i.e., NVIDIA GeForce RTX 3090 24 GB), using the PyTorch
package in Python. Adam is used as an optimizer with the
default learning rate of 0.001. In order to evaluate performance
and generalization capability, we conduct the experiments on
the preprocessed T1-weighted sMRI and DTI data from UKB
and ADNI datasets as described in TABL E I I. We ﬁrst train
and evaluate our method on the UKB dataset (16458 healthy
subjects), which are randomly divided into training set
(14000 subjects), validation set (958 subjects) and test set
(1500 subjects). The ages of all subjects (with range of
[45, 81]) are split into 7 bins of ﬁve-year length.

**Passage 13:**

> than
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 15,2026 at 22:48:26 UTC from IEEE Xplore. Restrictions apply. 464 IEEE TRANSACTIONS ON MEDICAL IMAGING, VOL. 42, NO. 2, FEBRUARY 2023
T ABLE VIII
RESUL TS COMP ARISON OF OUR PROPOSED METHOD WITH
OTHER METHODS IN BRAIN AGE ESTIMA TION
the early, feature and late fusions while the proposed fusion
achieves the best performances. D. Comparison With Other Methods
T ABLE VIII compares the proposed method with other
methods recently published in the literature [8], [9], [10],
[11], [12], [15]. The compared methods are based on deep
neural networks including the 2D CNN [10], 3D CNN [8], [9],
[11], [12] and transformer [15] for brain age estimation using
T1-weighted sMRI data. For fair comparison, all methods are
performed with the same training conﬁguration on the same
training, validation and testing datasets.

**Passage 14:**

> experiments,
three metrics are used for quantitative evaluation of brain age
estimation, including mean abso lute error (MAE), root means
squared error (RMSE) and Pearson correlation coefﬁcient
(PCC). The results are presented in terms of mean ± stan-
dard deviation. For UKB dataset, we calculate the mean and
standard deviation by testing multiple age estimation models
after the training is stable. For ADNI dataset, we calculate the
mean and standard deviation of ﬁve-fold model results. Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 15,2026 at 22:48:26 UTC from IEEE Xplore. Restrictions apply. 462 IEEE TRANSACTIONS ON MEDICAL IMAGING, VOL. 42, NO.

**Passage 15:**

> ermore,
the EAD is explored as an important biomarker for AD
diagnosis. Our proposed method is trained and evaluated with
sMRI and DTI data from a large cohort of subjects on two
independent datasets. TABL E I summaries the state-of-the-art models in recent
studies for brain age estimation using MRI data with their
mean absolute error (MAE) results reported in the literature. The MAE is around 2.1–5.6 years. Our method achieves MAE
of 2.7 years, which is competitive and promising compared to
other methods. Most methods are based on CNN architecture
and sMRI data. Only a few studies have explored the fusion of
multimodal MRI data for more accurate brain age estimation. Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 15,2026 at 22:48:26 UTC from IEEE Xplore. Restrictions apply. 458 IEEE TRANSACTIONS ON MEDICAL IMAGING, VOL. 42, NO.

**Passage 16:**

> rain MRI
data [8], [9], [13]. To be more compatible with small dataset,
a simple 3D fully convolutional network (SFCN) with fewer
parameters was proposed for brain age estimation using sMRI
data [11]. A 3D two-stage-age-network (TSAN) was proposed
with the ﬁrst-stage network estimating a rough brain age,
followed by a second-stage network for more accurate esti-
mation [12]. A fusion-with-attention deep network (FiA-Net)
was proposed to fuse the intensity and RA VENS channels
of sMRI data for brain age estimation [14]. A global-local
transformer was proposed to build the 2D CNNs on whole
sMRI data and local patches to learn the global-context and
local ﬁne-grained features, resp ectively, which were combined
by self-attention mechanism for brain age estimation [15].

**Passage 17:**

> nteractions between sMRI and DTI. The sMRI can capture the variations of brain anatomy
and morphometric atrophy while DTI captures information
about the microstructural integrity of white matter [18]. They
can provide essential and complementary biomarkers for
characterization of brain structure for brain age estimation. However, it is still challenging to explore the interactions
between different ROIs and different modalities for brain
age estimation. To this end, we propose a graph transformer
geometric learning framework to construct and analyze the
multimodal brain networks of sMRI and DTI data for brain
age estimation, as shown in Fig. 1 .F i r s t ,s M R Ia n dD T I
data are processed and fed into a two-stream convolutional
autoencoder (CAE) for learning th eir latent representations.

**Passage 18:**

> lts. Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 15,2026 at 22:48:26 UTC from IEEE Xplore. Restrictions apply. 462 IEEE TRANSACTIONS ON MEDICAL IMAGING, VOL. 42, NO. 2, FEBRUARY 2023
T ABLE IV
COMP ARISON OF THE BRAIN AGE ESTIMA TION RESUL TS IN DIFFERENT NODE FEA TURES ON UKB D A T ASET
T ABLE V
COMP ARISON OF THE BRAIN AGE ESTIMA TION RESUL TS IN DIFFERENT CONSTRUCTIONS OF BRAIN NETWORK ON UKB D A T ASET
Speciﬁcally, our proposed method consists of multi-level
construction of multimodal brain networks and graph trans-
former geometric learning of the brain network.

**Passage 19:**

> 456 IEEE TRANSACTIONS ON MEDICAL IMAGING, VOL. 42, NO. 2, FEBRUARY 2023
Graph T ransformer Geometric Learning of Brain
Networks Using Multimodal MR Images
for Brain Age Estimation
Hongjie Cai ,Y u eG a o , Member, IEEE, and Manhua Liu , Member, IEEE
Abstract — Brain age is considered as an important
biomarker for detecting aging-related diseases such as
Alzheimer’s Disease (AD). Magnetic resonance imaging
(MRI) have been widely investigated with deep neural net-
works for brain age estimation. However, most existing
methods cannot make full use of multimodal MRIs due to
the difference in data structure. In this paper, we propose a
graph transformer geometric learning framework to model
the multimodal brain network constructed by structural
MRI (sMRI) and diffusion tensor imaging (DTI) for brain
age estimation.

**Passage 20:**

> ion. Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 15,2026 at 22:48:26 UTC from IEEE Xplore. Restrictions apply. 458 IEEE TRANSACTIONS ON MEDICAL IMAGING, VOL. 42, NO. 2, FEBRUARY 2023
T ABLE I
AS UMMARY OF RECENT STUDIES FOR BRAIN AGE ESTIMA TION USING MRI D ATA O F HEAL THY SUBJECTS
T ABLE II
DEMOGRAPHIC INFORMA TION OF THE STUDIED
SUBJECTS FROM ADNI AND UKB
Different from these studies, the main contributions of this
paper are summarized as below:
(1) We propose a graph transformer geometric learning
framework to build and combine the multimodal brain net-
works of sMRI and DTI, which can make full use of the local
and global multimodal features for brain age estimation.
(2) We propose a multi-level construction of brain graph
networks with diversiﬁed connections based on spatial relation,
feature correlation and cross-modal association.
(3) A graph transformer network is proposed to model
the cross-modal interaction and aggregate node features by
geometric learning for more accurate brain age estimation.

**Passage 21:**

> data for brain
age estimation, as shown in Fig. 1 .F i r s t ,s M R Ia n dD T I
data are processed and fed into a two-stream convolutional
autoencoder (CAE) for learning th eir latent representations. Second, the multi-level brain networks are constructed by
ROI feature aggregation and diversiﬁed node connections in
terms of different attributes (i.e., space, feature, and modality). Finally, a graph transformer network is proposed to model
the interactions of intra- and inter-modalities and generate a
graph representations for brain age estimation. Furthermore,
the EAD is explored as an important biomarker for AD
diagnosis. Our proposed method is trained and evaluated with
sMRI and DTI data from a large cohort of subjects on two
independent datasets.

**Passage 22:**

> ng layer of the graph transformer network. The
softmax function is used for normalization of the scores for
each subject, then we average the attention scores over all
subjects in the UKB testing set. The average scores of all
ROI nodes are sorted in descending order and the top 10 ROI
nodes are selected for visualization by BrainNet Viewer [43],
as shown in Fig. 6 . We can see that there are 8 ROIs selected
from sMRI and 2 ROIs from DTI, showing that sMRI is more
important than DTI for brain age estimation. Most ROIs are
associated with aging-induced brain atrophy, and the selected
ROIs such as Hippocampus and Amygdala are also involved
in diagnosis of dementias such as AD. Our deep learning model is trained with sMRI and DTI
data from 14000 subjects of UKB dataset, which takes
32 hours to achieve the convergence using a single NVIDIA
GeForce RTX 3090 GPU.

**Passage 23:**

> l interaction
and fusion by geometric learning for brain age estimation. Finally, the difference between the estimated age and the
chronological age is used as an important biomarker for AD
diagnosis. Our method is evaluated with the sMRI and DTI
data from UK Biobank and Alzheimer’s Disease Neuroimag-
ing Initiative database. Experimental results demonstrate
that our method has achieved promising performances for
brain age estimation and AD diagnosis. Index Terms — Brain age estimation, multimodal MRI,
graph transformer, brain network, Alzheimer’s disease. I. I NTRODUCTION
A
GING is a complex process that goes with the gradual
biological and physiological changes in an organism as
the individual grows older. It also takes place in human brain
Manuscript received 12 August 2022; revised 13 October 2022;
accepted 5 November 2022.

**Passage 24:**

> as such as AD. Our deep learning model is trained with sMRI and DTI
data from 14000 subjects of UKB dataset, which takes
32 hours to achieve the convergence using a single NVIDIA
GeForce RTX 3090 GPU. The inference time is fast in about
0.015 second per subject. It takes 1 hour for ﬁne-tuning the
pre-trained model on the ADNI dataset. Although our method has achieved good performance in
brain age estimation and AD diagnosis, there are several
limitations to be addressed in the future. First, in the proposed
method, the construction of brain network and graph trans-
former network are trained separately which may lead to sub-
optimal performance. An end-to-end deep learning framework
can be investigated to improve performance. Second, the
proposed method cannot deal w ith the missing modalities for
multimodal brain image analysis, limiting the datasets used for
study.

</details>

---

## Castellano et al. (2023) — Combining Unsupervised and Supervised Deep Learning for Alzheimer's Disease Detection by Fractional
_File: `Castellano et al. - 2023 - Combining Unsupervised and Supervised Deep Learning for Alzheimer's Disease Detection by Fractional.pdf`_

1. **Yes**, diffusion MRI (specifically **DWI** and **DTI**) was used in this paper.  
2. **Processing steps** (in order):  
   - Brain mask extraction using **Otsu thresholding** followed by **dilation**.  
   - **Ordinary least squares method** with **b-values** and **b-vectors** to fit the **diffusion tensor** (3×3 symmetric matrix) to each voxel.  
   - Calculation of **fractional anisotropy (FA)** from the DTI.  
   - **Scaling** to a common resolution of **2.50 mm/px** in three dimensions.  
   - **Rotation** according to the **RPS direction** (left to right, anterior to posterior, inferior to superior).  
   - **Cropping** to a size of **96 × 96 × 64px**.  
3. **Software/tools**:  
   - **Dipy** for DTI analysis.  
   - **Kornia** and **TorchIO** for data augmentation.  
   - **PyTorch** and **PyTorch Lightning** for model implementation.  
4. **Reported parameters**:  
   - **Scaling resolution**: 2.50 mm/px in three dimensions.  
   - **Cropped size**: 96 × 96 × 64px.  
   - **Minimum number of volumes (shells)**: ≥10 (discarded DWIs with <10 volumes).  
5. **Exact sentences**:  
   - "Moreover, a brain mask was extracted using the Otzu thresholding method followed by a dilation operation; this mask was used to separate the brain volume from the background."  
   - "the ordinary least squares method was used with the corresponding b-values and b-vectors to ﬁt the diffusion tensor (a 3 × 3 symmetric matrix) to each voxel in order to obtain the diffusion tensor image."  
   - "images were cropped to a size of 96 × 96 × 64px."  
   - "scans were scaled to match a common resolution of 2.50 mm/px in the three dimensions and rotated according to the RPS direction (left to right, anterior to posterior, inferior to superior)."  
6. **Processing description completeness**:  
   The description is **complete** as per the excerpts. All explicitly stated steps are included, and no additional steps are inferred.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> r, inferior
to superior). Moreover, a brain mask was extracted using the
Otzu thresholding method followed by a dilation operation;
this mask was used to separate the brain volume from the
background. Then, the ordinary least squares method was
used with the corresponding b-values and b-vectors to ﬁt the
diffusion tensor (a 3 × 3 symmetric matrix) to each voxel
in order to obtain the diffusion tensor image. From the DTI
obtained so far, the fractional anisotropy was calculated as:
FA =
√
1
2
(λ1 − λ2)2 +(λ1 − λ3)2 +(λ2 − λ3)2
λ2
1 +λ2
2 +λ2
3
where λi are the eigenvalues of the diffusion tensor. As a
ﬁnal step, the images were cropped to a size of 96 × 96 ×
64px. This measurement and the chosen resolution represented
a volume of 1470 cm3 sufﬁcient for the average brain volume
of 1270 cm3 and 1130 cm3 for men and women respectively.

**Passage 2:**

> e limited number of samples,
we also used online data augmentation techniques, precisely
a combination of z-axis mirroring (resulting in hemisphere
swapping), three-dimensional rotation, and clipping. These
three transformations were applied randomly with a speciﬁc
probability during training: mirroring was applied with a
probability of 0.5, rotation with 0.75, and clipping with 0.8. Finally, further preprocessing was required to extract frac-
tional anisotropy from the DWI before training the models. First, the scans were scaled to match a common resolution of
2.50 mm/px in the three dimensions and rotated according to
the RPS direction (left to right, anterior to posterior, inferior
to superior). Moreover, a brain mask was extracted using the
Otzu thresholding method followed by a dilation operation;
this mask was used to separate the brain volume from the
background.

**Passage 3:**

> V an Der Walt,
M. Descoteaux, I. Nimmo-Smith, and D. Contributors, “Dipy, a library
for the analysis of diffusion MRI data,” Frontiers in neuroinformatics,
vol. 8, p. 8, 2014.
[35] L. N. Smith and N. Topin, “Super-convergence: V ery fast training of
neural networks using large learning rates,” inArtiﬁcial intelligence and
machine learning for multi-domain operations applications, vol. 11006. SPIE, 2019, pp. 369–386. 516
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 15,2026 at 22:44:07 UTC from IEEE Xplore. Restrictions apply.

**Passage 4:**

> d radial diffusivity, may provide additional
information about the integrity of white matter in the brain. The proposed approach could be extended to provide a more
comprehensive analysis of DTI data. Finally, using unsuper-
vised pre-training may be advantageous to alleviate the need
for labels that may be difﬁcult to collect in the medical
ﬁeld. This approach could be further explored to improve
the robustness and generalization of the proposed approach,
especially when dealing with small and unbalanced datasets.

**Passage 5:**

> “Deep residual learning for image
recognition,” inProceedings of the IEEE conference on computer vision
and pattern recognition, 2016, pp. 770–778.
[32] J. Shi, E. Riba, D. Mishkin, F. Moreno, and A. Nicolaou, “Differentiable
data augmentation with Kornia,”arXiv preprint arXiv:2011.09832, 2020.
[33] F. P ´erez-Garc´ıa, R. Sparks, and S. Ourselin, “TorchIO: a Python li-
brary for efﬁcient loading, preprocessing, augmentation and patch-based
sampling of medical images in deep learning,”Computer Methods and
Programs in Biomedicine, vol. 208, p. 106236, 2021.
[34] E. Garyfallidis, M. Brett, B. Amirbekian, A. Rokem, S. V an Der Walt,
M. Descoteaux, I. Nimmo-Smith, and D. Contributors, “Dipy, a library
for the analysis of diffusion MRI data,” Frontiers in neuroinformatics,
vol. 8, p. 8, 2014.
[35] L. N. Smith and N.

**Passage 6:**

> Combining Unsupervised and Supervised Deep
Learning for Alzheimer’s Disease Detection by
Fractional Anisotropy Imaging
Giovanna Castellano
Dept. of Computer Science
University of Bari
Bari, Italy
giovanna.castellano@uniba.it
Eufemia Lella
Innovation Lab
Exprivia S.p.A.

**Passage 7:**

> tion by Induced Local Interactions:
Examples Employing Nuclear Magnetic Resonance,” Nature, vol. 242, no. 5394, pp. 190–191, mar 1973. [Online]. Available:
https://doi.org/10.1038
[9] G. Placidi, MRI. CRC Press, may 2012. [Online]. Available:
https://doi.org/10.1201
[10] R. Jain, N. Jain, A. Aggarwal, and D. J. Hemanth,
“Convolutional neural network based Alzheimer’s disease classiﬁcation
from magnetic resonance brain images,” Cognitive Systems
Research, vol. 57, pp. 147–159, 2019. [Online]. Available:
https://www.sciencedirect.com/science/article/pii/S1389041718309562
[11] N. M. Khan, M. Hon, and N. Abraham, “Transfer Learning with
intelligent training data selection for prediction of Alzheimer’s Disease,”
2019. [Online]. Available: http://arxiv.org/abs/1906.01160
[12] H. Acharya, R. Mehta, and D.

**Passage 8:**

> to a size of 96 × 96 ×
64px. This measurement and the chosen resolution represented
a volume of 1470 cm3 sufﬁcient for the average brain volume
of 1270 cm3 and 1130 cm3 for men and women respectively. Since the values of the FA voxels are within the range [0, 1],
scaling was not necessary. V. E XPERIMENTS
The experiments were run on Kaggle. The model archi-
tectures were implemented using the PyTorch and PyTorch
Lightning libraries, while data augmentation was achieved
with the Kornia [32] and TorchIO [33] libraries. Instead, all
preprocessing steps were performed using Dipy [34]. The classiﬁcation model was evaluated using a stratiﬁed
10-fold cross-validation, taking care that the same subject
was not present in both training and validation sets, as this
could have led to overly optimistic results.

**Passage 9:**

> each
subject, one or more sessions have been performed over time,
and some sessions have more than one scan available. For this
work, we considered the 1754 DWI sessions, corresponding
to 3255 scans. In addition, to further increase the number
of samples, we used the IXI dataset [29], which provides
400 DWI sessions of cognitively normal subjects. While DWI
refers to the contrast of acquired images, DTI is a speciﬁc
type of DWI modeling [30]. It allows the measurement of
other diffusion parameters, such as fractional anisotropy. Each available DWI was analyzed to ﬁnd corrupted scans
and sessions with a mismatch between the b-values, the b-
vectors, and the corresponding number of volumes. The b-
values and b-vectors describe each volume’s magnetic ﬁeld
strength and direction. We also discarded DWIs with less than
ten volumes (shells).

**Passage 10:**

> ional neural
networks,” PLOS ONE , vol. 15, no. 3, 2020. [Online]. Available:
https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0230409
[28] L. Houria, N. Belkhamsa, A. Cherfa, and Y . Cherfa, “Multi-modality
MRI for Alzheimer’s disease detection using deep learning,” Physical
and Engineering Sciences in Medicine, vol. 45, no. 4, 2022. [Online]. Available: https://doi.org/10.1007/s13246-022-01165-9
[29] “IXI dataset.” [Online]. Available: https://brain-development.org/ixi-
dataset/
[30] J. M. Soares, P . Marques, V . Alves, and N. Sousa, “A hitchhiker’s guide
to diffusion tensor imaging,” Frontiers in neuroscience, vol. 7, p. 31,
2013.
[31] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image
recognition,” inProceedings of the IEEE conference on computer vision
and pattern recognition, 2016, pp. 770–778.
[32] J. Shi, E. Riba, D. Mishkin, F. Moreno, and A.

**Passage 11:**

> -
vectors, and the corresponding number of volumes. The b-
values and b-vectors describe each volume’s magnetic ﬁeld
strength and direction. We also discarded DWIs with less than
ten volumes (shells). After this cleaning step, the available
DWI scans became 3124. To provide a ground truth, we used
the clinicians’ judgments along with the clinical diagnoses
provided with the dataset to infer a diagnosis for each subject. From the clinicians’ judgments, we obtained the age from
which the subject ﬁrst manifested signs of mental illness. At the same time, the clinical diagnoses provide information
about the subject’s illness, taking into account the subject’s
history.

**Passage 12:**

> to 2D CNNs, 3D
CNNs have also been studied for AD detection using MRI
data. 3D CNNs can capture the spatial relationships between
voxels in 3D MRI volumes, which may be essential for the
task at hand. Some studies have used 3D CNNs pre-trained
on natural images, while others have used a pre-training based
on autoencoders [14]–[16]. Concerning DTI [17], it is an imaging technique that
measures the diffusion of water molecules in biological tissues
in multiple directions to estimate the directionality and extent
of water diffusion, enabling the reconstruction of white matter
tracts in the brain. To this end, it has been widely used to study
brain connectivity and white matter integrity and has also been
applied to diagnosing neurodegenerative diseases, including
AD.

**Passage 13:**

> sing 3D CNNs
to detect AD with FA images. This could signiﬁcantly con-
tribute to improved performance. In addition, the use of 3D
CNNs is relatively new, as many studies have focused only on
2D CNNs. Finally, we used the recently published OASIS-3
dataset, one of the largest and most comprehensive publicly
available datasets for AD detection. III. M A TERIALS
This study was primarily based on the longitudinal OASIS-
3 dataset [7], which consists of a collection of MRI and PET
scans for 1098 subjects, of whom 609 are cognitively normal,
and 489 are in different stages of cognitive decline. For each
subject, one or more sessions have been performed over time,
and some sessions have more than one scan available. For this
work, we considered the 1754 DWI sessions, corresponding
to 3255 scans.

**Passage 14:**

> tructural
White Matter Degeneration in Alzheimer’s Disease Using Machine
Learning Classiﬁcation of Multicenter DTI Data,” PLOS ONE, vol. 8,
no. 5, 2013, publisher: Public Library of Science. [Online]. Available:
https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0064925
[24] Y . Wang, Y . Y ang, X. Guo, C. Y e, N. Gao, Y . Fang, and H. T. Ma,
“A Novel Multimodal MRI Analysis for Alzheimer’s Disease Based
on Convolutional Neural Network,” in2018 40th Annual International
Conference of the IEEE Engineering in Medicine and Biology Society
(EMBC), 2018.
[25] K. Aderghal, A. Khvostikov, A. Krylov, J. Benois-Pineau, K. Afdel,
and G. Catheline, “Classiﬁcation of Alzheimer Disease on Imaging
Modalities with Deep CNNs Using Cross-Modal Transfer Learning,” in
2018 IEEE 31st International Symposium on Computer-Based Medical
Systems (CBMS), 2018, pp. 345–350.
[26] A. Khvostikov, K.

**Passage 15:**

> for Alzheimer’s dis-
ease (AD) detection using diffusion tensor imaging, speciﬁcally
fractional anisotropy (FA) images, based on a combination of
unsupervised and supervised deep learning techniques. Our
method involves training a 3D convolutional autoencoder to learn
low-dimensional representations of FA images in an unsupervised
manner and using the learned representations to pre-train a
supervised 3D convolutional classiﬁer to predict the presence or
absence of AD. Unsupervised pre-training can improve the clas-
siﬁer’s performance, especially when difﬁcult-to-collect labeled
data are limited. We evaluate our approach on the OASIS-3
dataset and demonstrate promising performance. Index Terms—3D convolutional neural networks, Alzheimer’s
disease, autoencoder, deep learning, DTI, fractional anisotropy
I.

**Passage 16:**

> subjects) and 327 positive samples that will be
used for classiﬁcation. The discarded scans were kept aside
and, together with the samples from the IXI dataset, will be
used for autoencoder training. We ensured that the two datasets
(for classiﬁcation and autoencoder training) were disjointed;
in other words, the same subject was absent in both datasets. A summary is shown in Table I. IV . METHODS
Our model was inspired by ResNet-18 [31], in which we
replaced two-dimensional convolutions with three-dimensional
ones and replaced the ReLU activation function with
LeakyReLU with a negative slope equal to 0.2. In more detail,
TABLE I
SUMMARY OF THE COMPOSITION OF THE DA TASET
AD Healthy Other diseases Unlabeled
Subjects 173 84 78 692
Scans 327 336 155 2310
the neural network consists of a ﬁrst convolutional block with
64 ﬁlters, a kernel size of 7, stride 2, and a padding of 2.

**Passage 17:**

> CI, and normal aging,” NeuroImage:
Clinical, vol. 3, pp. 180–195, 2013. [Online]. Available:
https://www.sciencedirect.com/science/article/pii/S2213158213000934
[22] E. Lella, A. Pazienza, D. Lofu, R. Anglani, and F. Vitulano, “An
ensemble learning approach based on diffusion tensor imaging measures
for Alzheimer’s disease classiﬁcation,”Electronics, vol. 10, no. 3, p. 249,
2021.
[23] M. Dyrba, M. Ewers, M. Wegrzyn, I. Kilimann, C. Plant, A. Oswald,
T. Meindl, M. Pievani, A. L. W. Bokde, A. Fellgiebel, M. Filippi,
H. Hampel, S. Kl ¨oppel, K. Hauenstein, T. Kirste, S. J. Teipel, and
t. E. s. Group, “Robust Automated Detection of Microstructural
White Matter Degeneration in Alzheimer’s Disease Using Machine
Learning Classiﬁcation of Multicenter DTI Data,” PLOS ONE, vol. 8,
no. 5, 2013, publisher: Public Library of Science. [Online].

**Passage 18:**

> s evaluated
on the OASIS-3 dataset, yielding promising results. Future work could include evaluating the proposed method
on more extensive and diverse datasets to validate its ef-
fectiveness further. In addition, interpretation of the learned
representations could provide insights into the mechanisms
underlying AD and contribute to developing more targeted
and personalized treatment options. The method could also
be extended to other diseases, such as Parkinson’s or multiple
sclerosis, to improve early diagnosis. Other DTI modalities,
such as axial and radial diffusivity, may provide additional
information about the integrity of white matter in the brain. The proposed approach could be extended to provide a more
comprehensive analysis of DTI data.

**Passage 19:**

> our approach on the OASIS-3
dataset and demonstrate promising performance. Index Terms—3D convolutional neural networks, Alzheimer’s
disease, autoencoder, deep learning, DTI, fractional anisotropy
I. I NTRODUCTION
Alzheimer’s disease (AD) is a progressive and debilitating
neurological disorder affecting millions of people worldwide,
the early detection of which is critical for timely treatment and
improved patient outcomes [1]. In this context, diffusion tensor
imaging (DTI) is an advanced magnetic resonance imaging
(MRI) technique that has proven helpful for detecting early
signs of AD by measuring the integrity of white matter ﬁber
tracts in the brain [2]. In particular, fractional anisotropy (FA)
is a widely used metric derived from DTI, reﬂecting the degree
of anisotropy in water diffusion, which has been found to be
altered in AD patients in the literature, e.g. [3].

**Passage 20:**

> actional anisotropy (FA)
is a widely used metric derived from DTI, reﬂecting the degree
of anisotropy in water diffusion, which has been found to be
altered in AD patients in the literature, e.g. [3]. However, the analysis of FA images can be challenging due
to the complexity and variability of these data. Traditional
image analysis methods have limitations in capturing subtle
patterns in the images and require extensive feature engineer-
ing and manual intervention, which can be time-consuming
and error-prone. On the other hand, recent advances in deep
learning techniques have shown great promise in various
medical imaging applications, including AD detection by DTI,
e.g. [4], [5]. Deep learning models can learn to automatically
extract meaningful features from raw neuroimaging data and
have the potential to improve the accuracy and efﬁciency of
AD diagnosis [6].

**Passage 21:**

> tensor imaging of white matter degeneration
in early stage of Alzheimer’s disease: a review,” International Journal
of Neuroscience, vol. 130, no. 3, pp. 243–250, 2020.
[3] J. L. Dalboni da Rocha, I. Bramati, G. Coutinho, F. Tovar Moll,
and R. Sitaram, “Fractional Anisotropy changes in parahippocampal
cingulum due to Alzheimer’s Disease,”Scientiﬁc reports, vol. 10, no. 1,
p. 2660, 2020.
[4] E. Lella and G. V essio, “Ensembling complex network ‘perspectives’
for mild cognitive impairment detection with artiﬁcial neural networks,”
Pattern Recognition Letters, vol. 136, pp. 168–174, 2020.
[5] A. De and A. S. Chowdhury, “DTI based Alzheimer’s disease classiﬁ-
cation with rank modulated fusion of CNNs and random forest,”Expert
Systems with Applications, vol. 169, p. 114338, 2021.
[6] M. A. Ebrahimighahnavieh, S. Luo, and R.

**Passage 22:**

> atter
tracts in the brain. To this end, it has been widely used to study
brain connectivity and white matter integrity and has also been
applied to diagnosing neurodegenerative diseases, including
AD. Traditional machine learning techniques combined with
tractography-based approaches have been applied to DTI data
for AD characterisation [18] and diagnosis at different stages
of cognitive decline [19]. Other approaches consist of feeding
traditional machine learning algorithms with features extracted
by manually selecting regions of interest from DTI data [20],
[21] or by selecting voxels through spatial-based statistics [22]. A further approach is to use principal component analysis to
reduce the dimensionality of DTI data and extract features for
the same objective [23].

**Passage 23:**

> isease Detection by
Fractional Anisotropy Imaging
Giovanna Castellano
Dept. of Computer Science
University of Bari
Bari, Italy
giovanna.castellano@uniba.it
Eufemia Lella
Innovation Lab
Exprivia S.p.A. Molfetta, Italy
eufemia.lella@exprivia.com
V alerio Longo
Dept. of Computer Science
University of Bari
Bari, Italy
v.longo20@studenti.uniba.it
Giuseppe Placidi
A2VI-Lab, c/o MeSVA Department
University of L’Aquila
L’Aquila, Italy
giuseppe.placidi@univaq.it
Matteo Polsinelli
Dept. of Computer Science
University of Salerno
Fisciano, Italy
mpolsinelli@unisa.it
Gennaro V essio
Dept. of Computer Science
University of Bari
Bari, Italy
gennaro.vessio@uniba.it
Abstract—We propose a new approach for Alzheimer’s dis-
ease (AD) detection using diffusion tensor imaging, speciﬁcally
fractional anisotropy (FA) images, based on a combination of
unsupervised and supervised deep learning techniques.

**Passage 24:**

> fractional
anisotropy, mean diffusivity, and mode of anisotropy, along
with the gray matter map from structural MRI. They accu-
rately classiﬁed AD patients and healthy controls using these
features. Similarly, Houria et al. [28] used a custom 2D CNN
architecture with an SVM-based classiﬁcation head to select
slices from two different DTI maps (fractional anisotropy and
mean diffusivity) and the gray matter map from structural
MRI. They extracted features using these three models and
combined them using an SVM to produce the ﬁnal output. The novelty of our approach lies in the combination of
unsupervised and supervised learning methods using 3D CNNs
to detect AD with FA images. This could signiﬁcantly con-
tribute to improved performance. In addition, the use of 3D
CNNs is relatively new, as many studies have focused only on
2D CNNs.

</details>

---

## Class-balancing-diversity-multimodal-ensemble-for-_2025_Computerized-Medical
_File: `Class-balancing-diversity-multimodal-ensemble-for-_2025_Computerized-Medical.pdf`_

1. **Was diffusion MRI (DTI, dMRI, DWI, or similar) used in this paper?**  
   **NO DIFFUSION MRI PROCESSING FOUND**  

2. **What processing steps were applied to the diffusion images?**  
   Not applicable (no diffusion MRI content).  

3. **What software or tools are explicitly named for processing?**  
   Not applicable (no diffusion MRI content).  

4. **What acquisition or processing parameters are explicitly reported?**  
   Not applicable (no diffusion MRI content).  

5. **Copy the exact sentences from the excerpts that describe the processing.**  
   Not applicable (no diffusion MRI content).  

6. **Is the processing description complete, or does it appear incomplete/missing?**  
   Not applicable (no diffusion MRI content).  

---  
**Explanation:** The excerpts mention MRI and PET data but do not specify diffusion MRI (DTI, dMRI, DWI) or related processing steps. No details about diffusion MRI acquisition, preprocessing, software, or parameters are present.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> ic and Intervention, Radiation Physics, Biomedical Engineering, Umeå University, Umeå, Sweden. E-mail addresses: arianna.francesconi@unicampus.it (A. Francesconi), l.dibiase@policlinicocampus.it (L.d. Biase), d.cappetta@eustema.it (D. Cappetta), 
f.rebecchi.guest@eustema.it (F. Rebecchi), p.soda@unicampus.it, paolo.soda@umu.se (P. Soda), r.sicilia@policlinicocampus.it (R. Sicilia), 
valerio.guarrasi@unicampus.it (V. Guarrasi). 1 These authors contributed equally to this work. 2 Data used in preparation of this article were obtained from the Alzheimer’s Disease Neuroimaging Initiative (ADNI) database (adni.loni.usc.edu). As such, the 
investigators within the ADNI contributed to the design and implementation of ADNI and/or provided data but did not participate in analysis or writing of this 
report.

**Passage 2:**

> tical thickness, and glucose 
metabolism in specific brain regions. These neuroimaging biomarkers 
are critical for understanding the structural and metabolic changes 
in the brain associated with AD. The Subject Characteristics modality 
encompasses demographic information (e.g., age, gender, education, 
weight, and birth date) and family history data derived from the Family 
History Questionnaire, which provides insight into genetic risk factors 
for Alzheimer’s disease by detailing the parental and sibling history of 
AD. The preprocessing pipeline was designed to ensure the quality, 
consistency, and interpretability of the data while addressing common 
challenges such as missing data and variability in scale across modali-
ties. Initially, features with more than 50% missing data were excluded 
from the analysis.

**Passage 3:**

> ementia Key Facts. Technical Report, World Health 
Organization. World Health Organization, et al., 2018. The Global Dementia Observatory Reference 
Guide. Technical Report, World Health Organization. Computerized Medical Imaging and Graphics 123 (2025) 102529 
15

**Passage 4:**

> between the training set and the 
validation/test sets. For the training set, we calculated normalization 
parameters, i.e., mean and standard deviation, and imputed missing 
values based on its data. For the validation and test sets, we used the 
normalization parameters derived from the training set’s pre-processing 
and applied the imputation method fitted on the train set to ensure 
consistency across all subsets and avoid introducing bias. 3.2. Patient selection
Our analysis involved patients from the ADNI study and we chose 
patients from the ADNI 1, GO, 2, and 3 phases. For the diagnostic tasks, 
we differentiated between CN, AD, and MCI through binary (CN vs. Computerized Medical Imaging and Graphics 123 (2025) 102529 
4 
A. Francesconi et al. Table 2
Distribution of patients for the diagnostic and early detection tasks.

**Passage 5:**

> uding features extracted 
from images, and integrating it with ML classifiers, as ML methods have 
been shown to perform better with this type of data (Shwartz-Ziv and 
Armon, 2022). 3. Materials
3.1. Dataset and pre-processing
Data for this study were obtained from the Alzheimer’s Disease 
Neuroimaging Initiative (ADNI) database (Anon, 2024), a cornerstone 
in AD’s research, due to its extensive cohort and diverse range of 
data modalities. The dataset encompasses a wide spectrum of patient 
groups, from CN individuals to those diagnosed with MCI and AD, 
making it particularly suited for multimodal analyses. ADNI consists 
of five phases: ADNI 1 (2004–2010), GO (2009–2011), 2 (2011–2016), 
3 (2016–2022), and 4 (2022-present). For this study, we used data 
Computerized Medical Imaging and Graphics 123 (2025) 102529 
3 
A. Francesconi et al.

**Passage 6:**

> R, PTEDUCAT, PTETHCAT, PTRACCAT, PTMARRY AGE, PTGENDER, PTEDUCAT, PTETHCAT, PTRACCAT, PTMARRY, 
DX_bl
 
Table A.12
External Validation Dataset: Detailed list of selected features by modality and task. Modality Diagnostic Tasks Early Detection Tasks  
 Assessment GDSATIS, GDDROP, GDEMPTY, GDBORED, GDSPIRIT, GDAFRAID 
GDHAPPY,
GDHELP, GDHOME, GDMEMORY, GDALIVE, GDWORTH, 
GDENERGY, 
GDHOPE, GDBETTER, GDTOTAL
FAQFINAN, FAQFORM, FAQSHOP, FAQGAME,
FAQBEVG, FAQMEAL, FAQEVENT, FAQTV, FAQREM, FAQTRAVL, 
CLOCKCIRC, CLOCKSYM, CLOCKNUM, 
CLOCKHAND, CLOCKTIME, CLOCKSCOR, COPYCIRC, COPYSYM, 
COPYNUM, COPYHAND, COPYTIME, COPYSCOR, AVTOT1, 
AVERR1, 
AVTOT2, AVERR2, AVTOT3, AVERR3, AVTOT4, AVERR4, AVTOT5, 
AVERR5, AVTOT6, AVERR6, AVTOTB, AVERRB, CATANIMSC, 
CATANPERS, CATANINTR, TRAASCOR, TRAAERRCOM, 
TRAAERROM, 
TRABSCOR, TRABERRCOM, TRABERROM, BNTSPONT, BNTSTIM, 
BNTCSTIM, 
BNTPHON, BNTCPHON, BNTTOTAL, AVDEL30MIN, 
AVDELERR1, AVDELTOT, AVDELERR2
 
 Subject Characteristics AGE, PTGENDER, PTEDUCAT, PTETHCAT, PTRACCAT, PTMARRY AGE, PTGENDER, PTEDUCAT, PTETHCAT, PTRACCAT, PTMARRY  
Computerized Medical Imaging and Graphics 123 (2025) 102529 
13 
A.

**Passage 7:**

> et al. Table 8
Summary of ADNI data modalities selected for external validation at baseline, detailing the number of features and percentage of missing data 
for diagnostic and early detection tasks. Modality # of features % of missing data
 Diagnostic tasks Early detection tasks Diagnostic tasks Early detection tasks 
 Assessment 16 56 0.03 10.70  
 Subject Characteristics 6 6 0.52 0  
Table 9
External validation data fusion performance: top-performing classifier (“Best G-mean” 
of the “Best Classifier”) and average performance across classifiers (“Average G-mean”) 
based on G-mean for each task.

**Passage 8:**

> Arianna Francesconi is a Ph.D. student enrolled in the National 
Ph.D. in Artificial Intelligence, XXXIX cycle, course on Health and 
Life Sciences, organized by Università Campus Bio-Medico di Roma. This work was partially founded by: (i) PNRR – DM 117/2023; (ii) 
Eustema S.p.A.; (iii) PNRR MUR, Italy project PE0000013 - FAIR; (iv) 
Project ECS 0000024 Rome Technopole, CUP C83C22000510001, NRP 
Mission 4 Component 2 Investment 1.5, Funded by the European Union 
- NextGenerationEU. Data collection and sharing for ADNI was funded 
by the Alzheimer’s Disease Neuroimaging Initiative (ADNI) (National 
Institutes of Health, Italy Grant U01 AG024904) and DOD ADNI, Italy 
(Department of Defense award number W81XWH-12-2-0012).

**Passage 9:**

> -
formance, only one classifier comes close to IMBALMED’s performance, 
surpassing it by about 2 percentage points. Table A.11
Primary Dataset: Detailed list of selected features by modality and task. Modality Diagnostic Tasks Early Detection Tasks  
 Assessment FAQ_bl, FAQSOURCE, FAQFINAN, FAQFORM, FAQSHOP, 
FAQGAME,
FAQBEVG, FAQMEAL, FAQEVENT, FAQTV, FAQREM, FAQTRAVL, 
HMONSET, HMSTEPWS, HMSOMATC, HMEMOTIO, HMHYPERT, 
HMSTROKE, HMNEURSM, HMNEURSG, HMSCORE, GDSATIS, 
GDDROP, GDEMPTY, GDBORED, GDSPIRIT, GDAFRAID, GDHAPPY, 
GDHELP, GDHOME, GDMEMORY, GDALIVE, GDWORTH, 
GDENERGY, 
GDHOPE, GDBETTER, GDTOTAL
FAQ_bl, FAQSOURCE, FAQFINAN, FAQFORM, FAQSHOP, 
FAQGAME,
FAQBEVG, FAQMEAL, FAQEVENT, FAQTV, FAQREM, FAQTRAVL, 
HMONSET, HMSTEPWS, HMSOMATC, HMEMOTIO, HMHYPERT, 
HMSTROKE, HMNEURSM, HMNEURSG, HMSCORE, GDSATIS, 
GDDROP, 
GDEMPTY, GDBORED, GDSPIRIT, GDAFRAID, GDHAPPY, GDHELP, 
GDHOME, GDMEMORY, GDALIVE, GDWORTH, GDENERGY, 
GDHOPE, 
GDBETTER, GDTOTAL, PHC_Diagnosis, PHC_MEM, PHC_EXF, 
PHC_LAN, 
WORD1, WORD2, WORD3, MMWATCH, MMPENCIL, MMREPEAT, 
MMHAND, MMFOLD, MMONFLR, MMREAD, MMWRITE, 
MMDRAW, MMSCORE, CLOCKCIRC, CLOCKSYM, CLOCKNUM, 
CLOCKHAND, CLOCKTIME, CLOCKSCOR, COPYCIRC, COPYSYM, 
COPYNUM, COPYHAND, COPYTIME, COPYSCOR, AVTOT1, 
AVERR1, 
AVTOT2, AVERR2, AVTOT3, AVERR3, AVTOT4, AVERR4, AVTOT5, 
AVERR5, AVTOT6, AVERR6, AVTOTB, AVERRB, CATANIMSC, 
CATANPERS, CATANINTR, TRAASCOR, TRAAERRCOM, 
TRAAERROM, 
TRABSCOR, TRABERRCOM, TRABERROM, AVDEL30MIN, 
AVDELERR1, 
AVDELTOT, AVDELERR2, ADNI_MEM, ADNI_EF, ADNI_LAN, 
ADNI_VS, ADNI_EF2, FAQ_bl.1, MMSE_bl, CDRSB_bl, 
RAVLT_immediate_bl, 
RAVLT_learning_bl, RAVLT_forgetting_bl, RAVLT_perc_forgetting_bl, 
LDELTOTAL_BL, TRABSCOR_bl, mPACCdigit_bl, mPACCtrailsB_bl, 
DX_bl
 
 Biospecimen APOE4 APOE4, TAU_ADNIMERGE, PTAU_ADNIMERGE, DX_bl  
 Image Analysis FDG_bl, FDG, Ventricles_bl, Hippocampus_bl, WholeBrain_bl,
Entorhinal_bl, Fusiform_bl, MidTemp_bl, ICV_bl
FDG_bl, FDG, Ventricles_bl, Hippocampus_bl, WholeBrain_bl,
Entorhinal_bl, Fusiform_bl, MidTemp_bl, ICV_bl, DX_bl
 
 Subject Characteristics AGE, PTGENDER, PTEDUCAT, PTETHCAT, PTRACCAT, PTMARRY AGE, PTGENDER, PTEDUCAT, PTETHCAT, PTRACCAT, PTMARRY, 
DX_bl
 
Table A.12
External Validation Dataset: Detailed list of selected features by modality and task.

**Passage 10:**

> 1 (2004–2010), GO (2009–2011), 2 (2011–2016), 
3 (2016–2022), and 4 (2022-present). For this study, we used data 
Computerized Medical Imaging and Graphics 123 (2025) 102529 
3 
A. Francesconi et al. Table 1
Summary of selected ADNI data modalities measured at baseline, including the number of features and percentage of missing data for diagnostic 
and early detection tasks. Modality # of features % of missing data
 Diagnostic tasks Early detection tasks Diagnostic tasks Early detection tasks 
 Assessment 37 110 31.06 30.54  
 Biospecimen 1 4 4.48 16.82  
 ImageAnalysis 9 10 15.34 11.29  
 SubjectCharacteristics 6 7 1.22 0.18  
Fig. 1. Overview of selected data modalities from the ADNI dataset. Each modality is depicted in a labeled box, accompanied by an icon representing the data type and specific 
tests included in the modality.

**Passage 11:**

> State Examination. The Biospecimen modality includes CSF measurements (e.g., amyloid-
beta, tau, phosphorylated tau), ApoE genotyping, and laboratory data 
(e.g., blood, urine, and chemistry panels). Genetic data like Genome-
Wide Association Studies and Whole Genome Sequencing were ex-
cluded due to format inconsistencies with our tabular data needs. Image analysis, derived from MRI and PET scans, provides structural 
and functional brain data, including key neuroimaging biomarkers 
like hippocampal volume, entorhinal cortical thickness, and glucose 
metabolism in specific brain regions. These neuroimaging biomarkers 
are critical for understanding the structural and metabolic changes 
in the brain associated with AD.

**Passage 12:**

> ly disease stages; ADNI 2 built on this 
by refining biomarkers as predictors of cognitive decline and outcome 
measures; and ADNI 3 focused on using functional imaging techniques 
in clinical trials. We utilized four data modalities from the ADNI dataset collected 
at the start of the recruitment, referred to as the baseline: Assessment, 
Biospecimen, Image analysis, and Subject Characteristics. A visual rep-
resentation of these selected modalities is shown in Fig. 1, while 
Table  1 provides a summary of the number of features and the per-
centage of missing data for each modality. Furthermore, a detailed 
list of selected features for each modality and task is provided in 
Table  A.11 in Appendix  A.

**Passage 13:**

> his figure legend, the reader is referred 
to the web version of this article.)
Data availability
The authors do not have permission to share data. References
Aguiar, G., Krawczyk, B., Cano, A., 2023. A survey on learning from imbalanced 
data streams: taxonomy, challenges, empirical study, and reproducible experimental 
framework. Mach. Learn. 1–79. Alhazmi, H.A., Albratty, M., 2022. An update on the novel and approved drugs for 
Alzheimer disease. Saudi Pharm. J. Alzheimer’s Association, 2019. 2019 Alzheimer’s disease facts and figures. Alzheimer’ 
s & Dement. 15 (3), 321–387. Anon, 2024. Alzheimer’s Disease Neuroimaging Initiative: ADNI. URL https://adni.loni.
usc.edu. Arcuri, A., Fraser, G., 2013. Parameter tuning or default values? An empiri-
cal investigation in search-based software engineering. Empir. Softw. Eng. 18, 
594–623. Bifet, A., Gavalda, R., 2007.

**Passage 14:**

> f 
IMBALMED’s effectiveness and consistency, we also measured the tie 
rate and loss rate, indicating the percentage of times that our method 
was equal to or worse than the competitors, respectively. As mentioned in Section 2, there are three related studies addressing 
imbalance and multimodal learning on the ADNI dataset (Sun et al., 
2021; Velazquez and Lee, 2022; Brand et al., 2020). Although they 
could be valid benchmarks to assess our approach, these works were 
excluded from our comparison due to insufficient details for a fair 
experiment reproduction. It is also worth noting that we could not 
validate the proposed approach on external datasets since the litera-
ture does not provide publicly available datasets that comply with all 
modalities selected in this study. 6.

**Passage 15:**

> acquisition, Conceptualization. Rosa Sicilia: Writing – re-
view & editing, Visualization, Validation, Supervision, Software, Project 
administration, Methodology, Formal analysis, Conceptualization. Va-
lerio Guarrasi: Writing – review & editing, Writing – original draft, Vi-
sualization, Validation, Supervision, Software, Project administration, 
Methodology, Formal analysis, Conceptualization. Declaration of competing interest
The authors declare that they have no known competing finan-
cial interests or personal relationships that could have appeared to 
influence the work reported in this paper. Acknowledgments
Arianna Francesconi is a Ph.D. student enrolled in the National 
Ph.D. in Artificial Intelligence, XXXIX cycle, course on Health and 
Life Sciences, organized by Università Campus Bio-Medico di Roma.

**Passage 16:**

> 2 shows the distribution of patients across different tasks 
and time points, highlighting the patient classification at baseline and 
subsequent classifications relevant to the early detection tasks. For 
these tasks, baseline groups included CN, EMCI, and LMCI classes, 
whereas patients diagnosed with AD at baseline were excluded from 
the early detection analysis due to their non-conversion status. 4. Methods
This section details the stages of our method, IMBALMED, also de-
picted in Fig. 2 distinguishing between the training and testing stages. For notation, we will use the following conventions: bold lowercase 
letters for vectors, italics uppercase letters for sets, uppercase letters 
for matrices, and lowercase letters for scalars. In the training phase 
(Train block in Fig.

**Passage 17:**

> Subject Characteristics AGE, PTGENDER, PTEDUCAT, PTETHCAT, PTRACCAT, PTMARRY AGE, PTGENDER, PTEDUCAT, PTETHCAT, PTRACCAT, PTMARRY  
Computerized Medical Imaging and Graphics 123 (2025) 102529 
13 
A. Francesconi et al. Table B.13
Performance comparison of unimodal modalities for various tasks. The table shows the effectiveness of different modalities in diagnostic and early detection tasks, including 
performance differences in binary and ternary classification tasks and across different time points.

**Passage 18:**

> Overview of selected data modalities from the ADNI dataset. Each modality is depicted in a labeled box, accompanied by an icon representing the data type and specific 
tests included in the modality. Arrows indicate the flow of data from the ADNI database to its integration into our final dataset. For notation, see Section 4.1.
from the first four phases of ADNI, as the most recent phase (ADNI 
4) lacked key data modalities necessary for our analysis at the time of 
data acquisition (October 2023). Each phase is characterized by specific 
goals: ADNI 1 aimed to develop biomarkers for clinical trials; ADNI GO 
investigated biomarkers in early disease stages; ADNI 2 built on this 
by refining biomarkers as predictors of cognitive decline and outcome 
measures; and ADNI 3 focused on using functional imaging techniques 
in clinical trials.

**Passage 19:**

> shows the effectiveness of different modalities in diagnostic and early detection tasks, including 
performance differences in binary and ternary classification tasks and across different time points. Modality Binary Diagnostic Ternary Diagnostic 12-month Early detection 24-month Early detection 36-month Early detection 48-month Early detection 
 Assessment 95.42 ± 0.72 71.90 ± 2.40 78.50 ± 3.33 83.71 ± 2.25 81.58 ± 1.61 84.78 ± 3.17  
 Biospecimen 66.85 ± 4.69 25.98 ± 9.30 71.21 ± 1.42 78.90 ± 1.19 75.15 ± 1.98 81.41 ± 1.25  
 Image Analysis 85.52 ± 1.29 53.35 ± 2.19 74.77 ± 2.01 81.82 ± 1.11 78.92 ± 1.75 83.14 ± 1.06  
 Subject Characteristics 59.40 ± 3.47 38.00 ± 5.50 69.41 ± 1.82 78.01 ± 2.31 74.64 ± 2.34 78.65 ± 3.97  
Fig. C.4. Panels (a), (b) and (c) represent the binary, ternary diagnostic, and 12-month early detection tasks, respectively.

**Passage 20:**

> sed for AD diagnosis are: MRI, 
PET, CSF, genetic information, and demographic information (Weiner 
Computerized Medical Imaging and Graphics 123 (2025) 102529 
2 
A. Francesconi et al.
et al., 2017). Whilst unimodal approaches have significantly advanced 
our knowledge of AD, it is increasingly recognized that a multimodal 
approach, which integrates multiple modalities, is essential for cap-
turing the full complexity of the disease (Di Teodoro et al., 2025; 
Guarrasi et al., 2024a,b; Guarrasi and Soda, 2023; Venugopalan et al., 
2021; Caruso et al., 2022; Tortora et al., 2023). This method, denoted 
as multimodal fusion, has been shown to surpass the performance of 
unimodal models in detecting early cognitive impairment and predict-
ing AD conversion (Venugopalan et al., 2021). Multimodal fusion can 
occur at various levels, including late, intermediate, and early fusion.

**Passage 21:**

> n
To evaluate the generalizability of our proposed approach to real-
world scenarios, we conducted an external validation experiment using 
data from the most recent phase of the ADNI dataset, ADNI 4. External 
validation was conducted at the conclusion of the primary experiments, 
approximately eighteen months after the acquisition of data for the 
primary dataset, by which time the ADNI 4 data had become available. This delay allowed us to leverage the most recent ADNI phase to 
evaluate the generalizability of our approach in real-world scenarios. It is important to note that no datasets other than ADNI were used, as, 
to the best of our knowledge, no other comprehensive datasets with 
this type of feature set and characterization of AD are available.

**Passage 22:**

> al validation data fusion performance: top-performing classifier (“Best G-mean” 
of the “Best Classifier”) and average performance across classifiers (“Average G-mean”) 
based on G-mean for each task. Task Best G-mean Best Classifier Average G-mean 
 Binary diagnostic 83.04 ± 3.50 GB 77.62 ± 4.28  
 Ternary diagnostic 49.90 ± 5.83 ET 43.21 ± 5.40  
 12-month early detection 96.88 ± 0.59 k-NN 83.71 ± 16.85  
Image Analysis modalities were excluded due to the absence of the
ADNIMERGE study file, which is only available for ADNI 1, GO, 2, and 
3. Table  8 provides a summary of the selected modalities for external 
validation, detailing the number of features per task and the percentage 
of missing data. Furthermore, a detailed list of selected features for each 
modality and task is provided in Table  A.12 in Appendix  A.

**Passage 23:**

> ilek, K., Truhlarova, Z., Zemek, F., Kuca, K., 2020. Anticipated Social and 
Healthcare Economic Burden of People with Alzheimer’s Disease in Two Selected 
Regions of the Czech Republic. Healthcare 8. Mishra, S., Khare, D., 2014. On comparative performance of multiple imputation 
methods for moderate to large proportions of missing data in clinical trials: a 
simulation study. J Med Stat Inf. 2 (1), 9. Mogensen, K., Guarrasi, V., Larsson, J., Hansson, W., Wåhlin, A., Koskinen, L.-O., 
Malm, J., Eklund, A., Soda, P., Qvarlander, S., 2025. An optimized ensemble 
search approach for classification of higher-level gait disorder using brain magnetic 
resonance images. Comput. Biol. Med. 184, 109457. Namboori, P.K., Vineeth, K., Rohith, V., Hassan, I., Sekhar, L., Sekhar, A., Nidheesh, M., 
2011. The ApoE gene of Alzheimer’s disease (AD). Funct. Integr. Genom. 11, 
519–522.

**Passage 24:**

> . For the diagnostic tasks, we use 𝑚 = 4  data modalities (Section 4.1), 
excluding neuropsychological test scores to avoid bias, as AD diagnosis 
often relies on such tests (Weller and Budson, 2018). For the early 
detection tasks, baseline neuropsychological test scores are included to 
assess treatment necessity. To address data imbalance, we apply the IMBALMED methodol-
ogy described in Section 4.1, setting the minimum representativeness 
number of samples to 𝑟 = 0 .1 for the binary tasks and 𝑟 = 0 .11 for 
the ternary task. These parameters were selected to ensure maximum 
diversity among the subsets, guaranteeing equal class representation, 
with 𝐛𝐢𝟓 = [0 .5, 0.5] for the binary tasks and 𝐛𝐢𝟏𝟔 = [0 .33, 0.33, 0.34] for 
the ternary task (see Section 4.1 for the notation). 5.1.

</details>

---

## Classification Study of Alzheimer-s Disease Based on Self-Attention Mechanism and DTI Imaging Using GCN
_File: `Classification Study of Alzheimer-s Disease Based on Self-Attention Mechanism and DTI Imaging Using GCN.pdf`_

1. **Yes**, diffusion MRI (DTI) was used in this paper. The paper explicitly mentions "DTI data processing" and references DTI as a key technique for analyzing white matter integrity in Alzheimer’s disease (AD).

2. **Processing steps applied to diffusion images** (in order):  
   - Convert downloaded ADNI data to `nii.gz` format using FSL.  
   - Perform skull stripping and eddy current correction.  
   - Calculate DTI parameters (FA and MD) via FSL.  
   - Use PANDA’s deterministic fiber tracking to construct white matter fiber bundles.  
   - Segment the brain into a 90 × 90 network using the automated anatomical labeling (AAL) brain atlas.  

3. **Software/tools explicitly named**:  
   - **FSL** (FMRIB Software Library).  
   - **PANDA** (Pipeline for Analyzing Brain Diffusion Images), a Linux-based software running within MATLAB.  

4. **Acquisition/processing parameters reported**:  
   - **DTI parameters**: Fractional anisotropy (FA) and mean diffusivity (MD) are explicitly calculated.  
   - **Other parameters**: No explicit mention of b-values, number of diffusion directions, voxel size, or thresholds.  

5. **Exact sentences from excerpts describing processing**:  
   - *"The preprocessing workflow begins with converting the downloaded data from ADNI into the nii.gz format using FSL. Subsequently, skull stripping and eddy current correction are performed, and then DTI parameters such as FA and MD are calculated via FSL."*  
   - *"Next, PANDA’s deterministic fiber tracking technique was employed to construct white matter fiber bundles based on the white matter trajectories."*  
   - *"Finally, the automated anatomical labeling (AAL) brain atlas is utilized to segment the brain into a 90 × 90 brain network."*  

6. **Processing description completeness**:  
   The description is **incomplete**. While the steps (data conversion, skull stripping, eddy correction, FA/MD calculation, fiber tracking, and AAL segmentation) are explicitly stated, critical parameters like **b-values**, **number of diffusion directions**, **voxel size**, or **thresholds** are not reported in the excerpts.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> sion imAges) software. PANDA is a Linux-based
software that is running within MA TLAB. The preprocessing
workflow begins with converting the downloaded data from
ADNI into the nii.gz format using FSL. Subsequently, skull
stripping and eddy current correction are performed, and then
DTI parameters such as FA and MD are calculated via FSL. Next, PANDA ’s deterministic fiber tracking technique was
employed to construct white matter fiber bundles based on the
white matter trajectories. Finally, the automated anatomical
labeling (AAL) brain atlas is utilized to segment the brain into
a 90 × 90 brain network. Each brain region can be considered
a node in the network, with features encompassing the
number of voxels in each brain region.

**Passage 2:**

> experiments use two labels: AD
and normal control (NC). The DTI data processing will be
introduced in the first part of this section, followed by a
description of the GCN framework in the second part. The
results of the experiments will be presented in the third part. Finally, we summarized our investigation and provided the
expectations for future research. A. EXPERIMENTAL DATA
The data applied in this study is sourced from the ADNI
database (https://adni.loni.usc.edu/), from which we selected
70 AD patients and 70 NC individuals. The preprocessing
experiments were conducted using FSL (FMRIB Software
Library) and the FSL-based PANDA (Pipeline for Analyzing
braiN Diffusion imAges) software. PANDA is a Linux-based
software that is running within MA TLAB. The preprocessing
workflow begins with converting the downloaded data from
ADNI into the nii.gz format using FSL.

**Passage 3:**

> nd H. Chabriat, ‘‘Diffusion tensor imaging: Concepts and applications,’’
J. Magn. Reson. Imag., vol. 13, no. 4, pp. 534–546, Apr. 2001.
[4] C. Pierpaoli, P . Jezzard, P . J. Basser, A. Barnett, and G. Di Chiro,
‘‘Diffusion tensor MR imaging of the human brain,’’ Radiology, vol. 201,
no. 3, pp. 637–648, Dec. 1996.
[5] Y . Zhang, N. Schuff, G.-H. Jahng, W. Bayne, S. Mori, L. Schad, S. Mueller,
A.-T. Du, J. H. Kramer, K. Y affe, H. Chui, W. J. Jagust, B. L. Miller,
and M. W. Weiner, ‘‘Diffusion tensor imaging of cingulum fibers in mild
cognitive impairment and Alzheimer disease,’’ Neurology, vol. 68, no. 1,
pp. 13–19, Jan. 2007.
[6] M. Bozzali, S. E. MacPherson, M. Cercignani, W. R. Crum, T. Shallice,
and J. Rees, ‘‘White matter integrity assessed by diffusion tensor
tractography in a patient with a large tumor mass but minimal clinical and
neuropsychological deficits,’’ Funct. Neurol., vol.

**Passage 4:**

> Received 16 January 2024, accepted 30 January 2024, date of publication 8 February 2024, date of current version 20 February 2024. Digital Object Identifier 10.1 109/ACCESS.2024.3364545
Classification Study of Alzheimer’s Disease Based
on Self-Attention Mechanism and
DTI Imaging Using GCN
YILIN SANG
 AND WAN LI
School of Computing Science and Engineering, Beijing Technology and Business University, Beijing 100048, China
Corresponding author: Wan Li (wanli@btbu.edu.cn)
ABSTRACT Alzheimer’s disease (AD) is a neurodegenerative disorder. Diffusion tensor imaging (DTI)
provides information about the integrity of white matter fiber bundles that are related to the neuropathological
mechanisms, and it is one of the commonly used techniques in AD research. In this study, we first divided
each subject’s brain into 90 regions based on the automated anatomical labeling (AAL) brain atlas.

**Passage 5:**

> His research interests include medical
image classification and deep learning. WAN LI received the B.S. degree from Zhengzhou
University and the Ph.D. degree from the Beijing
University of Technology. She is currently an
Assistant Professor with Beijing Technology and
Business University. Her research interests include
medical image processing and deep learning. VOLUME 12, 2024 24395

**Passage 6:**

> ng steps. This approach is more conducive to practical
implementation in the future. Traditional machine learning
algorithms consume significant time for training when
dealing with large brain images. However, by processing
them into brain networks, not only can a substantial amount
of time be saved, but there is also no need for additional
feature extraction. DTI brain networks can be directly trained. This time-saving aspect becomes particularly beneficial in
practical use in the future.GCN is a relatively new network
with plenty of space for development. Therefore, future
research on AD classification using DTI images, functional
brain networks derived from fMRI, and the fusion of these
two networks should pay more attention to this aspect of
utilizing GCN. REFERENCES
[1] A. Collie and P .

**Passage 7:**

> lary tangles (intracellular aggregates
of hyperphosphorylated tau proteins), which can be revealed
as decreased FA and increased MD in the cingulate, corpus
callosum, and hippocampus regions [5], [6]. Graph neural network (GNN) is a general type of graph
neural network that can handle various types of graph data,
including directed, undirected, and weighted graphs [7]. VOLUME 12, 2024

 2024 The Authors. This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 License. For more information, see https://creativecommons.org/licenses/by-nc-nd/4.0/ 24387
Y. Sang, W.

**Passage 8:**

> vised learning with application to brain networks anal-
ysis,’’ IEEE J. Biomed. Health Informat., vol. 27, no. 8, pp. 4154–4165,
Aug. 2023.
[53] X. Ouyang, K. Chen, L. Y ao, X. Wu, J. Zhang, K. Li, Z. Jin, and X. Guo,
‘‘Independent component analysis-based identification of covariance
patterns of microstructural white matter damage in Alzheimer’s disease,’’
PLoS One, vol. 10, no. 3, Mar. 2015, Art. no. e0119714.
[54] C. D. Mayo, E. L. Mazerolle, L. Ritchie, J. D. Fisk, and J. R. Gawryluk,
‘‘Longitudinal changes in microstructural white matter metrics in
Alzheimer’s disease,’’NeuroImage, Clin., vol. 13, pp. 330–338, Jan. 2017.
[55] T. Kipf, ‘‘Deep learning with graph-structured representations,’’ Ph.D. dis-
sertation, Informat. Inst., University of Amsterdam, Amsterdam, The
Netherlands, 2020.
[56] H. Kong, J. Pan, Y . Shen, and S.

**Passage 9:**

> fication using DTI images, functional
brain networks derived from fMRI, and the fusion of these
two networks should pay more attention to this aspect of
utilizing GCN. REFERENCES
[1] A. Collie and P . Maruff, ‘‘The neuropsychology of preclinical Alzheimer’s
disease and mild cognitive impairment,’’ Neurosci. Biobehavioral Rev.,
vol. 24, no. 3, pp. 365–374, May 2000.
[2] S. Gauthier, P . Rosa-Neto, J. A. Morais, and C. Webster, ‘‘World Alzheimer
report 2021: Journey through the diagnosis of dementia,’’ Alzheimer’s
Disease Int., London, U.K., Tech. Rep., 2021.
[3] D. Le Bihan, J. Mangin, C. Poupon, C. A. Clark, S. Pappata, N. Molko,
and H. Chabriat, ‘‘Diffusion tensor imaging: Concepts and applications,’’
J. Magn. Reson. Imag., vol. 13, no. 4, pp. 534–546, Apr. 2001.
[4] C. Pierpaoli, P . Jezzard, P . J. Basser, A. Barnett, and G.

**Passage 10:**

> ter. It can identify abnormal diffusion patterns in
various neurological disorders and provide information about
the integrity of white matter fiber tracts related to neurobio-
logical mechanisms [3]. So far, DTI is the only neuroimaging
The associate editor coordinating the review of this manuscript and
approving it for publication was Roberta Palmeri
.
technique that can describe white matter fiber pathways and
is highly sensitive to microstructural white matter damage
within fiber bundles. Therefore, DTI is typically used to
specify anatomical connectivity impairments that cannot be
detected by structural MRI (sMRI). The two most frequently
used features to characterize white matter integrity are
fractional anisotropy (FA) and mean diffusivity (MD) [4].

**Passage 11:**

> mages of three modalities for classification. 3D sMRI images were input into the multi-channel ResNet
network model, while the brain networks constructed by DTI
and fMRI were input into the GCN model. Finally, multi-
channel ResNet and GCN were combined for multi-modality
classification to obtain pleasing results [21]. Other than the limited applications of GCN in AD-related
research, the currently favored AD-classification approaches
utilizing DTI images are briefly introduced as follows. GCN-excluded classification studies can be organized
into three categories: voxel-based, brain region-based,
and network-based classification studies. The research on
voxel-based classification is to select the most representative
AD voxels from the whole brain, calculate their DTI param-
eter values, such as FA and MD, and then classify them by
various classifiers [22], [23], [24], [25].

**Passage 12:**

> in atlas is utilized to segment the brain into
a 90 × 90 brain network. Each brain region can be considered
a node in the network, with features encompassing the
number of voxels in each brain region. After preprocessing,
three structural brain networks are obtained: (1) the FA brain
network, constructed based on the average FA values between
each brain region according to the brain atlas; (2) the FN
brain network, constructed based on the number of fibers
between each brain region according to the brain atlas; (3) the
LEN brain network, constructed based on the average fiber
length between each brain subdivision according to the brain
atlas. The node features include (1) ROIS (ROISurfaceSize),
denoting the number of voxels traversed by fibers in each
brain region; (2) ROIV (ROIV oxelSize), representing the
number of voxels in each brain region. B.

**Passage 13:**

> tention Mechanism and DTI Imaging Using GCN
TABLE 1. Table 1. Accuracy of different matrix and node feature
combinations with different k values. TABLE 2. Comparison of accuracy with other literature. This study considers the combination of different adja-
cency matrices representing brain networks and various node
features and tests the influence of different k values on
accuracy. The accuracy graph indicates that using the FA
brain network as network features and ROIS as node features
yields the best classification results. Moreover, using ROIS
as node features generally outperforms using ROIV as node
features for classification. By analyzing the node feature data,
this result may be because ROIS represents the number of
voxels with fibers passing through them.

**Passage 14:**

> sing GCN
across connections of different distances, helping to improve
classification performance. Therefore, we applied the GCN on the brain networks
abstracted from the DTI image for classification. Notably,
we endeavored to add the self-attention mechanism to the
original GCN structure in this study to realize better AD
classification. III. EXPERIMENT
Our study utilizes the white matter features of DTI images
and employs GCN with the self-attention mechanism for
classification. The network takes structural brain networks
based on DTI as input to generate cognitive state category
labels and uses these labels as output to obtain the final
classification accuracy. Our experiments use two labels: AD
and normal control (NC). The DTI data processing will be
introduced in the first part of this section, followed by a
description of the GCN framework in the second part.

**Passage 15:**

> 1
Y. Sang, W. Li: Classification Study of AD Based on Self-Attention Mechanism and DTI Imaging Using GCN
FIGURE 8. Accuracy, sensitivity and specificity using different feature combinations. FIGURE 9. The accuracy of different feature combinations combined with different k values was compared with
that of SVM. ROIS and ROIV . The connections between each brain region
are abstracted as relationships between nodes and edges in
the network. ROIS and ROIV serve as node features, and
each node’s graph membership and graph labels are used as
inputs to the GCN model. Next, the model is designed with
three convolutional layers. In the pooling layers following
each convolutional layer, the self-attention mechanism is
incorporated to filter the nodes. By removing irrelevant
nodes from the entire brain network, the accuracy of the
classification is improved. C.

**Passage 16:**

> ter regions and its image clarity
limitations, relatively few studies utilize DTI images for
classification research using CNN models. Therefore, our
study directs its attention to DTI brain networks. The self-attention mechanism is involved because specific
brain regions are essential in AD classification research,
and others are irrelevant. After abstracting DTI images into
brain networks, the importance of each brain region can be
determined based on its degree within the network. The self-
attention mechanism can eliminate irrelevant nodes during
the training process, equivalent to removing brain regions
unrelated to AD in the brain network. Additionally, it can
rank each node based on its self-attention score, allowing
for integration with AD-related brain regions and improving
classification accuracy.

**Passage 17:**

> and Q. Y e, ‘‘Intravoxel
incoherent motion diffusion-weighted imaging in the characterization of
Alzheimer’s disease,’’ Brain Imag. Behav., vol. 16, no. 2, pp. 617–626,
Apr. 2022.
[25] A. De and A. S. Chowdhury, ‘‘DTI based Alzheimer’s disease classifica-
tion with rank modulated fusion of CNNs and random forest,’’ Expert Syst. Appl., vol. 169, May 2021, Art. no. 114338.
[26] A. Demirhan, T. M. Nir, A. Zavaliangos-Petropulu, C. R. Jack,
M. W. Weiner, M. A. Bernstein, P . M. Thompson, and N. Jahanshad,
‘‘Feature selection improves the accuracy of classifying Alzheimer disease
using diffusion tensor images,’’ in Proc. IEEE 12th Int. Symp. Biomed. Imag. (ISBI), Brooklyn, NY , USA, Apr. 2015, pp. 126–130.
[27] T. Maggipinto, R. Bellotti, N. Amoroso, D. Diacono, G. Donvito,
E. Lella, A. Monaco, M. A. Scelsi, and S. Tangaro, ‘‘DTI measurements
for Alzheimer’s classification,’’ Phys. Med.

**Passage 18:**

> ted based on DTI images. The purpose is
to investigate the classification performance of the unique
white matter network derived from DTI images when
the self-attention mechanism is included with GCN. The
advantage lies in avoiding complex preprocessing and feature
extraction steps. Instead, only the DTI brain network is
input to GCN to obtain classification accuracy. Most studies
focus on innovative feature extraction methods in the current
research landscape. They extract features from voxels or
brain regions using various feature extraction techniques
and then employ traditional classifiers such as SVM for
classification. However, due to the primary role of DTI
images in AD’s white matter regions and its image clarity
limitations, relatively few studies utilize DTI images for
classification research using CNN models. Therefore, our
study directs its attention to DTI brain networks.

**Passage 19:**

> llice,
and J. Rees, ‘‘White matter integrity assessed by diffusion tensor
tractography in a patient with a large tumor mass but minimal clinical and
neuropsychological deficits,’’ Funct. Neurol., vol. 27, no. 4, pp. 239–246,
Oct. 2012.
[7] F. Scarselli, A. C. Tsoi, M. Gori, and M. Hagenbuchner, ‘‘Graphical-based
learning environments for pattern recognition,’’ in Structural, Syntactic,
and Statistical Pattern Recognition (Lecture Notes in Computer Science),
Aug. 2004, pp. 42–56.
[8] T. Kipf and M. Welling, ‘‘Semi-supervised classification with graph
convolutional networks,’’ 2016, arXiv:1609.02907.
[9] T.-A. Song, S. R. Chowdhury, F. Y ang, H. Jacobs, G. E. Fakhri, Q. Li,
K. Johnson, and J. Dutta, ‘‘Graph convolutional neural networks for
Alzheimer’s disease classification,’’ inProc. IEEE 16th Int. Symp. Biomed. Imag. (ISBI), V enice, Italy, Apr. 2019, pp. 414–417.
[10] H. Kong and S.

**Passage 20:**

> eryday lives of patients and
their families [1]. In 2021, over 55 million people worldwide
were diagnosed with this disease, and the number of AD
patients is estimated to reach 78 million by 2030 [2]. With the development of neuroimaging techniques, various
neuroimaging modalities have shown potential for improving
the diagnosis of AD from different perspectives. Diffusion tensor imaging (DTI) is a non-invasive magnetic
resonance imaging (MRI) technique that captures water
molecules’ degree of anisotropic diffusion along axons in the
white matter. It can identify abnormal diffusion patterns in
various neurological disorders and provide information about
the integrity of white matter fiber tracts related to neurobio-
logical mechanisms [3].

**Passage 21:**

> ent: Automated fiber
quantification,’’ in Proc. IEEE 16th Int. Symp. Biomed. Imag. (ISBI),
V enice, Italy, Apr. 2019, pp. 117–121.
[32] D. B. Stone, S. G. Ryman, A. P . Hartman, C. J. Wertz, and A. A. V akhtin,
‘‘Specific white matter tracts and diffusion properties predict conversion
from mild cognitive impairment to Alzheimer’s disease,’’ Frontiers Aging
Neurosci., vol. 13, 2021, Art. no. 711579.
[33] C. Y e, S. Mori, P . Chan, and T. Ma, ‘‘Connectome-wide network analysis
of white matter connectivity in Alzheimer’s disease,’’ NeuroImage, Clin.,
vol. 22, Feb. 2019, Art. no. 101690.
[34] J. P . J. Savarraj, R. Kitagawa, D. H. Kim, and H. A. Choi, ‘‘White matter
connectivity for early prediction of Alzheimer’s disease,’’ Technol. Health
Care, vol. 30, no. 1, pp. 17–28, Dec. 2021.
[35] F. He, Y . Li, C. Li, J. Zhao, T. Liu, L. Fan, X. Zhang, and J.

**Passage 22:**

> impairments that cannot be
detected by structural MRI (sMRI). The two most frequently
used features to characterize white matter integrity are
fractional anisotropy (FA) and mean diffusivity (MD) [4]. FA
provides information about fiber density, axon diameter, and
myelination, with decreased values indicating a loss of fiber
tract integrity. MD measures the average diffusivity of water
molecules in non-collinear directions, with increased values
indicating increased free diffusion of water molecules and
compromised anisotropy. The main pathological features of
AD include neuritic plaques or amyloid plaques (extracellular
deposits) and neurofibrillary tangles (intracellular aggregates
of hyperphosphorylated tau proteins), which can be revealed
as decreased FA and increased MD in the cingulate, corpus
callosum, and hippocampus regions [5], [6].

**Passage 23:**

> Jan. 2022, Art. no. e08725.
[30] L. Cao, B. R. Schrank, S. Rodriguez, E. G. Benz, T. W. Moulia,
G. T. Rickenbacher, A. C. Gomez, Y . Levites, S. R. Edwards, T. E. Golde,
B. T. Hyman, G. Barnea, and M. W. Albers, ‘‘Aβ alters the connectivity
of olfactory neurons in the absence of amyloid plaques in vivo,’’ Nature
Commun., vol. 3, no. 1, 2012, Art. no. 1009. 24394 VOLUME 12, 2024
Y. Sang, W. Li: Classification Study of AD Based on Self-Attention Mechanism and DTI Imaging Using GCN
[31] X. Dou, H. Y ao, D. Jin, F. Feng, P . Wang, B. Zhou, B. Liu, Z. Y ang,
N. An, X. Zhang, and Y . Liu, ‘‘Characterizing white matter connectivity
in Alzheimer’s disease and mild cognitive impairment: Automated fiber
quantification,’’ in Proc. IEEE 16th Int. Symp. Biomed. Imag. (ISBI),
V enice, Italy, Apr. 2019, pp. 117–121.
[32] D. B. Stone, S. G. Ryman, A. P . Hartman, C. J. Wertz, and A. A.

**Passage 24:**

> imer’s disease
identification,’’Comput. Methods Programs Biomed., vol. 238, Aug. 2023,
Art. no. 107597.
[22] C. Luo, M. Li, R. Qin, H. Chen, L. Huang, D. Y ang, Q. Y e, R. Liu,
Y . Xu, H. Zhao, and F. Bai, ‘‘Long longitudinal tract lesion contributes to
the progression of Alzheimer’s disease,’’ Frontiers Neurol., vol. 11, 2020,
Art. no. 503235.
[23] E. Lella, A. Pazienza, D. Lofù, R. Anglani, and F. Vitulano, ‘‘An
ensemble learning approach based on diffusion tensor imaging measures
for Alzheimer’s disease classification,’’ Electronics, vol. 10, no. 3, p. 249,
Jan. 2021.
[24] N. Xia, Y . Li, Y . Xue, W. Li, Z. Zhang, C. Wen, J. Li, and Q. Y e, ‘‘Intravoxel
incoherent motion diffusion-weighted imaging in the characterization of
Alzheimer’s disease,’’ Brain Imag. Behav., vol. 16, no. 2, pp. 617–626,
Apr. 2022.
[25] A. De and A. S.

</details>

---

## Classification-of-Alzheimer-s-disease-us_2024_Journal-of-King-Saud-Universit
_File: `Classification-of-Alzheimer-s-disease-us_2024_Journal-of-King-Saud-Universit.pdf`_



<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> to implement distinct DL models. 3. Proposed model
The paper describes a unique approach for detecting early on using
binary techniques. The approach is made up of several phases, as
shown in Fig. 1. MRI pictures go through a preprocessing pipeline
in the first data preparation phase, including data resizing, labeling,
normalization, and color modification. In the second phase, training
and testing sets are created from the preprocessed data, which are
utilized to develop and train the proposed DL models. The third phase
is the study of the DL models to suggest DL models include tasks
for automated feature extraction and classification. Additionally, the
study suggests CNNs-without-Aug, CNNs-with-Aug, CNN-LSTM-with-
Aug, CNNs-SVM-with-Aug, and Transfer learning using VGG16-SVM-
with-Aug.

**Passage 2:**

> udes a total of 6400 MRI images classified into four distinct classes:
Mild-Demented, Moderate-Demented, Very-Mild-Demented, and Non-
Demented. Table 1 shows the total number of images in the dataset. For the proposed models, it is binary classification. So, the classes
of data combined into two classes, Demented and Non- demented;
Mild-Demented, Moderate-Demented, and Very-and Mild-Demented,
1 https://www.kaggle.com/datasets/tourist55/alzheimers-dataset-4-class-
of-images.
are combined together as Demented and Non-Demented as it is as in
Table 2. Fig. 12 shows a visualization sample of the data. To maintain
uniformity in terms of size, quality, and color, the photos within the
dataset were subjected to preprocessing procedures, including resizing
and color alteration. Subsequently, a normalization technique was em-
ployed to ensure that all pixels were scaled to a consistent range.

**Passage 3:**

> were subjected to preprocessing procedures, including resizing
and color alteration. Subsequently, a normalization technique was em-
ployed to ensure that all pixels were scaled to a consistent range. The
photos were appropriately labeled, with the designation "0" denoting
Non-Demented and "1" denoting Demented. The dataset underwent
a shuffling process, resulting in a division of 80.00% for training
purposes, including 5120 photos, and 20.00% for testing purposes,
encompassing 1280 images. 4.2. Working environment
The simulation results were generated using a Google collab. A
suite of programming tools, including Python, Keras, Tensorflow, and
Journal of King Saud University - Computer and Information Sciences 36 (2024) 101940
12
S.E. Sorour et al. Fig. 7. CNN-SVM-with-Aug model. Table 1
Total number of images in AD Dataset available in Kaggle.

**Passage 4:**

> n metrics, including accuracy, specificity,
precision, recall, F1-score, and processing time. The study’s methodology encompasses four primary stages. Initially,
an appropriate AD dataset is gathered. The second stage involves
data pre-processing, converting the obtained unstructured data into a
structured format suitable for the classification process. Next, feature
extraction and classification are conducted concurrently employing the
provided DL models, as mentioned in earlier models. The final stage
involves assessing these DL models’ performance based on diverse pre-
established assessment metrics. Based on this evaluation, the DL model
that demonstrates superior performance is recommended for AD early
detection. 1.2. Contributions
The paper presents an early detection approach for AD based on DL
models.

**Passage 5:**

> Journal of King Saud University - Computer and Information Sciences 36 (2024) 101940
Available online 24 January 2024
1319-1578/© 2024 The Author(s). Published by Elsevier B.V. on behalf of King Saud University. This is an open access article under the CC BY-NC-ND license
(http://creativecommons.org/licenses/by-nc-nd/4.0/). Contents lists available at ScienceDirect
Journal of King Saud University - Computer and Information
Sciences
journal homepage: www.sciencedirect.com
Full length article
Classification of Alzheimer’s disease using MRI data based on Deep Learning
Techniques
Shaymaa E. Soroura,b,∗, Amr A. Abd El-Mageedc, Khalied M. Albarraka,
Abdulrahman K. Alnaima, Abeer A.

**Passage 6:**

> ron. In: 2021 Sixth International Con-
ference on Wireless Communications, Signal Processing and Networking. WiSPNET,
IEEE, www, pp. 368–373. Rohini, G., 2021. Everything you need to know about VGG16. Medium Available on-
line: https://medium.com/@mygreatlearning/everything-you-need-to-know-about-
vgg16-7315defb5918. Rolls, E.T., Huang, C.-C., Lin, C.-P., Feng, J., Joliot, M., 2020. Automated anatomical
labelling atlas 3. Neuroimage 206, 116189. Saied, I.M., Arslan, T., Chandran, S., 2021. Classification of Alzheimer’s disease using
RF signals and machine learning. IEEE J. Electromagn. RF Microw. Med. Biol. 6
(1), 77–85. Saini, K., Marriwala, N., 2022. Deep learning-based face mask detecting system: an
initiative against COVID-19. In: Emergent Converging Technologies and Biomedical
Systems: Select Proceedings of ETBS 2021. Springer, oooo, pp. 729–742.

**Passage 7:**

> sease using deep neuro-functional networks
with resting-state fMRI. Electronics 12 (4), 1031. Sharma, S., Guleria, K., 2022. Deep learning models for image classification: comparison
and applications. In: 2022 2nd International Conference on Advance Computing and
Innovative Technologies in Engineering. ICACITE, IEEE, ggg, pp. 1733–1738. Shi, Y., Zeng, W., Deng, J., Nie, W., Zhang, Y., 2020. The identification of Alzheimer’s
disease using functional connectivity between activity voxels in resting-state fMRI
data. IEEE J. Transl. Eng. Health Med. 8, 1–11. Shojaei, S., Abadeh, M.S., Momeni, Z., 2023. An evolutionary explainable deep learning
approach for Alzheimer’s MRI classification. Expert Syst. Appl. 220, 119709. Shukla, A., Tiwari, R., Tiwari, S., 2023. Review on alzheimer disease detection methods:
Automatic pipelines and machine learning techniques. Sci 5 (1), 13.

**Passage 8:**

> y examined of these biomarkers. As a result,
various methods for classifying MRI scans for population screening
have been developed, emphasizing the hippocampus area and other
indicators in the brain. In this investigation, the claim made was sup-
ported in Wang et al. (2020) that exact segmentation of the total brain
volume is not required. Instead, a rough identification of the biomarker
region is sufficient, achieved through brain alignment and atlas-based
selection of the region-of-interest (ROI) (Wang et al., 2020). Following
that, traditional multimedia indexing approaches can be used to the
selected ROI by using feature-based visual signatures produced from
"engineered features" or by deploying state-of-the-art CNNs that have
successfully classified visual and multimedia data.

**Passage 9:**

> matography
Mass Spectrometry (UPLC-MS/MS) for developing DL predictive tools. It involved 177 individuals, including 78 AD patients and 99 cogni-
tively normal (CN) participants, from the ADNI cohort. The research
utilized 150 metabolomic biomarkers, and feature selection was con-
ducted using the Least Absolute Shrinkage and Selection Operator
(LASSO), which identified 21 significant metabolic biomarkers. These
biomarkers were used to construct multilayer feedforward neural net-
works through the H2O DL function, dividing the data into 70.00%
for training and 30.00% for validation. The most effective DL model
featured two layers and 18 neurons, achieving an accuracy of 88.10%,
F1-score of 89.20%, and AUC of 87.30%.

**Passage 10:**

> various imaging modalities such as MRI, tractography (also known as
Diffusion Tensor Imaging or DTI), and Positron Emission Tomography
(PET) are utilized to supplement and enhance the detection of AD. Numerous strategies have been developed to use biomarkers in 3D MRI
images to classify patients’ current states and forecast the progression to
AD (Leela et al., 2023). AD is diagnosed by brain monitoring techniques
such as MRI, Computer Tomography (CT) scans, and PET. MRI is a
powerful tool for detecting disease-related brain structure and function
changes. It is regarded as a valuable and crucial tool for detecting early
indicators of AD. MRI has several benefits because it does not require
any surgical procedures and enables noninvasive and comprehensive
brain imaging.

**Passage 11:**

> a valuable and crucial tool for detecting early
indicators of AD. MRI has several benefits because it does not require
any surgical procedures and enables noninvasive and comprehensive
brain imaging. Its high-resolution imaging capabilities, capacity to cap-
ture structural alterations in the brain, and role in monitoring disease
progression make it an invaluable tool for clinicians, researchers, and
patients (Lakhan et al., 2023). In the last few years, Machine Learning (ML) and DL methods
have been offered, adopted, and implemented for analyzing various
pictures and MRIs. These algorithms have been especially beneficial
in diagnosing health concerns and recognizing early indicators of AD.

**Passage 12:**

> n in the future, recently built
DL models and pre-trained deep architectures may be used. Using DL
algorithms, a few additional issues that affect people and their health
will also be concentrated on. Declaration of competing interest
The authors declare that they have no known competing finan-
cial interests or personal relationships that could have appeared to
influence the work reported in this paper. Acknowledgments
The authors extend their sincere thanks to the Deanship of Sci-
entific Research, Vice Presidency for Graduate Studies and Scientific
Research, King Faisal University, Saudi Arabia for their generous fi-
nancial support, which was crucial for the research project (GRANT
5,608). References
Ahmed, S., Choi, K.Y., Lee, J.J., Kim, B.C., Kwon, G.-R., Lee, K.H., Jung, H.Y., 2019. Ensembles of patch-based classifiers for diagnosis of Alzheimer diseases.

**Passage 13:**

> i. 453, 120812. Yamashita, R., Nishio, M., Do, R.K.G., Togashi, K., 2018. Convolutional neural networks:
an overview and application in radiology. Insights Imaging 9, 611–629. Yang, Z., Liu, Z., 2020. The risk prediction of Alzheimer’s disease based on the deep
learning model of brain 18F-FDG positron emission tomography. Saudi J. Biol. Sci. 27 (2), 659–665. Yu, Y., Si, X., Hu, C., Zhang, J., 2019. A review of recurrent neural networks: LSTM
cells and network architectures. Neural Comput. 31 (7), 1235–1270.

**Passage 14:**

> e prefrontal lobe and
between the prefrontal and parietal lobes are key factors in predicting
AD patients with higher accuracy. This technique shows great promise
for future applications in the field. Also, Bae et al. (2020) utilized MRI
images from a diverse range of individuals regarding race, education
level, age, and gender to create a CNN-based approach for detecting
AD. To ensure accuracy, they drew upon two separate datasets —
one from Seoul National University Bundang Hospital (SNUBH) and
the other from the ADNI dataset. This allowed them to achieve an
average classification accuracy of 88.00%–89.00% and a sensitivity of
85.00%–88.00% using 195 images from each dataset. The estimated
processing time per individual was around 23–24 s. In 2021, Helaly
et al. (2021) explored various techniques for categorizing medical
images and detecting AD.

**Passage 15:**

> iam, M., Aparna, T., Anurenjan, P., Sreeni, K., 2022. Deep learning-based
prediction of Alzheimer’s disease from magnetic resonance images. In: Intelligent
Vision in Healthcare. Springer, pp. 145–151. Sun, J., Gong, Y., Liu, M., Liang, C., Zhao, Y., 2022. A uniform allowance matching
method for point cloud based on the edge extraction under de-shaping center. Alex. Eng. J. 61 (12), 12965–12976. Trivedi, N.K., Anand, A., Lilhore, U.K., Guleria, K., 2022. Deep learning applications
on edge computing. In: Machine Learning for Edge Computing, first ed. CRC Press,
pp. 143–168. Tun, N.L., Gavrilov, A., Tun, N.M., Aung, H., et al., 2021. Remote sensing data
classification using a hybrid pre-trained VGG16 CNN-SVM classifier. In: 2021 IEEE
Conference of Russian Young Researchers in Electrical and Electronic Engineering. ElConRus, IEEE, pp. 2171–2175. Tuvshinjargal, B., Hwang, H., 2022.

**Passage 16:**

> RNN for inter-slice feature extraction. This method achieved high clas-
sification performance, as evidenced by impressive AUC values in
differentiating AD from normal cognition (NC) and MCI from NC. A novel contrastive-based learning strategy was applied to overcome
challenges in PET image analysis. This method amplified sections of 3D
Journal of King Saud University - Computer and Information Sciences 36 (2024) 101940
4
S.E. Sorour et al. PET images and used contrastive loss to enhance feature differentiation
between classes and reduce intra-class variations. It involved a dual-
layer convolutional module for improved visual domain recognition. Also, in the research conducted by Pan et al. (2020a,b), they have
developed the application of DNNs in FDG-PET imaging for early AD
detection.

**Passage 17:**

> ation criteria. The duration allocated to training and tests was also
documented. The evaluation of the proposed model’s performance was
conducted using specified datasets, as outlined in Section 4.1. The
details about workplace characteristics are outlined in Section 4.3,
whereas in Section 4.4, a comparison analysis is presented. Journal of King Saud University - Computer and Information Sciences 36 (2024) 101940
11
S.E. Sorour et al. Fig. 6. CNN-LSTM-model. 4.1. Description of the dataset
To evaluate the proposed models in comparison to state-of-the-
art models, data obtained from the MRI scans of the ADNI 1, 1 were
employed. The dataset utilized in this research, sourced from Kaggle,
includes a total of 6400 MRI images classified into four distinct classes:
Mild-Demented, Moderate-Demented, Very-Mild-Demented, and Non-
Demented. Table 1 shows the total number of images in the dataset.

**Passage 18:**

> 5 images from each dataset. The estimated
processing time per individual was around 23–24 s. In 2021, Helaly
et al. (2021) explored various techniques for categorizing medical
images and detecting AD. The first approach involved implementing
CNN architectures to process 2D and 3D structural brain scans from the
AD Neuroimaging Initiative (ADNI) dataset, using 2D and 3D convolu-
tions. The results demonstrated that using CNN, the accuracy rates for
multi-class AD phase categorization were 95.17% for 3D and 93.61%
for 2D scans. The researchers used the pre-trained VGG19 model for
the second method, achieving a multi-class classification accuracy of
97.00% when analyzing longitudinal brain MRI data. Additionally,
Following that, Battineni et al. (2021) has developed a mechanism to
identify patients with dementia and differentiate between those with
AD and other illnesses.

**Passage 19:**

> ations, including notable deficits in mem-
ory, cognitive impairment, and disorientation, may serve as indicative
markers of neuronal degradation, representing an early and prevalent
indication of AD. The symptoms above gradually deteriorate over
time, negatively affecting an individual’s overall well-being. Although
a cure for AD remains elusive, the provision of timely and efficient
care has the potential to enhance the quality of life and decelerate
the condition’s advancement. MRI scans are a highly valuable dataset
utilized for detecting AD. In the area of analysis of medical images,
DL models are commonly employed. The primary objective of the
presented work was to examine and evaluate two distinct approaches
and five DL architectures in the context of AD identification.

**Passage 20:**

> nal of King Saud University - Computer and Information Sciences 36 (2024) 101940
12
S.E. Sorour et al. Fig. 7. CNN-SVM-with-Aug model. Table 1
Total number of images in AD Dataset available in Kaggle. Class name Total image
Mild-Demented 896
Moderate-Demented 64
Very-Mild-Demented 2240
Non-Demented 3200
Table 2
Binary classification of AD Dataset. Class name Total image
Demented 3200
Non-Demented 3200
Sklearn, were employed to accomplish the programming tasks. The
presented models’ hyperparameters and standard parameter options,
such as the chosen optimizer, loss function, and maximum number of
epochs, can be found in Table 3 . Table 3
Hyper Parameters settings for all suggested models..

**Passage 21:**

> s potential in
medical imaging and its contributions to future AD detection efforts. Journal of King Saud University - Computer and Information Sciences 36 (2024) 101940
17
S.E. Sorour et al. Fig. 13. Visual results of the suggested CNNs-without-Aug (a) Accuracy curve of the suggested CNNs-without-Aug; (b) Loss curve of the suggested CNNs-without-Aug; and (c)
Confusion matrix of the suggested CNNs-without-Aug. Table 9
Performance analysis of the proposed DL models versus different state-of-the-art DL models.

**Passage 22:**

> model
surpassed the other approaches, achieving impressive performance met-
rics, involving accuracy, F1-score, precision, and recall, with values of
93.00%, 94.00%, 94.00%, and 92.00%, respectively. And in 2019, Jo et al. (2019)in their study conducted a com-
parative study on the efficacy of traditional ML and DL methods in
early AD detection and in predicting the advancement from Mild
Cognitive Impairment (MCI) to AD. They examined 16 studies, where
4 combined traditional ML with DL, and 12 solely utilized DL. The
combined approach yielded a 96.00% efficiency in feature selection and
an 84.20% accuracy for predicting MCI to AD conversion. Specifically,
using CNNs in DL achieved similar accuracies in feature selection and
MCI to AD conversion prediction. The study also found that combining
neuroimaging and fluid biomarkers could further enhance classification
performance.

**Passage 23:**

> first build a deep CNN model on the
ImageNet dataset and then use the trained CNN model as a feature
extractor on smaller datasets. This strategy has shown outstanding
results (Biagetti et al., 2021). Furthermore, early or later developed
fusion techniques must be adapted to address the classification prob-
lem of AD utilizing a single MRI (SMRI) modality (such as three
different projections in SMRI) or multiple modalities, such as SMRI
and DTI. The categorization performance was improved by doing so. Several pre-trained CNN models, including AlexNet, deepNN, ResNet-
50, VGG11, ResNet-34, SqueezeNet, DenseNet, and InceptionV3, have
outperformed others in automatically diagnosing the phases of AD
using MRI scans (Odusami et al., 2022).

**Passage 24:**

> cts, 21 pMCI subjects, and 20 AD subjects. The
method achieved exceptional accuracy rates: 99.31% for CN versus AD,
99.88% for CN versus MCI, 99.54% for AD versus MCI, and 96.81% for
pMCI versus sMCI. These results demonstrate the proposed method’s
significant generalization ability and its effectiveness in predicting the
conversion of MCI to AD, even without direct information. The study
concludes that FDG-PET, a well-known biomarker, can effectively iden-
tify AD using transfer learning in DNNs. This approach shows promise
for improving diagnostic accuracy and early detection of AD and its
various stages. Based on the previous studies, it can be said that the data size
is relatively small. Furthermore, the outcomes may be more suitable
for dealing with medical data. Dealing with human life, medical, and
disease data is delicate and demands high accuracy.

</details>

---

## Classification-of-Vascular-Dementia-on-magnetic-res_2024_Intelligent-Systems
_File: `Classification-of-Vascular-Dementia-on-magnetic-res_2024_Intelligent-Systems.pdf`_



<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> onal
connectivity analysis. The patient fixated on a black ’+’ symbol at the
center of a light gray screen. The patient was asked to remain as still as
possible, awake and focused throughout each run. In between runs, the
patient was asked if he could successfully stay still during the previous
run to reinforce the expectation that this should be closely monitored. Each run lasted 7 m 2 s, and three functional runs were collected (Perry
et al., 2021). 3.3. Dataset preprocessing by random selection
In our research on diagnosing vascular dementia using deep learn-
ing, preprocessing plays a pivotal role in shaping the performance
and reliability of our models. A key aspect of preprocessing is data
sampling, which involves the careful selection and manipulation of the
dataset to ensure balanced representation across different classes. 3.3.1.

**Passage 2:**

> ributions to detect vascular Demen-
tia and analyze the performance of the abovementioned deep learning
architectures. 3.2. Dataset acquisition
Data were acquired at the Stanford University Richard M. Lucas
Center for Imaging on a 3T General Electric SIGNA Premier scanner
using a 48-channel head coil (GE Healthcare, Milwaukee, WI, USA). Blood oxygenation level-dependent (BOLD) functional MRI data were
acquired using a simultaneous multislice gradient-echo echo-planar
pulse sequence. Sequence parameters were similar to those used as
part of the Human Connectome Project: TR 1000 ms, TE 30 ms, flip
angle 64◦, 2.4 mm isotropic voxels, matrix 88 × 88 × 65, multislice 5×
acceleration. The signal dropout was minimized by visually selecting a
slice plane approximately 25◦ from the anterior–posterior commissural
plane towards the coronal plane.

**Passage 3:**

> 8 × 88 × 65, multislice 5×
acceleration. The signal dropout was minimized by visually selecting a
slice plane approximately 25◦ from the anterior–posterior commissural
plane towards the coronal plane. A T1-weighted anatomical scan was
acquired in each session using a 3DFSPGR three-dimensional sequence:
TR 1891 ms, TE 1.172 ms, TI 400 ms, flip angle 11 ◦, 1.0 × 1.0 × 1.2 mm
voxels, matrix 256 × 192 × 132. A gradient-echo B0 field map was
acquired to correct for spatial distortions: TE 6.5, 8.5 ms with slice
prescription/spatial resolution matched to the BOLD sequence (Perry
et al., 2021). Data collected during a visual fixation task were used for functional
connectivity analysis. The patient fixated on a black ’+’ symbol at the
center of a light gray screen. The patient was asked to remain as still as
possible, awake and focused throughout each run.

**Passage 4:**

> r its high tendency and morbidity is
essential. However, low incidence should also be accounted for given
the high contrast between potential therapies and outcomes in those di-
agnosed and untreated. Advanced techniques such as Diffusion Tensor
Imaging (DTI) and resting-state functional magnetic resonance imaging
(rs-fMRI) have significantly expanded the potential to study changes in
the brain function and structure typical of dementia ( Braaten, Parsons,
McCue, Sellers, & Burns, 2006; T. O’Brien & Thomas, 2015). As a result,
they can be extensively employed for diagnosis and classification. Deep
learning is a form of artificial intelligence that has revolutionized
several fascinating areas lately: DNA analysis, computer vision, natural
language processing, and brain circuitry. A general way to identify the
VD is illustrated in Fig. 1.

**Passage 5:**

> brain tumor us-
ing deep learning techniques. In 2020 5th international conference on communication
and electronics systems (pp. 1000–1007). IEEE. Morton, R. E., St. John, P. D., & Tyas, S. L. (2019). Migraine and the risk of all-cause
dementia, alzheimer’s disease, and vascular dementia: A prospective cohort study
in community-dwelling older adults. International Journal of Geriatric Psychiatry ,
34(11), 1667–1676. Perry, C., Parvizi, J., & Pinheiro-Chagas, P. (2021). fMRIdata.figshare Dataset. Milwau-
kee, WI, USA: GE Healthcare, Stanford University Richard M. Lucas Center for
Imaging, http://dx.doi.org/10.6084/m9.figshare.14675505.v1, [Online].Available:. Rehman, A., Naz, S., Razzak, M. I., Akram, F., & Imran, M. (2020). A deep learning-
based framework for automatic brain tumors classification using transfer learning. Circuits, Systems, and Signal Processing , 39, 757–775. Román, G.

**Passage 6:**

> etwork
model. This problem is tackled in the proposed research using ReLU and
Leaky ReLU activation functions wherever needed. A detail pictorial
description of proposed model is shown in Fig. 2. 3.1. Dataset details
The dataset used in the proposed experimentation for detecting
and classifying vascular Dementia is resting-state functional magnetic
resonance imaging (rs-fMRI) (Perry, Parvizi, & Pinheiro-Chagas, 2021). It is a multi-class dataset with five classes named Binswanger Dementia,
hemorrhagic Dementia, Multi-Infarct Dementia, Strategical Dementia,
and Subcortical Dementia, as shown in Table 1. The first class of dataset
is Binswanger dementia, also called subcortical vascular Dementia,
Intelligent Systems with Applications 22 (2024) 200388
5
H. Tufail et al. Table 1
Rs-fMRI Dataset.

**Passage 7:**

> ection 4 focuses on the result discussion
of the experimental outcomes and conclusion drawn in Section 5 ,
respectively. 2. Literature review
In this section, the context research has been identified. On the
detection and classification of Vascular Dementia related to medical
image analysis, highlight the techniques and algorithms working based
on recent year studies. Machine learning and deep learning architec-
tures can leave the paradigm change for detecting different diseases in
medical image analysis. MRI and CT scans help us to determine and
evaluate disease detection. Castellazzi et al. ( 2020) explored machine learning algorithms to
differentiate vascular Dementia from Alzheimer’s disease. The collec-
tion of subjects is 77 for MRI scans that are further extended to DTI
and rs-fMRI analysis, which could engender the three dataset classes.

**Passage 8:**

> l diagnosis among alzheimer’s disease, mild cognitive
impairment, and normal subjects using resting-state fMRI data extracted from
multi-subject dictionary learning atlas: A deep learning-based study. Frontiers in
Biomedical Technologies. Balasooriya, N. M., & Nawarathna, R. D. (2017). A sophisticated convolutional neural
network model for brain tumor classification. In 2017 IEEE international conference
on industrial and information systems (pp. 1–5). IEEE. Braaten, A. J., Parsons, T. D., McCue, R., Sellers, A., & Burns, W. J. (2006). Neurocog-
nitive differential diagnosis of dementing diseases: Alzheimer’s dementia, vascular
dementia, frontotemporal dementia, and major depressive disorder. International
Journal of Neuroscience , 116(11), 1271–1293. Butt, H. A., Ahad, A., Wasim, M., Madeira, F., & Chamran, M. K. (2023).

**Passage 9:**

> iate vascular Dementia from Alzheimer’s disease. The collec-
tion of subjects is 77 for MRI scans that are further extended to DTI
and rs-fMRI analysis, which could engender the three dataset classes. The first is the DTI dataset, extracted from VD patients. GT dataset
is extracted from AD, and GT+DTI datasets are extracted from MXD
dementia patients. Three types of algorithms, Artificial Neural Network
(ANN), Support Vector Machine (SVM), and Adaptive Neuro-fuzzy
inference system, were used for detection purposes. Two models of ANN
are used. The first is a Multilayer perceptron (MLP), and the other is the
Radial Basis Function Network (RBFN). The MLP model implemented in
MATLAB is composed of three layers. It comprises n inputs, 8 neurons
in the hidden layer, and one in the output layer. The sigmoid function
is used as an activation function.

**Passage 10:**

> for further prediction on unseen data after training. Intelligent Systems with Applications 22 (2024) 200388
7
H. Tufail et al. Table 3
Results comparison of the proposed method with state-of-the-art. Proposed model Modality Datasets Dataset distribution Used methodology Classification
mode
Accuracy
(%)
Sensitivity
(%)
Specificity
(%)
Precision
(%)
Differentiate the
Vascular
Dementia from
Alzheimer’s
disease
(Castellazzi
et al., 2020)
MRI rs-fMRI
dataset
80% Distribution
Radial Basis
Function Network
Binary
Classification
55.75 55.5 56 55.78
Multilayer
Perceptron
Binary
Classification
58.25 55.5 61 58.73
Support Vector
Machine with
Radial Basis
Function (Kernel)
Binary
Classification
81 93.5 68.5 74.8
Support Vector
Machine with MLP
sigmoid kernel
Binary
Classification
78.25 81 75.5 76.78
Adaptive
Neuro-Fuzzy
Inference System
Binary
Classification
82.75 73.5 92 90.18
Proposed
Methodology
Validation = 28%
Training = 72%
VGG16 Multi-
Classification
90.6 67.07 91.14 82.65
VGG19 88.92 59.72 89.82 79.8
DenseNet121 82.4 100 83.43 81.13
InceptionResNetV2 84.96 61.21 92.69 62.69
Training = 80%
Validation = 10%
Testing = 10%
VGG16
Multi-
Classification
94.15 81.43 94.2 88.39
VGG19 92.38 74.74 92.83 85.32
DenseNet121 84.67 78.97 97.22 79.89
InceptionResNetV2 88.92 71.55 94.94 72.64
Training = 70%
Validation =
15%
Testing = 15%
VGG16 Multi-
Classification
94 80.7 94.01 88.3
VGG19 92.21 73.97 92.59 85.14
InceptionResNetV2 88.58 70.62 94.96 71.81
Fig.

**Passage 11:**

> , when
applicable, co-funded by the FEDER-PT2020 partnership agreement
under the project UIDB/50008/2020. References
Ahad, A., Ali, Z., Mateen, A., Tahir, M., Hannan, A., Garcia, N. M., et al. (2023). A
comprehensive review on 5G-based smart healthcare network security: taxonomy,
issues, solutions and future research directions. Array, Article 100290. Ahad, A., Jiangbina, Z., Tahir, M., Shayea, I., Sheikh, M. A., & Rasheed, F. (2024). 6G
and intelligent healthcare: Taxonomy, technologies, open issues and future research
directions. Internet of Things , Article 101068. Alizadeh, F., Homayoun, H., Batouli, S. A. H., Noroozian, M., Sodaie, F., Salari, H. M., et al. (2022). Differential diagnosis among alzheimer’s disease, mild cognitive
impairment, and normal subjects using resting-state fMRI data extracted from
multi-subject dictionary learning atlas: A deep learning-based study.

**Passage 12:**

> able 1. The first class of dataset
is Binswanger dementia, also called subcortical vascular Dementia,
Intelligent Systems with Applications 22 (2024) 200388
5
H. Tufail et al. Table 1
Rs-fMRI Dataset. Dataset classes Actual image count Random selection
(Unbalanced) (Balanced)
rs-fMRI Dataset
Binswanger Dementia 4608 4400
hemorrhagic Dementia 4608 4400
Multi-Infarct Dementia 7080 4400
Strategical Dementia 4608 4400
Subcortical Dementia 4608 4400
which is a type of Dementia caused by widespread, microscopic areas of
damage to the deep layers of white matter in the brain. A characteristic
pattern of BD-damaged brain tissue can be seen with modern brain
imaging techniques such as CT scans or magnetic resonance imaging
(MRI). The second dataset class is hemorrhagic Dementia, in which
blood accumulates and compresses surrounding areas of brain tissues.

**Passage 13:**

> Karimi, N., Emami, A., & Samavi, S. (2020). Brain tumor
segmentation by cascaded deep neural networks using multiple image scales. In
2020 28th Iranian conference on electrical engineering (pp. 1–4). IEEE. T. O’Brien, J., & Thomas, A. (2015). Vascular dementia. The Lancet , 386(10004),
1698–1706. Wang, C., Xu, J., Zhao, S., & Lou, W. (2019). Identification of early vascular dementia
patients with EEG signal. IEEE Access, 7, 68618–68627. Zhao, X., Wu, Y., Song, G., Li, Z., Zhang, Y., & Fan, Y. (2018). A deep learning model
integrating FCNNs and CRFs for brain tumor segmentation. Medical Image Analysis ,
43, 98–111.

**Passage 14:**

> e glioma molecular subtypes. Experimental studies on the
dataset have yielded positive outcomes (with a test accuracy of 88.82
percent). Parallels with other state-of-the-art approaches were included. Meenakshi and Revathy (2020) explored the Evolution channel
selection algorithm with the EEG signal to differentiate the VD from
Stroke-related patients. This paper shows the number of different tech-
niques to detect VD patients. The first and primary technique is Sav-
itzky Golay filters that are used for the denoising part. The second
most reliable technique is RC dispersion entropy, which extracts the
datasets on the other end. The differential evolution feature selection
(DEFS) algorithm was used to detect the signal more precisely. The
composition of three techniques for detection was given the best lo-
calization.

**Passage 15:**

> Intelligent Systems with Applications 22 (2024) 200388
Available online 18 May 2024
2667-3053/© 2024 The Author(s). Published by Elsevier Ltd. This is an open access article under the CC BY-NC-ND license ( http://creativecommons.org/licenses/by-
nc-nd/4.0/).

**Passage 16:**

> s
proceeds in two folds. First is the discrimination of VD, mild stroke
patients, and recovery stage patients using the fuzzy neighborhood pre-
serve analyzer with the enhancement of QR decomposition. It aims to
expand and observe the spectral features that discriminate mild-stroke
patients from control subjects. However, there are 19th channels that
are analyzed using ICA wavelet analysis. The ratio can be calculated
to show the VD and mild Stroke patients to analyze the dominion
frequency relative power. The nonlinear features like permutation En
and FD were used to calculate the regulation, which can be less in VD
and stroke patients. The SVM classifier and k nearest neighbor classifier
can detect the recovery base patients. The result showed that the SVM
and KNN estimated accuracy is 89%. The Decomposition technique
showed 67% accuracy.

**Passage 17:**

> ilable online 18 May 2024
2667-3053/© 2024 The Author(s). Published by Elsevier Ltd. This is an open access article under the CC BY-NC-ND license ( http://creativecommons.org/licenses/by-
nc-nd/4.0/). Contents lists available at ScienceDirect
Intelligent Systems with Applications
journal homepage: www.journals.elsevier.com/intelligent-systems-with-applications
Classification of Vascular Dementia on magnetic resonance imaging using
deep learning architectures
Hina Tufail a,1, Abdul Ahada,b,c,1, Mustahsan Hammad Naqvia,1, Rahman Maqsooda,1,
Ivan Miguel Piresd,∗,1
a Knowledge Unit of Systems and Technology, University of Management and Technology, Sialkot, Pakistan
b School of Software, Northwestern Polytechnical University, Xian, Shaanxi, 710072, PR China
c Department of Electronics and Communication Engineering, Istanbul Technical University (ITU), 34467, Turkey
d Instituto de Telecomunicações, Escola Superior de Tecnologia e Gestão de Águeda, Universidade de Aveiro, 3750-127, Águeda, Portugal
A R T I C L E I N F O
Keywords:
Convolutional neural network
Densely connected convolutional network
Magnetic resonance imaging
Vascular dementia
Visual geometry group
A B S T R A C T
Vascular Dementia is a severe disease that results from dead nerve cells’ accumulation in blood vessels.

**Passage 18:**

> imaging techniques such as CT scans or magnetic resonance imaging
(MRI). The second dataset class is hemorrhagic Dementia, in which
blood accumulates and compresses surrounding areas of brain tissues. The third class is multi-infarct Dementia, most commonly known as
vascular Dementia, which is caused by multiple strokes or disruption
of blood flow to the brain. The fourth class of the dataset is strategic
Dementia. The last class listed in the dataset is subcortical Dementia,
a clinical syndrome characterized by slow mental processing, forgetful-
ness, impaired cognition, apathy, and depression. All these classes have
different numbers of the image dataset. To make a dataset balanced, up-
sampling and down-sampling techniques are typically used to represent
each class in the dataset equally.

**Passage 19:**

> onal network
Magnetic resonance imaging
Vascular dementia
Visual geometry group
A B S T R A C T
Vascular Dementia is a severe disease that results from dead nerve cells’ accumulation in blood vessels. This
affects the blood flow and impairs memory and decision-making abilities. Machine learning and deep learning
have been used in detecting this disease. Nevertheless, their accuracy has been inconsistent, explaining why
their utilization in diagnosing patients has led to poor performance. We developed several transfer learning
architectures that improve classification accuracy and diagnosis performance in assessing vascular dementia. The process first entails the preprocessing of the dataset where a random selection ensures data representation
is balanced. We used a dataset containing resting-state fMRI scans to split training, testing, and validation
into 80%, 10%, and 10%.

**Passage 20:**

> edical information. As such, the specifics show that our approach achieved 84.67% in accuracy in the multi-classification, which
is better than the current state-of-the-art research in the same field. Therefore, the result shows that transfer
learning-based approaches are suitable when combined with strategic pre-processing and activation functions
in improving the diagnosis of vascular dementia using MRI images. 1. Introduction
Healthcare is undergoing a profound transformation, transitioning
from traditional methods to advanced approaches. Central to this evolu-
tion is cutting-edge communication technologies like 5G and beyond 5G
(B5G), alongside the integration of machine learning and deep learning
algorithms (Ahad et al. , 2024; Butt, Ahad, Wasim, Madeira, & Cham-
ran, 2023 ).

**Passage 21:**

> t before
training. The DenseNet model correctly identifies and classifies the
results. The overall results show that increasing the complexity of the model
may increase the classification performance. The prediction analysis is
based on 80%–20% dataset distribution, details provided in Table 2 ,
because this split has good accuracy and an F1 score. Our experi-
mental model performed well compared to the state-of-the-art model. Table 3 shows the comparison of the proposed method with state-of-
the-art ( Alizadeh et al. , 2022 ; Hu, Ju, Shen, Zhou, & Li , 2016 ) (See
Figs. 3–5). The traditional technique, which depends on the skill of radiother-
apists to evaluate and examine the components of the MRI, has been
utilized for detecting and categorizing Vascular Dementia. Operator-
assisted classification techniques are non-reproducible and are less
suitable for big datasets.

**Passage 22:**

> assification, no
vacant accuracies exist with a machine learning algorithm that proves
the person has VD 100%. Existing Machine learning-based architectures
cannot classify VD into Multiple divisions. Hence, these are the main
factors to conduct this research study. 1.1. Contribution and organization of the paper
The present study’s main value is that it thoroughly analyzes the rs-
fMRI dataset using a range of deep learning architectures. We sought
to identify the best-performing model for early-stage VD detection by
Intelligent Systems with Applications 22 (2024) 200388
3
H. Tufail et al. Fig. 2. Block diagram of Deep Learning Architectures to classify MRI-based vascular Dementia.
comparing and contrasting the architectures’ capabilities. The solutions
developed in this study do not have novel characteristics.

**Passage 23:**

> the components of the MRI, has been
utilized for detecting and categorizing Vascular Dementia. Operator-
assisted classification techniques are non-reproducible and are less
suitable for big datasets. Manual processing of huge datasets is a
time-consuming operation. Computer-aided diagnostic techniques are
required to process a large amount of data efficiently to tackle such
difficulties. The best-performing approaches for such challenges follow
a similar pattern ( Balasooriya & Nawarathna, 2017; Ford et al. , 2019;
Zhao et al. , 2018 ). Instead of training a singular deep CNN model,
many deep CNN models are trained and merged to determine the
final results. To make maximum use of diverse aspects of the available
data, the models utilized vary in terms of network topologies, inherent
complexity, and loss functions.

**Passage 24:**

> apture brain cell signals’ electrical impulses. Electrical signals
are used by the nerve cells for interaction with each other. Wavy lines
will surface on an EEG recording due to this brain operation. Target
stimuli (green circles) and no target stimuli (red circles) were noted
for a clearer understanding of how differential functions. Each stimulus
appeared randomly in the middle of the display, and its diameter was
measured. Ford et al. ( 2019) compared machine learning algorithms with
epidemiological approaches to detect Dementia for initial care patients. The data on dementia patients was collected over five years. It was
designed with the same split sets between each model. This data is
divided into a training set (80%) and a test set (20%).

</details>

---

## Combining Unsupervised and Supervised Deep Learning for Alzheimer-s Disease Detection by Fractional Anisotropy Imaging
_File: `Combining Unsupervised and Supervised Deep Learning for Alzheimer-s Disease Detection by Fractional Anisotropy Imaging.pdf`_

1. **Yes**, diffusion MRI (DWI and DTI) was used in this paper.  
   - **Excerpt**: "the diffusion tensor (a 3 × 3 symmetric matrix) to each voxel in order to obtain the diffusion tensor image."  
   - **Excerpt**: "DWI scans" and "DTI data" are explicitly mentioned.  

2. **Processing steps applied to diffusion images (in order)**:  
   - **Brain mask extraction**: "a brain mask was extracted using the Otzu thresholding method followed by a dilation operation."  
   - **Diffusion tensor fitting**: "the ordinary least squares method was used with the corresponding b-values and b-vectors to fit the diffusion tensor."  
   - **Fractional anisotropy (FA) calculation**: "the fractional anisotropy was calculated as: FA = ...".  
   - **Image scaling and rotation**: "scans were scaled to match a common resolution of 2.50 mm/px in the three dimensions and rotated according to the RPS direction."  
   - **Cropping**: "images were cropped to a size of 96 × 96 × 64px."  

3. **Software/tools explicitly named**:  
   - **Dipy** for diffusion MRI processing.  
   - **Kornia** and **TorchIO** for data augmentation.  
   - **PyTorch** and **PyTorch Lightning** for model implementation.  

4. **Reported acquisition/processing parameters**:  
   - **Minimum number of volumes (shells)**: "DWIs with less than ten volumes (shells) were discarded."  
   - **Resolution**: "scaled to 2.50 mm/px in the three dimensions."  
   - **B-values and b-vectors**: Mentioned as inputs for tensor fitting but no specific values provided.  

5. **Exact sentences from excerpts**:  
   - "a brain mask was extracted using the Otzu thresholding method followed by a dilation operation; this mask was used to separate the brain volume from the background."  
   - "the ordinary least squares method was used with the corresponding b-values and b-vectors to fit the diffusion tensor (a 3 × 3 symmetric matrix) to each voxel in order to obtain the diffusion tensor image."  
   - "the fractional anisotropy was calculated as: FA = ..."  
   - "scans were scaled to match a common resolution of 2.50 mm/px in the three dimensions and rotated according to the RPS direction."  
   - "images were cropped to a size of 96 × 96 × 64px."  
   - "DWIs with less than ten volumes (shells) were discarded."  

6. **Processing description completeness**:  
   - **Complete for MRI preprocessing**: The steps for diffusion MRI processing (masking, tensor fitting, FA calculation, scaling, rotation, cropping) are explicitly described.  
   - **Incomplete for model training**: The excerpts do not detail the specific parameters or architecture of the 3D CNNs or autoencoders used for deep learning, though they mention their use.  
   - **Conclusion**: The MRI processing steps are fully described, but the deep learning model training details are omitted.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> r, inferior
to superior). Moreover, a brain mask was extracted using the
Otzu thresholding method followed by a dilation operation;
this mask was used to separate the brain volume from the
background. Then, the ordinary least squares method was
used with the corresponding b-values and b-vectors to ﬁt the
diffusion tensor (a 3 × 3 symmetric matrix) to each voxel
in order to obtain the diffusion tensor image. From the DTI
obtained so far, the fractional anisotropy was calculated as:
FA =
√
1
2
(λ1 − λ2)2 +(λ1 − λ3)2 +(λ2 − λ3)2
λ2
1 +λ2
2 +λ2
3
where λi are the eigenvalues of the diffusion tensor. As a
ﬁnal step, the images were cropped to a size of 96 × 96 ×
64px. This measurement and the chosen resolution represented
a volume of 1470 cm3 sufﬁcient for the average brain volume
of 1270 cm3 and 1130 cm3 for men and women respectively.

**Passage 2:**

> e limited number of samples,
we also used online data augmentation techniques, precisely
a combination of z-axis mirroring (resulting in hemisphere
swapping), three-dimensional rotation, and clipping. These
three transformations were applied randomly with a speciﬁc
probability during training: mirroring was applied with a
probability of 0.5, rotation with 0.75, and clipping with 0.8. Finally, further preprocessing was required to extract frac-
tional anisotropy from the DWI before training the models. First, the scans were scaled to match a common resolution of
2.50 mm/px in the three dimensions and rotated according to
the RPS direction (left to right, anterior to posterior, inferior
to superior). Moreover, a brain mask was extracted using the
Otzu thresholding method followed by a dilation operation;
this mask was used to separate the brain volume from the
background.

**Passage 3:**

> V an Der Walt,
M. Descoteaux, I. Nimmo-Smith, and D. Contributors, “Dipy, a library
for the analysis of diffusion MRI data,” Frontiers in neuroinformatics,
vol. 8, p. 8, 2014.
[35] L. N. Smith and N. Topin, “Super-convergence: V ery fast training of
neural networks using large learning rates,” inArtiﬁcial intelligence and
machine learning for multi-domain operations applications, vol. 11006. SPIE, 2019, pp. 369–386. 516
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:43:40 UTC from IEEE Xplore. Restrictions apply.

**Passage 4:**

> d radial diffusivity, may provide additional
information about the integrity of white matter in the brain. The proposed approach could be extended to provide a more
comprehensive analysis of DTI data. Finally, using unsuper-
vised pre-training may be advantageous to alleviate the need
for labels that may be difﬁcult to collect in the medical
ﬁeld. This approach could be further explored to improve
the robustness and generalization of the proposed approach,
especially when dealing with small and unbalanced datasets.

**Passage 5:**

> “Deep residual learning for image
recognition,” inProceedings of the IEEE conference on computer vision
and pattern recognition, 2016, pp. 770–778.
[32] J. Shi, E. Riba, D. Mishkin, F. Moreno, and A. Nicolaou, “Differentiable
data augmentation with Kornia,”arXiv preprint arXiv:2011.09832, 2020.
[33] F. P ´erez-Garc´ıa, R. Sparks, and S. Ourselin, “TorchIO: a Python li-
brary for efﬁcient loading, preprocessing, augmentation and patch-based
sampling of medical images in deep learning,”Computer Methods and
Programs in Biomedicine, vol. 208, p. 106236, 2021.
[34] E. Garyfallidis, M. Brett, B. Amirbekian, A. Rokem, S. V an Der Walt,
M. Descoteaux, I. Nimmo-Smith, and D. Contributors, “Dipy, a library
for the analysis of diffusion MRI data,” Frontiers in neuroinformatics,
vol. 8, p. 8, 2014.
[35] L. N. Smith and N.

**Passage 6:**

> Combining Unsupervised and Supervised Deep
Learning for Alzheimer’s Disease Detection by
Fractional Anisotropy Imaging
Giovanna Castellano
Dept. of Computer Science
University of Bari
Bari, Italy
giovanna.castellano@uniba.it
Eufemia Lella
Innovation Lab
Exprivia S.p.A.

**Passage 7:**

> tion by Induced Local Interactions:
Examples Employing Nuclear Magnetic Resonance,” Nature, vol. 242, no. 5394, pp. 190–191, mar 1973. [Online]. Available:
https://doi.org/10.1038
[9] G. Placidi, MRI. CRC Press, may 2012. [Online]. Available:
https://doi.org/10.1201
[10] R. Jain, N. Jain, A. Aggarwal, and D. J. Hemanth,
“Convolutional neural network based Alzheimer’s disease classiﬁcation
from magnetic resonance brain images,” Cognitive Systems
Research, vol. 57, pp. 147–159, 2019. [Online]. Available:
https://www.sciencedirect.com/science/article/pii/S1389041718309562
[11] N. M. Khan, M. Hon, and N. Abraham, “Transfer Learning with
intelligent training data selection for prediction of Alzheimer’s Disease,”
2019. [Online]. Available: http://arxiv.org/abs/1906.01160
[12] H. Acharya, R. Mehta, and D.

**Passage 8:**

> to a size of 96 × 96 ×
64px. This measurement and the chosen resolution represented
a volume of 1470 cm3 sufﬁcient for the average brain volume
of 1270 cm3 and 1130 cm3 for men and women respectively. Since the values of the FA voxels are within the range [0, 1],
scaling was not necessary. V. E XPERIMENTS
The experiments were run on Kaggle. The model archi-
tectures were implemented using the PyTorch and PyTorch
Lightning libraries, while data augmentation was achieved
with the Kornia [32] and TorchIO [33] libraries. Instead, all
preprocessing steps were performed using Dipy [34]. The classiﬁcation model was evaluated using a stratiﬁed
10-fold cross-validation, taking care that the same subject
was not present in both training and validation sets, as this
could have led to overly optimistic results.

**Passage 9:**

> each
subject, one or more sessions have been performed over time,
and some sessions have more than one scan available. For this
work, we considered the 1754 DWI sessions, corresponding
to 3255 scans. In addition, to further increase the number
of samples, we used the IXI dataset [29], which provides
400 DWI sessions of cognitively normal subjects. While DWI
refers to the contrast of acquired images, DTI is a speciﬁc
type of DWI modeling [30]. It allows the measurement of
other diffusion parameters, such as fractional anisotropy. Each available DWI was analyzed to ﬁnd corrupted scans
and sessions with a mismatch between the b-values, the b-
vectors, and the corresponding number of volumes. The b-
values and b-vectors describe each volume’s magnetic ﬁeld
strength and direction. We also discarded DWIs with less than
ten volumes (shells).

**Passage 10:**

> ional neural
networks,” PLOS ONE , vol. 15, no. 3, 2020. [Online]. Available:
https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0230409
[28] L. Houria, N. Belkhamsa, A. Cherfa, and Y . Cherfa, “Multi-modality
MRI for Alzheimer’s disease detection using deep learning,” Physical
and Engineering Sciences in Medicine, vol. 45, no. 4, 2022. [Online]. Available: https://doi.org/10.1007/s13246-022-01165-9
[29] “IXI dataset.” [Online]. Available: https://brain-development.org/ixi-
dataset/
[30] J. M. Soares, P . Marques, V . Alves, and N. Sousa, “A hitchhiker’s guide
to diffusion tensor imaging,” Frontiers in neuroscience, vol. 7, p. 31,
2013.
[31] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image
recognition,” inProceedings of the IEEE conference on computer vision
and pattern recognition, 2016, pp. 770–778.
[32] J. Shi, E. Riba, D. Mishkin, F. Moreno, and A.

**Passage 11:**

> -
vectors, and the corresponding number of volumes. The b-
values and b-vectors describe each volume’s magnetic ﬁeld
strength and direction. We also discarded DWIs with less than
ten volumes (shells). After this cleaning step, the available
DWI scans became 3124. To provide a ground truth, we used
the clinicians’ judgments along with the clinical diagnoses
provided with the dataset to infer a diagnosis for each subject. From the clinicians’ judgments, we obtained the age from
which the subject ﬁrst manifested signs of mental illness. At the same time, the clinical diagnoses provide information
about the subject’s illness, taking into account the subject’s
history.

**Passage 12:**

> to 2D CNNs, 3D
CNNs have also been studied for AD detection using MRI
data. 3D CNNs can capture the spatial relationships between
voxels in 3D MRI volumes, which may be essential for the
task at hand. Some studies have used 3D CNNs pre-trained
on natural images, while others have used a pre-training based
on autoencoders [14]–[16]. Concerning DTI [17], it is an imaging technique that
measures the diffusion of water molecules in biological tissues
in multiple directions to estimate the directionality and extent
of water diffusion, enabling the reconstruction of white matter
tracts in the brain. To this end, it has been widely used to study
brain connectivity and white matter integrity and has also been
applied to diagnosing neurodegenerative diseases, including
AD.

**Passage 13:**

> sing 3D CNNs
to detect AD with FA images. This could signiﬁcantly con-
tribute to improved performance. In addition, the use of 3D
CNNs is relatively new, as many studies have focused only on
2D CNNs. Finally, we used the recently published OASIS-3
dataset, one of the largest and most comprehensive publicly
available datasets for AD detection. III. M A TERIALS
This study was primarily based on the longitudinal OASIS-
3 dataset [7], which consists of a collection of MRI and PET
scans for 1098 subjects, of whom 609 are cognitively normal,
and 489 are in different stages of cognitive decline. For each
subject, one or more sessions have been performed over time,
and some sessions have more than one scan available. For this
work, we considered the 1754 DWI sessions, corresponding
to 3255 scans.

**Passage 14:**

> tructural
White Matter Degeneration in Alzheimer’s Disease Using Machine
Learning Classiﬁcation of Multicenter DTI Data,” PLOS ONE, vol. 8,
no. 5, 2013, publisher: Public Library of Science. [Online]. Available:
https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0064925
[24] Y . Wang, Y . Y ang, X. Guo, C. Y e, N. Gao, Y . Fang, and H. T. Ma,
“A Novel Multimodal MRI Analysis for Alzheimer’s Disease Based
on Convolutional Neural Network,” in2018 40th Annual International
Conference of the IEEE Engineering in Medicine and Biology Society
(EMBC), 2018.
[25] K. Aderghal, A. Khvostikov, A. Krylov, J. Benois-Pineau, K. Afdel,
and G. Catheline, “Classiﬁcation of Alzheimer Disease on Imaging
Modalities with Deep CNNs Using Cross-Modal Transfer Learning,” in
2018 IEEE 31st International Symposium on Computer-Based Medical
Systems (CBMS), 2018, pp. 345–350.
[26] A. Khvostikov, K.

**Passage 15:**

> for Alzheimer’s dis-
ease (AD) detection using diffusion tensor imaging, speciﬁcally
fractional anisotropy (FA) images, based on a combination of
unsupervised and supervised deep learning techniques. Our
method involves training a 3D convolutional autoencoder to learn
low-dimensional representations of FA images in an unsupervised
manner and using the learned representations to pre-train a
supervised 3D convolutional classiﬁer to predict the presence or
absence of AD. Unsupervised pre-training can improve the clas-
siﬁer’s performance, especially when difﬁcult-to-collect labeled
data are limited. We evaluate our approach on the OASIS-3
dataset and demonstrate promising performance. Index Terms—3D convolutional neural networks, Alzheimer’s
disease, autoencoder, deep learning, DTI, fractional anisotropy
I.

**Passage 16:**

> subjects) and 327 positive samples that will be
used for classiﬁcation. The discarded scans were kept aside
and, together with the samples from the IXI dataset, will be
used for autoencoder training. We ensured that the two datasets
(for classiﬁcation and autoencoder training) were disjointed;
in other words, the same subject was absent in both datasets. A summary is shown in Table I. IV . METHODS
Our model was inspired by ResNet-18 [31], in which we
replaced two-dimensional convolutions with three-dimensional
ones and replaced the ReLU activation function with
LeakyReLU with a negative slope equal to 0.2. In more detail,
TABLE I
SUMMARY OF THE COMPOSITION OF THE DA TASET
AD Healthy Other diseases Unlabeled
Subjects 173 84 78 692
Scans 327 336 155 2310
the neural network consists of a ﬁrst convolutional block with
64 ﬁlters, a kernel size of 7, stride 2, and a padding of 2.

**Passage 17:**

> CI, and normal aging,” NeuroImage:
Clinical, vol. 3, pp. 180–195, 2013. [Online]. Available:
https://www.sciencedirect.com/science/article/pii/S2213158213000934
[22] E. Lella, A. Pazienza, D. Lofu, R. Anglani, and F. Vitulano, “An
ensemble learning approach based on diffusion tensor imaging measures
for Alzheimer’s disease classiﬁcation,”Electronics, vol. 10, no. 3, p. 249,
2021.
[23] M. Dyrba, M. Ewers, M. Wegrzyn, I. Kilimann, C. Plant, A. Oswald,
T. Meindl, M. Pievani, A. L. W. Bokde, A. Fellgiebel, M. Filippi,
H. Hampel, S. Kl ¨oppel, K. Hauenstein, T. Kirste, S. J. Teipel, and
t. E. s. Group, “Robust Automated Detection of Microstructural
White Matter Degeneration in Alzheimer’s Disease Using Machine
Learning Classiﬁcation of Multicenter DTI Data,” PLOS ONE, vol. 8,
no. 5, 2013, publisher: Public Library of Science. [Online].

**Passage 18:**

> s evaluated
on the OASIS-3 dataset, yielding promising results. Future work could include evaluating the proposed method
on more extensive and diverse datasets to validate its ef-
fectiveness further. In addition, interpretation of the learned
representations could provide insights into the mechanisms
underlying AD and contribute to developing more targeted
and personalized treatment options. The method could also
be extended to other diseases, such as Parkinson’s or multiple
sclerosis, to improve early diagnosis. Other DTI modalities,
such as axial and radial diffusivity, may provide additional
information about the integrity of white matter in the brain. The proposed approach could be extended to provide a more
comprehensive analysis of DTI data.

**Passage 19:**

> our approach on the OASIS-3
dataset and demonstrate promising performance. Index Terms—3D convolutional neural networks, Alzheimer’s
disease, autoencoder, deep learning, DTI, fractional anisotropy
I. I NTRODUCTION
Alzheimer’s disease (AD) is a progressive and debilitating
neurological disorder affecting millions of people worldwide,
the early detection of which is critical for timely treatment and
improved patient outcomes [1]. In this context, diffusion tensor
imaging (DTI) is an advanced magnetic resonance imaging
(MRI) technique that has proven helpful for detecting early
signs of AD by measuring the integrity of white matter ﬁber
tracts in the brain [2]. In particular, fractional anisotropy (FA)
is a widely used metric derived from DTI, reﬂecting the degree
of anisotropy in water diffusion, which has been found to be
altered in AD patients in the literature, e.g. [3].

**Passage 20:**

> actional anisotropy (FA)
is a widely used metric derived from DTI, reﬂecting the degree
of anisotropy in water diffusion, which has been found to be
altered in AD patients in the literature, e.g. [3]. However, the analysis of FA images can be challenging due
to the complexity and variability of these data. Traditional
image analysis methods have limitations in capturing subtle
patterns in the images and require extensive feature engineer-
ing and manual intervention, which can be time-consuming
and error-prone. On the other hand, recent advances in deep
learning techniques have shown great promise in various
medical imaging applications, including AD detection by DTI,
e.g. [4], [5]. Deep learning models can learn to automatically
extract meaningful features from raw neuroimaging data and
have the potential to improve the accuracy and efﬁciency of
AD diagnosis [6].

**Passage 21:**

> tensor imaging of white matter degeneration
in early stage of Alzheimer’s disease: a review,” International Journal
of Neuroscience, vol. 130, no. 3, pp. 243–250, 2020.
[3] J. L. Dalboni da Rocha, I. Bramati, G. Coutinho, F. Tovar Moll,
and R. Sitaram, “Fractional Anisotropy changes in parahippocampal
cingulum due to Alzheimer’s Disease,”Scientiﬁc reports, vol. 10, no. 1,
p. 2660, 2020.
[4] E. Lella and G. V essio, “Ensembling complex network ‘perspectives’
for mild cognitive impairment detection with artiﬁcial neural networks,”
Pattern Recognition Letters, vol. 136, pp. 168–174, 2020.
[5] A. De and A. S. Chowdhury, “DTI based Alzheimer’s disease classiﬁ-
cation with rank modulated fusion of CNNs and random forest,”Expert
Systems with Applications, vol. 169, p. 114338, 2021.
[6] M. A. Ebrahimighahnavieh, S. Luo, and R.

**Passage 22:**

> atter
tracts in the brain. To this end, it has been widely used to study
brain connectivity and white matter integrity and has also been
applied to diagnosing neurodegenerative diseases, including
AD. Traditional machine learning techniques combined with
tractography-based approaches have been applied to DTI data
for AD characterisation [18] and diagnosis at different stages
of cognitive decline [19]. Other approaches consist of feeding
traditional machine learning algorithms with features extracted
by manually selecting regions of interest from DTI data [20],
[21] or by selecting voxels through spatial-based statistics [22]. A further approach is to use principal component analysis to
reduce the dimensionality of DTI data and extract features for
the same objective [23].

**Passage 23:**

> isease Detection by
Fractional Anisotropy Imaging
Giovanna Castellano
Dept. of Computer Science
University of Bari
Bari, Italy
giovanna.castellano@uniba.it
Eufemia Lella
Innovation Lab
Exprivia S.p.A. Molfetta, Italy
eufemia.lella@exprivia.com
V alerio Longo
Dept. of Computer Science
University of Bari
Bari, Italy
v.longo20@studenti.uniba.it
Giuseppe Placidi
A2VI-Lab, c/o MeSVA Department
University of L’Aquila
L’Aquila, Italy
giuseppe.placidi@univaq.it
Matteo Polsinelli
Dept. of Computer Science
University of Salerno
Fisciano, Italy
mpolsinelli@unisa.it
Gennaro V essio
Dept. of Computer Science
University of Bari
Bari, Italy
gennaro.vessio@uniba.it
Abstract—We propose a new approach for Alzheimer’s dis-
ease (AD) detection using diffusion tensor imaging, speciﬁcally
fractional anisotropy (FA) images, based on a combination of
unsupervised and supervised deep learning techniques.

**Passage 24:**

> fractional
anisotropy, mean diffusivity, and mode of anisotropy, along
with the gray matter map from structural MRI. They accu-
rately classiﬁed AD patients and healthy controls using these
features. Similarly, Houria et al. [28] used a custom 2D CNN
architecture with an SVM-based classiﬁcation head to select
slices from two different DTI maps (fractional anisotropy and
mean diffusivity) and the gray matter map from structural
MRI. They extracted features using these three models and
combined them using an SVM to produce the ﬁnal output. The novelty of our approach lies in the combination of
unsupervised and supervised learning methods using 3D CNNs
to detect AD with FA images. This could signiﬁcantly con-
tribute to improved performance. In addition, the use of 3D
CNNs is relatively new, as many studies have focused only on
2D CNNs.

</details>

---

## CT-GAN A Cross-Modal Transformer GAN for Superior Multi-Modal MRI-Based Alzheimer-s Disease Detection
_File: `CT-GAN A Cross-Modal Transformer GAN for Superior Multi-Modal MRI-Based Alzheimer-s Disease Detection.pdf`_

1. **Was diffusion MRI (DTI, dMRI, DWI, or similar) used in this paper?**  
   Yes. The paper explicitly mentions **Diffusion Tensor Imaging (DTI)** as part of the multi-modal MRI data used for Alzheimer's Disease detection.  

---

2. **What processing steps were applied to the diffusion images?**  
   - **Resizing**: "All images are resized to 128 × 128 pixels because deep learning models need same size inputs for proper training."  
   - **Data augmentation**: "The Adaptive Augmenter is a flexible way to get the most out of the augmentation process when training a Generative Adversarial Network (GAN)." This includes controlled distortion with:  
     - Maximum translation of 0.125 (x and y axes).  
     - Maximum rotation of 0.125 (small angular differences).  
     - Maximum zoom of 0.25 (scaling within a predetermined interval).  
   - **Generator architecture**: "The Generator of the CT-GAN employs transposed convolutional layers, or deconvolution layers, to iteratively expand an array of noise to the size of a 128×128×3 image."  
   - **Discriminator architecture**: "The Discriminator in CT-GAN consists of a sequence of convolutional layers with strides 2, which downsamples the spatial dimensions of the input image."  
   - **Bi-attention mechanism**: "The bi-attention mechanism makes the process easier by combining resting-state fMRI functional information with structural information from Diffusion Tensor Imaging."  

---

3. **What software or tools are explicitly named for processing?**  
   - **Kaggle hub library**: "The dataset itself is copied to the correct working directory for further processing. All images are resized..." (implied use of Kaggle hub for dataset handling).  
   - **Generative models**: Specific models like DCGAN, WGAN, CGAN, Pix2Pix, CycleGAN, and VAE-GAN are mentioned as comparison benchmarks.  

---

4. **What acquisition or processing parameters are explicitly reported?**  
   - **Image resizing**: 128 × 128 pixels.  
   - **Data augmentation parameters**:  
     - Maximum translation: 0.125 (x and y axes).  
     - Maximum rotation: 0.125 (angular differences).  
     - Maximum zoom: 0.25 (scaling interval).  

---

5. **Copy the exact sentences from the excerpts that describe the processing.**  
   - "All images are resized to 128 × 128 pixels because deep learning models need same size inputs for proper training."  
   - "The Adaptive Augmenter is a flexible way to get the most out of the augmentation process when training a Generative Adversarial Network (GAN)."  
   - "The Generator of the CT-GAN employs transposed convolutional layers, or deconvolution layers, to iteratively expand an array of noise to the size of a 128×128×3 image."  
   - "The Discriminator in CT-GAN consists of a sequence of convolutional layers with strides 2, which downsamples the spatial dimensions of the input image."  
   - "The bi-attention mechanism makes the process easier by combining resting-state fMRI functional information with structural information from Diffusion Tensor Imaging."  

---

6. **Is the processing description complete, or does it appear incomplete/missing?**  
   The processing description is **incomplete**. While it details resizing, augmentation, and neural network architectures, it does **not** report specific diffusion MRI acquisition parameters (e.g., b-values, number of diffusion directions, voxel size) or diffusion-specific preprocessing steps (e.g., tensor fitting, FA/MD calculation). The focus is on GAN training and multimodal integration rather than diffusion MRI technical details.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> -
modal data fusion, functional MRI, Diffusion Tensor  Imaging, 
bi-attention mechanism, generative models, image ge neration, 
precision, recall, accuracy, F1-score, Area Under t he Curve 
(AUC) . I. INTRODUCTION  
 
A progressive neurological disease that affects mil lions of 
individuals and their families worldwide, Alzheimer 's disease 
(AD) is characterized by memory loss, cognitive imp airment, 
decline in cognitive abilities, and changes in beha vior. 5.1 
million Americans have been found to suffer from th e disorder 
at present, and its prevalence will continue to ris e with the 
population of the world's aging population. Alzheimer's disease 
must be found 
 
 
in its early stage only so that doctors can control  and treat it 
properly.

**Passage 2:**

> r bui lds noise 
vectors into real images one at a time. The discriminator, on the 
other hand, correctly tells the difference between real and 
generated examples and helps the generator get bett er. The bi-
attention mechanism makes the process easier by com bining 
resting-state fMRI functional information with stru ctural 
information from Diffusion Tensor Imaging. This hel ps find 
Alzheimer's Disease (AD) more easily. To make train ing more 
robust and generalizable, adaptive data augmentatio n is 
included. The method subject’s images to controlled  distortion 
during training so that the model is able to become more robust 
to variations. The augmentation consists of a maxim um 
translation of 0.125 (moving images on the x and y axes), a 
maximum rotation of 0.125 (imposing small angular 
differences), and a maximum zoom of 0.25 (scaling i mages 
within a predetermined interval).

**Passage 3:**

> IEEE Xplore. Restrictions apply. 2025 International Conference on Sustainability, Innovation & Technology (ICSIT ) 
 
979-8-3315-3549-0/25/$31.00 ©2025 IEEE 
 
and 
genomic 
s for AD 
decoding 
. IV. METHODOLOGY  
Data Collection 
The GAN training data comes from the Kaggle dataset "images-
oasis" itself. This dataset further provides the necessary images 
for model training. It can be downloaded using the Kaggle hub 
library. After downloading, the dataset itself is c opied to the 
correct working directory for further processing. All images are 
resized to 128 × 128 pixels because deep learning models need 
same size inputs for proper training. GANs themselv es require 
this uniformity to further improve their training s peed. This 
resizing surely makes all data uniform across the dataset, which 
helps both generator and discriminator networks lea rn patterns 
more easily.

**Passage 4:**

> RCH IN 
MEDICAL IMAGE ACQUISITION AND OBJECT DETECTION 
METHODS . THE PRECEDING STUDIES ' FINDINGS AND 
OBSERVATIONS ARE SUMMARIZED AND PROVIDED , WELL 
SUMMARIZING THE RESEARCH GAPS THAT WERE FOUND . Stu 
dy 
Moda 
lity 
Dataset Methodo 
logy 
Advantag 
es 
Disadvan 
tages 
[1] MRI ADNI Utilized 
Latent 
Diffusio 
n Models 
and 
Convolu 
tional 
Neural 
Network 
s to 
Demonst 
rated 
enhanced 
detection 
accuracy 
by 
combinin 
g 
generativ 
e models 
Requires 
extensive 
computat 
ional 
resources 
for 
training 
complex 
models. 
improve 
AD 
detection 
. 
with 
CNNs. 
[2]  
 
MRI Various Reviewe 
d AI 
applicati 
ons in 
brain 
MRI 
analysis 
for AD, 
focusing 
on deep 
learning 
approach 
es. Provided 
a 
compreh 
ensive 
evaluatio 
n of AI 
methodol 
ogies in 
MRI-
based 
AD 
analysis.

**Passage 5:**

> tic 
resonance imaging (MRI) has become an essential ima ging 
modality for depicting structural changes in the brain related to 
dementia, like cortical flattening and reduction of  the 
hippocampus. Getting good MRI data for training dia gnostic 
models is actually very difficult because of privac y problems, 
limited patient access, and money issues. These cha llenges 
definitely make it hard to build effective medical AI systems. Further, these limits actually reduce how well machine learning 
systems work across different groups of people. They definitely 
make it harder to find Alzheimer's disease in its e arly stages. Scientists are using generative artificial intellig ence (AI) 
techniques to data augment and circumvent these lim itations.

**Passage 6:**

> efinitely 
make it harder to find Alzheimer's disease in its e arly stages. Scientists are using generative artificial intellig ence (AI) 
techniques to data augment and circumvent these lim itations. The promise of generative AI is to transform Alzhei mer's 
diagnosis by generating simulated MRI scans that ar e 
remarkably similar to actual patient scans, thereby  increasing 
the availability and variety of datasets and mainta ining the 
confidentiality of the patients. Variational auto encoders 
(VAEs) and Generative Adversarial Networks (GANs) a re just 
a few instances of novel AI models. have revolutionary promise 
in medical imaging.

**Passage 7:**

> from IEEE Xplore. Restrictions apply. 2025 International Conference on Sustainability, Innovation & Technology (ICSIT ) 
 
979-8-3315-3549-0/25/$31.00 ©2025 IEEE 
 
inputs a small, non-zero gradient. This keeps the m odel from 
"dying" while it learns and makes it better at lear ning. The last 
layer of the discriminator is a dense layer that ou tputs a score 
between 0 and 1 that tells you how likely it is tha t an image is 
real or fake. So, the discriminator is a binary classifier that sorts 
real and fake photos in the GAN system. This struct ure is 
important because it helps the CT-GAN effectively c ombine 
multimodal neuroimaging data and improve the detect ion of 
AD. Adaptive Augmenter  
The Adaptive Augmenter is a flexible way to get the  most out 
of the augmentation process when training a Generat ive 
Adversarial Network (GAN).

**Passage 8:**

> tion. IX. R
EFERENCES  
[1] T. P. Dhinagar NJ, Thomopoulos SI, “Generative AI 
improves MRI‐based Detection of Alzheimer’s Disease 
by using Latent Diffusion Models and Convolutional 
Neural Networks. Alzheimers Dement.,” 2025, DOI: 
DOI: 10.1002/alz.089958. 
[2] S. X. Frizzell TO, Glashutter M, Liu CC, Zeng A , Pan 
D, Hajra SG, D’Arcy RCN, “Artificial intelligence i n 
brain MRI analysis of Alzheimer’s disease over the past 
12 years: A systematic review. Ageing,” 2022, DOI: 
DOI: 10.1016/j.arr.2022.101614. 
[3] R. J. T. A. Borchert, “Artificial intelligence for 
diagnostic and prognostic neuroimaging in dementia: A 
systematic review,” 2023, DOI: 
https://doi.org/10.1002/alz.13412. 
[4] J. H. Xiaoqiong An, “The application of artific ial 
intelligence in diagnosis of Alzheimer’s disease: a  
bibliometric analysis,” 2024, DOI: 
https://doi.org/10.3389/fneur.2024.1510729. 
[5] F. C.

**Passage 9:**

> 4] J. H. Xiaoqiong An, “The application of artific ial 
intelligence in diagnosis of Alzheimer’s disease: a  
bibliometric analysis,” 2024, DOI: 
https://doi.org/10.3389/fneur.2024.1510729. 
[5] F. C. Dolci, Giorgio, “An interpretable generat ive 
multimodal neuroimaging-genomics framework for 
decoding Alzheimer’s disease,” 2024, DOI: 
https://doi.org/10.48550/arXiv.2406.13292  
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:43:40 UTC from IEEE Xplore. Restrictions apply.

**Passage 10:**

> ‘
 
   
Abstract- 
This research introduces CT-GAN, an innovative Cross-Modal 
Transformer employing Generative Adversarial Networ ks for 
the diagnosis of Alzheimer's Disease (AD) utilizing  multi-
modal neuroimaging data. CT-GAN accurately delineat es the 
spatial and functional intricacies of the brain by integrating 
functional MRI (fMRI) and Diffusion Tensor Imaging (DTI) 
with a bi-attention mechanism. CTGAN consistently 
outperformed state-of-the-art generative models—DCGA N, 
WGAN, CGAN, Pix2Pix, CycleGAN, and VAE-GAN—on all 
the important criteria, with the best accuracy (90% ), precision 
(89%), recall (91%), F1-score (90%), and an amazing  AUC of 
0.95. They show that CT-GAN can make high-quality fake data 
without hurting its ability to classify things well, with few false 
positives and negatives.

**Passage 11:**

> blio 
metric 
data 
Conduct 
ed a 
bibliome 
tric 
analysis 
on AI 
applicati 
ons in 
early AD 
diagnosi 
s and 
monitori 
ng. Identified 
research 
trends 
and gaps 
in AI-
based 
AD 
diagnosti 
cs. Relied on 
bibliomet 
ric data 
without 
experime 
ntal 
analysis. 
[5] MRI 
and 
Geno 
mics 
ADNI Develop 
ed an 
interpret 
able 
generati 
ve 
multimo 
dal 
framewo 
rk 
combini 
ng 
neuroim 
aging 
Enhance 
d 
understan 
ding of 
AD by 
integratin 
g 
multimod 
al data 
with 
interpreta 
bility. Complex 
ity in 
integratin 
g diverse 
data 
types and 
ensuring 
interpreta 
bility. Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:43:40 UTC from IEEE Xplore. Restrictions apply. 2025 International Conference on Sustainability, Innovation & Technology (ICSIT ) 
 
979-8-3315-3549-0/25/$31.00 ©2025 IEEE 
 
and 
genomic 
s for AD 
decoding 
. IV.

**Passage 12:**

> iewe 
d AI 
applicati 
ons in 
brain 
MRI 
analysis 
for AD, 
focusing 
on deep 
learning 
approach 
es. Provided 
a 
compreh 
ensive 
evaluatio 
n of AI 
methodol 
ogies in 
MRI-
based 
AD 
analysis. Lacked 
experime 
ntal 
validatio 
n of 
discussed 
methods. 
[3] MRI Multipl 
e 
cohorts 
Systemat 
ically 
reviewed 
AI 
applicati 
ons in 
neuroim 
aging for 
dementia 
diagnosi 
s and 
prognosi 
s. Offered 
insights 
into the 
integratio 
n of AI in 
clinical 
settings 
for 
dementia 
care. Did not 
focus 
exclusive 
ly on 
MRI 
modalitie 
s. 
[4] MRI Biblio 
metric 
data 
Conduct 
ed a 
bibliome 
tric 
analysis 
on AI 
applicati 
ons in 
early AD 
diagnosi 
s and 
monitori 
ng. Identified 
research 
trends 
and gaps 
in AI-
based 
AD 
diagnosti 
cs.

**Passage 13:**

> t (over 85%), more 
powerful augmentations are used to add more diversi ty to the 
training data. When accuracy falls too low, augmentation power 
is decreased in order to preserve training stability. This method 
provides an active balance between discriminator an d 
generator, resulting in more effective and stable training, which 
is paramount for improving the capability of CT-GAN  to 
integrate multimodal neuroimaging data for AD detection. Model Design 
In this cross-modal Transformer GAN model design, t he 
Generator of the CT-GAN employs transposed convolut ional 
layers, or deconvolution layers, to iteratively exp and an array 
of noise to the size of a 128×128×3 image. It starts from a low-
dimensional latent space, restoring it to a higher one. Every 
sampling layer increases the size of the image and improves its 
structure.

**Passage 14:**

> as ef fectively as 
CT-GAN. The ROC curve comparison firmly positions C T-
GAN in the lead, followed by WGAN and Pix2Pix, whic h 
perform decently but not with the same classification accuracy. VIII. C
ONCLUSION  
In brief, the CT-GAN model has achieved better perf ormance 
in key evaluation measures like F1-score, AUC, reca ll, 
accuracy, and precision compared to traditional gen erative 
models like DCGAN, WGAN, CGAN, Pix2Pix, CycleGAN, 
and VAE-GAN when it comes to identifying dementia. The 
ability of the model to map functionally and structurally perfect 
incorporation through a bi-attention mechanism enab les it to 
capture both spatial and the intricate operations o f the brain, 
making it appropriate for use in sophisticated appl ications in 
medicine.

**Passage 15:**

> over ph ases and 
anatomical variations. In addition, the models can denoise data 
and improve image quality, reducing the difficulty of detecting 
early illness biomarkers by clinicians and machines. The ability 
of generative AI to mimic disease progression provi des new 
avenues for the training of diagnostic models such that 
researchers and clinicians can observe the temporal progression 
of Alzheimer's from its beginning to late stages. Apart from data 
augmentation, generative AI also addresses major practical and 
ethical challenges of Alzheimer's research.

**Passage 16:**

> on, 
91% recall, and 90% F1-score are remarkable, the CT -GAN 
demonstrates its ability to generate high-quality a nd accurate 
images while effectively distinguishing between rea l and fake 
samples. This performance is especially noteworthy when 
considering its specialized application in Alzheime r's Disease 
(AD) detection, where combining Dispersion Tensor M apping 
and functional MRI through the bi-attention mechani sm 
significantly enhances its capability to model both  the brain's 
functioning and anatomical components. In compariso n, 
DCGAN achieves a solid performance with an accuracy  of 
85%, but it is less capable in terms of recall (87%) and precision 
(83%) when compared to CT-GAN.

**Passage 17:**

> tivation function, which norm alizes the 
output pixel values to the range between 0 and 1, t hus making 
the generated image have normalized pixel values fo r 
visualization or additional processing. The Discrim inator in 
CT-GAN consists of a sequence of convolutional laye rs with 
strides 2, which downsamples the spatial dimensions  of the 
input image. This helps the model focus on high-lev el features 
and ignore other unnecessary details. Leaky ReLU ac tivation 
functions take the place of regular ReLU and give n egative 
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:43:40 UTC from IEEE Xplore. Restrictions apply. 2025 International Conference on Sustainability, Innovation & Technology (ICSIT ) 
 
979-8-3315-3549-0/25/$31.00 ©2025 IEEE 
 
inputs a small, non-zero gradient.

**Passage 18:**

> others do well for typical image generation tasks, CT-GAN's 
advanced architecture for multi-modal data integration makes it 
the better option for intricate medical application s like AD 
detection. Its capacity to balance precision and recall, as well as 
its relatively higher accuracy and F1-score, makes it the better 
model for tasks that involve both quality image cre ation and 
classification accuracy. Additionally, a deeper analysis of the confusion ma trix and 
ROC curve metrics was performed to highlight the mo del's 
strengths in minimizing false positives and false negatives. Figure 1 Proposed Model Performance 
 
Model Accurac 
y 
CT-GAN 
(Proposed 
Model) 
90% 
DCGAN 85% 
WGAN 88% 
CGAN 84% 
VAE-
GAN 80% 
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:43:40 UTC from IEEE Xplore. Restrictions apply.

**Passage 19:**

> identiality of the patients. Variational auto encoders 
(VAEs) and Generative Adversarial Networks (GANs) a re just 
a few instances of novel AI models. have revolutionary promise 
in medical imaging. High-quality synthesized MRI im ages can 
be produced through generative AI algorithms. augme nting 
current datasets, and global optimization of diagno stic 
algorithm training, in Alzheimer's disease, where g lobal minor 
alterations in brain structure are crucial for earl y detection, 
generative AI enhances diagnostic accuracy by provi ding 
global variability in presentations of data over ph ases and 
anatomical variations. In addition, the models can denoise data 
and improve image quality, reducing the difficulty of detecting 
early illness biomarkers by clinicians and machines.

**Passage 20:**

> 91%), F1-score (90%), and an amazing  AUC of 
0.95. They show that CT-GAN can make high-quality fake data 
without hurting its ability to classify things well, with few false 
positives and negatives. It works well in high-risk  medical 
settings because it has a better balance between pr ecision and 
recall. The results show that professional designs like CT-GAN 
are very important for working with complicated mul ti-modal 
data. They also show that CT-GAN could be a useful tool for 
analyzing and diagnosing medical images, not just f or AD 
diagnosis. Keywords:  CT-GAN, Alzheimer's Disease detection, multi-
modal data fusion, functional MRI, Diffusion Tensor  Imaging, 
bi-attention mechanism, generative models, image ge neration, 
precision, recall, accuracy, F1-score, Area Under t he Curve 
(AUC) . I.

**Passage 21:**

> ation & Technology (ICSIT ) 
 
979-8-3315-3549-0/25/$31.00 ©2025 IEEE 
 
 
Where, 
TP=True Positive. FN=False Negative. False Positive Rate: 
 
Where, 
FP=False Positive. TN=True Negative. V. VI. VII. R
ESULTS AND DISCUSSION  
Model Accuracy Precision Recall F1-
Score 
CT-GAN 
(Proposed 
Model) 
90% 89% 91% 90% 
DCGAN 85% 83% 87% 85% 
WGAN 88% 86% 89% 87% 
CGAN 84% 82% 86% 84% 
VAE-GAN 80% 79% 82% 80% 
Pix2Pix 87% 84% 88% 86% 
CycleGAN 83% 81% 85% 83% 
 
The table highlights the exceptional performance of  your CT-
GAN model across key evaluation evaluations—F1-scor e, 
recall, accuracy, and precision. 90% accuracy, 89%  precision, 
91% recall, and 90% F1-score are remarkable, the CT -GAN 
demonstrates its ability to generate high-quality a nd accurate 
images while effectively distinguishing between rea l and fake 
samples.

**Passage 22:**

> the temporal progression 
of Alzheimer's from its beginning to late stages. Apart from data 
augmentation, generative AI also addresses major practical and 
ethical challenges of Alzheimer's research. AI-gene rated 
synthetic datasets don't have clear patient identities, so they can 
CT-GAN: A Cross-Modal Transformer GAN for Superior 
Multi-Modal MRI-Based Alzheimer’s Disease Detection 
 
  
Rushabh Patole 
1                                    
Department of Computer Technology  
Yeshwantrao Chavan College of Engineering, Nagpur, India.     
rushabhpatole.9@gmail.com  
 
Dr.

**Passage 23:**

> the two classes accurately. W hen 
compared to other models, CT-GAN outperforms DCGAN 
(AUC 0.91), WGAN (AUC 0.93), CGAN (AUC 0.88), VAE-
GAN (AUC 0.84), Pix2Pix (AUC 0.92), and CycleGAN (AUC 
0.86). These models have good AUC scores, but CT-GA N is 
better at balancing the Because it has a high true positive rate 
and a low false positive rate, it is the most relia ble model for 
classification jobs. The fact that it has a higher AUC not only 
shows that it can accurately classify things, but i t also sets it 
apart from the other models, making CT-GAN the best  choice 
in this comparison. The CT-GAN model is clearly better for the 
job of AD detection, which is a niche application that combines 
data from different sources. This is shown by all t he measures 
of Recall, accuracy, precision, and F1-score of the  different 
generative models.

**Passage 24:**

> E 
 
  
 
The table of ROC curves for the CT-GAN model, along with its 
remarkable capacity to differentiate among positive  and 
negative classes is shown by its area under the cur ve (AUC) of 
0.95. The model is quite successful in accurately classifying 
positive cases while reducing false positives accor ding to the 
AUC value, resulting in a robust performance. The c urve itself 
illustrates an excellent proportion of true positiv es and a low 
number of false positives, confirming the model's c apacity to 
differentiate between the two classes accurately. W hen 
compared to other models, CT-GAN outperforms DCGAN 
(AUC 0.91), WGAN (AUC 0.93), CGAN (AUC 0.88), VAE-
GAN (AUC 0.84), Pix2Pix (AUC 0.92), and CycleGAN (AUC 
0.86).

</details>

---

## Deep-Learning-in-Smart-Healthcare--A-GAN-based-Approach-f_2024_Procedia-Comp
_File: `Deep-Learning-in-Smart-Healthcare--A-GAN-based-Approach-f_2024_Procedia-Comp.pdf`_

1. **Was diffusion MRI (DTI, dMRI, DWI, or similar) used in this paper?**  
   Yes. The paper explicitly mentions "diffusion-weighted imaging (DWI) and diffusion tensor imaging (DTI)" as applied to detect diffusion-related phenomena [20].

---

2. **What processing steps were applied to the diffusion images?**  
   The following steps are explicitly stated:  
   - Preprocessing MRI images for normalization and smoothing to remove anomalies.  
   - Dividing the MRI image into black and white pixels.  
   - Using a CNN to extract features for classification.  
   - Data augmentation using GANs.  

---

3. **What software or tools are explicitly named for processing?**  
   - Generative Adversarial Networks (GANs) [8].  
   - Convolutional Neural Networks (CNNs).  
   - The Alzheimer’s Disease Neuroimaging Initiative (ADNI) dataset [7].  

---

4. **What acquisition or processing parameters are explicitly reported?**  
   - The dataset source is the ADNI dataset [7].  
   - No specific parameters (e.g., b-values, number of directions, voxel size) are reported.  

---

5. **Copy the exact sentences from the excerpts that describe the processing.**  
   - "We take magnetic resonance imaging (MRI) from a scanner and then preprocess the image for normalization and smoothing to remove anomalies. Afterwards, we divide the MRI image into black and white pixels. Our CNN will extract the features from the image to classify dementia into four categories..."  
   - "This hybrid model employs three types of data pre-processing: Image Filtering, data normalization, and data augmentation."  
   - "The presented research introduces a novel Generative Adversarial Network (GAN) architecture [22], comprising a discriminator, a generator, and their combined network."  

---

6. **Is the processing description complete, or does it appear incomplete/missing?**  
   The processing description appears **incomplete**. While general MRI preprocessing steps (normalization, smoothing, pixel division) and GAN-based augmentation are described, no specific diffusion MRI processing steps (e.g., diffusion tensor calculation, b-values, or directional analysis) are detailed. The focus is on standard MRI and CNN-based classification, not diffusion-specific techniques.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> n.d. [Online]. Available: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7924338/
[19] A. W. Toga and J. C. Mazziotta, Brain Atlases and Their Applications. Academic Press, 2000.
[20] D. Le Bihan and H. Johansen-Berg, Diffusion Tensor Imaging: Concepts and Applications. Oxford University Press, 2010.
[21] W. W. Kuo, C. T. Lin, C. C. Chen, M. H. Wu, and M. L. Lee, “A support vector machine-based approach for diagnosis of alzheimer’s disease
using pet/fdg images,”IEEE Transactions on Medical Imaging, vol. 33, pp. 96–101, 2014.
[22] H. H. N. Alrashedy, A. F. Almansour, D. M. Ibrahim, and M. A. A. Hammoudeh, “Braingan: Brain mri image generation and classification
framework using gan architectures and cnn models,” Sensors, vol. 22, no. 11, p. 4297, 2022.

**Passage 2:**

> n.d. [Online]. Available: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7924338/
[19] A. W. Toga and J. C. Mazziotta, Brain Atlases and Their Applications. Academic Press, 2000.
[20] D. Le Bihan and H. Johansen-Berg, Diffusion Tensor Imaging: Concepts and Applications. Oxford University Press, 2010.
[21] W. W. Kuo, C. T. Lin, C. C. Chen, M. H. Wu, and M. L. Lee, “A support vector machine-based approach for diagnosis of alzheimer’s disease
using pet/fdg images,”IEEE Transactions on Medical Imaging, vol. 33, pp. 96–101, 2014.
[22] H. H. N. Alrashedy, A. F. Almansour, D. M. Ibrahim, and M. A. A. Hammoudeh, “Braingan: Brain mri image generation and classification
framework using gan architectures and cnn models,” Sensors, vol. 22, no. 11, p. 4297, 2022. Hina Tufail  et al. / Procedia Computer Science 241 (2024) 146–153 153
H.

**Passage 3:**

> hted (T2-w) scans, with FLAIR being the third frequently used sequence
[19]. Diffusion-weighted imaging (DWI) and diffusion tensor imaging (DTI) are applied to detect diffusion-related
phenomena [20]. Studies often involve the use of various image modalities, including structural magnetic resonance
imaging (sMRI), fluorodeoxyglucose-positron emission tomography (FDG-PET), single-photon emission computed
tomography (SPECT), diffusion tensor imaging (DTI), and arterial spin labeling combined with DTI datasets (ASL
+ DTI) [9]. Different image modalities allow observers to detect certain phenomena that may not be visible in other
modalities [9]. According to their study, the authors mainly used structural magnetic resonance imaging (SMRI),
focusing on T1-weighted (T1-W) images [15].

**Passage 4:**

> sion recovery (FLAIR) imaging [19]. The most commonly used sequences in medical imag-
ing are T1-weighted (T1-w) and T2-weighted (T2-w) scans, with FLAIR being the third frequently used sequence
[19]. Diffusion-weighted imaging (DWI) and diffusion tensor imaging (DTI) are applied to detect diffusion-related
phenomena [20]. Studies often involve the use of various image modalities, including structural magnetic resonance
imaging (sMRI), fluorodeoxyglucose-positron emission tomography (FDG-PET), single-photon emission computed
tomography (SPECT), diffusion tensor imaging (DTI), and arterial spin labeling combined with DTI datasets (ASL
+ DTI) [9]. Different image modalities allow observers to detect certain phenomena that may not be visible in other
modalities [9].

**Passage 5:**

> assify the disease into the four stages
mentioned previously. We take magnetic resonance imaging (MRI) from a scanner and then preprocess the image for
normalization and smoothing to remove anomalies. Afterwards, we divide the MRI image into black and white pixels. Our CNN will extract the features from the image to classify dementia into four categories: early stage, moderate
stage, advanced stage, and Last Stage. The Dataset of Alzheimer’s Disease Neuroimaging Initiative (ADNI) [7] has
been used for this proposed research. Further, this paper is also applying GAN [8] to solve the issue of a highly
unbalanced dataset of Alzheimer’s. 148 Hina Tufail  et al. / Procedia Computer Science 241 (2024) 146–153
H. Tufail et al. / Procedia Computer Science 00 (2019) 000–000 3
2.

**Passage 6:**

> ng (DTI), and arterial spin labeling combined with DTI datasets (ASL
+ DTI) [9]. Different image modalities allow observers to detect certain phenomena that may not be visible in other
modalities [9]. According to their study, the authors mainly used structural magnetic resonance imaging (SMRI),
focusing on T1-weighted (T1-W) images [15]. SMRI has proven effective in diagnostic applications by clearly delin-
eating the contrasting characteristics of healthy and pathological soft tissues within organs [16]. The dataset in this
work was sourced from the PET (positron emission tomography) database [21]. The study identified support vector
machines (SVM) as the most effective classifier, achieving an accuracy rate of 90.91% [21].

**Passage 7:**

> burden of alzheimer’s disease,” Alzheimer’s &
Dementia, vol. 3, no. 3, pp. 186–191, 2007.
[6] S. Gauthier, B. Reisberg, M. Zaudig, R. C. Petersen, K. Ritchie, K. Broich, S. Belleville, H. Brodaty, D. Bennett, H. Chertkow et al., “Mild
cognitive impairment,” The Lancet, vol. 367, no. 9518, pp. 1262–1270, 2006.
[7] C. R. Jack Jr, M. A. Bernstein, N. C. Fox, P . Thompson, G. Alexander, D. Harvey, B. Borowski, P . J. Britson, J. L. Whitwell, C. Ward et al.,
“The alzheimer’s disease neuroimaging initiative (adni): Mri methods,” Journal of Magnetic Resonance Imaging: An Official Journal of the
International Society for Magnetic Resonance in Medicine, vol. 27, no. 4, pp. 685–691, 2008.
[8] I. Goodfellow, J. Pouget-Abadie, M. Mirza, B. Xu, D. Warde-Farley, S. Ozair, A. Courville, and Y . Bengio, “Generative adversarial networks,”
arXiv preprint arXiv:1406.2661, 2014.
[9] A.

**Passage 8:**

> burden of alzheimer’s disease,” Alzheimer’s &
Dementia, vol. 3, no. 3, pp. 186–191, 2007.
[6] S. Gauthier, B. Reisberg, M. Zaudig, R. C. Petersen, K. Ritchie, K. Broich, S. Belleville, H. Brodaty, D. Bennett, H. Chertkow et al., “Mild
cognitive impairment,” The Lancet, vol. 367, no. 9518, pp. 1262–1270, 2006.
[7] C. R. Jack Jr, M. A. Bernstein, N. C. Fox, P . Thompson, G. Alexander, D. Harvey, B. Borowski, P . J. Britson, J. L. Whitwell, C. Ward et al.,
“The alzheimer’s disease neuroimaging initiative (adni): Mri methods,” Journal of Magnetic Resonance Imaging: An Official Journal of the
International Society for Magnetic Resonance in Medicine, vol. 27, no. 4, pp. 685–691, 2008.
[8] I. Goodfellow, J. Pouget-Abadie, M. Mirza, B. Xu, D. Warde-Farley, S. Ozair, A. Courville, and Y . Bengio, “Generative adversarial networks,”
arXiv preprint arXiv:1406.2661, 2014.
[9] A.

**Passage 9:**

> ssion com-
puted tomography (SPECT) is another technique, using gamma rays emission from a radiopharmaceutical to create
three-dimensional images of the brain’s internal structures and functions [18]. MRI is currently utilized to examine
brain morphology [19], with several sequences available, such as T1-weighted imaging, T2-weighted imaging, and
fluid-attenuated inversion recovery (FLAIR) imaging [19]. The most commonly used sequences in medical imag-
ing are T1-weighted (T1-w) and T2-weighted (T2-w) scans, with FLAIR being the third frequently used sequence
[19]. Diffusion-weighted imaging (DWI) and diffusion tensor imaging (DTI) are applied to detect diffusion-related
phenomena [20].

**Passage 10:**

> [14]. The methodologies for dementia diagnosis vary and include axial tomography (CT) [15], structural imaging using
magnetic resonance imaging (MRI) [16], and positron emission tomography (PET) [17]. Single-photon emission com-
puted tomography (SPECT) is another technique, using gamma rays emission from a radiopharmaceutical to create
three-dimensional images of the brain’s internal structures and functions [18]. MRI is currently utilized to examine
brain morphology [19], with several sequences available, such as T1-weighted imaging, T2-weighted imaging, and
fluid-attenuated inversion recovery (FLAIR) imaging [19]. The most commonly used sequences in medical imag-
ing are T1-weighted (T1-w) and T2-weighted (T2-w) scans, with FLAIR being the third frequently used sequence
[19].

**Passage 11:**

> et Details
The Alzheimer’s Disease Neuroimaging Initiative (ADNI) [7] is a longitudinal multi-site observational research
of older people with normal cognition, mild cognitive impairment (MCI), or AD. The National Institutes of Health
(NIH) and industry support it jointly through the NIH Foundation. The purpose of this research is to compare the effec-
tiveness of using information obtained from magnetic resonance imaging (MRI), fludeoxyglucose positron emission
tomography (18F) (FDG PET), urine, serum, and cerebrospinal fluid (CSF) biomarkers, as well as clinical and neuro
psychometric assessments, to track disease progression in the three groups mentioned above of the elderly people.

**Passage 12:**

> n phenomena that may not be visible in other
modalities [9]. According to their study, the authors mainly used structural magnetic resonance imaging (SMRI),
focusing on T1-weighted (T1-W) images [15]. SMRI has proven effective in diagnostic applications by clearly delin-
eating the contrasting characteristics of healthy and pathological soft tissues within organs [16]. The dataset in this
work was sourced from the PET (positron emission tomography) database [21]. The study identified support vector
machines (SVM) as the most effective classifier, achieving an accuracy rate of 90.91% [21]. However, a limitation
of this study is its focus solely on the binary categorization of Alzheimer’s disease (AD), neglecting the potential for
multi-classification of Alzheimer’s disease [21]. 3.

**Passage 13:**

> assify the disease into the four stages
mentioned previously. We take magnetic resonance imaging (MRI) from a scanner and then preprocess the image for
normalization and smoothing to remove anomalies. Afterwards, we divide the MRI image into black and white pixels. Our CNN will extract the features from the image to classify dementia into four categories: early stage, moderate
stage, advanced stage, and Last Stage. The Dataset of Alzheimer’s Disease Neuroimaging Initiative (ADNI) [7] has
been used for this proposed research. Further, this paper is also applying GAN [8] to solve the issue of a highly
unbalanced dataset of Alzheimer’s.

**Passage 14:**

> exploring additional metrics are
recommended.
(a)
 (b)
Fig. 3. Model evaluation: (a) Before data augmentation; (b) After data augmentation. Table 2. Result metrics before and after data augmentation. Before data augmentation After data augmentation
precision recall F1-score support precision recall F1-score support
normal 0.62 0.83 0.71 640 0.71 0.83 0.77 640
very-mild 0.55 0.48 0.51 448 0.66 0.58 0.62 448
mild 0.62 0.12 0.20 179 0.60 0.45 0.51 179
moderate 0.00 0.00 0.00 12 0.36 0.33 0.35 12
5. Conclusion
The study effectively illustrates the potential of generative adversarial networks (GANs) in conjunction with trans-
fer learning-based convolutional neural network (CNN) models for classifying Alzheimer’s disease (AD) stages from
magnetic resonance imaging (MRI) data.

**Passage 15:**

> tting-edge machine learning methods to address major obstacles in medical image interpretation. Future research
on AD should explore advanced machine-learning techniques and integrative data analysis. Experimenting with deep
8 H. Tufail et al. /Procedia Computer Science 00 (2019) 000–000
learning architectures like ResNet, DenseNet, and EfficientNet can improve feature extraction and classification accu-
racy. Integrating multi-modal data sources like PET scans, biomarkers, and genetic information can provide a holistic
view of the disease. Longitudinal data monitoring and federated learning can enhance personalized medicine and
collaborative research. Acknowledgements
This work is funded by FCT/MEC through national funds and, when applicable, co-funded by the FEDER-PT2020
partnership agreement under the project UIDB/50008/2020.

**Passage 16:**

> tting-edge machine learning methods to address major obstacles in medical image interpretation. Future research
on AD should explore advanced machine-learning techniques and integrative data analysis. Experimenting with deep
8 H. Tufail et al. /Procedia Computer Science 00 (2019) 000–000
learning architectures like ResNet, DenseNet, and EfficientNet can improve feature extraction and classification accu-
racy. Integrating multi-modal data sources like PET scans, biomarkers, and genetic information can provide a holistic
view of the disease. Longitudinal data monitoring and federated learning can enhance personalized medicine and
collaborative research. Acknowledgements
This work is funded by FCT/MEC through national funds and, when applicable, co-funded by the FEDER-PT2020
partnership agreement under the project UIDB/50008/2020.

**Passage 17:**

> f the proposed model. Addi-
tionally, we conduct a comparative analysis with existing models to demonstrate the efficacy of our approach. A B
CD
Fig. 1. Block Diagram of the proposed methodology. 3.1. Dataset Details
The Alzheimer’s Disease Neuroimaging Initiative (ADNI) [7] is a longitudinal multi-site observational research
of older people with normal cognition, mild cognitive impairment (MCI), or AD. The National Institutes of Health
(NIH) and industry support it jointly through the NIH Foundation. The purpose of this research is to compare the effec-
tiveness of using information obtained from magnetic resonance imaging (MRI), fludeoxyglucose positron emission
tomography (18F) (FDG PET), urine, serum, and cerebrospinal fluid (CSF) biomarkers, as well as clinical and neuro
psychometric assessments, to track disease progression in the three groups mentioned above of the elderly people.

**Passage 18:**

> the effectiveness of training and testing the entire proposed
research model. This hybrid model employs three types of data pre-processing: Image Filtering, data normalization,
and data augmentation. Figure 1, in the rectangle A, illustrates the sequence of these pre-processing techniques. 3.3. Data Augmentation using Generative Adversarial Networks (GANs)
The presented research introduces a novel Generative Adversarial Network (GAN) architecture [22], comprising a
discriminator, a generator, and their combined network. Each model is meticulously designed to accomplish specific
tasks to generate realistic MRI images of Alzheimer’s disease. The models’ architectures are outlined below, providing
a detailed insight into their layers and parameters. The discriminator employs a sequence of convolutional and dense layers interleaved with leaky rectified linear
unit (LeakyReLU) activations.

**Passage 19:**

> the effectiveness of training and testing the entire proposed
research model. This hybrid model employs three types of data pre-processing: Image Filtering, data normalization,
and data augmentation. Figure 1, in the rectangle A, illustrates the sequence of these pre-processing techniques. 3.3. Data Augmentation using Generative Adversarial Networks (GANs)
The presented research introduces a novel Generative Adversarial Network (GAN) architecture [22], comprising a
discriminator, a generator, and their combined network. Each model is meticulously designed to accomplish specific
tasks to generate realistic MRI images of Alzheimer’s disease. The models’ architectures are outlined below, providing
a detailed insight into their layers and parameters. The discriminator employs a sequence of convolutional and dense layers interleaved with leaky rectified linear
unit (LeakyReLU) activations.

**Passage 20:**

> ScienceDirect
Available online at www.sciencedirect.com
Procedia Computer Science 241 (2024) 146–153
1877-0509 © 2024 The Authors. Published by Elsevier B.V .

**Passage 21:**

> from MRI
images. However, training the hybrid model in our Microsoft Windows environment takes approximately 10 to 12
hours. This part of the algorithm is presented in Figure 1, in the rectangle D. 4. Experimentation and Results
Different evaluation metrics can be used to prove the proposed system’s performance. The classification algorithm
divides the data into four categories: True positive (TP) for the correctly classified true labels, True negative (TN)
for correctly classified false labels, False positive (FP) for the incorrectly classified false labels, and False negative
(FN) incorrectly classified true labels. Precision, recall, F1-score, and support are metrics used in machine learning to
evaluate the performance of classification models. Precision measures the accuracy of positive predictions, indicating
how many predicted items are positive.

**Passage 22:**

> from MRI
images. However, training the hybrid model in our Microsoft Windows environment takes approximately 10 to 12
hours. This part of the algorithm is presented in Figure 1, in the rectangle D. 4. Experimentation and Results
Different evaluation metrics can be used to prove the proposed system’s performance. The classification algorithm
divides the data into four categories: True positive (TP) for the correctly classified true labels, True negative (TN)
for correctly classified false labels, False positive (FP) for the incorrectly classified false labels, and False negative
(FN) incorrectly classified true labels. Precision, recall, F1-score, and support are metrics used in machine learning to
evaluate the performance of classification models. Precision measures the accuracy of positive predictions, indicating
how many predicted items are positive.

**Passage 23:**

> 00–000
C: In this phase, we construct a hybrid model by integrating the InceptionV3 model with a tuned CNN model for
Alzheimer’s detection. The image dataset is then split into training and test sets. The model undergoes training
and validation using appropriate images. D: The effectiveness of our hybrid model is assessed by evaluating its accuracy. Performance metrics such as accu-
racy, precision, recall, f1 score, and confusion matrix are employed in this stage of the proposed model. Addi-
tionally, we conduct a comparative analysis with existing models to demonstrate the efficacy of our approach. A B
CD
Fig. 1. Block Diagram of the proposed methodology. 3.1. Dataset Details
The Alzheimer’s Disease Neuroimaging Initiative (ADNI) [7] is a longitudinal multi-site observational research
of older people with normal cognition, mild cognitive impairment (MCI), or AD.

**Passage 24:**

> tuning parameters, addressing class imbalances, and exploring additional metrics are
recommended.
(a)
 (b)
Fig. 3. Model evaluation: (a) Before data augmentation; (b) After data augmentation. Table 2. Result metrics before and after data augmentation. Before data augmentation After data augmentation
precision recall F1-score support precision recall F1-score support
normal 0.62 0.83 0.71 640 0.71 0.83 0.77 640
very-mild 0.55 0.48 0.51 448 0.66 0.58 0.62 448
mild 0.62 0.12 0.20 179 0.60 0.45 0.51 179
moderate 0.00 0.00 0.00 12 0.36 0.33 0.35 12
5. Conclusion
The study effectively illustrates the potential of generative adversarial networks (GANs) in conjunction with trans-
fer learning-based convolutional neural network (CNN) models for classifying Alzheimer’s disease (AD) stages from
magnetic resonance imaging (MRI) data.

</details>

---

## Esteve et al. (2025) — topoEEG An Python-framework for analyzing EEG data in neurodegeneratives disease through Topologica
_File: `Esteve et al. - 2025 - topoEEG An Python-framework for analyzing EEG data in neurodegeneratives disease through Topologica.pdf`_

1. **Was diffusion MRI (DTI, dMRI, DWI, or similar) used in this paper?**  
   **NO DIFFUSION MRI PROCESSING FOUND**  

2. **What processing steps were applied to the diffusion images?**  
   Not applicable (no diffusion MRI processing reported).  

3. **What software or tools are explicitly named for processing?**  
   Not applicable (no diffusion MRI processing reported).  

4. **What acquisition or processing parameters are explicitly reported?**  
   Not applicable (no diffusion MRI processing reported).  

5. **Copy the exact sentences from the excerpts that describe the processing.**  
   Not applicable (no diffusion MRI processing reported).  

6. **Is the processing description complete, or does it appear incomplete/missing?**  
   **NO DIFFUSION MRI PROCESSING FOUND** (processing described pertains to EEG, not diffusion MRI).

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> rchitecture
The architecture of topoEEG is designed for both flexibility and ef-
ficiency, integrating various components that work together to provide 
a comprehensive neuroimaging analysis pipeline. It is built on top of 
well-established libraries like MNE-Python and TensorFlow, while also 
incorporating novel topological methods through TDL. As illustrated in Fig. 1, the topoEEG software can be divided into 
several key components:
SoftwareX 31 (2025) 102222 
2 
M. Esteve et al. Fig. 1. Overview of the topoEEG software architecture. A. The key modules and their interconnections. B. Detailed workflow of EEG data processing and analysis.
• EEG Data Preprocessing: This module handles raw EEG data, in-
cluding artifact removal and cleaning using Independent Compo-
nent Analysis (ICA).

**Passage 2:**

> er standalone tools, it provides a unified solution, en-
hancing the accessibility of sophisticated analytics and supporting research in the diagnosis and understanding 
of neurodegenerative diseases. Code metadata
 Current code version v01  
 Permanent link to code/repository used for this code version https://github.com/ElsevierSoftwareX/SOFTX-D-25-00134  
 Legal Code License MIT License  
 Code versioning system used git  
 Software code languages, tools, and services used Python  
 Compilation requirements, operating environments & dependencies pandas, numpy, matplotlib, scipy, scikit-learn, persim, ripser, gudhi, giotto-tda, mne, 
concurrent.futures, torch, tensorflow, imbalanced-learn
 
 If available Link to developer documentation/manual https://github.com/MiriamEsteve/topoEEG  
 Support email for questions miriam.estevecampello@uchceu.es  
1.

**Passage 3:**

> d connectivity studies [15]. FieldTrip, on the other hand, excels in 
time–frequency analysis and non-parametric statistical testing, mak-
ing it invaluable for investigating neural oscillations [16]. SPM pro-
vides advanced statistical modeling tools, often used in functional and 
structural MRI studies to detect regional brain activity changes [17]. FSL specializes in diffusion imaging and tractography, offering essen-
tial tools for studying white matter connectivity [18]. Additionally,
EEGLAB stands out for its user-friendly interface and extensive library 
of plugins for preprocessing and analyzing EEG data [19]. MNE-Python
integrates seamlessly with OpenNeuro data, providing comprehensive 
tools for source estimation and functional connectivity analysis [20].

**Passage 4:**

> environments. Researchers can now automate preprocessing and feature extraction, 
leading to faster, more reproducible analyses, while clinicians can more 
easily identify early biomarkers of disease. This streamlining of the 
analysis process has led to more efficient workflows and improved 
collaboration across multidisciplinary teams, ultimately accelerating 
the pace of neuroimaging research. The software is already being used in various academic and clinical 
settings, with a growing number of publications demonstrating its 
effectiveness in the study of neurodegenerative diseases. topoEEG has 
been downloaded over 8000 times and cited in more than 20 research 
articles, highlighting its impact and adoption within the neuroscience 
community.

**Passage 5:**

> erasti E, Annunziato M. Topological data 
analysis for neuroscience. Front Comput Neurosci 2020;14(49).
[45] Gunter MW, Müller T, Ziegelmann D. Machine learning for neuroimaging: A 
systematic review. Neuroinformatics 2020;18(3):295–320.
[46] Severi M, Ricci L, Rossi F. A comprehensive review of deep learning methods 
for EEG analysis. J Neurosci Methods 2023;384:109054.
[47] Carlsson G. Topology and data. Bull Am Math Soc 2009;46(2):255–308.
[48] Reininghaus J, Huber S, Bauer U, Kwitt R. A stable multi-scale kernel for 
topological machine learning. Adv Neural Inf Process Syst 2015;28. SoftwareX 31 (2025) 102222 
10

**Passage 6:**

> ton KJ. Statistical parametric mapping: A novel approach to neuroimaging. Hum Brain Mapp 1994;1:210–30.
[18] Smith SM. Advances in functional magnetic resonance imaging with diffusion 
tensor imaging. Magn Reson Imaging 2004;22:93–102.
[19] Delorme A. EEGLAB: An open-source toolbox for analysis of EEG and MEG data. J Neurosci Methods 2004;134:9–21.
[20] Gramfort A. MNE-Python: A comprehensive open-source tool for EEG/MEG 
analysis. NeuroImage 2014;86:546–58.
[21] Kachare A, et al. Neural network-based techniques for detecting Alzheimer’s 
disease from EEG signals. J Neurosci Methods 2024;289:123–34.
[22] Alessandrini M, Biagetti G, Crippa P, Falaschetti L, Luzzi S, Turchetti C. EEG-based Alzheimer’s disease recognition using robust-PCA and LSTM re-
current neural network.

**Passage 7:**

> andon ML, Rodriguez C. MNE: A software package for pro-
cessing magnetoencephalography and electroencephalography data. NeuroImage 
2020;207:116355.
[38] Oostenveld R, Fries P, Maris E, Schoffelen JM. FieldTrip: Open source software 
for advanced analysis of MEG, EEG, and invasive electrophysiological data. Comput Intell Neurosci 2011;2011:156869.
[39] Zhang X, Zhao H, Wang J, Li Y. Topological data analysis in neuroscience: 
Methods and applications. J Comput Neurosci 2021;49(2):223–39.
[40] Yu Haitao, Lei Xinyu, Song Zhenxi, Liu Chen, Wang Jiang. Supervised network-
based fuzzy learning of EEG signals for Alzheimer’s disease identification. IEEE Trans Fuzzy Syst 2020;28(1):60–71. http://dx.doi.org/10.1109/TFUZZ. 2019.2903753.
[41] Zhang X, Zhao H, Wang J, Li Y. Spatiotemporal dynamics of periodic and 
aperiodic brain activity under peripheral nerve stimulation with acupuncture.

**Passage 8:**

> n brain 
networks. FieldTrip Known for 
time–frequency analysis 
and statistical testing
topoEEG adds topological 
methods to this analysis, helping 
to detect hidden patterns in 
neural oscillations. SPM Focuses on statistical 
modeling for fMRI
topoEEG enhances statistical 
models by integrating topological 
feature extraction, leading to 
improved network analysis. FSL Specializes in diffusion 
imaging and 
tractography
topoEEG applies TDA to better 
interpret white matter 
connectivity, uncovering more 
detailed structural patterns. EEGLAB A major tool for EEG 
preprocessing and 
analysis
topoEEG introduces TDA-based 
feature extraction, improving 
high-dimensional data analysis for 
better diagnostics. MNE-Python Provides comprehensive 
EEG/MEG tools
topoEEG extends its capabilities 
by leveraging TDA to analyze 
complex topological changes in 
brain networks.
 
progression [11,12].

**Passage 9:**

> eceived 28 February 2025; Received in revised form 19 May 2025; Accepted 28 May 2025
SoftwareX 31 (2025) 102222 
Available online 21 June 2025 
2352-7110/© 2025 The Authors. Published by Elsevier B.V. This is an open access article under the CC BY-NC license ( http://creativecommons.org/licenses/by- 
nc/4.0/ ). M. Esteve et al. Table 1
Comparison of existing neuroimaging frameworks and the features of the proposed framework. Framework Core Capabilities topoEEG Highlights  
 Brainstorm Primarily used for 
MEG/EEG source 
localization
topoEEG improves connectivity 
analysis by incorporating TDA, 
which helps reveal deeper 
topological structures in brain 
networks. FieldTrip Known for 
time–frequency analysis 
and statistical testing
topoEEG adds topological 
methods to this analysis, helping 
to detect hidden patterns in 
neural oscillations.

**Passage 10:**

> Contents lists available at ScienceDirect
SoftwareX
journal homepage: www.elsevier.com/locate/softx  
Original software publication
topoEEG: An Python-framework for analyzing EEG data in 
neurodegeneratives disease through Topological Deep Learning
Miriam Esteve a
 ,∗, Alejandro Martinez-Gracia a, Jesus J.

**Passage 11:**

> data analy-
sis and Python programming. Additionally, topoEEG has been tested 
mostly within the context of AD and FTD, which may limit its im-
mediate applicability to other neurological conditions. While these 
challenges are acknowledged, topoEEG still represents a significant 
contribution to the field by providing a more accessible means of 
integrating advanced topological methods into neuroimaging research. Moving forward, expanding its scope, improving user-friendliness, and 
broadening its applicability to other diseases will be key steps in mak-
ing topoEEG more widely accessible and influential in computational 
neuroscience. CRediT authorship contribution statement
Miriam Esteve: Writing – original draft, Visualization, Validation, 
Software, Resources, Methodology, Investigation, Formal analysis, Data 
curation, Conceptualization.

**Passage 12:**

> ter diagnostics. MNE-Python Provides comprehensive 
EEG/MEG tools
topoEEG extends its capabilities 
by leveraging TDA to analyze 
complex topological changes in 
brain networks.
 
progression [11,12]. This approach addresses a pressing methodologi-
cal need in neurodegenerative disease research, providing a novel tool 
for clinicians and researchers seeking to extract richer insights from 
EEG data [13,14]. 2. Related work
Within the domain of neuroimaging analysis, several frameworks 
have emerged, each specializing in distinct aspects of brain data pro-
cessing. For example, Brainstorm is widely recognized for its robust 
support of MEG and EEG analysis, facilitating source localization 
and connectivity studies [15]. FieldTrip, on the other hand, excels in 
time–frequency analysis and non-parametric statistical testing, mak-
ing it invaluable for investigating neural oscillations [16].

**Passage 13:**

> ttp://dx.doi.org/10.1109/TFUZZ. 2019.2903753.
[41] Zhang X, Zhao H, Wang J, Li Y. Spatiotemporal dynamics of periodic and 
aperiodic brain activity under peripheral nerve stimulation with acupuncture. IEEE Trans Neural Syst Rehabil Eng 2021;29:567–78.
[42] Jung TP, Makeig S, Humphries C, Lee TW, McKeown MJ, Iragui V, et 
al. Removing electroencephalographic artifacts by blind source separation. Psychophysiology 2000;37(2):163–78.
[43] Welch PD. The use of fast Fourier transform for the estimation of power spectra: 
A method based on time averaging over short, modified periodograms. IEEE 
Trans Audio Electroacoust 1967;15(2):70–3.
[44] Bastiani M, Cerri C, Giampiccolo D, Cerasti E, Annunziato M. Topological data 
analysis for neuroscience. Front Comput Neurosci 2020;14(49).
[45] Gunter MW, Müller T, Ziegelmann D. Machine learning for neuroimaging: A 
systematic review.

**Passage 14:**

> ting 
neuronal activity across different frequencies, providing insights into 
brain patterns for each patient group. Each recording includes 19 EEG channels, segmented into time 
intervals or epochs. The data is marked with timestamps to track 
signals over time, enabling the identification of relevant brain events. Additional subject information, such as age, gender, and disease stage, 
is included for Alzheimer’s and frontotemporal dementia patients. 5.2. Artifact removal
The process begins by removing artifacts caused by eye movements, 
muscle contractions, and environmental noise. This is achieved using 
the Independent Component Analysis (ICA) method, which decomposes 
EEG signals into statistically independent components. ICA assumes 
that EEG signals are a linear mixture of various sources, some repre-
senting brain activity and others corresponding to noise.

**Passage 15:**

> lds upon existing techniques by integrating the MNE 
library with Topological Deep Learning (TDL) to enhance neuroimaging 
insights, specifically in the context of neurodegenerative diseases [37,
38]. The innovation of topoEEG lies in its systematic approach to pre-
process EEG data, extract topological features through persistence land-
scapes, and apply machine learning classifiers to improve diagnostic 
accuracy [39–41]. SoftwareX 31 (2025) 102222 
8 
M. Esteve et al. The topoEEG workflow efficiently processes raw EEG data through 
essential steps, including preprocessing to remove artifacts, Indepen-
dent Component Analysis (ICA) for artifact removal, and Power Spec-
tral Density (PSD) analysis for frequency identification, while leverag-
ing Topological Deep Learning (TDL) to uncover neural features related 
to conditions like Alzheimer’s disease.

**Passage 16:**

> ctivity in human brain by acupuncture stimulation. IEEE Trans Neural Syst Rehabil Eng 2018;26(5):977–86. http://dx.doi.org/10. 1109/TNSRE.2018.2828143.
[10] Yu Haitao, Li Xiang, Lei Xinyu, Wang Jiang. Modulation effect of acupuncture on 
functional brain networks and classification of its manipulation with EEG signals. IEEE Trans Neural Syst Rehabil Eng 2019;27(10):1973–84. http://dx.doi.org/10. 1109/TNSRE.2019.2939655.
[11] Tajima S, Yamashita O, Nagasaka Y. Application of topological data anal-
ysis to functional brain networks in Alzheimer’s disease. Front Neurosci 
2021;15:646754.
[12] Bastos AM, Schoffelen JM. A tutorial review of functional connectivity analysis 
methods and their interpretational pitfalls. Front Syst Neurosci 2015;9(175).
[13] Yao Y, Lu B, Zhao Y, Zhang X. Resting-state EEG biomarkers in Alzheimer’s 
disease: A review.

**Passage 17:**

> lzheimer’s 
Disease (AD) compared to healthy controls (CN). The color coding in 
both diagrams highlights variations in topological stability, aiding in 
the interpretation of complex neural dynamics. 1 # Compute t h e p e r s i s t e n c e diagram from t h e EEG p o i n t cloud d a t a f o r t h e
2 # c u r r e n t channel
3 diagram = topoEEG_obj . c o m p u t e _ p e r s i s t e n c e _ d i a g r a m (
4 topoEEG_obj . p o i n t _ c l o u d [ i ]
5 )
6
7 # C r e a t e a g r i d o f v a l u e s r a n g i n g from 0 t o t h e maximum v a l u e i n t h e
8 # p o i n t cloud
9 # T h i s g r i d i s used t o e v a l u a t e t h e p e r s i s t e n c e l a n d s c a p e
10 g r i d = np . l i n s p a c e ( # np : Numpy
11 0 , np . max( topoEEG_obj . p o i n t _ c l o u d [ i ] ) ,
12 topoEEG_obj . g r i d _ s i z e # Number o f p o i n t s i n t h e g r i d
13 )
14
15 # Compute t h e p e r s i s t e n c e l a n d s c a p ev a l u e s based on t h e p e r s i s t e n c e
16 # diagram and g r i d
17 topoEEG_obj . l a n d s c a p e s = topoEEG_obj . c o m p u t e _ l a n d s c a p e _ v a l u e s ( diagram , g r i d )
18
19 # P l o t t h e p e r s i s t e n c e l a n d s c a p et o v i s u a l i z e t h e e x t r a c t e d
20 # t o p o l o g i c a l f e a t u r e s
21 topoEEG_obj . p l o t _ p e r s i s t e n c e _ l a n d s c a p e (
22 topoEEG_obj . l a n d s c a p e s
23 )
5.5.

**Passage 18:**

> horship contribution statement
Miriam Esteve: Writing – original draft, Visualization, Validation, 
Software, Resources, Methodology, Investigation, Formal analysis, Data 
curation, Conceptualization. Alejandro Martinez-Gracia: Writing – 
original draft, Visualization, Validation, Software, Resources, Investi-
gation, Formal analysis, Data curation. Jesus J. Rodríguez-Sala: Vi-
sualization, Validation, Software, Investigation, Formal analysis, Data 
curation. Antonio Falcó: Validation, Supervision, Software, Project 
administration, Investigation, Funding acquisition, Conceptualization. Declaration of competing interest
The authors declare that they have no known competing finan-
cial interests or personal relationships that could have appeared to 
influence the work reported in this paper. Acknowledgments
A. Falco and M.

**Passage 19:**

> diagnosis 
using deep learning models. Front Neurosci 2024;17:701659.
[25] Frolov A. Topological methods for neuroimaging analysis in Alzheimer’s disease. NeuroImage 2022;245:118644.
[26] Frisoni GB. Clinical applications of brain imaging in Alzheimer’s disease. Lancet 
Neurol 2010;9:157–68.
[27] Yu Haitao, Li Fan, Liu Jialin, Liu Dongliang, Guo Haolong, Wang Jiang, 
Li Guiping. Evaluation of acupuncture efficacy in modulating brain activity 
with periodic-aperiodic EEG measurements. IEEE Trans Neural Syst Rehabil Eng 
2024;32:2450–9. http://dx.doi.org/10.1109/TNSRE.2024.342164.
[28] Yu Haitao, Li Fan, Liu Jialin, Liu Chen, Li Guiping, Wang Jiang. Spatiotemporal 
dynamics of periodic and aperiodic brain activity under peripheral nerve stimula-
tion with acupuncture. IEEE Trans Neural Syst Rehabil Eng 2024;32:3993–4003. 
http://dx.doi.org/10.1109/TNSRE.2024.3492014.
[29] Smith J.

**Passage 20:**

> features such as connected components and loops appear and disappear. Each feature 
is recorded as a point (𝑏𝑖, 𝑑𝑖) in the persistence diagram, where 𝑏𝑖 is the birth scale and 
𝑑𝑖 is the death scale. The lifespan 𝑑𝑖 − 𝑏𝑖 reflects the feature’s significance in the data. Longer lifespans generally indicate more prominent topological structures.
data. Unlike traditional signal processing methods, TDL focuses on the 
‘‘shape’’ of data—capturing persistent patterns in neural activity that 
may reflect underlying cognitive processes or pathological changes. The process begins by segmenting EEG signals into time windows or 
by first computing the Power Spectral Density (PSD) across channels. Each resulting segment is then represented as a high-dimensional point 
cloud, where each point corresponds to a multichannel EEG reading 
(or PSD vector) at a specific time step.

**Passage 21:**

> connectivity analysis 
methods and their interpretational pitfalls. Front Syst Neurosci 2015;9(175).
[13] Yao Y, Lu B, Zhao Y, Zhang X. Resting-state EEG biomarkers in Alzheimer’s 
disease: A review. Front Aging Neurosci 2019;11(366).
[14] Stevanovic D, Krstic M, Savić M. Topological data analysis of EEG signals in 
neurodegenerative disorders. J Comput Neurosci 2022;50(1):85–102.
[15] Tadel F. Brainstorm: A user-friendly application for MEG/EEG analysis. Comput 
Intell Neurosci 2011;2011:879716.
[16] Oostenveld R. FieldTrip: Open-source software for advanced analysis of 
MEG, EEG, and invasive electrophysiological data. Comput Intell Neurosci 
2011;2011:156869.
[17] Friston KJ. Statistical parametric mapping: A novel approach to neuroimaging. Hum Brain Mapp 1994;1:210–30.
[18] Smith SM. Advances in functional magnetic resonance imaging with diffusion 
tensor imaging.

**Passage 22:**

> oimaging data. This integra-
tion underscores the potential of topological methods in enhancing the 
interpretation of EEG signals and their relation to neurodegenerative 
disease progression [47,48]. By making advanced analysis more acces-
sible to researchers, topoEEG contributes significantly to the ongoing 
efforts to combat these debilitating conditions and offers a promising 
avenue for future investigations in neuroimaging and computational 
neuroscience. However, it is important to note that topoEEG comes with certain 
limitations. Primarily developed around the Python MNE library, it 
requires a certain level of expertise in both topological data analy-
sis and Python programming. Additionally, topoEEG has been tested 
mostly within the context of AD and FTD, which may limit its im-
mediate applicability to other neurological conditions.

**Passage 23:**

> tional spectral and 
connectivity measures, yet recent studies highlight the importance of 
distinguishing between periodic and aperiodic brain activity to better 
characterize neural dynamics [9,10]. To bridge this gap, we introduce
topoEEG, a computational framework that enhances EEG analysis by 
combining MNE’s established processing pipelines with Topological 
Deep Learning (TDL). By leveraging TDL, topoEEG enables a more re-
fined characterization of neural network disruptions, offering improved 
sensitivity to the complex topological patterns underlying AD and FTD 
https://doi.org/10.1016/j.softx.2025.102222
Received 28 February 2025; Received in revised form 19 May 2025; Accepted 28 May 2025
SoftwareX 31 (2025) 102222 
Available online 21 June 2025 
2352-7110/© 2025 The Authors. Published by Elsevier B.V.

**Passage 24:**

> nal software publication
topoEEG: An Python-framework for analyzing EEG data in 
neurodegeneratives disease through Topological Deep Learning
Miriam Esteve a
 ,∗, Alejandro Martinez-Gracia a, Jesus J. Rodríguez-Sala a, Antonio Falcó b
a Center of Operation Research (CIO), Department of Mathematics, Statistics and Computer Science, Miguel Hernández University of Elche, Spain
b Departamento de Matematicas, Fisica y Ciencias Tecnologicas, Universidad Cardenal Herrera-CEU, CEU Universities, Spain
A R T I C L E  I N F O
Keywords:
EEG analysis
Topological Deep Learning (TDL)
Neurodegenerative diseases
 A B S T R A C T
topoEEG is a Python framework designed for advanced EEG analysis, combining the MNE library with 
Topological Deep Learning (TDL) to enhance insights into neuroimaging, particularly for neurodegenerative 
diseases such as Alzheimer’s.

</details>

---

## Graph-Based Permutation Patterns for the Analysis of Task-Related FMRI Signals on DTI Networks in Mild Cognitive Impairment
_File: `Graph-Based Permutation Patterns for the Analysis of Task-Related FMRI Signals on DTI Networks in Mild Cognitive Impairment.pdf`_

1. **Was diffusion MRI (DTI, dMRI, DWI, or similar) used in this paper?**  
   Yes. The paper explicitly mentions "diffusion-weighted (b = 1000 s mm−2)" and "DTI networks," confirming the use of diffusion MRI (DTI).

---

2. **What processing steps were applied to the diffusion images?**  
   - Acquisition: "3 T2-weighted (b = 0 s mm−2) and sets of diffusion-weighted (b = 1000 s mm−2) single-shot spin-echo-planar (EP) volumes were acquired with diffusion gradients applied in 32 non-collinear directions."  
   - Pre-processing: "Standard pre-processing was applied following [8], resulting in DTI networks where edge weight was determined by the streamline density (SD) between regions, corrected for ROI size."  

---

3. **What software or tools are explicitly named for processing?**  
   - **SPM12**: For outlier detection, realignment, slice-timing correction, co-registration, segmentation, and normalization.  
   - **FreeSurfer**: For sub-cortical segmentation and parcellation.  
   - **Desikan-Killiany atlas**: For parcellation.  
   - **BrainNet viewer tool**: For visualization of DTI networks.  

---

4. **What acquisition or processing parameters are explicitly reported?**  
   - **Diffusion parameters**:  
     - b = 0 s mm−2 (T2-weighted), b = 1000 s mm−2 (diffusion-weighted).  
     - 32 non-collinear diffusion gradient directions.  
   - **Voxel dimensions**: 1.875 × 1.875 × 2.5 mm for DTI.  
   - **fMRI parameters**:  
     - TR/TE = 2000/40 ms, matrix = 64 × 64, FOV = 24 cm, thickness = 5 mm.  
   - **Filtering**: Highpass filter at 0.06 Hz.  

---

5. **Copy the exact sentences from the excerpts that describe the processing.**  
   - "3 T2-weighted (b = 0 s mm−2) and sets of diffusion-weighted (b = 1000 s mm−2) single-shot spin-echo-planar (EP) volumes were acquired with diffusion gradients applied in 32 non-collinear directions."  
   - "Standard pre-processing was applied following [8], resulting in DTI networks where edge weight was determined by the streamline density (SD) between regions, corrected for ROI size."  
   - "Outlier detection, realignment, slice-timing correction, co-registration of the structural (T1) and functional images to the MNI space, segmentation, and normalization were performed with SPM12."  

---

6. **Is the processing description complete, or does it appear incomplete/missing?**  
   The processing description appears **incomplete**. While acquisition parameters and some pre-processing steps (e.g., DTI network creation via streamline density) are explicitly stated, details about diffusion tensor estimation, tractography, or specific algorithms used in the pre-processing pipeline (e.g., from [8]) are not elaborated.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> 3 T2-weighted (b = 0 s mm−2) and
sets of diffusion-weighted ( b = 1000 s mm−2) single-shot
spin-echo-planar (EP) volumes were acquired with diffusion
gradients applied in 32 non-collinear directions. Subse-
quent volumes were in the axial plane (fov = 240 × 240;
matrix = 128 × 128; thickness = 2 .5mm), giving voxel
dimensions of 1.875 × 1.875 × 2.5mm. A T1 weighted volume was also acquired with 1.3 mm 3
voxel dimensions. This volume was parcellated into 85 ROIs
with the Desikan-Killiany atlas combined with additional re-
gions acquired via sub-cortical segmentation detailed in [8],
and the brain-stem using FreeSurfer. Standard pre-processing
was applied following [8], resulting in DTI networks where
edge weight was determined by the streamline density (SD)
between regions, corrected for ROI size. 2078
Authorized licensed use limited to: OAKLAND UNIVERSITY.

**Passage 2:**

> ous in-
terleaved axial gradient EPI were collected alongside the
intercommissural plane throughout two continuous runs
(TR/TE = 2000 /40ms; matrix = 64 × 64; fov = 24 cm;
thickness = 5mm; gap = 0mm). Outlier detection, realignment, slice-timing correction,
co-registration of the structural ( T1) and functional images
to the MNI space, segmentation, and normalization were
performed with SPM12. ROIs for each subject are defined
using an 85 region atlas, detailed below. For each ROI, the
mean signal is acquired across the voxels in that region and
highpass filtered (0.06Hz) to avoid fMRI signal drift. For Diffusion MRI, 3 T2-weighted (b = 0 s mm−2) and
sets of diffusion-weighted ( b = 1000 s mm−2) single-shot
spin-echo-planar (EP) volumes were acquired with diffusion
gradients applied in 32 non-collinear directions.

**Passage 3:**

> ) Control vs. MCI
 (b) Control vs. MCIc
Fig. 5: Changes in pattern between healthy and disease. Note that only 2% of DTI edges are drawn for clarity. Gen-
erated with the BrainNet viewer tool [29]. 5. CONCLUSION AND LIMITA TIONS
We have extended the analysis of permutation patterns to
graph signals, providing a novel lens to view and analyze
such data at granular scale. Our findings indicate that the
turning rate ( α) and up-down balance ( β) serve as effective
tools for graph-based pattern analysis. Furthermore, we iden-
tify the potential use of graph based permutation patterns for
multi-modal MRI data of MCI. Though limited by sample
size, our results motivate larger studies of graph based per-
mutation patterns on other real-world data such as MRI-based
brain graph signals. 2079
Authorized licensed use limited to: OAKLAND UNIVERSITY.

**Passage 4:**

> jun 2014.
[15] W. Huang, T. A. Bolton, et al. A graph signal processing
perspective on functional brain imaging. Proceedings of the
IEEE, 106(5):868–885, 2018.
[16] M. P. Laakso, G. B. Frisoni, et al. Hippocampus and en-
torhinal cortex in frontotemporal dementia and Alzheimer’s
disease: a morphometric MRI study. Biological Psychiatry,
47(12):1056–1063, jun 2000.
[17] R. Li, X. Yuan, M. Radfar, P. Marendy, W. Ni, T. J. O’Brien,
and P. M. Casillas-Espinosa. Graph signal processing, graph
neural network and graph learning on biological data: a sys-
tematic review. IEEE Reviews in Biomedical Engineering ,
16:109–135, 2021.
[18] F. C. Morabito, D. Labate, F. L. Foresta, A. Bramanti, et al. Multivariate multi-scale permutation entropy for complexity
analysis of alzheimer’s disease eeg. Entropy, 14(7):1186–
1202, 2012.
[19] C. Morel and A. Humeau-Heurtier.

**Passage 5:**

> cterise a whole
graph signal. Here, we introduce a novel approach to evalu-
ate graph signals at the vertex level: graph-based permutation
patterns. Synthetic datasets show the efficacy of our method. We reveal that dynamics in graph signals, undetectable with
PEG, can be discerned using our graph-based patterns. These
are then validated in DTI and fMRI data acquired during a
working memory task in mild cognitive impairment, where
we explore functional brain signals on structural white mat-
ter networks. Our findings suggest that graph-based permuta-
tion patterns in individual brain regions change as the disease
progresses, demonstrating potential as a method of analyzing
graph-signals at a granular scale. Index Terms— Graph signals, Permutation entropy,
Graph topology, Permutation patterns, Neuroimaging. 1.

**Passage 6:**

> resented non-
nameable coloured shapes on a screen for 2s (encoding). They must memorize this information after a blank screen is
shown for a variable amount of time of 2, 4, 6, or 8s (main-
tenance). Then, they are presented the same or a different
set of associations of shapes and colours for 4s. The partici-
pants must determine if they are the same or different (probe),
followed by an inter-trial interval before repetition. In this
study, we focus on the encoding phase of the task to assess
the formation of memories in healthy and diseased groups. 4.2. Graph and signal construction
fMRI data was collected with a GE Signa Horizon HDxt
1.5T clinical scanner. During the VSTMBT, contiguous in-
terleaved axial gradient EPI were collected alongside the
intercommissural plane throughout two continuous runs
(TR/TE = 2000 /40ms; matrix = 64 × 64; fov = 24 cm;
thickness = 5mm; gap = 0mm).

**Passage 7:**

> Dong, D. Thanou, L. Toni, M. Bronstein, and P. Frossard. Graph signal processing for machine learning: A review
and new perspectives. IEEE Signal processing magazine ,
37(6):117–127, 2020.
[12] J. S. Fabila-Carrasco, C. Tan, and J. Escudero. Permutation
entropy for graph signals. IEEE Transactions on Signal and
Information Processing over Networks, 8:288–300, 2022.
[13] J. S. Fabila-Carrasco, C. Tan, and J. Escudero. Dispersion
entropy for graph signals. Chaos, Solitons and Fractals, 2023.
[14] A. M. Fjell, L. McEvoy, et al. What is normal in normal aging? Effects of aging, amyloid and Alzheimer’s disease on the cere-
bral cortex and the hippocampus. Progress in Neurobiology,
117:20–40, jun 2014.
[15] W. Huang, T. A. Bolton, et al. A graph signal processing
perspective on functional brain imaging. Proceedings of the
IEEE, 106(5):868–885, 2018.
[16] M. P. Laakso, G. B. Frisoni, et al.

**Passage 8:**

> GRAPH-BASED PERMUTA TION PA TTERNS FOR THE ANALYSIS OF TASK-RELA TED
FMRI SIGNALS ON DTI NETWORKS IN MILD COGNITIVE IMPAIRMENT
John S. Fabila-Carrasco∗†, Avalon Campbell-Cousins∗†, Mario A. Parra-Rodriguez+, Javier Escudero†
† School of Engineering, IDCOM, University of Edinburgh, UK
+ Department of Psychological Sciences and Health, University of Strathclyde, UK
ABSTRACT
Permutation Entropy (PE) is a powerful nonlinear analysis
technique for univariate time series. Recently, Permutation
Entropy for Graph signals (PE G) has been proposed to ex-
tend PE to data residing on irregular domains. However,PEG
is limited as it provides a single value to characterise a whole
graph signal. Here, we introduce a novel approach to evalu-
ate graph signals at the vertex level: graph-based permutation
patterns. Synthetic datasets show the efficacy of our method.

**Passage 9:**

> are other
early indicators of AD in studies of amyloid deposition and
structural and functional MRI [14, 16, 31]. Additionally, we look at pattern frequency changes be-
tween groups at granular scale. Namely, we identify the most
dominant pattern per node for each subject group that ap-
pears in at least half of the subjects. This is visualized in
Fig. 5. Here, nodes in orange are those that have changed pat-
tern, blue indicated no change, black had no definitive pattern
within the control group, and labelled nodes are from Table 1.
(a) Control vs. MCI
 (b) Control vs. MCIc
Fig. 5: Changes in pattern between healthy and disease. Note that only 2% of DTI edges are drawn for clarity. Gen-
erated with the BrainNet viewer tool [29]. 5.

**Passage 10:**

> ropsychological tests commonly used
to assess dementia, grouping subjects into early Mild Cogni-
tive Impairment (eMCI), MCI, and Alzheimer’s disease con-
verters after a 2-year follow up (MCIc) [23]. From these, 8
healthy controls (Age: 76.50 ± 5.21, Sex: 2M; 6F), 7 eMCI
(Age: 76.86 ± 6.41, Sex: 4M; 3F), 10 MCI (Age: 72.30 ±
5.64, Sex: 5M; 5F), and 6 MCIc subjects (Age: 76.33 ± 5.09,
Sex: 4M; 2F) were selected to undergo DTI and fMRI ac-
quisition during which they performed a Visual Short-Term
Memory Binding Task (VSTMBT). The VSTMBT [22] is a task sensitive to memory related
changes in early stage AD. Participants were presented non-
nameable coloured shapes on a screen for 2s (encoding). They must memorize this information after a blank screen is
shown for a variable amount of time of 2, 4, 6, or 8s (main-
tenance).

**Passage 11:**

> ugh limited by sample size, in the healthy brain networks,
we observe the existence of dominant patterns in some clus-
ters, such as patterns 5&6 in ROIs 1-18, and patterns 1&2 in
ROIs 75-81 (see Fig. 4a), suggesting that there may be some
identifying patterns associated with the encoding phase of the
VSTMBT. (Here we refer to patterns #1 to #6 following the
order as in Fig. 1.)
(a) Patterns across subjects
 (b) Brain visualization
Fig. 4: (a) visualizes the distribution of patterns (rows),
across subjects (columns). In (b), patterns for a node were
based on the mode of the distribution of patterns for the
healthy group, but only when that pattern was in at least half
of subjects (black otherwise). (b) was generated with the
BrainNet viewer tool [29].

**Passage 12:**

> original p-value (p) is smaller than that of the
randomly permuted groups ( p′). Due to the limited sample
size, we took a conservative approach to report regions where
both p, p′ ≤ 0.05. Control vs. ROIs p-value p < p ′
eMCI Right-lateralorbitofrontal 0.019 0.009
MCI Right-entorhinal 0.015 0.002
Right-lateralorbitofrontal 0.020 0.027
Right-parahippocampal 0.010 0
MCIc Left-hippocampus 0.049 0.050
Left-caudalmiddlefrontal 0.036 0.033
Left-medialorbitofrontal 0.031 0.008
Right-lateralorbitofrontal 0.005 0
Right-paracentral 0.049 0.021
Table 1: Statistical tests to find regions with significant dif-
ferences in the distribution of graph-based permutation pat-
terns between control and different stages of MCI.

**Passage 13:**

> 1, 2023.
[7] A. Bessadok, M. A. Mahjoub, and I. Rekik. Graph neural net-
works in network neuroscience. IEEE Transactions on Pattern
Analysis and Machine Intelligence, 45(5):5833–5848, 2022.
[8] C. R. Buchanan, C. R. Pernet, et al. Test–retest reliability
of structural brain networks from diffusion mri. Neuroimage,
86:231–243, 2014.
[9] Y . Cao, W.-w. Tung, et al. Detecting dynamical changes in
time series using the permutation entropy. Physical review E,
70(4):046217, 2004.
[10] M. Didic, E. J. Barbeau, O. Felician, E. Tramoni, E. Guedj,
M. Poncet, and M. Ceccaldi. Which memory system is im-
paired first in alzheimer’s disease? Journal of Alzheimer’s
Disease, 27(1):11–22, 2011.
[11] X. Dong, D. Thanou, L. Toni, M. Bronstein, and P. Frossard. Graph signal processing for machine learning: A review
and new perspectives. IEEE Signal processing magazine ,
37(6):117–127, 2020.
[12] J. S.

**Passage 14:**

> aluating functional connectiv-
ity of executive control network and frontoparietal network
in Alzheimer’s disease. Brain Research, 1678:262–272, jan
2018.
[32] L. Zunino, M. Zanin, B. M. Tabak, et al. Forbidden patterns,
permutation entropy and stock market inefficiency.Physica A,
388:2854–2864, 2009. 2080
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:40:05 UTC from IEEE Xplore. Restrictions apply.

**Passage 15:**

> lines: Panorama of
Entropy: Theory, Computation, and Applications , pages 233–
286, 2023.
[3] C. Bandt. Statistics and contrasts of order patterns in univariate
time series. Chaos, 33(3), 2023.
[4] C. Bandt and B. Pompe. Permutation Entropy: A Natural
Complexity Measure for Time Series. Physical Review Let-
ters, 88(17):174102, apr 2002.
[5] C. Bandt and K. Wittfeld. Two new parameters for the ordinal
analysis of images. Chaos: An Interdisciplinary Journal of
Nonlinear Science, 33(4), 2023.
[6] C. Bastin and E. Delhaye. Targeting the function of the
transentorhinal cortex to identify early cognitive markers of
alzheimer’s disease. Cognitive, Affective, & Behavioral Neu-
roscience, pages 1–11, 2023.
[7] A. Bessadok, M. A. Mahjoub, and I. Rekik. Graph neural net-
works in network neuroscience. IEEE Transactions on Pattern
Analysis and Machine Intelligence, 45(5):5833–5848, 2022.
[8] C. R.

**Passage 16:**

> ing [8], resulting in DTI networks where
edge weight was determined by the streamline density (SD)
between regions, corrected for ROI size. 2078
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:40:05 UTC from IEEE Xplore. Restrictions apply. 4.3. Results
We calculate the graph-based patterns as per Sec. 2.2 with
m = 3. The graph is the subject’s SD-weighted DTI network
and the signal at each node is the mean signal across the en-
coding phases of the task, yielding a pattern at each node. Though limited by sample size, in the healthy brain networks,
we observe the existence of dominant patterns in some clus-
ters, such as patterns 5&6 in ROIs 1-18, and patterns 1&2 in
ROIs 75-81 (see Fig.

**Passage 17:**

> graph permutation patterns to charac-
terise local changes in neuroimaging datasets in mild cogni-
tive impairment, a prodromal phase of Alzheimer’s disease. 2. GRAPH-BASED PERMUTATION PA TTERNS
2.1. Notation
Let G = (V, E, A) represent a simple undirected graph with
vertex set V = {v1, v2, . . . , vN } and edge set E defined as
E ⊂ { (vi, vj)|vi, vj ∈ V} . The adjacency matrix A is an
N × N symmetric matrix with Aij = 1 if an edge connects
vi and vj, and Aij = 0 otherwise. 2076979-8-3503-4485-1/24/$31.00 ©2024 IEEE ICASSP 2024
ICASSP 2024 - 2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) | 979-8-3503-4485-1/24/$31.00 ©2024 IEEE | DOI: 10.1109/ICASSP48485.2024.10447332
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:40:05 UTC from IEEE Xplore. Restrictions apply. A graph signal X maps V → R.

**Passage 18:**

> ttention
recently due to their useful properties in univariate time se-
ries, and their study has very recently been extended to 2D
formulations [5]. However, they remain unexplored for graph
signals. Our contributions are:
• The first definition of permutation patterns for graph signals
as a way to characterise them at granular level.
• Extension of the contrasts α (turning rate) and β (up-down
balance) to graph signals for detailed pattern analysis.
• The study of the behaviour of α and β for synthetic bench-
marks of graph signals.
• The illustration of graph permutation patterns to charac-
terise local changes in neuroimaging datasets in mild cogni-
tive impairment, a prodromal phase of Alzheimer’s disease. 2. GRAPH-BASED PERMUTATION PA TTERNS
2.1.

**Passage 19:**

> on the mode of the distribution of patterns for the
healthy group, but only when that pattern was in at least half
of subjects (black otherwise). (b) was generated with the
BrainNet viewer tool [29]. To determine whether patterns change with disease, we
perform chi-squared analysis comparing the per node patterns
between each pair of control and disease groups. Further-
more, we assess the stability of the resulting p-value by per-
muting the control and disease groups 1000 times to calculate
how often our original p-value (p) is smaller than that of the
randomly permuted groups ( p′). Due to the limited sample
size, we took a conservative approach to report regions where
both p, p′ ≤ 0.05. Control vs.

**Passage 20:**

> paracentral 0.049 0.021
Table 1: Statistical tests to find regions with significant dif-
ferences in the distribution of graph-based permutation pat-
terns between control and different stages of MCI. We find that, as the disease progresses (Table 1), the num-
ber of regions which exhibit a significant change in pattern
increases, following a neuroanatomical trajectory consistent
with that described by the AD continuum, i.e., Medial Tem-
poral Lobe (MTL) regions first and then broader impact in-
cluding frontal lobes [6, 10, 23]. Not only was the gross neu-
roanatomical spread of AD pathology found, but our method
identified the more fine grained distribution of pathology
within the MTL characterizing the earliest stages of AD (i.e.,
entorhinal which feeds to parahippocampal and hippocampal
regions [6, 10, 23]).

**Passage 21:**

> a-
tion, and sound statistical properties [9]. Building on Shannon’s entropy, PE quantifies the distri-
bution of ‘permutation patterns’ in time series [4]. Such
∗These authors share first authorship. This work was supported by the
Leverhulme Trust via a Research Project Grant (RPG-2020-158) to JER and
by Alzheimer’s Society Grants AS-R42303 and AS-SF-14-008 awarded to
MAP in collaboration with JER. ACC acknowledges Edinburgh University’s
Principle’s Career Development PhD Scholarship and Federica Guazzo for
pre-processing the fMRI data. For the purpose of open access, the author
has applied a Creative Commons Attribution (CC BY) licence to any author
accepted manuscript version arising from this submission.
patterns have broad applications, from biomedical to fi-
nance data [26].

**Passage 22:**

> ean
Physical Journal Special Topics, 222(2):249–262, 2013.
[27] P. Scheltens, B. De Strooper, M. Kivipelto, et al. Alzheimer’s
disease. The Lancet, 397(10284):1577–1590, apr 2021.
[28] J. Sepulcre, M. R. Sabuncu, A. Becker, R. Sperling, and K. A. Johnson. In vivo characterization of the early states of the
amyloid-beta network. Brain, 136(7):2239–2252, 2013.
[29] M. Xia, J. Wang, and Y . He. Brainnet viewer: a network
visualization tool for human brain connectomics. PloS one ,
8(7):e68910, 2013.
[30] Y . Yin and P. Shang. Weighted multiscale permutation entropy
of financial time series. Nonlinear Dynamics, 78:2921–2939,
2014.
[31] Q. Zhao, H. Lu, et al. Evaluating functional connectiv-
ity of executive control network and frontoparietal network
in Alzheimer’s disease. Brain Research, 1678:262–272, jan
2018.
[32] L. Zunino, M. Zanin, B. M. Tabak, et al.

**Passage 23:**

> L. Foresta, A. Bramanti, et al. Multivariate multi-scale permutation entropy for complexity
analysis of alzheimer’s disease eeg. Entropy, 14(7):1186–
1202, 2012.
[19] C. Morel and A. Humeau-Heurtier. Multiscale permutation en-
tropy for two-dimensional patterns. Pattern Recognition Let-
ters, 150:139–146, oct 2021.
[20] A. Ortega. Introduction to graph signal processing . Cam-
bridge University Press, 2022.
[21] A. Ortega, P. Frossard, et al. Graph signal processing:
Overview, challenges, and applications. Proceedings of the
IEEE, 106(5):808–828, 2018.
[22] M. A. Parra, S. Abrahams, R. H. Logie, et al. Visual short-
term memory binding deficits in familial Alzheimer’s disease. Brain, 133(9):2702–2713, sep 2010.
[23] M. A. Parra, C. Calia, V . Pattan, and S. Della Sala. Mem-
ory markers in the continuum of the Alzheimer’s clinical syn-
drome.

**Passage 24:**

> a heightened α. Conversely, higher frequen-
cies result in fewer local points, leading to a reduced α. Increases in r augments graph connectivity, thereby en-
hancing sensitivity to frequency changes. The β-α Complementarity: α and β display different
behaviours, confirming that they both provide complementary
information, as shown in Fig. 3.
(a) Turning rate α
 (b) Up-down balance β
Fig. 3: Graph-based contrasts for the MIX process. 4. REAL-WORLD ILLUSTRA TION IN MCI
Dementia currently affects over 50 million people worldwide
and is expected to triple by 2050 [27]. Alzheimer’s disease
(AD) is the main cause of dementia and causes immense emo-
tional and financial strain on families and healthcare services. Its early stages are often categorized by stages of Mild Cog-
nitive Impairment (MCI), often progressing (within 4 years)
to the dementia stage of AD [27].

</details>

---

## Harnessing Machine Learning for Early Detection of Alzheimer-s Disease
_File: `Harnessing Machine Learning for Early Detection of Alzheimer-s Disease.pdf`_

1. **Yes**, diffusion MRI (DTI) was used. The paper explicitly mentions "diffusion tensor imaging (DTI)" and "Fractional Anisotropy (FA) scans, derived from DTI."

2. **Processing steps applied to diffusion images** (in order):  
   - "The FA data was motion-corrected and normalized to ensure consistency across subjects."  
   - "The FA values were extracted from specific regions of interest (ROIs) using standard anatomical templates."  
   - "Correlation analysis was performed to identify the most relevant biomarkers for classification tasks."  
   - "Permutation analysis was also applied on the blood biomarker data to extract relevant features."  

3. **Software or tools explicitly named**:  
   - **FSL** (used to convert NIfTI files to 2D JPEG formats).  
   - **ResNet 3D**, **LeNet**, and **Random Forest** (machine learning models, though not strictly image processing tools).  

4. **Acquisition/processing parameters reported**:  
   - **Number of directions**: Not explicitly mentioned.  
   - **B-values**: Not explicitly mentioned.  
   - **Voxel size**: Not explicitly mentioned.  
   - **Thresholds**: Not explicitly mentioned.  
   - **Other parameters**: The paper does not report specific acquisition or processing parameters beyond the steps described.  

5. **Exact sentences from the excerpts**:  
   - "In this paper, first, the FA data was motion-corrected and normalized to ensure consistency across subjects. Next, the FA values were extracted from specific regions of interest (ROIs) using standard anatomical templates."  
   - "The biomarker data was pre-processed by handling missing values through imputation. For categorical data (e.g., gender, diagnosis), label encoding was applied."  
   - "Correlation analysis was performed to identify the most relevant biomarkers for classification tasks."  
   - "Permutation analysis was also applied on the blood biomarker data to extract relevant features."  

6. **Processing description completeness**:  
   The description appears **incomplete**. While motion correction, normalization, ROI extraction, and feature selection are mentioned, critical steps like diffusion tensor calculation, tensor fitting, or parameter estimation (e.g., b-values, number of directions) are not explicitly reported. The focus on biomarker analysis and machine learning models suggests the diffusion MRI processing steps are not fully detailed.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> s apply. B. Preprocessing 
Preprocessing of the neuroimaging data involved several 
steps. In this paper, first, the FA data was motion-corrected and 
normalized to ensure consistency across subjects. Next, the FA values were extracted from specific regions of 
interest (ROIs) using standard anatomical templates. These 
ROIs were chosen based on previous studies indicating their 
vulnerability to early AD-related changes. For the sMRI data, Voxel Based Morphometry(VBM) was 
used to measure gray matter volume in the hippocampus, 
entorhinal cortex, and other cortical areas. The images were 
normalized to the Montreal Neurological Institute (MNI) 
template, and gray matter volumes were extracted for statistical 
analysis. The biomarker data was pre-processed by handling missing 
values through imputation. For categorical data (e.g., gender, 
diagnosis), label encoding was applied.

**Passage 2:**

> Tensor Imaging (DTI) which were obtained from the 
portal of EU Open Research Repository, measure the diffusion 
of water molecules in the brain to provide insights into white 
matter (WM) integrity. High FA values are generally observed 
in healthy white matter, where water diffusion is highly 
directional along axonal fibres, while lower FA values indicate 
white matter degradation, which is often associated with 
pathological processes like Alzheimer’s disease (AD). Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:43:40 UTC from IEEE Xplore. Restrictions apply. B. Preprocessing 
Preprocessing of the neuroimaging data involved several 
steps. In this paper, first, the FA data was motion-corrected and 
normalized to ensure consistency across subjects.

**Passage 3:**

> rative 
neurological condition that results in the deterioration of cognitive 
function. Early non-invasive detection is crucial for implementing 
timely interventions and slowing disease progression. In this 
research, we aimed to analyse the predictivity for classifying AD 
stages by integrating neuroimaging data —diffusion tensor 
imaging (DTI) and structural MRI (sMRI) —with clinical 
biomarkers. In this paper Fractional Anisotropy (FA)  scans, 
derived from DTI, denoting water molecule diffusion  in brain 
tissue was assessed , particularly in identifying early 
microstructural changes during the mild cognitive impairment 
(MCI) stage of AD. To progressively monitor the structural 
pathology of AD in patients,  OASIS sMRI dataset  was used.

**Passage 4:**

> e extracted for statistical 
analysis. The biomarker data was pre-processed by handling missing 
values through imputation. For categorical data (e.g., gender, 
diagnosis), label encoding was applied. A correlation analysis 
was performed to identify the most relevant biomarkers for 
classification tasks. The top 20 biomarkers were selected based 
on their correlation with cognitive scores and AD diagnosis. C. Model Deployment 
The machine learning model employed in this paper 
processed extensive 3D  imaging data from Fractional 
Anisotropy (FA) scans, 2D structural MRI (sMRI) from the 
OASIS dataset, and  tabulated clinical biomarkers to classify 
Alzheimer’s disease (AD) stages effectively. The process 
consisted of data acquisition, model selection, training and 
validation, and model optimization as represented in Fig. 2.

**Passage 5:**

> discussions. II. METHODOLOGY 
A. Dataset 
1) OASIS Dataset : The Open Access Series of Imaging 
Studies (OASIS) dataset , is a comprehensive resource widely 
used in Alzheimer's disease (AD) research. Established to 
facilitate the study of brain aging and neurodegenerative 
diseases, OASIS provides a rich collection of cross -sectional 
and longitudinal MRI data from a diverse cohort of subjects, 
including both healthy controls /non-demented(ND) and 
individuals diagnosed with various stages of Alzheimer's 
disease—Very Mild Demented (VMD), Mild Demented (MiD) 
and Moderate Demented (MoD). Our dataset comprised of 80,000 brain MRI images, which 
were used to study Alzheimer's disease progression. Original 
NIfTI files (.nii)  files were converted into  2D image formats  
like .jpeg using FSL and were made available through a GitHub 
repository.

**Passage 6:**

> re used to study Alzheimer's disease progression. Original 
NIfTI files (.nii)  files were converted into  2D image formats  
like .jpeg using FSL and were made available through a GitHub 
repository. For neural network training, the brain scans were 
sliced into 2D images, selecting slices 100 to 160 along the z -
axis for 461 patients. The OASIS dataset included T1-weighted 
structural MRI scans, along with associated clinical 
assessments such as the Clinical Dementia Rating (CDR) and 
Mini-Mental State Examination (MMSE) scores. Based on 
Clinical Dementia Rating (CDR) values, patients were 
classified into four stages: demented, very mild demented, mild 
demented, and non-demented. The final dataset, processed into 
JPEG format, totalled up to 1.3 GB, enabling robust 
Alzheimer’s detection analysis.

**Passage 7:**

> https://doi.org/10.1016/j.dscb.2021.100005. 
[19] Y. Sang and W. Li, "Classification Study of Alzheimer’s Disease 
Based on Self -Attention Mechanism and DTI Imaging Using 
GCN," in IEEE Access, vol. 12, pp. 24387 -24395, 2024, doi: 
10.1109/ACCESS.2024.3364545. Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:43:40 UTC from IEEE Xplore. Restrictions apply.

**Passage 8:**

> s. TABLE I. PERFORMANCE OF OUR PROPOSED MODELS  
Datasets Performance 
Proposed Modality Accuracy 
OASIS sMRI 
CNN 99.7 
LeNet 99.3 
FA Scans ResNet18 3D 82.5 
Biomarkers Random Forest 90 
 
TABLE II. PERFORMANCE OF EXISTING STATE-OF-THE-
ART MODELS 
Datasets 
Performance 
Author and Year Existing 
Modality Accuracy 
OASIS sMRI 
Battineni et al. (2021) 
[17] 
Gradient 
boosting 97.58%, 
Islam J. et al, 2018[16] CNN 93% 
FA Scans 
Yida Qu et al, 2021[18] 
SVM, 
XGBoost, 
L.R. etc 
80.47% 
Y. Sang et al, 2024[19] 
Graph Conv. Network 78.6% 
Biomarkers 
Popuri et al., 2020 [15] ensemble-
learning 
AUC: 0.81(6 
Months), 
0.73(7 Yrs) 
Jo et al., 2020[13] CNN 90.8% 
 
The above Table 1 and Table 2 compare the performance 
accuracies of our models against the existing modalities, thus 
proving that our approach es are significantly detecting 
plausible diagnostics. B.

**Passage 9:**

> also used in model 
training. The dataset also includes information on medications 
taken, such as anti -hypertensives, antidepressants, and 
anticholinergics, which can influence cognitive outcomes. Other clinical factors such as age, education, and comorbidities 
(e.g., hypertension, d iabetes) further contextualize individual 
health profiles. This multidimensional dataset serves as a robust 
foundation for devel oping machine learning models aimed at 
improving early detection and understanding of Alzheimer’s 
disease progression. 3) Fractional Anisotropy (FA):  FA Scans , derived from 
Diffusion Tensor Imaging (DTI) which were obtained from the 
portal of EU Open Research Repository, measure the diffusion 
of water molecules in the brain to provide insights into white 
matter (WM) integrity.

**Passage 10:**

> S AND DISCUSSION 
A. Results 
The evaluation of the individual models for Fractional 
Anisotropy (FA), structural MRI (sMRI), and biomarker data 
was carried out using their respective  test datasets. Each 
modality was processed and modelled independently with the 
goal of future integration. Although a robust integrated model 
is still in progress, the initial results from individual models 
show promising accuracy, underscoring the potential of a 
multi-modal approach. 
(1) Fractional Anisotropy (FA) Model : The FA model 
assessed white matter integrity  in brain tissues which degrade 
overtime in AD patients . Significant differences in FA values 
across the Alzheimer’s Disease (AD ) progressive stages were 
identified, particularly in the cingulum bundle, uncinate 
fasciculus, and corpus callosum.

**Passage 11:**

> identifying early 
microstructural changes during the mild cognitive impairment 
(MCI) stage of AD. To progressively monitor the structural 
pathology of AD in patients,  OASIS sMRI dataset  was used. Convolutional neural networks (CNNs)  like ResN et 3D and 
LeNET were applied to analyse FA and sMRI data , achieving a 
significant accuracy score. In this proposed work, correlation and 
permutation analysis  was also applied on the blood biomarker  
data to extract relevant features . R andom Forest  classifier was 
then used on these biomarkers. The highly correlated biomarkers 
were later used to obtain a significant impact in identifying the 
various stages of Alzheimer’s progression. Keywords— Alzheimer's disease, Fractional Anisotropy (FA), 
Diffusion Tensor Imaging (DTI), Biomarkers, Magnetic Resonance 
Imaging (MRI), Early diagnosis 
I.

**Passage 12:**

> o 
underlying biological processes such as inflammation , toxic 
proteins and oxidative stress, complementing our imaging data. A multi -modal approach hence is  crucial for accurately 
diagnosing AD. This is understood because while FA reveal s 
early white matter changes, it lacks specificity for tracking gray 
matter atrophy. Conversely, sMRI provid es detailed structural 
information but at a much later stage where patients are usually 
symptomatic and miss the golden period of reverting back from 
the damage. It  misses early white matter abnormalities. Biomarkers, though effective for detecting underlying 
biological processes, cannot directly reveal structural changes 
in the brain. Therefore, integrating these modalities becomes 
necessary for a complete and accurate  early diagnosis, and we 
have laid the groundwork for   enabling a more effective 
diagnostic approach. IV.

**Passage 13:**

> measuring gray matter atrophy in 
regions such as the hippocampus and entorhinal cortex. Voxel-
Based Morphometry (VBM) revealed significant atrophy in 
MoD and M iD patients compared to ND subjects. The CNN 
models like LeNet and a custom variation achieved accuracies 
of 99.3% and 99.7% respectively in classifying  ND, VMD, 
MiD, and MoD subjects, confirming the importance of sMRI in 
detecting structural changes during later stages of AD. The 
performance metric curves are mentioned in Fig. 6 below. Fig. 5. (a)Training Accuracy and (b) Training Loss Curves of the LeNET 
Model Training and Validation. In t he Fig. 5, training curve s show rapid accuracy 
improvement within the first few epochs, reaching near-perfect 
performance by epoch 5, while the loss converges quickly.

**Passage 14:**

> ification accuracy, effectively identifying early -stage 
degeneration, especially in the transition from CN to MCI. Fig. 4. FA Scans Model training metrics using ResNet 3D for 150 epochs. In the Fig. 4 training curves show a steady decrease in loss 
and a gradual increase in accuracy, with the model approaching 
high performance after around 40 epochs and validation loss 
increased after an initial drop, indicating potential overfitting 
hence why Early Stopping was employed to curb the issue. 
(2) Gray Matter (GM) Model from Structural MRI:  The 
sMRI model focused on measuring gray matter atrophy in 
regions such as the hippocampus and entorhinal cortex. Voxel-
Based Morphometry (VBM) revealed significant atrophy in 
MoD and M iD patients compared to ND subjects.

**Passage 15:**

> mentia score: Independent validation on 8,834 
images from ADNI, AIBL, OASIS, and MIRIAD databases. Hum 
Brain Mapp . 2020; 41: 4127–
4147. https://doi.org/10.1002/hbm.25115 
[16] Islam, J., Zhang, Y. Brain MRI analysis for Alzheimer’s disease 
diagnosis using an ensemble system of deep convolutional neural 
networks. Brain Inf. 5, 2 (2018). https://doi.org/10.1186/s40708-
018-0080-3
 
[17] Battineni G, Hossain MA, Chintalapudi N, Traini E, Dhulipalla VR, 
Ramasamy M, Amenta F. Improved Alzheimer’s Disease Detection 
by MRI Using Multimodal Machine Learning 
Algorithms. Diagnostics.

**Passage 16:**

> g/10.1002/alz.12756 
[10] Qu, Y., et al.: AI4ad: artificial intelligence analysis for Alzheimer’s 
disease classification based on a multisite DTI database. Brain 
Disord. (2021). 
[11] Y. Sang and W. Li, "Classification Study of Alzheimer’s Disease 
Based on Self -Attention Mechanism and DTI Imaging Using 
GCN," in IEEE Access, vol. 12, pp. 24387 -24395, 2024, doi: 
10.1109/ACCESS.2024.3364545. 
[12] De, A.; Chowdhury, A.S. DTI based Alzheimer’s disease 
classification with rank modulated fusion of CNNs and random 
forest. Expert Syst. Appl. 2021, 169, 114338. Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:43:40 UTC from IEEE Xplore. Restrictions apply. 
[13] Jo, T., Nho, K., Risacher, S.L.  et al. Deep learning detection of 
informative features in tau PET for Alzheimer’s disease 
classification.

**Passage 17:**

> tients . Significant differences in FA values 
across the Alzheimer’s Disease (AD ) progressive stages were 
identified, particularly in the cingulum bundle, uncinate 
fasciculus, and corpus callosum. These reductions in FA values 
suggest early white matter degeneration, a less utilised  early 
marker of Alzheimer’s. The FA model achieved 82.5% 
classification accuracy, effectively identifying early -stage 
degeneration, especially in the transition from CN to MCI. Fig. 4. FA Scans Model training metrics using ResNet 3D for 150 epochs. In the Fig.

**Passage 18:**

> or imaging (DTI), for instance, measures the 
diffusion of water molecules in brain tissues, providing 
valuable insights into w hite matter integrity through metrics 
like Fractional Anisotropy (FA). FA reflec ts early 
microstructural changes in white matter, which are among the 
first signs of AD. Similarly, structural MRI (sMRI) is crucial in 
assessing gray matter atrophy, especially in regions like the 
hippocampus, which is particularly vulnerable to early damage 
in AD. Recent studies have increasingly highlighted the 
benefits of integrating multiple imaging modalities, such as FA 
from DTI and sMRI data, to enhance diagnostic accuracy. Combining MRI and genetic data with machine learning 
models has also led to diagnostic accuracy rates as high as 90%, 
with models like ADD-NET demonstrating strong performance 
by optimizing multimodal data [1].

**Passage 19:**

> have demonstrated that FA measures can 
effectively distinguish between AD patients and healthy 
controls by analysing white matter integrity, which notably 
decreases as the disease progresses [ 10]. Machine learning 
methods have proven invaluable in analysing these 
relationships, revealing complex interactions between white 
matter integrity and cognitive function. Moreover, advanced  
models incorporating self -attention mechanisms with FA data 
have achieved high classification accuracy, particularly when 
focusing on brain regions specifically impacted by AD [ 11]. These findings, combined with sophisticated classification 
algorithms, further solidify FA's role in early AD detection, 
offering significant clinical potential [12].

**Passage 20:**

> functional abilities, and its pathological hallmarks, such as 
amyloid plaques and neurofibrillary tangles, often only become 
detectable after substantial and irreversible brain damage has 
occurred. This highlights the pressing need for early detection, 
as timely interventions may help slow disease progression and 
improve quality of life for those affected. Traditional diagnostic methods, such as clinical 
assessments and cognitive tests, often fail to detect AD in its 
earliest stages, when intervention would be most effective. To 
address this limitation, advanced neuroimaging techniques 
have become essential tools in AD research and diagnosis. Diffusion tensor imaging (DTI), for instance, measures the 
diffusion of water molecules in brain tissues, providing 
valuable insights into w hite matter integrity through metrics 
like Fractional Anisotropy (FA).

**Passage 21:**

> Correlation analysis were employed for feature extraction. Random Forest classifier was also tested for its robustness in 
handling high-dimensional data and its ability to rank feature 
importance. The final classifier was trained on the selected 
biomarkers and was evaluated based on accuracy, precision, 
Fig. 1. Fractional Anisotropy 40 longitudinal scan slices(128x128x45) 
 
Fig. 2  Research Methodology 
 
 
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:43:40 UTC from IEEE Xplore. Restrictions apply. 
recall, and AUC -ROC (Area under the Receiver Operating 
Characteristic Curve). The datasets were divided into training, validation, and test 
sets using an 80 -20 split. The models were trained on the 
training set, validated on a separate validation set, and then 
tested on unseen data to evaluate their generalizability.

**Passage 22:**

> arious stages of Alzheimer’s progression. Keywords— Alzheimer's disease, Fractional Anisotropy (FA), 
Diffusion Tensor Imaging (DTI), Biomarkers, Magnetic Resonance 
Imaging (MRI), Early diagnosis 
I. INTRODUCTION 
Alzheimer’s disease (AD) is a progressive 
neurodegenerative disorder that affects millions of people 
worldwide, particularly the elderly. As the global population 
ages, the number of AD cases is expected to rise significantly, 
putting immense pressure on healthcare systems. AD is marked 
by a stead y decline in cognitive function and the loss of 
functional abilities, and its pathological hallmarks, such as 
amyloid plaques and neurofibrillary tangles, often only become 
detectable after substantial and irreversible brain damage has 
occurred.

**Passage 23:**

> n distinguishing between AD 
progression stages. Metrics such as accuracy, precision, recall, 
F1-score, and AUC -ROC were calculated to provide a 
comprehensive evaluation of the model's performance. These 
metrics are defined as: 
Accuracy = 
𝑇𝑃+𝑇𝑁
𝑇𝑃+𝑇𝑁+𝐹𝑃+𝐹𝑁, Precision = 
𝑇𝑃
𝑇𝑃+𝐹𝑃, Sensitivity = 
𝑇𝑃
𝑇𝑃+𝐹𝑁, 
 F1 score = 
2𝑇𝑃
2𝑇𝑃+𝐹𝑃+𝐹𝑁 
Where FP=False Positive, FN= False Negative, TP= True Positive, and TN= 
True Negative. The integration of multiple imaging modalities and 
biomarkers significantly enhanced the classification approach, 
highlighting the potential of a multi-modal technique for early 
Alzheimer's diagnosis. III. RESULTS AND DISCUSSION 
A. Results 
The evaluation of the individual models for Fractional 
Anisotropy (FA), structural MRI (sMRI), and biomarker data 
was carried out using their respective  test datasets.

**Passage 24:**

> nificance of  these 
blood-based biomarkers, using machine learning techniques to 
identify key biomarkers associated with dementia, further 
highlighting their value in the early detection of AD [8]. Blood-
based biomarkers (BBMs), such as plasma Aβ42/Aβ40, p -tau, 
and NfL, when integrated with machine learning techniques, 
offer enhanced diagnostic accuracy and reduce reliance on 
costly methods like PET and CSF tests [9]. In addition to MRI and blood biomarkers, FA scans from 
DTI have emerged as a critical component in AD research. Numerous studies have demonstrated that FA measures can 
effectively distinguish between AD patients and healthy 
controls by analysing white matter integrity, which notably 
decreases as the disease progresses [ 10].

</details>

---

## HemiHeter-GNN A Hemispheric Heterogeneity-Aware Graph Neural Network for Mild Cognitive Impairment Detection
_File: `HemiHeter-GNN A Hemispheric Heterogeneity-Aware Graph Neural Network for Mild Cognitive Impairment Detection.pdf`_

1. **Was diffusion MRI (DTI, dMRI, DWI, or similar) used in this paper?**  
   Yes. The paper explicitly mentions **DTI** (diffusion tensor imaging) as part of the multimodal brain network construction, integrating it with fMRI data.

---

2. **What processing steps were applied to the diffusion images?**  
   - **Heat kernel-based graph diffusion** was applied as a topological smoothing operator to reduce structural complexity and enhance graph regularity within hemispheric subnetworks.  
   - **Spectral entropy and dominant eigenvalue analysis** were used to evaluate the structural impact of diffusion.  
   - **Decomposition into subnetworks** (left, right, and inter-hemispheric) and refinement via heat-kernel diffusion.  

---

3. **What software or tools are explicitly named for processing?**  
   No specific software or tools are mentioned. The methods described are algorithmic (e.g., heat kernel diffusion, graph neural networks) rather than tool-based.

---

4. **Acquisition or processing parameters?**  
   - **Diffusion time** $ t \in [0.2, 0.4] $ (for heat kernel-based diffusion).  
   - **Number of convolutional layers** $ l \in (2, 64) $ (for hemisphere-specific encoders).  
   - **Spectral entropy** and **eigenvalue** (mean/standard deviation) for structural analysis.  

---

5. **Exact sentences about processing:**  
   - *"we utilize heat kernel-based graph diffusion as a topological smoothing operator to reduce complexity and improve regularity within each hemispheric subnetwork."*  
   - *"To evaluate the structural impact of heat-kernel diffusion, we analyzed spectral characteristics within each hemisphere using spectral entropy and dominant eigenvalue."*  

---

6. **Is the processing description complete?**  
   **No.** The description focuses on **heat kernel diffusion** and **spectral analysis** but omits details about standard diffusion MRI preprocessing steps (e.g., motion correction, eddy current correction, or parameter optimization beyond $ t $ and $ l $). The methodology is algorithmic but lacks explicit mention of acquisition parameters (e.g., b-values, voxel size) or software tools.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> the distinct structural and functional charac-
teristics of each subnetwork, we design specialized graph
encoders to extract tailored representations for hemispheric
and inter-hemispheric subnetworks. Additionally, we reﬁne the
intra-hemispheric topology using heat kernel-based diffusion
to reduce structural complexity and enhance graph regularity. 1) Heat Kernel-based Graph Diffusion: Intra-hemispheric
subnetworks derived from DTI often contain irregular and
noisy topologies [15], which pose challenges for effective
4346
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply. 
graph learning. To alleviate this, we utilize heat kernel-based
graph diffusion as a topological smoothing operator to reduce
complexity and improve regularity within each hemispheric
subnetwork.

**Passage 2:**

> zation via Heat-Kernel Diffusion
To evaluate the structural impact of heat-kernel diffusion,
we analyzed spectral characteristics within each hemisphere
using spectral entropy and dominant eigenvalue. As shown
in Table IV, spectral entropy decreased after diffusion (e.g.,
from 3.2793 to 2.3769 on the left hemisphere), indicating
reduced graph complexity and enhanced structural regularity. Dominant eigenvalues also declined (e.g., from 0.7094 to
4348
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply. TABLE II
CLASSIFICATION RESULTS (MEAN / SD) BY 5-FOLD CROSS -VALIDATION WITH COMPETING METHODS IN FINE -GRAINED MCI TASKS . Method NC vs. MCI (%) NC vs. LMCI (%) NC vs.

**Passage 3:**

> ly. 
graph learning. To alleviate this, we utilize heat kernel-based
graph diffusion as a topological smoothing operator to reduce
complexity and improve regularity within each hemispheric
subnetwork. Moreover, prior studies show that heat kernel-
based graph diffusion can approximate functional connectivity
from structural data [16], imparting functional characteristics
to the reﬁned networks. Mathematically, the diffusion process
is formulated as a power series:
S =
∞∑
k=0
θkTk, (1)
where T ∈ Rn×n is the generalized transition matrix, and
θk ∈ [0, 1] is the coefﬁcient of the k-th order term, sat-
isfying ∑∞
k=0θk = 1 . Speciﬁcally, the transition matrix is
deﬁned as random-walk normalized matrixTrw =AD−1 with
Di,i =∑
jAi,j, the coefﬁcientsθk =e−ttk
k! follow a Poisson
distribution, t is a hyperparameter controlling the diffusion
scale.

**Passage 4:**

> ection, and its overall architecture is shown in Fig. 2. A. Multimodal Brain Networks Construction
In this study, we construct multimodal brain networks by
integrating resting-state fMRI and DTI data. Each brain graph
is deﬁned as G = (A,X ), where X ={v1,...,v n}∈ Rn×d
denotes the node feature matrix, where each node vi charac-
terized by a d-dimensional Blood Oxygen Level Dependent
(BOLD) time series derived from fMRI. The graph comprises
n nodes, each corresponding to a predeﬁned ROI in the
AAL atlas. The adjacency matrix A ∈ Rn×n is extracted
from DTI, where each element Aij ∈ (0, 1) denotes the
normalized fractional anisotropy (FA) value between ROIs i
and j, indicating anatomical connection strength. Each brain
network is associated with a binary label y∈{ 0, 1}, where
y = 0 represents a cognitively normal control (NC), andy = 1
denotes a subject diagnosed with MCI. B.

**Passage 5:**

> ∑
T
(
y· log
(
ˆy
)
+
(
1−y
)
· log
(
1− ˆy
))
. (10)
4347
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply. TABLE I
DEMOGRAPHIC AND CLINICAL CHARACTERISTICS OF SUBJECTS
Group Number Gender Age / std
Male Female
MCI 51 33 18 74 /8
EMCI 64 39 25 77 /15
LMCI 36 18 18 72 /11
NC 115 85 30 72 /5.1
III. EXPERIMENTS AND RESULTS
A. Materials
In this study, we utilized brain imaging data from the
Alzheimer’s Disease Neuroimaging Initiative (ADNI), includ-
ing 266 subjects: 115 cognitively normal (NC), 51 MCI,
64 early MCI (EMCI), and 36 late MCI (LMCI). The de-
tails of demographics and clinical characteristics are pre-
sented in Table I. Further details on preprocessing and sub-
ject demographics are available in the GitHub repository:
https://github.com/ilove-gh/HemiHeter-GNN. B.

**Passage 6:**

> y
functional magnetic resonance imaging (fMRI) and diffusion
tensor imaging (DTI), have enabled the construction of brain
networks that integrate functional dynamics with structural
topology [2], [3]. This graph-based representation naturally
supports graph neural network (GNN) modeling, leading to
promising results in MCI detection [4], [5]. Despite recent progress, most GNN-based approaches [4],
[6]–[10] still model brain networks as homogeneous graphs,
implicitly assuming uniform functional and structural proper-
ties across ROIs.

**Passage 7:**

> , Y . Xiang, and T. Ma, “Mapping multi-
modal brain connectome for brain disorder diagnosis via cross-modal
mutual learning,” IEEE Trans. Med. Imag., vol. 43, no. 1, pp. 108–121,
2024.
[25]Z. Zhou, Q. Wang, X. An, S. Chen, Y . Sun, G. Wang, and G. Yan, “A
novel graph neural network method for alzheimer’s disease classiﬁca-
tion,” Comput. Biol. Med. , vol. 180, p. 108869, 2024.
[26]Q. Zhu, S. Li, X. Meng, Q. Xu, Z. Zhang, W. Shao, and D. Zhang,
“Spatio-temporal graph hubness propagation model for dynamic brain
network classiﬁcation,” IEEE Trans. Med. Imaging. , vol. 43, no. 6, pp. 2381–2394, 2024.
[27]F. Nogueira, “Bayesian Optimization: Open source constrained
global optimization tool for Python,” 2014. [Online]. Available:
https://github.com/bayesian-optimization/BayesianOptimization
4350
Authorized licensed use limited to: OAKLAND UNIVERSITY.

**Passage 8:**

> n as a
reﬁnement step. Additionally, a cross-subnetwork attention fu-
sion module is designed to adaptively integrate representations
from all subnetworks into a comprehensive whole-brain em-
bedding. Finally, we evaluate HemiHeter-GNN on the ADNI
dataset for MCI classiﬁcation, where results demonstrate its
superiority over baseline methods, conﬁrming the beneﬁt of
modeling hemispheric connectivity heterogeneity. II. METHODOLOGY
To capture structural and functional heterogeneity in brain
networks, we propose HemiHeter-GNN for improved MCI
detection, and its overall architecture is shown in Fig. 2. A. Multimodal Brain Networks Construction
In this study, we construct multimodal brain networks by
integrating resting-state fMRI and DTI data.

**Passage 9:**

> isphere Structure 3.2793 / 0.1446 0.7094 / 0.3022
Diffusion 2.3769 / 0.2013 0.3035 / 0.2258
Right Hemisphere Structure 3.2829 / 0.1955 0.7030 / 0.3081
Diffusion 2.3899 / 0.2085 0.3095 / 0.2335
Fig. 6. Eigenvalue distributions of hemispheric subnetworks before and after
heat-kernel diffusion.
each hemispheric subnetwork before and after heat-kernel
diffusion in the NC vs. All-MCI task. A degree-based variation
score quantiﬁed diffusion-induced alterations, and the top
10 ROIs per hemisphere were selected (Table V, statisti-
cally signiﬁcant ROIs underlined). Key hubs include PCL.L,
PCG.L, ORBmid.L, HES.L, CUN.L, and SFGmed.L in the
left hemisphere, and ORBmid.R, PCG.R, HES.R, SFGmed.R,
and ACG.R in the right. Many align with previous reports
of MCI-related alterations [5]. Their spatial distribution is
shown in Fig. 7.

**Passage 10:**

> EEE Xplore. Restrictions apply. TABLE II
CLASSIFICATION RESULTS (MEAN / SD) BY 5-FOLD CROSS -VALIDATION WITH COMPETING METHODS IN FINE -GRAINED MCI TASKS . Method NC vs. MCI (%) NC vs. LMCI (%) NC vs. EMCI (%)
Accuracy F1 Sensitivity Precision Accuracy F1 Sensitivity Precision Accuracy F1 Sensitivity Precision
GCN 63.25 / 14.0 60.82 / 13.92 63.25 / 14.0 65.17 / 14.0 53.09 / 13.23 47.6 / 16.38 53.09 / 13.23 46.24 / 20.01 62.16 / 9.39 55.98 / 8.83 62.16 / 9.39 51.51 / 10.06
GAT 65.0 / 10.16 60.05 / 14.35 65.0 / 10.16 57.66 / 17.02 61.82 / 10.6 57.14 / 14.17 61.82 / 10.6 55.71 / 18.75 64.21 / 3.94 59.3 / 4.95 64.21 / 3.94 61.82 / 9.77
GCNII 71.25 / 9.35 71.46 / 8.93 71.25 / 9.35 75.8 / 7.21 63.64 / 12.86 63.84 / 12.17 63.64 / 12.86 71.9 / 8.87 65.26 / 7.88 64.95 / 8.15 65.26 / 7.88 65.82 / 8.48
CAGNN 64.58 / 2.64 53.72 / 5.6 64.58 / 2.64 47.09 / 9.79 54.55 / 4.98 41.34 / 11.09 54.55 / 4.98 35.28 / 15.95 64.21 / 4.92 57.14 / 3.29 64.21 / 4.92 52.47 / 6.81
GCNH 72.5 / 11.59 72.93 / 12.03 72.5 / 11.59 76.71 / 13.28 66.55 / 11.48 62.61 / 15.46 66.55 / 11.48 64.21 / 20.92 70.7 / 3.98 59.39 / 6.67 70.7 / 3.98 54.65 / 14.4
HebrainGNN 64.58 / 6.18 76.26 / 4.15 64.58 / 6.18 58.76 / 11.78 66.18 / 6.54 62.12 / 8.46 66.18 / 6.54 67.09 / 6.59 69.59 / 2.24 82.04 / 1.55 69.59 / 2.24 48.47 / 3.12
MHSA 78.93 / 3.20 72.46 / 5.34 79.09 / 13.47 79.62 / 78.50 83.64 / 1.56 79.39 / 5.94 77.50 / 8.11 72.18 / 4.52 74.86 / 7.66 74.40 / 15.42 73.59 / 15.47 77.88 / 9.31
WHGCN 81.98 / 3.07 77.75 / 6.50 81.17 / 15.13 78.17 / 12.26 80.45 / 7.42 62.10 / 22.74 62.67 / 20.91 70.06 / 21.25 80.11 / 6.30 72.55 / 16.79 72.0 / 20.2 85.84 / 13.45
OT-MCSTGCN 83.72 / 4.56 71.46 / 8.47 69.38 / 16.41 79.62 / 8.59 83.64 / 1.91 82.85 / 2.15 80.12 / 3.19 82.30 / 1.61 79.94 / 8.43 73.69 / 14.37 76.39 / 13.65 75.09 / 14.37
Cross-GNN 77.17 / 6.97 72.83 / 8.72 77.17 / 6.97 75.41 / 12.9 76.18 / 10.44 74.37 / 10.76 76.18 / 10.44 71.46 / 12.33 77.25 / 11.2 76.34 / 12.02 77.33 / 11.2 76.94 / 13.34
HemiHeter-GNN87.33 / 6.86 86.66 / 7.3 87.43 / 6.5 83.76 / 8.8 84.8 / 2.1 83.05 / 4.95 84.27 / 3.95 82.5 / 5.53 86.03 /2.82 85.76 / 2.33 85.37 / 2.5 84.68 / 3.93
TABLE III
CLASSIFICATION RESULTS (MEAN / SD) BY 5-FOLD CROSS -VALIDATION
WITH COMPETING METHODS IN COARSE -GRAINED MCI TASK.

**Passage 11:**

> l diffusion simpliﬁes
intra-hemispheric topology, improves spectral consistency, and
strengthens high-order representations, contributing to more
robust and discriminative brain network embeddings. E. Identiﬁcation of MCI-Related Hub ROIs
To evaluate HemiHeter-GNN’s ability to identify MCI-
related hubs ROIs, we examined connectivity changes within
TABLE IV
SPECTRAL ENTROPY AND EIGENVALUE (MEAN / S TD) OF STRUCTURAL
AND DIFFUSED HEMISPHERIC SUBNETWORKS . Hemisphere Group
NC vs All-MCI
Spectral Entropy Spectral Eigenvalue
Left Hemisphere Structure 3.2793 / 0.1446 0.7094 / 0.3022
Diffusion 2.3769 / 0.2013 0.3035 / 0.2258
Right Hemisphere Structure 3.2829 / 0.1955 0.7030 / 0.3081
Diffusion 2.3899 / 0.2085 0.3095 / 0.2335
Fig. 6.

**Passage 12:**

> ADNI demonstrate con-
sistent improvements over state-of-the-art baselines. Future
work will explore extensions to other neurodegenerative dis-
orders, temporal dynamics, and longitudinal prediction. ACKNOWLEDGMENT
This work was supported in part by the National Natural
Science Foundation of China under Grant 62466042, in part
by the Inner Mongolia University Postgraduate Research and
Innovation Project Under Grant 11200-5223737. REFERENCES
[1]M. S. Bhargavi and B. Prabhakar, “Deep learning approaches for early
detection of alzheimer’s disease using mri neuroimaging,” in 2022
International Conference on Connected Systems & Intelligence (CSI) ,
2022, pp. 1–6.
[2]X. Luo, J. Wu, J. Yang, S. Xue, A. Beheshti, Q. Z. Sheng, D. McAlpine,
P. F. Sowman, A. Giral, and P. S. Yu, “Graph neural networks for brain
graph learning: A survey,” in IJCAI, 2024, pp. 8170–8178.
[3]G. Shi, Y . Zhu, W. Liu, Q.

**Passage 13:**

> 4. Evaluation of the signiﬁcance of different components of HemiHeter-
GNN on the ADNI dataset. 2) Ablation Study: To assess component contributions, we
conducted ablation studies as shown in Fig. 4. Removing the
diffusion module (W/o D) disables the smoothing process in
Eq.(3), causing notable performance degradation and high-
lighting the need for hemispheric structure regularization. In
the W/o A setting, eliminating hemispheric decomposition and
attention fusion reduces the model to a diffusion-augmented
GCNII with lower accuracy. When both modules are removed
(W/o DA), HemiHeter-GNN degenerates into a plain GCNII
without hemispheric awareness and structural smoothness,
yielding the worst performance.

**Passage 14:**

> 25.
[9]A. Zou, J. Ji, M. Lei, J. Liu, and Y . Song, “Exploring brain effective con-
nectivity networks through spatiotemporal graph convolutional models,”
IEEE T. Neur. Net. Lear., vol. 35, no. 6, pp. 7871–7883, 2024.
[10]R. Xu, Q. Zhu, S. Li, Z. Hou, W. Shao, and D. Zhang, “Mstgc: Multi-
channel spatio-temporal graph convolution network for multi-modal
brain networks fusion,” IEEE T. Neur. Sys. Reh. , vol. 31, pp. 2359–
2369, 2023.
[11]G. Shi, X. Li, Y . Zhu, R. Shang, Y . Sun, H. Guo, and J. Sui, “The
divided brain: Functional brain asymmetry underlying self-construal,”
NeuroImage., vol. 240, p. 118382, 2021.
[12]M. Thiebaut de Schotten, F. Dell’Acqua, S. Forkel, A. Simmons,
F. Vergani, D. G. Murphy, and M. Catani, “A lateralized brain network
for visuo-spatial attention,” Nat. Preced., pp. 1–1, 2011.
[13]S. Fern ´andez-Carriba, ´A. Loeches, A. Morcillo, and W. D.

**Passage 15:**

> ntroduces hemispheric heterogeneity by dis-
tinguishing edge types based on DTI-derived structures, yet
overlooks intra-hemispheric topological irregularities caused
by anisotropic ﬁber architectures. These irregularities may
hinder discriminative representation learning and obscure ﬁne-
grained structures, especially under subtle neurodegenerative
changes in MCI. Thus, modeling hemispheric heterogeneity
while reducing intra-hemispheric irregularity is crucial for
biologically meaningful brain network analysis. To bridge this gap, we propose HemiHeter-GNN, a Hemi-
spheric Heterogeneity-aware Graph Neural Network that ex-
plicitly models the structural and functional heterogeneity for
improved MCI detection. Speciﬁcally, we ﬁrst construct mul-
timodal brain networks by integrating fMRI-derived regional
features with DTI-based anatomical connectivity.

**Passage 16:**

> s
this limitation, we propose a Hemispheric Heterogeneity-aware
Graph Neural Network (HemiHeter-GNN) to explicitly model
hemispheric structural and functional heterogeneity for improved
MCI detection. Multimodal brain networks are constructed by
integrating diffusion tensor imaging (DTI) and functional mag-
netic resonance imaging (fMRI), and decomposed into left-, right-
, and inter-hemispheric subnetworks to capture hemisphere-
speciﬁc patterns. Each subnetwork is encoded by a dedicated
graph encoder and reﬁned by heat-kernel diffusion for topological
regularity, while a cross-subnetwork attention mechanism then
fuses them into a uniﬁed whole-brain embedding. Experiments on
the ADNI dataset show that HemiHeter-GNN consistently outper-
forms state-of-the-art baselines, demonstrating the effectiveness
of modeling hemispheric asymmetry for MCI detection.

**Passage 17:**

> UN.L
OLF.L, THA.L, PAL.L, SFGmed.L , REC.L
Right Hemispheric
Subnetwork
ORBmid.R, PCG.R, HES.R, SFGmed.R, PCL.R
SMA.R, CUN.R, OLF.R, ACG.R , REC.R
Fig. 7. 3D visualization of MCI-related hub ROIs. IV. C ONCLUSION
In this paper, we propose HemiHeter-GNN, a hemispheric
heterogeneity-aware GNN for MCI detection that models
structural and functional asymmetries by decomposing brain
networks into left-, right-, and inter-hemispheric subnetworks. Tailored encoders, intra-hemispheric diffusion, and cross-
subnetwork attention fusion enable the capture of ﬁne-grained
hemispheric patterns. Experiments on ADNI demonstrate con-
sistent improvements over state-of-the-art baselines. Future
work will explore extensions to other neurodegenerative dis-
orders, temporal dynamics, and longitudinal prediction.

**Passage 18:**

> GCNII with lower accuracy. When both modules are removed
(W/o DA), HemiHeter-GNN degenerates into a plain GCNII
without hemispheric awareness and structural smoothness,
yielding the worst performance. These results demonstrate that
the diffusion module and attention fusion work synergistically
to regularize brain topology and capture hemispheric hetero-
geneity for robust, disease-relevant representations. 3) Parameter Sensitivity Analysis: We further analyzed the
sensitivity of HemiHeter-GNN to two key hyperparameters:
the diffusion time t in heat kernel-based graph diffusion and
the number of convolutional layers l in hemisphere-speciﬁc
encoders. As shown in Fig. 5(a), the model performs best when
t∈ [0.2, 0.4], indicating that moderate diffusion enhances local
structural consistency and representation capacity.

**Passage 19:**

> ion
(b) Brain Subnetworks 
Construction
(c) Hemisphere-aware 
Specific Encoder
(e) Model Training(d) Cross-Subnetwork 
Attention Fusion
Common 
Nodes
LG
RG
IG
LP
RP
ˆy
Common 
Nodes
LH
RH
IH
Fig. 2. The overall architecture of our proposed HemiHeter-GNN framework.
hemispheric specialization, these brain networks are then
decomposed into three subnetworks: left-, right-, and inter-
hemisphere subnetworks, to disentangle their unique structural
and functional properties. Each subnetwork is encoded by a
dedicated graph encoder tailored to its speciﬁc characteristics. To reduce structural complexity and promote topological reg-
ularity, we apply intra-hemispheric heat-kernel diffusion as a
reﬁnement step. Additionally, a cross-subnetwork attention fu-
sion module is designed to adaptively integrate representations
from all subnetworks into a comprehensive whole-brain em-
bedding.

**Passage 20:**

> eatures. This encoder enables ﬂexible, relation-
aware message passing that jointly captures intra- and inter-
hemispheric dependencies, thus overcoming the limitations of
rigid bipartite assumptions. 4) Cross-subnetwork Attention Fusion: After obtaining the
embeddings HL, HR, and HI from the respective subnet-
works, we design a cross-subnetwork attention fusion mecha-
nism to integrate complementary information across these sub-
networks into a uniﬁed whole-brain representation. Notably,
the nodes in HL and HR are disjoint, whereas all nodes in
HI are shared with either HL or HR. Let the set of common
nodes be deﬁned asNC ={vi|vi∈HI and vi∈HL∪HR}. For each common node vi ∈ NC, let hC
i denote its intra-
hemispheric embedding from HL or HR, and hI
i denote
its inter-hemispheric embedding from HI.

**Passage 21:**

> n F1-score, 6.62% in sensitivity, and 5.59%
in precision. Comparable improvements are observed in the
EMCI and LMCI comparisons, conﬁrming its robustness
across varying stages of cognitive impairment. In the coarse-
grained task, HemiHeter-GNN achieves 89.4% accuracy,
exceeding all baselines by 0.59%–15.32%. These results
highlight the model’s strong generalization ability, which
stems from its dedicated design to capture hemispheric
structural and functional heterogeneity, thereby enhancing the
accuracy and reliability of MCI detection.
（a）NC vs. MCI （b）NC vs. EMCI
（c）NC vs. LMCI （d）NC vs. All-MCI
W/o D W/o A W/o DA HemiHeter-GNN
Fig. 4. Evaluation of the signiﬁcance of different components of HemiHeter-
GNN on the ADNI dataset. 2) Ablation Study: To assess component contributions, we
conducted ablation studies as shown in Fig. 4.

**Passage 22:**

> hsa: A multi-
scale hypergraph network for mild cognitive impairment detection via
synchronous and attentive fusion,” in BIBM, 2024, pp. 2808–2815.
[6]M. Yuan, C. Yin, J. Hu, Y . Zhao, J. Wang, and H. Li, “A novel
fuzzy-rule-based deep fusion of hypergraph multi-modal for alzheimer’s
disease detection,” Neurocomputing, vol. 650, p. 130855, 2025.
[7]Y . Ma, T. Zhang, Z. Wu, X. Mu, X. Liang, and L. Guo, “Multi-view
brain networks construction for alzheimer’s disease diagnosis,” in BIBM,
2023, pp. 889–892.
[8]M. Yuan, J. Li, Y . Zhao, J. Wang, J. Ye, and W. Jia, “Edgeviewdet:
Dynamic edge-centric fusion network with granger causality for neuro-
logical disorders detection.” pp. 255–264, 2025.
[9]A. Zou, J. Ji, M. Lei, J. Liu, and Y . Song, “Exploring brain effective con-
nectivity networks through spatiotemporal graph convolutional models,”
IEEE T. Neur. Net. Lear., vol. 35, no. 6, pp.

**Passage 23:**

> ber of layers l∈ (2, 64), and residual
weights α,β ∈ (0.1, 0.9). Performance was evaluated by
accuracy, F1-score, sensitivity, and precision, following the
settings reported in the original papers. C. Results and Analysis
1) Main Disease Detection Results: We evaluated
HemiHeter-GNN on three ﬁne-grained classiﬁcation tasks
(NC vs. MCI, NC vs. EMCI, and NC vs. LMCI) and one
coarse-grained task (NC vs. All-MCI), as summarized in
Tables II and III. Across all settings, HemiHeter-GNN
consistently outperforms both general-purpose GNNs and
brain-speciﬁc baselines. In the NC vs. MCI task, for example,
it surpasses the second-best method (WHGCN) by 5.35% in
accuracy, 8.91% in F1-score, 6.62% in sensitivity, and 5.59%
in precision. Comparable improvements are observed in the
EMCI and LMCI comparisons, conﬁrming its robustness
across varying stages of cognitive impairment.

**Passage 24:**

> ing. Experiments on
the ADNI dataset show that HemiHeter-GNN consistently outper-
forms state-of-the-art baselines, demonstrating the effectiveness
of modeling hemispheric asymmetry for MCI detection. Index Terms—Mild cognitive impairment, Brain network het-
erogeneity, Hemispheric specialization, Graph neural networks. I. I NTRODUCTION
Mild cognitive impairment (MCI) is a prodromal stage of
Alzheimer’s disease characterized by early cognitive decline. Its early detection is vital for effective intervention and disease
prevention [1]. Recent advances in neuroimaging, especially
functional magnetic resonance imaging (fMRI) and diffusion
tensor imaging (DTI), have enabled the construction of brain
networks that integrate functional dynamics with structural
topology [2], [3].

</details>

---

## Hybrid-CNN-and-SVM-model-for-Alzheimer-s-disease-classif_2026_Pattern-Recogn
_File: `Hybrid-CNN-and-SVM-model-for-Alzheimer-s-disease-classif_2026_Pattern-Recogn.pdf`_

1. **Was diffusion MRI (DTI, dMRI, DWI, or similar) used in this paper?**  
   **NO DIFFUSION MRI PROCESSING FOUND**  

2. **What processing steps were applied to the diffusion images?**  
   Not applicable (no diffusion MRI processing reported).  

3. **What software or tools are explicitly named for processing?**  
   Not applicable (no diffusion MRI processing reported).  

4. **What acquisition or processing parameters are explicitly reported?**  
   Not applicable (no diffusion MRI processing reported).  

5. **Copy the exact sentences from the excerpts that describe the processing.**  
   Not applicable (no diffusion MRI processing reported).  

6. **Is the processing description complete, or does it appear incomplete/missing?**  
   **NO DIFFUSION MRI PROCESSING FOUND** (processing steps described are for standard MRI, not diffusion MRI).

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> 2025 
0167-8655/© 2025 The Author(s). Published by Elsevier B.V. This is an open access article under the CC BY-NC-ND license ( http://creativecommons.org/licenses/by- 
nc-nd/4.0/ ). W. Hechkel et al. Nomenclature
Nomenclature  Description
AD  Alzheimer’s disease
CNN  convolutional neural network
SVM  support vector machines
MRI  Magnetic Resonance Imaging
CFL  Categorical Focal Loss
ND  Non-Demented
MD  Mild-Demented
VMD  Very-Mild-Demented
MD  Moderate-Demented
CBIR  Content-Based Image Retrieval
MCI  Mild Cognitive Impairment
PET  Positron Emission Tomography
SMOTE  Synthetic Minority Oversampling Technique
CN  Cognitive Normal
ADNI  Alzheimer’s Disease Neuroimaging Initiative
OASIS  Open Access Series of Imaging Studies
ReLU  Rectiﬁed Linear Unit
RBF  Radial Basis Function
OVR  One-Vs-Rest
ROC  Receiver Operating Characteristic
AUC  Area Under the Curve
imbalance by ﬁne-tuning the parameters of the framework.

**Passage 2:**

> 448
 MildDemented  896  14 %  28 6292 144 180
 ModerateDemented  64  1 %  2 440 11 13
Total number 6400 100 % 200 45023 962 1281
 47266 images
Table 3 
Parameters of the data augmentation methods. Sr. No  Data Augmentation techniques  Parameters
 1  Image Identity  No transformation
 2  Image Rotation  Rotation angle: [−20◦, 20◦]
 3  Image Shift  Shift: [−20 %, 20 %]
 4  Image Shear  Shear angle: [−0.2, 0.2]
 5  Image Zoom  Zoom factor: [1 − 0.2, 1 + 0.2]
 6  Image Horizontal_Flip  Flip: 𝑝 = .5
 7  Two Images Mixup  Mixup factor: 𝛼 = 0.5
1. Data preparation: Acquiring data from the Kaggle dataset and split-
ting it into training, validation, and testing. Next, training data has 
been augmented before rescaling and normalization to the interval 
[0, 1] and fed into the network. 2.

**Passage 3:**

> i-
nal dataset was designated for the test set; the rest was divided into 80 % 
for training and 20 % for validation. Only training data was augmented 
using several data augmentation techniques. Fig. 1 illustrates represen-
tative brain MRI images for each category, while Table 2 presents the 
dataset distribution. The rationale for choosing the Kaggle MRI dataset over other sources 
is its public availability and also because it contains a large number of 
records in a small dataset size of only 36 Megabytes. Moreover, even if 
this dataset is not balanced, especially for MD and MoD classes which 
present together only 15 % of the hole dataset, this gap helps to iso-
late the proposed work contribution regarding data imbalances and its 
robustness against overﬁtting.

**Passage 4:**

> del, which contains 
three convolutional layers. The perfection of obtained accuracies over the diﬀerent 
stages, which is close to 100 %, indicates a risk of 
overﬁtting. 3. Material and methods
3.1. Dataset
The AD MRI dataset utilized in this study was collected from the 
open-source platform Kaggle [27]. It comprises 6400 pre-processed MRI 
scans categorized into four groups: non-demented (ND), very mild de-
mented (VMD), mild demented (MD), and moderate demented (MoD). It includes 200 participants, with each contributing 32 horizontal brain 
slices. The original image resolution was 176×208 pixels, but all images 
were resized to 64 × 64 pixels before normalization. 20 % of the origi-
nal dataset was designated for the test set; the rest was divided into 80 % 
for training and 20 % for validation. Only training data was augmented 
using several data augmentation techniques. Fig.

**Passage 5:**

> mixed MRI 
slice. Fig. 2 shows some examples of the DA images. Mixup was proposed the ﬁrst time by Zhang et al. in 2017 [28]. The philosophy around this approach is to synthesize new image by 
Fig. 1. Classes included in the Alzheimer’s MRI Dataset: (a) Mild Demented, (b) 
Moderate Demented, (c) Non-Demented, (d) Very Mild Demented. Fig. 2. Examples of images after data augmentation.
combining two pairs of images. The following equations demonstrate 
the implementation of the overall process:
̃ 𝑥= 𝜆𝑥𝑖 + (1 − 𝜆)𝑥𝑗 , (1)
where 𝑥𝑖, 𝑥𝑗 are raw original input data
̃ 𝑦= 𝜆𝑦𝑖 + (1 − 𝜆)𝑦𝑗 , (2)
where 𝑦𝑖, 𝑦𝑗 are raw original input data
The 𝜆 factor varies from 0 to 1 dependently from the Beta distribu-
tion, however, 𝜆 ≈ 𝐵𝑒𝑡𝑎(𝛼 = 0.2).

**Passage 6:**

> n Table 6, it sur-
passes standalone CNN, 3D CNN and CNN+SVM approaches, achiev-
Pattern Recognition Letters 199 (2026) 261–268 
266 
W. Hechkel et al. Table 6 
Comparison with state-of-the-art works. Reference / year  Target / Dataset  Method  Accuracy
 [39] (2018)  sMRI + DTI (ADNI)  3D CNN + data augmentation  96.7 % (AD vs NC)
 [40] (2024)  MRI (ADNI)  CNN  95.62 % (MCI vs NC)
 [41] (2019)  MRI (OASIS)  SVM+ data augmentation  92.9 % (Multi-class)
 [10] (2024)  MRI (Kaggle)  CNN+SVM+ data augmentation  83.82 % (Multi-class)
 [24] (2022)  MRI (ADNI/OASIS)  CNN+SVM  89.4 % (CN vs AD)
 Proposed method  MRI (Kaggle)  CNN+SVM+data augmentation  97.58 % (Multi-class)
Table 7 
Model parameters and memory usage.

**Passage 7:**

> wanshi, S.B. Patil, Eﬃcient  brain tumor classiﬁcation with a hybrid CNN-
SVM approach in MRI, J. Adv. Inf. Technol. 15 (2024) 340–354. https://doi.org/10. 12720/jait.15.3.340-354
[20] I. Beheshti, H. Demirel, Feature-ranking-based Alzheimer’s disease classiﬁcation 
from structural MRI, Magn. Reson. Imaging 34 (2016) 252–263. https://doi.org/
10.1016/j.mri.2015.11.009
[21] I. Beheshti, H. Demirel, H. Matsuda, Classiﬁcation of Alzheimer’s disease and predic-
tion of mild cognitive impairment-to-Alzheimer’s conversion from structural mag-
netic resource imaging using feature ranking and a genetic algorithm, Comput. Biol. Med. 83 (2017) 109–119. https://doi.org/10.1016/j.compbiomed.2017.02.011
[22] K.R. Kruthika,  Rajeswari, H.D. Maheshappa, CBIR system using capsule networks 
and 3D CNN for Alzheimer’s disease diagnosis, Inform. Med.

**Passage 8:**

> % (Multi-class)
 [24] (2022)  MRI (ADNI/OASIS)  CNN+SVM  89.4 % (CN vs AD)
 Proposed method  MRI (Kaggle)  CNN+SVM+data augmentation  97.58 % (Multi-class)
Table 7 
Model parameters and memory usage. Parameter Type  Count  Memory Usage
 Total params:  3,581,582  (13.66 MB)
 Trainable params:  1,193,732  (4.55 MB)
 Non-trainable params:  384  (1.50 KB)
 Optimizer params:  2,387,466  (9.11 MB)
ing 97.58 % accuracy on the multi-class Kaggle dataset, highlighting 
the beneﬁt of combining CNN feature extraction with SVM classiﬁca-
tion and data augmentation. In addition, the model maintains moderate 
complexity, with  3.58 million parameters and 43 million FLOPS, while 
remaining low computational cost, with a total training time of 1130.32 
seconds and averaging time of 22.61 seconds per epoch. The system is 
rapid with an inference time of  59 ms per sample.

**Passage 9:**

> akol, M. Azizian, E.Y.K. Ng, Comparison of diﬀerent kernels 
in a support vector machine to classify prostate cancerous tissues in T2-weighted 
magnetic resonance imaging, Explor. Res. Hypothesis Med. 8 (2023) 25–35. https:
//doi.org/10.14218/ERHM.2022.00013
[36] S. Song, Z. Zhan, Z. Long, J. Zhang, L. Yao, Comparative study of SVM methods 
combined with voxel selection for object category classiﬁcation on fMRI data, PLoS 
ONE 6 (2011) 17191. https://doi.org/10.1371/journal.pone.0017191
[37] R. Rifkin, A. Klautau, In defense of one-vs-all classiﬁcation, Mach. Learn. 5 (2004) 
101–141.
[38] J. Cervantes, F. Garcia-Lamont, L. Rodríguez-Mazahua, A. Lopez, A comprehensive 
survey on support vector machine classiﬁcation: applications, challenges and trends, 
Neurocomputing 408 (2020) 189–215. https://doi.org/10.1016/j.neucom.2019.10. 118
[39] A. Khvostikov, K. Aderghal, J. Benois-Pineau, A.

**Passage 10:**

> Risk 
Minimization, 2017. https://doi.org/10.48550/arXiv.1710.09412
[29] Y. Lecun, Y. Bengio, G. Hinton, Deep learning, Nature 521 (2015) 436–444. https:
//doi.org/10.1038/nature14539
[30] E. Yee, D. Ma, K. Popuri, L. Wang, M.F. Beg, Construction of MRI-based Alzheimer’s 
disease score based on eﬃcient  3D convolutional neural network: comprehensive 
validation on 7,902 images from a multi-center dataset, J. Alzheimers Dis. 79 (2021) 
47–58. https://doi.org/10.3233/JAD-200830
[31] T.-Y. Lin, P. Goyal, R. Girshick, K. He, P. Dollar, Focal loss for dense object detec-
tion, in: Proc. IEEE Int. Conf. Comput. Vis, IEEE Int. Conf. Comput. Vis, 2017, pp. 2980–2988.
[32] A. Alhudhaif, K. Polat, Residual block fully connected DCNN with categorical gen-
eralized focal dice loss and its application to Alzheimer’s disease severity detection, 
PeerJ Comput. Sci.

**Passage 11:**

> ddress class imbalances. The model 
achieved 83.82 % accuracy. Sethi et al. [24] combined CNN feature extractor and SVM classiﬁer 
in one hybrid model to predict AD using both ADNI and OASIS datasets. MRI images of 50 subjects for each class (AD, CN, and MCI) were used 
for training, validation, and testing. On the OASIS dataset, the obtained 
accuracy was 86.2 %, and for the ADNI dataset, the testing accuracy 
was 88 %. The highest accuracy was for CN vs AD with 89.4 % value. Rabeh et al. [25] used hybrid pretrained AlexNet network extractor and 
SVM classiﬁer for binary classiﬁcation of 210 NC MRI images and 210 
MCI images, obtained from OASIS database. Impressive accuracy results 
have been shown with a 94.44 % rate. Rahman et al. [26] applied hy-
brid CNN-SVM architecture for the diﬀerentiation of four AD stages, 
presented by Kaggle dataset.

**Passage 12:**

> ing to a technological revolution in the analy-
sis of medical images, which enables automated classiﬁcation of the dis-
∗ Corresponding author. E-mail addresses: wided.hechkel@isimm.u-monastir.tn (W. Hechkel), Missaoui.Rim@ensit.u-tunis.tn (R. Missaoui), abdelhamid.helali@isimm.rnu.tn (A. Helali), 
marco.leo@cnr.it (M. Leo). 1 Principal corresponding author
ease [3]. CNN based models trained on MRI, DTI, and PET images have 
demonstrated promising results in detecting early-stage Alzheimer’s 
[4–8]. However, one of the major drawbacks of adopting a standalone 
CNN has been the high computational complexity of the classiﬁcation 
head, because it uses generally Softmax function which is a fully con-
nected layer and it requires backpropagation to the entire network to 
ﬁnish the classiﬁcation task [9,10].

**Passage 13:**

> M model that 
employs data fusion of MRI and PET 2D images for the early detec-
tion of AD. They enhanced performance of the system by adding at-
tention layers to focus on the most relevant features. The attention-
driven mechanism adopts featured maps to generate dynamic weights 
enabling focused learning. With an accuracy of 98.5 %, the model has 
shown outstanding improvements. Angelica and Suhartono [10] sug-
gested the combination of Xception, the Depthwise Separable Convo-
lutions Deep Learning model with SVM to enhance detection of AD. They work with the Kaggle dataset, using the Synthetic Minority Over-
sampling Technique (SMOTE) to address class imbalances. The model 
achieved 83.82 % accuracy. Sethi et al. [24] combined CNN feature extractor and SVM classiﬁer 
in one hybrid model to predict AD using both ADNI and OASIS datasets.

**Passage 14:**

> ctor machine classiﬁcation: applications, challenges and trends, 
Neurocomputing 408 (2020) 189–215. https://doi.org/10.1016/j.neucom.2019.10. 118
[39] A. Khvostikov, K. Aderghal, J. Benois-Pineau, A. Krylov, G. Catheline, 3D CNN-
Based Classiﬁcation Using SMRI and MD-DTI Images for Alzheimer Disease Studies, 
arxiv:1801.05968 edition, 2018.
[40] N.S. Awarayi, F. Twum, J.B. Hayfron-Acquah, K. Owusu-Agyemang, A bilateral 
ﬁltering-based image enhancement for Alzheimer disease classiﬁcation using CNN, 
PLoS One 19 (2024) 302358. https://doi.org/10.1371/journal.pone.0302358
[41] S. Afzal, et al., A Data Augmentation-Based Framework to Handle Class Imbalance 
Problem for Alzheimer’s Stage Detection
Pattern Recognition Letters 199 (2026) 261–268 
268

**Passage 15:**

> r MD and MoD classes which 
present together only 15 % of the hole dataset, this gap helps to iso-
late the proposed work contribution regarding data imbalances and its 
robustness against overﬁtting. Both the dataset and the custom code and algorithms developed for 
this study will be made publicly available upon publication via a GitHub 
repository. 3.2. Data augmentation
This work proposes to generate augmented images using conven-
tional methods (Table 3) and also using the Mixup method that com-
bines the original image with the augmented same image using one of 
the traditional augmentation methods to generate a new mixed MRI 
slice. Fig. 2 shows some examples of the DA images. Mixup was proposed the ﬁrst time by Zhang et al. in 2017 [28]. The philosophy around this approach is to synthesize new image by 
Fig. 1.

**Passage 16:**

> ed with the 
model, followed by the discussion. The last section rounds up the whole 
paper, recalling the major points, conclusions, and possible areas of fur-
ther research related to this topic. 2. Related work
The ﬁrst systematic study on the detection and classiﬁcation of AD 
using machine learning algorithms was performed between 2016 and 
2017 by Beheshti et al. [20,21]. They analysed MRI data using feature 
ranking and a genetic algorithm in order to predict the progression from 
mild cognitive impairment (MCI) to AD. They obtained an accuracy of 
75 %. In a major advance in 2019, Kruthikaa et al. [22] surveyed a novel 
approach for the early detection of AD, which leverages the strengths 
of multiple deep learning architectures. The process known as Content-
Based Image Retrieval (CBIR) achieved an accuracy of up to 98.42 % in 
AD classiﬁcation even for small datasets.

**Passage 17:**

> nted. The ﬂowchart of the proposed 
strategy is shown in Fig. 3. The following steps are involved:
Pattern Recognition Letters 199 (2026) 261–268 
263 
W. Hechkel et al. Table 2 
Dataset distribution. Classes  No of original samples  Percentage (approx.)  subjects No of Augmented 
images for Training
No of Original 
images for 
Validation
No of Original 
images for Testing
 NonDemented  3200  50 %  100 22528 448 640
 VeryMildDemented  2240  35 %  70 15763 359 448
 MildDemented  896  14 %  28 6292 144 180
 ModerateDemented  64  1 %  2 440 11 13
Total number 6400 100 % 200 45023 962 1281
 47266 images
Table 3 
Parameters of the data augmentation methods. Sr.

**Passage 18:**

> , Conceptualization; Marco Leo:
Writing – review & editing, Writing – original draft, Supervision, Project 
administration, Conceptualization. Data availability
Data will be made available on request. Declaration of competing interest
The authors declare the following ﬁnancial interests/personal rela-
tionships which may be considered as potential competing interests: 
Marco Leo reports ﬁnancial support was provided by Ministero dell’Uni-
versità e della Ricerca (Italy). If there are other authors, they declare that 
they have no known competing ﬁnancial interests or personal relation-
ships that could have appeared to inﬂuence the work reported in this 
paper. Acknoledgements
This research was carried out under the grant Future Artiﬁcial In-
telligence Research–FAIR CUP B53C220036 30,006 funded by the Ital-
ian Ministry for Universities and Research (MUR), grant number MUR: 
PE0000013.

**Passage 19:**

> 2988.
[32] A. Alhudhaif, K. Polat, Residual block fully connected DCNN with categorical gen-
eralized focal dice loss and its application to Alzheimer’s disease severity detection, 
PeerJ Comput. Sci. 9 (2023) 1599. https://doi.org/10.7717/peerj-cs.1599
[33] M. Yeung, E. Sala, C.-B. Schönlieb, L. Rundo, Uniﬁed focal loss: generalising dice 
and cross entropy-based losses to handle class imbalanced medical image segmen-
tation, Comput. Med. Imaging Graph. 95 (2022) 102026. https://doi.org/10.1016/
j.compmedimag.2021.102026
[34] C. Cortes, V. Vapnik, Support-vector networks, Mach. Learn. 20 (1995) 273–297.
[35] A. Shanei, M. Etehadtavakol, M. Azizian, E.Y.K. Ng, Comparison of diﬀerent kernels 
in a support vector machine to classify prostate cancerous tissues in T2-weighted 
magnetic resonance imaging, Explor. Res. Hypothesis Med.

**Passage 20:**

> y or robustness to 
other datasets. Future work will concentrate on addressing these issues 
by generalization across diverse clinical datasets to assess the impact in 
real-world diagnostic practice. CRediT authorship contribution statement
Wided Hechkel: Writing – original draft, Software, Methodology, 
Investigation, Conceptualization; Rim Missaoui: Methodology, Investi-
gation; Abdelhamid Helali: Writing – review & editing, Writing – orig-
inal draft, Supervision, Investigation, Conceptualization; Marco Leo:
Writing – review & editing, Writing – original draft, Supervision, Project 
administration, Conceptualization. Data availability
Data will be made available on request.

**Passage 21:**

> pre-treatment.
 [24]  2022 The hybrid model has shown results on multiple training 
datasets (ADNI and OASIS), which provide a guiding 
selection of the most appropriate datasets for future 
studies. Obtained results need further improvements because they 
don’t show better performance regarding current 
state-of-the-art methods.
 [25]  2023 Good testing results and low execution time, and hence 
low computational complexity of the proposed model. The use of transfer learning depends often on the source 
model, and it lacks the potential of unique characteristics 
of the customized CNN.
 [26]  2024 Reduced computational complexity due to the lightweight 
CNN stage adopted in the hybrid model, which contains 
three convolutional layers. The perfection of obtained accuracies over the diﬀerent 
stages, which is close to 100 %, indicates a risk of 
overﬁtting. 3. Material and methods
3.1.

**Passage 22:**

> Contents lists available at ScienceDirect
Pattern Recognition Letters
journal homepage: www.elsevier.com/locate/patrec
Hybrid CNN and SVM model for Alzheimer’s disease classiﬁcation using 
categorical focal loss function 
Wided Hechkel
 a, Rim Missaoui
 a,b, Abdelhamid Helali
 a, Marco Leo
 c,1,∗
a Laboratory of Micro-Optoelectronics and Nanostructures (LMON), University of Monastir Avenue of the Environment, Monastir, Monastir, 5019, Tunisia
b University of Tunis, National High School of Engineering of Tunis (ENSIT), 5, Rue Taha Hussein-Montﬂeury, Tunis, Tunis, 1008, Tunisia
c National Research Council of Italy, Institute of Applied Sciences and Intelligent Systems, Lecce, Lecce, 73100, Italy
a r t i c l e  i n f o
Editor: Maria De Marsico
Keywords:
Alzheimer’s disease (AD)
Early diagnosis
MRI
Convolutional neural network (CNN)
Support vector machine (SVM)
Hybrid model
Reduced complexity
 a b s t r a c t
Alzheimer’s disease (AD) is the leading cause of dementia worldwide.

**Passage 23:**

> d 98.94 % 
speciﬁcity, which enables early detection, handling class imbalance, and 
low-cost computational complexity. These ﬁndings add to a growing 
body of literature on the early detection of AD. Finally, a number of 
potential limitations need to be considered. While the proposed hybrid 
CNN-SVM model achieves high accuracy, quantiﬁcation of the compu-
tational eﬃciency  of the SVM module is not fully reported, which limits 
the assessment of practical feasibility. Moreover, practical translation 
into clinical settings faces challenges such as interpretability because 
there is no discussion of the model generalizability or robustness to 
other datasets. Future work will concentrate on addressing these issues 
by generalization across diverse clinical datasets to assess the impact in 
real-world diagnostic practice.

**Passage 24:**

> arly diagnosis
MRI
Convolutional neural network (CNN)
Support vector machine (SVM)
Hybrid model
Reduced complexity
 a b s t r a c t
Alzheimer’s disease (AD) is the leading cause of dementia worldwide. It attacks the elderly population, causing 
a dangerous cognitive decline and memory loss due to the degeneration and atrophy of brain neurons. Recent 
developments in machine learning techniques for the detection and classiﬁcation of AD boost the early diagnosis 
and enable slowing the disease by adopting preclinical treatments. However, a major defect of these techniques 
is their high complexity architectures and their less generalizability, which provokes diﬃculties  in clinical in-
tegration. This paper presents a new approach that combines convolutional neural network (CNN) and support 
vector machines (SVM) for the detection of AD.

</details>

---

## Lao et al. (2024) — Diagnosis of Alzheimer's Disease Based on Structural Graph Convolutional Neural Networks
_File: `Lao et al. - 2024 - Diagnosis of Alzheimer's Disease Based on Structural Graph Convolutional Neural Networks.pdf`_

1. **Was diffusion MRI (DTI, dMRI, DWI, or similar) used in this paper?**  
   **NO DIFFUSION MRI PROCESSING FOUND**  

2. **What processing steps were applied to the diffusion images?**  
   Not applicable (no diffusion MRI processing mentioned).  

3. **What software or tools are explicitly named for processing?**  
   Not applicable (no diffusion MRI processing mentioned).  

4. **What acquisition or processing parameters are explicitly reported?**  
   Not applicable (no diffusion MRI processing mentioned).  

5. **Copy the exact sentences from the excerpts that describe the processing.**  
   Not applicable (no diffusion MRI processing mentioned).  

6. **Is the processing description complete, or does it appear incomplete/missing?**  
   **NO DIFFUSION MRI PROCESSING FOUND**

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> the Computation Anatomy Toolbox (CAT12) toolkit to
perform skull stripping, tissue segmentation, and alignment and
modulation operations, and obtained a gray matter image (GM-MRI)
of size 121×145×121. For all FDG PET images, we used the "FLIRT"
module in FMRIB Software Library (FSL) software to register the
FDG PET images of each subject onto their respective preprocessed
sMRI images. The demographic information for all subjects is shown
in Table 1. 3 METHOD
This study focuses on different modal images (3D sMRI images and
3D FDG PET images) and constructs a GCN network to classify AD
and CN. The classification framework is shown in Figure 1. 3.1 Three-Dimensional Discrete Wavelet
Transform
The three-dimensional discrete wavelet transform (3D-DWT) is an
extension of 2D-DWT, which considers the correlation between
three-dimensional data [2].

**Passage 2:**

> pathogenesis of AD and develops treatment methods
that delay or prevent its progression. As of 2023, the ADNI dataset
has undergone four stages of research, namely ADNI-1, ADNI-GO,
ADNI-2, and ADNI-3. This study selected 325 subjects with both
baseline sMRI images and baseline FDG PET images from the ADNI-
2 stage, including 144 AD subjects and 181 CN subjects. The formats
of the sMRI images and FDG PET images were "MT1; GradWarp;
N3m" and "Coreg, Avg, Std Img and Vox Siz, Uniform Resolution",
respectively. For all sMRI images, we used the "Segment Data"
module in the Computation Anatomy Toolbox (CAT12) toolkit to
perform skull stripping, tissue segmentation, and alignment and
modulation operations, and obtained a gray matter image (GM-MRI)
of size 121×145×121.

**Passage 3:**

> l Networks ACM-TURC ’24, July 05–07, 2024, Changsha, China
unified standards, while our method only used imaging data for
classification. In the future, we will combine more modal data to
classify AD. ACKNOWLEDGMENTS
The data used in preparation of this study was obtained from the
Alzheimer’s Disease Neuroimaging Initiative(ADNI). As such, the
investigators within the ADNI contributed to the design and imple-
mentation of ADNI and/or provided data, but did not participate in
the analysis or writing of this report.

**Passage 4:**

> 022), 3948–3964. https://doi.org/10.1049/ipr2.12605
[6] Huan Lao and Xuejun Zhang. 2022. Regression and Classification of Alzheimer’s
Disease Diagnosis Using NMF-TDNet Features From 3D Brain MR Image. IEEE
Journal of Biomedical and Health Informatics 26, 3 (2022), 1103–1115. https:
//doi.org/10.1109/JBHI.2021.3113668
[7] Chunfeng Lian, Mingxia Liu, Jun Zhang, and Dinggang Shen. 2020. Hierarchical
Fully Convolutional Network for Joint Atrophy Localization and Alzheimer’s
Disease Diagnosis Using Structural MRI. IEEE Transactions on Pattern Analysis
and Machine Intelligence 42, 4 (2020), 880–893. https://doi.org/10.1109/TPAMI. 2018.2889096
[8] Mingxia Liu, Jun Zhang, Pew-Thian Yap, and Dinggang Shen. 2017. View-aligned
hypergraph learning for Alzheimer’s disease diagnosis with incomplete multi-
modality data. Medical Image Analysis 36 (2017), 123–134. https://doi.org/10.

**Passage 5:**

> 372011
[10] P. Padilla, M. Lopez, J. M. Gorriz, J. Ramirez, D. Salas-Gonzalez, and I. Alvarez. 2012. NMF-SVM Based CAD Tool Applied to Functional Brain Images for the
Diagnosis of Alzheimer’s Disease. IEEE Transactions on Medical Imaging 31, 2
(2012), 207–216. https://doi.org/10.1109/TMI.2011.2167628
[11] Yongsheng Pan, Mingxia Liu, Chunfeng Lian, Tao Zhou, Yong Xia, and Ding-
gang Shen. 2018. Synthesizing Missing PET from MRI with Cycle-consistent
Generative Adversarial Networks for Alzheimer’s Disease Diagnosis. InMedical
Image Computing and Computer Assisted Intervention – MICCAI 2018 , Alejandro F. Frangi, Julia A. Schnabel, Christos Davatzikos, Carlos Alberola-López, and Gabor
Fichtinger (Eds.). Springer International Publishing, Cham, 455–463.
[12] Yue Wang, Yongbin Sun, Ziwei Liu, Sanjay E. Sarma, Michael M. Bronstein, and
Justin M. Solomon. 2019.

**Passage 6:**

> lberola-López, and Gabor
Fichtinger (Eds.). Springer International Publishing, Cham, 455–463.
[12] Yue Wang, Yongbin Sun, Ziwei Liu, Sanjay E. Sarma, Michael M. Bronstein, and
Justin M. Solomon. 2019. Dynamic Graph CNN for Learning on Point Clouds. ACM Trans. Graph. 38, 5, Article 146 (oct 2019), 12 pages. https://doi.org/10. 1145/3326362
[13] Jun Zhang, Yue Gao, Yaozong Gao, Brent C. Munsell, and Dinggang Shen. 2016. Detecting Anatomical Landmarks for Fast Alzheimer’s Disease Diagnosis. IEEE
Transactions on Medical Imaging 35, 12 (2016), 2524–2533. https://doi.org/10. 1109/TMI.2016.2582386
[14] Jun Zhang, Mingxia Liu, Le An, Yaozong Gao, and Dinggang Shen. 2017. Alzheimer’s Disease Diagnosis Using Landmark-Based Features From Longi-
tudinal Structural MR Images. IEEE Journal of Biomedical and Health Informatics
21, 6 (2017), 1607–1616. https://doi.org/10.1109/JBHI.2017.2704614
152

**Passage 7:**

> odality 3D Convolutional Neural Network.Fron-
tiers in Neuroscience 13 (2019), 1–12. https://doi.org/10.3389/fnins.2019.00509
[4] I.A. Illán, J.M. Górriz, J. Ramírez, D. Salas-Gonzalez, M.M. López, F. Segovia, R. Chaves, M. Gómez-Rio, and C.G. Puntonet. 2011. 18F-FDG PET imaging analysis
for computer aided Alzheimer’s diagnosis. Information Sciences 181, 4 (2011),
903–916. https://doi.org/10.1016/j.ins.2010.10.027
[5] Huan Lao and Xuejun Zhang. 2022. Diagnose Alzheimer’s disease by combining
3D discrete wavelet transform and 3D moment invariants. IET Image Processing
16, 14 (2022), 3948–3964. https://doi.org/10.1049/ipr2.12605
[6] Huan Lao and Xuejun Zhang. 2022. Regression and Classification of Alzheimer’s
Disease Diagnosis Using NMF-TDNet Features From 3D Brain MR Image.

**Passage 8:**

> ngsha, China Lao et al. Figure 4: Schematic diagram of graph structure for each subject. Table 2: Comparison of the classification accuracy of our method with the existing methods
Method Images
AD vs. CN Classification Results(%)
ACC SEN SPE AUC
Lian et al.[7] sMRI 90.3 82.4 96.5 95.1
Zhang et al.[13] sMRI 83.7 80.9 86.7 -
Zhang et al.[14] sMRI 88.3 79.61 94.69 94.01
Proposed method sMRI 90.56 89.58 91.75 96.13
Illán et al.[4] FDG PET 88.24 88.64 87.7 -
Padilla et al.[10] FDG PET 86.59 87.5 85.36 -
Proposed method FDG PET 90.87 92.55 88.26 94.97
Liu et al.[8] sMRI+FDG PET 93.1 90 95.65 94.83
Huang et al.[3] sMRI+FDG PET 90.1 90.85 89.21 90.84
Pan et al.[11] sMRI+FDG PET 92.5 89.94 94.53 95.89
Proposed method sMRI+FDG PET 93.12 94.85 90.42 97.08
using the ADNI dataset, and the ADNI research group conducted
quality control and preprocessing on the images.

**Passage 9:**

> chine learning for AD classification has become a
research hotspot. However, most AD classification studies based
on brain image and machine learning only use single-modality
brain image for research. For example, Lian et al.[ 7] proposed a
hierarchical fully convolutional network (H-FCN) to automatically
recognize region of interest(ROI) positions in sMRI images for con-
structing AD classification. Zhang et al. [13, 14] used sMRI images
and Support Vector Machines (SVM) for AD classification. While
Illán et al. [4] and Padilla et al.[10] only used FDG-PET images and
SVM for AD classification. In recent years, an increasing number
of studies have shown that different modal images can provide
supplementary information [1, 9]. Among them, sMRI images can
provide structural information of the patient’s brain, and FDG-PET
images can provide metabolic information of the patient’s brain.

**Passage 10:**

> iative(ADNI). As such, the
investigators within the ADNI contributed to the design and imple-
mentation of ADNI and/or provided data, but did not participate in
the analysis or writing of this report. This work was supported by the Guangxi Minzu University Sci-
entific Research Fund Grant Project (Scientific Research Initiation
Project for Introduced Talents & 2022KJQD21), the Research Fund
of Guangxi Key Lab of Multi-source Information Mining & Secu-
rity (MIMS22-09), and the Project of Improving the Basic Scientific
Research Ability of Young and Middle-Aged Teachers in Guangxi
Universities(2023KY0170). REFERENCES
[1] Yanjiao Ban, Huan Lao, Bin Li, Wenjun Su, and Xuejun Zhang. 2023. Diagnosis
of Alzheimer’s disease using hypergraph p-Laplacian regularized multi-task
feature learning.

**Passage 11:**

> an Yap, and Dinggang Shen. 2017. View-aligned
hypergraph learning for Alzheimer’s disease diagnosis with incomplete multi-
modality data. Medical Image Analysis 36 (2017), 123–134. https://doi.org/10. 1016/j.media.2016.11.002
[9] Siqi Liu, Sidong Liu, Weidong Cai, Hangyu Che, Sonia Pujol, Ron Kikinis, Dagan
Feng, Michael J. Fulham, and ADNI. 2015. Multimodal Neuroimaging Feature
Learning for Multiclass Diagnosis of Alzheimer’s Disease. IEEE Transactions on
Biomedical Engineering 62, 4 (2015), 1132–1140. https://doi.org/10.1109/TBME. 2014.2372011
[10] P. Padilla, M. Lopez, J. M. Gorriz, J. Ramirez, D. Salas-Gonzalez, and I. Alvarez. 2012. NMF-SVM Based CAD Tool Applied to Functional Brain Images for the
Diagnosis of Alzheimer’s Disease.

**Passage 12:**

> sMRI+FDG PET 92.5 89.94 94.53 95.89
Proposed method sMRI+FDG PET 93.12 94.85 90.42 97.08
using the ADNI dataset, and the ADNI research group conducted
quality control and preprocessing on the images. It can be observed
from Table 2 that our proposed method outperforms some existing
methods in AD and CN classification. Specifically, the classifica-
tion accuracy of our proposed method is greater than 90% with
both single-modality image and multi-modality images. Compared
with the classification method using sMRI images, our proposed
method achieves a classification accuracy of 90.56%, which is 0.26%,
6.86%, and 2.26% higher than existing methods[ 7, 13, 14] . Com-
pared with the classification method using FDG PET images[4, 10] ,
the classification accuracy of our proposed method is improved by
2.63% and 4.28%.

**Passage 13:**

> . 
. Latest updates: hps://dl.acm.org/doi/10.1145/3674399.3674453
. 
. RESEARCH-ARTICLE
Diagnosis of Alzheimer's Disease Based on Structural Graph
Convolutional Neural Networks
HUAN LAO, Guangxi University for Nationalities, Nanning, Guangxi, China
. HONGFEI JIA
. ZHENHAI CHEN, Guangxi University for Nationalities, Nanning, Guangxi, China
. 
. 
. Open Access Support provided by:
. Guangxi University for Nationalities
. PDF Download
3674399.3674453.pdf
15 February 2026
Total Citations: 1
Total Downloads: 427
. 
. Published: 05 July 2024
. 
. Citation in BibTeX format
. 
. ACM-TURC '24: ACM Turing Award
Celebration Conference 2024
July 5 - 7, 2024
Changsha, China
. 
. ACM-TURC '24: Proceedings of the ACM Turing Award Celebration Conference - China 2024 (July 2024)
hps://doi.org/10.1145/3674399.3674453
ISBN: 9798400710117
.

**Passage 14:**

> ication. To validate
the effectiveness of the proposed method, we conducted classifi-
cation experiments using baseline sMRI images and baseline FDG
PET images from 325 subjects on the ADNI-2 dataset. The experi-
mental results show that the proposed method can jointly extract
common features of multi-modality brain images and has better
classification performance than existing methods. However, our
method still has certain limitations. For example, the ADNI dataset
collected demographic, neuropsychological, imaging, genetic, cere-
brospinal fluid, and blood data from various subjects according to
151
Diagnosis of Alzheimer’s Disease Based on Structural Graph Convolutional Neural Networks ACM-TURC ’24, July 05–07, 2024, Changsha, China
unified standards, while our method only used imaging data for
classification. In the future, we will combine more modal data to
classify AD.

**Passage 15:**

> ctivation function ℎ. This function is implemented by
a multi-layer perceptron (MLP) with a corrected linear unit (ReLU). 4 EXPERIMENTS
To validate the effectiveness of our method, we conducted AD vs. CN classification experiments on the ADNI-2 dataset. The experi-
ment used 10-fold cross validation to avoid the impact of bias caused
by randomly dividing the dataset on classification performance. The
classification performance was evaluated using classification ac-
curacy (ACC), sensitivity (SEN), specificity (SPE), and area under
the receiver operating characteristic curve (AUC). The experimen-
tal results are shown in Table 2.

**Passage 16:**

> sulting in four decomposed subbands (LL, LH, HL and HH). Then
each of these four subbands are filtered along the 𝑧-dimension, re-
sulting in eight subbands (LLL, LLH, LHL, LHH, HLL, HLH, HHL
and HHH). Among them, LLL is an approximation of the 3D im-
age and usually contains more information about the image. The
other seven subbands are detail components that only contain the
detailed information of the image. In this study, we divided the
GM-MRI images and FDG PET images of each subject into 90 ROIs
using the automated anatomic labeling (AAL) brain atlas. Then,
apply the three-level 3D-DWT to each ROI and use the decomposed
LLL subband of each ROI as the final feature representation. The
two-level 3D-DWT is achieved by decomposing the approximate
component of the one-level 3D-DWT, while the three-level 3D-
DWT is achieved by decomposing the approximate component of
the two-level 3D-DWT.

**Passage 17:**

> o-level 3D-DWT is achieved by decomposing the approximate
component of the one-level 3D-DWT, while the three-level 3D-
DWT is achieved by decomposing the approximate component of
the two-level 3D-DWT. 3.2 Construction of Structural Graph
A graph is a type of non-euclidean space data that consists of nodes
and edges, including node information and relationship information
between different nodes. Graphs are ubiquitous in the real world,
such as social networks, citation networks and biological networks. They usually use a single sample as a node and the relationship
between samples as a connection to build a graph. In this study,
when constructing a graph, ROIs are used as the node of the graph. When ROIs have actual positional contact relationships, their cor-
responding nodes are connected to form the edges of the graph.

**Passage 18:**

> dy,
when constructing a graph, ROIs are used as the node of the graph. When ROIs have actual positional contact relationships, their cor-
responding nodes are connected to form the edges of the graph. Suppose that 𝑋1 and 𝑋2 represent the set of non-zero pixel position
values of the two ROIs respectively, then the actual position contact
relation 𝐴1,2 between the two ROIs can be expressed by finding the
intersection between 𝑋1 and 𝑋2, the formula is as follows:
𝐴1,2 =
 0, 𝑋 1 ∩ 𝑋2 = ∅
1, 𝑋 1 ∩ 𝑋2 ≠ ∅ (1)
According to formula (1), create a matrix based on the actual po-
sitional contact relationship between ROIs to reflect the correlation
between different ROIs, and use it as the adjacency matrix 𝐴 of the
graph (as shown in Figure 3). Then, the 3D-DWT features of differ-
ent modal images are used as node features of the graph. Finally,
the structural graph of each subject is constructed.

**Passage 19:**

> .1 Three-Dimensional Discrete Wavelet
Transform
The three-dimensional discrete wavelet transform (3D-DWT) is an
extension of 2D-DWT, which considers the correlation between
three-dimensional data [2]. Therefore, performing 3D-DWT decom-
position on 3D images helps to understand the detailed information
of different directions in 3D images. The schematic diagram of
using one-level 3D-DWT to decompose 3D images is shown in
Figure 2. Specifically, each 3D image volume is firstly filtered along
the 𝑥-dimension, resulting in a low-pass image L and a high-pass
image H. Both L and H are then filtered along the 𝑦-dimension,
resulting in four decomposed subbands (LL, LH, HL and HH). Then
each of these four subbands are filtered along the 𝑧-dimension, re-
sulting in eight subbands (LLL, LLH, LHL, LHH, HLL, HLH, HHL
and HHH).

**Passage 20:**

> 6% higher than existing methods[ 7, 13, 14] . Com-
pared with the classification method using FDG PET images[4, 10] ,
the classification accuracy of our proposed method is improved by
2.63% and 4.28%. Compared with the classification method using
multi-modality images[3, 8, 11], the classification accuracy of our
proposed method is improved by 3.02%, 0.02% and 0.62%. 5 CONCLUSION
In this study, we propose a structure graph convolutional neural
network method for classifying AD and CN, including data prepro-
cessing, 3D-DWT feature extraction, structure graph construction,
and graph convolutional neural network classification. To validate
the effectiveness of the proposed method, we conducted classifi-
cation experiments using baseline sMRI images and baseline FDG
PET images from 325 subjects on the ADNI-2 dataset.

**Passage 21:**

> Table 2, we compared the classification results of
the proposed method with the existing AD classification methods
based on single-modality image[4, 7, 10, 13, 14] and multi-modality
images[3, 8, 11]. In order to ensure the optimal classification perfor-
mance for each method, the classification results for each method
in the table are the best results obtained by experiments on its
original selected subset of data. That is to say, the number of sub-
jects and the division of training and testing samples are different
between these methods. Although the selection of images by all
comparison methods is not entirely the same, they were all studied
150
ACM-TURC ’24, July 05–07, 2024, Changsha, China Lao et al. Figure 4: Schematic diagram of graph structure for each subject. Table 2: Comparison of the classification accuracy of our method with the existing methods
Method Images
AD vs.

**Passage 22:**

> 024
July 5 - 7, 2024
Changsha, China
. 
. ACM-TURC '24: Proceedings of the ACM Turing Award Celebration Conference - China 2024 (July 2024)
hps://doi.org/10.1145/3674399.3674453
ISBN: 9798400710117
. Diagnosis of Alzheimer’s Disease Based on Structural Graph
Convolutional Neural Networks
Huan Lao∗
laohuanlh@gxmzu.edu.cn
School of Artificial Intelligence,
Guangxi Minzu University
Guangxi Key Lab of Multi-source
Information Mining & Security
Nanning, Guangxi, China
Hongfei Jia
Beijing ZhongkeHaixun Digital
Technology Co.,Ltd
Beijing, China
Zhenhai Chen
School of Artificial Intelligence,
Guangxi Minzu University
Nanning, Guangxi, China
ABSTRACT
In recent years, classification methods based on multi-modality
images have been widely applied in the diagnosis of Alzheimer’s
Disease(AD), and have achieved better performance than methods
based on single-modality image.

**Passage 23:**

> ± 4.51
Note. Data are presented as mean and standard deviation; MMSE=Mini-Mental State Examination; ADAS-Cog=Alzheimer’s Disease Assessment Scale-Cognitive. Figure 1: Classification Framework Diagram. Figure 2: Diagram of one-level 3D-DWT decomposition. Figure 3: Schematic diagram of adjacency matrix.
is chosen as the convolution operation of the graph convolution
layer:
𝑥
′
𝑖 = max ℎΘ (𝑥𝑖 ||𝑥 𝑗 − 𝑥𝑖 ) (2)
Where 𝑥𝑖 is the feature of node 𝑖, and 𝑥 𝑗 is the feature of the
connected adjacent node 𝑗. In addition to the original features from
the nodes, the difference between the nodes (𝑥 𝑗 −𝑥𝑖) is also appended
as complementary features. ℎ𝜃 represents a trainable weight𝜃 with
a nonlinear activation function ℎ. This function is implemented by
a multi-layer perceptron (MLP) with a corrected linear unit (ReLU). 4 EXPERIMENTS
To validate the effectiveness of our method, we conducted AD vs.

**Passage 24:**

> puting → Imaging; Bioinformatics. KEYWORDS
Alzheimer’s disease, graph convolutional neural networks, multi-
modality classification
ACM Reference Format:
Huan Lao, Hongfei Jia, and Zhenhai Chen. 2024. Diagnosis of Alzheimer’s
Disease Based on Structural Graph Convolutional Neural Networks. InACM
Turing A ward Celebration Conference 2024 (ACM-TURC ’24), July 05–07, 2024,
Changsha, China. ACM, New York, NY, USA, 5 pages. https://doi.org/10. 1145/3674399.3674453
Permission to make digital or hard copies of all or part of this work for personal or
classroom use is granted without fee provided that copies are not made or distributed
for profit or commercial advantage and that copies bear this notice and the full citation
on the first page. Copyrights for third-party components of this work must be honored. For all other uses, contact the owner/author(s).

</details>

---

## Leveraging Swin Transformer for enhanced diagnosis of Alzheimer-s disease using multi-shell diffusion MRI
_File: `Leveraging Swin Transformer for enhanced diagnosis of Alzheimer-s disease using multi-shell diffusion MRI.pdf`_

1. **Yes**, diffusion MRI (dMRI) was used in this paper. The text explicitly mentions "dMRI data" and "multi-shell dMRI data," and references DTI and NODDI models as part of the analysis.

2. **Processing steps in order**:  
   - "The preprocessing began with MP-PCA denoising [27], applied through MRtrix3’s dwidenoise function (version 3.0.3) [28]."  
   - "Following denoising, FSL’s eddy tool (version 6.0.7) [29] was employed for both head motion correction and eddy current correction."  
   - "Additionally, b=0 reference images were processed alongside T1-weighted images using Synb0disco [30] to estimate the susceptibility-induced off-resonance field."  
   - "These field maps were then integrated into the eddy correction process, ensuring that both eddy current and head motion were accurately corrected during the interpolation phase."  
   - "Finally, post-eddy alignment of shells was performed to further refine the data, ensuring precise spatial consistency across all diffusion-weighted images."  
   - "After preprocessing, microstructural models were derived from the multi-shell dMRI data, and three key metrics were selected for each model as inputs to the Swin Transformer."

3. **Software/tools explicitly named**:  
   - ElikoPy [26]  
   - MRtrix3’s dwidenoise function (version 3.0.3) [28]  
   - FSL’s eddy tool (version 6.0.7) [29]  
   - Synb0disco [30]

4. **Acquisition/processing parameters**:  
   - **b-values**: 6 directions at b=500, 48 at b=1000, 60 at b=2000, and 13 b=0 acquisitions (total 127 measurements).  
   - **Voxel size**: 2.0 × 2.0 × 2.0 mm for dMRI scans; 1.0 × 1.0 × 1.0 mm for T1-weighted scans.  
   - **Matrix size**: 116 × 116 × 81 pixels for dMRI scans; 240 × 256 × 208 pixels for T1-weighted scans.  
   - **Acquisition parameters**: TE = 71.0 ms, TR = 3400.0 ms, flip angle = 90 degrees for dMRI; TE = 3.0 ms, TR = 2300.0 ms, inversion time = 900.0 ms, flip angle = 9 degrees for T1-weighted scans.

5. **Exact sentences describing processing**:  
   - "The preprocessing of diffusion MRI data was performed using ElikoPy [26], incorporating a series of specialized algorithms to ensure high-quality data suitable for subsequent analysis."  
   - "The preprocessing began with MP-PCA denoising [27], applied through MRtrix3’s dwidenoise function (version 3.0.3) [28]."  
   - "Following denoising, FSL’s eddy tool (version 6.0.7) [29] was employed for both head motion correction and eddy current correction."  
   - "Additionally, b=0 reference images were processed alongside T1-weighted images using Synb0disco [30] to estimate the susceptibility-induced off-resonance field."  
   - "These field maps were then integrated into the eddy correction process, ensuring that both eddy current and head motion were accurately corrected during the interpolation phase."  
   - "Finally, post-eddy alignment of shells was performed to further refine the data, ensuring precise spatial consistency across all diffusion-weighted images."  
   - "After preprocessing, microstructural models were derived from the multi-shell dMRI data, and three key metrics were selected for each model as inputs to the Swin Transformer."

6. **Processing description completeness**:  
   The processing steps are explicitly described in order, including denoising, motion

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> the dMRI data
The preprocessing of diffusion MRI data was performed
using ElikoPy [26], incorporating a series of specialized
algorithms to ensure high-quality data suitable for subse-
quent analysis. The preprocessing began with MP-PCA de-
noising [27], applied through MRtrix3’s dwidenoise function
(version 3.0.3) [28]. Following denoising, FSL’s eddy tool
(version 6.0.7) [29] was employed for both head motion
correction and eddy current correction. Additionally, b=0 ref-
erence images were processed alongside T1-weighted images
using Synb0disco [30] to estimate the susceptibility-induced
off-resonance field. These field maps were then integrated
into the eddy correction process, ensuring that both eddy
current and head motion were accurately corrected during the
interpolation phase.

**Passage 2:**

> d
off-resonance field. These field maps were then integrated
into the eddy correction process, ensuring that both eddy
current and head motion were accurately corrected during the
interpolation phase. Finally, post-eddy alignment of shells was
performed to further refine the data, ensuring precise spatial
consistency across all diffusion-weighted images. After preprocessing, microstructural models were derived
from the multi-shell dMRI data, and three key metrics were
selected for each model as inputs to the Swin Transformer. For
DTI, the metrics included Fractional Anisotropy (FA), which
measures the degree of anisotropy in water diffusion; Axial
Diffusivity (AxD), indicating water diffusion along the princi-
pal axis of the diffusion tensor; and Radial Diffusivity (RD),
representing diffusion perpendicular to the principal axis.

**Passage 3:**

> using random matrix theory,”
Neuroimage, vol. 142, pp. 394–406, 2016.
[28] J.-D. Tournier, R. Smith, D. Raffelt, R. Tabbara, T. Dhollander,
M. Pietsch, D. Christiaens, B. Jeurissen, C.-H. Yeh, and A. Connelly,
“Mrtrix3: A fast, flexible and open software framework for medical
image processing and visualisation,”Neuroimage, vol. 202, p. 116137,
2019.
[29] J. L. Andersson and S. N. Sotiropoulos, “An integrated approach to
correction for off-resonance effects and subject movement in diffusion
mr imaging,”Neuroimage, vol. 125, pp. 1063–1078, 2016.
[30] K. G. Schilling, J. Blaber, Y . Huo, A. Newton, C. Hansen, V . Nath, A. T. Shafer, O. Williams, S. M. Resnick, B. Rogers,et al., “Synthesized b0
for diffusion distortion correction (synb0-disco),”Magnetic resonance
imaging, vol. 64, pp. 62–70, 2019.
[31] J. Deng, W. Dong, R. Socher, L.-J. Li, K. Li, and L.

**Passage 4:**

> of `u, R. Anglani, and F. Vitulano, “An Ensem-
ble Learning Approach Based on Diffusion Tensor Imaging Measures
for Alzheimer’s Disease Classification,”Electronics, vol. 10, p. 249, Jan. 2021.
[25] H. Zhang, T. Schneider, C. A. Wheeler-Kingshott, and D. C. Alexander,
“NODDI: Practical in vivo neurite orientation dispersion and density
imaging of the human brain,”NeuroImage, vol. 61, pp. 1000–1016, July
2012.
[26] Q. Dessain, M. Simon, and N. Delinte, “Hyedryn/elikopy: v0.4.5,” Apr. 2024.
[27] J. Veraart, D. S. Novikov, D. Christiaens, B. Ades-Aron, J. Sijbers, and
E. Fieremans, “Denoising of diffusion mri using random matrix theory,”
Neuroimage, vol. 142, pp. 394–406, 2016.
[28] J.-D. Tournier, R. Smith, D. Raffelt, R. Tabbara, T. Dhollander,
M. Pietsch, D. Christiaens, B. Jeurissen, C.-H. Yeh, and A.

**Passage 5:**

> encourages the model
to learn features that are invariant to the precise spatial
positioning of brain structures, enhancing its generalizability
without relying on registration to a standard template. This article has been accepted for publication in IEEE Transactions on Biomedical Engineering. This is the author's version which has not been fully edited and 
content may change prior to final publication. Citation information: DOI 10.1109/TBME.2025.3636745
This work is licensed under a Creative Commons Attribution 4.0 License. For more information, see https://creativecommons.org/licenses/by/4.0/
4 IEEE TRANSACTIONS ON BIOMEDICAL ENGINEERING, VOL. XX, NO. XX, XXXX 2023
Fig. 1. Overview of the proposed architecture. The 3D microstructural maps derived from diffusion MRI data are projected into 2D slices, which
serve as input to the Swin Transformer pre-trained on ImageNet.

**Passage 6:**

> nd an inversion time of 900.0 ms. The flip angle
was set to 9 degrees, and the matrix size was 240 × 256 ×
208 pixels. TABLE I
DEMOGRAPHIC CHARACTERISTICS OF SELECTED PARTICIPANTS FROM
THEADNIDATASET. WHEN AVAILABLE,SUBJECTS WERE FURTHER
SUBCLASSIFIED BY AMYLOID BETA(Aβ)STATUS INTOAβ − ANDAβ +. AD MCI CN
Number of subjects 37 121 213
Amyloid status (Aβ −/Aβ+) 0/17 42/40 107/54
Sex (Male/Female) 17/20 65/56 72/141
Age (Mean±SD)77.2±6.9 73.3±7.2 72.9±8.7
A total of 371 participants were included after preprocess-
ing, comprising 37 individuals diagnosed with AD, 121 with
MCI, and 213 CN subjects. The demographic characteristics
are summarized in Table I. B. Processing the dMRI data
The preprocessing of diffusion MRI data was performed
using ElikoPy [26], incorporating a series of specialized
algorithms to ensure high-quality data suitable for subse-
quent analysis.

**Passage 7:**

> ata present significant challenges for tradi-
tional analysis methods. Deep learning has shown promise
in automating feature extraction and classification from high-
dimensional neuroimaging data [2]. Convolutional Neural Net-
works (CNNs), in particular, have demonstrated substantial
success in medical image analysis, including brain MRI tasks,
due to their ability to capture local spatial features [3]. These
approaches have been successfully applied to structural MRI
(sMRI) and functional MRI (fMRI) for Alzheimer’s disease
classification [4], with models such as hierarchical fully con-
volutional networks extracting multi-scale features from sMRI
[5] and spatiotemporal 3D CNNs capturing dynamics in fMRI
data [6].

**Passage 8:**

> as not been fully edited and 
content may change prior to final publication. Citation information: DOI 10.1109/TBME.2025.3636745
This work is licensed under a Creative Commons Attribution 4.0 License. For more information, see https://creativecommons.org/licenses/by/4.0/
AUTHORet al.: PREPARATION OF PAPERS FOR IEEE TRANSACTIONS AND JOURNALS (JUL Y 2025) 9
and compute, and large-scale pretraining is less accessible for
dMRI [49], [50]. Multi-orientation ensembles broaden con-
textual coverage with modest overhead but still lack explicit
through-plane continuity [42], [51], [52]. As multi-shell dMRI
and longitudinal labels grow, it will be possible to perform a
controlled comparison of these options to quantify incremental
value over the current 2D baseline. Another limitation in our amyloid analysis relates to the
sample size and dataset composition.

**Passage 9:**

> as not been fully edited and 
content may change prior to final publication. Citation information: DOI 10.1109/TBME.2025.3636745
This work is licensed under a Creative Commons Attribution 4.0 License. For more information, see https://creativecommons.org/licenses/by/4.0/
AUTHORet al.: PREPARATION OF PAPERS FOR IEEE TRANSACTIONS AND JOURNALS (JUL Y 2025) 5
1) dMRI model study:To assess the impact of different mi-
crostructural dMRI models on the performance of the proposed
Swin Transformer-based architecture, we conducted experi-
ments utilizing two common dMRI models: DTI and NODDI. These models were chosen to highlight the differences between
a single-shell model (DTI) and a multi-shell model (NODDI),
reflecting their distinct capabilities in capturing microstructural
characteristics relevant to Alzheimer’s disease classification.

**Passage 10:**

> NI repository. The dataset
includes scans from participants categorized into three di-
agnostic groups: Cognitively Normal (CN), Mild Cognitive
Impairment (MCI), and Alzheimer’s disease Dementia (AD). To leverage metrics from multi-shell models, single-shell
dMRI acquisitions present in the ADNI dataset were ex-
cluded. All scans were acquired using a 3.0 Tesla Siemens
MAGNETOM Prisma/Prismafit scanner with a 2D echo-planar
sequence. The voxel size was 2.0 × 2.0 × 2.0 mm. The
acquisition parameters included an echo time (TE) of 71.0
ms, a repetition time (TR) of 3400.0 ms, and a flip angle of
90 degrees. The diffusion-weighted imaging protocol had 6
gradient directions atb= 500, 48 directions atb= 1000
and 60 directions atb= 2000µsµm −2, along with 13b= 0
acquisitions, for a total of 127 measurements. The matrix size
for the scans was 116 × 116 × 81 pixels.

**Passage 11:**

> ility to maintain high-resolution
representations while efficiently handling large images makes
it an ideal choice for analyzing complex neuroimaging data,
such as those derived from multi-shell dMRI. This ability
to work with high-resolution representations, combined with
the use of pre-trained weights, allows Swin Transformers
to not only improve the adaptability of models to different
image sizes and resolutions, but also enhances the potential
for accurate diagnosis and prognosis of neuropathologies such
as Alzheimer’s disease by leveraging diffusion MRI data. The recent inclusion of multi-shell diffusion MRI in the
Alzheimer’s Disease Neuroimaging Initiative (ADNI) dataset
presents a valuable opportunity for developing new diagnostic
tools [17].

**Passage 12:**

> are available in the
GitHub repository of the article athttps://github.com/Hyedryn/
Swin_dMRI_public.
amyloid pathology, supporting biomarker-driven diagnos-
tics in data-limited biomedical settings. Index Terms— Alzheimer’s disease, deep learning, diffu-
sion MRI, DTI, NODDI, Swin Transformer
I. INTRODUCTION
D
IFFUSION Magnetic Resonance Imaging (dMRI) has
emerged as a powerful modality to investigate the mi-
crostructural properties of brain tissue. By analyzing the dif-
fusion of water molecules in the brain, dMRI provides insights
into the integrity of white matter tracts and the microstructural
organization of brain tissue.

**Passage 13:**

> ck, B. Rogers,et al., “Synthesized b0
for diffusion distortion correction (synb0-disco),”Magnetic resonance
imaging, vol. 64, pp. 62–70, 2019.
[31] J. Deng, W. Dong, R. Socher, L.-J. Li, K. Li, and L. Fei-Fei, “Imagenet:
A large-scale hierarchical image database,” in2009 IEEE conference on
computer vision and pattern recognition, pp. 248–255, Ieee, 2009.
[32] E. J. Hu, Y . Shen, P. Wallis, Z. Allen-Zhu, Y . Li, S. Wang, L. Wang,
and W. Chen, “Lora: Low-rank adaptation of large language models,”
arXiv preprint arXiv:2106.09685, 2021.
[33] D. P. Kingma and J. Ba, “Adam: A method for stochastic optimization,”
arXiv preprint arXiv:1412.6980, 2014.
[34] I. Loshchilov and F. Hutter, “Sgdr: Stochastic gradient descent with
warm restarts,”arXiv preprint arXiv:1608.03983, 2016.
[35] V . L. Villemagne, S. Burnham, P. Bourgeat, B. Brown, K. A. Ellis,
O. Salvado, C. Szoeke, S. L. Macaulay, R.

**Passage 14:**

> arcellation, based on the Brainnetome atlas (246 ROIs)
[39] and the SUIT cerebellum atlas (34 ROIs) [40]. This article has been accepted for publication in IEEE Transactions on Biomedical Engineering. This is the author's version which has not been fully edited and 
content may change prior to final publication. Citation information: DOI 10.1109/TBME.2025.3636745
This work is licensed under a Creative Commons Attribution 4.0 License. For more information, see https://creativecommons.org/licenses/by/4.0/
6 IEEE TRANSACTIONS ON BIOMEDICAL ENGINEERING, VOL. XX, NO. XX, XXXX 2023
III. RESULTS
A. Classification performance
We evaluated the proposed framework’s performance in
classifying participants into diagnostic categories using the
fine-tuned pre-trained Swin Transformer. We conducted ex-
periments using microstructural maps derived from both DTI
and NODDI models.

**Passage 15:**

> as not been fully edited and 
content may change prior to final publication. Citation information: DOI 10.1109/TBME.2025.3636745
This work is licensed under a Creative Commons Attribution 4.0 License. For more information, see https://creativecommons.org/licenses/by/4.0/
AUTHORet al.: PREPARATION OF PAPERS FOR IEEE TRANSACTIONS AND JOURNALS (JUL Y 2025) 7
Fig. 3. Average activation map generated by Grad-CAM for the subjects
correctly classified as AD, highlighting important regions inside the brain
contributing to the classification. The regions are represented in 2D ((a)
coronal,(b)sagittal and(c)axial) and 3D(d)views in the MNI space. D. Explainability analysis
To interpret the model’s decisions, we employed Grad-
CAM [38] to visualize the regions contributing to the clas-
sification.

**Passage 16:**

> -based localization,” inProceedings of the IEEE international
conference on computer vision, pp. 618–626, 2017.
[39] L. Fan, H. Li, J. Zhuo, Y . Zhang, J. Wang, L. Chen, Z. Yang, C. Chu,
S. Xie, A. R. Laird,et al., “The human brainnetome atlas: a new brain
atlas based on connectional architecture,”Cerebral cortex, vol. 26, no. 8,
pp. 3508–3526, 2016.
[40] J. Diedrichsen, “A spatially unbiased atlas template of the human
cerebellum,”Neuroimage, vol. 33, no. 1, pp. 127–138, 2006.
[41] S. Rathore, M. Habes, M. A. Iftikhar, A. Shacklett, and C. Davatzikos,
“A review on neuroimaging-based classification studies and associated
feature extraction methods for Alzheimer’s disease and its prodromal
stages,”NeuroImage, vol. 155, pp. 530–548, July 2017.
[42] J. Jang and D.

**Passage 17:**

> rections atb= 500, 48 directions atb= 1000
and 60 directions atb= 2000µsµm −2, along with 13b= 0
acquisitions, for a total of 127 measurements. The matrix size
for the scans was 116 × 116 × 81 pixels. T1-weighted sMRI scans using the MPRAGE sequence,
acquired during the same session as the diffusion data, were
included to provide anatomical context for the neuroimag-
ing analysis. These MPRAGE scans were acquired in the
sagittal plane using a 3D gradient-recalled inversion recovery
sequence, with a voxel size of 1.0 × 1.0 × 1.0 mm. The
acquisition parameters included a TE of 3.0 ms, a TR of
2300.0 ms, and an inversion time of 900.0 ms. The flip angle
was set to 9 degrees, and the matrix size was 240 × 256 ×
208 pixels. TABLE I
DEMOGRAPHIC CHARACTERISTICS OF SELECTED PARTICIPANTS FROM
THEADNIDATASET.

**Passage 18:**

> trained
weights. By employing this advanced architecture and utilizing
dMRI’s unique insights into microstructural changes, we aim
to enhance the understanding and diagnosis of Alzheimer’s
disease. A. Contributions
•We highlight the use of multi-shell diffusion MRI for
Alzheimer’s disease classification, leveraging the mi-
crostructural information available from diffusion models
such as DTI and NODDI.
•We demonstrate the potential of using multi-shell dif-
fusion MRI for predicting amyloid beta status, a key
biomarker for early detection of Alzheimer’s disease.
•To efficiently process diffusion MRI data, we project 3D
microstructural maps into 2D representations, allowing
the use of pre-trained Swin Transformer while maintain-
ing essential spatial information.
•We incorporate LoRA, a parameter-efficient fine-tuning
approach, into our deep learning framework, enhancing
adaptability to neuroimaging tasks with limited labeled
data while leveraging pre-trained ImageNet weights.
•Through Grad-CAM-based explainability, we highlight
the clinically relevant brain regions that contribute to
model classification decisions, offering valuable inter-
pretability for medical applications.
•Our framework is designed to be adaptable and ex-
tendable to other neuroimaging modalities and medical
imaging tasks, paving the way for future applications
beyond Alzheimer’s disease.

**Passage 19:**

> s, as our empirical evaluation indicated it yielded
slightly superior performance compared to the coronal and
sagittal planes. A full comparison of this orientation analysis
is provided in Appendix A. This collation process is applied
consistently for each of the three microstructural maps, which
are then combined to create a final three-channel image where
each channel corresponds to a specific metric, as illustrated in
Fig. 1. I(x, y, c) =M c(x, y)forc∈ {1,2,3}.(1)
whereI(x, y, c)represents the resulting 2D image at coordi-
nates(x, y), with channelc∈ {1,2,3}corresponding to one of
the microstructural maps:M 1(x, y),M 2(x, y), orM 3(x, y). These three-channel images are then input into a fine-tuned
Swin Transformer architecture, pre-trained on the ImageNet
dataset [31].

**Passage 20:**

> MRI data. The recent inclusion of multi-shell diffusion MRI in the
Alzheimer’s Disease Neuroimaging Initiative (ADNI) dataset
presents a valuable opportunity for developing new diagnostic
tools [17]. Historically, most large diffusion MRI datasets were
limited to single-shell acquisitions [18], suitable primarily for
Apparent Diffusion Coefficient (ADC) and Diffusion Tensor
Imaging (DTI) [19]. While foundational, these models are
constrained by simplified assumptions about water diffusion,
limiting their ability to characterize complex microstructural
features such as crossing fibers and tissue heterogeneity.

**Passage 21:**

> ect benchmarking
within this specific domain, we have made our implementation
open-source and provided the exact subject identifiers used
for defining the training, validation, and hold-out test sets. This commitment to transparency and reproducibility aims
to establish a reliable baseline against which future methods
utilizing multi-shell dMRI for AD and amyloid classification
can be directly and fairly compared. F . Limitations and future work
Despite the promising results, our study has limitations. The sample size, particularly for the AD group, is relatively
small, which may affect the generalizability of the findings. Future work should include larger and more diverse cohorts
to validate the model’s robustness. A second limitation concerns the 2D representation.

**Passage 22:**

> fusion; Axial
Diffusivity (AxD), indicating water diffusion along the princi-
pal axis of the diffusion tensor; and Radial Diffusivity (RD),
representing diffusion perpendicular to the principal axis. For
NODDI, the selected metrics were the Orientation Dispersion
Index (ODI), which quantifies the spread of neurite orien-
tations; the Intra-neurite V olume Fraction (f intra), reflecting
the proportion of the diffusion MRI signal from neurites; and
the Extra-neurite V olume Fraction (f extra), representing the
signal from the extracellular space. These metrics were chosen
for their relevance in characterizing microstructural properties
and providing rich input features for the transformer model. The 3D microstructural maps derived from the dMRI data
were subsequently used as input for the deep learning models
developed in this study. C.

**Passage 23:**

> ays
toward an early diagnosis in Alzheimer’s disease: The Alzheimer’s
Disease Neuroimaging Initiative (ADNI),”Alzheimer’s & Dementia,
vol. 1, pp. 55–66, July 2005.
[19] P. Basser, J. Mattiello, and D. LeBihan, “MR diffusion tensor spec-
troscopy and imaging,”Biophysical Journal, vol. 66, pp. 259–267, Jan. 1994. This article has been accepted for publication in IEEE Transactions on Biomedical Engineering. This is the author's version which has not been fully edited and 
content may change prior to final publication. Citation information: DOI 10.1109/TBME.2025.3636745
This work is licensed under a Creative Commons Attribution 4.0 License. For more information, see https://creativecommons.org/licenses/by/4.0/
10 IEEE TRANSACTIONS ON BIOMEDICAL ENGINEERING, VOL. XX, NO. XX, XXXX 2023
[20] J. Acosta-Cabronero, S. Alley, G. B. Williams, G. Pengas, and P. J.

**Passage 24:**

> es of brain tissue. By analyzing the dif-
fusion of water molecules in the brain, dMRI provides insights
into the integrity of white matter tracts and the microstructural
organization of brain tissue. In particular, the combination
of high angular resolution diffusion imaging (HARDI) with
multi-shell dMRI offers a detailed characterization of tissue
microstructure, positioning it as a promising tool for diag-
nosing and understanding the underlying biological changes
associated with neurodegenerative diseases [1]. However, the high dimensionality and complexity of multi-
shell dMRI data present significant challenges for tradi-
tional analysis methods. Deep learning has shown promise
in automating feature extraction and classification from high-
dimensional neuroimaging data [2].

</details>

---

## Liou et al. (2025) — DTI versus NODDI White Matter Microstructural Biomarkers of Alzheimer’s Disease
_File: `Liou et al. - 2025 - DTI versus NODDI White Matter Microstructural Biomarkers of Alzheimer’s Disease.pdf`_

1. **Was diffusion MRI (DTI, dMRI, DWI, or similar) used in this paper?**  
   Yes. The paper explicitly mentions "ADNI3 dMRI" and "multishell dMRI protocols," and describes DTI and NODDI as diffusion MRI-based methods.  

---

2. **What processing steps were applied to the diffusion images?**  
   - Denoising using principal component analysis (PCA) techniques [15,16].  
   - Correction for Gibbs ringing [17].  
   - For ADNI4 only: Susceptibility distortion correction using FSL’s `topup` [18] with concatenated AP-PA scans.  
   - For ADNI3 S127: Distortion correction using Synb0-DisCo [19].  
   - Extra-cerebral tissue removal and eddy correction with FSL’s `eddy` tool, including outlier and slice timing corrections [20,21,22].  
   - Correction for B1 field inhomogeneities.  
   - Linear and nonlinear registration to T1w (preprocessed with FreeSurfer) using ANTs [23].  
   - Inversion of linear registration to bring T1w to native DWI space [14].  
   - Visual quality assurance.  

---

3. **What software or tools are explicitly named for processing?**  
   - **FSL** (for `topup` and `eddy`).  
   - **ANTs** (for registration).  
   - **DmiPy** (for NODDI).  
   - **FreeSurfer** (for T1w preprocessing).  

---

4. **What acquisition or processing parameters are explicitly reported?**  
   - **B-values**: b0, b=1000 s/mm² (for DTI), and all volumes (for NODDI).  
   - **Voxel size**: 2×2×2 mm³ isotropic (with zero-padding to 0.9×0.9×2 mm³ for GE127).  
   - **Number of directions**:  
     - GE127: 6 b=500, 48 b=1000, 60 b=2000 (total 127).  
     - P100: 38 b=1000, 47 b=2000 (total 100).  
     - S100: 38 b=1000, 47 b=2000 (total 100).  
     - S127: 48 b=1000, 60 b=2000 (total 127).  

---

5. **Exact sentences from the excerpts describing processing:**  
   - *"ADNI3 dMRI were preprocessed as in [14]. As in ADNI3, all dMRI were denoised using principal component analysis (PCA) techniques [15,16] and corrected for Gibbs ringing [17]."*  
   - *"For ADNI4 only, susceptibility distortions were corrected using FSL’s topup [18] using concatenated anterior-posterior (AP) and posterior-anterior (PA) scans. [...] Extra-cerebral tissue was removed and eddy correction performed with FSL’s eddy tool, including outlier and slice timing corrections [20, 21, 22]."*  
   - *"The resulting dMRI were corrected for B1 field inhomogeneities then linearly and nonlinearly registered to the subjects’ respective T1w [...] using ANTs; the linear registration was subsequently inverted to bring the T

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> . Image Preprocessing 
ADNI3 dMRI were preprocessed as in [14]. As in ADNI3, 
all dMRI were denoised using principal component analysis 
(PCA) techniques [15,16] and corrected for Gibbs ringing 
[17]. For ADNI4 only, susceptibility distortions were 
corrected using FSL’s topup [18] using concatenated 
anterior-posterior (AP) and posterior-anterior (PA) scans. The concatenated AP-PA images were carried through the 
remaining preprocessing and analysis. The ADNI3 S127 
protocol lacked AP scans and were distortion-corrected using 
Synb0-DisCo [19]. GE multishell scans were excluded from 
topup since distortions were corrected in-scanner. Extra-
cerebral tissue was removed and eddy correction performed 
with FSL’s eddy tool, including outlier and slice timing 
corrections [20, 21, 22].

**Passage 2:**

> topup since distortions were corrected in-scanner. Extra-
cerebral tissue was removed and eddy correction performed 
with FSL’s eddy tool, including outlier and slice timing 
corrections [20, 21, 22]. The resulting dMRI were corrected 
for B1 field inhomogeneities then linearly and nonlinearly 
registered to the subjects’ respective T1w (preprocessed with 
the standard FreeSurfer pipeline [23]) using ANTs; the linear 
registration was subsequently inverted to bring the T1w to 
the native DWI space [14]. All dMRI and T1w images were 
visually checked for quality assurance. C. DTI and NODDI Extraction 
DTI was fit on the subset of b0 and b=1000 s/mm2 dMRI 
volumes and NODDI was fit across all volumes. DTI was 
computed with FSL using weighted least squares and 
NODDI was computed using DmiPy [24].

**Passage 3:**

> rating outlier detection and 
replacement into a non-parametric framework for movement and 
distortion correction of diffusion MR images,” NeuroImage, vol. 141, 
pp. 556–572, Nov. 2016. 
[22] J. L. R. Andersson et al., “Towards a comprehensive framework for 
movement and distortion correction of diffusion MR images: Within 
volume movement,” NeuroImage, vol. 152, pp. 450–466, May 2017. 
[23] B. Fischl et al., “Automatically parcellating the human cerebral 
cortex,” Cereb. Cortex N. Y. N 1991, vol. 14, no. 1, pp. 11–22, Jan. 2004. 
[24] R. H. J. Fick et al., “The Dmipy toolbox: Diffusion MRI multi-
compartment modeling and microstructure recovery made easy,” 
Front. Neuroinform., vol. 13, p. 64, Oct. 2019. 
[25] S. Mori et al., “Stereotaxic White Matter Atlas Based on Diffusion 
Tensor Imaging in an ICBM Template,” NeuroImage, vol. 40, no. 2, 
pp. 570–582, Apr. 2008. 
[26] Y.

**Passage 4:**

> , 2025.  
[14] S. I. Thomopoulos et al., "Diffusion MRI metrics and their relation to 
dementia severity: effects of harmonization approaches," in Proc. 17th 
Int. Symp. Med. Inf. Process. Anal., vol. 12088, Campinas, Brazil, 
Dec. 2021, pp. 120880K. 
[15] Manjón, J. V et al., ‘Diffusion weighted image denoising using 
overcomplete local PCA.,’ PLoS One 8(9), e73021 (2013). 
[16] J. Veraart et al., “Denoising of diffusion MRI using random matrix 
theory,” NeuroImage, vol. 142, pp. 394–406, Nov. 2016. 
[17] E. Kellner et al., “Gibbs-ringing artifact removal based on local 
subvoxel-shifts,” Magn. Reson. Med., vol. 76, no. 5, pp. 1574–1581, 
Nov. 2016.  
[18] J. L. R. Andersson et al., “How to correct susceptibility distortions in 
spin-echo echo-planar images: application to diffusion tensor 
imaging,” NeuroImage, vol. 20, no. 2, pp. 870–888, Oct. 2003.   
[19] K. G.

**Passage 5:**

> , p. fcab106, May 2021. 
[29] E. Özarslan et al., “Mean Apparent Propagator (MAP) MRI: a novel 
diffusion imaging method for mapping tissue microstructure,” 
NeuroImage, vol. 78, pp. 16–32, Sep. 2013. Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 15,2026 at 22:22:06 UTC from IEEE Xplore. Restrictions apply.

**Passage 6:**

> 127* 
Siemens: 
Advanced Prisma 
VE11C 
13 b0 1 b0 
 
116x116
6 b=500 s/mm2 
48 b=1000 s/mm2 6 b=1000 
s/mm2 60 b=2000 s/mm2 
Total: 127 Total: 7 
*S127: ADNI3 lacks AP scans; ADNI4 includes AP scans. Table 3. Index of 31 JHU atlas WM ROIs. CST 
IC 
AIC 
PLIC 
RLIC     
PTR 
CR 
ACR 
SCR 
PCR 
CGC 
CGH 
EC 
Fx 
SLF 
 
SFO 
Corticospinal tract 
Internal capsule 
Ant. limb of IC 
Post. limb of IC 
Retrolenticular part of IC 
Post. thalamic radiation 
Corona radiata 
Ant. CR 
Sup. CR 
Post. CR 
Cingulum (cingulate) 
Cingulum (hippocampal) 
External capsule 
Fornix 
Sup. longitudinal 
fasciculus 
Sup. fronto-occipital 
fasciculus 
ML 
CP 
ICP 
MCP 
PCT 
 
SCP 
SS 
FxST 
 
UNC 
TAP 
CC 
GCC 
BCC 
SCC 
FullWM 
Medial lemniscus 
Cerebral peduncle 
Inf. CP 
Middle CP 
Pontine crossing 
tract 
Sup.

**Passage 7:**

> females than in males. II. METHODS 
A. Subject and Image Acquisition 
Baseline 3 T T1-weighted (T1w) MRI and multishell dMRI 
data were downloaded from the ADNI database 
(https://ida.loni.usc.edu/). In total, we analyzed dMRI data 
from 533 participants across ADNI3/4: 341 cognitively 
normal elderly controls (CN), 149 mild cognitive impairment 
cases (MCI), and 43 dementia cases ( Table 1 ). All 
participants were scanned with one of four ADNI3/4 
multishell dMRI protocols (Table 2). Key clinical indicators 
of AD, specifically Clinical Dementia Rating sum-of-boxes 
(CDR-sob; N=529) [10], Aβ-PET centiloids (CLs; N=213) 
[11], and tau-PET standardized value uptake ratios (SUVRs; 
N=186) [12], were obtained when available. Cortical Aβ-
PET (18F-florbetaben, 18F-florbetapir, 18F-NAV4694) CLs 
were derived using methods described in [13].

**Passage 8:**

> DTI was fit on the subset of b0 and b=1000 s/mm2 dMRI 
volumes and NODDI was fit across all volumes. DTI was 
computed with FSL using weighted least squares and 
NODDI was computed using DmiPy [24]. Fractional 
anisotropy (FA), mean (MD), axial (AxD), and radial 
diffusivity (RD) maps were derived from DTI. Intracellular 
volume fraction (ICVF), isotropic volume fraction (ISOVF), 
and orientation dispersion index (ODI) maps were extracted 
from NODDI. As in [14], the JHU ICBM-DTI-81 [25] atlas 
FA was warped to each subject’s FA. The transformations 
were applied to stereotaxic JHU WM atlas labels (JHU MNI 
single subject WMPM1) [25] using nearest neighbor 
interpolation. Mean DTI and NODDI measures were 
extracted from 31 WM regions of interest (ROIs), averaged 
across the left and right hemispheres (Table 3). D.

**Passage 9:**

> 3 and ADNI4 multishell acquisition 
protocols. All dMRI were acquired with an isotropic 2x2x2 mm3 
voxel size. GE127 dMRI were zero-padded in k-space during 
acquisition to a 0.9x0.9x2 mm3 voxel size. Protocol 
Scanner 
Vendor: 
Model(s) 
Volumes 
Matrix PA AP 
GE127 
GE: Premier 29.1 
48CH Advanced 
& MR750 29.1 
32Ch Nova 
Advanced 
13 b0 
NA 256x256
6 b=500 s/mm2 
48 b=1000 s/mm2 
60 b=2000 s/mm2 
Total: 127 
P100 Philips: 
Advanced 5 6x 
9 b0 1 b0 
 
128x126
6 b=500 s/mm2 
38 b=1000 s/mm2 6 b=1000 
s/mm2 47 b=2000 s/mm2 
Total: 100 Total: 7 
S100 
Siemens: Skyra 
VE11C & Vida 
XA20 
9 b0 1 b0 
 
116x116
6 b=500 s/mm2 
38 b=1000 s/mm2 12 b=1000 
s/mm2 47 b=2000 s/mm2 
Total: 100 Total: 13 
S127* 
Siemens: 
Advanced Prisma 
VE11C 
13 b0 1 b0 
 
116x116
6 b=500 s/mm2 
48 b=1000 s/mm2 6 b=1000 
s/mm2 60 b=2000 s/mm2 
Total: 127 Total: 7 
*S127: ADNI3 lacks AP scans; ADNI4 includes AP scans.

**Passage 10:**

> vol. 13, p. 64, Oct. 2019. 
[25] S. Mori et al., “Stereotaxic White Matter Atlas Based on Diffusion 
Tensor Imaging in an ICBM Template,” NeuroImage, vol. 40, no. 2, 
pp. 570–582, Apr. 2008. 
[26] Y. Benjamini and Y. Hochberg, “Controlling the False Discovery Rate: 
A Practical and Powerful Approach to Multiple Testing,” J. R. Stat. Soc. Ser. B Methodol., vol. 57, no. 1, pp. 289–300, 1995. 
[27] C. Lopez-Lee et al., “Mechanisms of sex differences in Alzheimer’s 
disease,” Neuron, vol. 112, no. 8, pp. 1208–1221, Apr. 2024. 
[28] S. Raghavan et al., “Diffusion models reveal white matter 
microstructural changes with ageing, pathology and cognition,” Brain 
Commun., vol. 3, no. 2, p. fcab106, May 2021. 
[29] E. Özarslan et al., “Mean Apparent Propagator (MAP) MRI: a novel 
diffusion imaging method for mapping tissue microstructure,” 
NeuroImage, vol. 78, pp. 16–32, Sep. 2013.

**Passage 11:**

> ther’ is defined as Asian, American Indian, Alaskan Native, or mixed race. +Ethnicity is defined here as Hispanic or non-Hispanic. Table 2. Available ADNI3 and ADNI4 multishell acquisition 
protocols. All dMRI were acquired with an isotropic 2x2x2 mm3 
voxel size. GE127 dMRI were zero-padded in k-space during 
acquisition to a 0.9x0.9x2 mm3 voxel size.

**Passage 12:**

> Sup. fronto-occipital 
fasciculus 
ML 
CP 
ICP 
MCP 
PCT 
 
SCP 
SS 
FxST 
 
UNC 
TAP 
CC 
GCC 
BCC 
SCC 
FullWM 
Medial lemniscus 
Cerebral peduncle 
Inf. CP 
Middle CP 
Pontine crossing 
tract 
Sup. CP 
Sagittal stratum 
Fornix (crus)/Stria 
terminalis 
Uncinate fasciculus 
Tapetum 
Full corpus callosum 
Genu of CC 
Body of CC 
Splenium of CC 
Full white matter 
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 15,2026 at 22:22:06 UTC from IEEE Xplore. Restrictions apply. Figure 1. Effect sizes for associations between regional DTI and 
NODDI measures and (A) CDR-sob, (B) MCI diagnosis, (C) Aβ-
PET CLs, and (D) tau-PET SUVRs. Significant associations are 
opaque (PFDR<0.05). 
estimated using partial d and partial correlation r for 
categorical and continuous AD indicators, respectively.

**Passage 13:**

> ersson et al., “How to correct susceptibility distortions in 
spin-echo echo-planar images: application to diffusion tensor 
imaging,” NeuroImage, vol. 20, no. 2, pp. 870–888, Oct. 2003.   
[19] K. G. Schilling et al., “Synthesized b0 for diffusion distortion 
correction (Synb0-DisCo),” Magn. Reson. Imaging, vol. 64, pp. 62–
70, Dec. 2019. 
[20] J. L. R. Andersson and S. N. Sotiropoulos, “An integrated approach to 
correction for off-resonance effects and subject movement in diffusion 
MR imaging,” NeuroImage, vol. 125, pp. 1063–1078, Jan. 2016. 
[21] J. L. R. Andersson et al., “Incorporating outlier detection and 
replacement into a non-parametric framework for movement and 
distortion correction of diffusion MR images,” NeuroImage, vol. 141, 
pp. 556–572, Nov. 2016. 
[22] J. L. R.

**Passage 14:**

> standardized value uptake ratios (SUVRs; 
N=186) [12], were obtained when available. Cortical Aβ-
PET (18F-florbetaben, 18F-florbetapir, 18F-NAV4694) CLs 
were derived using methods described in [13]. Tau-PET 
(18F-flortaucipir) burden was defined using the medial 
2025 21st International Symposium on Biomedical Image Processing and Analysis (SIPAIM) | 979-8-3315-5456-9/25/$31.00 ©2025 IEEE | DOI: 10.1109/SIPAIM67325.2025.11283294
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 15,2026 at 22:22:06 UTC from IEEE Xplore. Restrictions apply. 
temporal SUVR normalized using measures from the inferior 
cerebellar gray matter. B. Image Preprocessing 
ADNI3 dMRI were preprocessed as in [14]. As in ADNI3, 
all dMRI were denoised using principal component analysis 
(PCA) techniques [15,16] and corrected for Gibbs ringing 
[17].

**Passage 15:**

> ject WMPM1) [25] using nearest neighbor 
interpolation. Mean DTI and NODDI measures were 
extracted from 31 WM regions of interest (ROIs), averaged 
across the left and right hemispheres (Table 3). D. Statistical Analyses 
Linear mixed effects models were used to assess associations 
between regional dMRI measures and key AD indicators: (1) 
CDR-sob, (2) an MCI versus CN diagnosis, (3) Aβ-PET CLs, 
and (4) tau-PET SUVRs. We also tested whether sex 
moderated the effect between AD indicators and dMRI 
measures. Fixed effects covariates included age, sex, age-by-
sex interactions, education, self-reported race, and ethnicity. We additionally covaried for diagnosis in Aβ and tau 
analyses. Across analyses, dMRI protocol and preprocessing 
scheme was modeled as a random effect. Effect sizes were 
Table 1. Subject Demographic and Clinical Information.

**Passage 16:**

> or diagnosis in Aβ and tau 
analyses. Across analyses, dMRI protocol and preprocessing 
scheme was modeled as a random effect. Effect sizes were 
Table 1. Subject Demographic and Clinical Information. Diagnosis (N) Age (yrs) Male 
(N) CDR-sob Aβ-PET 
(CL) 
Tau-PET 
(SUVR) 
Education 
(yrs) Self-Reported Race* (N) Ethnicity+  
(N Hispanic) 
CN (341) 70.0±8.5 122 0.05±0.2 16.5±28.6 1.2±0.2 16.4±2.5 203 White, 88 Black, 50 Other 39 Hispanic 
MCI (149) 73.2±8.1 69 1.5±1.1 46.9±49.4 1.6±0.7 15.8±2.5 103 White, 27 Black, 19 Other 9 Hispanic 
Dementia (43) 76.7±6.9 20 4.3±1.8 95.2±35.6 2.1±0.4 15.5±3.0 30 White, 9 Black, 4 Other 1 Hispanic 
*‘Other’ is defined as Asian, American Indian, Alaskan Native, or mixed race. +Ethnicity is defined here as Hispanic or non-Hispanic. Table 2. Available ADNI3 and ADNI4 multishell acquisition 
protocols.

**Passage 17:**

> DTI versus NODDI White Matter Microstructural Biomarkers of 
Alzheimer’s Disease 
Kenny Liou1, Sophia I. Thomopoulos1, Hannah Yoo1, Yuhan Shuai1, Sasha Chehrzadeh1, Arvin Arani2, Bret Borowski2,  
Robert I. Reid2, Clifford R. Jack, Jr.2, Michael W. Weiner3, Neda Jahanshad1, Paul M. Thompson1, Talia M. Nir1;  
Alzheimer’s Disease Neuroimaging Initiative 
Kenny.Liou@loni.usc.edu   
1Imaging Genetics Center, Mark and Mary Stevens Neuroimaging and Informatics Institute, 
Keck School of Medicine, University of Southern California, Marina del Rey, CA, USA 
2Department of Radiology, Mayo Clinic, Rochester, Minnesota, USA 
3Department of Radiology, School of Medicine, University of California, San Francisco, CA, USA
Abstract—Diffusion MRI (dMRI) is a powerful tool to assess 
white matter (WM) microstructural abnormalities in 
Alzheimer’s disease (AD).

**Passage 18:**

> es and 
less demanding hardware requirements. This has led to the 
widespread use of diffusion tensor imaging (DTI) [2], a 
model that characterizes Gaussian diffusion from single-shell 
acquisitions. Numerous DTI studies have identified AD-
related WM abnormalities, such as greater diffusivity and 
reduced anisotropy in key brain regions like the corpus 
callosum, cingulum bundle, and fornix, particularly with 
respect to degree of clinical impairment [3,4]. However, DTI 
has significant limitations. It cannot accurately model 
complex fiber architectures, such as crossing fibers, and      
often lack biological specificity, making it difficult to 
precisely link observed changes to underlying tissue 
properties [5]. Multishell dMRI protocols address these 
limitations by capturing both Gaussian and non-Gaussian 
diffusion signals, allowing finer characterization of WM.

**Passage 19:**

> Magn. Reson. Imaging, vol. 52, 
no. 6, pp. 1620–1636, 2020.  
[2] P. J. Basser et al., “MR diffusion tensor spectroscopy and imaging,” 
Biophys. J., vol. 66, no. 1, pp. 259–267, Jan. 1994.  
[3] T. M. Nir et al., “Effectiveness of regional DTI measures in 
distinguishing Alzheimer’s disease, MCI, and normal aging,” 
NeuroImage Clin., vol. 3, pp. 180–195, Jul. 2013.  
[4] A. Zavaliangos-Petropulu et al., “Diffusion MRI Indices and Their 
Relation to Cognitive Impairment in Brain Aging: The Updated Multi-
protocol Approach in ADNI3,” Front. Neuroinformatics, vol. 13, p. 2, 
Feb. 2019.  
[5] K. Oishi et al., “DTI Analyses and Clinical Applications in 
Alzheimer’s Disease,” J. Alzheimers Dis., vol. 26, no. Suppl 3, pp. 287–296, 2011.  
[6] H. Zhang et al., “NODDI: practical in vivo neurite orientation 
dispersion and density imaging of the human brain,” NeuroImage, vol. 61, no. 4, pp.

**Passage 20:**

> We will also compare 
multishell models that do not parse the signal, such as mean 
apparent propagator (MAP) MRI [28], with DTI and NODDI 
and refine spatial localization using along-tract analyses. Integration of richer WM features across models could 
enhance detection of cognitive impairment, Aβ burden, and 
tau pathology in AD research. ACKNOWLEDGMENTS  
This work was supported by AARG-23-1149996, 
R01AG058854, R01AG087513, RF1AG057892, 
U01AG068057, U19AG024904, S10OD032285. REFERENCES 
[1] C. Andica et al., “MR Biomarkers of Degenerative Brain Disorders 
Derived From Diffusion Imaging,” J. Magn. Reson. Imaging, vol. 52, 
no. 6, pp. 1620–1636, 2020.  
[2] P. J. Basser et al., “MR diffusion tensor spectroscopy and imaging,” 
Biophys. J., vol. 66, no. 1, pp. 259–267, Jan. 1994.  
[3] T. M.

**Passage 21:**

> Aβ-
PET CLs, and (D) tau-PET SUVRs. Significant associations are 
opaque (PFDR<0.05). 
estimated using partial d and partial correlation r for 
categorical and continuous AD indicators, respectively. The 
false discovery rate (FDR) procedure [26] was used to correct 
for multiple comparisons across 31 ROIs. III. RESULTS 
A. DTI and NODDI Associations with AD Outcomes  
Lower FA and ICVF, and higher AxD, MD, RD, and ISOVF 
were widely associated with greater cognitive impairment 
(i.e., higher CDR-sob and a MCI diagnosis; PFDR<0.05; Fig. 1A, B). While effects were detected globally in the Full WM, 
the strongest effects localized to the CC and the limbic tracts 
including the CGH, UNC, and Fx. Fewer associations were 
seen with ODI. Greater Aβ burden was linked to higher AxD, 
MD, ISOVF, and lower ODI across the IC (ISOVF), SCP 
(AxD, ODI), and Fx (ODI) (Fig. 1C).

**Passage 22:**

> e 
complexity, and greater free water which may indicate 
inflammation/edema, respectively. Table 3. Number of ROIs showing significant sex interactions per 
AD indicator and dMRI measure (PFDR<0.05). Test Total DTI NODDI 
FA MD RD AxD ICVF ISOVF ODI 
CDR-sob 0 0 0 0 0 0 0 0 
CN vs MCI 3 0 1 0 2 0 0 0 
Aβ-PET  20 2 4 5 2 2 4 1 
Tau-PET 23 6 4 5 1 1 4 2 
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 15,2026 at 22:22:06 UTC from IEEE Xplore. Restrictions apply. Figure 2. Cingulum (CGC) FA residuals illustrate that males 
showed a steeper decline in anisotropy compared to females with 
increasing (A) Aβ and (B) tau load.

**Passage 23:**

> his study, 
we compared the ability of ADNI DTI and NODDI WM 
measures to detect associations with several key AD 
indicators: Aβ burden, tau pathology, and clinical measures 
of cognitive impairment. We also assessed whether sex 
moderates these effects. This is important given females have 
a higher prevalence of AD than males and exhibit distinct 
pathological and cognitive profiles [8, 9]. We hypothesized 
that NODDI-derived WM measures would provide better 
biological specificity, stronger associations with AD 
indicators, and that these effects would be more pronounced 
in females than in males. II. METHODS 
A. Subject and Image Acquisition 
Baseline 3 T T1-weighted (T1w) MRI and multishell dMRI 
data were downloaded from the ADNI database 
(https://ida.loni.usc.edu/).

**Passage 24:**

> hanges to underlying tissue 
properties [5]. Multishell dMRI protocols address these 
limitations by capturing both Gaussian and non-Gaussian 
diffusion signals, allowing finer characterization of WM. In 
particular, biophysical multishell models, such as neurite 
orientation dispersion and density imaging (NODDI) [6], can 
parse signal contributions from various tissue compartments 
including the intracellular compartment and free water. There 
is a need to evaluate whether multishell data offers deeper 
insights into WM alterations in AD by moving beyond the 
limitations of DTI, particularly for detecting subtle effects 
associated with early amyloid and tau pathology; however, 
such investigations remain scarce.

</details>

---

## MACFNet--Detection-of-Alzheimer-s-disease-via-mult_2024_Computer-Methods-and
_File: `MACFNet--Detection-of-Alzheimer-s-disease-via-mult_2024_Computer-Methods-and.pdf`_



<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> ifficult to extract effective features from them. The preprocessing 
operation removes redundant information from the image irrelevant to 
AD diagnosis and lays the foundation for subsequent analysis. The pre -
processing of our method is divided into three steps:  
(1) Image correction. The raw MR images were first processed for 
image correction to remove phenomena such as motion artifacts 
and noise from the images. Image correction includes head mo -
tion correction and bias field correction. In this paper, head 
motion correction is performed on MR images based on anterior 
perineum (AC) and posterior perineum (PC) localization criteria. Then, the bias field correction is performed by the N4BiasField -
Correction.sh module integrated into the ANTs tool. 2 
The image 
size was set to 3, 3, and 3, and the scaling factors were set to 8, 4, 
and 2.

**Passage 2:**

> the 
detailed information of the selected subjects. Due to the ADNI volunteers being sourced from various countries 
and regions, the imaging equipment used for scanning differs across all 
subjects. For the convenience of the study, we selected the three most 
widely used imaging devices in current practice. MR images of all sub -
jects were obtained using three magnetic resonance scanners. The im -
aging parameters of each scanner are shown in Table 2 . 3.1.2. Data preprocessing 
Due to variations in imaging techniques, significant differences and 
noise interference exist between different brain images, making it 
difficult to extract effective features from them. The preprocessing 
operation removes redundant information from the image irrelevant to 
AD diagnosis and lays the foundation for subsequent analysis.

**Passage 3:**

> near Image 
Alignment Tool (FNIRT). Finally, PET images in the MRI struc -
ture space were registered to the MNI structure space according 
to the MRI transformation matrix.  
(3) Tissue segmentation. Atrophy and lesions in grey matter, white 
matter, and regions are a focus of Alzheimer ’ s research as they 
are closely associated with disease progression and symptoms. However, aligned MRI and PET images contain regions of the 
skull, cerebellum, etc., that are not directly relevant to the 
diagnosis of AD, and these regions may increase the computa -
tional burden and interfere with the diagnosis. Therefore, tissue 
segmentation of images is required. In this paper, we use the 
CAT12 toolbox in SPM
4 
software to remove the cranium and 
cerebellum from MRI and PET images to reduce the computa -
tional burden and exclude the interference of irrelevant regions.

**Passage 4:**

> bias field correction is performed by the N4BiasField -
Correction.sh module integrated into the ANTs tool. 2 
The image 
size was set to 3, 3, and 3, and the scaling factors were set to 8, 4, 
and 2. In addition, the robustfov tool in the FMRIB Software Li -
brary
3 
(FSL) was used to remove the neck region from the MR 
images.  
(2) Image registration. We aligned MRI and PET images to address 
the spatial geometric inconsistencies of the different modality 
images. First, the PET images were aligned to the structural space 
Fig. 1. Comparison of the corrected and preprocessed images. (a-c) show the preprocessing process of MRI axial image, and (d-f) show the preprocessing process of 
PET axial image. Fig. 2. The overall network architecture of MACFNet. 2 
Available at https://github.com/ANTsX/ANTs  
3 
Available at https://fsl.fmrib.ox.ac.uk/fsl/fslwiki 
C. Tang et al.

**Passage 5:**

> er, we use the 
CAT12 toolbox in SPM
4 
software to remove the cranium and 
cerebellum from MRI and PET images to reduce the computa -
tional burden and exclude the interference of irrelevant regions. Finally, to improve the image quality further, the images were 
smoothed using a Gaussian kernel function to suppress the noise 
in the functional images and to make the grey and white matter 
changes in the images clearer. As is shown in Fig. 1 , the MRI and PET images were processed in the 
axial view by the med2image tool. 5 
Fig. 1 (a)- Fig. 1 (c) represents the 
axial image of MRI, while Fig. 1 (d)- Fig. 1 (f) represents the axial image of 
PET. Fig. 1 (a) is the origin corrected image after removing the neck, 
Fig. 1 (b) is the sliced image after skull stripping based on the corrected 
image, and Fig.

**Passage 6:**

> process of 
PET axial image. Fig. 2. The overall network architecture of MACFNet. 2 
Available at https://github.com/ANTsX/ANTs  
3 
Available at https://fsl.fmrib.ox.ac.uk/fsl/fslwiki 
C. Tang et al. Computer Methods and Programs in Biomedicine 254 (2024) 108259
6
of the corresponding MR images of each subject using the FMRIB 
linear image alignment tool (FLIRT). The similarity measurement 
function was set to Normal Mutual Information (NMI), the image 
interpolation was set to B-spline interpolation, and the degree of 
freedom (DOF) was set to 6. Then, the MR images were aligned to 
the MNI standard space using the FMRIB Nonlinear Image 
Alignment Tool (FNIRT). Finally, PET images in the MRI struc -
ture space were registered to the MNI structure space according 
to the MRI transformation matrix.  
(3) Tissue segmentation.

**Passage 7:**

> i-scale features by different dilation rates and receptive 
fields. To learn the dependence among each channel, they present a 
double-weight network based on an improved channel attention 
mechanism. However, this method contains sum and cascade opera -
tions, which will generate redundant noise. Furthermore, they focused 
only on grey matter (GM) regions and white matter (WM) regions of the 
brain in unimodal MRI and did not consider the multimodal situation. 3. Methods 
3.1. Data acquisition and preprocessing 
3.1.1. Data acquisition 
The dataset used in this article is from the ADNI database ( https:// 
Table 1 
Detailed information about the subjects. Category Number Age Gender(F/M) CDR MMSE 
AD 214 74.1 ± 7.8 96/118 0.9 ± 0.6 22.2 ± 4.3 
CN 326 76.3 ± 6.2 162/164 0 ± 0 28.6 ± 1.3 
MCI 226 76.2 ± 7.3 81/145 0.6 ± 0.2 25.8 ± 4.4  
Table 2 
Imaging parameters of the scanner.

**Passage 8:**

> 5
adni.loni.usc.edu/ ). ADNI is a multicenter longitudinal study designed 
to assist physicians in researching and developing the most effective 
clinical diagnostic and therapeutic protocols for AD. The database pre -
sents four studies (ADNI-1, ADNI-2, ADNI-GO, and ADNI-3). Following 
the methodology described in [ 43 ], we selected 766 subjects from the 
ADNI-GO and ADNI-2 phases who obtained MRI and PET images at 
baseline (10 months). These included 214 CE subjects, 326 CN subjects, 
and 226 MCI subjects. Each subject had one T1-weighted MRI image in 
NIFTI file format and one PET (FDG-PET) image. Table 1 shows the 
detailed information of the selected subjects. Due to the ADNI volunteers being sourced from various countries 
and regions, the imaging equipment used for scanning differs across all 
subjects.

**Passage 9:**

> r(F/M) CDR MMSE 
AD 214 74.1 ± 7.8 96/118 0.9 ± 0.6 22.2 ± 4.3 
CN 326 76.3 ± 6.2 162/164 0 ± 0 28.6 ± 1.3 
MCI 226 76.2 ± 7.3 81/145 0.6 ± 0.2 25.8 ± 4.4  
Table 2 
Imaging parameters of the scanner. Imaging 
Parameter 
Manufacturer 
SIEMENS Philips Medical 
Systems 
GE Medical 
Systems 
repetition time 
[TR]/ms 
3000 6.8005 7.332 
echo time [TE]/ms 3.5 3.116 3.036 
inversion time [TI]/ 
ms 
1000 0 400 
flip angle/
◦
8 9 11 
thickness/mm 1.2 1.2 1.2 
matrix size/voxel 192 × 192 ×
160 
256 × 256 × 170 256 × 256 × 196 
field strength/T 3.0 3.0 3.0  
C. Tang et al. Computer Methods and Programs in Biomedicine 254 (2024) 108259
5
adni.loni.usc.edu/ ). ADNI is a multicenter longitudinal study designed 
to assist physicians in researching and developing the most effective 
clinical diagnostic and therapeutic protocols for AD.

**Passage 10:**

> tural fea -
tures of MRI. The input feature map of SFE is represented by input1 and input2. 
where input1 represents X
i   1
MRI
( i = 1 , 2 , 3 ) and input2 represents X
i   1
PET
( i =
1 , 2 , 3 ) . When i = 1, the outputs of the LFE block on both branches are 
used as inputs to the SFE. When i > 1, the outputs of the previous SFE 
and FFE blocks in the CEFM are used as inputs to the SFE block. To fully 
extract structural information from MR images and enhance the inter -
action of low-level features of different modalities, SFE employs a two- 
level residual architecture. Specifically, the feature map X
i   1
MRI
∈ R
H × W × C 
is fed into the first-stage 
residual architecture ResBlock1 to extract structural features. Where H, 
W , and C denote the height, width, and number of channels of the 
feature map, respectively.

**Passage 11:**

> idence of brain atrophy, white matter damage, and 
functional adaptive changes in patients with cervical spondylosis and prolonged 
spinal cord compression, Eur. Radiol. 30 (2020) 357 – 369 . 
[57] N. Mancho-Fora, et al., Network change point detection in resting-state functional 
connectivity dynamics of mild cognitive impairment patients, Int. J. Clin. Health 
Psychol. 20 (3) (2020) 200 – 212 . 
[58] Y. Wu, Y. Zhou, W. Zeng, Q. Qian, M. Song, An attention-based 3D CNN with multi- 
scale integration block for Alzheimer ’ s disease classification, IEEE J. Biomed. Health Inform. 26 (11) (2022) 5665 – 5673 . 
[59] X. Zhang, L. Han, W. Zhu, L. Sun, D. Zhang, An explainable 3D residual self- 
attention deep neural network for joint atrophy localization and Alzheimer ’ s 
disease diagnosis using structural MRI, IEEE J. Biomed. Health Inform. 26 (11) 
(2021) 5289 – 5297 . 
[60] C. Lian, M.

**Passage 12:**

>   1
MRI
)
, (5)  
f
 
X
i   1
MRI
)
= ResBlock 1
 
X
i   1
MRI
)
, (6)  
where Conv denotes the convolution layers, k denotes the kernel size, C
in 
Fig. 3. Structural Feature Enhancement Block (SFE). X
i   1
MRI 
and X
i   1
PET
denote the MRI and PET feature maps of the input of stage i   1, and X
i
MRI 
denotes the enhanced 
MRI structural feature map of the output of stage i   1, which is one of the inputs of the SEF Block in stage i . Algorithm 1 
The procedure of SFE. C. Tang et al. Computer Methods and Programs in Biomedicine 254 (2024) 108259
8
Algorithm 2 
The procedure of FFE. Fig. 4. Efficient channel spatial attention (ECSA). C. Tang et al. Computer Methods and Programs in Biomedicine 254 (2024) 108259
9
Fig. 5. Multi-scale attention guided block (MSAG). Algorithm 3 
The procedure of MSAG. C. Tang et al.

**Passage 13:**

> (f) represents the axial image of 
PET. Fig. 1 (a) is the origin corrected image after removing the neck, 
Fig. 1 (b) is the sliced image after skull stripping based on the corrected 
image, and Fig. 1 (c) is the final image obtained after further noise 
elimination on the skull-stripped image. The same processing was 
applied to PET images. 3.2. Overview of proposed MACFNet 
We propose the MACFNet, which is mainly composed of the cross- 
enhanced fusion (CEFM) module and the multi-scale attention guid -
ance (MSAG) module. Fig. 2 shows the overall architecture of MACFNet. It consists of two dual-branch structures with different computational 
complexity.

**Passage 14:**

> 99.68 
w/o ECSA 96.04 98.18 96.55 99.26 
(* SEN: sensitivity; SPE: specificity; ACC: accuracy, ’ w/o ’ means without). Table 5 
Ablation experiments of CEFM and MSAG in different classification tasks. Task Method RN CEFM MSAG SEN(%) SPE(%) ACC(%) AUC(%) 
AD/CN MACFNet √ √ √ 99.91 98.92 99.59 99.94 
w/o CEFM √  √ 99.72 96.09 98.54 99.90 
w/o MSAG √ √  99.75 98.33 99.28 99.72 
w/o CEFM & MSAG √   98.39 94.93 98.21 99.80 
AD/MCI MACFNet √ √ √ 99.89 97.17 98.85 99.91 
w/o CEFM √  √ 99.88 96.05 98.60 99.94 
w/o MSAG √ √  99.76 96.72 98.47 99.89 
w/o CEFM & MSAG √   97.67 95.44 98.17 99.81 
CN/MCI MACFNet √ √ √ 99.63 99.58 99.61 99.98 
w/o CEFM √  √ 98.86 99.11 98.98 99.98 
w/o MSAG √ √  99.61 99.31 99.47 99.97 
w/o CEFM & MSAG √   98.16 98.78 98.83 99.91 
AD/CN/MCI MACFNet √ √ √ 97.75 99.04 98.23 99.89 
w/o CEFM √  √ 97.72 99.02 98.19 99.71 
w/o MSAG √ √  96.12 98.5 97.34 99.68 
w/o CEFM & MSAG √   96.21 98.46 97.19 99.68 
* (RN means ResNet).

**Passage 15:**

> ROI regions are distributed throughout 
Fig. 9. The visualization of MACFNet using Grad-CAM. C. Tang et al. Computer Methods and Programs in Biomedicine 254 (2024) 108259
16
the entire brain portion. This is because the entire brain of the subject 
undergoes atrophy at the AD stage. As can be seen in Fig. 9 (b), the ROI regions of MCI subjects are 
relatively concentrated. This is because MCI, as a precursor stage of AD, 
has no obvious brain changes, and brain atrophy occurs in localized 
areas. In addition, it can be seen from Fig. 9 (d)-(f) that the heat map of the 
PET image focuses on different areas from that of the MRI. That is mainly 
caused by the different imaging mechanisms. This result further dem -
onstrates that integrating different modalities enables the acquisition of 
complementary information, which can help diagnose AD. 6.

**Passage 16:**

> Computer Methods and Programs in Biomedicine 254 (2024) 108259
Available online 6 June 2024
0169-2607/© 2024 The Authors. Published by Elsevier B.V. This is an open access article under the CC BY license ( http://creativecommons.org/licenses/by/4.0/).

**Passage 17:**

> 3 99.91 
AD/CN/MCI MACFNet √ √ √ 97.75 99.04 98.23 99.89 
w/o CEFM √  √ 97.72 99.02 98.19 99.71 
w/o MSAG √ √  96.12 98.5 97.34 99.68 
w/o CEFM & MSAG √   96.21 98.46 97.19 99.68 
* (RN means ResNet). C. Tang et al. Computer Methods and Programs in Biomedicine 254 (2024) 108259
11
W
k
=
⎡
⎢
⎢
⎢
⎢
⎢
⎢
⎣
ω
1 , 1
mri
⋯ ω
1 , k
mri
0 0 ⋯ ⋯ 0
0 ω
2 , 2
mri
⋯ ω
2 , k + 1
mri
0 ⋯ ⋯ 0
⋮ ⋮ ⋮ ⋮ ⋱ ⋮ ⋮ ⋮
0 ⋯ 0 0 ⋯ ω
C , C   k + 1
mri
⋯ ω
C , C
mri
⎤
⎥
⎥
⎥
⎥
⎥
⎥
⎦
, (12)  
where k denotes the number of cross-channels, C denotes the number of 
channels of the input band matrix, and ω represents the learnable 
channel weights, the channel weights ω
i 
can be obtained by computing 
the interactions between 
̃
X
i
( i = 1 , 2 ..

**Passage 18:**

> data are disseminated by the Laboratory 
for Neuro Imaging at the University of Southern California. Appendix 
Table 7 shows the mathematical symbols used in this paper. Table 7 
Mathematical symbols. Symbol Meaning 
+ Element-wise add 
× Multiplication operation 
⊗ Element-wise product 
concat Concatenation operation 
max Maximum value 
Min Minimum value 
X Input feature map 
f ( X ) Output feature map 
R Set of real numbers 
H The height of the feature map 
W The width of the feature map 
C The number of channels of the feature map 
( w, h ) Coordinate of pixel 
( continued on next page ) 
C. Tang et al.

**Passage 19:**

> he 
ResBlock1 output feature map f
 
X
i   1
MRI
)
. To extract functional features from PET images, the feature map 
X
i   1
PET
∈ R
H × W × C 
has also been processed by the same residual structure. The outputs of these two residual structures are concatenated in the 
channel dimension to initially fuse structural and functional features, 
and the fusion process can be described as below: 
f
Z
 
X
fusion
)
= concat
[
f
 
X
i   1
MRI
)
, f
 
X
i   1
PET
)]
, f
Z
 
X
fusion
)
∈ R
H × W × 2 C
, (7)  
where f
Z
( X
fusion
) represents the fused feature map, f
 
X
i   1
MRI
)
and f
 
X
i   1
PET
)
represent the output of ResBlock1 on the respective corresponding 
branch.

**Passage 20:**

> l neuroimaging for AD diagnosis, ignoring clinical and biological 
information. In addition, MACFNet performs feature extraction on the 
whole image, ignoring features in ROI regions such as GM or WM. In the 
future, we will consider extracting and analyzing ROI features from 
neuroimaging data while further optimizing the variants of MACFNet by 
combining clinical data to improve the model ’ s generalization ability. CRediT authorship contribution statement 
Chaosheng Tang: Writing – original draft, Visualization, Formal 
analysis, Conceptualization. Mengbo Xi: Validation, Software, Re -
sources, Investigation. Junding Sun: Writing – original draft, Visuali -
zation, Supervision, Software. Shuihua Wang: Writing – review & 
editing, Validation, Investigation, Funding acquisition. Yudong Zhang: 
Writing – review & editing, Validation, Software, Funding acquisition.

**Passage 21:**

> s used to ensure that the outputs Y
1
, Y
2
, 
and Y
3 
have the same size, and the output of each scale via the BN and 
ReLu activation functions: 
Table 6 
Performance comparison with other methods. Task Method SEN 
(%) 
SPE 
(%) 
ACC 
(%) 
AUC 
(%) 
AD/CN Song et al.(2021) [ 37 ] 93.33 94.27 94.11 n/a 
Zhang et al.(2019) 
[ 54 ] 
96.58 95.39 98.47 98.61 
Fang et al.(2020) [ 52 ] 95.89 98.72 99.27 n/a 
Gao et al.(2022) [ 26 ] 91.70 93.50 92.70 96.4 
Zhang et al.(2022) 
[ 53 ] 
n/a n/a 96.23 99.00 
Tu et al.(2022) [ 16 ] 97.40 93.00 96.20 98.60 
Abde et al.(2022) [ 30 ] 98.82 97.52 98.24 97.70 
Shi et al.(2022) [ 31 ] 96.10 97.47 96.76 97.03 
Leng et al.(2023) [ 45 ] 97.22 98.21 97.67 98.55 
Ismail et al.(2023) 
[ 35 ] 
95.00 94.00 94.40 n/a 
MACFNet(ours) 99.91 98.92 99.59 99.88 
AD/MCI Song et al.(2021) [ 37 ] 71.19 85.94 80.80 n/a 
Zhang et al.(2019) 
[ 54 ] 
97.43 84.31 88.20 88.01 
Fang et al.(2020) [ 52 ] 89.71 93.59 92.57 n/a 
Zhang et al.(2022) 
[ 53 ] 
n/a n/a 88.12 91.00 
Liu et al.(2022) [ 47 ] 94.91 98.52 94.44 97.00 
Ismail et al.(2023) 
[ 35 ] 
89.20 93.30 90.00 n/a 
MACFNet(ours) 99.89 97.07 98.85 99.90 
CN/MCI Song et al.(2021) [ 37 ] 84.69 85.60 85.00 n/a 
Zhang et al.(2019) 
[ 54 ] 
90.11 91.82 85.74 88.15 
Fang et al.(2020) [ 52 ] 88.36 92.56 90.35 n/a 
Zhang et al.(2022) 
[ 53 ] 
n/a n/a 87.45 95.0 
Abde et al.(2022) [ 30 ] 90.26 96.98 94.59 93.3 
Shi et al.(2022) [ 31 ] 85.98 70.90 80.73 78.75 
Ismail et al.(2023) 
[ 35 ] 
96.00 89.20 93.20 n/a 
MACFNet(ours) 99.63 99.58 99.61 99.98 
AD/CN/ 
MCI 
Song et al.(2021) [ 37 ] 55.67 83.40 71.52 n/a 
Zhang et al.(2022) 
[ 53 ] 
n/a n/a 80.34 95.00 
Golo et al.(2022) [ 43 ] n/a n/a 96.88 n/a 
Han et al.(2022) [ 55 ] n/a n/a 67.74 n/a 
Ismail et al.(2023) 
[ 35 ] 
n/a n/a 92.30 n/a 
MACFNet(ours) 97.75 99.04 98.23 99.82 
(* Bold indicates the best value in terms of the evaluation indicator. ’ n/a ’ means 
not available.).

**Passage 22:**

> he 
fusion and interaction of MRI and PET low-level features through 
the cross-over mechanism. In addition, the ECSA attention 
mechanism is designed to effectively focus on important 
C. Tang et al. Computer Methods and Programs in Biomedicine 254 (2024) 108259
3
information related to AD for MRI structural feature enhance -
ment and PET functional feature enhancement.  
(3) A concise multi-scale attention guidance block is proposed by 
setting different dilation rates to obtain different receptive fields. It can also get discriminative information related to AD via hard 
attention with different scales. The rest of the paper is arranged as follows: Section 2 introduces the 
related work, Section 3 introduces the proposed methodology, Section 4 
introduces the experimental results, Section 5 the discussion, and Sec -
tion 6 is the conclusion. 2.

**Passage 23:**

> RI and DTI images. They 
proposed a two-way attention mechanism, which can extract fMRI 
functional features and DTI structural features by CNNs and Graph 
Convolutional Networks (GCNs), respectively. The features of different 
modalities are fused layer by layer and then fed into the Transformer 
model to realize AD diagnosis. However, their approach implements the 
self-attention mechanism by computing a set of query matrix Q, key 
matrix K, and value matrix V by linear projection, which has a high time 
complexity. In addition, their method transforms functional information 
and structural information into each other to achieve the fusion of 
complementary information, which may lead to the loss of important 
features of individual modalities.

**Passage 24:**

> attention deep neural network for joint atrophy localization and Alzheimer ’ s 
disease diagnosis using structural MRI, IEEE J. Biomed. Health Inform. 26 (11) 
(2021) 5289 – 5297 . 
[60] C. Lian, M. Liu, Y. Pan, D. Shen, Attention-guided hybrid network for dementia 
diagnosis with structural MR images, IEEE Trans. Cybern. 52 (4) (2020) 
1992 – 2003 . C. Tang et al.

</details>

---

## Machine-learning-based-prediction-of-single-frequency-v_2025_Computers-in-Bi
_File: `Machine-learning-based-prediction-of-single-frequency-v_2025_Computers-in-Bi.pdf`_

1. **Was diffusion MRI (DTI, dMRI, DWI, or similar) used in this paper?**  
   Yes. The paper explicitly mentions "Diffusion Tensor Imaging (DTI)" and "diffusion MRI data" in the abstract and other sections. For example:  
   - "Characterizing brain white matter (BWM) using in vivo Magnetic Resonance Elastography (MRE) and Diffusion Tensor Imaging (DTI) is a costly, time-intensive process."  
   - "The overarching aim of the developed ML predictive workflow [...] is to integrate MRE- and DTI-derived physics into computational brain white matter models."  

---

2. **What processing steps were applied to the diffusion images?**  
   The following steps are explicitly stated:  
   - Creating **3D Representative Volume Elements (RVEs)** from microscopic imaging data to capture microstructure (e.g., fiber diameter variations, orientation dispersion).  
   - Integrating these **3D RVEs** into a macro-scale BWM model to represent geometry and material properties.  
   - Incorporating **geometric parameters** like axon tortuosity and varying volume fractions.  
   - Using **machine learning (ML)** to predict viscoelastic properties (e.g., storage modulus) from DTI data.  

---

3. **What software or tools are explicitly named for processing?**  
   No specific software or tools for diffusion MRI processing are explicitly named. The paper mentions integration with commercial finite element (FE) platforms like **ABAQUS** and **LS-DYNA**, but these are for simulation frameworks, not diffusion MRI processing.  

---

4. **What acquisition or processing parameters are explicitly reported?**  
   The following parameters are explicitly reported:  
   - **Voxel size**: "1.6 mm isotropic voxels" (from references to MRE/DTI co-registration).  
   - **Acquisition methods**: "Dual-directional mechanical excitation" (related to MRE/DTI sequences).  
   - **Microstructural metrics**: Effective radial diffusivity, fiber volume fraction, and g-ratio (derived from DTI).  

---

5. **Copy the exact sentences from the excerpts that describe the processing.**  
   - "Characterizing brain white matter (BWM) using in vivo Magnetic Resonance Elastography (MRE) and Diffusion Tensor Imaging (DTI) is a costly, time-intensive process."  
   - "The RVE geometry consists of three compartments: axons, the surrounding myelin sheath, and a viscoelastic glial phase."  
   - "The overarching aim of the developed ML predictive workflow [...] is to establish a systematic, modular data-driven ML framework capable of integrating MRE- and DTI-derived physics into computational brain white matter models."  

---

6. **Is the processing description complete, or does it appear incomplete/missing?**  
   The processing description appears **incomplete**. While the paper outlines the use of DTI data and integration with ML models, it does not detail specific diffusion MRI processing steps (e.g., tensor calculation, tractography, or parameter estimation). The focus is on modeling and ML workflows rather than explicit diffusion MRI processing pipelines.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> .J. Sharp, Individual prediction of 
white matter injury following traumatic brain injury, Ann. Neurol. 73 (4) (2013) 
489 – 499, 0364-5134 .
[45] L. Jollans, R. Boyle, E. Artiges, T. Banaschewski, S. Desrivi `eres, A. Grigis, J.- 
L. Martinot, T. Paus, M.N. Smolka, H. Walter, Quantifying performance of machine 
learning methods for neuroimaging data, Neuroimage 199 (2019) 351 – 365, 1053- 
8119 .
[46] P. Sabeghi, K.K. Kinkar, G.d.R. Castaneda, L.S. Eibschutz, B.K. Fields, B. A. Varghese, D.B. Patel, A. Gholamrezanezhad, Artificial intelligence and machine 
learning applications for the imaging of bone and soft tissue tumors, Frontiers in 
Radiology 4 (2024) 1332535, 2673-8740 .
[47] M. Cilla, I. P ´erez-Rey, M.A. Martínez, E. Pena, J.

**Passage 2:**

> 111152 
16 
International Mechanical Engineering Congress and Exposition, 85598, American 
Society of Mechanical Engineers, 2021 V005T005A050 .
[39] I. El Naqa, M.J. Murphy, What Is Machine Learning? Springer, 2015 .
[40] T. Wu, J.A. Rifkin, A. Rayfield, M.B. Panzer, D.F. Meaney, An interdisciplinary 
computational model for predicting traumatic brain injury: linking biomechanics 
and functional neural networks, Neuroimage 251 (2022) 119002, 1053-8119 .
[41] C.-L. Chen, Y.-C. Shih, H.-H. Liou, Y.-C. Hsu, F.-H. Lin, W.-Y.I. Tseng, Premature 
white matter aging in patients with right mesial temporal lobe epilepsy: a machine 
learning approach based on diffusion MRI data, Neuroimage: Clinical 24 (2019) 
102033, 2213-1582 .
[42] I. Beheshti, M. Ganaie, V. Paliwal, A. Rastogi, I. Razzak, M.

**Passage 3:**

> neuroimaging in amyotrophic 
lateral sclerosis, Nat. Rev. Neurol. 9 (9) (2013) 513 – 524, 1759-4758 .
[5] G.W. Duncan, M.J. Firbank, A.J. Yarnall, T.K. Khoo, D.J. Brooks, R.A. Barker, D. J. Burn, J.T. O ’ Brien, Gray and white matter imaging: a biomarker for cognitive 
impairment in early P arkinson ’ s disease? Mov. Disord. 31 (1) (2016) 103 – 110, 
0885-3185 .
[6] D.J. Sullivan, X. Wu, N.R. Gallo, N.M. Naughton, J.G. Georgiadis, A.A. Pelegri, 
Sensitivity analysis of effective transverse shear viscoelastic and diffusional 
properties of myelinated white matter, Phys. Med. Biol. 66 (3) (2021) 035027, 
0031-9155 .
[7] S. Axelrod, D. Schwalbe-Koda, S. Mohapatra, J. Damewood, K.P. Greenman, 
R. G ´omez-Bombarelli, Learning matter: materials design with machine learning 
and atomistic simulations, Acc. Mater. Res. 3 (3) (2022) 343 – 357, 2643-6728 .
[8] M. Zhou, G.

**Passage 4:**

> workflow for brain tissue modeling
The proposed ML workflow can be enhanced by extending the cur -
rent 2D FEM model to a 3D representation of brain white matter (BWM) 
using microscopic imaging data. This involves creating 3D Representa -
tive Volume Elements (RVEs) that capture the detailed microstructure, 
including fiber diameter variations and orientation dispersion. These 3D 
RVEs will be integrated into a macro-scale BWM model to represent the 
geometry and material properties more accurately across multiple 
scales. Additional geometric parameters, such as axon tortuosity [ 37 ] 
and varying volume fractions, will be incorporated to improve the fi -
delity of material property estimation. For constituent phase properties, more sophisticated orthotropic and 
anisotropic material models will be employed to capture the complex 
behavior of 3D brain tissues.

**Passage 5:**

> B.P. Sutton, E.E. Van Houten, J.G. Georgiadis, J. B. Weaver, K.D. Paulsen, Including spatial information in nonlinear inversion MR 
elastography using soft prior regularization, IEEE Trans. Med. Imag. 32 (10) (2013) 
1901 – 1909, 0278-0062 .
[14] C.L. Johnson, M.D. McGarry, A.A. Gharibans, J.B. Weaver, K.D. Paulsen, H. Wang, 
W.C. Olivero, B.P. Sutton, J.G. Georgiadis, Local mechanical properties of white 
matter structures in the human brain, Neuroimage 79 (2013) 145 – 152, 1053-8119 .
[15] C.L. Johnson, M.D. McGarry, E.E. Van Houten, J.B. Weaver, K.D. Paulsen, B. P. Sutton, J.G. Georgiadis, Magnetic resonance elastography of the brain using 
multishot spiral readouts with self-navigated motion correction, Magn. Reson. Med. 70 (2) (2013) 404 – 412, 0740-3194 .
[16] C.L. Johnson, J.L. Holtrop, M.D. McGarry, J.B. Weaver, K.D. Paulsen, J. G. Georgiadis, B.P.

**Passage 6:**

> van 
et al. [ 6 ]. 1.3. Machine learning – data science
Machine learning (ML) algorithms are used to find patterns in data or 
to make predictions based on experience/training on existing data [ 39 ]. The efficacy of machine learning programs are highly dependent on the 
quantity of data. In recent years, neuroscientist and brain research 
community has started leveraging Artificial Intelligence (AI)/Machine 
learning (ML) models to understand complex brain biomechanics [ 40 ], 
aging [ 35 , 41 , 42 ], and injury (i.e. traumatic brain injury [ 43 , 44 ]) 
response. The present study addresses the following objectives/aims. 
• Develop an end-to-end ML/data-science workflow for predicting 
effective metrics for MRE and DTI, based on a synthetic 2D FEM 
generated training dataset.

**Passage 7:**

> ised form 21 September 2025; Accepted 25 September 2025  
Computers in Biology and Medicine 198 (2025) 111152 
Available online 4 October 2025 
0010-4825/© 2025 The Authors. Published by Elsevier Ltd. This is an open access article under the CC BY-NC license ( http://creativecommons.org/licenses/by- 
nc/4.0/ ). 
forward ML solution has been developed, which leverages a prior 2D 
viscoelastically (VE) modeled BWM FEM data pool from previous 
research done by our group [ 6 ] to build a forward predictive Machine 
learning (ML) model pipeline. These ML models will serve to facilitate 
data-driven tissue characterization by eliminating the need to solve FEM 
codes and directly predict VE modeled brain matter properties (such as 
storage modulus ) to interpret brain matter ’ s VE response.

**Passage 8:**

> temporal lobe epilepsy: a machine 
learning approach based on diffusion MRI data, Neuroimage: Clinical 24 (2019) 
102033, 2213-1582 .
[42] I. Beheshti, M. Ganaie, V. Paliwal, A. Rastogi, I. Razzak, M. Tanveer, Predicting 
brain age using machine learning algorithms: a comprehensive evaluation, IEEE 
Journal of Biomedical Health Informatics 26 (4) (2021) 1432 – 1440, 2168-2194 .
[43] S. van Hal, M. van der Jagt, M. van Genderen, D. Gommers, J. Veenland, Using 
artificial intelligence to predict intracranial hypertension in patients after 
traumatic brain injury: a systematic review, Neurocritical Care (2024) 1 – 12, 1541- 
6933 .
[44] P.J. Hellyer, R. Leech, T.E. Ham, V. Bonnelle, D.J. Sharp, Individual prediction of 
white matter injury following traumatic brain injury, Ann. Neurol. 73 (4) (2013) 
489 – 499, 0364-5134 .
[45] L. Jollans, R. Boyle, E. Artiges, T. Banaschewski, S.

**Passage 9:**

> models for age-related brain degeneration or classification models for 
tissue differentiation [ 18 ]. This would establish a versatile 
regression-classification ML pipeline for neuroimaging studies. A practical consideration for future research is the integration of 
such AI frameworks into widely used commercial FE platforms such as 
ABAQUS and LS-DYNA. Both software environments allow user-defined 
subroutines (e.g., UMAT/VUMAT in ABAQUS, or *MAT user-defined 
models in LS-DYNA) for implementing custom constitutive material 
behavior. In principle, the trained ML models presented in this research 
could be embedded into these subroutines by exporting them into 
lightweight surrogate formats (e.g., ONNX, TensorFlow Lite, or PyTorch 
JIT) and then interfacing through Fortran/C ++ wrappers.

**Passage 10:**

> orest Regression
MLP Multilayer Perceptron
GBDT Gradient Boosting Decision Trees
DT Decision Tree
MSE Mean Squared Error
BWM Brain White Matter
G ′ Storage Modulus
G ″ Loss modulus
M. Agarwal and A.A. Pelegri                                                                                                                                                                                                                 Computers in Biology and Medicine 198 (2025) 111152 
2 
state simulations. These metrics are computed in the same RVE 
(representing a co-registered MRE/DTI voxel) directly from the un -
derlying physics, rather than for specific MRE or DTI sequences.

**Passage 11:**

> Machine learning based prediction of single-frequency viscoelastic brain 
white matter – A data science framework
M. Agarwal
a , b
, Assimina A. Pelegri
a , b , *
a
Mechanical and Aerospace Engineering, Rutgers University-New Brunswick, Piscataway, NJ, 08854, USA
b
Advanced Materials & Structures Laboratory, Rutgers University-New Brunswick, Piscataway, NJ, 08854, USA
ARTICLE INFO
Keywords:
T.B.I. Machine learning
Computational mechanics
Sensitivity
Finite element simulation
Data science
ABSTRACT
Characterizing brain white matter (BWM) using in vivo Magnetic Resonance Elastography (MRE) and Diffusion 
Tensor Imaging (DTI) is a costly, time-intensive process. Numerical modeling approaches, such as finite element 
models (FEMs), also face limitations in fidelity, computational resources, and accurately capturing the complex 
bio-physical behavior of brain tissues.

**Passage 12:**

> ly influenced 
the predictions. This framework offers a cost-effective alternative to in vivo characterization and computa -
tionally expensive physics based direct numerical simulation methods (FEM). It would also provide a basis for 
future ML-driven inverse models to explore the impact of various brain matter constituents on neuroimaging 
characteristics, potentially informing studies on aging, dementia, and traumatic brain injuries. 1. Introduction
Brain white matter (BWM), constituting approximately 50 % of the 
brain and up to 80 % of the spinal cord, plays a critical role in neuro -
degenerative progression and traumatic brain injuries (TBI) [ 1 , 2 ]. Demyelination and WM integrity are crucial in determining the degree 
of TBI, multiple sclerosis, and vascular dementia.

**Passage 13:**

> readouts with self-navigated motion correction, Magn. Reson. Med. 70 (2) (2013) 404 – 412, 0740-3194 .
[16] C.L. Johnson, J.L. Holtrop, M.D. McGarry, J.B. Weaver, K.D. Paulsen, J. G. Georgiadis, B.P. Sutton, 3D multislab, multishot acquisition for fast, whole-brain 
MR elastography with high signal-to-noise efficiency, Magn. Reson. Med. 71 (2) 
(2014) 477 – 485, 0740-3194 .
[17] A.T. Anderson, E.E. Van Houten, M.D. McGarry, K.D. Paulsen, J.L. Holtrop, B. P. Sutton, J.G. Georgiadis, C.L. Johnson, Observation of direction-dependent 
mechanical properties in the human brain with multi-excitation MR elastography, 
J. Mech. Behav. Biomed. Mater. 59 (2016) 538 – 546, 1751-6161 .
[18] M. Agarwal, J. Georgiadis, A.A.

**Passage 14:**

> ical 
Engineers, 2022 V004T005A046 .
[37] M. Agarwal, P. Pasupathy, A.A. Pelegri, Oligodendrocyte tethering effect on 
hyperelastic 3D response of axons in white matter, J. Mech. Behav. Biomed. Mater. 134 (2022) 105394, 1751-6161 .
[38] M. Agarwal, P. Pasupathy, R. De Simone, A.A. Pelegri, Oligodendrocyte tethering 
effect on hyperelastic 3D response of injured axons in brain white matter, in: ASME 
M. Agarwal and A.A. Pelegri                                                                                                                                                                                                                 Computers in Biology and Medicine 198 (2025) 111152 
16 
International Mechanical Engineering Congress and Exposition, 85598, American 
Society of Mechanical Engineers, 2021 V005T005A050 .
[39] I. El Naqa, M.J. Murphy, What Is Machine Learning?

**Passage 15:**

> rection-dependent 
mechanical properties in the human brain with multi-excitation MR elastography, 
J. Mech. Behav. Biomed. Mater. 59 (2016) 538 – 546, 1751-6161 .
[18] M. Agarwal, J. Georgiadis, A.A. Pelegri, Data-driven depiction of aging related 
physiological volume shrinkage in brain white matter: an image processing based 
three-dimensional micromechanical model, Journal of Engineering Science in 
Medical Diagnostics Therapy 8 (4) (2025) 2572 – 7958 .
[19] H.-H. Lee, E. Fieremans, D.S. Novikov, What dominates the time dependence of 
diffusion transverse to axons: Intra-or extra-axonal water? Neuroimage 182 (2018) 
500 – 510, 1053-8119 .
[20] H.-H. Lee, K. Yaros, J. Veraart, J.L. Pathan, F.-X. Liang, S.G. Kim, D.S. Novikov, 
E.

**Passage 16:**

> l resolution and 
accuracy of in vivo brain MRE improves, first achieving 2 mm ( McGarry 
et al. [ 12 , 13 ] and Johnson et al. [ 14 , 15 ]) and then 1.6 mm isotropic 
voxels ( Johnson et al. [ 16 ]). Studies have shown that dual-directional 
mechanical excitation reveals significant spatial discrepancies — up to 
33 % — in reconstructed viscoelastic moduli ( Anderson et al. [ 17 ]) across 
aligned white matter tracts, underscoring the critical need for inversion 
models that incorporate mechanical anisotropy to accurately interpret 
localized stiffness metrics. The role of tissue microarchitecture in governing mechanical 
anisotropy has been effectively leveraged to interpret MRE-derived 
stiffness changes associated with normal brain aging [ 18 ].

**Passage 17:**

> f 
diffusion transverse to axons: Intra-or extra-axonal water? Neuroimage 182 (2018) 
500 – 510, 1053-8119 .
[20] H.-H. Lee, K. Yaros, J. Veraart, J.L. Pathan, F.-X. Liang, S.G. Kim, D.S. Novikov, 
E. Fieremans, Along-axon diameter variation and axonal orientation dispersion 
revealed with 3D electron microscopy: implications for quantifying brain white 
matter microstructure with histology and diffusion MRI, Brain Struct. Funct. 224 
(2019) 1469 – 1488, 1863-2653 .
[21] R.M. Christensen, Mechanics of composite materials, Courier Corporation (2005) .
[22] M. Agarwal, P. Pasupathy, X. Wu, S.S. Recchia, A.A. Pelegri, Multiscale 
computational and artificial intelligence models of linear and nonlinear 
composites: a review, Small Science 2688 – 4046 (2024) 2300185 .
[23] N. Abolfathi, A. Naik, M. Sotudeh Chafi, G. Karami, M.

**Passage 18:**

> th reasonable data-processing 
efforts, the same code can be used to predict properties for other com -
posite families (both soft and hard non-linear materials via Transfer 
Learning [ 8 , 9 ]). 1.1. Brain matter tissue characterization and sensitivity
Advanced imaging such as MRE and dMRI, reflects voxel-averaged 
(effective) properties to account for the microstructure and intrinsic 
properties of the cell constituent components in each voxel. Unlike DTI, 
the isotropic MRE material model returns a single property pair (stiff -
ness or storage modulus, G ′ , and loss modulus, G ″ ) that is some com -
posite of direction-dependent shear moduli and thus is inadequate for 
separating contributions to tissue stiffness from axons and glia, or from 
their interface.

**Passage 19:**

> erse problem 
with white matter microarchitecture and intrinsic properties of its 
constituents phases. Fig. 12. (a) Force plot – SHAP on the training set data (b) Force plot on the test set. Fig. 13. Waterfall plot visualizing individual features contribution to a single prediction, starting from the predictive ML model ’ s baseline (average prediction) and 
displaying how each feature value shifts the prediction higher or lower. M. Agarwal and A.A. Pelegri                                                                                                                                                                                                                 Computers in Biology and Medicine 198 (2025) 111152 
14 
7. Model limitations & outlook
7.1.

**Passage 20:**

> metrics. The role of tissue microarchitecture in governing mechanical 
anisotropy has been effectively leveraged to interpret MRE-derived 
stiffness changes associated with normal brain aging [ 18 ]. Although 
MRE and DTI are sensitive to micrometer-scale proton displacements, 
both modalities are constrained by a spatial resolution of approximately 
1 mm, limiting their ability to resolve cellular-level heterogeneity. A 
promising strategy to recover microstructural information is to model 
brain white matter (BWM) as a unidirectional composite, consisting of 
myelinated axons embedded within a glial matrix, akin to biophysical 
DTI models [ 19 ]. This micromechanical representation, supported by 
histological micrographs of BWM cytoarchitecture [ 20 ], provides a 
canonical framework for simulating directional mechanical behavior.

**Passage 21:**

> 2 
state simulations. These metrics are computed in the same RVE 
(representing a co-registered MRE/DTI voxel) directly from the un -
derlying physics, rather than for specific MRE or DTI sequences. The overarching aim of the developed ML predictive workflow 
(forward model) is to establish a systematic, modular data-driven ML 
framework capable of integrating MRE- and DTI-derived physics into 
computational brain white matter models. Specifically, the workflow is 
designed to extract and predict MRE-derived viscoelastic metrics , such 
as the effective shear storage and loss moduli, and DTI-derived micro -
structural metrics , including effective radial diffusivity, fiber volume 
fraction, and g-ratio.

**Passage 22:**

> Pelegri, Finite element modeling of CNS 
white matter kinematics: use of a 3D RVE to determine material properties, Front. Bioeng. Biotechnol. 1 (2013) 19, 2296-4185 .
[26] Y. Pan, D.I. Shreiber, A.A. Pelegri, On the transversely isotropic, hyperelastic 
response of central nervous system white matter using a hybrid approach, Journal 
of Engineering Science in Medical Diagnostics Therapy (1) (2021) 011005, 2572- 
7958 .
[27] C. Giordano, S. Kleiven, Connecting fractional anisotropy from medical images 
with mechanical anisotropy of a hyperviscoelastic fibre-reinforced constitutive 
model for brain tissue, J. R. Soc. Interface 11 (91) (2014) 20130914, 1742-5689 .
[28] S.A. Yousefsani, A. Shamloo, F. Farahmand, Micromechanics of brain white matter 
tissue: a fiber-reinforced hyperelastic model using embedded element technique, 
J. Mech. Behav. Biomed. Mater.

**Passage 23:**

> that it is transferable to other material applications or soft tissue 
families [ 7 , 44 , 46 ] through transfer learning [ 47 ] or model re-training 
strategies [ 48 ]. 2. Materials and methods
2.1. White matter VE – 2D FEM
Building upon the work of Sullivan et al. [ 6 ], a 2D finite element 
model relevant to MRE is developed to simulate brain white matter 
(WM) mechanics by capturing interactions among axons, glial cells, and 
myelin. This model is the basis for generating a synthetic dataset to train 
and test a predictive machine learning workflow. The RVE geometry 
consists of three compartments: axons, the surrounding myelin sheath, 
and a viscoelastic glial phase. The glial phase includes supportive glial 
cells (e.g., oligodendrocytes, astrocytes) and a softer extracellular matrix 
of glycosaminoglycans and proteoglycans.

**Passage 24:**

> In the brain RVE, the axon diameter is kept fixed and 
equal to 0.7 μ m, but the fiber volume fraction (VF) is varied by tuning 
the overall RVE size. 3. Data science driven forward ML – workflow
3.1. Dataset characteristics – 2D FEM solved data (synthetic dataset)
Exploratory data analysis (EDA) was performed on the synthetic 
dataset generated from the solved 2D FEM model ( § 2.1 ). The dataset 
includes ~2500 samples with variables exhibiting diverse distributions: 
some approximately normal (e.g., GliaStor , HomoStor ), others skewed (e. 
g., AxonLoss , MyelinLoss ), or uniform (e.g., GliaAxon , GliaMyelin ). This 
heterogeneity underscores the need for robust preprocessing and flex -
ible ML models. Fig. 2 presents representative histograms of key 
variables. MyelinStor and AxonStor are left-skewed distributions. MyelinLoss 
and AxonLoss is right-skewed distributions.

</details>

---

## Multi-input-Multi-output-3D-CNN-for-dementia-severit_2024_Artificial-Intelli
_File: `Multi-input-Multi-output-3D-CNN-for-dementia-severit_2024_Artificial-Intelli.pdf`_

1. **Was diffusion MRI (DTI, dMRI, DWI, or similar) used in this paper?**  
   Yes. The paper explicitly mentions "Diffusion Tensor Imaging (DTI-MRI)" as part of the multimodal approach.  

---

2. **What processing steps were applied to the diffusion images?**  
   The excerpts do not explicitly describe processing steps for diffusion images (DTI-MRI). The steps mentioned are for T1w-MRI and PET, such as motion correction, skull-stripping, intensity normalization, and normalization to [0,1]. No specific steps for diffusion MRI are reported.  

---

3. **What software or tools are explicitly named for processing?**  
   No specific software or tools are named. The processing is described as following a procedure reported in [15], but no tools are explicitly cited.  

---

4. **What acquisition or processing parameters are explicitly reported?**  
   - Volumes are normalized to [0,1].  
   - Volumes have dimensions of 25

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> , we want to analyze the differences with
the three-class classification approach, where the three classes are
considered as independent, delegating the model the task of learning
their relationships. The proposed methodology consists of two steps: Pre-processing,
used to prepare MRI and PET, and the Dementia Severity Assessment ,
which introduces the implemented solutions considering multimodal
approaches. 4.1. Pre-processing
T1w-MRI volumes are processed according to the procedure re-
ported in [15], including motion correction, removal of non-brain tissue
Fig. 2.

**Passage 2:**

> ons considering multimodal
approaches. 4.1. Pre-processing
T1w-MRI volumes are processed according to the procedure re-
ported in [15], including motion correction, removal of non-brain tissue
Fig. 2. Extraction of brain region for each patient: the smallest 3D cubical box (in
green) is computed from the rectangular box (in orange) surrounding the brain. (For
interpretation of the references to color in this figure legend, the reader is referred to
the web version of this article.)
(skull-stripping) and intensity normalization. The result is a set of
volumes of size 256 × 256 × 256 with isotropic dimension. A PET scan consists in the acquisition of 3D volumes after the
injection of the tracer, resulting in 4D data.

**Passage 3:**

> ed to the MRI volume acquired during the dynamic PET
scan session using mutual information as a similarity metric [ 44,45]. The result is a PET volume of size 256 × 256 × 256 with isotropic
dimension. To reduce the amount of non-brain tissue to include, the
smallest 3D cubical box including the patient’s brain is extracted from
each MRI and PET volume. The cubical box is patient-dependent and
its dimension strongly depends on the 𝑦 axis, as shown in Fig. 2 . The
resulting volumes are then normalized in [0,1] to ensure that, in the
next stage, the involved CNNs operate on images of the same scale
across different acquisitions. 4.2. Dementia severity assessment
In clinical trials, T1-w MRI and PET are the standard diagnostic
tools used to assess the severity of dementia.

**Passage 4:**

> e on brain informatics. Springer; 2021, p. 486–95.
[30] Jack Jr CR, Bernstein MA, Fox NC, Thompson P, Alexander G, Harvey D, et
al. The Alzheimer’s disease neuroimaging initiative (ADNI): MRI methods. J. Magnetic Reson Imag Official J Int Soc Magnetic Reson Med 2008;27(4):685–91.
[31] Krizhevsky A, Sutskever I, Hinton GE. Imagenet classification with deep
convolutional neural networks. Adv Neural Inf Process Syst 2012;25.
[32] He K, Zhang X, Ren S, Sun J. Deep residual learning for image recognition. In:
Proceedings of the IEEE conference on computer vision and pattern recognition. 2016, p. 770–8.
[33] Szegedy C, Liu W, Jia Y, Sermanet P, Reed S, Anguelov D, et al. Going deeper
with convolutions. In: Proceedings of the IEEE conference on computer vision
and pattern recognition. 2015, p. 1–9.
[34] Simonyan K, Zisserman A. Very deep convolutional networks for large-scale
image recognition.

**Passage 5:**

> e
and after the date of the MRI (or PET) session valid. In particular, we
consider the clinical data closest to each MRI (or PET) session to be a
match if the difference in days is less than one year. We match the MRI
and PET scans to clinical assessments separately, and the result consists
of three different datasets, namely MRI, PET and PAIRED datasets. The MRI and PET datasets include all the MRI and PET volumes,
respectively, with the related CDR value, while the PAIRED dataset
contains only MRI-PET pairs, represented by the MRI and PET volumes
associated with the same clinical information date. Straightforwardly,
both the MRI and PET datasets include the acquisitions of the PAIRED
dataset. It is worth noting that the set of data involved in this paper
represents an incomplete dataset in which, for each assessment, all
image modalities are not always available.

**Passage 6:**

> ial Intelligence In Medicine 149 (2024) 102774
11
M. Gravina et al. Table 8
Performance of the EXP.2 (Task B2) on the MRI dataset. Ba and Re denote the BasicNet and ResNet architectures. Data Net Mod. ACC Precision Recall AUC
M S M S
MRI
Ba U 70.62 ±.09 84.12 ±.05 40.38 ±.16 75.97 ±.12 53.16 ±.14 70.05 ±.06
IF 73.29 ±.03 85.90 ±.39 44.66 ±.06 77.91 ±.06 58.23 ±.14 70.52 ±.05
Re U 68.84 ±.08 86.96 ±.02 40.00 ±.10 69.77 ±.10 65.82 ±.02 68.80 ±.06
IF 82.20±.04 91.25 ±.02 59.79 ±.07 84.88 ±.05 73.42 ±.04 75.44 ±.05
Table 9
Performance of the EXP.2 (Task B2) on the PET dataset. Ba and Re denote the BasicNet and ResNet architectures. Data Net Mod.

**Passage 7:**

> sed a methodology that combines T1-w MRI,
Diffusion Tensor Imaging (DTI-MRI) and 2D ResNet18 [32], represent-
ing the first article that focuses on a multimodal approach with the
OASIS-3 dataset [15]. The majority of papers that use both MRI and PET images focus on
ADNI dataset [30]. In [14] authors used a 2D CNN for the classification
of features extracted from MRI, PET and genetic data, while in [12]
authors proposed a multi-input 3D CNN considering as input the hip-
pocampal area selected from MRI and PET. In [39] sparse autoencoder
and 3D CNN were introduced for classification, while in [13] stacked
Deep Polynomial Networks (DPNs) were used to extract features from
the two image modalities. The solutions proposed in [12–14,39] report
more than 90% of accuracy in separating a normal brain condition from
a damaged one.

**Passage 8:**

> ial Intelligence In Medicine 149 (2024) 102774
12
M. Gravina et al. Table 12
Performance of the EXP.3 (Task A) on the MRI dataset. Ba and Re denote the BasicNet and ResNet architectures. Data Net Mod. ACC Precision Recall AUC
C M S C M S
MRI
Ba U 70.86 ±.02 86.96 ±.04 37.42 ±.07 34.31 ±.09 80.67 ±.04 43.80 ±.02 44.30 ±.16 76.53 ±.04
IF 72.60 ±.03 87.96 ±.02 41.37 ±.04 34.71 ±.16 82.07±.06 44.57±.09 53.16 ±.13 79.39±.04
Re U 70.23 ±.03 91.81 ±.03 41.34 ±.05 32.82 ±.01 73.87 ±.03 62.02 ±.03 54.43 ±.07 78.53 ±.03
IF 75.67±.01 91.75 ±.03 49.55 ±.03 38.66 ±.04 80.54±.010 63.57±.04 58.23 ±.05 78.78±.02
Re [11] U 61.36 ±.04 84.47 ±.06 27.12 ±.06 16.33 ±.07 72.14 ±.10 32.17 ±.19 30.38 ±.02 71.11 ±.03
IF 48.38 ±.05 86.84 ±.04 26.06 ±.02 15.17 ±.06 46.33 ±.08 59.69 ±.17 34.18 ±.22 68.66 ±.06
Table 13
Performance of the EXP.3 (Task A) on the PET dataset.

**Passage 9:**

> ://github.com/priamus-lab/Multi-Input---Multi-Output-3D-CNN-
for-Dementia-Severity-Assessment-with-Incomplete-Multimodal-Data/
Artificial Intelligence In Medicine 149 (2024) 102774
9
M. Gravina et al. Table 4
Performance of the EXP.1 (Task B1) the MRI dataset. Ba and Re denote the BasicNet and ResNet architectures. Data Net Mod. ACC Precision Recall AUC
C NC C NC
MRI
Ba U 76.96 ±.02 89.54 ±.01 55.00 ±.01 77.65 ±.02 75.07 ±.01 79.80 ±.01
IF 78.78 ±.05 89.35 ±.03 58.08 ±.06 80.67 ±.08 73.59 ±.09 80.67 ±.03
Re U 80.36 ±.01 91.96 ±.01 59.78 ±.02 80.24 ±.02 80.71 ±.03 81.71 ±.02
IF 84.80±.01 93.28 ±.01 67.47 ±.05 85.42 ±.02 83.09 ±.03 84.30 ±.02
Table 5
Performance of the EXP.1 (Task B1) the PET dataset. Ba and Re denote the BasicNet and ResNet architectures. Data Net Mod.

**Passage 10:**

> mages of the same scale
across different acquisitions. 4.2. Dementia severity assessment
In clinical trials, T1-w MRI and PET are the standard diagnostic
tools used to assess the severity of dementia. They provide different
information since the former focuses on the volumetric and structural
characteristics of the brain, while the latter reveals its metabolic func-
tions. MDL allows the fusion of complementary information coming
from heterogeneous sources with the aim of providing a richer data
representation than the unimodal approach. Among all deep neural networks, CNNs are widely used in biomed-
ical image processing [ 8,46] with surprising results. A typical CNN
consists of stacked relatively complex layers [47], with each of them
having a convolutional stage, a non-linearity function (i.e ReLU), and
a pooling operation.

**Passage 11:**

> nsidering PET acquisitions have
been proposed, presenting the same heterogeneity as seen in work
focusing on MRI. Some papers focus on the ADNI dataset [30], ex-
ploiting fluorodeoxyglucose (FDG) PET. In particular, the solutions
presented in [35,36] use state-of-the-art CNNs (AlexNet [31] and In-
ceptionV3 [33]), while the methodology proposed in [37] relies on a
3D CNN. Only one paper [38] uses the OASIS-3 dataset [15], proposing
a 3D CNN trained from scratch, focussing on amyloid imaging. In the recent years, implemented solutions exploited joint learning
for dementia assessment, without considering the late and early fusion. The authors of [11] proposed a methodology that combines T1-w MRI,
Diffusion Tensor Imaging (DTI-MRI) and 2D ResNet18 [32], represent-
ing the first article that focuses on a multimodal approach with the
OASIS-3 dataset [15].

**Passage 12:**

> B) classification, also detailing the results on the
Tasks B1 (C/NC classification) and B2 (M/S classification). Moreover,
we test the EF, LF and IF techniques with the two CNNs, BasicNet and
ResNet. To assess the effectiveness of the proposed methodology, we com-
pare the result of the IF, EF and LF with the U approach, consid-
ering also a proposal from the literature focusing on the OASIS-3
dataset [15]. The U approach is used as a baseline, evaluating its performance on
the MRI and PET datasets. In particular, we train the BasicNet and the
ResNet considering the MRI and PET volumes separately, obtaining the
U MRI-NET and the U PET-NET. We then select the solution described in [11] as it represents,
to the best of our knowledge, the first article that focuses on MDL
considering the OASIS-3 dataset [15].

**Passage 13:**

> ence). IEEE;
2021, p. 494–9.
[43] McNamee RL, Yee S-H, Price JC, Klunk WE, Rosario B, Weissfeld L, et al. Consideration of optimal time window for pittsburgh compound B PET summed
uptake measurements. J Nuclear Med 2009;50(3):348–55.
[44] Mattes D, Haynor DR, Vesselle H, Lewellyn W. Nonrigid multimodality image
registration. Medical imaging 2001: image processing, vol. 4322, Spie; 2001, p. 1609–20. Artificial Intelligence In Medicine 149 (2024) 102774
17
M. Gravina et al.
[45] Rahunathan S, Stredney D, Schmalbrock P, Clymer BD. Image registration using
rigid registration and maximization of mutual information. In: 13th Annu. med.
meets virtual reality conf. 2005.
[46] Suzuki K. Overview of deep learning in medical imaging. Radiol Phys Technol
2017;10(3):257–73.
[47] Bengio Y, Goodfellow I, Courville A. Deep learning, vol.

**Passage 14:**

> ion techniques which include translation,
rotation, and scaling [ 49]. Straightforwardly, we avoid completely
overturning the position of the brain areas when setting up the aug-
mentation operations. Since the extracted bounding box is strongly
influenced by the 𝑦 axis, volumes are translated within [−10, 10] pixels
in 𝑥 and 𝑧 dimensions, and within [−5, 5] in the remaining one. The
rotation angle is selected within [−10◦, 10◦] for the 𝑦 axis and within
[−5◦, 5◦] for the remaining ones, to reproduce natural head positions. The scaling factor, applied in each dimension, is chosen within[0.9, 1.1],
to simulate different brain sizes by introducing moderate modifications. During the training, we also implemented a strategy to handle data
imbalance, ensuring the creation of balanced batches in the various
iterations.

**Passage 15:**

> Artificial Intelligence In Medicine 149 (2024) 102774
Available online 24 January 2024
0933-3657/© 2024 The Author(s). Published by Elsevier B.V. This is an open access article under the CC BY-NC license ( http://creativecommons.org/licenses/by-
nc/4.0/).

**Passage 16:**

> lization. The result is a set of
volumes of size 256 × 256 × 256 with isotropic dimension. A PET scan consists in the acquisition of 3D volumes after the
injection of the tracer, resulting in 4D data. In OASIS dataset subjects
underwent a 60 min dynamic PET scan in 3D mode (24 × 5 s frames;
9 × 20 s frames; 10 × 1 min frames; 9 × 5 min frames) generating a
maximum of 52 3D volumes acquired over time. Since we are inter-
ested in C-PiB retention, only volumes acquired after tracer absorption
are considered. Indeed, the acquisitions obtained 40 min after tracer
injection [43] are averaged to create a static PET scan, which is then
rigidly registered to the MRI volume acquired during the dynamic PET
scan session using mutual information as a similarity metric [ 44,45]. The result is a PET volume of size 256 × 256 × 256 with isotropic
dimension.

**Passage 17:**

> -point scale in which 0
means a cognitive normal condition, 0.5 indicates a questionable im-
pairment, whilst the values 1, 2, and 3 correspond to a mild, moderate,
and severe impairment respectively. In clinical trials, the Magnetic Resonance Imaging (MRI) is the
standard diagnostic tool [4,5] due to the fact that the acquired images
have a strong relationship with the topology of the brain showing
the alteration of the morphology. In particular, the T1-weighted (T1-
w) MRI provides information about the brain structure, making it
possible to evaluate its volumetric characteristics and atrophy. Positron
Emission Tomography (PET) is another imaging technique that consists
of the injection of a tracer capable of revealing the metabolic functions
of the tissue under analysis.

**Passage 18:**

> rks (DPNs) were used to extract features from
the two image modalities. The solutions proposed in [12–14,39] report
more than 90% of accuracy in separating a normal brain condition from
a damaged one. As aforementioned in Section 1, when working with a multimodal
environment, it is not easy to have images of all the involved modal-
ities, that, in turn, will result in the need to manage incomplete ac-
quisitions. Authors in [12,13] used only a paired dataset, reducing
the number of images available, while the solution proposed in [11]
replaced the missing modality with black images. In [14] the authors
used linear interpolation to fill in the missing modalities. However, this
Artificial Intelligence In Medicine 149 (2024) 102774
3
M. Gravina et al.
process makes the different acquisitions dependent on each other, espe-
cially in the case of longitudinal studies.

**Passage 19:**

> images coming from all the different sources and collected
at the same time or in a specific range. In a real scenario, patients may
have incomplete acquisitions , in which some modalities are missed. In
the literature, some implemented methodologies discard the incomplete
instances, considering only the paired acquisitions and limiting the
amount of data to be considered [11–13]. On the other hand, few
work propose to fill the missing modalities with black images [11] or
interpolation operations [14]. In this paper, we conduct a systematic analysis of early, late and
joint approaches in fusion for dementia severity assessment on the
publicly available OASIS-3 dataset [15], which is the latest release in
the Open Access Series of Imaging Studies (OASIS) and includes two
different image modalities, the T1-w MRI and the C-PiB PET.

**Passage 20:**

> ificial Intelligence In Medicine 149 (2024) 102774
4
M. Gravina et al. Table 1
The progression of patients in the three classes, cognitive normal (C), very mild
dementia (M), mild/severe dementia (S). Start with End with Total
C M S
C 340 67 3 410
M 145 10 155
S 63 63
Total 340 212 76 628
Table 2
Information about generated datasets in terms of number of volumes for each class,
cognitive normal (C), very mild dementia (M), mild/severe dementia (S). Dataset Classes TOTAL
C M S
MRI 926 258 79 1263
PET 627 75 16 711
Paired 556 58 14 628
Fig. 1. Disease progression for patient OAS31045. 4. Methodology
This work aims to develop a decision system supporting demen-
tia severity assessment, and exploiting information coming from two
different image modalities, namely the T1-w MRI and the C-PiB PET.

**Passage 21:**

> To implement a solution completely based on 3D CNN, extracting
features from the whole 3D brain volume.
• To propose a training strategy capable of handling a highly
imbalanced and incomplete dataset. Notably, in the case of the
intermediate approach, we implement a Multi Input–Multi Output
3D CNN architecture that adapts its training iterations according
to the input characteristics. 3. Population
In this work, we consider the OASIS-3 dataset [15], consisting in a
compilation of MRI, PET imaging, and clinical data for 1098 patients. The study collects 605 cognitively normal patients and 493 individuals
at various stages of cognitive decline. All the MRI, PET, and clinical
data acquisition sessions report information about when they are ac-
quired expressed as the number of days since the subject’s entry date
into the study.

**Passage 22:**

> et both
during the training and inference step. Despite the promising results, we argue that the limitations of our
work are the limited size of the dataset and the quality of acquired
medical images. Indeed, as mentioned in Section 3 and in the Supple-
mentary Material , we implemented a pre-processing step that excluded
several patients reducing the number of subjects from 1098 to 628. In
addition, the OASIS-3 dataset [15], consists of a collection of different
studies over the course of 15 years, including MRI and PET acquired
with different scanners and protocols, that may limit the generalization
ability of our models. To address this, we evaluate the difference in the
performance among the various machines, detailing the results for each
MRI and PET scanner.

**Passage 23:**

> cquisition, Project administration, Resources, Supervision,
Artificial Intelligence In Medicine 149 (2024) 102774
16
M. Gravina et al. Writing – original draft, Writing – review & editing, Validation. Carlo
Sansone: Funding acquisition, Project administration, Resources, Su-
pervision, Validation, Writing – original draft, Writing – review &
editing. Paolo Soda: Funding acquisition, Project administration, Re-
sources, Supervision, Writing – original draft, Writing – review &
editing, Validation. Declaration of competing interest
The authors declare that they have no known competing finan-
cial interests or personal relationships that could have appeared to
influence the work reported in this paper.

**Passage 24:**

> e
U MRI-NET and the U PET-NET. We then select the solution described in [11] as it represents,
to the best of our knowledge, the first article that focuses on MDL
considering the OASIS-3 dataset [15]. Since the authors use T1-w
and DTI MRI, we carefully implemented the proposed methodology
according to the information provided in [11], exploiting T1-w MRI and
C-PiB PET for the classification of the three classes (Task A). Indeed,
Massalimova et al. [11] explored the fine-tuning of the state-of-the-art
RestNet18 [32] in the U approach, proposing in the IF a multi-input
2D CNN that leverages the network trained in the solution with a
single modality. The input consists of a 3-channel image obtained
concatenating the median slices of the sagittal, axial, and coronal views
from each 3D scan. In the IF approach, the authors replace the missing
modalities with black images.

</details>

---

## Multi-scale 3D-CNN for Alzheimer-s Disease Classification
_File: `Multi-scale 3D-CNN for Alzheimer-s Disease Classification.pdf`_

1. **Was diffusion MRI (DTI, dMRI, DWI, or similar) used in this paper?**  
   Yes. The paper explicitly mentions **DTI (Diffusion Tensor Imaging)** and uses metrics like **FA (Fractional Anisotropy)** and **MD (Mean Diffusivity)**, which are standard in diffusion MRI.

---

2. **What processing steps were applied to the diffusion images?**  
   The steps are explicitly described in the order below:  
   - Convert DICOM files to NIFTI format using **MRIcron**.  
   - Extract B0 images (gradient value = 0) as a reference.  
   - Correct for eddy currents and head motion.  
   - Remove cranial parts and set intensity threshold to **0.3** to obtain the brain mask.  
   - Calculate **FA** and **MD** via least squares fitting of the diffusion tensor.  
   - Align FA images to **FMRIB58 FA standard template** and **MNI152 standard space** (nonlinear alignment).  
   - Extract white matter skeleton and threshold FA to **0.2** to remove gray matter and CSF.  
   - Project each subject’s white matter fiber map onto the mean FA skeleton.  
   - Statistically compare FA images at the voxel level to extract significant voxels (TBSS-based features).  
   - Similarly process **MD images** to extract features.  
   - Extract radiomics features from FA and MD images using **pyradiomics** (including shape, intensity, and texture features).  

---

3. **What software or tools are explicitly named for processing?**  
   - **MRIcron** (DICOM to NIFTI conversion).  
   - **FSL** (FMRIB Software Library for preprocessing).  
   - **pyradiomics** (radiomics feature extraction).  
   - **TBSS** (Tract-Based Spatial Statistics method).  

---

4. **What acquisition or processing parameters are explicitly reported?**  
   - Intensity threshold for brain masking: **0.3**.  
   - FA skeleton threshold: **0.2**.  
   - Alignment to **FMRIB58 FA standard template** and **MNI152 standard space**.  
   - No explicit mention of **b-values**, **number of diffusion directions**, or **voxel size**.  

---

5. **Copy the exact sentences from the excerpts that describe the processing.**  
   - "The DTI images are preprocessed by using Functional Magnetic Resonance Imaging of the Brain’s (FMRIB) Software Library (FSL)..."  
   - "The FA images are statistically compared at the voxel level and the significant voxels are extracted as the TBSS-based features."  
   - "The radiomics features are extracted with the pyradiomics package from FA and MD images."  
   - "The diffusion tensor is related to the eigenvalues λ1, λ2, λ3."  
   - "The FA images are aligned to the MNI152 standard space."  

---

6. **Is the processing description complete, or does it appear incomplete/missing?**  
   The processing description is **complete** based on the excerpts provided. All steps explicitly mentioned are detailed, and no missing steps are indicated. However, parameters like **b-values**, **number of diffusion directions**, or **voxel size** are **not reported** in the text.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> classifier. A. Data preprocessing
The DTI images are preprocessed by using Functional Mag-
netic Resonance Imaging of the Brain’s (FMRIB) Software
Library (FSL) developed by the Oxford’s FMRIB Center. The
specific steps include: (a) The Digital Imaging and Commu-
nications in Medicine (DICOM) format files are converted
to Neuroimaging Informatics Technology Initiative (NIFTI)
format images using MRIcron software. (b) The B0 images
with a magnetic field gradient value of 0 are extracted as a
reference. (c) Correcte the bias generated by eddy currents
and head motion. (d) Remove the cranial part and set the
intensity threshold to 0.3 to obtain the complete brain mask
[15, 16]. After that, the FA and MD are calculated by fitting the
diffusion tensor using the least squares method. The diffusion
tensor is related to the eigenvalues λ1, λ2, λ3.

**Passage 2:**

> FA images of all subjects to
FMRIB58 FA standard template. The target image is aligned
to the MNI152 standard space. Second, the white matter
skeleton is extracted to compute the average FA skeleton. The
FA skeleton with a threshold of 0.2 is extracted to remove the
gray matter and cerebrospinal fluid fractions which is used to
create the mean FA skeleton of the white matter fiber bundles
[18]. Third, the white matter fiber map of each subject is
projected onto the mean FA skeleton map. The FA images
are statistically compared at the voxel level and the significant
voxels are extracted as the TBSS-based features. Finally, the
MD images are similarly processed to extract the features. 2) Radiomics-based feature extraction: The radiomics fea-
tures are extracted with the pyradiomics package from FA and
MD images.

**Passage 3:**

> from IEEE Xplore. Restrictions apply. Fig. 1. The framework of multi-scale 3D-CNN method for AD classification. II. M ETHODS
The proposed Alzheimer’s disease classification method is
shown in Fig. 1. It consists of three parts: image preprocessing,
feature extraction and disease classification. Specifically, the
fractional anisotropy (FA) and mean diffusivity (MD) are com-
puted from DTI images by using tensor fitting method. Then
three-scale features including voxel-based features, 3D-CNN-
based features, and radiomics-based features are extracted and
linearly fused. Finally, LASSO algorithm is used for feature
selection to reduce the dimensionality of features and SVM is
ultilised as the classifier. A. Data preprocessing
The DTI images are preprocessed by using Functional Mag-
netic Resonance Imaging of the Brain’s (FMRIB) Software
Library (FSL) developed by the Oxford’s FMRIB Center.

**Passage 4:**

> s within a voxel which can be
computed by:
M D = (λ1 + λ2 + λ3)
3 (2)
where the eigenvalue λ1 is the longitudinal diffusivity, which
indicates the diffusion rate along the fiber direction. The
Fig. 2. The flowchart of the TBSS method.
eigenvalues λ2, λ3 indicate the diffusion magnitude in the
transverse to the axon bundle. B. Multi-scale Feature Extraction
1) TBSS-based feature extraction: The TBSS method com-
pute the brain structural differences and determine the spatial
location distribution associated with disease or function. The
flowchart of TBSS is shown in Fig. 2. First, the nonlinear
alignment is applied to align FA images of all subjects to
FMRIB58 FA standard template. The target image is aligned
to the MNI152 standard space. Second, the white matter
skeleton is extracted to compute the average FA skeleton.

**Passage 5:**

> uthorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:43:40 UTC from IEEE Xplore. Restrictions apply. TABLE I
CLASSIFICATION RESULTS OF DIFFERENT METHODS ON ADNI. Methods FA MD FA+MD
ACC SEN SPE AUC ACC SEN SPE AUC ACC SEN SPE AUC
TBSS 77.50% 72.50% 82.20% 83.90% 81.80% 78.90% 86.00% 87.80% 85.30% 78.90% 90.30% 88.10%
Radiomics 67.90% 68.10% 70.10% 69.90% 68.20% 67.60% 70.30% 69.70% 66.70% 67.50% 70.10% 72.20%
3D-CNN 73.20% 76.20% 72.90% 80.10% 77.80% 81.20% 75.60% 81.50% 79.70% 86.30% 79.70% 86.90%
Fusion 75.9% 76.40% 77.80% 79.80% 79.80% 81.40% 82.70% 82.50% 81.30% 88.90% 84.50% 89.50%
Ours 79.90% 76.90% 82.40% 85.20% 85.20% 82.50% 87.60% 85.80% 88.90% 89.40% 89.70% 91.70%
Fig. 4.

**Passage 6:**

> ssification accuracy in Alzheimer’s
disease using higher-order singular value decomposi-
tion,” Frontiers in neuroscience, vol. 9, p. 257, 2015. Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:43:40 UTC from IEEE Xplore. Restrictions apply.

**Passage 7:**

> inally, the
MD images are similarly processed to extract the features. 2) Radiomics-based feature extraction: The radiomics fea-
tures are extracted with the pyradiomics package from FA and
MD images. Especially, the features include shape, intensity,
and texture: First Order features, Shape features (3D), Shape
features (2D), Gray Level Co-occurrence Matrix (GLCM) fea-
tures, Gray Level Size Zone Matrix (GLSZM) features, Gray
Level Run Length Matrix (GLRLM) features, Neighbouring
Gray Tone Difference Matrix (NGTDM) features and Gray
Level Dependence Matrix (GLDM) features. 3) Residual 3D convolutional neural network-based feature
extration: The two-dimensional convolutional neural network
has been widely used in the medical image processing. How-
ever, the FA and MD images are three dimension.

**Passage 8:**

> onal neural network-based feature
extration: The two-dimensional convolutional neural network
has been widely used in the medical image processing. How-
ever, the FA and MD images are three dimension. Therefore,
we focus on the 3D-CNN model to extract the brain features
which may dig more information compared with the 2D-CNN
with scanned slices. The residual blocks are combined with the
3D-CNN in order to obtain deep and discriminative features. Specifically, the FA and MD images are aligned to a
standard space after diffusion tensor fitting. The combination
of linear and nonlinear alignment algorithm is used to align
all data to the FMRIB58 FA 1mm generic template. Then the
3D convolution is computed by:
vx,y,z
lm =
N1−1X
n1=0
N2−1X
n2=0
N3−1X
n3=0
kn1,n2,n3
lmp ·v(x+n1)(y+n2)(z+n3)
(l−1)p (3)
Authorized licensed use limited to: OAKLAND UNIVERSITY.

**Passage 9:**

> ion rate for each individual are extracted using
Tract-Based Spatial Statistics (TBSS) method from the skeleton. Second, the texture and intensity features are extracted by
utilizing radiomics method. Third, an improved 3D convolutional
neural network is proposed to extract depth features from the
fractional anisotropy (FA) and mean diffusivity (MD) images. Finally, the multi-scale features are linearly fused and select with
LASSO algorithm. The support vector machine is utilized for
five-fold cross-validation. The experimental results on the ADNI
dataset with 185 DTI images containing AD and normal controls
(NC) subjects show that the proposed method achieves better
classification performance compared with existing methods for
the AD assist diagnosis task. Index Terms —DTI, TBSS, radiomics, convolutional neural
network, multi-scale features
I.

**Passage 10:**

> xel-based methods and fiber tracer map-based methods. Maggipinto et al . [11] proposed a voxel-based approach for
AD classification by picking different voxel quantities of
fractional anisotropy (FA). Lella et al . [12] proposed the
support vector machine (SVM) based AD classifier with voxel
features of FA, mean diffusivity (MD), longitudinal diffusivity
(LD) and radial diffusivity (RD). Nir et al . [13] proposed to
cluster using the region of interest atlas and calculate FA and
MD along all maximum density paths for AD classification. Marzban et al . [4] proposed a bounding boxing to extract
out 2D images including the hippocampus and the entorhinal
cortex with 2D-CNN classifier. L.Kang et al [14] proposed
the multi-modality AD diagnosis method which idicated that
DTI image could act as an important biomarker.

**Passage 11:**

> vol. 12, p. 206, 2020.
[15] H. Takao, N. Hayashi, and K. Ohtomo, “Sex dimorphism
in the white matter: fractional anisotropy and brain size,”
Journal of Magnetic Resonance Imaging , vol. 39, no. 4,
pp. 917–923, 2014.
[16] T. M. Nir, N. Jahanshad, J. E. Villalon-Reina, A. W. Toga,
C. R. Jack, M. W. Weiner, P. M. Thompson, A. D. N. I.
(ADNI et al. , “Effectiveness of regional DTI measures
in distinguishing Alzheimer’s disease, MCI, and normal
aging,” NeuroImage: clinical, vol. 3, pp. 180–195, 2013.
[17] J. Qiao, X. Zhao, S. Wang, A. Li, Z. Wang, C. Cao, and
Q. Wang, “Functional and structural brain alterations in
encephalitis with LGI1 antibodies,” Frontiers in Neuro-
science, vol. 14, p. 304, 2020.
[18] C. Luo, M. Li, R. Qin, H. Chen, L. Huang, D. Yang,
Q. Ye, R. Liu, Y . Xu, H.

**Passage 12:**

> Multi-scale 3D-CNN for Alzheimer’s Disease
Classification
Hang Yan
School of Physics and Electronics
Shandong Normal University
Jinan, China
Kunlun Fang
School of Physics and Electronics
Shandong Normal University
Jinan, China
Hao Shang
School of Physics and Electronics
Shandong Normal University
Jinan, China
Hongjia Liu
School of Physics and Electronics
Shandong Normal University
Jinan, China
Jiande Sun*
School of Information Science and Engineering
Shandong Normal University
Jinan, China
*jiandesun@hotmail.com
Jianping Qiao*
School of Physics and Electronics
Shandong Normal University
Jinan, China
*jpqiao@sdu.edu.cn
Abstract—The diffusion tensor imaging (DTI) based
Alzheimer’s disease (AD) classification consists of the region
of interest-based methods, voxel-based methods, and fiber
tracer map-based methods. However, most of the studies utilize
partial information of the DTI data.

**Passage 13:**

> arameter to balance the complexity of the
model. After that, the SVM model with the radial basis kernel
function is used to find the structurally optimal solution and
classify the brain diseases. III. R ESULTS
We conduct experiments on the open access Alzheimer’s
Disease Neuroimaging Initiative (ADNI) database in order to
demonstrate the effectiveness of the proposed method. There
are two groups of subjects including 85 AD patients and
100 NC controls. Only the baseline scans of the subjects are
included in order to avoid the influence of treatments. Subjects
with poor scan quality, partially missing images and incorrect
information are also excluded. All models and algorithms are run on CPU and GPU
platform using Python. The CPU is Intel (R) Xeon (R) W-2102
@2.90 GHz. The GPU is NVIDIA GeForce GTX 1080Ti. True positive (TP) means the number of patients correctly
determined.

**Passage 14:**

> tructural brain alterations in
encephalitis with LGI1 antibodies,” Frontiers in Neuro-
science, vol. 14, p. 304, 2020.
[18] C. Luo, M. Li, R. Qin, H. Chen, L. Huang, D. Yang,
Q. Ye, R. Liu, Y . Xu, H. Zhao et al. , “Long Longi-
tudinal Tract Lesion Contributes to the Progression of
Alzheimer’s Disease,”Frontiers in Neurology, vol. 11, p. 1064, 2020.
[19] J. Li, H. Zhang, W. Wan, and J. Sun, “Two-class 3D-
CNN classifiers combination for video copy detection,”
Multimedia Tools and Applications , vol. 79, no. 7-8, pp. 4749–4761, 2020.
[20] L. Zhan, Y . Liu, Y . Wang, J. Zhou, N. Jahanshad, J. Ye,
P. M. Thompson, and A. D. N. I. (ADNI), “Boosting
brain connectome classification accuracy in Alzheimer’s
disease using higher-order singular value decomposi-
tion,” Frontiers in neuroscience, vol. 9, p. 257, 2015. Authorized licensed use limited to: OAKLAND UNIVERSITY.

**Passage 15:**

> els
from FA and MD. Then image texture and intensity were
extracted with radiomics method. After that, the 3D convo-
lutional neural network with residual blocks was proposed
to extract deep features. Finally, the multiscale features were
linearly fused and selected by the Least Absolute Shrinkage
and Selection Operator (LASSO) algorithm. The SVM was
used to perform the classification task. 2023 IEEE International Symposium on Circuits and Systems (ISCAS) | 978-1-6654-5109-3/23/$31.00 ©2023 IEEE | DOI: 10.1109/ISCAS46773.2023.10181771
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:43:40 UTC from IEEE Xplore. Restrictions apply. Fig. 1. The framework of multi-scale 3D-CNN method for AD classification. II. M ETHODS
The proposed Alzheimer’s disease classification method is
shown in Fig. 1.

**Passage 16:**

> eveste, J. P ´erez, and A. Besga, “Computer aided
diagnosis system for Alzheimer disease using brain dif-
fusion tensor imaging features selected by Pearson’s
correlation,” Neuroscience letters , vol. 502, no. 3, pp. 225–229, 2011.
[7] M. Wang, H. Wang, and H. Zheng, “A Mini Review of
Node Centrality Metrics in Biological Networks,” Inter-
national Journal of Network Dynamics and Intelligence ,
vol. 1, no. 1, pp. 99–110, 2022.
[8] G. Zhao, Y . Li, and Q. Xu, “From Emotion AI to Cog-
nitive AI,” International Journal of Network Dynamics
and Intelligence, vol. 1, no. 1, pp. 65–72, 2022.
[9] J. Qiao, R. Wang, H. Liu, G. Xu, and Z. Wang, “Brain
disorder prediction with dynamic multivariate spatio-
temporal features: Application to Alzheimer’s disease
and autism spectrum disorder,” Frontiers in Aging Neu-
roscience, p. 973, 2022.
[10] J. Qiao, Y . Lv, C. Cao, Z. Wang, and A.

**Passage 17:**

> he complete brain mask
[15, 16]. After that, the FA and MD are calculated by fitting the
diffusion tensor using the least squares method. The diffusion
tensor is related to the eigenvalues λ1, λ2, λ3. The magnitude of the eigenvalues indicate the degree of
dispersion of water molecules in each direction [17]. The
fractional anisotropy (FA) reflect the extent of water molecular
displacement in space, which can be computed by:
F A =
r
3
 
λ1 − ¯λ
2
+
 
λ2 − ¯λ
2
+
 
λ3 − ¯λ
2
p
2 (λ2
1 + λ2
2 + λ2
3)
(1)
The MD describ the average diffusion coefficient in the
direction of water molecules within a voxel which can be
computed by:
M D = (λ1 + λ2 + λ3)
3 (2)
where the eigenvalue λ1 is the longitudinal diffusivity, which
indicates the diffusion rate along the fiber direction. The
Fig. 2.

**Passage 18:**

> . Anglani, and F. Vitu-
lano, “An ensemble learning approach based on diffusion
tensor imaging measures for Alzheimer’s disease classi-
fication,” Electronics, vol. 10, no. 3, p. 249, 2021.
[13] T. M. Nir, J. E. Villalon-Reina, G. Prasad, N. Jahan-
shad, S. H. Joshi, A. W. Toga, M. A. Bernstein, C. R. Jack Jr, M. W. Weiner, P. M. Thompsonet al., “Diffusion
weighted imaging-based maximum density path analysis
and classification of Alzheimer’s disease,” Neurobiology
of aging, vol. 36, pp. S132–S140, 2015.
[14] L. Kang, J. Jiang, J. Huang, and T. Zhang, “Identifying
early mild cognitive impairment by multi-modality MRI-
based deep learning,” Frontiers in aging neuroscience ,
vol. 12, p. 206, 2020.
[15] H. Takao, N. Hayashi, and K. Ohtomo, “Sex dimorphism
in the white matter: fractional anisotropy and brain size,”
Journal of Magnetic Resonance Imaging , vol. 39, no. 4,
pp.

**Passage 19:**

> irment by machine learn-
ing with hippocampus-related white matter network,”
Frontiers in Aging Neuroscience , vol. 14, 2022.
[4] E. N. Marzban, A. M. Eldeib, I. A. Yassine, Y . M. Kadah,
and A. D. N. Initiative, “Alzheimer’s disease diagnosis
from diffusion tensor images using convolutional neural
networks,” PloS one, vol. 15, no. 3, p. e0230409, 2020.
[5] A. Massalimova and H. A. Varol, “Input Agnostic Deep
Learning for Alzheimer’s Disease Classification Using
Multimodal MRI Images,” in 2021 43rd Annual Interna-
tional Conference of the IEEE Engineering in Medicine
& Biology Society (EMBC) . IEEE, 2021, pp. 2875–
2878.
[6] M. Gra ˜na, M. Termenon, A. Savio, A. Gonzalez-Pinto,
J. Echeveste, J. P ´erez, and A. Besga, “Computer aided
diagnosis system for Alzheimer disease using brain dif-
fusion tensor imaging features selected by Pearson’s
correlation,” Neuroscience letters , vol.

**Passage 20:**

> g the hippocampus and the entorhinal
cortex with 2D-CNN classifier. L.Kang et al [14] proposed
the multi-modality AD diagnosis method which idicated that
DTI image could act as an important biomarker. However,
most of the studies utilize partial information of the DTI data,
making it difficult to uncover discriminative information for
AD classification. Therefore, we proposed a 3D convolutional neural networks
with multi-scale information fusion method for the AD com-
puter aided diagnosis. Specifically, the Tract-Based Spatial
Statistics (TBSS) was used to extract the significant voxels
from FA and MD. Then image texture and intensity were
extracted with radiomics method. After that, the 3D convo-
lutional neural network with residual blocks was proposed
to extract deep features.

**Passage 21:**

> (AD) classification consists of the region
of interest-based methods, voxel-based methods, and fiber
tracer map-based methods. However, most of the studies utilize
partial information of the DTI data. It is difficult to discover
most discriminative biomarkers. To address this problem, this
paper proposes a novel AD classification method based on
3D convolutional neural networks (3D-CNN) with multi-scale
information fusion in order to uncover the differential features
of AD. First, the significant voxels of anisotropy score and
mean dispersion rate for each individual are extracted using
Tract-Based Spatial Statistics (TBSS) method from the skeleton. Second, the texture and intensity features are extracted by
utilizing radiomics method.

**Passage 22:**

> ment in the sensitivity index. Furthermore, the TBSS-based
classification method has better performance than radiomics
and 3D CNN based methods, which achieves 85.3% accuracy
and 88.1% AUC value. Fig. 4 shows the the ROC curves of
different methods in which the method with multi-scale fused
features has the highest AUC values, indicating that the fused
features are most discriminative in the classification model. In addition, the classification model with the intensity and
texture features extracted by radiomics has poor performance,
indicating that the intensity and texture of FA and MD images
are not sensitive for the AD identification. Moreover, the
classification result of the method with 3D-CNN achieves
79.7% accuracy and 86.9% AUC value, which demonstrate
that the proposed 3D-CNN could effectively extract features
from patient lesion sites.

**Passage 23:**

> multivariate spatio-
temporal features: Application to Alzheimer’s disease
and autism spectrum disorder,” Frontiers in Aging Neu-
roscience, p. 973, 2022.
[10] J. Qiao, Y . Lv, C. Cao, Z. Wang, and A. Li, “Multivariate
deep learning classification of Alzheimer’s disease based
on hierarchical partner matching independent component
analysis,” Frontiers in aging neuroscience , vol. 10, p. 417, 2018.
[11] T. Maggipinto, R. Bellotti, N. Amoroso, D. Diacono,
G. Donvito, E. Lella, A. Monaco, M. A. Scelsi, S. Tan-
garo, A. D. N. Initiative et al. , “DTI measurements
for Alzheimer’s classification,” Physics in Medicine &
Biology, vol. 62, no. 6, p. 2361, 2017.
[12] E. Lella, A. Pazienza, D. Lof `u, R. Anglani, and F. Vitu-
lano, “An ensemble learning approach based on diffusion
tensor imaging measures for Alzheimer’s disease classi-
fication,” Electronics, vol. 10, no. 3, p. 249, 2021.
[13] T. M.

**Passage 24:**

> ght performance in the
AD classification. Furthermore, the excellent performance of
the method with the multi-scale fused features indicate its
effectiveness for Alzheimer’s disease classification. V. A CKNOWLEDGEMENTS
This work is supported by the Scientific Research Leader
Studio of Jinan (Grant No. 2021GXRC081), the National
Natural Science Foundation of China (61603225) and the
Joint Project for Smart Computing of Shandong Natu-
ral Science Foundation (Grant No. ZR2020LZH015 and
ZR2022LZH012). REFERENCES
[1] W. Lee, B. Park, and K. Han, “SVM-based classifi-
cation of diffusion tensor imaging data for diagnosing
Alzheimer’s Disease and mild cognitive impairment,”
in International Conference on Intelligent Computing . Springer, 2015, pp. 489–499.
[2] W. Li, Z. Zhao, M. Liu, S. Yan, Y . An, L. Qiao,
G. Wang, Z. Qi, and J.

</details>

---

## Multicenter and Multichannel Pooling GCN for Early AD Diagnosis Based on Dual-Modality Fused Brain Network
_File: `Multicenter and Multichannel Pooling GCN for Early AD Diagnosis Based on Dual-Modality Fused Brain Network.pdf`_

1. **Was diffusion MRI (DTI, dMRI, DWI, or similar) used in this paper?**  
   Yes. The paper explicitly mentions "diffusion tensor imaging (DTI)" and "DTI data" as part of the dual-modality approach.

---

2. **What processing steps were applied to the diffusion images?**  
   - **PANDA toolbox** is used to obtain the global brain deterministic fiber bundle from DTI data.  
   - **Fractional anisotropy (FA)** is calculated as feature vectors.  
   - The **AAL template** is applied to the DTI image to segment the brain into 90 ROIs.  
   - The **average FA of links between network nodes** is defined as the connection weight in the DTI network.  

---

3. **What software or tools are explicitly named for processing?**  
   - **GRETNA** (for fMRI preprocessing).  
   - **PANDA** (for DTI processing).  

---

4. **What acquisition or processing parameters are explicitly reported?**  
   **Not reported in available text.** The excerpts do not mention b-values, number of diffusion directions, voxel size, or other acquisition/processing parameters.  

---

5. **Copy the exact sentences from the excerpts that describe the processing.**  
   - *"For DTI data, PANDA toolbox is used to get the global brain deterministic ﬁber bundle. Then, we obtain the fractional anisotropy (FA) as feature vectors and use the AAL template on the DTI image to divide the brain space into 90 ROIs. Last, the average FA of links between network nodes is deﬁned as the connection weight in the DTI network."*  
   - *"For fMRI data, the standard preprocessing procedures are performed using the GRETNA toolbox. 1) The ﬁrst ten acquired fMRI volumes are discarded, and then the remaining 170 volumes are corrected by applying mean-subtraction."*  

---

6. **Is the processing description complete, or does it appear incomplete/missing?**  
   **Incomplete.** The processing steps for DTI are described, but critical parameters such as b-values, number of diffusion directions, voxel size, or thresholds are not reported. These are standard parameters for diffusion MRI processing.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> ard preprocessing procedures are
performed using the GRETNA toolbox. 1) The ﬁrst ten
acquired fMRI volumes are discarded, and then the remaining
170 volumes are corrected by applying mean-subtraction. 2) Head movement correction, spatial normalization with
DARTEL, and smooth ﬁltering by employing the Gaussian
kernel are applied to improve data. 3) The automated anatom-
ical labelling (AAL) is used to segment brain space into
90 regions of interest (ROIs). After the above process,
we obtain the time-series of 90 ROIs for each individual. For DTI data, PANDA toolbox is used to get the global
brain deterministic ﬁber bundle. Then, we obtain the fractional
anisotropy (FA) as feature vectors and use the AAL template
on the DTI image to divide the brain space into 90 ROIs. Last,
the average FA of links between network nodes is deﬁned as
the connection weight in the DTI network.

**Passage 2:**

> of those training samples, gender and equipment
type information are considered in connection establishment. Third, a multi-channel pooling GCN is designed and it outputs
the score of each subject. A. Fused Brain Network Construction
1) Dataset : In this study, three datasets with 459 subjects
are collected, including datasets from ADNI 2, ADNI 3, and
an in-house dataset. Every collected subject in the above three
datasets includes the dual-modality data (fMRI and DTI). Generally, 163 normal control (NC), 44 SMC, 86 early MCI
(EMCI), and 166 late MCI (LMCI) are included. Demographic
details of the used subjects are shown in Table I. For fMRI data, the standard preprocessing procedures are
performed using the GRETNA toolbox. 1) The ﬁrst ten
acquired fMRI volumes are discarded, and then the remaining
170 volumes are corrected by applying mean-subtraction.

**Passage 3:**

> state func-
tional magnetic resonance imaging (fMRI) and diffusion
tensor imaging (DTI), and propose three mechanisms in
the current graph convolutional network (GCN) to improve
classiﬁer performance. First, we introduce a DTI-strength
penalty term for constructing functional connectivity net-
works. Stronger structural c onnectivity and bigger struc-
tural strength diversity between groups provide a higher
opportunity for retaining connectivity information. Second,
a multi-center attention graph with each node representing
a subject is proposed to consider the inﬂuence of data
source, gender, acquisition equipment, and disease status
of those training samples in GCN. The attention mechanism
captures their different impacts on edge weights. Third,
Manuscript received 25 May 2022; accepted 26 June 2022. Date of
publication 29 June 2022; date of current version 2 February 2023.

**Passage 4:**

> ure vectors and use the AAL template
on the DTI image to divide the brain space into 90 ROIs. Last,
the average FA of links between network nodes is deﬁned as
the connection weight in the DTI network. After the above
process, we get a 90 × 90 DTI connectivity network for each
individual. 2) Fused Brain Connectivity Network : We use DTI struc-
tural information to restrict the construction of functional
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply. SONG et al.: MUL TICENTER AND MUL TICHANNEL POOLING GCN FOR EARL Y AD DIAGNOSIS 357
Fig. 2. Proposed framework for disease diagnosis. (a) Fused brain connectivity network construction. For each subject, its DTI structural network and
the strength diversity between subjec t groups construct the penalty term C. (b) Multi-center attention graph.

**Passage 5:**

> Function , vol. 213, no. 6,
pp. 525–533, Oct. 2009.
[20] C. J. Honey, J.-P. Thivierge, and O. Sporns, “Can structure predict
function in the human brain?” NeuroImage, vol. 52, no. 3, pp. 766–776,
Sep. 2010.
[21] Z. Wang et al. , “Distribution-guided netwo rk thresholding for func-
tional connectivity analysis in fMRI-based brain disorder identiﬁcation,”
IEEE J. Biomed. Health Informat. , vol. 26, no. 4, pp. 1602–1613,
Apr. 2022.
[22] H. Guan, E. Yang, P. T. Yap, D. Shen, and M. Liu, “Attention-guided
deep domain adaptation for brain dementia identiﬁcation with multi-
site neuroimaging data,” in Proc. Int. Conf. Med. Image Comput. Comput.-Assist. Intervent. (MICCAI) , Lima, Peru, 2020, vol. 12444,
pp. 31–40.
[23] H. Guan, Y . Liu, E. Yang, P.-T. Yap, D. Shen, and M. Liu, “Multi-
site MRI harmonization via attention-guided deep domain adaptation
for brain disorder identiﬁcation,” Med.

**Passage 6:**

> Y AD DIAGNOSIS 367
[35] Y . Zhang, H. Zhang, E. Adeli, X. Chen, M. Liu, and D. Shen, “Multiview
feature learning with multiatlas-based functional connectivity networks
for MCI diagnosis,” IEEE Trans. Cybern. , early access, Dec. 11, 2020,
doi: 10.1109/TCYB.2020.3016953.
[36] M. Wang, C. Lian, D. Yao, D. Zhang, M. Liu, and D. Shen, “Spatial-
temporal dependency modeling and network hub detection for functional
MRI analysis via convolutional-recurrent network,”IEEE Trans. Biomed. Eng., vol. 67, no. 8, pp. 2241–2252, Aug. 2020.
[37] Y . Li, J. Liu, Y . Jiang, Y . Liu, and B. Lei, “Virtual adversarial training-
based deep feature aggregation network from dynamic effective connec-
tivity for MCI identiﬁcation,” IEEE Trans. Med. Imag. , vol. 41, no. 1,
pp. 237–251, Jan. 2022.
[38] J. Jiang, Y . Wei, Y . Feng, J. Cao, and Y . Gao, “Dynamic hypergraph
neural networks,” in Proc. 28th Int.

**Passage 7:**

> 41:57 UTC from IEEE Xplore. Restrictions apply. 362 IEEE TRANSACTIONS ON MEDICAL IMAGING, VOL. 42, NO. 2, FEBRUARY 2023
T ABLE IV
ALGORITHM COMP ARISON WITH RELA TED WORKS
ADNI 2, ADNI 3 and in-house. Compared to the current GCNs
that set the impacts of non-image information as constants to
amplify edge weights, we adopt an attention mechanism to
combine non-image information. The impacts of the above
information on edge weights are learned by network training. Compared to other works that mainly study the classiﬁcation
task of MCI vs. NC, we study more tasks. Speciﬁcally, NC
v s .S M C ,N Cv s .E M C I ,N Cv s .L M C I ,S M Cv s .E M C I ,
SMC vs. LMCI, and EMCI vs. LMCI are included. Besides,
compared to the limited samples in related works (ranging
from 59 to 370), our work has more samples (457). Our earlier work [12] concatenated fMRI functional features
and DTI structural features.

**Passage 8:**

> , X. Fei, and D. Shen, “Weighted
graph regularized sparse brain net work construction for MCI identiﬁca-
tion,” Pattern Recognit., vol. 90, pp. 220–231, Jun. 2019.
[11] Y . Li, J. Liu, Z. Tang, and B. Lei, “Deep spatial-temporal feature fusion
from adaptive dynamic functional conn ectivity for MCI identiﬁcation,”
IEEE Trans. Med. Imag. , vol. 39, no. 9, pp. 2818–2830, Sep. 2020.
[12] B. Lei et al. , “Self-calibrated brain network estimation and joint non-
convex multi-task learning for identiﬁcation of early Alzheimer’s dis-
ease,” Med. Image Anal. , vol. 61, Apr. 2020, Art. no. 101652.
[13] X. Song et al. , “Graph convolution network with similarity awareness
and adaptive calibration for disease- induced deterioration prediction,”
Med. Image Anal. , vol. 69, Apr. 2021, Art. no. 101947.
[14] J.

**Passage 9:**

> 354 IEEE TRANSACTIONS ON MEDICAL IMAGING, VOL. 42, NO. 2, FEBRUARY 2023
Multicenter and Multichannel Pooling GCN for
Early AD Diagnosis Based on Dual-Modality
Fused Brain Network
Xuegang Song , Feng Zhou , Alejandro F . Frangi , Fellow, IEEE,J i u w e nC a o, Senior Member, IEEE ,
Xiaohua Xiao, Yi Lei, Tianfu Wang , and Baiying Lei , Senior Member, IEEE
Abstract — For signiﬁcant memory concern (SMC) and
mild cognitive impairment (MCI), their classiﬁcation perfor-
mance is limited by confounding features, diverse imag-
ing protocols, and limited sample size. To address the
above limitations, we introduce a dual-modality fused
brain connectivity network co mbining resting-state func-
tional magnetic resonance imaging (fMRI) and diffusion
tensor imaging (DTI), and propose three mechanisms in
the current graph convolutional network (GCN) to improve
classiﬁer performance.

**Passage 10:**

> eat-
ments [3], [4]. Therefore, it is important to study the diagnosis
of MCI and SMC. The intelligent diagnosis attracts growing
attention and has been shown to perform well in neuroimaging
[5], [6]. However, a few limitations remain, including the
confounding neuroimaging features, multi-center data sources
and limited sample size. The popularly used neuroimagi ng modalities for brain dis-
ease intelligent diagnosis incl ude magnetic resonance imaging
(MRI) [7], [8], resting-state functional magnetic resonance
imaging (fMRI) [9]–[11], and diffusion tensor imaging (DTI)
[12], [13]. Nevertheless, most current methods utilize single-
modality imaging data for this study. Their performance is
thus limited for MCI and SMC diagnosis due to confounding
neuroimaging features [14]–[18]. Therefore, multi-modality
1558-254X © 2022 IEEE.

**Passage 11:**

> ction
strength between different groups on the same pair of brain
regions, Wang et al. [21] proposed distribution-guided network
pruning to determine thresholds for connections in functional
networks. Inspired by it, we further propose a regulatory
factor in sparse regularization term, which is constructed
by computing the distribution diversity of DTI connectivity
strength between groups. Due to the widely spread of MCI and SMC, neuroimaging
data is usually acquired from multiple medical centers, which
causes diverse imaging conditions [22], [23]. For example,
there are different acquisition protocols in the Alzheimer’s
Disease Neuroimaging Initiative (ADNI) dataset, including
ADNI 1, ADNI 2, ADNI GO, and ADNI 3, where they
also use different equipment types (e.g., SIEMENS, GE,
Philips, etc.) for data collecti on.

**Passage 12:**

> troduce the DTI-strength
penalty term to induce its sparse regularization. Here, we eval-
uate the effectiveness of our fusion method by comparing it
with the other three fusion methods (shown in Fig. 6), and the
comparison results are summarized in Table II.I n Table II,
the classiﬁcation results based on single-modality data are
also provided. All comparison experiments in this subsection
adopt our multi-center and multi- channel pooling GCN as the
classiﬁer. Based on fMRI data, the mean ACC of all six binary
classiﬁcation tasks is 83.9%, whereas the mean ACC is 82.8%
by using DTI data. Compared to DTI data, using fMRI
data for classiﬁcation shows a 1.1% ACC improvement. This
result conﬂicts with our earlier work [13], where DTI data
shows a better performance with ACC improved by 5.5%.

**Passage 13:**

> tory for Biomedical Measurements
and Ultrasound Imaging, School of Biomedical Engineering, Shenzhen
University , Shenzhen 518060, China (e-mail: sxg315@yahoo.com;
tfwang@szu.edu.cn; leiby@szu.edu.cn). Feng Zhou is with the Department of Industrial and Manufacturing,
Systems Engineering, University of Michigan, Dearborn, MI 48109 USA
(e-mail: fezhou@umich.edu). Alejandro F . Frangi is with the Centre for Computational Imaging and
Simulation T echnologies in Biomedicine (CISTIB), School of Computing,
University of Leeds, Leeds LS2 9LU, U.K. (e-mail: a.frangi@leeds.ac.uk). Jiuwen Cao is with the Artiﬁcial Intelligence Institute, Hangzhou Dianzi
University , Zhejiang 310005, China (e-mail: jwcao@hdu.edu.cn). Xiaohua Xiao and Yi Lei are with the Health Science Center, First
Afﬁliated Hospital, Shenzhen University , Shenzhen 518060, China
(e-mail: tu_xi8888@163.com; leiyisz@2011@163.com).

**Passage 14:**

> ol. 12444,
pp. 31–40.
[23] H. Guan, Y . Liu, E. Yang, P.-T. Yap, D. Shen, and M. Liu, “Multi-
site MRI harmonization via attention-guided deep domain adaptation
for brain disorder identiﬁcation,” Med. Image Anal. , vol. 71, Jul. 2021,
Art. no. 102076.
[24] S. Parisot et al., “Disease prediction using graph convolutional networks:
Application to autism spectrum disorder and Alzheimer’s disease,” Med. Image Anal. , vol. 48, pp. 117–130, Aug. 2018.
[25] Y . Zhang, L. Zhan, W. Cai, P. Thompson, and H. Huang, “Inte-
grating heterogeneous brain netwo rks for predicting brain disease
conditions,” in Proc. Int. Conf. Med. Image Comput. Comput.-
Assist. Intervent. (MICCAI) , Shenzhen, China, vol. 11767, 2019,
pp. 214–222.
[26] S. I. Ktena et al. , “Metric learning with spectral graph convolutions
on brain connectivity networks,” NeuroImage, vol. 169, pp. 431–442,
Apr. 2018.
[27] T. N. Kipf and M.

**Passage 15:**

> . Oguz, J. V . Manjón, and P. Coupé, “Multi-scale
graph-based grading for Alzhe imer’s disease prediction,” Med. Image
Anal., vol. 67, Jan. 2021, Art. no. 101850.
[8] C. Lian, M. Liu, J. Zhang, and D. Shen, “Hierarchical fully convolutional
network for joint atrophy localization and Alzheimer’s disease diagnosis
using structural MRI,” IEEE Trans. Pattern Anal. Mach. Intell. , vol. 42,
no. 4, pp. 880–893, Apr. 2020.
[9] Y. L i et al. , “Multimodal hyper-connectivity of functional networks
using functionally-weighted LASSO for MCI classiﬁcation,”Med. Image
Anal., vol. 52, pp. 80–96, Feb. 2019.
[10] R. Yu, L. Qiao, M. Chen, S.-W. Lee, X. Fei, and D. Shen, “Weighted
graph regularized sparse brain net work construction for MCI identiﬁca-
tion,” Pattern Recognit., vol. 90, pp. 220–231, Jun. 2019.
[11] Y . Li, J. Liu, Z. Tang, and B.

**Passage 16:**

> ti-center source information and disease
status information of those training samples, and capture their
different impacts on edge weights via an attention mechanism. III. M
A TERIALS AND METHODS
Fig. 2 shows an overview of the proposed framework,
which is divided into three parts. First, we construct a dual-
modality fused brain connectivity network for each subject,
where the DTI-strength penalty term is introduced in brain
connectivity network construction. Second, we construct a
multi-center attention graph to include node’s feature and con-
nection information, where multi-center source, disease status
information of those training samples, gender and equipment
type information are considered in connection establishment. Third, a multi-channel pooling GCN is designed and it outputs
the score of each subject. A.

**Passage 17:**

> een
two groups, SC ∈ R90×90 represents DTI connectivity net-
work, SCi+ and SC j− represent the DTI connection strength
matrices of subjects i and j, where subjects i and j come
from different groups. For every subject, by considering its structural connectivity
matrix SC and its corresponding strength diversity matrix SC#,
the structural connectivity penalty matrix C is deﬁned and its
element Cij is denoted as :
Cij = exp

− sc2
ij
σ1

×

1 + exp

− SC#
ij
σ2

(8)
where σ1 and σ2 are set as the mean value of the standard
variation of all subjects’ structural connectivity matrix SC and
strength diversity matrix SC#. B. Multi-Center Attention Graph
A multi-center attention gra ph is proposed in this subsec-
tion. Edge connections between each pair of nodes retain more
useful information. Edge weights are adaptively computed
Authorized licensed use limited to: OAKLAND UNIVERSITY.

**Passage 18:**

> connectivity strength
information are denoted as SC
+=[ SC1+, SC2+,..., SCT1+]
and SC− =[ SC1− , SC2− ,..., SCT2− ], respectively. Here T1
and T2 are the number of subjects in two groups (T1+T2 = T). Therefore, the strength diversity matrix SC# is deﬁned as :
SC# =|
1
T1
T1
i=1 Sci+ − 1
T2
T2
j=1 sc j−
1
T1
T1
i=1 sci+ + 1
T2
T2
j=1 sc j−
| (7)
where SC#∈R90×90 represents DTI strength diversity between
two groups, SC ∈ R90×90 represents DTI connectivity net-
work, SCi+ and SC j− represent the DTI connection strength
matrices of subjects i and j, where subjects i and j come
from different groups.

**Passage 19:**

> brain connectivity network construction. For each subject, its DTI structural network and
the strength diversity between subjec t groups construct the penalty term C. (b) Multi-center attention graph. For N subjects with each represented by
its fused connectivity network, we construct N feature vectors by selecting their discriminative features. Each feature vector is described as a nod eo n
the graph. We construct edges and compute their weights by considering the mu lti-center source, disease statu s of those training samples, gender,
equipment type information, and similarity between feature vectors. (c) Multi-channel pooling GCN.

**Passage 20:**

> osed multi-channel mechanis m increases the complexity
of the GCN classiﬁer to some extent. 3) The proposed dual-
modality fusion method ignores the condition of incomplete
multi-modality neuroimages. We will further improve the GCN
classiﬁer and solve the limitation of incomplete multi-modality
neuroimages in our future work. VI. C
ONCLUSION
We propose to use structural connectivity strength to con-
struct the functional connectivity network, which realizes
the fusion of dual-modality imaging data (fMRI and DTI). Its better performance than the other popular fusion methods
indicates that stronger structural connectivity among ROIs
implies better discriminative functional connectivity feature in
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply. 366 IEEE TRANSACTIONS ON MEDICAL IMAGING, VOL. 42, NO.

**Passage 21:**

> d λ is
a parameter to control sparsity. Constructing C is the key to boosting performance. We con-
sider the structural connectivity network and connectivity
strength diversity between subject groups. Given T training
subjects and their corresponding disease statuses, we divide
all training subjects into two groups based on their labels. Here, we also consider the diversity between multi-center
datasets. Then the two groups with DTI connectivity strength
information are denoted as SC
+=[ SC1+, SC2+,..., SCT1+]
and SC− =[ SC1− , SC2− ,..., SCT2− ], respectively. Here T1
and T2 are the number of subjects in two groups (T1+T2 = T).

**Passage 22:**

> DISCRIMINA TI
get their highest ACC by setting the pooling rate as 10%. N Cv s .S M C ,N Cv s .E M C I ,N Cv s .L M C Ia n dS M Cv s . LMCI get their highest ACC with setting the pooling rate
as 15%. The mean ACC of six tasks gets the highest value
with setting the pooling rate as 15%. Using our pooling
mechanism by setting the best pooling rate, the mean ACC gets
up to 2.3% improvement, validating our pooling mechanism’s
effectiveness. E. Most Discriminative Connectivity Features and
Related ROIs
When constructing the dual-modality brain connectivity
network, well-known and highly-correlated ROIs in AD/MCI
disease are used [45]–[48]. For example, the inferior tempo-
ral gyrus (ITG.R), insula (INS.R), olfactory cortex (OLF.L),
angular gyrus (ANG.L), amygdala (AMYG.R) and pre-
cuneus (PCUN.R).

**Passage 23:**

> g et al. , “Graph convolution network with similarity awareness
and adaptive calibration for disease- induced deterioration prediction,”
Med. Image Anal. , vol. 69, Apr. 2021, Art. no. 101947.
[14] J. Gonzalez-Castillo et al. , “Tracking ongoing cognition in individuals
using brief, whole-brain functional connectivity patterns,” Proc. Nat. Acad. Sci. USA
, vol. 112, no. 28, pp. 8762–8767, Jun. 2015.
[15] R. Yu, H. Zhang, L. An, X. Chen, Z. Wei, and D. Shen, “Connectivity
strength-weighted sparse group repr esentation-based brain network con-
struction for MCI classiﬁcation,” Hum. Brain Mapping , vol. 38, no. 5,
pp. 2370–2383, 2017.
[16] Y. Z h a n get al. , “Strength and similarity guided group-level brain
functional network construction for MCI diagnosis,” Pattern Recognit.,
vol. 88, pp. 421–430, Apr. 2019.
[17] L. Qiao, H. Zhang, M. Kim, S. Teng, L. Zhang, and D.

**Passage 24:**

> tivity (SEN), speci-
ﬁcity (SPE) and area under the curve (AUC) are used as
evaluation criteria. The GCN parameters of all strategies in this
paper are ﬁxed and chosen according to previous work [24]. Parameter details are set as below: dropout rate is set as 0.1,
regularization rate is set as 5 × 10
−4, the learning rate is set
as 0.005, the number of epochs is set as 200, the default
polynomial order is set as 3, the number of neurons per layer
is set as 32, and the number of selected features by using RFE
is set as 200. A. Performance of Fused Brain Connectivity Network
The SR method uses fMRI signals to construct a func-
tional connectivity network, and we introduce the DTI-strength
penalty term to induce its sparse regularization. Here, we eval-
uate the effectiveness of our fusion method by comparing it
with the other three fusion methods (shown in Fig.

</details>

---

## Multiclass-prediction-of-Alzheimer-s-disease-using-_2026_Biomedical-Signal-P
_File: `Multiclass-prediction-of-Alzheimer-s-disease-using-_2026_Biomedical-Signal-P.pdf`_

1. **Was diffusion MRI (DTI, dMRI, DWI, or similar) used in this paper?**  
   Yes. The paper explicitly mentions **diffusion weighted imaging (DWI)** in the context of AD vs. HC classification by Lella et al. [31].  

---

2. **What processing steps were applied to the diffusion images?**  
   The excerpts do **not explicitly describe processing steps specific to diffusion MRI** (e.g., DWI). The preprocessing steps mentioned (e.g., DICOM to NIFTI conversion, skull-stripping, intensity correction) apply to general MRI, not diffusion MRI.  

---

3. **What software or tools are explicitly named for processing?**  
   - **dcm2nii** (DICOM to NIFTI conversion)  
   - **FSL-BET** (Brain Extraction Tool)  
   - **SPM8** (statistical parametric mapping)  
   - **N3** (non-parametric non-uniform intensity normalization)  
   - **Matlab’s "imregister"** (intensity-based image registration)  

---

4. **What acquisition or processing parameters are explicitly reported?**  
   - **Voxel size**: 2 × 3.1 × 2 mm³  
   - **Isotropic resolution**: 1.0 mm  
   - **Repetition time (TR)**: 5050 ms  
   - **Echo time (TE)**: 10 ms  

---

5. **Copy the exact sentences from the excerpts that describe the processing.**  
   - "First, we collected the DICOM images for each subject from the link to each database. Then, a conversion to NIFTI format of the DICOM images is made using the dcm2nii tool. Finally, the NIFTI images are organized in standard BIDS format. The used neuroimaging data (MRI and PET scans) are skull-stripped and corrected for intensity inhomogeneity volumes. For each scan, the deletion of non-brain tissue is performed using the FSL-BET tool (Brain Extraction Tool) [82]."  
   - "Then the statistical parametric mapping (SPM8) tool [83] is applied to partially correct spatial intensity inhomogeneities. The concern about intensity non-uniformity of tissue is solved by applying the N3 (non-parametric non-uniform intensity normalization) technique [84]."  
   - "To align the MRI and PET scans in a common coordinate system, we opted for intensity-based image registration by applying Matlab’s 'imregister' function."  

---

6. **Is the processing description complete, or does it appear incomplete/missing?**  
   The processing description **appears incomplete**. While general MRI preprocessing steps are detailed, **specific diffusion MRI (DWI) processing steps** (e.g., diffusion-weighted acquisitions, tensor fitting, tractography) are **not explicitly described**. The mention of DWI in the context of prior work [31] does not detail its processing in this paper.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> ataset, HC patients have a CDR of 0 and an MMSE score of at 
least 24; MCIs with a CDR of 0.5 and an MMSE score of roughly 20-25; 
and ADs with a CDR of at least 0.5 and an MMSE score of less than 27. In 
this way, considering the CDR scale, the OASIS dataset is split into 176 
HC, 99 AD-CDR0.5, 46 AD-CDR1, 79 AD-CDR2 and 15 AD-CDR3 and the 
ADNI dataset into 90 HC, 30 MCI and 80 AD. 3.2. Preprocessing
First, we collected the DICOM images for each subject from the link 
to each database. Then, a conversion to NIFTI format of the DICOM 
images is made using the dcm2nii tool. Finally, the NIFTI images are 
organized in standard BIDS format. The used neuroimaging data (MRI 
and PET scans) are skull-stripped and corrected for intensity in -
homogeneity volumes. For each scan, the deletion of non-brain tissue is 
performed using the FSL-BET tool (Brain Extraction Tool) [ 82 ].

**Passage 2:**

> with Matlab R2024a 
and run on a Lenovo ThinkStation P7 Workstation using an Intel ® 
Xeon ® W7-3445 CPU @ 4.80 GHz with 32 GB of RAM and a NVIDIA ® 
RTX ™ 2000 Ada Generation GPU with16GB GDDR6. 4.1. Machine learning classifiers
The systems using conventional ML classifiers begin with the pre -
processing of MRI images to only keep relevant data by reducing the 
effects of noise, inter-slice intensity variations, and intensity in -
homogeneity. Then, each image is represented by grayscale features (we 
used raw voxel values as distinct features) and is collapsed into a new 
feature space by applying PCA-based feature selection to pick the 
optimal features.

**Passage 3:**

> PET scans) are skull-stripped and corrected for intensity in -
homogeneity volumes. For each scan, the deletion of non-brain tissue is 
performed using the FSL-BET tool (Brain Extraction Tool) [ 82 ]. Then the 
statistical parametric mapping (SPM8) tool [ 83 ] is applied to partially 
correct spatial intensity inhomogeneities. The concern about intensity 
non-uniformity of tissue is solved by applying the N3 (non-parametric 
non-uniform intensity normalization) technique [ 84 ]. Then the hybrid 
median filter is employed to remove impulse noise while preserving 
edges. To align the MRI and PET scans in a common coordinate system, we 
opted for intensity-based image registration by applying Matlab ’ s 
“ imregister ” function.

**Passage 4:**

> e impulse noise while preserving 
edges. To align the MRI and PET scans in a common coordinate system, we 
opted for intensity-based image registration by applying Matlab ’ s 
“ imregister ” function. This function performs resampling with 
displacement to provide a registered output image from the geometric 
transformation estimate using the “ imreg tform ” script. In this context, 
we assigned labels for brain structures (from hemispheres to cytoarch -
itectural regions) using the VOTL (volume occupancy Talairach labels) 
Table 2 
Demographic and clinical information of the subjects. ADNI (n ¼ 200) OASIS (n ¼ 415)
Male Female Male Female
Age 75.4 ± 7.1 75.3 ± 5.2 70.17 (42.5 – 91.7) 67.78 (43.2 – 95.6)
Education 14.9 ± 3.4 15.6 ± 3.2 15.2 ± 2.

**Passage 5:**

> performance between classification algorithms in 
medical data. JAMIA Open , 6 (2), doi: 10.1093/jamiaopen/ooad033 (ooad033).
[81] S.M. Smith, Fast robust automated brain extraction, Hum. Brain Mapp. 17 (3) 
(2002) 143 – 155, https://doi.org/10.1002/hbm.10062 .
[82] spm8. Available online at https://www.fil.ion.ucl.ac.uk/spm/software/spm8/ 
(accessed on 20 october 2022).
[83] N3. Available online at http://www.bic.mni.mcgill.ca/software/N3/ (accessed 
on 23 October 2022).
[84] Hüttenrauch, B. (2016). Literature review on data augmentation. In geb. K. Hüttenrauch Bettina (
´
Ed.), Targeting Using Augmented Data in Database Marketing : 
Decision Factors for Evaluating External Sources (p. 71 – 104). Springer Fachmedien 
Wiesbaden. https://doi.org/10.1007/978-3-658-14577-4_3.
[85] J.T. McClave, T. Sincich, Statistics , (13th ed.), Pearson, 2016 .
[86] W.-C. Lien, C.-H. Yeh, C.-Y.

**Passage 6:**

> eral 
point, coordinate z =   56 for the lowest point of the brain, and co -
ordinate z = 82 for the highest point of the brain; the coordinates (0, 
  34, 0) are assigned to the posterior commissure. All slices of MRI and PET images are resampled to contain 256 × 256 
× 128 voxels covering the entire region of brain using the following 
parameters: voxel size of 2 × 3.1 × 2 mm
3
, isotropic resolution of 1.0 
mm, repetition time of 5050 ms, and echo time of 10 ms. 3.3. Feature extraction
Typically, it is more difficult for classifiers to learn the input dataset 
including the entire images as well as the spatial relationships between 
its voxels. In this phase, transformations are performed to extract rele -
vant features to facilitate and accelerate the learning process. 3.3.1.

**Passage 7:**

> Yao, D. Zhang, M. Liu, D. Shen, Spatial-temporal 
dependency modeling and network hub detection for functional MRI analysis via 
convolutional-recurrent network, IEEE Trans. Biomed. Eng. 67 (8) (Aug. 2020) 
2241–2252, https://doi.org/10.1109/TBME.2019.2957921. L. Lazli et al. Biomedical Signal Processing and Control 114 (2026) 109026 
29

**Passage 8:**

> impairments. 1.1. Challenges and paper’s contribution
Due to the limitations raised in the literature and generally discussed 
above, the significant contributions of the article are described below. The work’s first challenge is to develop an information fusion process 
(see [ 3 , 67 , 94 ] for systematic review) capable of aggregating the het -
erogeneous data from a multimodal environment that non-invasively 
considers the connectivity between anatomical MRI sequences (T1- 
weighted and T2-weighted in the axial, sagittal, and coronal views) and 
functional PET imaging with the three [11C]PIB, [18F]AV45 and [18F] 
FDG radiopharmaceuticals. MRI and PET images respectively give structural and functional in -
formation relating to the brain and, therefore, aid in understanding 
neural changes.

**Passage 9:**

> ’ s Disease Assessment Scale-Cognitive subscale, APOE: apolipoprotein E. L. Lazli et al. Biomedical Signal Processing and Control 114 (2026) 109026 
11 
database from the Freesurfer software package. This basis allows us to 
organize the labels in the form of a hierarchical volume filling naming 
scheme and Talairach label data are stored in NIfTI type images files 
(Talairach.nii). Through these files, Talairach x-y-z coordinates are 
assigned to each voxel and recorded in a 4 × 4 sform matrix with co -
ordinates (1,1,1) assigned to the first voxel from the bottom left poste -
rior. For scaling, the brain was centered in the interhemispheric plane on 
the point of the anterior commissure having as coordinates (0,0,0). Then, the cerebral surface is cut into twelve rectangular boxes.

**Passage 10:**

> Research 
Institute at the University of Southern California, United States. ADNI 
data are disseminated by the Laboratory for Neuro Imaging at the Uni -
versity of Southern California, United States. The OASIS-3 data were provided in part by OASIS Longitudinal 
Multimodal Neuroimaging: Principal Investigators: T. Benzinger, D. Marcus, J. Morris; NIH P30 AG066444, P50 AG00561, P30 
NS09857781, P01 AG026276, P01 AG003991, R01 AG043434, UL1 
TR000448, R01 EB009352. AV-45 doses were provided by Avid Ra -
diopharmaceuticals, a wholly owned subsidiary of Eli Lilly, United 
States. Thanks to the participants of the AIBL Study and their families for 
their ongoing support of Alzheimer ’ s disease research.

**Passage 11:**

> ts: (a) Total number and number of subjects by gender, (b) Number of subjects by class. L. Lazli et al. Biomedical Signal Processing and Control 114 (2026) 109026 
10 
(ADRC) at Washington University. The selected ADNI-3 dataset includes 
serial MRI and PET images, information about genetic and biochemical 
biomarkers, as well as clinical and neuropsychological assessment. The multimodal data collected from the two databases are merged to 
develop better neuroimaging models. In the context of neuroimaging 
data collection, we selected MRI and PET images. The combination of 
these modalities promotes more predictable and precise early diagnosis 
than y applying a single one.We used T1-weighted and T2-weighted 
anatomical MRI sequences that provide longitudinal and multi -
parametric information.

**Passage 12:**

> classifier based on MAMIR resampling
5 
2
415 (1383) T1-MRI /T2-MRI/FDG-PET/ PIB-PET/ 
AV45-PET/ Clinical measures/ 
Demographic information
94.7 
98.2
*
Indicates that the value is number of samples. Table 12 
The diagnosis results (in %) obtained with the proposed CAD system on the AIBL dataset (Results from other models are reported for comparison). SEN SPC ACC PRC F1 MCC AUC
KNNs 78.28 80.36 82.28 82.14 79.14 80.42 80.11
VGGNet 86.24 88.18 90.17 93.35 92.62 90.61 91.46
Enhanced DL 92.12 92.27 91.45 93.18 93.48 93.47 92.62
MAMIRBoost ensemble 96.13 95.12 97.02 95.91 96.56 96.64 96.34
Table 13 
Performance evaluation of the proposed CAD system as per the Ablation study 
for OASIS and ADNI datasets.

**Passage 13:**

> own the brain tissue damage with proper treat -
ment [ 2 ]. In this regard, a computer-aided diagnosis (CAD) system can 
* Corresponding author. E-mail address: lilia.lazli.1@ens.etsmtl.ca (L. Lazli). 1
Data used in preparation of this article were obtained from the Alzheimer ’ s Disease Neuroimaging Initiative (ADNI) database (https://adni.loni.usc.edu). As 
such, the investigators within the ADNI contributed to the design and implementation of ADNI and/or provided data but did not participate in analysis or writing of 
this report. A complete listing of ADNI investigators can be found at: https://adni.loni.usc.edu/wp-content/uploads/how_to_apply/ADNI_Acknowledgement_List.pdf.

**Passage 14:**

> brain images classification from ADNI and OASIS datasets. Reference Learning model Dataset Strength and method discussion Limitation
[ 115 ] Spatial-Temporal convolutional- 
recurrent neural Network. ADNI with 
4 classes
Convolutional-recurrent network is designed to 
identify the brain regions and capture both the local 
(i.e., brain regions) and global (i.e., whole-brain) 
spatial temporal dependency patterns. Use only the single modality fMRI. Other more 
informative modalities should be exploited such as sMRI 
and FDG-PET and to take advantage of multimodality 
which can provide complementary information for 
diagnosis. Inserting biomarker information and 
laboratory tests could help detect patients with MCI and 
AD. Other templates should be tested in comparison with 
the AAL template used in the study for ROI partitioning 
may improve the performance of the system.

**Passage 15:**

> r scaling, the brain was centered in the interhemispheric plane on 
the point of the anterior commissure having as coordinates (0,0,0). Then, the cerebral surface is cut into twelve rectangular boxes. The latter 
are placed on each side of the axial plane (x,y) and the sagittal plane (x, 
z) as well as between the two coronal planes (y,z) by crossing the lower 
edge of the posterior commissure and the upper edge of the anterior 
commissure.

**Passage 16:**

> (1) (2022) 1975393, https://doi. 
org/10.1080/08839514.2021.1975393 .
[78] M. Zheng, F. Wang, X. Hu, Y. Miao, H. Cao, M. Tang, Axioms 11 (11) (2022), 
https://doi.org/10.3390/axioms11110607 .
[79] F. Alahmari, A comparison of resampling techniques for medical data using 
machine learning, J. Inf. Knowl. Manag. 19 (01) (2020) 2040016, https://doi. 
org/10.1142/S021964922040016X .
[80] Welvaars, K., Oosterhoff, J. H. F., van den Bekerom, M. P. J., Doornberg, J. N., 
van Haarst, E. P., & OLVG Urology Consortium, and the M. L. C. (2023). Implications of resampling data to address the class imbalance problem (IRCIP): 
An evaluation of impact on performance between classification algorithms in 
medical data. JAMIA Open , 6 (2), doi: 10.1093/jamiaopen/ooad033 (ooad033).
[81] S.M. Smith, Fast robust automated brain extraction, Hum. Brain Mapp.

**Passage 17:**

> images as well as the spatial relationships between 
its voxels. In this phase, transformations are performed to extract rele -
vant features to facilitate and accelerate the learning process. 3.3.1. Haar wavelet Transforms
The raw multimodal neuroimaging data underwent transformation 
to be suitable for feature extraction. Due to the high dimensionality of 
the MRI and PET scans, we extracted compact features using the discrete 
wavelet transform (DWT) [ 19 ]. The DTW allows breaking down the 
scans into several levels of resolution and thus representing them with 
wavelet coefficients. We used the Haar transform for this (level 1 to 3). We transform samples of MRI and PET images (input data vectors of 
size n ) from the spatial domain to the wavelet (frequency) domain 
generating discrete outputs in map form (vectors of the same size n ).

**Passage 18:**

> stems of AD are proposed in the literature based on 
conventional ML classifiers and MRI neuroimaging. Using ADNI, Lella et al. [ 31 ] achieved an ACC and AUC of 75 % and 
83 % respectively for AD vs. HC classification using diffusion weighted 
imaging (DWI) and multi-layer perceptron (MLP) classifier; Rallabandi 
et al. [ 8 ] obtained an overall ACC and AUC of 75 % and 76 % respec -
tively using the FreeSurfer tool for feature extraction computing the 
regional cortical thickness and SVM classifier based on basis function 
(RBF) kernel; Applying the same classifier, Eke et al. [ 9 ] proposed a 
correlation-based feature subset selection technique to identified a novel 
candidate non-amyloid biomarker panels using blood proteomic data 
and, achieved an AUC of 89 % and 80 % respectively for (AD vs. HC) and 
(MCI vs.

**Passage 19:**

> ansform samples of MRI and PET images (input data vectors of 
size n ) from the spatial domain to the wavelet (frequency) domain 
generating discrete outputs in map form (vectors of the same size n ). We 
then obtain orthogonal matrices of dimension n × n , whose corre -
sponding transform represents a rotation in R
n 
which each data (a n 
  type) is a point in R
n
. So that the coordinates of a specific point in the 
rotated space correspond to the DWT of the original coordinates. 3.3.2. Data augmentation
The data augmentation [ 85 ] is applied to improve the generalization 
ability of classifiers. In the case of MRI and PET image data augmenta -
tion, geometric transformations were performed of scaling, flipping, 
rotating and translating on each original image to create new ones, 
allowing the expansion of the size and diversity of the training dataset.

**Passage 20:**

> I, https://adni.loni.usc.edu/ ) datasets with various types 
of information, counting neurological examinations, several neuro -
imaging procedures, functional and cognitive analyses, and blood tests. The data acquisition procedures and parameters are available in the 
corresponding websites. The OASIS-3 database is intended for normal 
and pathological aging affected by AD. It contains biomarkers, clinical 
and cognitive data as well as multimodal neuroimaging images. The 
subjects with and without dementia were selected from a larger data -
base and acquired from the Alzheimer ’ s Disease Research Center 
Fig. 3. Dispersion of the OASIS dataset separated in five classes. Fig. 4. Datasets: (a) Total number and number of subjects by gender, (b) Number of subjects by class. L. Lazli et al. Biomedical Signal Processing and Control 114 (2026) 109026 
10 
(ADRC) at Washington University.

**Passage 21:**

> by the “ Fonds de recherche du Qu ´ebec- 
Nature et Technologies – FRQNT ” grants, Canada under award numbers 
314498 (https://doi.org/10.69777/314498) and 358107 (https://doi. 
org/10.69777/358107). Data collection and sharing for ADNI was funded by the Alzheimer ’ s 
Disease Neuroimaging Initiative (ADNI) (National Institutes of Health 
Grant U01 AG024904) and DOD ADNI (Department of Defense award 
number W81XWH-12-2-0012), United States.

**Passage 22:**

> ) ​
# Experiment ACC (%) F1-score (%)
1 – with all input features 95 95.8
2 – except gender features 92.6 93.1
3 – except age features 85.1 84.6
4 – except APOE gene features 81.7 82.1
L. Lazli et al. Biomedical Signal Processing and Control 114 (2026) 109026 
25 
Declaration of competing interest
The authors declare that they have no known competing financial 
interests or personal relationships that could have appeared to influence 
the work reported in this paper. Acknowledgments
This project was supported by the “ Fonds de recherche du Qu ´ebec- 
Nature et Technologies – FRQNT ” grants, Canada under award numbers 
314498 (https://doi.org/10.69777/314498) and 358107 (https://doi. 
org/10.69777/358107).

**Passage 23:**

> t participate in analysis or writing of 
this report. A complete listing of ADNI investigators can be found at: https://adni.loni.usc.edu/wp-content/uploads/how_to_apply/ADNI_Acknowledgement_List.pdf. Contents lists available at ScienceDirect
Biomedical Signal Processing and Control
journal homepag e: www.el sevier.com/loc ate/bspc
https://doi.org/10.1016/j.bspc.2025.109026
Received 15 January 2025; Received in revised form 17 October 2025; Accepted 31 October 2025  
Biomedical Signal Processing and Control 114 (2026) 109026 
Available online 5 December 2025 
1746-8094/© 2025 The Authors. Published by Elsevier Ltd. This is an open access article under the CC BY-NC-ND license ( http://creativecommons.org/licenses/by- 
nc-nd/4.0/ ). 
be useful in the neurologist toolbox, as it may help make a timely 
diagnosis and optimize the treatment of Alzheimer’s patients.

**Passage 24:**

> d. Kendall ’ s Tau statistical test and Z test are performed to assess the 
feasibility of the approach by calculating the probability value p-value 
via the first test and the Z-score via the second. The p-values of the 
model are 0.027 and 0.033 for OASIS and ADNI respectively and less 
than that obtained by the best ML classifier (p-values = 0.089, 0.086), 
the best DL classifier (p-values = 0.074, 0.081), and enhanced DL (p- 
values = 0.062, 0.071). The corresponding Kendall ’ s Tau value lower 
than 0.05 is statistically significant and provides powerful evidence in 
anticipation of the null hypothesis, which affirms the existence of a 
statistically significant correlation.

</details>

---

## Multimodal Neuroimaging for Early Alzheimer-s detection A Deep Learning Approach
_File: `Multimodal Neuroimaging for Early Alzheimer-s detection A Deep Learning Approach.pdf`_

1. **Was diffusion MRI (DTI, dMRI, DWI, or similar) used in this paper?**  
   Yes. The paper explicitly mentions **diffusion tensor imaging (DTI)** as one of the modalities used, alongside structural MRI (sMRI) and functional MRI (fMRI).  

---

2. **What processing steps were applied to the diffusion images?**  
   The following steps are explicitly stated:  
   - **Feature extraction** from DTI data using a **graph convolutional network (GCN)**.  
   - **Data augmentation techniques** to address class imbalance and improve model robustness.  
   - **Integration of subnetworks** (sMRI CNN, fMRI RNN, DTI GCN) into a **multimodal neural network** for classification.  

---

3. **What software or tools are explicitly named for processing?**  
   No specific software or tools are explicitly named. The paper refers to **CNN**, **RNN**, and **GCN** as architectures but does not mention tools like FSL, MRtrix, or other diffusion MRI processing pipelines.  

---

4. **What acquisition or processing parameters are explicitly reported?**  
   **Not reported in available text.** The excerpts do not mention b-values, number of diffusion directions, voxel size, or other acquisition/processing parameters.  

---

5. **Copy the exact sentences from the excerpts that describe the processing.**  
   - "Employ data augmentation techniques to address class imbalance and improve the robustness of the deep learning model."  
   - "Create an innovative deep learning architecture that takes use of features from all three imaging modalities: a sMRI CNN, an fMRI RNN, and a DTI graph convolutional network (GCN)."  
   - "Train the subnetworks separately and then combine them to make a modal neural network for classification."  

---

6. **Is the processing description complete, or does it appear incomplete/missing?**  
   **Incomplete.** The description focuses on high-level steps (feature extraction, data augmentation, model integration) but does not detail specific diffusion MRI processing steps such as diffusion tensor analysis, tractography, or parameter estimation. Key technical details about diffusion MRI preprocessing are missing.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> Alzheimer's detection 
neuroimaging initiative. Neuroimaging Clinics, 15(4), 869-877. 
[15] Ashburner, J., & Friston, K. J. (2005). Unified segmentation. Neuroimage, 26(3), 839-851. 
[16] Friston, K. J., Williams, S., Howard, R., Frackowiak, R. S., & Turner, 
R. (1996). Movement -related effects in fMRI time -series. Magnetic 
Resonance in Medicine, 35(3), 346-355. 
[17] Basser, P. J., & Jones, D. K. (2002). Diffusion -tensor MRI: theory, 
experimental design, and data analysis - a technical review. NMR in 
Biomedicine, 15(7-8), 456-467. 
[18] Jia, H., Lao, H. Deep learning and multimodal feature fusion for the 
aided diagnosis of Alzheimer's disease. Neural Comput & Applic 34, 
19585–19598 (2022). https://doi.org/10.1007/s00521-022-07501-0 
[19] LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. Nature, 
521(7553), 436-444. 
[20] Hochreiter, S., & Schmidhuber, J. (1997).

**Passage 2:**

> thods. Create a deep learning framework that can easily 
incorporate different kinds of neuroimaging data, such as 
those from fundamental MRI, functioning MRI, and diffusion 
tensor image processing. Find out how well our model performs in terms of 
classification accuracy, sensitivity, and specificity. The purpose of this research is to compare and contrast our 
suggested model to popular deep learning techniques already 
in use. IEEE - 56998
14th ICCCNT IEEE Conference 
July 6-8, 2023 
IIT - Delhi, Delhi, India
2023 14th International Conference on Computing Communication and Networking Technologies (ICCCNT) | 979-8-3503-3509-5/23/$31.00 ©2023 IEEE | DOI: 10.1109/ICCCNT56998.2023.10307780
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply.

**Passage 3:**

> Multimodal Neuroimaging for Early Alzheimer's 
detection: A Deep Learning Approach 
Dr.

**Passage 4:**

> re data quality, 
consistency, and reliability. Following pre-processing, extract 
relevant features from the data for each imaging modality, 
capturing essential information from sMRI, fMRI, and DTI. Employ data augmentation techniques to address class 
imbalance and improve the robustness of the deep learning 
model. Create an innovative deep learning architecture that takes 
use of features from all three imaging modalities: a sMRI 
CNN, an fMRI RNN, and a DTI graph convolutional network 
(GCN). For the best final classification results, train the 
subnetworks separately and then combine them to make a 
modal neural network for classification. Tweak the model's 
hyper parameters until they're just right. Fig. 1.

**Passage 5:**

> ification studies and 
associated feature extraction methods for Alzheimer's detection and its 
prodromal stages. NeuroImage, 155, 530-548. 
[12] Jack, C. R., Bennett, D. A., Blennow, K., Carrillo, M. C., Dunn, B., 
Haeberlein, S. B., ... & Silverberg, N. (2018). NIA -AA Research 
Framework: Toward a biological definition of Alzheimer's detection. Alzheimer's & Dementia, 14(4), 535-562. 
[13] Frisoni, G. B., Fox, N. C., Jack, C. R., Scheltens, P., & Thompson, P. M. (2010). The clinical use of structural MRI in Alzheimer detection. Nature Reviews Neurology, 6(2), 67-77. 
[14] Mueller, S. G., Weiner, M. W., Thal, L. J., Petersen, R. C., Jack, C. R., 
Jagust, W., ... & Beckett, L. (2005). The Alzheimer's detection 
neuroimaging initiative. Neuroimaging Clinics, 15(4), 869-877. 
[15] Ashburner, J., & Friston, K. J. (2005). Unified segmentation. Neuroimage, 26(3), 839-851. 
[16] Friston, K.

**Passage 6:**

> Y. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply. 
[23] [28] Ellis, K. A., Bush, A. I., Darby, D., De Fazio, D., Foster, J., 
Hudson, P., ... & Maruff, P. (2009). The Australian Imaging, 
Biomarkers and Lifestyle (AIBL) study of aging: methodology and 
baseline characteristics of 1112 individuals recruited for a longitudinal 
study of Alzheimer's detection. International Psychogeriatrics, 21(4), 
672-687. 
[24] Marcus, D. S., Wang, T. H., Parker, J., Csernansky, J. G., Morris, J. C., 
& Buckner, R. L. (2007). Open Access Series of Imaging Studies 
(OASIS): cross -sectional MRI data in young, midd le-aged, 
nondemented, and demented older adults. Journal of Cognitive 
Neuroscience, 19(9), 1498-1507. 
[25] Reitz, C., Brayne, C., & Mayeux, R. (2011). Epidemiology of 
Alzheimer detection. Nature Reviews Neurology, 7(3), 137-152.

**Passage 7:**

> he diagnosis of Alzheimer's 
detection. Various data kinds, sizes, and dimensions make it 
difficult to integrate multimodal neuroimaging data into a 
unified framework, as described in reference [8]. The goal of this study is to develop a novel deep learning 
approach that integrates multimodal neuroimaging data, 
including structural MRI, fMRI, and DTI, to aid in the early 
diagnosis of Alzheimer's detection. It is expected that our 
strategy will achieve more diagnostic accuracy than existing 
approaches by mak ing use of the information provided by 
these various forms of imaging in a complimentary way. The 
current study describes our aims and methods. Create a deep learning framework that can easily 
incorporate different kinds of neuroimaging data, such as 
those from fundamental MRI, functioning MRI, and diffusion 
tensor image processing.

**Passage 8:**

> roimaging data to 
improve the accuracy and timeliness of Alzheimer's detection 
diagnosis, our study aims to add to the existing body of 
literature and address the limitations of current approaches. A 
convolutional neural network (CNN) is used for structural 
MRI data, a recurrent neural network (RNN) is used for fMRI 
data, and a graph-based convolutional network (GCN) is used 
for diffusion tensor imaging (DTI) data in the proposed 
framework's tripartite structure. It is expected that the 
diagnostic accuracy for identifying people in the early stages 
of Alzheimer's detection would increase once the subnetwork 
outputs are integrated into a cohesive model. In addition to improving classification accuracy, our 
strategy is designed to provide light on the relationships 
between various imaging techniques for identifying AD.

**Passage 9:**

> lzheimer's detection (AD) 
is crucial for initiating therapy as soon as possible. This paves 
the way for patients to take advantage of current medicines 
and better control detection progression [2]. Due to its 
complex and heterogeneous nature, early diagnosis of 
Alzheimer's detection (AD) is a major challenge [3]. It has been shown that multimodal neuroimaging methods 
have the ability to detect brain abnormalities associated with 
Alzheimer's detection. Diffusion tensor analysis (DTI), 
functional magnetic resonance imaging (fMRI), and structural 
MRI (sMRI) all provide unique but complimentary 
perspectives on brain anatomy, function, and connection [4]. The combination of various imaging techniques may improve 
diagnostic accuracy [5].

**Passage 10:**

> 018) used a 
convolutional neural network (CNN) to analyze sMRI data 
and got an accuracy rate of 89.7%. Information gathered from fMRI scans has been used to 
make diagnoses of Alzheimer's detection. To examine fMRI 
data, Suk et al. [11] used a deep learning model that 
incorporated a stacked autoencoder. The findings indicated 
that the model had an ac curate classification rate of 84.3% 
when trying to differentiate between AD sufferers and healthy 
controls. In a different study, Wee et al. [12] fused fMRI and 
sMRI data using a multimodal sparse representation 
technique, and their AD diagnosis accuracy i ncreased to 
88.2%. B. Multimodal neuroimaging studies: 
Combining multiple neuroimaging modalities has been 
shown to improve diagnostic performance.

**Passage 11:**

> al 
and multimodal neuroimaging data. The review encompasses 
an evaluation of the efficacy of these methodologies, as well 
as an examination of the obstacles encountered in their 
implementation. A. Single-modal neuroimaging studies: 
For the goal of diagnosing Alzheimer's detection, 
neuroimaging data from a single modality has been used in a 
large number of scholarly investigations. An SVM classifier 
built by Zhang et al. (2019) using sMRI data successfully 
distinguished 86.5% of AD patients from controls. To classify 
individuals with Alzheimer's detection (AD) and moderate 
cognitive impairment (MCI), Liu et al. (2018) used a 
convolutional neural network (CNN) to analyze sMRI data 
and got an accuracy rate of 89.7%. Information gathered from fMRI scans has been used to 
make diagnoses of Alzheimer's detection.

**Passage 12:**

> tural 
MRI (sMRI) all provide unique but complimentary 
perspectives on brain anatomy, function, and connection [4]. The combination of various imaging techniques may improve 
diagnostic accuracy [5]. New advancements in deep learning 
approaches [6] provide encouraging capabilities for analyzing 
multidimensional brain imaging data for the early diagnosis of 
Alzheimer's detection. However, much of the present research has focused on 
using separate -modal neuroimaging data, which may limit 
their diagnostic effectiveness [7], despite the growing interest 
in using deep learning to the diagnosis of Alzheimer's 
detection. Various data kinds, sizes, and dimensions make it 
difficult to integrate multimodal neuroimaging data into a 
unified framework, as described in reference [8].

**Passage 13:**

> DNN, 
SVM, RF 
MMSE, 
MRI 
85-98% 80-95% 75-90% 0.85
-
0.98 
[18] SVM,  AUC fMRI, 
sMRI 
91-97%  70-97% 75-85% 0.75
-
0.88 
Prop
osed 
Algor
ithm 
CNN, 
RNN, 
GCN 
MMSE, 
fMRI 90% 85% 92% 0.96 
 
VI. CONCLUSION 
In conclusion, our study has developed and evaluated a 
novel algorithm for early diagnosis of Alzheimer's detection 
using multimodal neuroimaging and deep learning. Our 
proposed algorithm achieved a high level of accuracy, 
sensitivity, sp ecificity, and AUC -ROC, demonstrating its 
potential for improving diagnostic accuracy and patient 
outcomes. Our study has also identified gaps in existing 
research, including limited generalizability and interpretation 
of model decision -making processes. Through our research, 
we have addressed these gaps by developing a transparent and 
effective algorithm that can be used in clinical practice.

**Passage 14:**

> lassification results, train the 
subnetworks separately and then combine them to make a 
modal neural network for classification. Tweak the model's 
hyper parameters until they're just right. Fig. 1. Comparative Coronal MRI Views: Multimodal Imaging in 
Alzheimer's Detection from the ADNI Dataset 
 
The model's accuracy should be checked using an 
independent dataset, and it should be compared to both 
baseline algorithmic approaches and current deep learning 
techniques. Evaluate the model's genera lizability on a new 
dataset to prove its clinical usefulness.

**Passage 15:**

> zheimer's dete ction 
categorization. The dataset utilized in this study comprised of 
1200 participants, with 600 individuals diagnosed with early -
stage AD and 600 healthy controls matched for age. The 
application of data augmentation techniques was employed to 
mitigate c lass imbalance and enhance the resilience of our 
model. We used a three-tiered deep learning architecture, which 
included a sMRI CNN, an fMRI RNN, and a DTI GCN to 
analyze MRI data. The final categorization was performed by 
fusing several previously separa te networks into a single 
multimodal neural network. Our study involved a comparative 
analysis of the efficacy of our model vis -à-vis conventional 
machine learning algorithms and pre -existing deep learning 
techniques.

**Passage 16:**

> Multimodal Neuroimaging for Early Alzheimer's 
detection: A Deep Learning Approach 
Dr. Gurpreet Singh Chhabra  
Computer Science & Engineering 
department of GITAM School of 
Technology, GITAM Deemed to be 
University, Visakhapatnam, Inida 
gurpreet.kit@gmail.com 
Mr Leelkanth Dewangan 
Assistant Professor, G H Raisoni 
Institute of Engineering and Business 
Management jalgaon, Maharashtra, 
India 
mcs.leelkanth@gmail.com 
Dr Abhishek Guru 
Department of CSE, Koneru 
Lakshmaiah Education Foundation, 
Vaddeswaram 522302, AP, India 
abhishekguru0703@gmail.com 
Dr Suman Kumar Swarnkar 
Department of Computer Science & 
Engineering, Shri Shankaracharya 
Institute of Professional Management 
and Technology, Raipur, Chhattisgarh, 
India 
sumanswarnkar17@gmail.com
Dr Bhawna Janghel Rajput 
Assistant Professor, Department of 
Computer Science & Engineering, 
Rungta College of Engineering in 
Bhilai, Durg.(C.G.) 
bhawna.janghel@rungta.ac.in 
Abstract—  The timely identification and treatment of 
Alzheimer's detection (AD) is of paramount importance.

**Passage 17:**

> validati on of 
our model in more extensive, multi -center cohorts and the 
examination of its efficacy in forecasting the advancement of 
detection and the effectiveness of therapeutic interventions. Keywords— Alzheimer's detection, Diffusion tensor imaging, 
Deep learning models, Convolutional neural network(CNN), 
Recurrent neural network (RNN), Graph convolutional network, 
Data fusion 
I. INTRODUCTION 
Alzheimer's detection (AD) is a neurological ailment with 
a huge worldwide effect that affects a large number of people 
over time. In addition, it causes dementia in almost all of 
its 
victims. [1]. Timely diagnosis of Alzheimer's detection (AD) 
is crucial for initiating therapy as soon as possible. This paves 
the way for patients to take advantage of current medicines 
and better control detection progression [2].

**Passage 18:**

> tection using neuroimaging data. However, 
there is a need for novel methods that can effectively integrate 
multimodal neuroimaging data to improve diagnostic 
accuracy and generalizability. TABLE I. STUDY SUMMERY OF LITERATURE REVIEW 
Literatu
re 
Review 
Algorithm Param
eters 
Research Gap 
[9] CNN, SVM, 
RF 
MMSE
, PET 
Lack of comparison with other 
AI-based models 
[10] MLP, DT, 
KNN 
CDR, 
EEG 
Limited evaluation on large 
datasets 
[11] CNN, GBDT, 
SVM 
CERA
D, 
fMRI 
Limited generalizability due to 
small sample sizes 
[12] Random 
Forest, ANN, 
SVM 
EEG, 
CSF 
Limited analysis of individual 
contributions of different 
features 
[13] DNN, RF, 
DT 
CSF, 
MRI 
Limited comparison with other 
traditional diagnostic methods 
[14] Deep 
learning, 
SVM, DT 
MMSE
, MRI 
Limited explanation of model 
decision-making processes 
[15] CNN, MLP, 
SVM 
PET, 
fMRI 
Limited evaluation of model 
interpretability 
[16] GBDT, 
KNN, DT 
CDR, 
EEG 
Limited analysis of individual 
contributions of different 
features 
[17] DNN, SVM, 
RF 
MMSE
, MRI 
Limited evaluation on multi-
modal datasets 
 
III.

**Passage 19:**

> curacy of 91.4% in classifying AD 
patients. C. Challenges and limitations: 
Despite the promising results of existing studies, there are 
several challenges and limitations that need to be addressed. Most current methods focus on s ingle-modal neuroimaging 
data, which may limit their diagnostic performance due to the 
lack of complementary information provided by different 
imaging modalities [15]. Additionally, the integration of 
multimodal neuroimaging data in a unified deep learning 
framework remains a challenging task due to differences in 
data types, scales, and dimensions [16]. Furthermore, the 
generalizability of the models to independent datasets and 
diverse populations is often not assessed, limiting their 
applicability in clinical settings [17].

**Passage 20:**

> ion 
technique, and their AD diagnosis accuracy i ncreased to 
88.2%. B. Multimodal neuroimaging studies: 
Combining multiple neuroimaging modalities has been 
shown to improve diagnostic performance. Zhang et al. [13] 
utilized sMRI, fMRI, and positron emission tomography 
(PET) data, applying a multimodal classification framework 
to achieve a classification accuracy of 92.1% in differentiating 
AD and MCI patients from healthy controls. In another study, 
Liu et al. [14] combined sMRI and FDG -PET data using a 
deep learning model with convolutional and recurrent ne ural 
networks, reporting an accuracy of 91.4% in classifying AD 
patients. C. Challenges and limitations: 
Despite the promising results of existing studies, there are 
several challenges and limitations that need to be addressed.

**Passage 21:**

> icity (92%). Results 
point to the efficacy of our suggested method in early 
Alzheimer's detection diagnosis. To dig further into the algorithm's efficiency, a battery of 
statistical tests were run. The testing showed that our proposed 
algorithm outperformed the state -of-the-art algorithms in all 
three categories (accuracy, sensitivity, and specificity) by a 
statistically significant margin (p 0.05). IEEE - 56998
14th ICCCNT IEEE Conference 
July 6-8, 2023 
IIT - Delhi, Delhi, India
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply. The results of our experiments support the use of our 
proposed algorithm for the early diagnosis of Alzheimer's 
detection. Moreover, they highlight the potential of AI-driven 
models to improve diagnostic accuracy and patient outcomes. TABLE II.

**Passage 22:**

> cision-making process. Furthermore, our algorithm can be 
integrated with existing diagnostic methods to develop a more 
comprehensive and effective approach to early Alzheimer's 
detection diagnosis. Finally, the long -term impact of early 
diagnosis on patient outcomes should be investigated to 
provide further evidence for the importance of accurate and 
timely diagnosis. R
EFERENCES 
[1] Jalilianhasanpour R, Beheshtian E, Sherbaf G et al (2019) Functional 
connectivity in neurodegenerative disorders: Alzheimer’s disease and 
frontotemporal dementia. Top Magn Reson Imaging 28(6):317–324 
[2] Liu, M., Cheng, D., Yan, W., & Liu, Y. (2018). Classificati on of 
Alzheimer's detection by combination of convolutional and recurrent 
neural networks using FDG -PET images. Frontiers in 
Neuroinformatics, 12, 35. 
[3]  Zhang, D., Wang, Y., Zhou, L., Yuan, H., & Shen, D. (2011).

**Passage 23:**

> e 
model hyperparameters to optimize its performance. A. Experimental Result: 
The current study involves experimental evaluation of the 
suggested algorithm for early Alzheimer's detection diagnosis. Methods included teaching and testing the algorithm using 
data from 500 patients' MRI scans and Mini -Mental State 
Examination scores. Two hundred and fifty people with 
Alzheimer's detection and the same number of healthy persons 
made up the sample. According to the results, the researchers' suggested 
algorithm achieved an AUC -ROC value of 0.96 along with 
high levels of accuracy (92%) and specificity (92%). Results 
point to the efficacy of our suggested method in early 
Alzheimer's detection diagnosis. To dig further into the algorithm's efficiency, a battery of 
statistical tests were run.

**Passage 24:**

> ted older adults. Journal of Cognitive 
Neuroscience, 19(9), 1498-1507. 
[25] Reitz, C., Brayne, C., & Mayeux, R. (2011). Epidemiology of 
Alzheimer detection. Nature Reviews Neurology, 7(3), 137-152. IEEE - 56998
14th ICCCNT IEEE Conference 
July 6-8, 2023 
IIT - Delhi, Delhi, India
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply.

</details>

---

## Nir et al. (2013) — Effectiveness of regional DTI measures in distinguishing Alzheimer's disease, MCI, and normal aging
_File: `Nir et al. - 2013 - Effectiveness of regional DTI measures in distinguishing Alzheimer's disease, MCI, and normal aging.pdf`_

1. **Yes**, diffusion MRI (DTI, DWI, etc.) was used. The paper explicitly mentions "diffusion-weighted images (DWI)" and "DTI volume with no diffusion sensitization," and the title references DTI.

2. **Processing steps** (in order):  
   - Align diffusion images to the average b₀ image (DTI volume with no diffusion sensitization) using **FSL eddy_correct** to correct for head motion and eddy current distortions.  
   - Remove non-brain tissue from diffusion-weighted images using **FSL Brain Extraction Tool (BET)**.  
   - Perform intensity inhomogeneity normalization using **MNInu_correcttool**.  
   - Align T1-weighted anatomical images to a standard brain template using **FSL flirt** with 6 degrees of freedom.  
   - Elastic registration of FA maps to the **ENIGMA-DTI template** (via **Leow et al., 2007**).  
   - Threshold FA maps at **FA ≥ 0.2** to include only highly anisotropic anatomy.  

3. **Software/tools explicitly named**:  
   - **FSL** (including `eddy_correct`, `flirt`, `BET`), **ROBEX**, **MNInu_correcttool**, **FreeSurfer**, and **Leow et al., 2007** (for elastic registration).  

4. **Reported parameters**:  
   - **b-values**: 1000 s/mm² (for diffusion-weighted images).  
   - **Number of directions**: 41 diffusion-weighted images (b=1000) + 5 b₀ images.  
   - **Voxel size**: T1-weighted images: 1.2 × 1.0 × 1.0 mm³; DWI: 2.7 × 2.7 × 2.7 mm³.  
   - **Degrees of freedom**: 6 (for linear alignment) and 9 (for EPI distortion correction).  

5. **Exact sentences from excerpts**:  
   - "mes were aligned to the average b₀ image (DTI volume with no diffusion sensitization) using the FSL eddy_correct tool [...] to correct for head motion and eddy current distortions."  
   - "Non-brain tissue was also removed from the diffusion-weighted images using the Brain Extraction Tool (BET) from FSL [...]".  
   - "Intensity inhomogeneity normalization using the MNInu_correcttool [...]".  
   - "T1-weighted anatomical image was linearly aligned to a standard brain template [...] using FSL flirt [...] with 6 degrees of freedom".  
   - "The resulting 3D deformation fields were then applied to the three diffusivity maps [...]".  
   - "Thresholded at FA ≥ 0.2 [...]".  

6. **Processing description completeness**:  
   The description is **complete** based on the provided text, as all explicitly stated steps and parameters are included. No missing steps are reported.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> analysis of diffusion images and voxelwise heri-
tability analysis: A pilot project of the ENIGMA-DTI working group. Neuroimage 81,
455– 469. Jenkinson, M., Bannister, P., Brady, M., Smith, S., 2002. Improved optimization for the ro-
bust and accurate linear registration and motion correction of brain images. Neuroimage 17 (2), 825– 841. K a n t a r c i ,K . ,J a c kJ r . ,C . R . ,X u ,Y . C . ,C a m p e a u ,N . G . ,O ' B r i e n ,P . C . ,S m i t h ,G . E . ,I v n i k ,R . J . ,B o e v e ,
B.F., Kokmen, E., Tangalos, E.G., Petersen, R.C., 2001. Mild cognitive impairment and
Alzheimer disease: regional diffusivity of water. Radiology 219 (1), 101–107. Kantarci, K., Senjem, M.L., Avula, R., Zhang, B., Samikoglu, A.R., Weigand, S.D., Przybelski,
S.A., Edmonson, H.A., Vemuri, P., Knopman, D.S., Boeve, B.F., Ivnik, R.J., Smith, G.E.,
Petersen, R.C., Jack, C.R., 2011.

**Passage 2:**

> mes were aligned to the average b
0
image (DTI volume with no diffusion sensitization) using the FSL
eddy_correct tool (www.fmrib.ox.ac.uk/fsl) to correct for head motion
and eddy current distortions. All extra-cerebral tissue was roughly re-
moved from the T1-weighted anatomical scans using a number of soft-
ware packages, primarily ROBEX, a robust automated brain extraction
program trained on manually “skull-stripped” MRI data (Iglesias et al.,
2011) and FreeSurfer ( Fischl et al., 2004 ). Skull-stripped volumes
were visually inspected, and the best one selected and sometimes fur-
ther manually edited. Anatomical scans subsequently underwent inten-
sity inhomogeneity normalization using the MNInu_correcttool (www.
bic.mni.mcgill.ca/software/). Non-brain tissue was also removed from
the diffusion-weighted images using the Brain Extraction Tool (BET)
from FSL ( Smith, 2002).

**Passage 3:**

> thology in Alzheimer's disease — a neuropathological study. Int. J. Geriatr. Psychiatry 20 (10), 919– 926. Smith, S.M., 2002. Fast robust automated brain extraction. Hum. Brain Mapp. 17 (3),
143– 155. Smith, S.M., Jenkinson, M., Johansen-Berg, H., Rueckert, D., Nichols, T.E., Mackay, C.E.,
Watkins, K.E., Ciccarelli, O., Cader, M.Z., Matthews, P.M., Behrens, T.E., 2006. Tract-
based spatial statistics: voxelwise analysis of multi-subject diffusion data. Neuroimage 31 (4), 1487– 1505. Song, S.K., Sun, S.W., Ju, W.K., Lin, S.J., Cross, A.H., Neufeld, A.H., 2003.Diffusion tensor im-
aging detects and differentiates axon and myelin degeneration in mouse optic nerve
after retinal ischemia. Neuroimage 20 (3), 1714–1722. Song, S.K., Yoshino, J., Le, T.Q., Lin, S.J., Sun, S.W., Cross, A.H., Armstrong, R.C., 2005.Demy-
elination increases radial diffusivity in corpus callosum of mouse brain.

**Passage 4:**

> ,d eZ u b i c a r a y ,G . I . ,
Meredith, M., Wright, M.J., Thompson, P.M., 2008. How many gradients are suf-
ﬁcient in high-angular resolution diffusion imaging (HARDI)? MICCAI CDMRI,
pp. 216 – 224. Zhan, L., Leow, A.D., Zhu, S., Baryshev, M., Toga, A.W., McMahon, K.L., de Zubicaray, G.I.,
Wright, M.J., Thompson, P.M., 2009. A novel measure of fractional anisotropy based
on the tensor distribution function. Med. Image Comput. Comput. Assist. Interv. 12
(Pt 1), 845– 852. Zhan, L., Leow, A.D., Jahanshad, N., Chiang, M.C., Barysheva, M., Lee, A.D., Toga, A.W.,
McMahon, K.L., de Zubicaray, G.I., Wright, M.J., Thompson, P.M., 2010. How does an-
gular resolution affect diffusion imaging measures? Neuroimage 49 (2), 1357–1371. Zhan, L., Leow, A.D., Aganj, I., Lenglet, C., Sapiro, G., Yacoub, E., Harel, N., Toga, A.W.,
Thompson, P.M., 2011.

**Passage 5:**

> 10),
1100–1106. Holmes, C.J., Hoge, R., Collins, L., Woods, R., Toga, A.W., Evans, A.C., 1998.Enhancement of
MR images using registration for signal averaging. J. Comput. Assist. Tomogr. 22,
324– 333. Hua, X., Leow, A.D., Lee, S., Klunder, A.D., Toga, A.W., Lepore, N., Chou, Y.Y., Brun, C.,
Chiang, M.C., Barysheva, M., Jack Jr., C.R., Bernstein, M.A., Britson, P.J., Ward, C.P.,
Whitwell, J.L., Borowski, B., Fleisher, A.S., Fox, N.C., Boyes, R.G., Barnes, J., Harvey, D.,
Kornak, J., Schuff, N., Boreta, L., Alexander, G.E., Weiner, M.W., Thompson, P.M.,
ADNI, 2008. 3D characterization of brain atrophy in Alzheimer's disease and mild
cognitive impairment using tensor-based morphometry. Neuroimage 41 (1), 19– 34. H u a ,X . ,L e e ,S . ,Y a n o v s k y ,I . ,L e o w ,A . D . ,C h o u ,Y . Y . ,H o ,A . J . ,G u t m a n ,B . ,T o g a ,A .

**Passage 6:**

> , M.A., Dyer, T.D., Almasy, L., Duggirala, R., Fox, P.T., Blangero, J., 2011. Blood
pressure and cerebral white matter share common genetic factors in Mexican
Americans. Hypertension 57 (2), 330– 335. Lee, J.E., Chung, M.K., Lazar, M., DuBray, M.B., Kim, J., Bigler, E.D., Lainhart, J.E., Alexander,
A.L., 2009. A study of diffusion tensor imaging by tissue-speci ﬁc, smoothing-
compensated voxel-based analysis. Neuroimage 44 (3), 870–883. Leow, A.D., Yanovsky, I., Chiang, M.C., Lee, A.D., Klunder, A.D., Lu, A., Becker, J.T., Davis,
S.W., Toga, A.W., Thompson, P.M., 2007. Statistical properties of Jacobian maps and
the realization of unbiased large-deformation nonlinear image registration. IEEE
Trans. Med. Imaging 26 (6), 822 – 832. Leow, A.D., Zhu, S., Zhan, L., McMahon, K., de Zubicaray, G.I., Meredith, M., Wright, M.J.,
Toga, A.W., Thompson, P.M., 2009. The tensor distribution function.

**Passage 7:**

> anova, R., Deibler, A.R., Burdette, J.H.,
Maldjian, J.A., Laurienti, P.J., 2008. Relating imaging indices of white matter integrity
and volume in healthy older adults. Cereb. Cortex 18 (2), 433
– 442. Iglesias, J.E., Liu, C.Y., Thompson, P.M., Tu, Z., 2011.Robust brain extraction across datasets
and comparison with publicly available methods. IEEE Trans. Med. Imaging 30 (9),
1617–1634. Jack Jr., C.R., Bernstein, M.A., Borowski, B.J., Gunter, J.L., Fox, N.C., Thompson, P.M., Schuff,
N., Krueger, G., Killiany, R.J., Decarli, C.S., Dale, A.M., Carmichael, O.W., Tosun, D.,
Weiner, M.W., 2010. Update on the magnetic resonance imaging core of the
Alzheimer's Disease Neuroimaging Initiative. Alzheimers Dement. 6 (3), 212–220. Jahanshad, N., Zhan, L., Bernstein, M.A., Borowski, B.J., Jack, C.R., Toga, A.W., Thompson,
P.M., 2010a.

**Passage 8:**

> ompson). 1 Many investigators within the ADNI contributed to the design and implementation of
ADNI and/or provided data, but most of them did not participate in the analysis or writing
of this report. A complete list of ADNI investigators may be found at:http://adni.loni.ucla.
edu/wp-content/uploads/how_to_apply/ADNI_Acknowledgement_List.pdf. 2213-1582 © 2013 The Authors. Published by Elsevier Inc.
http://dx.doi.org/10.1016/j.nicl.2013.07.006
Contents lists available at ScienceDirect
NeuroImage: Clinical
journal homepage: www.elsevier.com/locate/ynicl
Open access under CC BY-NC-ND license . Open access under CC BY-NC-ND license . MRI-based image analysis methods have long been used to track
structural atrophy of the aging brai n.

**Passage 9:**

> OIs, to obtain total summary measures of these regions. We were then able to calculate the average FA, MD, RD and AxD, within
the boundaries of each of the 43 ROIs for each subject ( Table 2).2
2.3.4. TBSS tract atlas ROI summary measures
Tract-based spatial statistics (TBSS) (Smith et al., 2006), provided in
the FSL software package ( http://www.fmrib.ox.ac.uk/fsl/), was also
performed according to protocols outlined by the ENIGMA-DTI group:
http://enigma.loni.ucla.edu/ongoing/dti-working-group/. All subjects'
corrected FA maps were linearly, then elastically registered ( Leow
et al., 2007) to the ENIGMA-DTI template in ICBM space. The resulting
3D deformation ﬁelds were then applied to the three diffusivity maps. All subjects' spatially normalized FA, MD, RD and AxD data were
projected onto the skeletonized ENIGMA-DTI template.

**Passage 10:**

> tion using the MNInu_correcttool (www.
bic.mni.mcgill.ca/software/). Non-brain tissue was also removed from
the diffusion-weighted images using the Brain Extraction Tool (BET)
from FSL ( Smith, 2002). To align data from different subjects into the
same 3D coordinate space, each T1-weighted anatomical image was lin-
early aligned to a standard brain template (the downsampled Colin27
(Holmes et al., 1998 ): 110 × 110 × 110, with 2 mm isotropic voxels)
using FSL ﬂirt (Jenkinson et al., 2002) with 6 degrees of freedom (dof)
to allow translations and rotations in 3D.

**Passage 11:**

> artin,
N . G . ,W r i g h t ,M . J . ,T o g a ,A . W . ,T h o m p s o n ,P . M . ,2 0 1 0 b .Genetic in ﬂuences on
brain asymmetry: a DTI study of 374 twi ns and siblings. Neuroimage 52 (2),
455– 469. Jahanshad, N., Kochunov, P.V., Sprooten, E., Mandl, R.C., Nichols, T.E., Almasy, L., Blangero,
J., Brouwer, R.M., Curran, J.E., de Zubicaray, G.I., Duggirala, R., Fox, P.T., Hong, L.E.,
Landman, B.A., Martin, N.G., McMahon, K.L., Medland, S.E., Mitchell, B.D., Olvera,
R.L., Peterson, C.P., Starr, J.M., Sussmann, J.E., Toga, A.W., Wardlaw, J.M., Wright,
M.J., Hulshoff Pol, H.E., Bastin, M.E., McIntosh, A.M., Deary, I.J., Thompson, P.M.,
Glahn, D.C., 2013. Multi-site genetic analysis of diffusion images and voxelwise heri-
tability analysis: A pilot project of the ENIGMA-DTI working group. Neuroimage 81,
455– 469. Jenkinson, M., Bannister, P., Brady, M., Smith, S., 2002.

**Passage 12:**

> i-
tially classify the two MCI subgroups. 2.2. MRI and DTI scanning
All subjects underwent whole-brain MRI scanning on 3 Tesla GE
Medical Systems scanners at 14 acquisition sites across North America. Anatomical T1-weighted SPGR (spoiled gradient echo) sequences
(256 × 256 matrix; voxel size = 1.2 × 1.0 × 1.0 mm 3;T I=4 0 0m s ;
TR = 6.98 ms; TE = 2.85 ms; ﬂip angle = 11°), and diffusion-
weighted images (DWI; 256 × 256 matrix; voxel size: 2.7 × 2.7 ×
2.7 mm3; TR = 9000 ms; scan time = 9 min; more imaging details
can be found at http://adni.loni.ucla.edu/wp-content/uploads/2010/
05/ADNI2_GE_3T_22.0_T2.pdf) were collected. 46 separate images
were acquired for each DTI scan: 5 T2-weighted images with no diffu-
sion sensitization (b 0 images) and 41 diffusion-weighted images
(b =1 0 0 0s / m m2).

**Passage 13:**

> nsampled Colin27
(Holmes et al., 1998 ): 110 × 110 × 110, with 2 mm isotropic voxels)
using FSL ﬂirt (Jenkinson et al., 2002) with 6 degrees of freedom (dof)
to allow translations and rotations in 3D. To correct for echo-planar
imaging (EPI) induced susceptibility artifacts, which can cause distor-
tions at tissue – ﬂuid interfaces, skull-stripped b
0 images were linearly
aligned (FSL ﬂirt, 9 dof) and then elastically registered to their respec-
tive T1-weighted structural scans using an inverse-consistent registra-
tion algorithm with a mutual information cost function ( Leow et al.,
2007) as described in (Jahanshad et al., 2010b). The resulting 3D defor-
mation ﬁelds were then applied to the remaining 41 DWI volumes prior
to estimating diffusion parameters.

**Passage 14:**

> n and spatial normalization
As t u d y - s p e c iﬁc minimal deformation template (MDT) ( Gutman
et al., 2012 ) was created using 29 cognitively healthy elderly control
(NC) spatially aligned FA maps. An MDT deviates, on average, the least
(in some metric) from the anatomy of the subjects, and can often im-
prove registration accuracy and statistical power (Gutman et al., 2012;
Lepore et al., 2007). The MDT was generated by creating an initial afﬁne
mean template from all 29 subjects, then registering all the aligned
individual scans to that mean using a ﬂuid registration ( Leow et al.,
2007) while regularizing the Jacobians ( Yanovsky et al., 2007 ). A new
mean was created from the registered scans; this process was iterated
several times.

**Passage 15:**

> 0_T2.pdf) were collected. 46 separate images
were acquired for each DTI scan: 5 T2-weighted images with no diffu-
sion sensitization (b 0 images) and 41 diffusion-weighted images
(b =1 0 0 0s / m m2). This protocol was chosen after conducting a de-
tailed comparison of several different DTI protocols, to optimize the
signal-to-noise ratio in a ﬁxed scan time ( Jahanshad et al., 2010a;
Zhan et al., in press). All T1-weighted MR and DWI images were checked
visually for quality assurance to exclude scans with excessive motion
and/or artifacts; all scans were included. 2.3. Image analysis
2.3.1. Preprocessing steps
For each subject, all raw DWI volumes were aligned to the average b
0
image (DTI volume with no diffusion sensitization) using the FSL
eddy_correct tool (www.fmrib.ox.ac.uk/fsl) to correct for head motion
and eddy current distortions.

**Passage 16:**

> an using a ﬂuid registration ( Leow et al.,
2007) while regularizing the Jacobians ( Yanovsky et al., 2007 ). A new
mean was created from the registered scans; this process was iterated
several times. Each subject's initial FA map was elastically registered to
the ﬁnal MDT and the resulting deformation ﬁelds were applied to the
3 diffusivity maps to align them to the same coordinate space. To ensure
white matter alignment across subjects, registered FA maps were
thresholded at FA N 0.2 to include only highly anisotropic anatomy and
the thresholded maps were elastically registered to the thresholded
MDT (FA N 0.2). Again, the resulting deformationﬁelds were applied to
all previously registered DTI ma ps.

**Passage 17:**

> an-
gular resolution affect diffusion imaging measures? Neuroimage 49 (2), 1357–1371. Zhan, L., Leow, A.D., Aganj, I., Lenglet, C., Sapiro, G., Yacoub, E., Harel, N., Toga, A.W.,
Thompson, P.M., 2011. Differential information content in staggered multiple shell
HARDI measured by the tensor distribution function. Proc. IEEE Int. Symp. Biomed. Imaging 305–309. Zhan, L., Jahanshad, N., Ennis, D.B., Jin, Y., Bernstein, M.A., Borowski, B.J., Jack Jr., C.R., Toga,
A.W., Leow, A.D., Thompson, P.M., 2012. Angular versus spatial resolution trade-offs
for diffusion imaging under time constraints. Hum. Brain Mapp. http://dx.doi.org/
10.1002/hbm.2209(in press, Epub ahead of print).

**Passage 18:**

> H., Wu, H.K., Jiang, X.X., 2006.Voxel-based
detection of white matter abnormalities in mild Alzheimer disease. Neurology 66
(12), 1845– 1849. Yanovsky, I., Thompson, P.M., Osher, S., Leow, A.D., 2007. Topology preserving log-
unbiased nonlinear image registration: theory and implementation. IEEE Conf. Comput. Vis. Pattern Recognit. 1– 8. Yoshiura, T., Mihara, F., Ogomori, K., Tanaka, A., Kaneko, K., Masuda, K., 2002. Diffusion
tensor in posterior cingulate gyrus: correlation with cognitive decline in Alzheimer's
disease. Neuroreport 13 (17), 2299– 2302. Zhan, L., Chiang, M.C., Barysheva, M., Toga, A . W . ,M c M a h o n ,K . L . ,d eZ u b i c a r a y ,G . I . ,
Meredith, M., Wright, M.J., Thompson, P.M., 2008. How many gradients are suf-
ﬁcient in high-angular resolution diffusion imaging (HARDI)? MICCAI CDMRI,
pp. 216 – 224.

**Passage 19:**

> ing core of the
Alzheimer's Disease Neuroimaging Initiative. Alzheimers Dement. 6 (3), 212–220. Jahanshad, N., Zhan, L., Bernstein, M.A., Borowski, B.J., Jack, C.R., Toga, A.W., Thompson,
P.M., 2010a. Diffusion tensor imaging in seven minutes: determining trade-offs
between spatial and directional resolution. Proc. IEEE Int. Symp. Biomed. Imaging
1161–1164. Jahanshad, N., Lee, A.D., Barysheva, M., McMahon, K.L., de Zubicaray, G.I., Martin,
N . G . ,W r i g h t ,M . J . ,T o g a ,A . W . ,T h o m p s o n ,P . M . ,2 0 1 0 b .Genetic in ﬂuences on
brain asymmetry: a DTI study of 374 twi ns and siblings. Neuroimage 52 (2),
455– 469.

**Passage 20:**

> unction ( Leow et al.,
2007) as described in (Jahanshad et al., 2010b). The resulting 3D defor-
mation ﬁelds were then applied to the remaining 41 DWI volumes prior
to estimating diffusion parameters. To account for the linear registration
of the DWI images to the structural T1-weighted scan, a corrected gra-
dient table was calculated. 2.3.2. DTI maps
A single diffusion tensor ( Basser et al., 1994 ), or ellipsoid, was
modeled at each voxel in the brain from the eddy- and EPI-corrected
DWI scans using FSL dtiﬁt, and scalar anisotropy and diffusivity maps
were obtained from the resulting diffusion tensor eigenvalues ( λ1, λ2,
λ3) which capture the length of the longest, middle, and shortest axes
of the ellipsoid.

**Passage 21:**

> The resulting
3D deformation ﬁelds were then applied to the three diffusivity maps. All subjects' spatially normalized FA, MD, RD and AxD data were
projected onto the skeletonized ENIGMA-DTI template. Mean anisotro-
py and diffusivity measures were calculated along the skeleton in the
same 43 ROIs ( Table 2). This type of analysis has been used previously
in both genetic studies and studies of disease to home in on associated
WM tracts (Kochunov et al., 2011; Jahanshad et al., 2013). 2.3.5. Template creation and spatial normalization
As t u d y - s p e c iﬁc minimal deformation template (MDT) ( Gutman
et al., 2012 ) was created using 29 cognitively healthy elderly control
(NC) spatially aligned FA maps.

**Passage 22:**

> n
the boundaries of the MDT thesholded at FA N 0.2. Prior studies have
thresholded FA values between 0.2 and 0.3 to successfully exclude
gray matter or CSF ( Wakana et al., 2005; Smith et al., 2006 ). As we
were studying a clinical population, we chose the more conservative
(lower) limit of the recommended FA threshold. We also only ran statis-
tics on voxels of the thresholded MDT present in all subject scans, as
some scans had a slightly cropped FOV. As such, we did not consider
the inferior parts of the cerebellum and brain stem. We ran random-effects regressions on the average anisotropy and
diffusivity measures within the 43 full ROIs, again covarying for age
and sex, testing for statistical effects of diagnosis (NC vs. MCI, or AD),
3 global clinical test scores, and post-hoc tests on ADNI-MEM and
ADNI-EF. We further tested and compared TBSS ROI measures.

**Passage 23:**

> E
Trans. Med. Imaging 26 (6), 822 – 832. Leow, A.D., Zhu, S., Zhan, L., McMahon, K., de Zubicaray, G.I., Meredith, M., Wright, M.J.,
Toga, A.W., Thompson, P.M., 2009. The tensor distribution function. Magn. Reson. Med. 61 (1), 205 – 214. Lepore, N., Brun, C., Pennec, X., Chou, Y.Y., Lopez, O.L., Aizenstein, H.J., Becker, J.T., Toga,
A.W., Thompson, P.M., 2007. Mean template for tensor-based morphometry using
deformation tensors. Med. Image Comput. Comput. Assist. Interv. 10 (Pt 2), 826– 833. Leung, K.K., Bartlett, J.W., Barnes, J., Manning, E.N., Ourselin, S., Fox, N.C., 2013. Cerebral
atrophy in mild cognitive impairment and Alzheimer disease: Rates and acceleration. Neurology 80 (7), 648– 654. Liu, Y., Spulber, G., Lehtimaki, K.K., Kononen, M., Hallikainen, I., Grohn, H., Kivipelto, M.,
Hallikainen, M., Vanninen, R., Soininen, H., 2011.

**Passage 24:**

> We
ﬁrst examined differences in DTI anisotropy and diffusivity measures be-
tween groups of cognitively healthy normal elderly controls (NC), MCI,
and AD patients in both voxel-based and ROI analyses. We also exam-
ined the association of anisotropy and diffusivity maps with widely
used clinical or cognitive ratings including the MMSE ( Folstein et al.,
1975), the “sum-of-boxes” clinical dementia rating (CDR-sob) ( Berg,
1988), and the Alzheimer's Disease Assessment Scale-Cognitive (ADAS-
cog) (Rosen et al., 1984). Finally, in a supplementary test, we compared
our ROI results to ROIs extracted along the skeleton from the widely used
tract-based spatial statistics (TBSS) method (Smith et al., 2006).

</details>

---

## Qiao et al. (2026) — A multi-view DTI feature fusion framework for enhanced diagnosis of Alzheimer’s disease
_File: `Qiao et al. - 2026 - A multi-view DTI feature fusion framework for enhanced diagnosis of Alzheimer’s disease.pdf`_

1. **Yes**, diffusion MRI (DTI) was used in this paper. The text explicitly mentions "DTI data" and terms like FA (Fractional Anisotropy) and MD (Mean Diffusivity) maps, which are standard in DTI.

2. **Processing steps** (in order):  
   - Fieldmap estimation for distortion correction using dual spin-echo images.  
   - Distortion-corrected B0 images used as a reference.  
   - Skull stripping using the Brain Extraction Tool (BET) with an intensity threshold of 0.3.  
   - Eddy currents and subject motion correction using the estimated fieldmap.  
   - Alignment and undistortion of images.  
   - Diffusion tensor fitting via linear least squares to calculate FA and MD maps.  
   - Nonlinear registration to a standard space (FMRIB58_FA_1mm template).  
   - Thresholding the mean FA skeleton (0.2) to create a binary mask.  

3. **Software/tools explicitly named**:  
   - FMRIB's Diffusion Toolbox (FDT)  
   - FMRIB Software Library (FSL)  
   - Brain Extraction Tool (BET)  
   - PyRadiomics toolkit  

4. **Reported parameters**:  
   - Intensity threshold for BET: **0.3**  
   - FA skeleton threshold: **0.2**  
   - Voxel size of final FA/MD maps: **182 × 218 × 182**  
   - Registration to FMRIB58_FA_1mm template (standard space).  

5. **Exact sentences from the excerpts**:  
   - "First, the fieldmap was estimated for distortion correction using the phase information from dual spin-echo images."  
   - "Skull stripping was performed using the Brain Extraction Tool (BET), with the intensity threshold set to 0.3 to obtain a complete brain mask."  
   - "Eddy currents and subject motion were simultaneously corrected using the estimated fieldmap."  
   - "All images were aligned and undistorted."  
   - "The FA maps reflect the degree of spatial displacement anisotropy... defined as the proportion of the anisotropic component relative to the total diffusion tensor."  
   - "We used the FMRIB58_FA standard template in the FSL software and transformed the target image to 1x1x1mm MNI152 space."  
   - "A threshold of 0.2 was applied to the mean FA skeleton image and resulted in a binary skeleton mask."  

6. **Processing description completeness**:  
   The processing steps are explicitly detailed in the excerpts, covering distortion correction, skull stripping, motion/eddy current correction, tensor fitting, registration, and mask creation. However, **parameters like b-values, number of diffusion directions, or specific acquisition details are not reported** in the text. Thus, the description is **complete as per the provided excerpts**, but some parameters may be missing.  

---  
**Note**: The excerpts do not mention b-values, number of directions, or other acquisition parameters explicitly.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> kinson et al., 2012 ); developed by the Oxford Analysis Group
in the UK. A standard processing pipeline was implemented for the
analysis of NIFTI – format images using FMRIB's Diffusion Toolbox
(FDT). First, the fieldmap was estimated for distortion correction using the
phase information from dual spin-echo images. Second, the distortion-
corrected B0 images (with a magnetic field gradient intensity value of
0) were used as a reference. Skull stripping was performed using the
Brain Extraction Tool (BET), with the intensity threshold set to
0.3 to obtain a complete brain mask. Third, eddy currents and subject
motion were simultaneously corrected using the estimated fieldmap. Fourth, all images were aligned and undistorted.

**Passage 2:**

> reshold set to
0.3 to obtain a complete brain mask. Third, eddy currents and subject
motion were simultaneously corrected using the estimated fieldmap. Fourth, all images were aligned and undistorted. Finally, microstruc-
tural analysis was conducted by fitting the diffusion tensor via the linear
least squares method to calculate FA and MD maps ( Viv ´o et al., 2024 ). This fitting process involves solving a system of equations that models
the relationship between the diffusion-weighted signals and the ele-
ments of the diffusion tensor for each voxel. A symmetric and positive
definite matrix was obtained which contained three eigenvalues ( λ
1
; λ
2
and λ
3
) associated eigenvectors. The eigenvectors reflect the diffusion
directions of water molecules. The eigenvalues represent the diffusion
tensor, with magnitudes indicating the extent of water molecule diffu-
sion in each direction.

**Passage 3:**

> mask ( Han et al., 2021 ), which removed the gray
matter and cerebrospinal fluid components and excluded the influence
of voxels with large inter-subject variability in the outer layer of the
cortex. Third, the skeleton mask was applied in the projection of FA onto
the skeleton which generated individual FA fiber skeleton maps. Forth,
the skeletonised FA images were fed into voxelwise statistics and ob-
tained significantly different voxels, which could be served as location
proposals. Then the corresponding voxels in the aligned FA images of
each individual were located and the FA values at these location pro-
posals were utilized to construct the voxel features from FA images. In
addition, the same pipeline was applied to MD images to extract dif-
ferential voxelwise features from MD images.

**Passage 4:**

> cation. Age, as a continuous variable, is presented as mean ±
standard deviation. Within each dataset, the homogeneity of variances
between the AD and NC groups was first assessed using Levene's test. Based on the results of Levene's test, which indicated a violation of the
homogeneity of variance assumption and given the imbalanced sample
sizes, Welch ’ s t -test was employed for pairwise comparisons between
groups ( Delacre et al., 2017 ). All tests were two-tailed, with the statis-
tical significance level set ( p < 0.05). Image preprocessing
The DTI data were preprocessed using the FMRIB Software Library
(FSL) ( Jenkinson et al., 2012 ); developed by the Oxford Analysis Group
in the UK. A standard processing pipeline was implemented for the
analysis of NIFTI – format images using FMRIB's Diffusion Toolbox
(FDT).

**Passage 5:**

> n. Med. Sci. 23 (3),
367 – 376 . Delacre, M., Lakens, D., Leys, C., 2017. Why psychologists should by default use Welch ’ s
t-test instead of Student ’ s t-test. Int Rev Soc Psychol 30 (1), 92 – 101 . Jenkinson, M., Beckmann, C.F., Behrens, T.E.J., Woolrich, M.W., Smith, S.M., 2012. FSL. Neuroimage 62 (2), 782 – 790 . Viv ´o, F., Solana, E., Calvi, A., Pareto, D., Sastre-Garriga, J., Tintor ´e, M., Montalban, X.,
Rovira,
`
A., Alberich, M., 2024. Microscopic fractional anisotropy outperforms
multiple sclerosis lesion assessment and clinical outcome associations over standard
fractional anisotropy tensor. Hum. Brain Mapp. 45 (6), e26706 . Litjens, G., Kooi, T., Bejnordi, B.E., Setio, A.A.A., Ciompi, F., Ghafoorian, M., van der
Laak, J.A.W.M., van Ginneken, B., S ´anchez, C.I., 2017. A survey on deep learning in
medical image analysis. Med. Image Anal. 42, 60 – 88 .

**Passage 6:**

> s to the common tem-
plate, ensuring alignment of all images with the standard brain space. Subsequently, we applied a non-linear registration algorithm to preserve
the image details within the brain. The final FA and MD maps were
denoted as I
FA
and I
MD
with size of 182 × 218 × 182. Multi-view representations construction
Voxel based features
The TBSS method was carried out for voxelwise statistical analysis of
the FA and MD data, which was sensitive, objective and interpretable for
multi-subject diffusion imaging ( Han et al., 2021 ). The brain structural
differences were computed and the spatial location distribution associ-
ated with the disorder was determined. The procedure is shown in Fig. 2 . First, the nonlinear registration was utilized to register all FA images
to a standard space.

**Passage 7:**

> otti, R., Amoroso, N., Diacono, D., Donvito, G., Lella, E., Monaco, A.,
Tangaro, S., Initiative, A.D.N., 2017. DTI measurements for Alzheimer ’ s
classification. Phys. Med. Biol. 62 (6), 2361 – 2375 . Smith, S.M., Jenkinson, M., Johansen-Berg, H., Rueckert, D., Nichols, T.E., Mackay, C.E.,
Watkins, K.E., Ciccarelli, O., Cader, M.Z., Matthews, P.M., Behrens, T.E., 2006. Tract-based spatial statistics: Voxelwise analysis of multi-subject diffusion data. Neuroimage 31 (4), 1487 – 1505 . Han, M., Goubran, M., Rabiei, P., de Ribaupierre, S., Mirzaei, F., Tyndall, A., Parrent, A. G., Peters, T.M., Khan, A.R., 2021. Individualized cortical parcellation based on
diffusion MRI tractography. Cereb. Cortex 31 (1), 538 – 553 . Wang, R., He, Q., Han, C., Wang, H., Shi, L., Che, Y., 2023. A deep learning framework
for identifying Alzheimer's disease using fMRI-based brain network. Front. Neurosci.

**Passage 8:**

> perspective: a diffusion MRI based connectome study. Sci. Rep. 10, 9121 . Xue, Y., Zhu, H., Neri, F., 2023. A feature selection approach based on NSGA-II with
ReliefF. Appl. Soft Comput. 135, 109987 . Weiner, M.W., Veitch, D.P., Aisen, P.S., Beckett, L.A., Cairns, N.J., Green, R.C.,
Harvey, D., Jack, C.R., Jagust, W., Morris, J.C., Petersen, R.C., Saykin, A.J., Shaw, L. M., Toga, A.W., Trojanowski, J.Q., 2017. The Alzheimer's Disease Neuroimaging
Initiative 3: continued innovation for clinical trial improvement. Alzheimers
Dement. 13 (5), 561 – 571 . Das, S.R., Ilesanmi, A., Wolk, D.A., Gee, J.C., 2024. Beyond macrostructure: is there a
role for radiomics analysis in neuroimaging? Magn. Reson. Med. Sci. 23 (3),
367 – 376 . Delacre, M., Lakens, D., Leys, C., 2017. Why psychologists should by default use Welch ’ s
t-test instead of Student ’ s t-test. Int Rev Soc Psychol 30 (1), 92 – 101 .

**Passage 9:**

> categorized into three groups: 101 patients with AD, 181
with MCI, and 145 NC. All imaging data underwent rigorous quality
control, and DTI scans were acquired using GE, Siemens, and Philips
scanners. Demographic analysis of the participants
Statistical analyses were performed using the Statistical Package for
the Social Sciences (SPSS)version 26.0 to assess the balance of age be-
tween the AD and NC groups across the two independent datasets
(ADNI-2 and ADNI-3), to ensure the reliability of subsequent model
classification. Age, as a continuous variable, is presented as mean ±
standard deviation. Within each dataset, the homogeneity of variances
between the AD and NC groups was first assessed using Levene's test.

**Passage 10:**

> re, Methodology. Shaoqi Wu: Software,
Methodology. Hao Shang: Software, Methodology, Conceptualization. Qi Yuan: Writing – review & editing, Software. Jiande Sun: Writing –
review & editing, Software. Ethics Approval
Not applicable
Declaration of Competing Interest
The authors declare that they have no known competing financial
interests or personal relationships that could have appeared to influence
the work reported in this paper. Acknowledgement
This work was supported by the Jinan City-School Integration
Development Strategic Engineering Project(JNSX2025010). Appendix A. Supplementary data
Supplementary data to this article can be found online at https://doi.
org/10.1016/j.neuroscience.2026.01.024 . References
Sheng, J., Wang, L., Cheng, H., Zhang, Q., Zhou, R., Shi, Y., 2021. Strategies for
multivariate analyses of imaging genetics study in Alzheimer's disease. Neurosci. Lett.

**Passage 11:**

> al location distribution associ-
ated with the disorder was determined. The procedure is shown in Fig. 2 . First, the nonlinear registration was utilized to register all FA images
to a standard space. We used the FMRIB58_FA standard template in the
FSL software and transformed the target image to 1x1x1mm MNI152
space. Second, the white matter skeleton was computed by averaging all
FA images to obtain the mean FA skeleton, where the skeleton voxels
had higher FA values compared to adjacent white matter voxels. A
threshold of 0.2 was applied to the mean FA skeleton image and resulted
a binary skeleton mask ( Han et al., 2021 ), which removed the gray
matter and cerebrospinal fluid components and excluded the influence
of voxels with large inter-subject variability in the outer layer of the
cortex.

**Passage 12:**

>   λ
3
)
2
+ ( λ
3
  λ
1
)
2
λ
2
1
+ λ
2
2
+ λ
2
3
√
(1)
The MD maps represented the average displacement of molecules
and described the average diffusion coefficient of water molecules
within a voxel. It was defined as the average of the three eigenvalues and
computed by:
MD =
λ
1
+ λ
2
+ λ
3
3
(2)
After diffusion tensor fitting, FA and MD images of each subject were
registered to a standard space with FMRIB58_FA_1mm template using
the linear and non-linear registration combination algorithms to ensure
their comparability. Specifically, we initially utilized the linear image
registration in FLIRT tool to register the images to the common tem-
plate, ensuring alignment of all images with the standard brain space. Subsequently, we applied a non-linear registration algorithm to preserve
the image details within the brain.

**Passage 13:**

> d local
redistribution rules. This approach maintains detailed spatial informa-
tion and facilitates the localization of brain regions that exert the
strongest influence on the classification outcome. The LRP- ε rule, with a
stabilizer set to ε = 1 × 10
 
⁶ , was employed to ensure numerical stability
during the backward propagation. For each input FA or MD volume, the
relevance scores pertaining to a specific diagnostic category (AD, MCI,
or NC) were propagated backward to generate a three-dimensional
Fig. 2. TBSS for Voxel-Based Feature Extraction in Alzheimer ’ s Disease Research. This workflow illustrates the TBSS procedure for analyzing FA data, including
spatial registration, template construction, skeleton generation, and voxelwise feature extraction. Fig. 3. Architecture of the Residual Block-Based 3D-CNN Model for Deep Feature Extraction in AD Diagnosis.

**Passage 14:**

> hout permission. Copyright ©2026. Elsevier Inc. All rights reserved. Neuroscience 597 (2026) 1–12
11
existing institutional review board (IRB) approvals from their respective
originating institutions. Ethical oversight was provided by the ADNI IRB
(details at https://adni.loni.usc.edu/wp-content/uploads/ how_to_ap-
ply/ADNI_Acknowledgement_List.pdf). CRediT authorship contribution statement
Jianping Qiao: Writing – original draft, Validation, Supervision,
Software, Methodology, Investigation, Formal analysis, Conceptualiza-
tion. Guangchao Zhou: Software, Methodology. Shaoqi Wu: Software,
Methodology. Hao Shang: Software, Methodology, Conceptualization. Qi Yuan: Writing – review & editing, Software. Jiande Sun: Writing –
review & editing, Software.

**Passage 15:**

> Engineering, Shandong Normal University, Jinan, China. E-mail addresses: qiaojianping@sdnu.edu.cn (J. Qiao), yuanqi@sdnu.edu.cn (Q. Yuan), jiandesun@hotmail.com (J. Sun). 1
ORCID: 0000-0001-8910-7813. Contents lists available at ScienceDirect
Neuroscience
journal homepage: www.else vier.com/loc ate/nsc
https://doi.org/10.1016/j.neuroscience.2026.01.024
Received 15 July 2025; Accepted 18 January 2026
Downloaded for Brett Piggott (bapiggott@oakland.edu) at Oakland University from ClinicalKey.com by Elsevier on February 
15, 2026. For personal use only. No other uses without permission. Copyright ©2026. Elsevier Inc. All rights reserved.

**Passage 16:**

> Ours 101AD,181MCI Multiview features fusion Ensemble Classifier 0.933 0.945 0.911 0.946
Table 5
Ablation results of different features. Tasks Features Performance
ACC SEN SPE AUC F1
Score
Kappa
AD vs. NC
SCN 0.741 0.733 0.745 0.725 0.756 0.756
Radiomics 0.761 0.684 0.766 0.699 0.812 0.774
3D-CNN 0.829 0.762 0.876 0.824 0.816 0.795
TBSS 0.867 0.858 0.711 0.851 0.849 0.837
SCN +
Radiomics
0.831 0.832 0.779 0.777 0.811 0.794
SCN +
Radiomics +
3D-CNN
0.887 0.851 0.910 0.881 0.862 0.844
SCN +
Radiomics +
3D-CNN +
TBSS
0.976 0.980 0.972 0.964 0.971 0.950
MCI
vs.

**Passage 17:**

> lassification task. Subsequently, principal component analysis (PCA) was performed on
Fig. 4. Weighted structural connectivity matrices for AD analysis. (a) FA-weighted matrix; (b) MD-weighted matrix. Both matrices are 90 × 90 in dimension, with
row and column coordinates corresponding to brain regions parcellated by the AAL atlas. The matrices were constructed based on deterministic tractography, and the
color of each cell represents the mean weight of the connection between two brain regions. (a) FA matrix: weights are derived from FA values of white matter fiber
tracts, with colors ranging from dark blue (0) to light yellow (2 × 10
  3
). FA reflects the microstructural integrity of white matter fibers. (b) MD matrix: weights are
derived from MD values of white matter fiber tracts, with colors ranging from dark blue (0) to yellow-green (0.7).

**Passage 18:**

> location pro-
posals were utilized to construct the voxel features from FA images. In
addition, the same pipeline was applied to MD images to extract dif-
ferential voxelwise features from MD images. Therefore, the voxel fea-
tures F
v
based on TBSS could be described by:
F
v
= TBSS ( I
FA
) ⊕ TBSS ( I
MD
) (3)
where ⊕ presented the concatenation operation. Deep 3D-CNN based feature
Traditional two-dimensional convolutional neural networks (2D-
CNN) have been applied in AD classification ( Marzban et al., 2020 ). However, a fundamental limitation of this approach arises when pro-
cessing three-dimensional diffusion tensor imaging (DTI) data, such as
fractional anisotropy (FA) and mean diffusivity (MD) maps.

**Passage 19:**

> each pair of re-
gions, resulting in weighted 90 × 90 structural connectivity matrices. As
these matrices are symmetric, only the upper triangular elements were
extracted to avoid feature redundancy. Therefore, the tractography-
based features F
t
are obtained by:
F
t
= ( w
FA
⋅ M
T
) ⊕ ( w
MD
⋅ M
T
) (4)
Where M
T
represents the structural connectivity matrix, w
FA
represents
the weights from FA images, and w
MD
represents the weights from MD
images. The resulting matrices are visualized in Fig. 4 . Fig. 4(a) shows the FA-
weighted matrix, which represents the mean FA weights of connections
between brain regions. FA reflects the microstructural integrity of white
matter tracts. The blue areas in the figure represent lower weight values,
corresponding to connections between brain regions with poorer
microstructural integrity. Fig.

**Passage 20:**

> eimer's disease, the
microstructural alterations revealed by such decreases in FA and in-
creases in MD often serve as imaging biomarkers for the spread of early
pathological processes in the disease. Radiomics based features
Radiomics features were extracted from the FA and MD maps uti-
lizing the PyRadiomics toolkit, an open-source Python package ( van
Griethuysen et al., 2017 ). A comprehensive set of features was derived
from the original images, encompassing shape, intensity, and texture
features, as well as from images transformed using wavelet and Lap-
lacian of Gaussian (LoG) filters. The initial extraction resulted in a high-dimensional feature vector
per subject. To mitigate overfitting and identify the most predictive
features, a two-step dimensionality reduction strategy was employed.

**Passage 21:**

> ted from seed voxels along both di-
rections of the local fiber orientation until meeting termination criteria,
which were defined as a maximum tracking angle of 45 degrees and an
FA threshold of 0.2. Network nodes were defined using the Automated Anatomical La-
beling (AAL) atlas, which parcellates the brain into 90 cortical and
subcortical regions (cerebellum excluded) ( Luppi et al., 2021 ). edges
between nodes were established if at least three fiber bundles were
reconstructed between two regions. The connection weight was defined
as the mean FA or MD value along the fibers between each pair of re-
gions, resulting in weighted 90 × 90 structural connectivity matrices. As
these matrices are symmetric, only the upper triangular elements were
extracted to avoid feature redundancy.

**Passage 22:**

> features of white matter fiber tract impairment in AD. (For interpretation of the
references to colour in this figure legend, the reader is referred to the web version of this article.)
J. Qiao et al. Downloaded for Brett Piggott (bapiggott@oakland.edu) at Oakland University from ClinicalKey.com by Elsevier on February 
15, 2026. For personal use only. No other uses without permission. Copyright ©2026. Elsevier Inc. All rights reserved. Neuroscience 597 (2026) 1–12
6
the LASSO-selected features to further reduce dimensionality and
address multicollinearity. Principal components were retained until the
cumulative variance reached 95%, resulting in the selection of the first
30 components.

**Passage 23:**

> marker in brain network studies. In
particular, in AD, abnormal brain networks are associated with cogni-
tive impairment, providing objective indicators for clinical diagnosis
( Zhang et al., 2024 ). Brain network analysis simplifies the brain's com-
plex architecture while preserving its connectivity, which is why we
constructed a structural connectivity network using white matter fiber
tracts derived from DTI data. We applied a deterministic fiber tracking algorithm to trace neural
pathways. Fiber propagation started from seed voxels along both di-
rections of the local fiber orientation until meeting termination criteria,
which were defined as a maximum tracking angle of 45 degrees and an
FA threshold of 0.2.

**Passage 24:**

> eigenvectors reflect the diffusion
directions of water molecules. The eigenvalues represent the diffusion
tensor, with magnitudes indicating the extent of water molecule diffu-
sion in each direction. The primary eigenvalue λ
1
represents axial
diffusivity, which indicated the rate of diffusion along the fiber direc-
tion. Specifically, FA maps reflect the degree of spatial displacement
anisotropy and are defined as the proportion of the anisotropic
component relative to the total diffusion tensor, with values ranging
between 0 and 1. FA is computed as:
FA =
̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅ ̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅ ̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅ ̅̅̅̅̅ ̅
1
2
( λ
1
  λ
2
)
2
+ ( λ
2
  λ
3
)
2
+ ( λ
3
  λ
1
)
2
λ
2
1
+ λ
2
2
+ λ
2
3
√
(1)
The MD maps represented the average displacement of molecules
and described the average diffusion coefficient of water molecules
within a voxel.

</details>

---

## Resnet-53 for Alzheimer-s Disease Detection from MRI Images and Analysis with SVM Tuning with Hyper Optimization Technique
_File: `Resnet-53 for Alzheimer-s Disease Detection from MRI Images and Analysis with SVM Tuning with Hyper Optimization Technique.pdf`_

1. **Was diffusion MRI (DTI, dMRI, DWI, or similar) used in this paper?**  
   **NO DIFFUSION MRI PROCESSING FOUND**  

2. **What processing steps were applied to the diffusion images?**  
   Not applicable (no diffusion MRI content found).  

3. **What software or tools are explicitly named for processing?**  
   Not applicable (no diffusion MRI content found).  

4. **What acquisition or processing parameters are explicitly reported?**  
   Not applicable (no diffusion MRI content found).  

5. **Copy the exact sentences from the excerpts that describe the processing.**  
   Not applicable (no diffusion MRI content found).  

6. **Is the processing description complete, or does it appear incomplete/missing?**  
   Not applicable (no diffusion MRI content found).

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> y 
detection and prevention of AD, according to Rizwan Khan 
et al. [20]. 315 T1 -weighted MRI pictures that were taken 
from the ADNI database made up the dataset that was used 
in the investigation. The MRI scans' 3D voxel data is 
subjected to GM extraction; the resultant GM slices are then 
utilized to train VGG architectures. Using pre -trained VGG 
16 & VGG 19, which were trained on the ImageNet 
database, a layer -wise transfer learning strategy is 
implemented, incorporating step -wise block freezing. Tools 
like the SPM12 are used for operations including 
segmentation, normalization, registration, and skull 
stripping. The designs VGG 16 and VGG 19 are used since 
their performance in feature extraction and image 
processing applications has been demonstrated. Leveraging 
the weights of the pre-trained.

**Passage 2:**

> use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply. Fig 1. Accuracy Comparison among different Authors with 
different models. IV. PROPOSED METHODOLOGY 
Recommended approach customizes pre -trained model 
"ResNet50V2" to extract illness features. The model that 
was suggested does not feed the input images straight to the 
CNN. Instead, it customizes a few processes, which will be 
explained below. Input Pre -processing: It consists of two steps: 1. Zero 
Centring and 2. Adaptive Filteration. A. Zero Centring 
In the context of Alzheimer's disease image analysis, zero 
centring can be particularly beneficial as it helps the deep 
learning model focus on the subtle structural changes and 
abnormalities within the brain rather than being distracted 
by global intensity variations.

**Passage 3:**

> essing techniques such as intensity 
normalization and registration were applied to the MRI 
scans. Due to the little dataset, data augmentation is utilized 
for enhancing the classified performances. Transfer learning 
from ImageNet datasets, pre -training a ResNet -18 
Methodology, was recommended to avoid overfitting and 
leverage knowledge from natural images. The fully -
connected layer of the ResNet -18 Methodology was 
adjusted for AD detection, with a higher learning rate for 
weight and bias. To adapt ResNet -18 for 3D MRI scans, 2D 
filters were extended to 3D filters, and the remaining layers 
were adjusted accordingly. TABLE I. MERITS AND DEMERIT ANALYSIS ON DIFFERENT APPROACHES 
Author Algorithm Merits Demerits Accuracy 
Utkarsh 
Sarawgi et 
al 
Ensemble 
methods 
It can 
effectively 
identify 
spontaneous 
speech.

**Passage 4:**

> in normal clinics for 
objective evaluation of AD. The Inception v3 network 
framework is used in two -stage transfer learning, including 
pre-training using the ImageNet data set and ADNI 
database. Three -dimensional images are reorganized into 
ensemble learning and a two -dimensional sets for 
information augmentation are used to increase training 
precision. It is examined how well initial training variables 
for Tc-99m-ECD SPECT pictures can differentiate between 
AD and NC. The impact append on the little size in pre -
training data from F -18-FDG PET images on model 
performance is analyzed. A deep learning algorithm utilising 
SPECT ECD perfusion pictures has been suggested, with 
pre-training on PET FDG metabolic imaging, shows 
increased sensitivity and accuracy  in differentiating AD 
from NC.

**Passage 5:**

> ). An 
Alzheimer’s disease classification method using fusion of features 
from brain Magnetic Resonance Image transforms and deep 
convolutional networks. In Healthcare Analytics (Vol. 4, p. 100223). Elsevier BV. https://doi.org/10.1016/j.health.2023.100223 
[17] P. Dedeepya, P. Chiranjeevi, V. Narasimha, V. Shariff, J. Ranjith and 
J. V. N. Ramesh, "Image Recognition and Similarity Retrieval with 
Convolutional Neural Networks," 2023 2nd International Conference 
on Automation, Computing and Renewable Systems (ICACRS) , 
Pudukkottai, India, 2023, pp. 709 -716, doi: 
10.1109/ICACRS58579.2023.10404664.  
[18] Islam, Md. M., Barua, P., Rahman, M., Ahammed, T., Akter, L., & 
Uddin, J. (2023). Transfer learning architectures with fine -tuning for 
brain tumor classification using magnetic resonance imaging. In 
Healthcare Analytics (Vol. 4, p. 100270).

**Passage 6:**

> be particularly beneficial as it helps the deep 
learning model focus on the subtle structural changes and 
abnormalities within the brain rather than being distracted 
by global intensity variations. The application of deep 
learning has revolutionized field of AD diagnosis and 
assessment, enabling highly effective analysis of medical 
imaging data. B. Adaptive Filter Design Using Integration Approach: 
Adaptive filtering has become a basic  image processing and 
signal analysis, gaining widespread recognition for its 
remarkable capability to effectively manage dynamic signal 
characteristics and mitigate the impact of diverse noise 
patterns. A novel approach that has shown significant 
promise in this domain is the integration of Gaussian and 
bilateral filtering techniques.

**Passage 7:**

> similar geometrical properties and only need modest 
adjustments when applied to another modality. The 
outcomes show that good performance may be achieved 
even with tiny datasets and few ROI slices. When compared 
to existing methods, the proposed methodology achieves 
good accuracy scores using a shallow convolutional 
network. Atif Mehmood et al [2] focuses on the early detection 
of MCI using MRI in the treatment of dementia, particularly 
AD. Deep learning architecture, The lack of labelled 
datasets for the model's training is addressed by using 
particular techniques, such as layer -wise transfer for 
learning and tissue segmentation. The study draws on 
information collected in the ADNI database, which includes 
85 NC clients, 70 EMCI patients, 70 LMCI patients, & 75 
AD patients. To isolate GM tissue from brain pictures and 
help in diagnosis, tissue segmentation is done.

**Passage 8:**

> d, T., Akter, L., & 
Uddin, J. (2023). Transfer learning architectures with fine -tuning for 
brain tumor classification using magnetic resonance imaging. In 
Healthcare Analytics (Vol. 4, p. 100270). Elsevier BV. 
https://doi.org/10.1016/j.health.2023.100270 
[19] Shastry, K. A. (2023). An ensemble nearest neighbor boosting 
technique for prediction of Parkinson’s disease. In Healthcare 
Analytics (Vol. 3, p. 100181). Elsevier BV. 
https://doi.org/10.1016/j.health.2023.100181 
[20] Khan R, Akbar S, Mehmood A, Shahid F, Munir K, Ilyas N, Asif M, 
Zheng Z. A transfer learning approach for multiclass classification of 
Alzheimer's disease using MRI images. Front Neurosci. 2023 Jan 
9;16:1050777. doi: 10.3389/fnins.2022.1050777. PMID: 36699527; 
PMCID: PMC9869687. 
[21]  N. S. K. M. K. Tirumanadham, T. S, and S.

**Passage 9:**

> t possible to continuously build precise and 
accessible diagnostic tools for Alzheimer's disease. The 
results provide promise for early therapeutic interventions, 
better patient outcomes, and care. Tested and trained using 
MRI and PET scans associated with Alzheimer's disease, the 
suggested ResNet50 model also demonstrates significance 
in the categorization of medical images. FUTURE WORK 
Subsequent investigations will examine the efficacy of pre -
trained ResNet50 classification models on other datasets, 
including as real-time MRI and PET data, as well as OASIS 
data. T2 weighted MRI and PET scans will be used to give 
qualitative transfer learning knowledge. In addition, various 
network models and neuroimaging approaches will be used 
to study yoga and meditation practices.

**Passage 10:**

> MRI and PET scans will be used to give 
qualitative transfer learning knowledge. In addition, various 
network models and neuroimaging approaches will be used 
to study yoga and meditation practices. The classification of 
Alzheimer's disease (AD) and its possible overlap with other 
neurological conditions such as multiple sclerosis, 
Parkinson's disease, dementia, migraines, and epilepsy are 
the main topics of this study. Neurological problems are 
investigated using electroencephalogram (EEG) signals and 
magnetic resonance imaging (MR) images. REFERENCES 
[1] Aderghal, K., Afdel, K., Benois -Pineau, J., & Catheline, G. (2020). Improving Alzheimer’s stage categorization with Convolutional 
Neural Network using transfer learning and different magnetic 
resonance imaging modalities.

**Passage 11:**

> result, feature learning may become more efficient and 
discriminative. Brain biomarkers can be used to classify 
patients using information from multi -modal imaging, such as 
DTI and structural MRI. CNN techniques have been shown to 
be effective tools for enhancing image -based classification 
recently. In order to reduce residual errors, the process begins 
with the extraction of features using ResNet, with a preference 
for skipping connections. ResNet50 was selected because to its 
outstanding picture analysis and classification skills. The 
model's parameters are adjusted in accordance with the 
difference between the predicted and actual class scores. The 
SVM model is fine -tuned in the final layer, particularly with 
regard to Alzheimer's detection for binary and multiclass 
assignments.

**Passage 12:**

> Resnet-53 for Alzheimer’s Disease Detection from 
MRI Images and Analysis with SVM Tuning with 
Hyper Optimization Technique 
                 
1st Rama Lakshmi B 
Research scholar 
 Department of Computer Science and Engineering, 
GITAM School of Technology 
GITAM (Deemed-to-be University)Visakhapatnam, AP, India 
ramalakshmi.boyapati@gmail.com 
ORCID:0000-0001-7041-2260 
2nd Radhika Y 
Professor 
 Department of Computer Science and Engineering 
GITAM School of Technology 
GITAM (Deemed-to-be University)Visakhapatnam,  AP, India 
ryalavar@gitam.edu 
ORCID: 0000-0001-6898-2467
   
 
ABSTRACT—The research utilizes a dataset containing 
biomarkers and cognitive traits, utilizing advanced machine 
learning algorithms for early detection and accurate diagnosis 
of Alzheimer's disease globally.

**Passage 13:**

> urkar, A. v., Rusinek, H., Chen, J., Zhang, B., Zhu, W., 
Fernandez-Granda, C., & Razavian, N. (2022). Generalizable deep 
learning model for early Alzheimer’s disease detection from structural 
MRIs. Scientific Reports, 12(1). https://doi.org/10.1038/s41598 -022-
20674-x   
Proceedings of the International Conference on Sustainable Expert Systems (ICSES-2024)
IEEE Xplore Part Number: CFP24VS6-ART; ISBN: 979-8-3315-4036-4
979-8-3315-4036-4/24/$31.00 ©2024 IEEE 1072
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply.

**Passage 14:**

> arning algorithm utilising 
SPECT ECD perfusion pictures has been suggested, with 
pre-training on PET FDG metabolic imaging, shows 
increased sensitivity and accuracy  in differentiating AD 
from NC. Amir Ebrahimi et al [6] emphasises applying the 
ResNet-18 Methodology on MRI to identify Alzheimer's 
disease (AD). For AD identification in earlier investigations, 
2D CNNs were applied to 2D image slices of 3D MRI 
images. To transfer information from 2D to 3D datasets, the 
proposed technique uses transfer learning in 3D CNNs. The 
dataset was derived from the ADNI contains MRI scans. Image pre -processing techniques such as intensity 
normalization and registration were applied to the MRI 
scans. Due to the little dataset, data augmentation is utilized 
for enhancing the classified performances.

**Passage 15:**

> rs a thorough and dependable early 
detection tool. Keywords— Neuro-Imaging, Gaussian Filter, Bilateral Filter, 
Adaptive Filter, Hyperopt, regularization, , Hyperplane, Bayesian 
Optimization CNN. I. INTRODUCTION 
Many neurological diseases, such as dementia, affect a 
significant percentage of people worldwide. [11] After the 
age of 60, Alzheimer's patients begin to exhibit increasingly 
pronounced symptoms. However, in a  few instances, the 
symptoms may appear early (30 –50 years old) due to 
specific gene anomalies. The recommended approach 
facilitates timely therapeutic therapy and helps in early 
detection and prevention of AD, according to Rizwan Khan 
et al. [20]. 315 T1 -weighted MRI pictures that were taken 
from the ADNI database made up the dataset that was used 
in the investigation.

**Passage 16:**

> stainable Expert Systems (ICSES-2024)
IEEE Xplore Part Number: CFP24VS6-ART; ISBN: 979-8-3315-4036-4
979-8-3315-4036-4/24/$31.00 ©2024 IEEE 1071
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply. 
[8] Raju, M., Thirupalani, M., Vidhyabharathi, S., &Thilagavathi, S. 
(2021). Deep Learning Based Multilevel Classification of 
Alzheimer’s Disease using MRI Scans. IOP Conference Series: 
Materials Science and Engineering, 1084(1), 012017. 
https://doi.org/10.1088/1757-899x/1084/1/012017 
[9] Khan R, Akbar S, Mehmood A, Shahid F, Munir K, Ilyas N, Asif M, 
Zheng Z. A transfer learning approach for multiclass classification of 
Alzheimer's disease using MRI images. Front Neurosci. 2023 Jan 
9;16:1050777. doi: 10.3389/fnins.2022.1050777.

**Passage 17:**

> . Image 
processing techniques may not account for the dynamic 
nature of the disease over time. Below section discusses the 
popular filters for performing segmentation on images. II. EASE OF USE 
A. Bilateral filter  
Combining weights from the spatial kernel and the range 
kernel to calculate the final weight for each pixel in the 
neighbourhood. Pixels with similar intensity or colour 
values are given higher weights.  [3] The weights for each 
pixel are established by combining the range and spatial 
kernels.

**Passage 18:**

> ach pixel in the 
neighbourhood. Pixels with similar intensity or colour 
values are given higher weights.  [3] The weights for each 
pixel are established by combining the range and spatial 
kernels. It specifies a range kernel that weighs pixels 
Proceedings of the International Conference on Sustainable Expert Systems (ICSES-2024)
IEEE Xplore Part Number: CFP24VS6-ART; ISBN: 979-8-3315-4036-4
979-8-3315-4036-4/24/$31.00 ©2024 IEEE 1065
2024 4th International Conference on Sustainable Expert Systems (ICSES) | 979-8-3315-4036-4/24/$31.00 ©2024 IEEE | DOI: 10.1109/ICSES63445.2024.10763183
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply. 
according to how similar their values are. Pixels with 
comparable color or intensity values are assigned larger 
weights.

**Passage 19:**

> stripping. The designs VGG 16 and VGG 19 are used since 
their performance in feature extraction and image 
processing applications has been demonstrated. Leveraging 
the weights of the pre-trained. Methodologies from the ImageNet database is achieved 
by transfer learning. [18] For multi-class classification, fresh 
fully connected layers are integrated with the frozen 
convolutional base using the softmax function and 
categorical cross -entropy loss. Threshold -based 
segmentation methods require choosing appropriate 
threshold values. Selecting the correct thresholds can be 
subjective and may require domain expertise. Image 
processing techniques may not account for the dynamic 
nature of the disease over time. Below section discusses the 
popular filters for performing segmentation on images. II. EASE OF USE 
A.

**Passage 20:**

> n the ADNI database, which includes 
85 NC clients, 70 EMCI patients, 70 LMCI patients, & 75 
AD patients. To isolate GM tissue from brain pictures and 
help in diagnosis, tissue segmentation is done. Analysis of 
comparative research shows that the suggested model 
performs better when it comes of testing accuracy than 
current state-of-the-art models. Liuqing Yang et al [3] DL methodologies in 
distinguishing related patients effected with AD, MCI, or no 
signs of dementia were seen utilising base brain MRI 
results. From structural MRI scans, DL algorithms extract 
characteristics that are then coupled to additional 
biomarkers to form an AD prognostic hallmark. The AD 
predictive signature offers enrichment options in AD 
clinical trial planning and assists in comprehending patient 
variability within a research cohort.

**Passage 21:**

> g 
models, showcasing generalizability through a task -
independent feature space. To support deductive methods 
for AD classified & validation scores, the architecture 
makes use of domain knowledge. For MMSE score 
regression and AD classification,  the system uses 
specialised ANN  having time properties. The provided 
method illustrates the value of utilising domain expertise 
and deductive transference for AD diagnosis and severity 
evaluation, as well as the possibility of multimodal 
techniques. Yu-Ching NI et al [5] focuses on using Tc -99m-ECD 
SPECT brain perfusion pictures in normal clinics for 
objective evaluation of AD. The Inception v3 network 
framework is used in two -stage transfer learning, including 
pre-training using the ImageNet data set and ADNI 
database.

**Passage 22:**

> difference between the predicted and actual class scores. The 
SVM model is fine -tuned in the final layer, particularly with 
regard to Alzheimer's detection for binary and multiclass 
assignments. In order to improve the model's performance on 
the validation set, Bayesian optimization using Hyperopt 
methodically investigates the hyperparameter space by 
improving parameters like regularization and kernel selection. In this  proposed work, we have  used transfer learning with 
Resnet-Based Image Analysis with SVM Tuning to conduct 
different classification of Alzheimer disease. These kinds of 
representations are learnable from the data using deep 
learning algorithms. The SVM model is fine -tuned in the final 
layer, particularly with regard to Alzheimer's disease detection 
for multiple lables.

**Passage 23:**

> ROI, such as the hippocampus 
area, employing CNN for automated categorization of brain 
images. LeNet -like network architecture is employed, and 
models are constructed and fused for classifying AD. The 
technique examines several transfer learning techniques, 
including sMRI, DTI, cross -domain methodology utilized in 
MNIST data set, and (iii) a hybrid methodology 
incorporating two kinds. The suggested technique, which 
makes use of glib CNN, is appropriate for the less resolving 
in both techniques. Even with tiny datasets, which are 
typical in medical image analysis, it still produces 
meaningful findings.

**Passage 24:**

> which 
makes use of glib CNN, is appropriate for the less resolving 
in both techniques. Even with tiny datasets, which are 
typical in medical image analysis, it still produces 
meaningful findings. Cross -modal transfer learning,  & a 
combination of the two utilising a shallow LeNet network 
are some of the transfer learning strategies that are 
compared. [15] The method avoids 3D conv & full -brain 
utilisation by using the "2 -D+" methodology previously 
devised for the hippocampus area. According to the 
interpretation of the data, filters taught on one modality have 
similar geometrical properties and only need modest 
adjustments when applied to another modality. The 
outcomes show that good performance may be achieved 
even with tiny datasets and few ROI slices.

</details>

---

## Sang and Li (2024) — Classification Study of Alzheimer’s Disease Based on Self-Attention Mechanism and DTI Imaging Using
_File: `Sang and Li - 2024 - Classification Study of Alzheimer’s Disease Based on Self-Attention Mechanism and DTI Imaging Using.pdf`_

1. **Yes**, diffusion MRI (DTI) was used in this paper.  
2. **Processing steps** (in order):  
   - Convert downloaded ADNI data to `nii.gz` format using FSL.  
   - Perform skull stripping and eddy current correction.  
   - Calculate DTI parameters (FA and MD) via FSL.  
   - Use PANDA’s deterministic fiber tracking to construct white matter fiber bundles.  
   - Segment the brain into a 90 × 90 network using the AAL brain atlas.  

3. **Software/tools explicitly named**:  
   - FSL (FMRIB Software Library)  
   - PANDA (Pipeline for Analyzing Brain Diffusion Images)  
   - MATLAB (PANDA runs within MATLAB)  

4. **Acquisition/processing parameters reported**:  
   - Not reported in available text.  

5. **Exact sentences from excerpts**:  
   - "The preprocessing workflow begins with converting the downloaded data from ADNI into the nii.gz format using FSL. Subsequently, skull stripping and eddy current correction are performed, and then DTI parameters such as FA and MD are calculated via FSL. Next, PANDA’s deterministic fiber tracking technique was employed to construct white matter fiber bundles based on the white matter trajectories. Finally, the automated anatomical labeling (AAL) brain atlas is utilized to segment the brain into a 90 × 90 brain network."  

6. **Processing description completeness**:  
   The description is complete based on the explicitly stated steps in the text.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> sion imAges) software. PANDA is a Linux-based
software that is running within MA TLAB. The preprocessing
workflow begins with converting the downloaded data from
ADNI into the nii.gz format using FSL. Subsequently, skull
stripping and eddy current correction are performed, and then
DTI parameters such as FA and MD are calculated via FSL. Next, PANDA ’s deterministic fiber tracking technique was
employed to construct white matter fiber bundles based on the
white matter trajectories. Finally, the automated anatomical
labeling (AAL) brain atlas is utilized to segment the brain into
a 90 × 90 brain network. Each brain region can be considered
a node in the network, with features encompassing the
number of voxels in each brain region.

**Passage 2:**

> experiments use two labels: AD
and normal control (NC). The DTI data processing will be
introduced in the first part of this section, followed by a
description of the GCN framework in the second part. The
results of the experiments will be presented in the third part. Finally, we summarized our investigation and provided the
expectations for future research. A. EXPERIMENTAL DATA
The data applied in this study is sourced from the ADNI
database (https://adni.loni.usc.edu/), from which we selected
70 AD patients and 70 NC individuals. The preprocessing
experiments were conducted using FSL (FMRIB Software
Library) and the FSL-based PANDA (Pipeline for Analyzing
braiN Diffusion imAges) software. PANDA is a Linux-based
software that is running within MA TLAB. The preprocessing
workflow begins with converting the downloaded data from
ADNI into the nii.gz format using FSL.

**Passage 3:**

> nd H. Chabriat, ‘‘Diffusion tensor imaging: Concepts and applications,’’
J. Magn. Reson. Imag., vol. 13, no. 4, pp. 534–546, Apr. 2001.
[4] C. Pierpaoli, P . Jezzard, P . J. Basser, A. Barnett, and G. Di Chiro,
‘‘Diffusion tensor MR imaging of the human brain,’’ Radiology, vol. 201,
no. 3, pp. 637–648, Dec. 1996.
[5] Y . Zhang, N. Schuff, G.-H. Jahng, W. Bayne, S. Mori, L. Schad, S. Mueller,
A.-T. Du, J. H. Kramer, K. Y affe, H. Chui, W. J. Jagust, B. L. Miller,
and M. W. Weiner, ‘‘Diffusion tensor imaging of cingulum fibers in mild
cognitive impairment and Alzheimer disease,’’ Neurology, vol. 68, no. 1,
pp. 13–19, Jan. 2007.
[6] M. Bozzali, S. E. MacPherson, M. Cercignani, W. R. Crum, T. Shallice,
and J. Rees, ‘‘White matter integrity assessed by diffusion tensor
tractography in a patient with a large tumor mass but minimal clinical and
neuropsychological deficits,’’ Funct. Neurol., vol.

**Passage 4:**

> Received 16 January 2024, accepted 30 January 2024, date of publication 8 February 2024, date of current version 20 February 2024. Digital Object Identifier 10.1 109/ACCESS.2024.3364545
Classification Study of Alzheimer’s Disease Based
on Self-Attention Mechanism and
DTI Imaging Using GCN
YILIN SANG
 AND WAN LI
School of Computing Science and Engineering, Beijing Technology and Business University, Beijing 100048, China
Corresponding author: Wan Li (wanli@btbu.edu.cn)
ABSTRACT Alzheimer’s disease (AD) is a neurodegenerative disorder. Diffusion tensor imaging (DTI)
provides information about the integrity of white matter fiber bundles that are related to the neuropathological
mechanisms, and it is one of the commonly used techniques in AD research. In this study, we first divided
each subject’s brain into 90 regions based on the automated anatomical labeling (AAL) brain atlas.

**Passage 5:**

> His research interests include medical
image classification and deep learning. WAN LI received the B.S. degree from Zhengzhou
University and the Ph.D. degree from the Beijing
University of Technology. She is currently an
Assistant Professor with Beijing Technology and
Business University. Her research interests include
medical image processing and deep learning. VOLUME 12, 2024 24395

**Passage 6:**

> ng steps. This approach is more conducive to practical
implementation in the future. Traditional machine learning
algorithms consume significant time for training when
dealing with large brain images. However, by processing
them into brain networks, not only can a substantial amount
of time be saved, but there is also no need for additional
feature extraction. DTI brain networks can be directly trained. This time-saving aspect becomes particularly beneficial in
practical use in the future.GCN is a relatively new network
with plenty of space for development. Therefore, future
research on AD classification using DTI images, functional
brain networks derived from fMRI, and the fusion of these
two networks should pay more attention to this aspect of
utilizing GCN. REFERENCES
[1] A. Collie and P .

**Passage 7:**

> lary tangles (intracellular aggregates
of hyperphosphorylated tau proteins), which can be revealed
as decreased FA and increased MD in the cingulate, corpus
callosum, and hippocampus regions [5], [6]. Graph neural network (GNN) is a general type of graph
neural network that can handle various types of graph data,
including directed, undirected, and weighted graphs [7]. VOLUME 12, 2024

 2024 The Authors. This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 License. For more information, see https://creativecommons.org/licenses/by-nc-nd/4.0/ 24387
Y. Sang, W.

**Passage 8:**

> vised learning with application to brain networks anal-
ysis,’’ IEEE J. Biomed. Health Informat., vol. 27, no. 8, pp. 4154–4165,
Aug. 2023.
[53] X. Ouyang, K. Chen, L. Y ao, X. Wu, J. Zhang, K. Li, Z. Jin, and X. Guo,
‘‘Independent component analysis-based identification of covariance
patterns of microstructural white matter damage in Alzheimer’s disease,’’
PLoS One, vol. 10, no. 3, Mar. 2015, Art. no. e0119714.
[54] C. D. Mayo, E. L. Mazerolle, L. Ritchie, J. D. Fisk, and J. R. Gawryluk,
‘‘Longitudinal changes in microstructural white matter metrics in
Alzheimer’s disease,’’NeuroImage, Clin., vol. 13, pp. 330–338, Jan. 2017.
[55] T. Kipf, ‘‘Deep learning with graph-structured representations,’’ Ph.D. dis-
sertation, Informat. Inst., University of Amsterdam, Amsterdam, The
Netherlands, 2020.
[56] H. Kong, J. Pan, Y . Shen, and S.

**Passage 9:**

> fication using DTI images, functional
brain networks derived from fMRI, and the fusion of these
two networks should pay more attention to this aspect of
utilizing GCN. REFERENCES
[1] A. Collie and P . Maruff, ‘‘The neuropsychology of preclinical Alzheimer’s
disease and mild cognitive impairment,’’ Neurosci. Biobehavioral Rev.,
vol. 24, no. 3, pp. 365–374, May 2000.
[2] S. Gauthier, P . Rosa-Neto, J. A. Morais, and C. Webster, ‘‘World Alzheimer
report 2021: Journey through the diagnosis of dementia,’’ Alzheimer’s
Disease Int., London, U.K., Tech. Rep., 2021.
[3] D. Le Bihan, J. Mangin, C. Poupon, C. A. Clark, S. Pappata, N. Molko,
and H. Chabriat, ‘‘Diffusion tensor imaging: Concepts and applications,’’
J. Magn. Reson. Imag., vol. 13, no. 4, pp. 534–546, Apr. 2001.
[4] C. Pierpaoli, P . Jezzard, P . J. Basser, A. Barnett, and G.

**Passage 10:**

> ter. It can identify abnormal diffusion patterns in
various neurological disorders and provide information about
the integrity of white matter fiber tracts related to neurobio-
logical mechanisms [3]. So far, DTI is the only neuroimaging
The associate editor coordinating the review of this manuscript and
approving it for publication was Roberta Palmeri
.
technique that can describe white matter fiber pathways and
is highly sensitive to microstructural white matter damage
within fiber bundles. Therefore, DTI is typically used to
specify anatomical connectivity impairments that cannot be
detected by structural MRI (sMRI). The two most frequently
used features to characterize white matter integrity are
fractional anisotropy (FA) and mean diffusivity (MD) [4].

**Passage 11:**

> mages of three modalities for classification. 3D sMRI images were input into the multi-channel ResNet
network model, while the brain networks constructed by DTI
and fMRI were input into the GCN model. Finally, multi-
channel ResNet and GCN were combined for multi-modality
classification to obtain pleasing results [21]. Other than the limited applications of GCN in AD-related
research, the currently favored AD-classification approaches
utilizing DTI images are briefly introduced as follows. GCN-excluded classification studies can be organized
into three categories: voxel-based, brain region-based,
and network-based classification studies. The research on
voxel-based classification is to select the most representative
AD voxels from the whole brain, calculate their DTI param-
eter values, such as FA and MD, and then classify them by
various classifiers [22], [23], [24], [25].

**Passage 12:**

> in atlas is utilized to segment the brain into
a 90 × 90 brain network. Each brain region can be considered
a node in the network, with features encompassing the
number of voxels in each brain region. After preprocessing,
three structural brain networks are obtained: (1) the FA brain
network, constructed based on the average FA values between
each brain region according to the brain atlas; (2) the FN
brain network, constructed based on the number of fibers
between each brain region according to the brain atlas; (3) the
LEN brain network, constructed based on the average fiber
length between each brain subdivision according to the brain
atlas. The node features include (1) ROIS (ROISurfaceSize),
denoting the number of voxels traversed by fibers in each
brain region; (2) ROIV (ROIV oxelSize), representing the
number of voxels in each brain region. B.

**Passage 13:**

> tention Mechanism and DTI Imaging Using GCN
TABLE 1. Table 1. Accuracy of different matrix and node feature
combinations with different k values. TABLE 2. Comparison of accuracy with other literature. This study considers the combination of different adja-
cency matrices representing brain networks and various node
features and tests the influence of different k values on
accuracy. The accuracy graph indicates that using the FA
brain network as network features and ROIS as node features
yields the best classification results. Moreover, using ROIS
as node features generally outperforms using ROIV as node
features for classification. By analyzing the node feature data,
this result may be because ROIS represents the number of
voxels with fibers passing through them.

**Passage 14:**

> sing GCN
across connections of different distances, helping to improve
classification performance. Therefore, we applied the GCN on the brain networks
abstracted from the DTI image for classification. Notably,
we endeavored to add the self-attention mechanism to the
original GCN structure in this study to realize better AD
classification. III. EXPERIMENT
Our study utilizes the white matter features of DTI images
and employs GCN with the self-attention mechanism for
classification. The network takes structural brain networks
based on DTI as input to generate cognitive state category
labels and uses these labels as output to obtain the final
classification accuracy. Our experiments use two labels: AD
and normal control (NC). The DTI data processing will be
introduced in the first part of this section, followed by a
description of the GCN framework in the second part.

**Passage 15:**

> 1
Y. Sang, W. Li: Classification Study of AD Based on Self-Attention Mechanism and DTI Imaging Using GCN
FIGURE 8. Accuracy, sensitivity and specificity using different feature combinations. FIGURE 9. The accuracy of different feature combinations combined with different k values was compared with
that of SVM. ROIS and ROIV . The connections between each brain region
are abstracted as relationships between nodes and edges in
the network. ROIS and ROIV serve as node features, and
each node’s graph membership and graph labels are used as
inputs to the GCN model. Next, the model is designed with
three convolutional layers. In the pooling layers following
each convolutional layer, the self-attention mechanism is
incorporated to filter the nodes. By removing irrelevant
nodes from the entire brain network, the accuracy of the
classification is improved. C.

**Passage 16:**

> ter regions and its image clarity
limitations, relatively few studies utilize DTI images for
classification research using CNN models. Therefore, our
study directs its attention to DTI brain networks. The self-attention mechanism is involved because specific
brain regions are essential in AD classification research,
and others are irrelevant. After abstracting DTI images into
brain networks, the importance of each brain region can be
determined based on its degree within the network. The self-
attention mechanism can eliminate irrelevant nodes during
the training process, equivalent to removing brain regions
unrelated to AD in the brain network. Additionally, it can
rank each node based on its self-attention score, allowing
for integration with AD-related brain regions and improving
classification accuracy.

**Passage 17:**

> and Q. Y e, ‘‘Intravoxel
incoherent motion diffusion-weighted imaging in the characterization of
Alzheimer’s disease,’’ Brain Imag. Behav., vol. 16, no. 2, pp. 617–626,
Apr. 2022.
[25] A. De and A. S. Chowdhury, ‘‘DTI based Alzheimer’s disease classifica-
tion with rank modulated fusion of CNNs and random forest,’’ Expert Syst. Appl., vol. 169, May 2021, Art. no. 114338.
[26] A. Demirhan, T. M. Nir, A. Zavaliangos-Petropulu, C. R. Jack,
M. W. Weiner, M. A. Bernstein, P . M. Thompson, and N. Jahanshad,
‘‘Feature selection improves the accuracy of classifying Alzheimer disease
using diffusion tensor images,’’ in Proc. IEEE 12th Int. Symp. Biomed. Imag. (ISBI), Brooklyn, NY , USA, Apr. 2015, pp. 126–130.
[27] T. Maggipinto, R. Bellotti, N. Amoroso, D. Diacono, G. Donvito,
E. Lella, A. Monaco, M. A. Scelsi, and S. Tangaro, ‘‘DTI measurements
for Alzheimer’s classification,’’ Phys. Med.

**Passage 18:**

> ted based on DTI images. The purpose is
to investigate the classification performance of the unique
white matter network derived from DTI images when
the self-attention mechanism is included with GCN. The
advantage lies in avoiding complex preprocessing and feature
extraction steps. Instead, only the DTI brain network is
input to GCN to obtain classification accuracy. Most studies
focus on innovative feature extraction methods in the current
research landscape. They extract features from voxels or
brain regions using various feature extraction techniques
and then employ traditional classifiers such as SVM for
classification. However, due to the primary role of DTI
images in AD’s white matter regions and its image clarity
limitations, relatively few studies utilize DTI images for
classification research using CNN models. Therefore, our
study directs its attention to DTI brain networks.

**Passage 19:**

> llice,
and J. Rees, ‘‘White matter integrity assessed by diffusion tensor
tractography in a patient with a large tumor mass but minimal clinical and
neuropsychological deficits,’’ Funct. Neurol., vol. 27, no. 4, pp. 239–246,
Oct. 2012.
[7] F. Scarselli, A. C. Tsoi, M. Gori, and M. Hagenbuchner, ‘‘Graphical-based
learning environments for pattern recognition,’’ in Structural, Syntactic,
and Statistical Pattern Recognition (Lecture Notes in Computer Science),
Aug. 2004, pp. 42–56.
[8] T. Kipf and M. Welling, ‘‘Semi-supervised classification with graph
convolutional networks,’’ 2016, arXiv:1609.02907.
[9] T.-A. Song, S. R. Chowdhury, F. Y ang, H. Jacobs, G. E. Fakhri, Q. Li,
K. Johnson, and J. Dutta, ‘‘Graph convolutional neural networks for
Alzheimer’s disease classification,’’ inProc. IEEE 16th Int. Symp. Biomed. Imag. (ISBI), V enice, Italy, Apr. 2019, pp. 414–417.
[10] H. Kong and S.

**Passage 20:**

> eryday lives of patients and
their families [1]. In 2021, over 55 million people worldwide
were diagnosed with this disease, and the number of AD
patients is estimated to reach 78 million by 2030 [2]. With the development of neuroimaging techniques, various
neuroimaging modalities have shown potential for improving
the diagnosis of AD from different perspectives. Diffusion tensor imaging (DTI) is a non-invasive magnetic
resonance imaging (MRI) technique that captures water
molecules’ degree of anisotropic diffusion along axons in the
white matter. It can identify abnormal diffusion patterns in
various neurological disorders and provide information about
the integrity of white matter fiber tracts related to neurobio-
logical mechanisms [3].

**Passage 21:**

> ent: Automated fiber
quantification,’’ in Proc. IEEE 16th Int. Symp. Biomed. Imag. (ISBI),
V enice, Italy, Apr. 2019, pp. 117–121.
[32] D. B. Stone, S. G. Ryman, A. P . Hartman, C. J. Wertz, and A. A. V akhtin,
‘‘Specific white matter tracts and diffusion properties predict conversion
from mild cognitive impairment to Alzheimer’s disease,’’ Frontiers Aging
Neurosci., vol. 13, 2021, Art. no. 711579.
[33] C. Y e, S. Mori, P . Chan, and T. Ma, ‘‘Connectome-wide network analysis
of white matter connectivity in Alzheimer’s disease,’’ NeuroImage, Clin.,
vol. 22, Feb. 2019, Art. no. 101690.
[34] J. P . J. Savarraj, R. Kitagawa, D. H. Kim, and H. A. Choi, ‘‘White matter
connectivity for early prediction of Alzheimer’s disease,’’ Technol. Health
Care, vol. 30, no. 1, pp. 17–28, Dec. 2021.
[35] F. He, Y . Li, C. Li, J. Zhao, T. Liu, L. Fan, X. Zhang, and J.

**Passage 22:**

> impairments that cannot be
detected by structural MRI (sMRI). The two most frequently
used features to characterize white matter integrity are
fractional anisotropy (FA) and mean diffusivity (MD) [4]. FA
provides information about fiber density, axon diameter, and
myelination, with decreased values indicating a loss of fiber
tract integrity. MD measures the average diffusivity of water
molecules in non-collinear directions, with increased values
indicating increased free diffusion of water molecules and
compromised anisotropy. The main pathological features of
AD include neuritic plaques or amyloid plaques (extracellular
deposits) and neurofibrillary tangles (intracellular aggregates
of hyperphosphorylated tau proteins), which can be revealed
as decreased FA and increased MD in the cingulate, corpus
callosum, and hippocampus regions [5], [6].

**Passage 23:**

> Jan. 2022, Art. no. e08725.
[30] L. Cao, B. R. Schrank, S. Rodriguez, E. G. Benz, T. W. Moulia,
G. T. Rickenbacher, A. C. Gomez, Y . Levites, S. R. Edwards, T. E. Golde,
B. T. Hyman, G. Barnea, and M. W. Albers, ‘‘Aβ alters the connectivity
of olfactory neurons in the absence of amyloid plaques in vivo,’’ Nature
Commun., vol. 3, no. 1, 2012, Art. no. 1009. 24394 VOLUME 12, 2024
Y. Sang, W. Li: Classification Study of AD Based on Self-Attention Mechanism and DTI Imaging Using GCN
[31] X. Dou, H. Y ao, D. Jin, F. Feng, P . Wang, B. Zhou, B. Liu, Z. Y ang,
N. An, X. Zhang, and Y . Liu, ‘‘Characterizing white matter connectivity
in Alzheimer’s disease and mild cognitive impairment: Automated fiber
quantification,’’ in Proc. IEEE 16th Int. Symp. Biomed. Imag. (ISBI),
V enice, Italy, Apr. 2019, pp. 117–121.
[32] D. B. Stone, S. G. Ryman, A. P . Hartman, C. J. Wertz, and A. A.

**Passage 24:**

> imer’s disease
identification,’’Comput. Methods Programs Biomed., vol. 238, Aug. 2023,
Art. no. 107597.
[22] C. Luo, M. Li, R. Qin, H. Chen, L. Huang, D. Y ang, Q. Y e, R. Liu,
Y . Xu, H. Zhao, and F. Bai, ‘‘Long longitudinal tract lesion contributes to
the progression of Alzheimer’s disease,’’ Frontiers Neurol., vol. 11, 2020,
Art. no. 503235.
[23] E. Lella, A. Pazienza, D. Lofù, R. Anglani, and F. Vitulano, ‘‘An
ensemble learning approach based on diffusion tensor imaging measures
for Alzheimer’s disease classification,’’ Electronics, vol. 10, no. 3, p. 249,
Jan. 2021.
[24] N. Xia, Y . Li, Y . Xue, W. Li, Z. Zhang, C. Wen, J. Li, and Q. Y e, ‘‘Intravoxel
incoherent motion diffusion-weighted imaging in the characterization of
Alzheimer’s disease,’’ Brain Imag. Behav., vol. 16, no. 2, pp. 617–626,
Apr. 2022.
[25] A. De and A. S.

</details>

---

## Singh Chhabra et al. (2023) — Multimodal Neuroimaging for Early Alzheimer's detection A Deep Learning Approach
_File: `Singh Chhabra et al. - 2023 - Multimodal Neuroimaging for Early Alzheimer's detection A Deep Learning Approach.pdf`_

1. **Was diffusion MRI (DTI, dMRI, DWI, or similar) used in this paper?**  
   Yes. The paper explicitly mentions **diffusion tensor imaging (DTI)** as one of the modalities used, alongside structural MRI (sMRI) and functional MRI (fMRI).  

---

2. **What processing steps were applied to the diffusion images?**  
   - **Feature extraction** from DTI data as part of multimodal analysis.  
   - **Data augmentation techniques** to address class imbalance and improve model robustness.  
   - **Integration of subnetworks** (sMRI CNN, fMRI RNN, DTI GCN) into a multimodal neural network for classification.  

---

3. **What software or tools are explicitly named for processing?**  
   No specific software or tools are explicitly named. The paper refers to neural network architectures (CNN, RNN, GCN) but does not mention tools like FSL, MRtrix, or other diffusion MRI processing packages.  

---

4. **What acquisition or processing parameters are explicitly reported?**  
   **Not reported in available text.** The excerpts do not mention b-values, number of diffusion directions, voxel size, or other technical parameters related to diffusion MRI acquisition or processing.  

---

5. **Copy the exact sentences from the excerpts that describe the processing.**  
   - "Employ data augmentation techniques to address class imbalance and improve the robustness of the deep learning model."  
   - "Create an innovative deep learning architecture that takes use of features from all three imaging modalities: a sMRI CNN, an fMRI RNN, and a DTI graph convolutional network (GCN)."  

---

6. **Is the processing description complete, or does it appear incomplete/missing?**  
   **Incomplete.** The description mentions high-level steps (e.g., data augmentation, feature extraction, and network integration) but does not specify detailed diffusion MRI processing steps (e.g., tensor estimation, tractography, or parameter optimization). The focus is on the deep learning framework rather than diffusion MRI-specific technical details.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> Alzheimer's detection 
neuroimaging initiative. Neuroimaging Clinics, 15(4), 869-877. 
[15] Ashburner, J., & Friston, K. J. (2005). Unified segmentation. Neuroimage, 26(3), 839-851. 
[16] Friston, K. J., Williams, S., Howard, R., Frackowiak, R. S., & Turner, 
R. (1996). Movement -related effects in fMRI time -series. Magnetic 
Resonance in Medicine, 35(3), 346-355. 
[17] Basser, P. J., & Jones, D. K. (2002). Diffusion -tensor MRI: theory, 
experimental design, and data analysis - a technical review. NMR in 
Biomedicine, 15(7-8), 456-467. 
[18] Jia, H., Lao, H. Deep learning and multimodal feature fusion for the 
aided diagnosis of Alzheimer's disease. Neural Comput & Applic 34, 
19585–19598 (2022). https://doi.org/10.1007/s00521-022-07501-0 
[19] LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. Nature, 
521(7553), 436-444. 
[20] Hochreiter, S., & Schmidhuber, J. (1997).

**Passage 2:**

> thods. Create a deep learning framework that can easily 
incorporate different kinds of neuroimaging data, such as 
those from fundamental MRI, functioning MRI, and diffusion 
tensor image processing. Find out how well our model performs in terms of 
classification accuracy, sensitivity, and specificity. The purpose of this research is to compare and contrast our 
suggested model to popular deep learning techniques already 
in use. IEEE - 56998
14th ICCCNT IEEE Conference 
July 6-8, 2023 
IIT - Delhi, Delhi, India
2023 14th International Conference on Computing Communication and Networking Technologies (ICCCNT) | 979-8-3503-3509-5/23/$31.00 ©2023 IEEE | DOI: 10.1109/ICCCNT56998.2023.10307780
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 15,2026 at 22:48:07 UTC from IEEE Xplore. Restrictions apply.

**Passage 3:**

> Multimodal Neuroimaging for Early Alzheimer's 
detection: A Deep Learning Approach 
Dr.

**Passage 4:**

> re data quality, 
consistency, and reliability. Following pre-processing, extract 
relevant features from the data for each imaging modality, 
capturing essential information from sMRI, fMRI, and DTI. Employ data augmentation techniques to address class 
imbalance and improve the robustness of the deep learning 
model. Create an innovative deep learning architecture that takes 
use of features from all three imaging modalities: a sMRI 
CNN, an fMRI RNN, and a DTI graph convolutional network 
(GCN). For the best final classification results, train the 
subnetworks separately and then combine them to make a 
modal neural network for classification. Tweak the model's 
hyper parameters until they're just right. Fig. 1.

**Passage 5:**

> Y. Downloaded on February 15,2026 at 22:48:07 UTC from IEEE Xplore. Restrictions apply. 
[23] [28] Ellis, K. A., Bush, A. I., Darby, D., De Fazio, D., Foster, J., 
Hudson, P., ... & Maruff, P. (2009). The Australian Imaging, 
Biomarkers and Lifestyle (AIBL) study of aging: methodology and 
baseline characteristics of 1112 individuals recruited for a longitudinal 
study of Alzheimer's detection. International Psychogeriatrics, 21(4), 
672-687. 
[24] Marcus, D. S., Wang, T. H., Parker, J., Csernansky, J. G., Morris, J. C., 
& Buckner, R. L. (2007). Open Access Series of Imaging Studies 
(OASIS): cross -sectional MRI data in young, midd le-aged, 
nondemented, and demented older adults. Journal of Cognitive 
Neuroscience, 19(9), 1498-1507. 
[25] Reitz, C., Brayne, C., & Mayeux, R. (2011). Epidemiology of 
Alzheimer detection. Nature Reviews Neurology, 7(3), 137-152.

**Passage 6:**

> ification studies and 
associated feature extraction methods for Alzheimer's detection and its 
prodromal stages. NeuroImage, 155, 530-548. 
[12] Jack, C. R., Bennett, D. A., Blennow, K., Carrillo, M. C., Dunn, B., 
Haeberlein, S. B., ... & Silverberg, N. (2018). NIA -AA Research 
Framework: Toward a biological definition of Alzheimer's detection. Alzheimer's & Dementia, 14(4), 535-562. 
[13] Frisoni, G. B., Fox, N. C., Jack, C. R., Scheltens, P., & Thompson, P. M. (2010). The clinical use of structural MRI in Alzheimer detection. Nature Reviews Neurology, 6(2), 67-77. 
[14] Mueller, S. G., Weiner, M. W., Thal, L. J., Petersen, R. C., Jack, C. R., 
Jagust, W., ... & Beckett, L. (2005). The Alzheimer's detection 
neuroimaging initiative. Neuroimaging Clinics, 15(4), 869-877. 
[15] Ashburner, J., & Friston, K. J. (2005). Unified segmentation. Neuroimage, 26(3), 839-851. 
[16] Friston, K.

**Passage 7:**

> he diagnosis of Alzheimer's 
detection. Various data kinds, sizes, and dimensions make it 
difficult to integrate multimodal neuroimaging data into a 
unified framework, as described in reference [8]. The goal of this study is to develop a novel deep learning 
approach that integrates multimodal neuroimaging data, 
including structural MRI, fMRI, and DTI, to aid in the early 
diagnosis of Alzheimer's detection. It is expected that our 
strategy will achieve more diagnostic accuracy than existing 
approaches by mak ing use of the information provided by 
these various forms of imaging in a complimentary way. The 
current study describes our aims and methods. Create a deep learning framework that can easily 
incorporate different kinds of neuroimaging data, such as 
those from fundamental MRI, functioning MRI, and diffusion 
tensor image processing.

**Passage 8:**

> roimaging data to 
improve the accuracy and timeliness of Alzheimer's detection 
diagnosis, our study aims to add to the existing body of 
literature and address the limitations of current approaches. A 
convolutional neural network (CNN) is used for structural 
MRI data, a recurrent neural network (RNN) is used for fMRI 
data, and a graph-based convolutional network (GCN) is used 
for diffusion tensor imaging (DTI) data in the proposed 
framework's tripartite structure. It is expected that the 
diagnostic accuracy for identifying people in the early stages 
of Alzheimer's detection would increase once the subnetwork 
outputs are integrated into a cohesive model. In addition to improving classification accuracy, our 
strategy is designed to provide light on the relationships 
between various imaging techniques for identifying AD.

**Passage 9:**

> lzheimer's detection (AD) 
is crucial for initiating therapy as soon as possible. This paves 
the way for patients to take advantage of current medicines 
and better control detection progression [2]. Due to its 
complex and heterogeneous nature, early diagnosis of 
Alzheimer's detection (AD) is a major challenge [3]. It has been shown that multimodal neuroimaging methods 
have the ability to detect brain abnormalities associated with 
Alzheimer's detection. Diffusion tensor analysis (DTI), 
functional magnetic resonance imaging (fMRI), and structural 
MRI (sMRI) all provide unique but complimentary 
perspectives on brain anatomy, function, and connection [4]. The combination of various imaging techniques may improve 
diagnostic accuracy [5].

**Passage 10:**

> 018) used a 
convolutional neural network (CNN) to analyze sMRI data 
and got an accuracy rate of 89.7%. Information gathered from fMRI scans has been used to 
make diagnoses of Alzheimer's detection. To examine fMRI 
data, Suk et al. [11] used a deep learning model that 
incorporated a stacked autoencoder. The findings indicated 
that the model had an ac curate classification rate of 84.3% 
when trying to differentiate between AD sufferers and healthy 
controls. In a different study, Wee et al. [12] fused fMRI and 
sMRI data using a multimodal sparse representation 
technique, and their AD diagnosis accuracy i ncreased to 
88.2%. B. Multimodal neuroimaging studies: 
Combining multiple neuroimaging modalities has been 
shown to improve diagnostic performance.

**Passage 11:**

> al 
and multimodal neuroimaging data. The review encompasses 
an evaluation of the efficacy of these methodologies, as well 
as an examination of the obstacles encountered in their 
implementation. A. Single-modal neuroimaging studies: 
For the goal of diagnosing Alzheimer's detection, 
neuroimaging data from a single modality has been used in a 
large number of scholarly investigations. An SVM classifier 
built by Zhang et al. (2019) using sMRI data successfully 
distinguished 86.5% of AD patients from controls. To classify 
individuals with Alzheimer's detection (AD) and moderate 
cognitive impairment (MCI), Liu et al. (2018) used a 
convolutional neural network (CNN) to analyze sMRI data 
and got an accuracy rate of 89.7%. Information gathered from fMRI scans has been used to 
make diagnoses of Alzheimer's detection.

**Passage 12:**

> tural 
MRI (sMRI) all provide unique but complimentary 
perspectives on brain anatomy, function, and connection [4]. The combination of various imaging techniques may improve 
diagnostic accuracy [5]. New advancements in deep learning 
approaches [6] provide encouraging capabilities for analyzing 
multidimensional brain imaging data for the early diagnosis of 
Alzheimer's detection. However, much of the present research has focused on 
using separate -modal neuroimaging data, which may limit 
their diagnostic effectiveness [7], despite the growing interest 
in using deep learning to the diagnosis of Alzheimer's 
detection. Various data kinds, sizes, and dimensions make it 
difficult to integrate multimodal neuroimaging data into a 
unified framework, as described in reference [8].

**Passage 13:**

> DNN, 
SVM, RF 
MMSE, 
MRI 
85-98% 80-95% 75-90% 0.85
-
0.98 
[18] SVM,  AUC fMRI, 
sMRI 
91-97%  70-97% 75-85% 0.75
-
0.88 
Prop
osed 
Algor
ithm 
CNN, 
RNN, 
GCN 
MMSE, 
fMRI 90% 85% 92% 0.96 
 
VI. CONCLUSION 
In conclusion, our study has developed and evaluated a 
novel algorithm for early diagnosis of Alzheimer's detection 
using multimodal neuroimaging and deep learning. Our 
proposed algorithm achieved a high level of accuracy, 
sensitivity, sp ecificity, and AUC -ROC, demonstrating its 
potential for improving diagnostic accuracy and patient 
outcomes. Our study has also identified gaps in existing 
research, including limited generalizability and interpretation 
of model decision -making processes. Through our research, 
we have addressed these gaps by developing a transparent and 
effective algorithm that can be used in clinical practice.

**Passage 14:**

> lassification results, train the 
subnetworks separately and then combine them to make a 
modal neural network for classification. Tweak the model's 
hyper parameters until they're just right. Fig. 1. Comparative Coronal MRI Views: Multimodal Imaging in 
Alzheimer's Detection from the ADNI Dataset 
 
The model's accuracy should be checked using an 
independent dataset, and it should be compared to both 
baseline algorithmic approaches and current deep learning 
techniques. Evaluate the model's genera lizability on a new 
dataset to prove its clinical usefulness.

**Passage 15:**

> zheimer's dete ction 
categorization. The dataset utilized in this study comprised of 
1200 participants, with 600 individuals diagnosed with early -
stage AD and 600 healthy controls matched for age. The 
application of data augmentation techniques was employed to 
mitigate c lass imbalance and enhance the resilience of our 
model. We used a three-tiered deep learning architecture, which 
included a sMRI CNN, an fMRI RNN, and a DTI GCN to 
analyze MRI data. The final categorization was performed by 
fusing several previously separa te networks into a single 
multimodal neural network. Our study involved a comparative 
analysis of the efficacy of our model vis -à-vis conventional 
machine learning algorithms and pre -existing deep learning 
techniques.

**Passage 16:**

> Multimodal Neuroimaging for Early Alzheimer's 
detection: A Deep Learning Approach 
Dr. Gurpreet Singh Chhabra  
Computer Science & Engineering 
department of GITAM School of 
Technology, GITAM Deemed to be 
University, Visakhapatnam, Inida 
gurpreet.kit@gmail.com 
Mr Leelkanth Dewangan 
Assistant Professor, G H Raisoni 
Institute of Engineering and Business 
Management jalgaon, Maharashtra, 
India 
mcs.leelkanth@gmail.com 
Dr Abhishek Guru 
Department of CSE, Koneru 
Lakshmaiah Education Foundation, 
Vaddeswaram 522302, AP, India 
abhishekguru0703@gmail.com 
Dr Suman Kumar Swarnkar 
Department of Computer Science & 
Engineering, Shri Shankaracharya 
Institute of Professional Management 
and Technology, Raipur, Chhattisgarh, 
India 
sumanswarnkar17@gmail.com
Dr Bhawna Janghel Rajput 
Assistant Professor, Department of 
Computer Science & Engineering, 
Rungta College of Engineering in 
Bhilai, Durg.(C.G.) 
bhawna.janghel@rungta.ac.in 
Abstract—  The timely identification and treatment of 
Alzheimer's detection (AD) is of paramount importance.

**Passage 17:**

> validati on of 
our model in more extensive, multi -center cohorts and the 
examination of its efficacy in forecasting the advancement of 
detection and the effectiveness of therapeutic interventions. Keywords— Alzheimer's detection, Diffusion tensor imaging, 
Deep learning models, Convolutional neural network(CNN), 
Recurrent neural network (RNN), Graph convolutional network, 
Data fusion 
I. INTRODUCTION 
Alzheimer's detection (AD) is a neurological ailment with 
a huge worldwide effect that affects a large number of people 
over time. In addition, it causes dementia in almost all of 
its 
victims. [1]. Timely diagnosis of Alzheimer's detection (AD) 
is crucial for initiating therapy as soon as possible. This paves 
the way for patients to take advantage of current medicines 
and better control detection progression [2].

**Passage 18:**

> tection using neuroimaging data. However, 
there is a need for novel methods that can effectively integrate 
multimodal neuroimaging data to improve diagnostic 
accuracy and generalizability. TABLE I. STUDY SUMMERY OF LITERATURE REVIEW 
Literatu
re 
Review 
Algorithm Param
eters 
Research Gap 
[9] CNN, SVM, 
RF 
MMSE
, PET 
Lack of comparison with other 
AI-based models 
[10] MLP, DT, 
KNN 
CDR, 
EEG 
Limited evaluation on large 
datasets 
[11] CNN, GBDT, 
SVM 
CERA
D, 
fMRI 
Limited generalizability due to 
small sample sizes 
[12] Random 
Forest, ANN, 
SVM 
EEG, 
CSF 
Limited analysis of individual 
contributions of different 
features 
[13] DNN, RF, 
DT 
CSF, 
MRI 
Limited comparison with other 
traditional diagnostic methods 
[14] Deep 
learning, 
SVM, DT 
MMSE
, MRI 
Limited explanation of model 
decision-making processes 
[15] CNN, MLP, 
SVM 
PET, 
fMRI 
Limited evaluation of model 
interpretability 
[16] GBDT, 
KNN, DT 
CDR, 
EEG 
Limited analysis of individual 
contributions of different 
features 
[17] DNN, SVM, 
RF 
MMSE
, MRI 
Limited evaluation on multi-
modal datasets 
 
III.

**Passage 19:**

> curacy of 91.4% in classifying AD 
patients. C. Challenges and limitations: 
Despite the promising results of existing studies, there are 
several challenges and limitations that need to be addressed. Most current methods focus on s ingle-modal neuroimaging 
data, which may limit their diagnostic performance due to the 
lack of complementary information provided by different 
imaging modalities [15]. Additionally, the integration of 
multimodal neuroimaging data in a unified deep learning 
framework remains a challenging task due to differences in 
data types, scales, and dimensions [16]. Furthermore, the 
generalizability of the models to independent datasets and 
diverse populations is often not assessed, limiting their 
applicability in clinical settings [17].

**Passage 20:**

> ion 
technique, and their AD diagnosis accuracy i ncreased to 
88.2%. B. Multimodal neuroimaging studies: 
Combining multiple neuroimaging modalities has been 
shown to improve diagnostic performance. Zhang et al. [13] 
utilized sMRI, fMRI, and positron emission tomography 
(PET) data, applying a multimodal classification framework 
to achieve a classification accuracy of 92.1% in differentiating 
AD and MCI patients from healthy controls. In another study, 
Liu et al. [14] combined sMRI and FDG -PET data using a 
deep learning model with convolutional and recurrent ne ural 
networks, reporting an accuracy of 91.4% in classifying AD 
patients. C. Challenges and limitations: 
Despite the promising results of existing studies, there are 
several challenges and limitations that need to be addressed.

**Passage 21:**

> icity (92%). Results 
point to the efficacy of our suggested method in early 
Alzheimer's detection diagnosis. To dig further into the algorithm's efficiency, a battery of 
statistical tests were run. The testing showed that our proposed 
algorithm outperformed the state -of-the-art algorithms in all 
three categories (accuracy, sensitivity, and specificity) by a 
statistically significant margin (p 0.05). IEEE - 56998
14th ICCCNT IEEE Conference 
July 6-8, 2023 
IIT - Delhi, Delhi, India
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 15,2026 at 22:48:07 UTC from IEEE Xplore. Restrictions apply. The results of our experiments support the use of our 
proposed algorithm for the early diagnosis of Alzheimer's 
detection. Moreover, they highlight the potential of AI-driven 
models to improve diagnostic accuracy and patient outcomes. TABLE II.

**Passage 22:**

> cision-making process. Furthermore, our algorithm can be 
integrated with existing diagnostic methods to develop a more 
comprehensive and effective approach to early Alzheimer's 
detection diagnosis. Finally, the long -term impact of early 
diagnosis on patient outcomes should be investigated to 
provide further evidence for the importance of accurate and 
timely diagnosis. R
EFERENCES 
[1] Jalilianhasanpour R, Beheshtian E, Sherbaf G et al (2019) Functional 
connectivity in neurodegenerative disorders: Alzheimer’s disease and 
frontotemporal dementia. Top Magn Reson Imaging 28(6):317–324 
[2] Liu, M., Cheng, D., Yan, W., & Liu, Y. (2018). Classificati on of 
Alzheimer's detection by combination of convolutional and recurrent 
neural networks using FDG -PET images. Frontiers in 
Neuroinformatics, 12, 35. 
[3]  Zhang, D., Wang, Y., Zhou, L., Yuan, H., & Shen, D. (2011).

**Passage 23:**

> ted older adults. Journal of Cognitive 
Neuroscience, 19(9), 1498-1507. 
[25] Reitz, C., Brayne, C., & Mayeux, R. (2011). Epidemiology of 
Alzheimer detection. Nature Reviews Neurology, 7(3), 137-152. IEEE - 56998
14th ICCCNT IEEE Conference 
July 6-8, 2023 
IIT - Delhi, Delhi, India
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 15,2026 at 22:48:07 UTC from IEEE Xplore. Restrictions apply.

**Passage 24:**

> e 
model hyperparameters to optimize its performance. A. Experimental Result: 
The current study involves experimental evaluation of the 
suggested algorithm for early Alzheimer's detection diagnosis. Methods included teaching and testing the algorithm using 
data from 500 patients' MRI scans and Mini -Mental State 
Examination scores. Two hundred and fifty people with 
Alzheimer's detection and the same number of healthy persons 
made up the sample. According to the results, the researchers' suggested 
algorithm achieved an AUC -ROC value of 0.96 along with 
high levels of accuracy (92%) and specificity (92%). Results 
point to the efficacy of our suggested method in early 
Alzheimer's detection diagnosis. To dig further into the algorithm's efficiency, a battery of 
statistical tests were run.

</details>

---

## Structural Connectivity Analysis in Cognitive Decline Insights from Graph Theory and Mass-Spring Modeling
_File: `Structural Connectivity Analysis in Cognitive Decline Insights from Graph Theory and Mass-Spring Modeling.pdf`_

1. **Yes**, diffusion MRI (DTI) was used in this paper. The text explicitly states: "DTI data acquired from Alzheimer’s disease initiatives (ADNI) database" and "preprocessed DTI data" were used.

2. **Processing steps applied to diffusion images** (in order):  
   - Eddy current correction and motion correction to minimize distortions.  
   - DTI image registration using an affine transformation to align with T1-weighted MRI.  
   - Tissue segmentation of T1-weighted MRI to classify gray matter, white matter, and cerebrospinal fluid.  
   - DTI reconstruction to compute diffusion tensor metrics (FA, MD).  
   - Fiber tracking using Diffusion Toolkit’s algorithms (deterministic streamline tracking or probabilistic tractography).  
   - Cortex parcellation using BrainSuite’s Gyral Surface Conformal Mapping (GSCM).  
   - Tractography-to-parcellation mapping to create structural connectivity matrices.  
   - Initial quality assessment to exclude datasets with severe artifacts or low signal-to-noise regions.  

3. **Software/tools explicitly named**:  
   - **BrainSuite** (for registration, segmentation, parcellation, and tractography-to-parcellation mapping).  
   - **Diffusion Toolkit** (for fiber tracking algorithms).  
   - **MRIcron** (for converting DICOM to NIFTI format).  

4. **Acquisition/processing parameters explicitly reported**:  
   - **54 diffusion directions**.  
   - **b-value of 1000 s/mm²**.  
   - **2 mm isotropic voxel size**.  
   - **Eddy current correction** and **motion correction**.  

5. **Exact sentences from the excerpts**:  
   - "BrainSuite’s Diffusion module corrected eddy currents and motion, mitigating distortions and artifacts."  
   - "The preprocessed DTI data was aligned with the T1-weighted structural MRI image acquired from the same subject."  
   - "Fractional anisotropy (FA), mean diffusivity (MD), and other diffusion metrics were calculated from the diffusion tensor."  
   - "BrainSuite utilizes Diffusion Toolkit’s fiber tracking algorithms, such as deterministic streamline tracking or probabilistic tractography."  
   - "The dataset, consisting of 54 diffusion directions, b-value 1000 s/mm², and 2 mm isotropic voxel size across 64 axial slices, underwent rigorous preprocessing in BrainSuite."  

6. **Processing description completeness**:  
   The processing steps are explicitly described in the order they were applied, including registration, segmentation, reconstruction, tracking, parcellation, and quality checks. All parameters (e.g., directions, b-value, voxel size) are reported. The description appears **complete** based on the excerpts.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> ns. BrainSuite’s Diffusion module corrected eddy currents
and motion, mitigating distortions and artifacts. V oxel-wise
diffusion was captured through diffusion tensor estimation
using the BrainSuite. BrainSuite’s non-linear registration en-
sured consistent anatomical alignment, and a generated brain
mask excluded non-brain regions. White matter fiber tracts,
tracked with BrainSuite’s algorithm, exhibited a 15% mean
fractional anisotropy increase post-preprocessing. Structural
connectivity matrices, representing brain region connections,
were derived from the constructed fiber tracts. Visualizations
included a tractogram image and connectogram for a subject
each from NC, MCI, and AD groups (Fig. 1a), with similar
patterns observed in other subjects. The tractogram analysis re-
vealed distinctive white matter connectivity patterns.

**Passage 2:**

> sing steps to correct for artifacts and distortions. Eddy current correction and motion correction were performed
to minimize distortions caused by eddy currents and subject
motion during scanning. A. Structural Connectivity Formation
1) DTI image registration: The preprocessed DTI data was
aligned with the T1-weighted structural MRI image acquired
from the same subject. The registration was performed using
an affine transformation to ensure proper spatial correspon-
dence between the DTI data and the anatomical structures. 2) Tissue segmentation: Tissue segmentation was carried
out on the T1-weighted structural MRI image to classify
different brain tissues, including gray matter, white matter,
and cerebrospinal fluid. BrainSuite’s tissue segmentation tools
were utilized, combining intensity-based and spatial priors for
accurate segmentation.

**Passage 3:**

> PET at ADNI-3 baseline were included. Demographic information such as age, sex, years of education,
Clinical Dementia Rating (CDR), Mini-Mental State Exam
(MMSE), and clinical diagnosis were recorded. The diffusion MRI data were acquired from a cohort of
participants, including 64 normal controls (NC) and patients
diagnosed with dementia-related disorders such as 57 mild
cognitive impairment (MCI) and 29 AD subjects. According
to ADNI criteria, Ethical approval was obtained, and all partic-
ipants provided informed consent. The acquired raw DICOM
files were converted to NIFTI format (.nii) which is compatible
with Brainsuite using MRIcron. The raw DTI data underwent
preprocessing steps to correct for artifacts and distortions. Eddy current correction and motion correction were performed
to minimize distortions caused by eddy currents and subject
motion during scanning. A.

**Passage 4:**

> ain tissues, including gray matter, white matter,
and cerebrospinal fluid. BrainSuite’s tissue segmentation tools
were utilized, combining intensity-based and spatial priors for
accurate segmentation. 3) DTI reconstruction: The diffusion tensor was recon-
structed from the preprocessed DTI data, providing informa-
tion about the diffusion of water molecules in different brain
tissues. Fractional anisotropy (FA), mean diffusivity (MD),
and other diffusion metrics were calculated from the diffusion
tensor. 4) Fiber tracking: Fiber tracking, or tractography, was
performed on the reconstructed DTI data to estimate the white
matter fiber pathways in the brain. BrainSuite utilizes Diffu-
sion Toolkit’s fiber tracking algorithms, such as deterministic
streamline tracking or probabilistic tractography, to generate
the white matter tracts.

**Passage 5:**

> of conversion from amnestic
mild cognitive impairment to alzheimer’s disease based on the brain
structural connectome,” Frontiers in neurology, vol. 9, p. 1178, 2019.
[12] C. Bhushan, J. P. Haldar, S. Choi, et al., “Co-registration and distortion
correction of diffusion and anatomical images based on inverse contrast
normalization,” Neuroimage, vol. 115, pp. 269–280, 2015.
[13] C. Bhushan, J. P. Haldar, A. A. Joshi, et al., “Inversion: A robust method
for co-registration of mprage and diffusion mri images,” in Joint Annual
Meeting ISMRM-ESMRMB, Milan, Italy , p. 2583, 2014.
[14] D. Varadarajan, C. Bhushan, C. Gonzalez-Zacarias, et al. , “Brainsuite
diffusion pipeline (bdp): Processing tools for diffusion-mri,” in 26th
Annual Meeting of the Organization for Human Brain Mapping. Online ,
2020.
[15] M. R. Brier, J. B. Thomas, A. M.

**Passage 6:**

> fore, in this investigation, we utilize DTI data acquired from
Alzheimer’s disease initiatives (ADNI) database, comprising
of including healthy controls and individuals at various stages
of dementia. BrainSuite [12]–[14], a comprehensive software
for brain image processing, is employed to preprocess the DTI
2023 IEEE International Conference on Bioinformatics and Biomedicine (BIBM) | 979-8-3503-3748-8/23/$31.00 ©2023 IEEE | DOI: 10.1109/BIBM58861.2023.10385749
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply. 2791
data and generate structural connectivity networks.

**Passage 7:**

> imal value of C=0.01 and a polynomial degree
of 2. A 10-folds cross-validation technique was then applied
using the selected features to classify subjects into NC, MCI,
and AD groups. III. R ESULTS
A. Structural connectivity formation
We optimized acquired diffusion MRI data for structural
connectivity analysis using a Siemens 3T scanner. The dataset,
consisting of 54 diffusion directions, b-value 1000 s/mm², and
2 mm isotropic voxel size across 64 axial slices, underwent
rigorous preprocessing in BrainSuite. Initial quality assessment
excluded datasets with severe artifacts or low signal-to-noise
regions. BrainSuite’s Diffusion module corrected eddy currents
and motion, mitigating distortions and artifacts. V oxel-wise
diffusion was captured through diffusion tensor estimation
using the BrainSuite.

**Passage 8:**

> [21] T. Liu, A. W. Bargteil, J. F. O’Brien, et al. , “Fast simulation of mass-
spring systems,” ACM Transactions on Graphics (TOG) , vol. 32, no. 6,
pp. 1–7, 2013.
[22] M. K. Hobert, V . M. Stein, P. Dziallas, et al. , “Evaluation of normal
appearing spinal cord by diffusion tensor imaging, fiber tracking, frac-
tional anisotropy, and apparent diffusion coefficient measurement in 13
dogs,” Acta Veterinaria Scandinavica, vol. 55, no. 1, pp. 1–7, 2013.
[23] Y . Zhang, J. Liu, L. Li, et al. , “A study on small-world brain func-
tional networks altered by postherpetic neuralgia,” Magnetic Resonance
Imaging, vol. 32, no. 4, pp. 359–365, 2014.
[24] K. Supekar, V . Menon, D. Rubin, et al., “Network analysis of intrinsic
functional brain connectivity in alzheimer’s disease,” PLoS computa-
tional biology, vol. 4, no. 6, p. e1000100, 2008.
[25] C.-Y . Lo, P.-N. Wang, K.-H.

**Passage 9:**

> athways in the brain. BrainSuite utilizes Diffu-
sion Toolkit’s fiber tracking algorithms, such as deterministic
streamline tracking or probabilistic tractography, to generate
the white matter tracts. 5) Cortex Parcellation: The cerebral cortex was parcellated
into different regions based on gyral and sulcal patterns. Brain-
Suite’s Gyral Surface Conformal Mapping (GSCM) method
was employed for cortical parcellation. 6) Tractography-to-parcellation mapping: The white mat-
ter tracts obtained from fiber tracking were mapped to specific
cortical regions based on their endpoints. This step allowed
us to create a structural connectivity matrix representing the
connections between different brain regions. B.

**Passage 10:**

> l. , “Brainsuite
diffusion pipeline (bdp): Processing tools for diffusion-mri,” in 26th
Annual Meeting of the Organization for Human Brain Mapping. Online ,
2020.
[15] M. R. Brier, J. B. Thomas, A. M. Fagan, et al., “Functional connectivity
and graph theory in preclinical alzheimer’s disease,” Neurobiology of
aging, vol. 35, no. 4, pp. 757–768, 2014.
[16] R. Guimera and L. A. N. Amaral, “Cartography of complex networks:
modules and universal roles,” Journal of Statistical Mechanics: Theory
and Experiment, vol. 2005, no. 02, p. P02001, 2005.
[17] T. Rittman, R. Borchert, S. Jones, et al., “Functional network resilience
to pathology in presymptomatic genetic frontotemporal dementia,” Neu-
robiology of Aging , vol. 77, pp. 169–177, 2019.
[18] J. Go ˜ni, A. Avena-Koenigsberger, N.

**Passage 11:**

> MCI
NC
1 1.1 1.2 1.3 1.4 1.5 1.6
AD
MCI
NC
pval =0.0180 pval = 0.0377
pval = 0.0314 pval = 0.0138
pval = 0.0000 pval = 0.0001
pval = 0.0185 pval = 0.0382
a. Positions
b. Velocities
c. Accelerations
d. Damping forces
Damping forces Damping forces
Accelerations Accelerations
Velocities Velocities
Positions Positions
Par triangularis R Transverse temporal gyrus L
Superior frontal gyrus L Parahippocampal gyrus L
Par Orbitas R
Superior frontal gyrus R Lateral orbital gyrus R
Superior frontal gyrus L
0.55 0.6 0.65 0.7 0.75 0.8
AD
MCI
NC
Velocities
1.6 1.8 2 2.2 2.4 2.6 2.8
Accelerations
AD
MCI
NC
0.7 0.75 0.8 0.850.65
AD
MCI
NC
Positions
0.055 0.06 0.065 0.07 0.075 0.08
AD
MCI
NC
Damping forces
pval = 0.0048
pval = 0.0185
pval = 0.0453
pval = 0.0226
Hippocampus L
Cuneus L
Hippocampus L
Supramarginal gyrus L
Fig.

**Passage 12:**

> ic interventions. In the following sections, the materials and methods used in
the study, including data acquisition, DTI preprocessing, graph
theory analysis, and statistical procedures are detailed. The
results of our investigation are then presented along with the
discussion of their implications. Finally, the manuscript would
be concluded by highlighting the potential clinical impact of
our findings and outlining directions for future research in this
promising area of study. II. M ETHODS
The DTI data employed for this study was acquired from
the Alzheimer’s Disease Neuroimaging Initiative3 database
(ADNI-3) (http://adni.loni.usc.edu/). ADNI was launched in
2003 as a public–private partnership with the primary goal
of testing whether serial MRI, PET,other biological mark-
ers,and clinical and neuropsychological assessments can be
combined to assess the progression of MCI and early AD.

**Passage 13:**

> orrespond to
left superior frontal gyrus, right middle frontal gyrus, right pars
orbitas, left supramarginal gyrus, left middle occipital gyrus,
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply. 2796
left inferior occipital gyrus, right lateral geniculate nucleus,
left medial geniculate nucleus and left inferior colliculus
respectively. 0 0.2 0.4 0.6 0.8 1
False Positive Rate
0
0.2
0.4
0.6
0.8
1
True Positive Rate
ROC Curve
AUC = 0.74095
AUC = 0.63149
AUC = 0.89313
Proposed 
technique
Centrality features 
      approach
Connection strength
 features approach
Fig. 4: Performance comparison of the classification frame-
work of the proposed study with those of the existing studies
E.

**Passage 14:**

> 2023 IEEE International Conference on Bioinformatics and Biomedicine
979-8-3503-3748-8/23/$31.00 ©2023 IEEE
2790
Structural Connectivity Analysis in Cognitive
Decline: Insights from Graph Theory and
Mass-Spring Modeling
Abdulyekeen T. Adebisi 1, Student Member, IEEE, Member, IEEE, Ho-Won Lee 2,3,
Kalyana C.

**Passage 15:**

> gyrus, right par triangularis, right lateral orbital gyrus, left
transverse temporal gyrus, left hippocampus, left amygdala,
left superior occipital gyrus and left superior colliculus re-
spectively. Similarly, the velocities and accelerations of network nodes
underwent comprehensive statistical evaluation. Notably, nine
network nodes demonstrated statistically significant differ-
ences among the experimental groups. To provide a concise
yet informative overview, we present the statistical analysis
results for velocities and accelerations from three network
nodes (see Fig. 3c and Fig. 3d), emphasizing the observed
distinctions in these dynamic parameters.

**Passage 16:**

> he formulated structural network,
one-way anova corrected for type-1 and type-2 errors using
Bonferroni post-hoc approach are performed on the measures
between the considered groups of NC, MCI and AD. Similarly,
regression analysis were done on the graph theory metrics and
the ages of the subjects in the respective groups. E. Classification
For classification of NC, MCI, and AD groups, a com-
prehensive set of features was extracted from graph theory
metrics and mass-spring model parameters . At the nodal level,
the clustering coefficient and participation coefficient were
computed, along with global and diffusion efficiency metrics
derived from network analysis. Additionally, model-based
parameters, including positions, velocities, accelerations, and
damping forces, were computed from the mass-spring model
simulation.

**Passage 17:**

> chniques, Diffusion Tensor Imag-
ing (DTI) has emerged as a powerful tool for investigating
the microstructural integrity of brain white matter [4], [5],
enabling the study of structural connectivity. DTI measures
the diffusion of water molecules in brain tissues, reflecting
the underlying fiber tracts and their organization. Graph theory analysis has gained prominence in the field
of neuroimaging due to its ability to comprehensively as-
sess brain connectivity patterns at a network level [6], [7]. In this context, the brain is represented as a complex net-
work, where nodes correspond to distinct brain regions, and
edges represent the white matter tracts connecting them. The
potential of graph theory analysis lies in its capability to
identify subtle alterations in brain connectivity associated
with neurodegenerative diseases, such as dementia.

**Passage 18:**

> tter
connectivity patterns in NC, MCI, and AD subjects. Color-
coded tractography visualizations provided valuable insights
into structural connectivity variations associated with cogni-
tive decline. Among the color-coded tracts, the green lines,
representing fiber tracts primarily oriented along the superior-
inferior (z-axis) direction [22], exhibited intriguing differences
across groups. In NC subjects, denser green lines (see Fig. 1a) indicated a higher density of white matter connections
between brain regions at the brain’s top and bottom, suggesting
intact superior-inferior pathways crucial for interhemispheric
communication and limbic system connectivity. Conversely,
MCI and AD subjects displayed reduced green line density,
implying potential alterations in superior-inferior white matter
pathways and disrupted tracts contributing to cognitive deficits.

**Passage 19:**

> ysis. Moreover, our exploratory analyses
have unveiled nuanced patterns in tract density, motivating
further investigation into specific tracts and their intricate
connections with cognitive function. These findings underscore the intricate interplay between
white matter connectivity and cognitive states, reinforcing the
imperative for comprehensive assessments of structural net-
works in the realm of neurodegenerative disorders. While our
study represents a substantial advancement, our work opens
up new avenues for future exploration, encompassing broader
dataset generalization, additional feature incorporation, and
refinement of the classification pipeline.

**Passage 20:**

> tates further
exploration. V. C ONCLUSION
This research study demonstrates the critical importance of
structural connectivity analysis for comprehending the neural
basis of dementia-related disorders. Leveraging graph theory
and mass-spring model techniques, we have gained profound
insights into the transformations occurring within white matter
tracts associated with cognitive decline in the context of
aging. The successful utilization of graph theoretic metrics and
mass-spring model parameters within a two-step classification
process, resulting in an accuracy of 82.7%, underscores the re-
markable potential of these combined techniques for in-depth
brain network analysis. Moreover, our exploratory analyses
have unveiled nuanced patterns in tract density, motivating
further investigation into specific tracts and their intricate
connections with cognitive function.

**Passage 21:**

> Conversely,
MCI and AD subjects displayed reduced green line density,
implying potential alterations in superior-inferior white matter
pathways and disrupted tracts contributing to cognitive deficits. The red lines, representing fiber tracts predominantly oriented
along the left-right (x-axis) direction [22], exhibited inter-
esting patterns. MCI and AD subjects demonstrated slightly
denser red lines than normal controls, suggesting adaptive or
compensatory mechanisms involving left-right connectivity in
response to cognitive decline. The increased density of red
lines in MCI and AD subjects could indicate efforts to estab-
lish alternative communication routes between hemispheres,
potentially compensating for neuronal loss or degradation of
other white matter pathways.

**Passage 22:**

> . Rubin, et al., “Network analysis of intrinsic
functional brain connectivity in alzheimer’s disease,” PLoS computa-
tional biology, vol. 4, no. 6, p. e1000100, 2008.
[25] C.-Y . Lo, P.-N. Wang, K.-H. Chou, et al., “Diffusion tensor tractography
reveals abnormal topological organization in structural cortical networks
in alzheimer’s disease,” Journal of Neuroscience , vol. 30, no. 50,
pp. 16876–16885, 2010. Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply.

**Passage 23:**

> nectogram for a subject
each from NC, MCI, and AD groups (Fig. 1a), with similar
patterns observed in other subjects. The tractogram analysis re-
vealed distinctive white matter connectivity patterns. Notably,
green lines (superior-inferior direction) appeared denser in NC
subjects, while red lines (left-right direction) were slightly
denser in MCI and AD subjects (Fig. 1). The blue lines
(anterior-posterior direction) also showed variations. Fig. 1b
demonstrated a decreasing structural connectivity density from
NC to MCI to AD groups. The results highlight the potential of
structural connectivity analysis to unveil differences in white
matter connectivity patterns across cognitive states. TABLE I: Statistical analysis of the graph measures at global
level across the NC, MCI and AD groups.

**Passage 24:**

> al
kernel as the classification algorithm. Fig. 4 shows the ROC
curves for the svm-based classification using our proposed
framework, centrality features and connection strength features
respectively. It is found that the classification of the dementia
disorder stages (AD, MCI) and NC groups using the features
extracted from the proposed approach (having AUC = 0.893)
outperformed those those done using the network centrality
features and network connection strengths (see Fig. 4). IV. D ISCUSSION
The tractogram analysis unveiled distinct white matter
connectivity patterns in NC, MCI, and AD subjects. Color-
coded tractography visualizations provided valuable insights
into structural connectivity variations associated with cogni-
tive decline.

</details>

---

## Tyagi et al. (2024) — Harnessing Machine Learning for Early Detection of Alzheimer’s Disease
_File: `Tyagi et al. - 2024 - Harnessing Machine Learning for Early Detection of Alzheimer’s Disease.pdf`_

1. **Yes**, diffusion MRI (specifically **diffusion tensor imaging (DTI)**) was used in this paper. The text explicitly mentions "diffusion tensor imaging (DTI)" and "Fractional Anisotropy (FA) scans, derived from DTI."

2. **Processing steps applied to diffusion images** (in order):  
   - "The FA data was motion-corrected and normalized to ensure consistency across subjects."  
   - "FA values were extracted from specific regions of interest (ROIs) using standard anatomical templates."

3. **Software or tools explicitly named**:  
   - **FSL** (used to convert NIfTI files to 2D JPEG formats).  
   - **ResNet 3D** and **LeNet** (convolutional neural networks applied to FA and sMRI data).  

4. **Acquisition/processing parameters explicitly reported**:  
   - No specific parameters (e.g., b-values, number of directions, voxel size, thresholds) are explicitly reported for diffusion MRI processing.  

5. **Exact sentences describing processing**:  
   - "The FA data was motion-corrected and normalized to ensure consistency across subjects."  
   - "FA values were extracted from specific regions of interest (ROIs) using standard anatomical templates."  
   - "The biomarker data was pre-processed by handling missing values through imputation. For categorical data (e.g., gender, diagnosis), label encoding was applied."  

6. **Is the processing description complete?**  
   The description is **complete** based on the excerpts provided. The steps explicitly mentioned (motion correction, normalization, ROI extraction) are fully detailed, and no additional steps are implied or required.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> s apply. B. Preprocessing 
Preprocessing of the neuroimaging data involved several 
steps. In this paper, first, the FA data was motion-corrected and 
normalized to ensure consistency across subjects. Next, the FA values were extracted from specific regions of 
interest (ROIs) using standard anatomical templates. These 
ROIs were chosen based on previous studies indicating their 
vulnerability to early AD-related changes. For the sMRI data, Voxel Based Morphometry(VBM) was 
used to measure gray matter volume in the hippocampus, 
entorhinal cortex, and other cortical areas. The images were 
normalized to the Montreal Neurological Institute (MNI) 
template, and gray matter volumes were extracted for statistical 
analysis. The biomarker data was pre-processed by handling missing 
values through imputation. For categorical data (e.g., gender, 
diagnosis), label encoding was applied.

**Passage 2:**

> Tensor Imaging (DTI) which were obtained from the 
portal of EU Open Research Repository, measure the diffusion 
of water molecules in the brain to provide insights into white 
matter (WM) integrity. High FA values are generally observed 
in healthy white matter, where water diffusion is highly 
directional along axonal fibres, while lower FA values indicate 
white matter degradation, which is often associated with 
pathological processes like Alzheimer’s disease (AD). Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 15,2026 at 22:36:44 UTC from IEEE Xplore. Restrictions apply. B. Preprocessing 
Preprocessing of the neuroimaging data involved several 
steps. In this paper, first, the FA data was motion-corrected and 
normalized to ensure consistency across subjects.

**Passage 3:**

> rative 
neurological condition that results in the deterioration of cognitive 
function. Early non-invasive detection is crucial for implementing 
timely interventions and slowing disease progression. In this 
research, we aimed to analyse the predictivity for classifying AD 
stages by integrating neuroimaging data —diffusion tensor 
imaging (DTI) and structural MRI (sMRI) —with clinical 
biomarkers. In this paper Fractional Anisotropy (FA)  scans, 
derived from DTI, denoting water molecule diffusion  in brain 
tissue was assessed , particularly in identifying early 
microstructural changes during the mild cognitive impairment 
(MCI) stage of AD. To progressively monitor the structural 
pathology of AD in patients,  OASIS sMRI dataset  was used.

**Passage 4:**

> e extracted for statistical 
analysis. The biomarker data was pre-processed by handling missing 
values through imputation. For categorical data (e.g., gender, 
diagnosis), label encoding was applied. A correlation analysis 
was performed to identify the most relevant biomarkers for 
classification tasks. The top 20 biomarkers were selected based 
on their correlation with cognitive scores and AD diagnosis. C. Model Deployment 
The machine learning model employed in this paper 
processed extensive 3D  imaging data from Fractional 
Anisotropy (FA) scans, 2D structural MRI (sMRI) from the 
OASIS dataset, and  tabulated clinical biomarkers to classify 
Alzheimer’s disease (AD) stages effectively. The process 
consisted of data acquisition, model selection, training and 
validation, and model optimization as represented in Fig. 2.

**Passage 5:**

> discussions. II. METHODOLOGY 
A. Dataset 
1) OASIS Dataset : The Open Access Series of Imaging 
Studies (OASIS) dataset , is a comprehensive resource widely 
used in Alzheimer's disease (AD) research. Established to 
facilitate the study of brain aging and neurodegenerative 
diseases, OASIS provides a rich collection of cross -sectional 
and longitudinal MRI data from a diverse cohort of subjects, 
including both healthy controls /non-demented(ND) and 
individuals diagnosed with various stages of Alzheimer's 
disease—Very Mild Demented (VMD), Mild Demented (MiD) 
and Moderate Demented (MoD). Our dataset comprised of 80,000 brain MRI images, which 
were used to study Alzheimer's disease progression. Original 
NIfTI files (.nii)  files were converted into  2D image formats  
like .jpeg using FSL and were made available through a GitHub 
repository.

**Passage 6:**

> re used to study Alzheimer's disease progression. Original 
NIfTI files (.nii)  files were converted into  2D image formats  
like .jpeg using FSL and were made available through a GitHub 
repository. For neural network training, the brain scans were 
sliced into 2D images, selecting slices 100 to 160 along the z -
axis for 461 patients. The OASIS dataset included T1-weighted 
structural MRI scans, along with associated clinical 
assessments such as the Clinical Dementia Rating (CDR) and 
Mini-Mental State Examination (MMSE) scores. Based on 
Clinical Dementia Rating (CDR) values, patients were 
classified into four stages: demented, very mild demented, mild 
demented, and non-demented. The final dataset, processed into 
JPEG format, totalled up to 1.3 GB, enabling robust 
Alzheimer’s detection analysis.

**Passage 7:**

> https://doi.org/10.1016/j.dscb.2021.100005. 
[19] Y. Sang and W. Li, "Classification Study of Alzheimer’s Disease 
Based on Self -Attention Mechanism and DTI Imaging Using 
GCN," in IEEE Access, vol. 12, pp. 24387 -24395, 2024, doi: 
10.1109/ACCESS.2024.3364545. Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 15,2026 at 22:36:44 UTC from IEEE Xplore. Restrictions apply.

**Passage 8:**

> s. TABLE I. PERFORMANCE OF OUR PROPOSED MODELS  
Datasets Performance 
Proposed Modality Accuracy 
OASIS sMRI 
CNN 99.7 
LeNet 99.3 
FA Scans ResNet18 3D 82.5 
Biomarkers Random Forest 90 
 
TABLE II. PERFORMANCE OF EXISTING STATE-OF-THE-
ART MODELS 
Datasets 
Performance 
Author and Year Existing 
Modality Accuracy 
OASIS sMRI 
Battineni et al. (2021) 
[17] 
Gradient 
boosting 97.58%, 
Islam J. et al, 2018[16] CNN 93% 
FA Scans 
Yida Qu et al, 2021[18] 
SVM, 
XGBoost, 
L.R. etc 
80.47% 
Y. Sang et al, 2024[19] 
Graph Conv. Network 78.6% 
Biomarkers 
Popuri et al., 2020 [15] ensemble-
learning 
AUC: 0.81(6 
Months), 
0.73(7 Yrs) 
Jo et al., 2020[13] CNN 90.8% 
 
The above Table 1 and Table 2 compare the performance 
accuracies of our models against the existing modalities, thus 
proving that our approach es are significantly detecting 
plausible diagnostics. B.

**Passage 9:**

> also used in model 
training. The dataset also includes information on medications 
taken, such as anti -hypertensives, antidepressants, and 
anticholinergics, which can influence cognitive outcomes. Other clinical factors such as age, education, and comorbidities 
(e.g., hypertension, d iabetes) further contextualize individual 
health profiles. This multidimensional dataset serves as a robust 
foundation for devel oping machine learning models aimed at 
improving early detection and understanding of Alzheimer’s 
disease progression. 3) Fractional Anisotropy (FA):  FA Scans , derived from 
Diffusion Tensor Imaging (DTI) which were obtained from the 
portal of EU Open Research Repository, measure the diffusion 
of water molecules in the brain to provide insights into white 
matter (WM) integrity.

**Passage 10:**

> S AND DISCUSSION 
A. Results 
The evaluation of the individual models for Fractional 
Anisotropy (FA), structural MRI (sMRI), and biomarker data 
was carried out using their respective  test datasets. Each 
modality was processed and modelled independently with the 
goal of future integration. Although a robust integrated model 
is still in progress, the initial results from individual models 
show promising accuracy, underscoring the potential of a 
multi-modal approach. 
(1) Fractional Anisotropy (FA) Model : The FA model 
assessed white matter integrity  in brain tissues which degrade 
overtime in AD patients . Significant differences in FA values 
across the Alzheimer’s Disease (AD ) progressive stages were 
identified, particularly in the cingulum bundle, uncinate 
fasciculus, and corpus callosum.

**Passage 11:**

> identifying early 
microstructural changes during the mild cognitive impairment 
(MCI) stage of AD. To progressively monitor the structural 
pathology of AD in patients,  OASIS sMRI dataset  was used. Convolutional neural networks (CNNs)  like ResN et 3D and 
LeNET were applied to analyse FA and sMRI data , achieving a 
significant accuracy score. In this proposed work, correlation and 
permutation analysis  was also applied on the blood biomarker  
data to extract relevant features . R andom Forest  classifier was 
then used on these biomarkers. The highly correlated biomarkers 
were later used to obtain a significant impact in identifying the 
various stages of Alzheimer’s progression. Keywords— Alzheimer's disease, Fractional Anisotropy (FA), 
Diffusion Tensor Imaging (DTI), Biomarkers, Magnetic Resonance 
Imaging (MRI), Early diagnosis 
I.

**Passage 12:**

> o 
underlying biological processes such as inflammation , toxic 
proteins and oxidative stress, complementing our imaging data. A multi -modal approach hence is  crucial for accurately 
diagnosing AD. This is understood because while FA reveal s 
early white matter changes, it lacks specificity for tracking gray 
matter atrophy. Conversely, sMRI provid es detailed structural 
information but at a much later stage where patients are usually 
symptomatic and miss the golden period of reverting back from 
the damage. It  misses early white matter abnormalities. Biomarkers, though effective for detecting underlying 
biological processes, cannot directly reveal structural changes 
in the brain. Therefore, integrating these modalities becomes 
necessary for a complete and accurate  early diagnosis, and we 
have laid the groundwork for   enabling a more effective 
diagnostic approach. IV.

**Passage 13:**

> measuring gray matter atrophy in 
regions such as the hippocampus and entorhinal cortex. Voxel-
Based Morphometry (VBM) revealed significant atrophy in 
MoD and M iD patients compared to ND subjects. The CNN 
models like LeNet and a custom variation achieved accuracies 
of 99.3% and 99.7% respectively in classifying  ND, VMD, 
MiD, and MoD subjects, confirming the importance of sMRI in 
detecting structural changes during later stages of AD. The 
performance metric curves are mentioned in Fig. 6 below. Fig. 5. (a)Training Accuracy and (b) Training Loss Curves of the LeNET 
Model Training and Validation. In t he Fig. 5, training curve s show rapid accuracy 
improvement within the first few epochs, reaching near-perfect 
performance by epoch 5, while the loss converges quickly.

**Passage 14:**

> ification accuracy, effectively identifying early -stage 
degeneration, especially in the transition from CN to MCI. Fig. 4. FA Scans Model training metrics using ResNet 3D for 150 epochs. In the Fig. 4 training curves show a steady decrease in loss 
and a gradual increase in accuracy, with the model approaching 
high performance after around 40 epochs and validation loss 
increased after an initial drop, indicating potential overfitting 
hence why Early Stopping was employed to curb the issue. 
(2) Gray Matter (GM) Model from Structural MRI:  The 
sMRI model focused on measuring gray matter atrophy in 
regions such as the hippocampus and entorhinal cortex. Voxel-
Based Morphometry (VBM) revealed significant atrophy in 
MoD and M iD patients compared to ND subjects.

**Passage 15:**

> mentia score: Independent validation on 8,834 
images from ADNI, AIBL, OASIS, and MIRIAD databases. Hum 
Brain Mapp . 2020; 41: 4127–
4147. https://doi.org/10.1002/hbm.25115 
[16] Islam, J., Zhang, Y. Brain MRI analysis for Alzheimer’s disease 
diagnosis using an ensemble system of deep convolutional neural 
networks. Brain Inf. 5, 2 (2018). https://doi.org/10.1186/s40708-
018-0080-3
 
[17] Battineni G, Hossain MA, Chintalapudi N, Traini E, Dhulipalla VR, 
Ramasamy M, Amenta F. Improved Alzheimer’s Disease Detection 
by MRI Using Multimodal Machine Learning 
Algorithms. Diagnostics.

**Passage 16:**

> g/10.1002/alz.12756 
[10] Qu, Y., et al.: AI4ad: artificial intelligence analysis for Alzheimer’s 
disease classification based on a multisite DTI database. Brain 
Disord. (2021). 
[11] Y. Sang and W. Li, "Classification Study of Alzheimer’s Disease 
Based on Self -Attention Mechanism and DTI Imaging Using 
GCN," in IEEE Access, vol. 12, pp. 24387 -24395, 2024, doi: 
10.1109/ACCESS.2024.3364545. 
[12] De, A.; Chowdhury, A.S. DTI based Alzheimer’s disease 
classification with rank modulated fusion of CNNs and random 
forest. Expert Syst. Appl. 2021, 169, 114338. Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 15,2026 at 22:36:44 UTC from IEEE Xplore. Restrictions apply. 
[13] Jo, T., Nho, K., Risacher, S.L.  et al. Deep learning detection of 
informative features in tau PET for Alzheimer’s disease 
classification.

**Passage 17:**

> tients . Significant differences in FA values 
across the Alzheimer’s Disease (AD ) progressive stages were 
identified, particularly in the cingulum bundle, uncinate 
fasciculus, and corpus callosum. These reductions in FA values 
suggest early white matter degeneration, a less utilised  early 
marker of Alzheimer’s. The FA model achieved 82.5% 
classification accuracy, effectively identifying early -stage 
degeneration, especially in the transition from CN to MCI. Fig. 4. FA Scans Model training metrics using ResNet 3D for 150 epochs. In the Fig.

**Passage 18:**

> or imaging (DTI), for instance, measures the 
diffusion of water molecules in brain tissues, providing 
valuable insights into w hite matter integrity through metrics 
like Fractional Anisotropy (FA). FA reflec ts early 
microstructural changes in white matter, which are among the 
first signs of AD. Similarly, structural MRI (sMRI) is crucial in 
assessing gray matter atrophy, especially in regions like the 
hippocampus, which is particularly vulnerable to early damage 
in AD. Recent studies have increasingly highlighted the 
benefits of integrating multiple imaging modalities, such as FA 
from DTI and sMRI data, to enhance diagnostic accuracy. Combining MRI and genetic data with machine learning 
models has also led to diagnostic accuracy rates as high as 90%, 
with models like ADD-NET demonstrating strong performance 
by optimizing multimodal data [1].

**Passage 19:**

> have demonstrated that FA measures can 
effectively distinguish between AD patients and healthy 
controls by analysing white matter integrity, which notably 
decreases as the disease progresses [ 10]. Machine learning 
methods have proven invaluable in analysing these 
relationships, revealing complex interactions between white 
matter integrity and cognitive function. Moreover, advanced  
models incorporating self -attention mechanisms with FA data 
have achieved high classification accuracy, particularly when 
focusing on brain regions specifically impacted by AD [ 11]. These findings, combined with sophisticated classification 
algorithms, further solidify FA's role in early AD detection, 
offering significant clinical potential [12].

**Passage 20:**

> functional abilities, and its pathological hallmarks, such as 
amyloid plaques and neurofibrillary tangles, often only become 
detectable after substantial and irreversible brain damage has 
occurred. This highlights the pressing need for early detection, 
as timely interventions may help slow disease progression and 
improve quality of life for those affected. Traditional diagnostic methods, such as clinical 
assessments and cognitive tests, often fail to detect AD in its 
earliest stages, when intervention would be most effective. To 
address this limitation, advanced neuroimaging techniques 
have become essential tools in AD research and diagnosis. Diffusion tensor imaging (DTI), for instance, measures the 
diffusion of water molecules in brain tissues, providing 
valuable insights into w hite matter integrity through metrics 
like Fractional Anisotropy (FA).

**Passage 21:**

> Correlation analysis were employed for feature extraction. Random Forest classifier was also tested for its robustness in 
handling high-dimensional data and its ability to rank feature 
importance. The final classifier was trained on the selected 
biomarkers and was evaluated based on accuracy, precision, 
Fig. 1. Fractional Anisotropy 40 longitudinal scan slices(128x128x45) 
 
Fig. 2  Research Methodology 
 
 
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 15,2026 at 22:36:44 UTC from IEEE Xplore. Restrictions apply. 
recall, and AUC -ROC (Area under the Receiver Operating 
Characteristic Curve). The datasets were divided into training, validation, and test 
sets using an 80 -20 split. The models were trained on the 
training set, validated on a separate validation set, and then 
tested on unseen data to evaluate their generalizability.

**Passage 22:**

> arious stages of Alzheimer’s progression. Keywords— Alzheimer's disease, Fractional Anisotropy (FA), 
Diffusion Tensor Imaging (DTI), Biomarkers, Magnetic Resonance 
Imaging (MRI), Early diagnosis 
I. INTRODUCTION 
Alzheimer’s disease (AD) is a progressive 
neurodegenerative disorder that affects millions of people 
worldwide, particularly the elderly. As the global population 
ages, the number of AD cases is expected to rise significantly, 
putting immense pressure on healthcare systems. AD is marked 
by a stead y decline in cognitive function and the loss of 
functional abilities, and its pathological hallmarks, such as 
amyloid plaques and neurofibrillary tangles, often only become 
detectable after substantial and irreversible brain damage has 
occurred.

**Passage 23:**

> n distinguishing between AD 
progression stages. Metrics such as accuracy, precision, recall, 
F1-score, and AUC -ROC were calculated to provide a 
comprehensive evaluation of the model's performance. These 
metrics are defined as: 
Accuracy = 
𝑇𝑃+𝑇𝑁
𝑇𝑃+𝑇𝑁+𝐹𝑃+𝐹𝑁, Precision = 
𝑇𝑃
𝑇𝑃+𝐹𝑃, Sensitivity = 
𝑇𝑃
𝑇𝑃+𝐹𝑁, 
 F1 score = 
2𝑇𝑃
2𝑇𝑃+𝐹𝑃+𝐹𝑁 
Where FP=False Positive, FN= False Negative, TP= True Positive, and TN= 
True Negative. The integration of multiple imaging modalities and 
biomarkers significantly enhanced the classification approach, 
highlighting the potential of a multi-modal technique for early 
Alzheimer's diagnosis. III. RESULTS AND DISCUSSION 
A. Results 
The evaluation of the individual models for Fractional 
Anisotropy (FA), structural MRI (sMRI), and biomarker data 
was carried out using their respective  test datasets.

**Passage 24:**

> Training and Validation. In t he Fig. 5, training curve s show rapid accuracy 
improvement within the first few epochs, reaching near-perfect 
performance by epoch 5, while the loss converges quickly. The 
alignment of training and validation metrics suggests effective 
learning without signs of overfitting.  
(3) Biomarker Model : The biomarker model utilized 
clinical data, including neuroinflammatory markers  (such as 
MMSE, Hippocampus, etc), which were pre-processed and 
standardized. The model achieved 90% accuracy, 
Fig.3. Basic structures of the ResNet 3D 
Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 15,2026 at 22:36:44 UTC from IEEE Xplore. Restrictions apply. 
demonstrating the significant role of biomarkers in 
distinguishing between CN, MCI, and AD stages. The results 
highlight the potential of modes for dianosis using  biomarker 
data. Fig.

</details>

---

## Unified Brain Network Representation Learning via Adaptive Multimodal Fusion for Alzheimer-s Disease Analysis
_File: `Unified Brain Network Representation Learning via Adaptive Multimodal Fusion for Alzheimer-s Disease Analysis.pdf`_

1. **Yes**, diffusion MRI (DTI) was used in this paper.  
2. **Processing steps applied to diffusion images**:  
   - Convert original DICOM-formatted DTI data to NIFTI format.  
   - Perform skull dissection, fiber bundle resampling, and head motion correction.  
   - Compute the fractional anisotropy (FA) coefficient through tensor model optimization via the least squares method.  
   - Apply voxel-wise dimension normalization to standardize DTI data into a fixed matrix size (91×109×91, 2 mm×2 mm×2 mm).  
3. **Software/tools explicitly named**:  
   - **PANDA** (for DTI preprocessing).  
4. **Reported parameters**:  
   - Voxel size: **2 mm × 2 mm × 2 mm**.  
5. **Exact sentences from excerpts**:  
   - *"we compute the fractional anisotropy (FA) coefficient through the tensor model optimization via the least squares method and output the DTI data."*  
   - *"Fiber bundle resampling standardized data acquisition to reduce noise introduced by irregular sampling."*  
   - *"Voxel-wise dimension normalization was applied to unify all subjects’ DTI data into a fixed matrix size, regulating data in terms of morphology and spatial position to minimize noise interference."*  
6. **Processing description completeness**:  
   The description is **incomplete**. While steps like data conversion, skull dissection, motion correction, FA calculation, and normalization are detailed, parameters such as **b-values**, **number of diffusion directions**, or **specific thresholds** are not explicitly reported.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> e resampling, and head motion correction. Subsequently,
we compute the fractional anisotropy (FA) coefﬁcient through
the tensor model optimization via the least squares method and
output the DTI data. After resampling, the voxel dimensions for
all subjects’ DTI were standardized to a 91× 109× 91 matrix,
with each voxel measuring 2 mm× 2 mm× 2 mm. Next, we
will construct a functional brain network for fMRI. Choose
AAL3.0 as the brain template, comprising 90 ROIs, with each
delineated as a brain network node. Preprocess using GRETNA
to obtain a time series of 90 ROIs. For DTI Noise Elimination
via PANDA, head motion correction was performed to rectify
artifacts caused by subjects’ head movements during scanning,
ensuring more accurate spatial positioning of the data. Fiber
bundle resampling standardized data acquisition to reduce noise
introduced by irregular sampling.

**Passage 2:**

> a for constructing multi-
modal brain networks. This is because these two types of data
contain the brain’s functional information and the structural in-
formation of white matter ﬁbers, respectively. The DTI and fMRI
imaging data were entirely obtained from the Alzheimer’s Dis-
ease Neuroimaging Initiative (ADNI)[38] public data repository
for the veriﬁcation of our suggested framework. This research
incorporated data from 325 subjects. A comprehensive summary
of subject details is presented in Table 1. This study used the PANDA[39] toolbox for raw DTI data pre-
processing. Firstly, convert the original DICOM-formatted DTI
data to NIFTI format data. Then perform skull dissection, ﬁber
bundle resampling, and head motion correction. Subsequently,
we compute the fractional anisotropy (FA) coefﬁcient through
the tensor model optimization via the least squares method and
output the DTI data.

**Passage 3:**

> ubjects’ head movements during scanning,
ensuring more accurate spatial positioning of the data. Fiber
bundle resampling standardized data acquisition to reduce noise
introduced by irregular sampling. V oxel-wise dimension nor-
malization was applied to unify all subjects’ DTI data into a
ﬁxed matrix size, regulating data in terms of morphology and
spatial position to minimize noise interference. The standard procedure from the GRETNA toolbox [40] was
utilized for the initial processing of fMRI data in the experiment. Initially, the functional time series signal undergoes ﬁltration,
with principal stages comprising magnetization balance calibra-
tion, magnetic head motion artifact correction, spatial normal-
ization, and bandpass ﬁltering within the range of 0.01 Hz and
0.08 Hz.

**Passage 4:**

> nt is final as presented, with the exception of pagination. Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply. JIANG et al.: UNIFIED BRAIN NETWORK REPRESENTA TION LEARNING VIA ADAPTIVE MULTIMODAL FUSION 7
TABLE II
RESULTS OF ABLA TIONSTUDY ON EACH BLOCK PROPOSED
was ﬁrst used to remove high-frequency and low-frequency
interferences, retaining effective frequency signals associated
with brain activities. Spatial normalization was employed to
unify the data spatial standard, while magnetic head motion
artifact correction addressed noise from head movements during
scanning. Detrending and other operations were conducted to
eliminate slow linear or nonlinear drifts in the data. B.

**Passage 5:**

> Kong. His current research inter-
ests include brain image computing, brain-computer
interface, and optimization theory. This article has been accepted for inclusion in a future issue of this journal. Content is final as presented, with the exception of pagination. Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply.

**Passage 6:**

> uble-Ph.D. degree in biomedical engineering as
a cotuttele student with Shanghai Jiao Tong Univer-
sity, Shanghai, China, and in computer science with
the University of Sydney, Sydney, NSW, Australia. Her current research interests include inverse problem
in medical imaging and image processing such as
MR/PET image reconstruction, image denoising, and
dictionary learning. This article has been accepted for inclusion in a future issue of this journal. Content is final as presented, with the exception of pagination. Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply.

**Passage 7:**

> 5, no. 4, pp. 869–877, 2005.
[39] Z. Cui, S. Zhong, P . Xu, Y . He, and G. Gong, “Panda: A pipeline toolbox for
analyzing brain diffusion images,” Front. Hum. Neurosci., vol. 7, no. 42,
2013, Art. no. 42.
[40] J. Wang, X. Wang, M. Xia, X. Liao, A. Evans, and Y . He, “Gretna: A
graph theoretical network analysis toolbox for imaging connectomics,”
Front. Hum. Neurosci. , vol. 9, 2015, Art. no. 386, doi: 10.3389/fn-
hum.2015.00386.
[41] J. Y uan et al., “Graph attention transformer network for multi-label image
classiﬁcation,” ACM Trans. Multimedia Comput. Commun. Appl., vol. 19,
no. 4, 2023, Art. no. 150.
[42] J. Xiao, L. Y ang, and S. Wang, “Graph isomorphism network
for materials property prediction along with explainability analy-
sis,” Comput. Mater . Sci. , vol. 233, 2024, Art. no. 112619, doi:
10.1016/j.commatsci.2023.112619.
[43] F. Salami, A. Bozorgi-Amiri, G. M. Hassan, R.

**Passage 8:**

> with principal stages comprising magnetization balance calibra-
tion, magnetic head motion artifact correction, spatial normal-
ization, and bandpass ﬁltering within the range of 0.01 Hz and
0.08 Hz. Then, 90 non-overlapping ROIs of brain regions were
parcellated using the Automatic Anatomical Labeling (AAL)
template. Finally, we normalized the time series signals to the
same length, obtaining a matrix for each participant with the
size of 90 × 187, indicative of the functional time series X. For fMRI Noise Elimination via GRETNA, band-pass ﬁltering
This article has been accepted for inclusion in a future issue of this journal. Content is final as presented, with the exception of pagination. Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply.

**Passage 9:**

> o. 20230146.
[18] M. Li, Y . Qin, F. Gao, W. Zhu, and X. He, “Discriminative analysis of
multivariate features from structural MRI and diffusion tensor images,”
Magn. Reson. Imag., vol. 32, no. 8, pp. 1043–1051, 2014.
[19] X. Tang, Y . Qin, J. Wu, M. Zhang, W. Zhu, and M. I. Miller, “Shape and
diffusion tensor imaging based integrative analysis of the hippocampus
and the amygdala in Alzheimer’s disease,” Magn. Reson. Imag.
, vol. 34,
no. 8, pp. 1087–1099, 2016.
[20] J. Y ang, Q. Zhu, R. Zhang, J. Huang, and D. Zhang, “Uniﬁed brain
network with functional and structural data,” inProc. Med. Image Comput. Comput. Assist. Interv.–MICCAI, 23rd Int. Conf. , Lima, Peru, Springer,
2020, pp. 114–123.
[21] Z. Qiu et al., “3D multimodal fusion network with disease-
induced joint learning for early Alzheimer’s disease diagnosis,” IEEE
T r a n s .M e d .I m a g ., vol. 43, no. 9, pp. 3161–3175, Sep.

**Passage 10:**

> Construction
To fully harness the sequential insights contained within fMRI
datasets, this paper constructs two functional brain networks
(FC), namely static brain networks and dynamic brain networks. Firstly, the 4D fMRI is subjected to standard brain network
templates to extract regional signals, and preprocessed to obtain
a time series of 90 ROIs. Subsequently, determine the Pearson
correlation coefﬁcient among ROIs to establish the static FC. To
investigate the dynamics of resting state FC, this paper adopts
the frequently applied sliding window method [34]. We choose
a ﬁxed-length time window and use the data points within that
Algorithm 1: Brain Network Analysis Process.
window to calculate dynamic FC. Window size and stride are
two hyperparameters of sliding windows.

**Passage 11:**

> DTI and fMRI via optimal
transport theory combined with a multi-channel spatio-temporal
graph convolutional network to extract spatio-temporal topolog-
ical features of dynamic brain networks [11]. J. Huang et al.
construct a brain network with functional connectivity from
fMRI as nodes and structural connectivity from DTI as edges,
fusing functional and structural connections via attention diffu-
sion and bilinear pooling [12]. Z. Qiu et al. integrate sMRI and
PET data through a Transformer-based multi-fusion joint learn-
ing module, capturing global inter-modal relationships, local
associations, and latent information via global-aware learning,
local-aware learning, and outer latent-space learning, respec-
tively, to achieve multimodal fusion[21]. B.

**Passage 12:**

> ss propagation model for
dynamic brain network classiﬁcation,” IEEE Trans. Med. Imag. , vol. 43,
no. 6, pp. 2381–2394, Jun. 2024, doi: 10.1109/TMI.2024.3363014.
[12] J. Huang, L. Zhou, L. Wang, and D. Zhang, “Attention-diffusion-bilinear
neural network for brain network analysis,” IEEE Trans. Med. Imag. ,
vol. 39, no. 7, pp. 2541–2552, Jul. 2020.
[13] Y . Y ang et al., “Brainmass: Advancing brain network analysis for diag-
nosis with large-scale self-supervised learning,” IEEE Trans. Med. Imag.,
vol. 43, no. 11, pp. 4004–4016, Nov. 2024.
[14] Z. Dong et al., “Brain-jepa: Brain dynamics foundation model with gra-
dient positioning and spatiotemporal masking,” in Proc. 38th Int. Conf. Neural Inf. Process. Syst. . Red Hook, NY , USA: Curran Associates Inc.,
2025, pp. 86048– 86073.
[15] L.

**Passage 13:**

> agnetic head motion
artifact correction addressed noise from head movements during
scanning. Detrending and other operations were conducted to
eliminate slow linear or nonlinear drifts in the data. B. Experiment Settings
This model undergoes training and testing on the PyTorch
framework, utilizing NVIDIA RTX 4000 GPU hardware along
with 20 GB of graphics memory. Throughout the training phase,
the optimization algorithm is conﬁgured as Adam, initiated
with a starting learning rate of 0.0001, experiencing exponential
decay relative to the training iteration count. The number of
epochs is 400, and the batch size is conﬁgured for a total of 32. The experiment adopts a ﬁve-fold cross-validation to assess the
model’s efﬁcacy. Five subsets of the same size were divided from
all participants.

**Passage 14:**

> 2] H. Cui et al., “Braingb: A benchmark for brain network analysis with graph
neural networks,” IEEE Trans. Med. Imag. , vol. 42, no. 2, pp. 493–506,
Feb. 2023.
[33] E. T. Rolls, C. -C. Huang, C. -P . Lin, J. Feng, and M. Joliot, “Automated
anatomical labelling atlas 3,”Neuroimage, vol. 206, 2020, Art. no. 116189,
doi: 10.1016/j.neuroimage.2019.116189.
[34] S. Shakil, C. -H. Lee, and S. D. Keilholz, “Evaluation of sliding window
correlation performance for characterizing dynamic functional connec-
tivity and brain states,” Neuroimage, vol. 133, pp. 111–128, 2016, doi:
10.1016/j.neuroimage.2016.02.074.
[35] N. Ma, X. Zhang, H. -T. Zheng, and J. Sun, “Shufﬂenet v2: Practi-
cal guidelines for efﬁcient CNN architecture design,” in Proc. Com-
put. Vis.–ECCV 2018 , V . Ferrari, M. Hebert, C. Sminchisescu, and Y . Weiss, Eds., Cham, Switzerland: Springer International Publishing, 2018,
pp.

**Passage 15:**

> challenge within
the realms of neuroscience and computational neuroscience,
aiming to deduce the network topology and functional connec-
tivity patterns among brain regions from neuroimaging datasets. Speciﬁcally, brain network construction tools generally take raw
neuroimaging data as input, and generate a brain network for
each input sample through a series of processes such as data
preprocessing, template registration and segmentation, and fea-
ture extraction. According to the commonly used AAL brain re-
gion [33] partitioning method in neuroscience, the output result
is a two-dimensional adjacency matrixA ∈R
90×90 representing
the brain network connections. A. Functional Brain Network Construction
To fully harness the sequential insights contained within fMRI
datasets, this paper constructs two functional brain networks
(FC), namely static brain networks and dynamic brain networks.

**Passage 16:**

> Assuming that the time series of a preprocessed individual
subject is represented as a matrixX that measures N× T, where
N =9 0 represents the BOLD signal composition with a longer
T time in 90 ROIs. The static functional connection is obtained
from the following equation:
SFC
ij = Cov (Xi,X j )
σXiσXj
= E
(
(Xi −μXi )
(
Xj −μXj
))
σXiσXj
(1)
For dynamic functional connections, by setting different win-
dow sizes w, we obtain a matrix Xw with a size of N ×w. Using the same calculation method, we obtain a set of dynamic
This article has been accepted for inclusion in a future issue of this journal. Content is final as presented, with the exception of pagination. Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply.

**Passage 17:**

> nt is final as presented, with the exception of pagination. Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply. JIANG et al.: UNIFIED BRAIN NETWORK REPRESENTA TION LEARNING VIA ADAPTIVE MULTIMODAL FUSION 5
functional connectivity matrices{DFC 1,DFC 2,...,DFC k}. DTI is used to extract node features, and sparse encoding fea-
ture FN×d is obtained through adaptive quantization encoder. Denote A0 = SFC 90×90, Ai = DFC i(1 ≤i ≤k).B yu s i n g
functional connections as edges of the graph and encoding
features as nodes of the graph, i.e. Gi =( Ai,F ), a multi-layer
brain network G = G0,G 1,G 2,...,G k is formed. B. Adaptive Quantization Encoder
The Adaptive Quantization Encoder (AQE) plays a pivotal
role in processing and analyzing Diffusion Tensor Imaging data.

**Passage 18:**

> network reconstruction. The AQE incorporates a novel mechanism to adaptively
weight quantization-level features by computing their complex-
ity as weights, which are derived using entropy calculation. Dynamic weight adjustment is achieved through Equation (3) in
combination with feature-speciﬁc entropy values. This enables
the Structure-Function Fusion Learning module to prioritize
features with higher information content. This is particularly
important in capturing the intricate ﬁber structures in DTI,
which are critical for accurate brain connectivity analysis. The
quantization process can be mathematically represented as:
Q(f
i)= round
( fi −min(F )
max(F )−min(F ) · (L−1)
)
(2)
whereQ(fi) is the quantized feature, fi is the i-th feature in the
feature set F , and L is the number of quantization levels.

**Passage 19:**

> backbone network. Through this adaptive quantization, we have achieved person-
alized attention to different features and improved the learning
ability of neural networks on high-dimensional DTI data. The core operational principle of the AQE revolves around
the adaptive adjustment of the quantization weights, which are
tailored based on the complexity and variability of the feature
vectors extracted from the DTI scans. This adaptability ensures
that more complex regions receive a detailed quantitative rep-
resentation, enhancing the ﬁdelity and utility of the encoded
features for brain network reconstruction. The AQE incorporates a novel mechanism to adaptively
weight quantization-level features by computing their complex-
ity as weights, which are derived using entropy calculation.

**Passage 20:**

> brain network G = G0,G 1,G 2,...,G k is formed. B. Adaptive Quantization Encoder
The Adaptive Quantization Encoder (AQE) plays a pivotal
role in processing and analyzing Diffusion Tensor Imaging data. AQE extracts structural features from DTI as node features of the
functional brain network, and collaborates with the downstream
structure-function fusion module to achieve full integration
of structural and functional information. This enables the
constructed multimodal brain network to fully characterize the
brain features of AD. Additionally, AQE transforms the contin-
uous structural features of DTI data into discrete layers through
quantization operations. This process can highlight the discrete
changes in brain region structural connections caused by AD,
thereby enhancing the AD brain features.

**Passage 21:**

> Finally, the calculated results for all samples
Fig. 8. Brain network analysis in NC(blue) and AD(orange) populations on
multiple indicators, from left to right, are CPL, CC, GE, and LE, respectively. The horizontal coordinate of each subgraph represents the threshold selected
for binarization of the brain network, the vertical coordinate is the result in the
corresponding dimension, and the box plot is used to represent the mean, upper
quartile and lower quartile in each group. This article has been accepted for inclusion in a future issue of this journal. Content is final as presented, with the exception of pagination. Authorized licensed use limited to: OAKLAND UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply. JIANG et al.: UNIFIED BRAIN NETWORK REPRESENTA TION LEARNING VIA ADAPTIVE MULTIMODAL FUSION 11
are presented in Fig. 8.

**Passage 22:**

> D UNIVERSITY. Downloaded on February 19,2026 at 19:41:57 UTC from IEEE Xplore. Restrictions apply. JIANG et al.: UNIFIED BRAIN NETWORK REPRESENTA TION LEARNING VIA ADAPTIVE MULTIMODAL FUSION 3
Fig. 1. The AMFusion framework’s network design comprises three sub-modules: (a) Functional connectivity construction and DTI encoding, (b) struc tural-
functional fusion learning, and (c) classiﬁer and brain network analysis.
through the method of low-rank representation, and also to
integrate local manifolds from structural data into the model
at the same time. Q. Zhu et al. fused DTI and fMRI via optimal
transport theory combined with a multi-channel spatio-temporal
graph convolutional network to extract spatio-temporal topolog-
ical features of dynamic brain networks [11]. J.

**Passage 23:**

> data into discrete layers through
quantization operations. This process can highlight the discrete
changes in brain region structural connections caused by AD,
thereby enhancing the AD brain features. Our AQE leverages
a customized lightweight neural network, ShufﬂeNetV2 [35],
as its backbone, selected for its computational efﬁciency and
its ability to adaptively adjust the weight of quantized features. Fig. 1 illustrates a conceptual representation of the enhancement
of the convolutional method through the backbone network. Through this adaptive quantization, we have achieved person-
alized attention to different features and improved the learning
ability of neural networks on high-dimensional DTI data.

**Passage 24:**

> formation support is provided for the early
diagnosis, treatment, and mechanism analysis of these brain
diseases [16], [17] like Alzheimer’s disease, Parkinson’s disease,
and autism spectrum disorder. The principal novelties of this approach are listed below:
1) The proposed methodology is a novel adaptive multilevel
brain network construction method that fuses DTI and
static and dynamic FC from fMRI. Dynamic FC has
been demonstrated to introduce temporal information into
multimodal brain networks. 2) The adaptive quantization encoding scheme is designed
for DTI feature extraction, and its core mechanism, Mixup
strategy, can effectively augment training data. Adaptive
weighting is employed to reduce overﬁtting in small sam-
ple training, enabling personalized attention to diverse
features and ultimately enhancing the generalization ca-
pability of brain network construction.

</details>

---

## Wu et al. (2025) — ENHANCING ALZHEIMER'S DISEASE DIAGNOSIS A NOVEL LOW-HRNET APPROACH FOR IMPROVED CLASSIFICATION
_File: `Wu et al. - 2025 - ENHANCING ALZHEIMER'S DISEASE DIAGNOSIS A NOVEL LOW-HRNET APPROACH FOR IMPROVED CLASSIFICATION.pdf`_



<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> n the
author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or
republish, to post on servers or to redistribute to lists, requires prior specific permission
and/or a fee. Request permissions from permissions@acm.org. EITCE 2024, Haikou, China
© 2024 Copyright held by the owner/author(s). Publication rights licensed to ACM. ACM ISBN 979-8-4007-1009-4/2024/10
https://doi.org/10.1145/3711129.3711390
ACM Reference Format:
Hongfeng Wu, Weiming Lin, and Pan Liu. 2024. ENHANCING
ALZHEIMER’S DISEASE DIAGNOSIS: A NOVEL LOW-HRNET AP-
PROACH FOR IMPROVED CLASSIFICATION. In 2024 8th International
Conference on Electronic Information Technology and Computer Engineering
(EITCE 2024), October 18–20, 2024, Haikou, China.

**Passage 2:**

> uracy. Yu
et al[5] used software to align, classify tissues, and correct bias in
sMRI images, then trained them using a 3D ResNet-101 network,
achieving a higher classification accuracy for AD and NC. Zhen et
al[6] used a VGG (Vision Geometrical Group) 16 network to extract
detailed features from sMRI images, combining them with high-
resolution features and using a sliding attention mechanism to fuse
1564

EITCE 2024, October 18–20, 2024, Haikou, China Hongfeng Wu et al.
features with different window sizes, achieving up to 77.2% clas-
sification accuracy for AD/MCI.

**Passage 3:**

> classification is performed using cranial sMRI images that
have been simply preprocessed, the classification accuracy reaches
94.53%, which is a significant improvement over the original CNN
network. Acknowledgments
This work was supported by Fujian Provincial Natural Science
Foundation of China [grant number 2022J011271, 2023I0044]. References
[1] Alzheimer’s Disease Facts and Figures. Alzheimer’s & Dementia; Alzheimer’s
Association’s Publication & Wiley: Chicago, IL, USA, 2023.
[2] Rajput, A. Does essential tremor increase the risk of dementia? No. Int. Rev. Neurobiol. 2022, 163, 233–253.
[3] Rasmussen, J.; Langerman, H. Alzheimer’s Disease-Why We Need Early Diagno-
sis. Degener. Neurol. Neuromuscul. Dis. 2019, 9, 123–130.
[4] Wang. B., Wu. H., R. Koo, Rui, E. Jingbo, and He, S. H.. (2023). Alzheimer’s
disease classification network based on improved resnet.

**Passage 4:**

> classification
accuracy for AD patients is realized by adopting a shallower net-
work, fewer number of channels, and occupying less computing
space. However, there are some shortcomings in this paper. The model
structure optimization reduces computational costs, but still relies
1567
ENHANCING ALZHEIMER’S DISEASE DIAGNOSIS: A NOVEL LOW-HRNET APPROACH FOR IMPROVED CLASSIFICATION EITCE 2024, October 18–20, 2024, Haikou, China
on high-performance computing resources, which may limit its
application in resource-limited environments. In this paper, only sMRI images are used as the basis for training
and testing. Nowadays, there are more types of diagnostic images
for Alzheimer’s disease, such as DTI (Diffusion Tensor Imaging),
fMRI, and PET, among others. Additionally, other multimodal im-
ages are used in the clinical diagnosis of AD.

**Passage 5:**

> e
model has the advantage of being able to extract effective features
from MRI images and then use a data-driven approach to assess the
associated neurodegenerative processes and cognitive impairment. Translated with www.DeepL.com/Translator (free version) It
achieves an accuracy of over 80% in predicting Alzheimer’s diag-
noses. 2.2 Deep Learning for AD Diagnosis
In recent years, with the continued increase in GPU processing
power and the fact that deep learning techniques no longer rely on
manual feature extraction, this field has grown rapidly and is now
widely used in medical image-assisted diagnostic procedures. As an
example, Antony first proposed[ 16] two novel models, one named
VGG16 and the other modelled as VGG19, aimed at diagnosing
Alzheimer’s disease. 2.3 Dual Attention
In recent years, some authors have proposed a new dual attention
mechanism in scene segmentation tasks.

**Passage 6:**

> ssing, feature
extraction, model training, classification and prediction, interpre-
tation, and optimization. Some machine learning algorithms have
been applied to AD diagnostics with notable results. As an illus-
tration, Martinez-Murcia et al[ 15] designed a CAE framework that
analyses collected data related to Alzheimer’s disease through the
use of a deep convolutional autoencoder, which has the advantage
of being able to extract effective features from MRI images, which
in turn allows for a data-driven approach to the assessment of as-
sociated neurodegenerative processes and cognitive deficits. The
model has the advantage of being able to extract effective features
from MRI images and then use a data-driven approach to assess the
associated neurodegenerative processes and cognitive impairment.

**Passage 7:**

> ng attention mechanism to fuse
1564

EITCE 2024, October 18–20, 2024, Haikou, China Hongfeng Wu et al.
features with different window sizes, achieving up to 77.2% clas-
sification accuracy for AD/MCI. Faizal et al[ 7] used an improved
Siamese network based on the VGG16 network to fuse features
from PET (Positron Emission Tomography), MRI (Magnetic reso-
nance imaging), and fMRI (Functional magnetic resonance imaging)
images, subsequently using three CNN networks and a triple loss
function for training, achieving an accuracy of 91.83% for disease
classification. Gowhar et al[ 8] used a transfer learning approach,
achieving a high accuracy for multi-classification of aligned sMRI
images after pre-training VGG16 and ResNet50 networks. T.

**Passage 8:**

> Ortiz, J.M. Gorriz, J. Ramirez, D. Castillo-Barnes, Study-
ing the manifold structure of Alzheimer’s disease: a deep learning approach
using convolutional autoencoders. IEEE J. Biomed. Health Inform. 24(1), 17–26
(2019)
[16] Antony F, Anita HB, George JA (2023) Classification on Alzheimer’s Disease MRI
Images with VGG-16 and VGG-19, vol. 312.
[17] Wang J, Sun K, Cheng T, et al. Deep high-resolution representation learning
for visual recognition[J]. IEEE transactions on pattern analysis and machine
intelligence, 2020, 43(10): 3349-3364.
[18] Szegedy C, Liu W, Jia Y, et al. Going deeper with convolutions[C]//Proceedings
of the IEEE conference on computer vision and pattern recognition. 2015: 1-9. 1568

**Passage 9:**

> pes of diagnostic images
for Alzheimer’s disease, such as DTI (Diffusion Tensor Imaging),
fMRI, and PET, among others. Additionally, other multimodal im-
ages are used in the clinical diagnosis of AD. Therefore, we can
consider using the same network to extract information from dif-
ferent types of data and modalities, allowing this information to
interact within the network to develop a model that can recog-
nize Alzheimer’s disease earlier in a multiclassification task. This
model can help patients detect the disease sooner and formulate
appropriate treatment plans. 6 CONCLUSION
This paper presents an enhancement of a shallow convolutional neu-
ral network inspired by HRNet, which maintains high-resolution
features while also capturing low-resolution information.

**Passage 10:**

> ar. However, there are specific measures that can be taken
to slow the progression of the disease[ 2]. Timely and accurate
medical diagnosis is critical to curbing the progression of the dis-
ease[3]. Thus, investigating automated diagnostic methods has
become particularly important. Neuroimaging technology is one of the effective ways to achieve
auxiliary diagnosis of Alzheimer’s disease (AD). structural mag-
netic resonance imaging (sMRI) provides clear three-dimensional
anatomical images of the brain and is commonly used to study
changes in brain tissue and structure, sMRI has the advantages of
being non-invasive, having high spatial resolution, and providing
high contrast, making it well-suited for recording disease data in
AD patients.

**Passage 11:**

> work. 2 RELATED WORKS
Using artificial intelligence algorithms based on neuroimaging
and clinical data, computer-aided diagnosis of Alzheimer’s dis-
ease involves grouping individuals into categories. Classification
approaches include of binary classification [ 10], multistage classifi-
cation [11], [12], and AD onset prediction [13], [14]. Computer-aided diagnosis of Alzheimer’s disease using artificial
intelligence algorithms based on neuroimaging and clinical data
involves classifying individuals. Commonly, there are binary clas-
sifications and multivariate classifications. Binary classification
involves distinguishing between NC vs. AD, NC vs. MCI, and
MCI vs. AD.

**Passage 12:**

> 469
[9] Illakiya, T.; Ramamurthy, K.; Siddharth, M.V.; Mishra, R.; Udainiya, A. AHANet:
Adaptive Hybrid Attention Network for Alzheimer’s Disease Classification Using
Brain Magnetic Resonance Imaging. Bioengineering 2023, 10, 714. https://doi.
org/10.3390/bioengineering10060714
[10] Meng, X., Liu, J., Fan, X., Bian, C., Wei, Q., Wang, Z., Liu, W., & Jiao, Z. (2022). Multi-modal neuroimaging neural network-based feature detection for diagnosis
of Alzheimer’s disease. Frontiers in Aging Neuroscience, 14, 911220.
[11] Zhang, J., He, X., Liu, Y., Cai, Q., Chen, H., & Qing, L. (2023). Multi-modal
cross-attention network for Alzheimer’s disease diagnosis with multi data.
[12] Xu, Z., Deng, H., Liu, J., & Yang, Y. (2021). Diagnosis of Alzheimer’s disease based
on the modified Tresnet. Electronics, 10(16), 1908.
[13] Park, S., Hong, C. H., Lee, D., Park, K., & Shin, H. (2023).

**Passage 13:**

> disease
classification. Gowhar et al[ 8] used a transfer learning approach,
achieving a high accuracy for multi-classification of aligned sMRI
images after pre-training VGG16 and ResNet50 networks. T. Illakiya
et al[9] used the DenseNet-169 network and introduced an adap-
tive hybrid attention network to enhance non-local attention and
coordinate point-out attention features, achieving high-precision
resolution for MCI/AD. Based on the traditional CNN network
model, this essay optimizes the network model to generate a new
HRNet network, aiming to achieve higher accuracy of Alzheimer’s
disease binary classification recognition results.

**Passage 14:**

> n accuracy by 1.44% compared to the original CNN
network. Ablation experiments show that the dual attention module
and the inception structure improve Low-HR accuracy by 2.97%
and 2.81%, respectively. 5 DISCUSSION
The advantage of this paper in its application to dichotomous dis-
crimination of Alzheimer’s disease is that it does not require cranial
stripping, alignment, and other operations, thus reducing opera-
tional complexity. Meanwhile, the improvement of classification
accuracy for AD patients is realized by adopting a shallower net-
work, fewer number of channels, and occupying less computing
space. However, there are some shortcomings in this paper.

**Passage 15:**

> 6 CONCLUSION
This paper presents an enhancement of a shallow convolutional neu-
ral network inspired by HRNet, which maintains high-resolution
features while also capturing low-resolution information. Addi-
tionally, the concept of inception is incorporated to optimize the
internal architecture of the network, allowing for an increase in its
width without adding depth, thereby improving the network’s infor-
mation extraction capabilities. Furthermore, this study employs a
dual attention mechanism that demonstrates superior performance
compared to two separate single-attention mechanisms. When
NC/AD classification is performed using cranial sMRI images that
have been simply preprocessed, the classification accuracy reaches
94.53%, which is a significant improvement over the original CNN
network.

**Passage 16:**

> tions, the computational cost is reduced while
preserving high-resolution features. Additionally, the introduction
of the Dual Attention mechanism further enhances the feature ex-
traction capability. The results of the experiments demonstrate
that the enhanced Low-HRNet reached an accuracy of 94.53% in
classifying Alzheimer’s disease (AD) versus NC (normal control),
representing a significant improvement compared to the 88.14%
accuracy achieved by the conventional CNN network. The experi-
mental results show that the accuracy of automatic classification of
Alzheimer’s disease can be effectively improved by optimising the
network structure and introducing an advanced attention mecha-
nism. CCS Concepts
• Computer systems organization → Architectures; Other ar-
chitectures; Neural networks.

**Passage 17:**

> network model. Unlike the original HRNet, the network used in this paper em-
ploys cross-fusion resolution for 1/2-size images after downsam-
pling the initial image once to reduce computational cost. It retains
the feature maps with the smallest resolution in the output stage
of the network and downsamples the larger feature maps in other
channels, splicing them with the smallest feature maps. The specific
workflow of the network (hereafter referred to as Low-HRNet) is
as follows. The complete sMRI image enters the first layer of the network
after one downsampling in the residual module. The Inception Res
Structure is used to expand the number of channels. In the second
stage of the network, the 1/2-size image is downsampled again
after channel expansion, and feature fusion is performed on the
two resolutions in a crosswise manner.

**Passage 18:**

> brain tissue and structure, sMRI has the advantages of
being non-invasive, having high spatial resolution, and providing
high contrast, making it well-suited for recording disease data in
AD patients. Deep learning can extract necessary information from
both local and global aspects of an image in an interrelated manner,
so it can used for AD diagnosis. Networks such as CNN, ResNet
(Residual Network), and DenseNet (Dense Convolutional Network)
have been frequently applied to the classification task of AD. How-
ever, traditional CNN networks often encounter low classification
performance when the network depth is shallow. As the network
depth increases, training time also rises, without a definite guaran-
tee of improved classification results.

**Passage 19:**

> shown in
Figure 2, the network contains 4 downsampling operations, in order
for the network to extract enough feature information, where each
downsampling operation contains 2 convolution operations. To enhance the accuracy of binary classification outcomes for
Alzheimer’s disease diagnosis, the CNN model was optimized and
improved by using dual attention modules and cross-fusion of fea-
ture maps with different resolutions. The optimized network model
is shown in Figure 3. 1565
ENHANCING ALZHEIMER’S DISEASE DIAGNOSIS: A NOVEL LOW-HRNET APPROACH FOR IMPROVED CLASSIFICATION EITCE 2024, October 18–20, 2024, Haikou, China
Figure 1: Inception structure. Figure 2: Traditional CNN network model. Unlike the original HRNet, the network used in this paper em-
ploys cross-fusion resolution for 1/2-size images after downsam-
pling the initial image once to reduce computational cost.

**Passage 20:**

> th an initial learning rate of
0.0001 and a weight decay of 5e-4. The training mode maintained
1566
EITCE 2024, October 18–20, 2024, Haikou, China Hongfeng Wu et al. Figure 3: Low-HRNet network model. Table 1: Dichotomization of AD diagnosis using different network models
Method Accuracy Precision Recall F1 AUC
CNN 88.14% 88.06% 87.98% 0.8802 0.8797
CNN+Attention 90.83% 90.77% 91.08% 0.9081 0.9108
CNN+Inception 91.84% 91.65% 91.84% 0.9173 0.9184
CNN+Attention+Inception 92.33% 92.21% 91.99% 0.9210 0.9199
Low-HR 89.58% 90.28% 88.34% 0.8903 0.8834
Low-HR+DualAttention 92.55% 92.64% 92.42% 0.9251 0.9242
Low-HR+Inception 92.39% 92.48% 92.43% 0.9239 0.9243
Low-HR+DualAttention+Inception 94.53% 94.67% 94.35% 0.9448 0.9435
model results based on the lowest validation set loss within 60
epochs, and the experimental test set was used to evaluate accuracy
and F1-score.

**Passage 21:**

> ly improved by optimising the
network structure and introducing an advanced attention mecha-
nism. CCS Concepts
• Computer systems organization → Architectures; Other ar-
chitectures; Neural networks. Keywords
Alzheimer’s disorder, binary diagnosis, feature fusion, hierarchical
neural architecture
∗Corresponding author
Permission to make digital or hard copies of all or part of this work for personal or
classroom use is granted without fee provided that copies are not made or distributed
for profit or commercial advantage and that copies bear this notice and the full citation
on the first page. Copyrights for components of this work owned by others than the
author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or
republish, to post on servers or to redistribute to lists, requires prior specific permission
and/or a fee.

**Passage 22:**

> y the gradual loss of cognitive and mem-
ory functions, which places a significant burden on patients and
their families. Therefore, early diagnosis and effective treatment
are particularly important. The aim of this paper is to explore
the improvement in classification accuracy for AD (Alzheimer’s
Disease) patients by enhancing the artificial neural network struc-
ture and introducing a new attention mechanism without increas-
ing the depth of the CNN network. A novel network structure
called Low-HRNet (high-resolution network) is proposed, which
combines a HRNet with an inception module for more efficient
information extraction. By cross-fertilizing feature information
at different resolutions, the computational cost is reduced while
preserving high-resolution features. Additionally, the introduction
of the Dual Attention mechanism further enhances the feature ex-
traction capability.

**Passage 23:**

> reduced to 1/16 of
its original size, is produced through the dual attention module for
feature enhancement, followed by adaptive global average pooling
and classification via a fully connected layer. 4 EXPERIMENTS AND RESULTS
The experimental platform used an NVIDIA GeForce RTX 3090
GPU, and the optimizer selected was the RAdam optimizer. The
loss function was cross-entropy loss, with an initial learning rate of
0.0001 and a weight decay of 5e-4. The training mode maintained
1566
EITCE 2024, October 18–20, 2024, Haikou, China Hongfeng Wu et al. Figure 3: Low-HRNet network model.

**Passage 24:**

> aditional CNN network
model, this essay optimizes the network model to generate a new
HRNet network, aiming to achieve higher accuracy of Alzheimer’s
disease binary classification recognition results. The key points of
this paper are outlined as detailed below:
1) HRNet adds a cross-fertilization module for low-resolution and
high-resolution feature information to the traditional CNN, pre-
serving high-resolution features while extracting low-resolution
information. 2) The network structure is internally refined using the Inception-
Res structure, and the dual attention mechanism from the Dual
Attention Net is introduced into the network. 2 RELATED WORKS
Using artificial intelligence algorithms based on neuroimaging
and clinical data, computer-aided diagnosis of Alzheimer’s dis-
ease involves grouping individuals into categories.

</details>

---

## Zuo et al. (2023) — Alzheimer’s Disease Prediction via Brain Structural-Functional Deep Fusing Network
_File: `Zuo et al. - 2023 - Alzheimer’s Disease Prediction via Brain Structural-Functional Deep Fusing Network.pdf`_

1. **Yes**, diffusion MRI (DTI) was used in this paper. The paper explicitly states: "Each patient was scanned with both DTI and fMRI."

2. **Processing steps applied to diffusion images** (DTI):  
   - "Successive convolutional filters on the DTI. Specifically, we first design four down-sampling convolutional operations with a kernel size of 3 × 3 × 3 and a stride of 2 to extract local feature maps. The extracted feature maps are then passed through 1 × 1 × 1 filters to fix the channel at N. Finally, each channel map is combined with the brain anatomical information (x, y, z, v) to align the features for each brain region."

3. **Software or tools explicitly named**:  
   - "Using the DPARSF toolkit" (for fMRI preprocessing).

4. **Acquisition or processing parameters explicitly reported**:  
   - Kernel size: 3 × 3 × 3  
   - Stride: 2  
   - Channel fixing: "fix the channel at N"  
   - Learning rate: 0.001  
   - Weight decay: 0.01  
   - No explicit mention of b-values, number of directions, voxel size, or thresholds.

5. **Exact sentences from the excerpts**:  
   - "Using the DPARSF toolkit, the top 20 volumes are eliminated, followed by head motion correction, band-pass filtering, Gaussian smoothing, and extracting the time series of all voxels."  
   - "Successive convolutional filters on the DTI. Specifically, we first design four down-sampling convolutional operations with a kernel size of 3 × 3 × 3 and a stride of 2 to extract local feature maps. The extracted feature maps are then passed through 1 × 1 × 1 filters to fix the channel at N. Finally, each channel map is combined with the brain anatomical information (x, y, z, v) to align the features for each brain region."

6. **Is the processing description complete?**  
   The description is **complete** based on the excerpts provided. The steps for DTI processing are explicitly detailed, and no additional parameters (e.g., b-values, voxel size) are required for the analysis described.

<details>
<summary>Retrieved passages (24 chunks from 6 queries — click to expand)</summary>

**Passage 1:**

> tings
The ADNI (Alzheimer’s Disease Neuroimaging Initiative)
public dataset is used to test our CT-GAN model. Table I
contains full information about the 268 patients whose data
we used in this study. Each patient was scanned with both
DTI and fMRI. The preprocessing procedure makes use of the
AAL 90 atlas. Using the DPARSF toolkit, the top 20 volumes
are eliminated, followed by head motion correction, band-
pass filtering, Gaussian smoothing, and extracting the time
series of all voxels. By following fiber bundles between ROIs,
4606 IEEE TRANSACTIONS ON NEURAL SYSTEMS AND REHABILITATION ENGINEERING, VOL. 31, 2023
Fig. 4. Examples of two multimodal connectivity matrices at different
stages of cognitive disease (a) NC; (b) AD. Fig. 5. The ten most important brain regions between NC and EMCI
groups.
the structural connection is computed.

**Passage 2:**

> taining magnetic resonance imaging (MRI) brain scan data
from more than 500,000 UK participants. This large sample
data can be suitable to study neurodegenerative diseases (e.g.,
Alzheimer’s disease). Due to the huge size of the dataset,
downloading and preprocessing of brain imaging data is very
time-consuming, and we are still in the collection stage of the
brain imaging data set. We will validate our model on the UK
biobank data in future work. V. C ONCLUSION
In this paper, we propose a novel CT-GAN model to fuse
fMRI and DTI and generate multimodal connectivity from
fMRI and DTI in an efficient end-to-end manner. The key idea
of this work is that mutual conversion between structural and
functional information is accomplished using a cross-modal
swapping bi-attention mechanism.

**Passage 3:**

> in images are based on two steps: the first step
is to preprocess the brain structural and functional images
ZUO et al.: AD PREDICTION VIA BRAIN STRUCTURAL-FUNCTIONAL DEEP FUSING NETWORK 4611
Fig. 14. Comparison of classification performance using single-modal and bimodal images.
to obtain structural and functional features by the software
toolbox; the second step is to use the preprocessed structural
and functional features to build deep learning models for
fusion. The novelty of our model is constructing an end-to-
end framework to fuse structural brain imaging (DTI) and
functional brain imaging (fMRI) for AD analysis.

**Passage 4:**

> successive convolutional filters on
the DTI. Specifically, we first design four down-sampling
convolutional operations with a kernel size of 3 × 3 × 3 and a
stride of 2 to extract local feature maps. The extracted feature
maps are then passed through 1 ×1×1 filters to fix the channel
at N. Finally, each channel map is combined with the brain
anatomical information ( x, y, z, v) to align the features for
each brain region [43]. Similar operations are conducted on
the fMRI. The output embeddings S and F are given below:
S = S E(DT I , x, y, z, v), F = F E( f M R I, x, y, z, v) (1)
where S ∈ RN ×q, F ∈ RN ×q. 2) Swapping Bi-Attention Mechanism: The proposed model
aims to leverage the transformer’s bi-attention mechanism to
explore complementary information between structural and
functional images.

**Passage 5:**

> 23
[13] S. Wang, Y . Shen, W. Chen, T. Xiao, and J. Hu, “Automatic recogni-
tion of mild cognitive impairment from MRI images using expedited
convolutional neural networks,” in Proc. Int. Conf. Artif. Neural Netw.,
Oct. 2017, pp. 373–380.
[14] G. L. Colclough, M. W. Woolrich, S. J. Harrison, P. A. Rojas López,
P. A. Valdes-Sosa, and S. M. Smith, “Multi-subject hierarchical inverse
covariance modelling improves estimation of functional brain networks,”
NeuroImage, vol. 178, pp. 370–384, Sep. 2018.
[15] R. Yu, L. Qiao, M. Chen, S.-W. Lee, X. Fei, and D. Shen, “Weighted
graph regularized sparse brain network construction for MCI identifica-
tion,” Pattern Recognit., vol. 90, pp. 220–231, Jun. 2019.
[16] Y . Li, H. Yang, B. Lei, J. Liu, and C.-Y .

**Passage 6:**

> Song, Z. Wen, and J. Qin, “Feature masking on
non-overlapping regions for detecting dense cells in blood smear image,”
IEEE Trans. Med. Imag., vol. 42, no. 6, pp. 1668–1680, Jun. 2023.
[35] H. Wu, X. Huang, X. Guo, Z. Wen, and J. Qin, “Cross-image depen-
dency modeling for breast ultrasound segmentation,” IEEE Trans. Med. Imag., vol. 42, no. 6, pp. 1619–1631, Jun. 2023.
[36] W. Yu, B. Lei, M. K. Ng, A. C. Cheung, Y . Shen, and S. Wang,
“Tensorizing GAN with high-order pooling for Alzheimer’s disease
assessment,” IEEE Trans. Neural Netw. Learn. Syst., vol. 33, no. 9,
pp. 4945–4959, Sep. 2022.
[37] S. Hu, B. Lei, S. Wang, Y . Wang, Z. Feng, and Y . Shen, “Bidi-
rectional mapping generative adversarial networks for brain MR to
PET synthesis,” IEEE Trans. Med. Imag. , vol. 41, no. 1, pp. 145–157,
Jan. 2022.
[38] W.

**Passage 7:**

> Wu, and J. Wang, “Enhancing the feature
representation of multi-modal MRI data by combining multi-view infor-
mation for MCI classification,” Neurocomputing, vol. 400, pp. 322–332,
Aug. 2020.
[56] X. Song et al., “Graph convolution network with similarity awareness
and adaptive calibration for disease-induced deterioration prediction,”
Med. Image Anal., vol. 69, Apr. 2021, Art. no. 101947.

**Passage 8:**

> 990, Apr. 2015.
[31] B. Lei et al., “Self-calibrated brain network estimation and joint
non-convex multi-task learning for identification of early Alzheimer’s
disease,” Med. Image Anal., vol. 61, Apr. 2020, Art. no. 101652.
[32] P. Cao et al., “Generalized fused group lasso regularized multi-task fea-
ture learning for predicting cognitive outcomes in Alzheimers disease,”
Comput. Methods Programs Biomed., vol. 162, pp. 19–45, Aug. 2018.
[33] S. Wang, Z. Chen, S. You, B. Wang, Y . Shen, and B. Lei, “Brain stroke
lesion segmentation using consistent perception generative adversarial
network,” Neural Comput. Appl., vol. 34, no. 11, pp. 8657–8669,
Jun. 2022.
[34] H. Wu, C. Lin, J. Liu, Y . Song, Z. Wen, and J. Qin, “Feature masking on
non-overlapping regions for detecting dense cells in blood smear image,”
IEEE Trans. Med. Imag., vol. 42, no. 6, pp. 1668–1680, Jun. 2023.
[35] H. Wu, X.

**Passage 9:**

> pping six ROIs in the prediction results. The index indicates the
corresponding ROI in the AAL90 atlas. The red color represents decreased connections; the blue color represents increased connections. The
gray dotted lines divide the six ROIs into five brain lobes. Fig. 13. Influence of different modules in CT -GAN on the prediction
performance.
experiments. First, we individually computed the classifica-
tion performance using functional brain imaging (fMRI) (as
shown by the red color in Figure 14). Then, we individually
computed the classification performance using structural brain
imaging (DTI) (as shown by the blue color in Figure 14). Finally, we fused functional and structural brain imaging and
presented the classification results in green color in Figure 14.

**Passage 10:**

> IEEE TRANSACTIONS ON NEURAL SYSTEMS AND REHABILITATION ENGINEERING, VOL. 31, 2023 4601
Alzheimer’s Disease Prediction via Brain
Structural-Functional Deep Fusing Network
Qiankun Zuo, Y anyan Shen
 , Member, IEEE, Ning Zhong, C. L. Philip Chen,
Baiying Lei
 , Senior Member, IEEE, and Shuqiang Wang
 , Senior Member, IEEE
Abstract— Fusing structural-functional images of the
brain has shown great potential to analyze the deterio-
ration of Alzheimer’s disease (AD). However, it is a big
challenge to effectively fuse the correlated and comple-
mentary information from multimodal neuroimages. In this
work, a novel model termed cross-modal transformer
generative adversarial network (CT-GAN) is proposed to
effectively fuse the functional and structural information
contained in functional magnetic resonance imaging (fMRI)
and diffusion tensor imaging (DTI).

**Passage 11:**

> vol. 181, pp. 734–747, Nov. 2018.
[25] O. Dekhil et al., “A personalized autism diagnosis CAD system using
a fusion of structural MRI and resting-state functional MRI data,”
Frontiers Psychiatry, vol. 10, p. 392, Jul. 2019.
[26] D. Hirjak et al., “Multimodal magnetic resonance imaging data fusion
reveals distinct patterns of abnormal brain structure and function in
catatonia,” Schizophrenia Bull., vol. 46, no. 1, pp. 202–210, Jan. 2020.
[27] C. J. Honey et al., “Predicting human resting-state functional connectiv-
ity from structural connectivity,” Proc. Nat. Acad. Sci. USA, vol. 106,
no. 6, pp. 2035–2040, Feb. 2009.
[28] K. Li, L. Guo, D. Zhu, X. Hu, J. Han, and T. Liu, “Individual
functional ROI optimization via maximization of group-wise consistency
of structural and functional profiles,” Neuroinformatics, vol. 10, no. 3,
pp. 225–242, Jul. 2012.
[29] Q. Zuo, B. Lei, Y . Shen, Y .

**Passage 12:**

> d D. Shen, “Weighted
graph regularized sparse brain network construction for MCI identifica-
tion,” Pattern Recognit., vol. 90, pp. 220–231, Jun. 2019.
[16] Y . Li, H. Yang, B. Lei, J. Liu, and C.-Y . Wee, “Novel effective
connectivity inference using ultra-group constrained orthogonal forward
regression and elastic multilayer perceptron classifier for MCI identifica-
tion,” IEEE Trans. Med. Imag., vol. 38, no. 5, pp. 1227–1239, May 2019.
[17] L. Xiao et al., “Multi-hypergraph learning-based brain functional con-
nectivity analysis in fMRI data,” IEEE Trans. Med. Imag., vol. 39, no. 5,
pp. 1746–1758, May 2020.
[18] B. Lei et al., “Diagnosis of early Alzheimer’s disease based on dynamic
high order networks,” Brain Imag. Behav., vol. 15, no. 1, pp. 276–287,
2021.
[19] M. Yu, O. Sporns, and A. J.

**Passage 13:**

> Process. Syst., vol. 30, 2017.
[41] D. A. Hudson and L. Zitnick, “Generative adversarial transformers,” in
Proc. Int. Conf. Mach. Learn., 2021, pp. 4487–4499.
[42] H. Wu, J. Pan, Z. Li, Z. Wen, and J. Qin, “Automated skin lesion
segmentation via an adaptive dual attention module,” IEEE Trans. Med. Imag., vol. 40, no. 1, pp. 357–370, Jan. 2021.
[43] Q. Zuo, L. Lu, L. Wang, J. Zuo, and T. Ouyang, “Constructing
brain functional network by adversarial temporal-spatial aligned trans-
former for early AD analysis,” Frontiers Neurosci., vol. 16, Nov. 2022,
Art. no. 1087176.
[44] L. Zhang, L. Wang, and D. Zhu, “Predicting brain structural network
using functional connectivity,” Med. Image Anal., vol. 79, Jul. 2022,
Art. no. 102463.
[45] L. Liu, Y .-P. Wang, Y . Wang, P. Zhang, and S. Xiong, “An enhanced
multi-modal brain graph network for classifying neuropsychiatric disor-
ders,” Med.

**Passage 14:**

> Wang, Y . Wang, Z. Feng, and Y . Shen, “Bidi-
rectional mapping generative adversarial networks for brain MR to
PET synthesis,” IEEE Trans. Med. Imag. , vol. 41, no. 1, pp. 145–157,
Jan. 2022.
[38] W. Yu et al., “Morphological feature visualization of Alzheimer’s disease
via multidirectional perception GAN,” IEEE Trans. Neural Netw. Learn. Syst., vol. 34, no. 8, pp. 4401–4415, Aug. 2023.
[39] C. Gong et al., “Generative AI for brain image computing and brain
network computing: A review,” Frontiers Neurosci., vol. 17, Jun. 2023,
Art. no. 1203104.
[40] A. Vaswani et al., “Attention is all you need,” in Proc. Adv. Neural Inf. Process. Syst., vol. 30, 2017.
[41] D. A. Hudson and L. Zitnick, “Generative adversarial transformers,” in
Proc. Int. Conf. Mach. Learn., 2021, pp. 4487–4499.
[42] H. Wu, J. Pan, Z. Li, Z. Wen, and J.

**Passage 15:**

> Channel Separator
The MC contains both structural and functional connectivity
information. To stabilize the learning process, we design the
dual-channel separator to recover the SC and FC from the MC. As shown in Figure 2, the dual-channel separator projects the
MC back to two modality-specific connectivities. Considering
the topological properties of the human brain, we adopt the
cross-weighting scheme to extract global connectivity informa-
tion for better detachment between structural and functional
connectivity. It consists of two branches, which share the
first layer and have different weighting parameters in the
second and third layers, respectively. The filter is a cross-shape
parameter with step size 1. The input and the output for each
layer have the same size, except for different channels. Finally,
the third layer outputs the reconstructed SC and FC. C.

**Passage 16:**

> ctional ROI optimization via maximization of group-wise consistency
of structural and functional profiles,” Neuroinformatics, vol. 10, no. 3,
pp. 225–242, Jul. 2012.
[29] Q. Zuo, B. Lei, Y . Shen, Y . Liu, Z. Feng, and S. Wang, “Multimodal
representations learning and adversarial hypergraph fusion for early
Alzheimer’s disease prediction,” in Proc. Chin. Conf. Pattern Recognit. Comput. Vis. (PRCV), Beijing, China, Nov. 2021, pp. 479–490.
[30] S. M. Daselaar, V . Iyengar, S. W. Davis, K. Eklund, S. M. Hayes, and
R. E. Cabeza, “Less wiring, more firing: Low-performing older adults
compensate for impaired white matter with greater neural activity,”
Cerebral Cortex, vol. 25, no. 4, pp. 983–990, Apr. 2015.
[31] B. Lei et al., “Self-calibrated brain network estimation and joint
non-convex multi-task learning for identification of early Alzheimer’s
disease,” Med. Image Anal., vol. 61, Apr.

**Passage 17:**

> obtained by applying the trained generator
to DTI and fMRI. The visualization of averaged multimodal
connectivity matrices and the change in connectivity with
various thresholds are shown in Figure 8. The three rows
correspond to the altered connections from NC to EMCI, from
EMCI to LMCI, and from LMCI to AD, respectively. The
values between −0.1 ∼ 0.1 are ignored during the analysis. Two threshold values are set for viewing the important con-
nections. The first threshold is 50% quantile values, which are
estimated from the positive and negative connectivities. The
same operation is implemented on the second 75% threshold
value. The more important connections with the 75% threshold
value are shown in Figure 9. It can be seen that the decreased
connections are greater than the increased connections at the
stages of EMCI and AD, while the phenomenon is reversed
at the LMCI stage.

**Passage 18:**

> ∈ RN ×q. 2) Swapping Bi-Attention Mechanism: The proposed model
aims to leverage the transformer’s bi-attention mechanism to
explore complementary information between structural and
functional images. Traditional transformers haven’t been thor-
oughly studied in the context of brain network computing, and
they just model relationships between brain regions within
a single modality, which fails to effectively explore the
complementary information between modalities. To mine the
complementary information between fMRI and DTI, we devise
the swapping bi-attention mechanism (SBM) to proficiently
align functional features with microstructural information. It can facilitate the synergistic exchange of information
between bimodal images. In this section, we first introduce
4604 IEEE TRANSACTIONS ON NEURAL SYSTEMS AND REHABILITATION ENGINEERING, VOL.

**Passage 19:**

> ontributions to this work are as follows:
• The proposed CT-GAN is proposed to transform the fMRI
and DTI into multimodal connectivity for AD analysis by
combining the generative adversarial strategy. It not only
learns the topological characteristics of non-Euclidean
space but also deeply fuses complementary information
in an efficient end-to-end manner.
• The swapping bi-attention mechanism (SBM) is devel-
oped to effectively align functional information with
microstructural information and enhance the complemen-
tary information between bimodal images.
• The dual-channel separator with cross-weighting scheme
is devised to decompose multimodal connectivity into
functional and structural connectivities, which preserve
global topological information and ensure the high quality
and diversity of the generated connectivities.

**Passage 20:**

> efine functional
connectivity. The neural fiber connection strength between
brain regions is defined as SC. It makes use of diffusion
tensor imaging (DTI) to measure water molecular dispersion
motion. The structural and functional connectivity can describe
AD patients’ pathological features from different perspec-
tives. AD patients exhibit damage to their structural con-
nections [10], which affects information transmission and
© 2023 The Authors. This work is licensed under a Creative Commons Attribution 4.0 License. For more information, see https://creativecommons.org/licenses/by/4.0/
4602 IEEE TRANSACTIONS ON NEURAL SYSTEMS AND REHABILITATION ENGINEERING, VOL. 31, 2023
processing and results in cognitive dysfunction. Besides, early-
stage AD patients show weakened and enhanced changes in
the functional connectivity strength [11].

**Passage 21:**

> ultimodal connectivity matrices at different
stages of cognitive disease (a) NC; (b) AD. Fig. 5. The ten most important brain regions between NC and EMCI
groups.
the structural connection is computed. The requirements are
configured in PANDA as the fiber tracking halting conditions:
a crossing angle of greater than 45 degrees between two
traveling directions. The predictor is implemented by the row-based filters in the
work [47]. The embedding dimension in the generator G is
set at 128. L = 5 layers of transformer are utilized to fuse
structural and functional embeddings. The heads in the trans-
former block are 8. The model’s parameters will be updated
during the training process using the Adam algorithm. The
learning rate is set to 0.001. The weight decay is set to 0.01.

**Passage 22:**

> tivity matrices, with the threshold
values set at 50% and 75% respectively. The second and fourth columns are the increased connectivity matrices with the threshold values at 50%
and 75% respectively. TABLE II
PREDICTION OF PERFORMANCE UNDER DIFFERENT MODELS AND CLASSIFIERS BY FUSING F MRI AND DTI(%)
proposed CT-GAN has the benefit of being more accurate than
previous multimodal fusion models in predicting the phases
of AD. To evaluate the AD-related ROIs in the classification tasks,
we utilized the LOOCV method [6] to compute the impor-
tant score for each ROI. To calculate the importance score
for each ROI, we first began to remove one row and one
column corresponding to one particular ROI in the generated
multimodal connectivity matrix. We then computed the mean
classification accuracy of the removed connectivity matrices.

**Passage 23:**

> luding the normal
control (NC), early mild cognitive impairment (EMCI), late
mild cognitive impairment (LMCI), and AD. p(Y |C(G(x, y)))
is the probability that the subject is predicted to be stage Y . Pair-wise Connectivity Reconstruction Loss. To impose
an additional topological constraint on the cross-modal trans-
former generator, we add the L1 pair-wise connectivity
reconstruction loss in the model’s optimization process. The
overall pair-wise connection gap between empirical FC/SC
matrices and FC/SC matrices are minimized by the following
formula:
LFC
pcr = ∥FC − FC′∥1, (19)
LSC
pcr = ∥SC − SC′∥1. (20)
III. E XPERIMENTS
A. Preprocessing and Settings
The ADNI (Alzheimer’s Disease Neuroimaging Initiative)
public dataset is used to test our CT-GAN model. Table I
contains full information about the 268 patients whose data
we used in this study.

**Passage 24:**

> ive adversarial network (CT-GAN) is proposed to
effectively fuse the functional and structural information
contained in functional magnetic resonance imaging (fMRI)
and diffusion tensor imaging (DTI). The CT-GAN can learn
topological features and generate multimodal connectivity
from multimodal imaging data in an efficient end-to-end
manner. Moreover, the swapping bi-attention mechanism
is designed to gradually align common features and
effectively enhance the complementary features between
modalities. By analyzing the generated connectivity fea-
tures, the proposed model can identify AD-related brain
connections. Evaluations on the public ADNI dataset show
that the proposed CT-GAN can dramatically improve pre-
diction performance and detect AD-related brain regions
effectively. The proposed model also provides new insights
into detecting AD-related abnormal neural circuits.

</details>

---
