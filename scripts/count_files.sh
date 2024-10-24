#!/bin/bash

# Check if the directory argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 /path/to/directory"
    exit 1
fi

# Assign the first argument to target_dir
target_dir="$1"

# Check if the provided argument is a valid directory
if [ ! -d "$target_dir" ]; then
    echo "Error: '$target_dir' is not a valid directory."
    exit 1
fi

# Count all files in the directory and its subdirectories
file_count=$(find "$target_dir" -type f | wc -l)

# Output the count
echo "Total number of files (excluding parent folder): $file_count"
