#!/bin/bash
# =============================================================================
# run_adni_fa_extraction.sh
# Processes all ADNI subjects that have a pre-computed FA NIfTI image.
# Runs N subjects in parallel (default: all cores).
#
# Registration: flirt affine only (no fnirt).
# For 116 large AAL ROIs, affine registration is sufficient and standard
# in the literature. fnirt was causing "matrix is singular" failures on
# these 116x116x80 native-space FA images.
#
# Usage:
#   ./run_adni_fa_extraction.sh                        # uses all cores
#   ./run_adni_fa_extraction.sh --jobs 4               # limit to 4 parallel jobs
#   ./run_adni_fa_extraction.sh --jobs 4 --list /path  # custom subject list
#
# Output: E:\adni_batch  (WSL: /mnt/e/adni_batch)
# Source on F:\ is never modified or deleted.
#
# Requires: GNU parallel  (sudo apt install parallel)
# =============================================================================

ADNI_ROOT="/mnt/f/DTI_Brett6/ADNI/ADNI"
OUT_ROOT="/mnt/e/adni_batch"
AAL_ATLAS="/home/brett/atlases/AAL_MNI_2mm.nii.gz"
FSL_HOME="/home/brett/fsl"
N_ROIS=116
SUBJ_LIST="/tmp/fa_subjects.txt"
N_JOBS=$(nproc)

while [[ $# -gt 0 ]]; do
    case "$1" in
        --jobs)  N_JOBS="$2";  shift 2 ;;
        --list)  SUBJ_LIST="$2"; shift 2 ;;
        *) echo "Unknown argument: $1"; exit 1 ;;
    esac
done

if [ ! -f "$SUBJ_LIST" ]; then
    echo "ERROR: Subject list not found at $SUBJ_LIST"
    exit 1
fi

if ! command -v parallel &>/dev/null; then
    echo "ERROR: GNU parallel not installed. Run: sudo apt install parallel"
    exit 1
fi

mkdir -p "${OUT_ROOT}/logs"
TOTAL=$(wc -l < "$SUBJ_LIST")

echo "============================================="
echo " ADNI FA Extraction"
echo " Subjects:      ${TOTAL}"
echo " Parallel jobs: ${N_JOBS}  (cores available: $(nproc))"
echo " Registration:  flirt affine only (no fnirt)"
echo " Reference:     FMRIB58_FA_1mm"
echo " Atlas:         AAL116"
echo " Output:        ${OUT_ROOT}"
echo " Subject list:  ${SUBJ_LIST}"
echo "============================================="

