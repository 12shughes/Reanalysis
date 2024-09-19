import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

years = [27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
for year in years:
    ds  = xr.open_dataset(f'/disco/share/sh1293/OpenMARS_data/CO2_ice/co2ice_openmars_my{year}.nc')
    ds['co2change'] = ds.co2ice.differentiate(coord='time')
    fig, ax = plt.subplots(1, 1)
    count, bins = np.histogram(ds.co2change, bins=[-20, -15, -10, -5, -4, -3, -2, -1, -0.5, 0.5, 1, 2, 3, 4, 5, 10, 15, 20])
    hist = ds.co2change.plot.hist(ax=ax, bins=[-20, -15, -10, -5, -4, -3, -2, -1, -0.5, 0.5, 1, 2, 3, 4, 5, 10, 15, 20])
    plt.savefig(f'/disco/share/sh1293/OpenMARS_data/CO2_ice/co2ice_openmars_my{year}.pdf')