import xarray as xr
import numpy as np
import functions as fcs

islev = 000
# dataset can be OpenMARS_data, EMARS_data/Control, EMARS_data/Analysis
datachoice = input('Enter directory code (o - OpenMARS, ec - EMARS control, ea - EMARS analysis): ')
while datachoice not in ['o', 'ec', 'ea']:
    print('Incorrect input')
    datachoice = input('Enter directory code (o - OpenMARS, ec - EMARS control, ea - EMARS analysis): ')

if datachoice == 'o':
    dataset = 'OpenMARS_data'
    set = 'openmars'
    years = [27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
elif datachoice == 'ec':
    dataset = 'EMARS_data/Control'
    set = 'emars'
    years = [24, 25, 26, 27]
elif datachoice == 'ea':
    dataset = 'EMARS_data/Analysis'
    set = 'emars'
    years = [24, 25, 26, 27, 28, 29, 30, 31, 32, 33]


path = '/disco/share/sh1293/%s/Isentropic/' %(dataset)

for year in years:
    print(year)
    print('Opening dataset')
    ds = xr.open_dataset(path + 'isentropic_%s_my%02d.nc' %(set, year))
    print('Organising data')
    if islev != 000:
        ds = ds.where(ds.level == islev, drop = True)
        ds['Ls'] = ds.Ls[:,0,0].drop_vars('lon').drop_vars('level')
    elif islev == 000:
        ds['Ls'] = ds.Ls[:,0].drop_vars('lon')
    da = ds.PV * 10**4
    da = da.assign_coords({'Ls':ds.Ls})
    print('Lait scaling')
    qs = fcs.lait_scale(da)
    print('Eddy enstrophy calculation')
    edd_ens = fcs.eddy_enstrophy(qs)
    print('Saving')
    edd_ens.to_netcdf('/disco/share/sh1293/%s/Eddy_enstrophy/lev%03d_my%02d.nc' %(dataset, islev, year))