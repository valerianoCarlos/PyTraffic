#!/bin/bash

# Path to the data directory
DATA_DIR="data"

# Delete all files in the data directory, but not directories
find "$DATA_DIR" -type f -delete

# Delete all files in subdirectories of the data directory
find "$DATA_DIR"/* -type d -exec find {} -type f -delete \;

echo "All files deleted from $DATA_DIR and its subdirectories."
