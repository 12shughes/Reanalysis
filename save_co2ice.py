import numpy as np
import xarray as xr
import glob
import os
import n_calculate_PV_OpenMARS as calc

opath = '/disco/share/sh1293/OpenMARS_data/Raw/'
print('opening data')
initds = xr.open_mfdataset(opath + 'openmars*.nc').astype('float32')

print('splitting by year')
years = np.sort(np.unique(initds.MY))
initds.close()
for year in years:
    year = int(year)
    print(year)
    yeards = initds.where((initds['MY'] == year).compute(), drop = True)
    d = calc.onevar_prep(yeards, 'co2ice')
    yeards.close()
    d.to_netcdf(f'/disco/share/sh1293/OpenMARS_data/CO2_ice/co2ice_openmars_my{year}.nc')
    d.close()