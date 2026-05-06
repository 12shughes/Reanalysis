#!/bin/bash
set -e  # Stop script on first error

# Remember where we started
CURR_DIR=$(pwd)

trap 'cd "$CURR_DIR"' EXIT

echo "Starting Analysis"

# Define base paths
BASE_DIR="/disco/share/sh1293/EMARS_data/Analysis"
RAW_DIR="$BASE_DIR/Raw"
REGRID_DIR="$BASE_DIR/Regrid2"
GRID_FILE="/disco/share/sh1293/OpenMARS_data/gridfile2.txt"

# Make sure output folder exists
mkdir -p "$REGRID_DIR"

# Loop over all .nc files in Raw directory
cd "$RAW_DIR" || exit 1
find . -type f -name "*.nc" | while read -r file; do
    echo "Processing: $file"

    # Strip leading './' if present
    clean_file="${file#./}"
    output_file="$REGRID_DIR/$clean_file"

    # Ensure any subdirectories in Regrid2 exist
    mkdir -p "$(dirname "$output_file")"

    if [ -e "$output_file" ]; then
        echo "Already regridded → $output_file"
    else
        echo "Regridding → $output_file"
        cdo remapcon,"$GRID_FILE" "$RAW_DIR/$clean_file" "$output_file"
    fi
done

# Return to original directory
cd "$CURR_DIR" || exit
