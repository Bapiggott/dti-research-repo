# --------- CONFIG ----------
SUBJ="002_S_0413"
WIN_DICOM="/mnt/e/adni-processing-pipeline/Week2/ProcessTest/ADNI/002_S_0413/Axial_DTI"
WORK=~/adni/${SUBJ}
READOUT_FALLBACK="0.05"   # used only if dwi.json lacks TotalReadoutTime

# --------- FOLDERS ----------
mkdir -p ${WORK}/raw ${WORK}/nifti ${WORK}/preproc

# --------- COPY DICOMS (avoid /mnt/c processing) ----------
cp -r "${WIN_DICOM}/"* ${WORK}/raw/

# --------- DICOM -> NIFTI ----------
dcm2niix -z y -f dwi -o ${WORK}/nifti ${WORK}/raw

# --------- VERIFY ----------
fslnvols ${WORK}/nifti/dwi.nii.gz
ls -lh ${WORK}/nifti

# --------- PREPROC ----------
cd ${WORK}/preproc

# b0 + BET mask
fslroi ../nifti/dwi.nii.gz b0 0 1
bet b0 b0_brain -f 0.3 -g 0 -m

# acqparams from json if possible (fallback otherwise)
PE=$(cat ../nifti/dwi.json 2>/dev/null | grep -oP '"PhaseEncodingDirection"\s*:\s*"\K[^"]+' | head -n 1)
RT=$(cat ../nifti/dwi.json 2>/dev/null | grep -oP '"TotalReadoutTime"\s*:\s*\K[0-9.]+' | head -n 1)
if [ -z "$RT" ]; then RT="${READOUT_FALLBACK}"; fi

# map PE -> vector
# j  -> 0  1 0
# j- -> 0 -1 0
# i  -> 1  0 0
# i- -> -1 0 0
VEC="0 1 0"
if [ "$PE" = "j-" ]; then VEC="0 -1 0"; fi
if [ "$PE" = "i"  ]; then VEC="1 0 0"; fi
if [ "$PE" = "i-" ]; then VEC="-1 0 0"; fi
echo "${VEC} ${RT}" > acqparams.txt

# index.txt
nvol=$(fslnvols ../nifti/dwi.nii.gz)
yes 1 | head -n "$nvol" > index.txt

# eddy (common robust flag: --repol)
eddy \
  --imain=../nifti/dwi.nii.gz \
  --mask=b0_brain_mask.nii.gz \
  --acqp=acqparams.txt \
  --index=index.txt \
  --bvecs=../nifti/dwi.bvec \
  --bvals=../nifti/dwi.bval \
  --repol \
  --out=eddy_corrected

# dtifit (use rotated bvecs)
dtifit \
  -k eddy_corrected.nii.gz \
  -o dti \
  -m b0_brain_mask.nii.gz \
  -r eddy_corrected.eddy_rotated_bvecs \
  -b ../nifti/dwi.bval

# register to MNI152 1mm
REF="$FSLDIR/data/standard/MNI152_T1_1mm.nii.gz"
flirt -in dti_FA.nii.gz -ref "$REF" -omat fa2mni.mat -out FA_MNI_affine.nii.gz
fnirt --in=dti_FA.nii.gz --ref="$REF" --aff=fa2mni.mat --iout=FA_MNI_fnirt.nii.gz

# crop 160x192x160
fslroi FA_MNI_fnirt.nii.gz FA_MNI_crop_160x192x160.nii.gz 11 160 13 192 11 160
fslinfo FA_MNI_crop_160x192x160.nii.gz | grep -E "dim1|dim2|dim3"