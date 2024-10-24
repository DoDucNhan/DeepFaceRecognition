#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Check if required arguments are passed
if [ "$#" -lt 3 ]; then
    echo "Usage: $0 --ethnic <ethnic> --ages <ages> --threshold <threshold>"
    exit 1
fi

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -e|--ethnic) ETHNIC="$2"; shift ;;
        -a|--ages) AGES="$2"; shift ;;
        -t|--threshold) THRESHOLD="$2"; shift ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Ensure ages are passed as a list
IFS=',' read -r -a AGE_LIST <<< "$AGES"

# Step 1: Extract necessary person images from the LFW dataset
echo "Step 1: Extracting necessary person images from the LFW dataset..."
python3 ./scripts/extract_data.py \
    --input-dir ./datasets/lfw \
    --output-dir ./datasets/extracted_images \
    --attribute-record ./datasets/lfw_attributes.txt \
    --ethnic "$ETHNIC" \
    --ages "${AGE_LIST[@]}" \
    --threshold "$THRESHOLD"

# Step 2: Apply face alignment to the extracted folder
echo "Step 2: Applying face alignment to the extracted folder..."
python3 ./scripts/multi_align.py \
    --input-dir ./datasets/extracted_images/ \
    --output-dir ./datasets/processed_data

# Step 3: Run rename script for PubFig dataset due to name format mismatch
echo "Step 3: Renaming folders for PubFig dataset due to name format mismatch..."
./scripts/rename_folders.sh ./datasets/pubfig

# Step 4: Extract necessary person images from PubFig and combine with LFW
echo "Step 4: Extracting necessary person images from PubFig dataset..."
python3 ./scripts/extract_data.py \
    --input-dir ./datasets/pubfig \
    --output-dir ./datasets/processed_data \
    --attribute-record ./datasets/pubfig_attributes.txt \
    --ethnic "$ETHNIC" \
    --ages "${AGE_LIST[@]}" \
    --threshold "$THRESHOLD"

# Step 5: Remove broken files and duplicates
echo "Step 5: Removing broken files and duplicates..."
./scripts/check_broken_jpgs.sh ./datasets/processed_data
./scripts/remove_duplicates.sh ./datasets/processed_data

# Step 6: Count how many images are left after processing
echo "Step 6: Counting the remaining images after processing..."
./scripts/count_files.sh ./datasets/processed_data

echo "Data preparation process complete!"
