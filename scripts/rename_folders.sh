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

# Iterate over each directory in the target directory
for dir in "$target_dir"/*; do
    # Check if it's a directory
    if [ -d "$dir" ]; then
        # Extract the current directory name
        current_name=$(basename "$dir")
        
        # Replace spaces with underscores
        new_name="${current_name// /_}"

        # Perform the renaming if the new name is different
        if [ "$current_name" != "$new_name" ]; then
            mv "$dir" "$target_dir/$new_name"
            echo "Renamed directory: '$current_name' to '$new_name'"
        fi
    fi
done
