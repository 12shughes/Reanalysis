import xarray as xr
import numpy as np
import functions as fcs

islev = 300


path = '/disco/share/sh1293/OpenMARS_data/Isentropic/'
years = [27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
for year in years:
    print(year)
    print('Opening dataset')
    ds = xr.open_dataset(path + 'isentropic_openmars_my%02d.nc' %(year))
    print('Organising data')
    ds = ds.where(ds.level == islev, drop = True)
    ds['Ls'] = ds.Ls[:,0,0].drop_vars('lon').drop_vars('level')
    da = ds.PV * 10**4
    da = da.assign_coords({'Ls':ds.Ls})
    print('Lait scaling')
    qs = fcs.lait_scale(da)
    print('Eddy enstrophy calculation')
    edd_ens = fcs.eddy_enstrophy(qs)
    print('Saving')
    edd_ens.to_netcdf('/disco/share/sh1293/OpenMARS_data/Eddy_enstrophy/lev%03d_my%02d.nc' %(islev, year))