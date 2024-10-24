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

# Declare an associative array to hold checksums
declare -A file_checksums

# Loop through all files in the target directory and its subdirectories
find "$target_dir" -type f | while read -r file; do
    # Calculate the SHA-512 checksum of the file
    checksum=$(sha512sum "$file" | awk '{ print $1 }')

    # Check if this checksum already exists in the array
    if [[ -n "${file_checksums[$checksum]}" ]]; then
        # If it exists, it's a duplicate; remove the file
        echo "Removing duplicate file: $file"
        rm "$file"
    else
        # If it doesn't exist, add it to the array
        file_checksums[$checksum]="$file"
    fi
done

echo "Duplicate removal process completed."