process_subject() {
    SUBJ="$1"
    [ -z "$SUBJ" ] && return

    # ── Ensure FSL is set up inside this subshell ─────────────────────────────
    if [ -z "$FSLDIR" ]; then
        export FSLDIR="$FSL_HOME"
        source "${FSLDIR}/etc/fslconf/fsl.sh"
        export PATH="${FSLDIR}/bin:$PATH"
    fi
    export FSLOUTPUTTYPE=NIFTI_GZ

    local REF="${FSLDIR}/data/standard/FMRIB58_FA_1mm.nii.gz"

    OUT="${OUT_ROOT}/${SUBJ}"
    LOG="${OUT_ROOT}/logs/${SUBJ}.log"

    if [ -f "${OUT}/node_features.csv" ]; then
        echo "[SKIP] ${SUBJ} — already processed"
        return
    fi

    FA_NII=$(find "${ADNI_ROOT}/${SUBJ}/Native_Space_Fractional_Anisotropy_Image" \
             -name "*.nii" 2>/dev/null | head -1)

    if [ -z "$FA_NII" ]; then
        echo "[SKIP] ${SUBJ} — no FA NIfTI found"
        return
    fi

    mkdir -p "${OUT}"

    {
        echo "[$(date)] START ${SUBJ}"

        # ── STEP 1: Copy FA to E:\ ────────────────────────────────────────────
        cp "$FA_NII" "${OUT}/FA_native.nii"
        echo "    FA source: $FA_NII"

        # ── STEP 2: Affine registration FA → FMRIB58_FA ──────────────────────
        # We use flirt only — no fnirt nonlinear step.
        # fnirt was failing with "inv(): matrix is singular" on these
        # native-space 116x116x80 FA images. Affine registration is standard
        # and sufficient for 116 large AAL ROIs.
        flirt \
            -in   "${OUT}/FA_native.nii" \
            -ref  "$REF" \
            -omat "${OUT}/fa2mni.mat" \
            -dof 12

        if [ ! -f "${OUT}/fa2mni.mat" ]; then
            echo "ERROR: flirt failed"; exit 1
        fi

        # ── STEP 3: Invert affine (MNI → subject space) ──────────────────────
        convert_xfm \
            -omat "${OUT}/mni2fa.mat" \
            -inverse "${OUT}/fa2mni.mat"
        rm -f "${OUT}/fa2mni.mat"

        if [ ! -f "${OUT}/mni2fa.mat" ]; then
            echo "ERROR: convert_xfm failed"; exit 1
        fi

        # ── STEP 4: Warp AAL116 atlas to subject space ────────────────────────
        flirt \
            -in      "${AAL_ATLAS}" \
            -ref     "${OUT}/FA_native.nii" \
            -init    "${OUT}/mni2fa.mat" \
            -applyxfm \
            -interp  nearestneighbour \
            -out     "${OUT}/AAL_subject_space.nii.gz"
        rm -f "${OUT}/mni2fa.mat"

        if [ ! -f "${OUT}/AAL_subject_space.nii.gz" ]; then
            echo "ERROR: atlas warp failed"; exit 1
        fi

        # ── STEP 5: Per-ROI extraction helper ─────────────────────────────────
        extract_roi_stats() {
            local map_file="$1"
            local out_csv="$2"
            local col_name="$3"
            echo "roi_id,${col_name},voxel_count" > "$out_csv"
            for roi_id in $(seq 1 ${N_ROIS}); do
                local mask="${OUT}/roi_tmp_${SUBJ}_${roi_id}.nii.gz"
                fslmaths "${OUT}/AAL_subject_space.nii.gz" \
                    -thr ${roi_id} -uthr ${roi_id} -bin "$mask"
                voxel_count=$(fslstats "$mask" -V | awk '{print $1}')
                if [ "$voxel_count" -gt 0 ] 2>/dev/null; then
                    mean_val=$(fslstats "$map_file" -k "$mask" -M)
                else
                    mean_val="0.0"
                fi
                echo "${roi_id},${mean_val},${voxel_count}" >> "$out_csv"
                rm -f "$mask"
            done
        }

        # ── STEP 6: Extract FA, delete copy ───────────────────────────────────
        extract_roi_stats "${OUT}/FA_native.nii" "${OUT}/roi_fa_stats.csv" "mean_fa"
        rm -f "${OUT}/FA_native.nii"

        # ── STEP 7: Extract MD / RD / AD if available ─────────────────────────
        for SCALAR in MD RD AD; do
            case $SCALAR in
                MD) SCALAR_DIR="${ADNI_ROOT}/${SUBJ}/Native_Space_Mean_Diffusivity_Image" ;;
                RD) SCALAR_DIR="${ADNI_ROOT}/${SUBJ}/Native_Space_Radial_Diffusivity_Image" ;;
                AD) SCALAR_DIR="${ADNI_ROOT}/${SUBJ}/Native_Space_Axial_Diffusivity_Image" ;;
            esac
            SCALAR_NII=$(find "$SCALAR_DIR" -name "*.nii" 2>/dev/null | head -1)
            if [ -n "$SCALAR_NII" ]; then
                cp "$SCALAR_NII" "${OUT}/${SCALAR}_native.nii"
                extract_roi_stats "${OUT}/${SCALAR}_native.nii" \
                    "${OUT}/roi_${SCALAR,,}_stats.csv" "mean_${SCALAR,,}"
                rm -f "${OUT}/${SCALAR}_native.nii"
                echo "    Extracted ${SCALAR} ROI stats"
            else
                echo "    INFO: No ${SCALAR} map for ${SUBJ}"
            fi
        done

        # ── STEP 8: Build combined node_features.csv ──────────────────────────
        echo "roi_id,mean_fa" > "${OUT}/node_features.csv"
        tail -n +2 "${OUT}/roi_fa_stats.csv" | awk -F',' '{print $1","$2}' \
            >> "${OUT}/node_features.csv"

        for SCALAR in md rd ad; do
            SCALAR_CSV="${OUT}/roi_${SCALAR}_stats.csv"
            if [ -f "$SCALAR_CSV" ]; then
                python3 - <<PYEOF
import csv
nf = "${OUT}/node_features.csv"
sc = "$SCALAR_CSV"
col = "mean_${SCALAR}"
rows_nf = list(csv.DictReader(open(nf)))
rows_sc = {r['roi_id']: r[col] for r in csv.DictReader(open(sc))}
with open(nf, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows_nf[0].keys()) + [col])
    w.writeheader()
    for r in rows_nf:
        r[col] = rows_sc.get(r['roi_id'], '0.0')
        w.writerow(r)
PYEOF
            fi
        done

        echo "[$(date)] DONE ${SUBJ}"

    } >> "$LOG" 2>&1

    if [ -f "${OUT}/node_features.csv" ]; then
        echo "[DONE] ${SUBJ}"
    else
        echo "[FAIL] ${SUBJ} — check ${LOG}"
    fi
}

export -f process_subject
export ADNI_ROOT OUT_ROOT AAL_ATLAS FSL_HOME N_ROIS

parallel \
    --jobs "$N_JOBS" \
    --bar \
    --joblog "${OUT_ROOT}/parallel_joblog.txt" \
    process_subject \
    :::: "$SUBJ_LIST"

DONE=$(ls "${OUT_ROOT}"/*/node_features.csv 2>/dev/null | wc -l)
echo ""
echo "============================================="
echo " All jobs finished"
echo " Subjects with node_features.csv: ${DONE} / ${TOTAL}"
echo " Full job log: ${OUT_ROOT}/parallel_joblog.txt"
echo "============================================="
