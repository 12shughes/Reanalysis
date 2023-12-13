# Reanalysis

A variety of code looking at different reanalysis data and trying to make plots with it

**[Processing.py](processing.py):**
Script to call functions to process Raw OpenMARS data and save with calculated PV values on isobaric and isentropic levels

**[PVmodule.py](PVmodule.py):**
The functions for making PV calculations

**[n_calculate_PV_OpenMARS.py](n_calculate_PV_OpenMARS.py):**
The code to process the OpenMARS data using functions from PVmodule

**[plot_pngs.py](plots_pngs.py):**
Code to create a png plot of PV on polar stereographic plot for every timestep

**[make_ani.py](make_ani.py):**
Code to combine pngs into an animation and save as a gif

**[functions.py](functions.py):**
Functions I've written for making PV calculations

**[eddy_enstrophy_calc.py](eddy_enstrophy_calc.py):**
Script to calculate eddy enstrophy for specified isentropic level (000 == all)

**[playing_eddy_enstrophy_plots.ipynb](playing_eddy_enstrophy_plots.ipynb):**
Notebook to make eddy enstrophy plots

**[save_grid.py](save_grid.py):**
Python file to save OpenMARS grid for regridding EMARS data

**[regridding.sh](regridding.sh):**
Bash file for regridding EMARS data to OpenMARS lat lon
