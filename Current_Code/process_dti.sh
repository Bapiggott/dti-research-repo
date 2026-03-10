#!/bin/bash
# =============================================================================
# full_dti_pipeline.sh
# Full DTI preprocessing pipeline: DICOM → FA/MD maps → MNI space
#
# Pipeline steps:
#   1.  Copy DICOMs
#   2.  dcm2niix  — DICOM → NIfTI
#   3.  BET       — skull strip b0 → brain mask
#   4.  topup     — susceptibility distortion correction (if reverse-PE b0 exists)
#   5.  eddy      — eddy current + motion correction
#   6.  dtifit    — tensor fitting → FA, MD maps
#   7.  flirt     — affine registration to MNI152
#   8.  fnirt     — nonlinear registration to MNI152
#   9.  fslroi    — crop to 160×192×160
# =============================================================================

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG — edit these
# ─────────────────────────────────────────────────────────────────────────────
SUBJ="002_S_0413"
WIN_DICOM="/mnt/e/adni-processing-pipeline/Week2/ProcessTest/ADNI/002_S_0413/Axial_DTI"
WORK=~/adni/${SUBJ}
READOUT_FALLBACK="0.05"   # used only if dwi.json lacks TotalReadoutTime

# If your ADNI data has a reverse phase-encoding b0 scan, point this to it.
# Common locations/names: dwi_reverse.nii.gz, dwi_PA.nii.gz, b0_PA.nii.gz
# If the file doesn't exist, topup will be skipped gracefully.
REVERSE_B0_DICOM=""   # leave empty if you have no reverse-PE DICOM folder
                      # e.g. "/mnt/e/adni-processing-pipeline/.../Axial_DTI_reverse"

REF="$FSLDIR/data/standard/MNI152_T1_1mm.nii.gz"

# ─────────────────────────────────────────────────────────────────────────────
# SETUP
# ─────────────────────────────────────────────────────────────────────────────
set -e   # exit on any error
echo "============================================="
echo " DTI Pipeline — Subject: ${SUBJ}"
echo "============================================="

mkdir -p ${WORK}/raw ${WORK}/nifti ${WORK}/preproc

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — COPY DICOMs
# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo ">>> [1/9] Copying DICOMs..."
cp -r "${WIN_DICOM}/"* ${WORK}/raw/

# Copy reverse-PE DICOMs if provided
if [ -n "$REVERSE_B0_DICOM" ] && [ -d "$REVERSE_B0_DICOM" ]; then
    mkdir -p ${WORK}/raw_reverse
    cp -r "${REVERSE_B0_DICOM}/"* ${WORK}/raw_reverse/
fi

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — DICOM → NIfTI
# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo ">>> [2/9] Converting DICOMs to NIfTI..."
dcm2niix -z y -f dwi -o ${WORK}/nifti ${WORK}/raw

# Convert reverse-PE DICOMs if they were copied
if [ -d "${WORK}/raw_reverse" ]; then
    dcm2niix -z y -f dwi_reverse -o ${WORK}/nifti ${WORK}/raw_reverse
fi

echo "    Volumes in dwi.nii.gz: $(fslnvols ${WORK}/nifti/dwi.nii.gz)"
ls -lh ${WORK}/nifti

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — SKULL STRIP (BET)
# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo ">>> [3/9] Skull stripping b0..."
cd ${WORK}/preproc

# Extract first b0 volume
fslroi ../nifti/dwi.nii.gz b0 0 1

# BET: -f 0.3 (fractional intensity threshold), -m (save mask)
bet b0 b0_brain -f 0.3 -g 0 -m
echo "    Brain mask created: b0_brain_mask.nii.gz"

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — BUILD acqparams + index FILES
# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo ">>> [4/9] Building acqparams and index files..."

# Read phase-encode direction and readout time from JSON sidecar
PE=$(cat ../nifti/dwi.json 2>/dev/null \
     | grep -oP '"PhaseEncodingDirection"\s*:\s*"\K[^"]+' | head -n 1)
RT=$(cat ../nifti/dwi.json 2>/dev/null \
     | grep -oP '"TotalReadoutTime"\s*:\s*\K[0-9.]+' | head -n 1)

if [ -z "$RT" ]; then
    echo "    WARNING: TotalReadoutTime not found in JSON. Using fallback: ${READOUT_FALLBACK}"
    RT="${READOUT_FALLBACK}"
fi
if [ -z "$PE" ]; then
    echo "    WARNING: PhaseEncodingDirection not found in JSON. Assuming j (AP)."
    PE="j"
fi

echo "    PhaseEncodingDirection: ${PE}   TotalReadoutTime: ${RT}"

# Map PE string → FSL vector
case "$PE" in
    j)  VEC="0 1 0"  ;;
    j-) VEC="0 -1 0" ;;
    i)  VEC="1 0 0"  ;;
    i-) VEC="-1 0 0" ;;
    *)  VEC="0 1 0"
        echo "    WARNING: Unknown PE direction '${PE}', defaulting to j (0 1 0)." ;;
esac

