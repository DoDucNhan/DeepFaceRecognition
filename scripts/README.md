# Data Preparation for Image Processing

This document outlines the steps to process images from the Labeled Faces in the Wild (LFW) dataset and the PubFig dataset for a face recognition project. The following steps detail the extraction, alignment, and preparation of images, including commands and parameters used in the scripts.

## Steps to Process

### 1. Extract Necessary Person Images from LFW Dataset

To extract images based on ethnicity and age from the LFW dataset, run the following command:

```bash
python3 ./scripts/extract_data.py --input-dir ./datasets/lfw --attribute-record ./datasets/lfw_attributes.txt 
```

### 2. Apply Face Alignment

After extraction, apply face alignment to the images in the extracted folder:

```bash
python3 ./scripts/multi_align.py --input-dir ./datasets/extracted_images/ --output-dir ./datasets/processed_data
```

### 3. Rename Folders in PubFig Dataset

Run the rename script before extracting data from the PubFig dataset to address name format mismatches:

```bash
./scripts/rename_folders.sh ./datasets/pubfig
```

### 4. Extract Necessary Person Images from PubFig Dataset

Extract images from the PubFig dataset into the processed data folder. Face alignment is unnecessary since this dataset already crops the faces:

```bash
python3 ./scripts/extract_data.py --input-dir ./datasets/pubfig --output-dir ./datasets/processed_data --attribute-record ./datasets/pubfig_attributes.txt
```

### 5. Remove Duplicates and Broken Files

After combining the datasets, run the following shell scripts to check for duplicates and remove any broken files:

```bash
./scripts/check_broken_jpgs.sh ./datasets/processed_data
./scripts/remove_duplicates.sh ./datasets/processed_data
```

### 6. Count Remaining Images

To count how many images remain after processing, use the following command:

```bash
./scripts/count_files.sh ./datasets/processed_data
```

### 7. Prepare the Dataset Using One Command

You can prepare the dataset in one command as follows:

```bash
./data_preparation.sh --ethnic 'Asian' --ages Child,Youth,'Middle Aged' --threshold 0.0
```

**Note:** Each age field should be separated by a comma (`,`), with no spaces. If an age descriptor consists of two words, enclose it in quotes (e.g., `'Middle Aged'`).

## Script Parameter Explanations

### `extract_data.py` Parameters

- `--input-dir`: Source dataset directory path.
- `--output-dir`: Destination directory path (default: `./datasets/extracted_images`).
- `--attribute-record`: Path to the attribute record file (required).
- `--ethnic`: Ethnic attribute to filter by (default: `Asian`).
- `--ages`: Age attributes to filter by (default: `['Child', 'Youth', 'Middle Aged']`).
- `--threshold`: Threshold for filtering attributes (default: `0.0`).

### `multi_align.py` Parameters

- `--input-dir`: Source directory containing person folders (required).
- `--output-dir`: Destination directory for cropped images (default: `./datasets/processed_data`).
- `--width`: Width of cropped face images (default: `112`).
- `--height`: Height of cropped face images (default: `112`).

## Conclusion

Follow the steps outlined above to prepare the image dataset for further processing and analysis. Ensure all scripts are in the specified paths and dependencies are met for smooth execution.

Feel free to adjust any part of the text to better fit your project's specific requirements or your preferred formatting style!
