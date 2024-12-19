# DeepFaceRecognition

## Dataset Preparation

### Datasets Used

For this project, we utilized two public datasets:

- **LFW Funneled Dataset**: A dataset of labeled faces in the wild. You can find it [here](https://www.kaggle.com/datasets/atulanandjha/lfwpeople).
- **PubFig Dataset**: A dataset of public figures' faces, available [here](https://www.kaggle.com/datasets/kaustubhchaudhari/pubfig-dataset-256x256-jpg). This dataset contains some overlap with LFW.

### Attribute Files

The attribute files for both datasets are available at the following locations:

- **LFW Attributes**: [LFW Attributes](https://vis-www.cs.umass.edu/lfw/#explore)
- **PubFig Attributes**: [PubFig Attributes](https://www.kaggle.com/datasets/kaustubhchaudhari/pubfig-dataset-256x256-jpg)

#### Preprocessing Steps for Attribute Files

1. Removed `#` symbols in the column names.
2. Adjusted the first four column names by replacing spaces with tabs (`\t`) to ensure compatibility with tab-separated data readers.

#### Dataset Structure

The dataset directory should be organized as follows:

```text
./datasets
    ├── lfw/                  # LFW dataset folder
    ├── pubfig/               # PubFig dataset folder
    ├── lfw_attributes.txt    # LFW attribute file
    ├── pubfig_attributes.txt # PubFig attribute file
```

### Filtering Criteria

The available fields for filtering the dataset are:

- **Ethnicity**: Asian, White, Black (only one ethnic attribute can be selected at a time).
- **Ages**: "Child," "Youth," "Middle Aged," and "Senior" (multiple age groups can be selected).

### Dataset Preparation Command

To prepare the dataset, you can run the following command:

```bash
./data_preparation.sh --ethnic 'Asian' --ages Child,Youth,'Middle Aged' --threshold 0.0
```

**Note**: Age fields are separated by commas with no spaces, and if an age field contains more than one word, it must be enclosed in quotes (e.g., `'Middle Aged'`).

### More Details

For more information on each step of the data preparation process, please refer to the [detailed instruction guide](./scripts/README.md).
