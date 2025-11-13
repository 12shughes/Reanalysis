#!/bin/bash

echo "Analysis"

# Change to the parent directory
cd "/disco/share/sh1293/EMARS_data/Analysis/Raw" || exit

files=$(find -name "*.nc")

cd "/disco/share/sh1293/EMARS_data/Analysis/" || exit

for file in $files; do
    echo "$file"
    if [ -e "Regrid2/$file" ]; then
        echo "Already regridded"
    else
        echo "Regridding"
        cdo remapcon,/disco/share/sh1293/OpenMARS_data/gridfile2.txt Raw/$file Regrid2/$file
    fi
done