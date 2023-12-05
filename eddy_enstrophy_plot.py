import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

islev = 000

years = [27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
path = '/disco/share/sh1293/OpenMARS_data/Eddy_enstrophy/'
i = 0
for year in years:
    da = xr.open_dataarray(path + 'lev%03d_my%02d.nc' %(islev, year))
    da = da.assign_coords({'MY':year})
    if i == 0:
        d = da
    else:
        d = xr.concat([d, da], dim = 'time')
    i+=1

plt.figure(figsize = (24, 8))
X, Y = np.meshgrid(d.time, d.level)
plt.scatter(X, Y, c = d.values)
plt.savefig(path + '/Plots/plot.pdf')