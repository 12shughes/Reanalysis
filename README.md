# Reanalysis

A variety of code looking at different reanalysis data and trying to make plots with it

**[processing_openmars.py](processing_openmars.py):**
Script to call functions to process Raw OpenMARS data and save with calculated PV values on isobaric and isentropic levels (this is the script that is run for OpenMARS)

**[PVmodule.py](PVmodule.py):**
The functions for making PV calculations (this is called by n_calc...)

**[n_calculate_PV_OpenMARS.py](n_calculate_PV_OpenMARS.py):**
The code to process the OpenMARS data using functions from PVmodule (this is called by processing.py)

**[plot_pngs.py](plots_pngs.py):**
Code to create a png plot of PV on polar stereographic plot for every timestep

**[make_ani.py](make_ani.py):**
Code to combine pngs into an animation and save as a gif

**[functions.py](functions.py):**
Functions I've written for making PV calculations

**[eddy_enstrophy_calc.py](eddy_enstrophy_calc.py):**
Script to calculate eddy enstrophy for specified isentropic level (000 == all)

**[playing_eddy_enstrophy_plots.ipynb](playing_eddy_enstrophy_plots.ipynb):**
Notebook to make eddy enstrophy plots (the best ones now incorporated in the python script below)

**[eddy_enstrophy_plot.py](eddy_enstrophy_plot.py):**
Script to make eddy enstrophy plots for scaled and non-scaled data

**[save_grid.py](save_grid.py):**
Python file to save OpenMARS grid for regridding EMARS data

**[regridding.sh](regridding.sh):**
Bash file for regridding EMARS data to OpenMARS lat lon

**[processing_emars.py](processing_emars.py):**
Script to call functions to process Regridded EMARS data and save with calculated PV values on isobaric and isentropic levels

**[n_calculate_PV_EMARS.py](n_calculate_PV_EMARS.py):**
The code to process the EMARS data using functions from PVmodule (this is called by processing.py)
