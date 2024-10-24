#!/bin/bash

# Check if a directory path is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <directory_path>"
    exit 1
fi

# Directory to check for JPEG files
DIRECTORY="$1"

# Check if the provided argument is a valid directory
if [ ! -d "$DIRECTORY" ]; then
    echo "Error: '$DIRECTORY' is not a valid directory."
    exit 1
fi

# Find all .jpg and .jpeg files in the specified directory
find "$DIRECTORY" -iname "*.jpg" -o -iname "*.jpeg" | while read -r file; do
    # Check if the file is a valid image using ImageMagick's identify command
    if ! identify "$file" >/dev/null 2>&1; then
        echo "Deleting broken file: $file"
        rm "$file"  # Delete the broken file
    fi
done

echo "Check complete."
