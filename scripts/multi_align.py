from face_crop_plus import Cropper
from typing import Union, Tuple
from pathlib import Path
from tqdm import tqdm

import os
import argparse
import logging


log_dir = './datasets/logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure logging
logging.basicConfig(
    filename='./datasets/logs/face_alignment.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatasetProcessor:
    """Handles batch processing of face cropping for a dataset."""
    
    def __init__(self, crop_size: Tuple[int, int] = (112, 112)):
        """
        Initialize the processor with given crop size.
        
        Args:
            crop_size: Tuple of (width, height) for face cropping
        """
        self.cropper = Cropper(output_size=crop_size, face_factor=1, strategy="largest")


    def process_dataset(self, 
                        src_root: Union[str, Path], 
                        dst_root: Union[str, Path]) -> None:
        """
        Process entire dataset with multiple person folders.
        
        Args:
            src_root: Root directory containing person folders
            dst_root: Destination root directory for cropped images
        """
        src_root = Path(src_root)
        dst_root = Path(dst_root)
        
        if not src_root.exists():
            raise ValueError(f"Source directory {src_root} does not exist")
        
        try:
            # Get all person folders
            person_folders = [f for f in src_root.iterdir() if f.is_dir()]
            total_persons = len(person_folders)
            
            if total_persons == 0:
                logger.warning(f"No person folders found in {src_root}")
                return
            
            logger.info(f"Found {total_persons} person folders")
            
            # Process each person folder
            for person_folder in tqdm(person_folders, desc="Processing persons"):
                try:
                    # Create person directory in destination
                    person_dst = dst_root / person_folder.name
                    person_dst.mkdir(parents=True, exist_ok=True)
                    
                    # Process the directory using face_crop_plus
                    logger.info(f"Processing {person_folder.name}")
                    
                    # Process the directory
                    processed_images = self.cropper.process_dir(
                        input_dir=str(person_folder),
                        output_dir=str(person_dst)
                    )
                    
                except Exception as e:
                    logger.error(f"Error processing folder {person_folder.name}: {str(e)}")
                    continue
                
            # Log final statistics
            logger.info("\nProcessing completed:")
            logger.info(f"Total persons processed: {total_persons}")
            
        except Exception as e:
            logger.error(f"Error processing folder: {str(e)}")


def main():
    """Main execution function with command line interface."""
    parser = argparse.ArgumentParser(
        description="Batch process face cropping for multiple persons"
    )
    
    parser.add_argument('-i', '--input-dir', type=str, required=True,
                        help="Source directory containing person folders")
    
    parser.add_argument('-o', '--output-dir', type=str, default='./datasets/processed_data',
                        help="Destination directory for cropped images")
    
    parser.add_argument('-W', "--width", type=int, default=112,
                        help="Width of cropped face images (default: 112)")
    
    parser.add_argument('-H', "--height", type=int, default=112,
                        help="Height of cropped face images (default: 112)")
    
    args = parser.parse_args()
    
    try:
        processor = DatasetProcessor(crop_size=(args.width, args.height))
        processor.process_dataset(args.input_dir, args.output_dir)
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()