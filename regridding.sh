#!/bin/bash

echo "Analysis"

# Change to the parent directory
cd "/disco/share/sh1293/EMARS_data/Analysis/Raw" || exit

files=$(find -name "*.nc")

cd "/disco/share/sh1293/EMARS_data/Analysis/" || exit

for file in $files; do
    echo "$file"
    if [ -e "Regrid/$file" ]; then
        echo "Already regridded"
    else
        echo "Regridding"
        cdo remapcon,/disco/share/sh1293/OpenMARS_data/gridfile.txt Raw/$file Regrid/$file
    fi
done

echo "Analysis1"

# Change to the parent directory
cd "/disco/share/sh1293/EMARS_data/Analysis/Raw" || exit

files=$(find -name "*.nc")

cd "/disco/share/sh1293/EMARS_data/" || exit

for file in $files; do
    echo "$file"
    if [ -e "Analysis_diff_grid/Regrid/$file" ]; then
        echo "Already regridded"
    else
        echo "Regridding"
        cdo remapcon,/disco/share/sh1293/OpenMARS_data/gridfile1.txt Analysis/Raw/$file Analysis_diff_grid/Regrid/$file
    fi
done


echo "Control"

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


echo "Background"

# Change to the parent directory
cd "/disco/share/sh1293/EMARS_data/Background/Raw" || exit

files=$(find -name "*.nc")

cd "/disco/share/sh1293/EMARS_data/Background/" || exit

for file in $files; do
    echo "$file"
    if [ -e "Regrid/$file" ]; then
        echo "Already regridded"
    else
        echo "Regridding"
        cdo remapcon,/disco/share/sh1293/OpenMARS_data/gridfile.txt Raw/$file Regrid/$file
    fi
done
