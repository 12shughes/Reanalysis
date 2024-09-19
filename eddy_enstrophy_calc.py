import xarray as xr
import numpy as np
import functions as fcs
import os
import pdb

islev = 000
# dataset can be OpenMARS_data, EMARS_data/Control, EMARS_data/Analysis
datachoice = input('Enter directory code (o - OpenMARS, ec - EMARS control, ea - EMARS analysis, m2 - MACDA2): ')
while datachoice not in ['o', 'ec', 'ea', 'm2']:
    print('Incorrect input')
    datachoice = input('Enter directory code (o - OpenMARS, ec - EMARS control, ea - EMARS analysis, m2 - MACDA2): ')

if datachoice == 'o':
    dataset = 'OpenMARS_data'
    set = 'openmars'
    #years = [27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
    years = [34]
elif datachoice == 'ec':
    dataset = 'EMARS_data/Control'
    set = 'emars'
    #years = [24, 25, 26, 27]
    years = [26]
elif datachoice == 'ea':
    dataset = 'EMARS_data/Analysis'
    set = 'emars'
    #years = [24, 25, 26, 27, 28, 29, 30, 31, 32, 33]
    years = [26, 29]
elif datachoice == 'm2':
    dataset = 'MACDA2_data'
    set = 'macda2'
    # years = [28, 29]
    years = [29]


path = '/disco/share/sh1293/%s/Isentropic/' %(dataset)

for year in years:
    print(year)
    if not os.path.exists('/disco/share/sh1293/%s/Eddy_enstrophy/lev%03d_my%02d.nc' %(dataset, islev, year))\
        or not os.path.exists('/disco/share/sh1293/%s/Eddy_enstrophy/scaled_lev%03d_my%02d.nc' %(dataset, islev, year))\
        or not os.path.exists('/disco/share/sh1293/%s/Eddy_enstrophy/scaled2_lev%03d_my%02d.nc' %(dataset, islev, year))\
        or not os.path.exists('/disco/share/sh1293/%s/Eddy_enstrophy/scaled3_lev%03d_my%02d.nc' %(dataset, islev, year))\
        or not os.path.exists('/disco/share/sh1293/%s/Eddy_enstrophy/scaled3_lev%03d_my%02d_50N.nc' %(dataset, islev, year)):
        print('Opening dataset')
        ds = xr.open_dataset(path + 'isentropic_%s_my%02d.nc' %(set, year))
        # pdb.set_trace()
        print('Organising data')
        if islev != 000:
            ds = ds.where(ds.level == islev, drop = True)
            ds['Ls'] = ds.Ls[:,0,0].drop_vars('lon').drop_vars('level')
        elif islev == 000:
            ds['Ls'] = ds.Ls[:,0].drop_vars('lon')
        #da = ds.PV * 10**4
        #da = da.assign_coords({'Ls':ds.Ls})
        print('Lait scaling')
        qs = fcs.lait_scale(ds)
        # pdb.set_trace()  
        qs = qs * 10**4
        qs = qs.assign_coords({'Ls':ds.Ls})
        if not os.path.exists('/disco/share/sh1293/%s/Eddy_enstrophy/lev%03d_my%02d.nc' %(dataset, islev, year)):
            print('Eddy enstrophy calculation')
            edd_ens = fcs.eddy_enstrophy(qs)
            print('Saving')
            edd_ens.to_netcdf('/disco/share/sh1293/%s/Eddy_enstrophy/lev%03d_my%02d.nc' %(dataset, islev, year))
        if not os.path.exists('/disco/share/sh1293/%s/Eddy_enstrophy/scaled_lev%03d_my%02d.nc' %(dataset, islev, year)):
            print('Scaled eddy enstrophy calculation')
            sc_edd_ens = fcs.scaled_eddy_enstrophy(qs)
            print('Saving')
            sc_edd_ens.to_netcdf('/disco/share/sh1293/%s/Eddy_enstrophy/scaled_lev%03d_my%02d.nc' %(dataset, islev, year))
        if not os.path.exists('/disco/share/sh1293/%s/Eddy_enstrophy/scaled2_lev%03d_my%02d.nc' %(dataset, islev, year)):
            print('Scaled2 eddy enstrophy calculation')
            sc2_edd_ens = fcs.scaled2_eddy_enstrophy(qs)
            print('Saving')
            sc2_edd_ens.to_netcdf('/disco/share/sh1293/%s/Eddy_enstrophy/scaled2_lev%03d_my%02d.nc' %(dataset, islev, year))
        if not os.path.exists('/disco/share/sh1293/%s/Eddy_enstrophy/scaled3_lev%03d_my%02d.nc' %(dataset, islev, year)):
            print('Scaled3 eddy enstrophy calculation')
            # pdb.set_trace()
            sc3_edd_ens = fcs.scaled3_eddy_enstrophy(qs)
            print('Saving')
            sc3_edd_ens.to_netcdf('/disco/share/sh1293/%s/Eddy_enstrophy/scaled3_lev%03d_my%02d.nc' %(dataset, islev, year))
        if not os.path.exists('/disco/share/sh1293/%s/Eddy_enstrophy/scaled3_lev%03d_my%02d_50N.nc' %(dataset, islev, year)):
            print('Scaled3 eddy enstrophy calculation')
            sc3_edd_ens = fcs.scaled3_eddy_enstrophy(qs, latmin=50)
            print('Saving')
            sc3_edd_ens.to_netcdf('/disco/share/sh1293/%s/Eddy_enstrophy/scaled3_lev%03d_my%02d_50N.nc' %(dataset, islev, year))
    else:
        print('Calculations already done')