# Reanalysis

A variety of code looking at different reanalysis data and trying to make plots with it

**[Processing](processing.py):**
Script to call functions to process Raw OpenMARS data and save with calculated PV values on isobaric and isentropic levels

**[PVmodule](PVmodule.py):**
The functions for making PV calculations

**[n_calculate_PV_OpenMARS](n_calculate_PV_OpenMARS.py):**
The code to process the OpenMARS data using functions from PVmodule

**[plot_pngs](plots_pngs.py):**
Code to create a png plot of PV on polar stereographic plot for every timestep

**[make_ani](make_ani.py):**
Code to combine pngs into an animation and save as a gif

**[functions](functions.py):**
Functions I've written for making PV calculations


**[eddy_enstrophy_calc](eddy_enstrophy_calc.py):**
Script to calculate eddy enstrophy for specified isentropic level (000 == all)

**[playing_eddy_enstrophy_plots](playing_eddy_enstrophy_plots.ipynb):**
Notebook to make eddy enstrophy plots