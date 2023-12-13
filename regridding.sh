#!/bin/bash


# Change to the parent directory
cd "/disco/share/sh1293/EMARS_data/Control/Raw" || exit

files=$(find -name "*.nc")

cd "/disco/share/sh1293/EMARS_data/Control/" || exit

for file in $files; do
    echo "$file"
    if [ -e "Regrid/$file" ]; then
        echo "Already regridded"
    else
        echo "Regridding"
        cdo remapcon,/disco/share/sh1293/OpenMARS_data/gridfile.txt Raw/$file Regrid/$file
    fi
done