echo "${VEC} ${RT}" > acqparams.txt

# index.txt: one entry per DWI volume, all pointing to acqparams row 1
nvol=$(fslnvols ../nifti/dwi.nii.gz)
yes 1 | head -n "$nvol" > index.txt
echo "    acqparams.txt: $(cat acqparams.txt)"
echo "    index.txt: ${nvol} volumes"

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — TOPUP (susceptibility distortion correction)
# Skipped gracefully if no reverse-PE b0 is available.
# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo ">>> [5/9] Topup (susceptibility distortion correction)..."

REVERSE_B0_NIFTI="../nifti/dwi_reverse.nii.gz"
TOPUP_ARG=""

if [ -f "$REVERSE_B0_NIFTI" ]; then
    echo "    Reverse-PE b0 found. Running topup..."

    # Extract single b0 from reverse-PE volume
    fslroi "$REVERSE_B0_NIFTI" b0_reverse 0 1

    # Merge forward + reverse b0 into one 4D pair
    fslmerge -t b0_pair b0 b0_reverse

    # Build acqparams for topup: forward line + reverse line (flipped PE vector)
    FWD_LINE=$(cat acqparams.txt)
    VEC_REV=$(echo "$VEC" | awk '{print -$1, -$2, -$3}')
    echo "$FWD_LINE"              >  acqparams_pair.txt
    echo "${VEC_REV} ${RT}"       >> acqparams_pair.txt

    topup \
        --imain=b0_pair \
        --datain=acqparams_pair.txt \
        --config=b02b0.cnf \
        --out=topup_results \
        --iout=b0_topup_corrected \
        --fout=topup_field

    echo "    topup complete."
    TOPUP_ARG="--topup=topup_results"

else
    echo "    No reverse-PE b0 found at ${REVERSE_B0_NIFTI}."
    echo "    Skipping topup. Eddy will correct eddy currents + motion only."
    echo "    To enable: acquire a reverse-PE b0 scan and set REVERSE_B0_DICOM above."
fi

# ─────────────────────────────────────────────────────────────────────────────
# STEP 6 — EDDY (eddy current + motion correction)
# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo ">>> [6/9] Running eddy..."

eddy \
    --imain=../nifti/dwi.nii.gz \
    --mask=b0_brain_mask.nii.gz \
    --acqp=acqparams.txt \
    --index=index.txt \
    --bvecs=../nifti/dwi.bvec \
    --bvals=../nifti/dwi.bval \
    --repol \
    ${TOPUP_ARG} \
    --out=eddy_corrected

echo "    eddy complete."

# ─────────────────────────────────────────────────────────────────────────────
# STEP 7 — DTIFIT (tensor fitting → FA, MD maps)
# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo ">>> [7/9] Running dtifit..."

dtifit \
    -k eddy_corrected.nii.gz \
    -o dti \
    -m b0_brain_mask.nii.gz \
    -r eddy_corrected.eddy_rotated_bvecs \
    -b ../nifti/dwi.bval

echo "    FA map: dti_FA.nii.gz"
echo "    MD map: dti_MD.nii.gz"

# ─────────────────────────────────────────────────────────────────────────────
# STEP 8 — REGISTER TO MNI152 (affine + nonlinear)
# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo ">>> [8/9] Registering FA to MNI152..."

# Affine first (FLIRT)
flirt \
    -in dti_FA.nii.gz \
    -ref "$REF" \
    -omat fa2mni.mat \
    -out FA_MNI_affine.nii.gz

# Nonlinear on top (FNIRT)
fnirt \
    --in=dti_FA.nii.gz \
    --ref="$REF" \
    --aff=fa2mni.mat \
    --iout=FA_MNI_fnirt.nii.gz

echo "    Registration complete."

# ─────────────────────────────────────────────────────────────────────────────
# STEP 9 — CROP TO 160×192×160
# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo ">>> [9/9] Cropping to 160×192×160..."

fslroi FA_MNI_fnirt.nii.gz FA_MNI_crop_160x192x160.nii.gz 11 160 13 192 11 160
fslinfo FA_MNI_crop_160x192x160.nii.gz | grep -E "dim1|dim2|dim3"

# ─────────────────────────────────────────────────────────────────────────────
# DONE
# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "============================================="
echo " Pipeline complete — ${SUBJ}"
echo "============================================="
echo " Key outputs in ${WORK}/preproc/:"
echo "   eddy_corrected.nii.gz          — motion/eddy corrected DWI"
echo "   dti_FA.nii.gz                  — fractional anisotropy map"
echo "   dti_MD.nii.gz                  — mean diffusivity map"
echo "   FA_MNI_fnirt.nii.gz            — FA in MNI152 space (nonlinear)"
echo "   FA_MNI_crop_160x192x160.nii.gz — FA cropped for model input"
if [ -n "$TOPUP_ARG" ]; then
echo "   topup_results.*                — susceptibility correction field"
echo "   (topup WAS applied)"
else
echo "   (topup was NOT applied — no reverse-PE b0 available)"
fi
echo "============================================="
