from dataclasses import dataclass
from pathlib import Path
from typing import List, Set

import os
import shutil
import logging
import argparse
import numpy as np
import pandas as pd


log_dir = './datasets/logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
else:
    with open('./datasets/logs/data_extracter.log', 'a') as f:
        f.write("\n" + "="*80 + "\n" + "New Run Starting\n" + "="*80 + "\n")

# Configure logging
logging.basicConfig(
    filename='./datasets/logs/data_extracter.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class FilterConfig:
    """Configuration class for dataset filtering parameters."""
    ethnicity: str
    ages: List[str]
    threshold: float = 0.0

    def validate(self, available_columns: Set[str]) -> None:
        """Validate configuration against available data columns."""
        if self.ethnicity not in available_columns:
            raise ValueError(f"Ethnicity '{self.ethnicity}' not found in dataset")
        
        missing_ages = [age for age in self.ages if age not in available_columns]
        if missing_ages:
            raise ValueError(f"Age groups {missing_ages} not found in dataset")


def load_attributes(attr_file: str) -> pd.DataFrame:
    """Load and parse the attribute file."""
    try:
        data = pd.read_csv(attr_file, sep='\t', skiprows=1)
        logger.info(f"Successfully loaded attributes from {attr_file}")
        return data
    except FileNotFoundError:
        logger.error(f"Attribute file not found: {attr_file}")
        raise
    except Exception as e:
        logger.error(f"Error reading attribute file: {e}")
        raise ValueError(f"Failed to parse attribute file: {e}")


def preprocess_age_ethnicity(data: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the dataset to assign an age group and ethnicity to each sample based on 
    the highest positive magnitude value for age and ethnicity attributes.
    
    Args:
        data (pd.DataFrame): DataFrame containing the age and ethnicity attributes.
        
    Returns:
        processed_data (pd.DataFrame): The DataFrame with additional 'assigned_age_group' and 'assigned_ethnicity' columns.
    """
    # Define columns for age and ethnicity
    processed_data = data.copy()
    age_columns = ['Child', 'Youth', 'Middle Aged', 'Senior']
    ethnicity_columns = ['Asian', 'White', 'Black']

    # Function to determine the age group for a single row
    def determine_age_group(row):
        max_value = float('-inf')
        assigned_group = None

        for col in age_columns:
            if row[col] > 0 and row[col] > max_value:
                max_value = row[col]
                assigned_group = col

        return assigned_group

    # Function to determine the ethnicity for a single row
    def determine_ethnicity(row):
        max_value = float('-inf')
        assigned_ethnicity = None

        for col in ethnicity_columns:
            if row[col] > 0 and row[col] > max_value:
                max_value = row[col]
                assigned_ethnicity = col

        return assigned_ethnicity

    # Apply the age group assignment function to each row
    processed_data['assigned_age_group'] = processed_data.apply(determine_age_group, axis=1)

    # Apply the ethnicity assignment function to each row
    processed_data['assigned_ethnicity'] = processed_data.apply(determine_ethnicity, axis=1)

    return processed_data


def filter_persons(data: pd.DataFrame, config: FilterConfig) -> np.ndarray:
    """Filter persons based on ethnicity and age group conditions."""
    config.validate(set(data.columns))
    
    # Ensure 'assigned_ethnicity' and 'assigned_age_group' columns exist
    if 'assigned_ethnicity' not in data.columns or 'assigned_age_group' not in data.columns:
        raise ValueError("Data must contain 'assigned_ethnicity' and 'assigned_age_group' columns.")
    
    # Filter based on the ethnicity and age group conditions
    ethn_mask = data['assigned_ethnicity'] == config.ethnicity
    age_mask = data['assigned_age_group'].isin(config.ages)
    # Combine masks with AND condition
    final_mask = ethn_mask & age_mask
    
    selected_persons = data.loc[final_mask, 'person'].unique()
    log_statistics(data, ethn_mask, age_mask, selected_persons, config.ethnicity)
    return selected_persons


def log_statistics(data: pd.DataFrame, 
                   ethnicity_mask: pd.Series, 
                   age_mask: pd.Series, 
                   selected_persons: np.ndarray, 
                   ethnicity: str) -> None:
    """
    Log statistics about the filtering results.
    
    Args:
        data (pd.DataFrame): The original DataFrame with all data.
        ethn_mask (pd.Series): Boolean mask for the ethnicity condition.
        age_mask (pd.Series): Boolean mask for the age group condition.
        selected_persons (np.ndarray): Array of filtered person identifiers.
        ethnicity (str): The ethnicity used for filtering.
    """
    stats = {
        "Total persons": data['person'].nunique(),
        f"Matching criteria": len(selected_persons),
        f"{ethnicity} persons": data[ethnicity_mask]['person'].nunique(),
        "Age range persons": data[age_mask]['person'].nunique()
    }
    
    for description, count in stats.items():
        logger.info(f"{description}: {count}")


def copy_image_folders(src_root: Path, 
                       dst_root: Path, 
                       selected_persons: List[str]) -> None:
    """
    Copy selected person image folders to destination.
    
    Args:
        src_root (str): The path to the source directory containing person folders.
        dst_root (str): The path to the destination directory where folders will be copied.
        selected_persons (list): List of person identifiers whose folders need to be copied.
    """
    if not src_root.is_dir():
        raise ValueError(f"Invalid source directory: {src_root}")

    dst_root.mkdir(parents=True, exist_ok=True)
    
    for person in selected_persons:
        person_sanitized = person.replace(" ", "_")
        src_path = src_root / person_sanitized
        dst_path = dst_root / person_sanitized

        if not src_path.exists():
            logger.warning(f"Source folder not found: {src_path}")
            continue

        if dst_path.exists():
            logger.warning(f"Destination folder exists, merging: {dst_path}")
            try:
                # Merge the content of src_path into dst_path
                for item in src_path.iterdir():
                    src_item_path = item
                    dst_item_path = dst_path / item.name

                    if src_item_path.is_dir():
                        # Recursively copy directories
                        shutil.copytree(src_item_path, dst_item_path, dirs_exist_ok=True)
                    else:
                        # Copy individual files and overwrite if necessary
                        shutil.copy2(src_item_path, dst_item_path)
                logger.info(f"Successfully merged {person_sanitized} into {dst_path}")
            except Exception as e:
                logger.error(f"Failed to merge {person_sanitized}: {e}")
            continue

        try:
            logger.info(f"Copying folder: {person_sanitized}")
            shutil.copytree(src_path, dst_path)
        except Exception as e:
            logger.error(f"Failed to copy {person_sanitized}: {e}")


def parse_arguments() -> argparse.Namespace:
    """Parse and validate command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Filter dataset and copy selected folders based on attributes.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('-i', '--input-dir', type=Path, required=True,
                        help="Source dataset directory path")
    parser.add_argument('-o', '--output-dir', type=Path, 
                        default='./datasets/extracted_images',
                        help="Destination directory path")
    parser.add_argument('-r', '--attribute-record', type=Path, required=True,
                        help="Attribute record file path")
    parser.add_argument('-e', '--ethnic', type=str, default='Asian',
                        help="Ethnic attribute to filter by")
    parser.add_argument('-a', '--ages', nargs='+',
                        default=['Child', 'Youth', 'Middle Aged'],
                        help="Age attributes to filter by")
    parser.add_argument('-t', '--threshold', type=float, default=0.0,
                        help="Threshold for filtering attributes")

    return parser.parse_args()


def main() -> None:
    """Main execution function."""
    try:
        args = parse_arguments()
        
        # Initialize filter and process data
        data = load_attributes(args.attribute_record)
        config = FilterConfig(args.ethnic, args.ages, args.threshold)
        processed_data = preprocess_age_ethnicity(data)
        
        logger.info(f"Filtering persons: {args.ethnic} AND ({' OR '.join(args.ages)})")
        selected_persons = filter_persons(processed_data, config)
        
        # Copy selected folders
        logger.info("Copying selected person folders...")
        copy_image_folders(args.input_dir, args.output_dir, selected_persons)
        
        logger.info("Processing completed successfully")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise


if __name__ == "__main__":
    main()