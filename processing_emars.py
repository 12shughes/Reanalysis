'''
Script to use the EMARS processing functions and create an output netcdf with all EMARS PV data
'''

import n_calculate_PV_EMARS as calc
import glob
import xarray as xr
import numpy as np

for type in ['Control/', 'Analysis/']:
    print(type)

    epath = '/disco/share/sh1293/EMARS_data/' + type + 'Regrid/'
    print('opening data')
    initds = xr.open_mfdataset(epath + 'emars*.nc', combine='nested', concat_dim='time')
    print('dealing with time')
    times = np.linspace(0,len(initds.time)-1, len(initds.time))
    initds = initds.assign(time=times)
    print('Extracting necessary part of dataset')
    if type == 'Control/':
        initds = initds[['MY', 'Ls', 'time', 't', 'u', 'v', 'ps', 'ak', 'bk', 'lon', 'lat', 'phalf', 'pfull']]
    elif type == 'Analysis/':
        initds = initds[['MY', 'Ls', 'time', 'T', 'u', 'v', 'ps', 'ak', 'bk', 'lon', 'lat', 'phalf', 'pfull']]

    levels = np.array([200., 225., 250., 275., 300., 310., 320., 330., 340.,
                        350., 360., 370., 380., 390., 400., 450., 500., 550.,
                        600., 650., 700., 750., 800., 850., 900., 950.])

    print('splitting by year')
    years = np.sort(np.unique(initds.MY))
    print(years)
    #years = [27]
    for year in years:
        print(year)
        splitds = initds.where((initds['MY'] == year).compute(), drop = True)
        print('prepping ds')
        midds, prs = calc.netcdf_prep(splitds, type)
        print('interpolating to isobaric')
        d_isobaric = calc.isobaric_interp(midds, prs)
        print('Splitting year in half')
        d_isobaric1 = d_isobaric.where((d_isobaric.Ls<=180.).compute(), drop=True)
        d_isobaric2 = d_isobaric.where((d_isobaric.Ls>180.).compute(), drop=True)
        print('First half of year')
        theta1, d_isobaric1['PV'] = calc.calculate_PV(d_isobaric1)
        print('Second half of year')
        theta2, d_isobaric2['PV'] = calc.calculate_PV(d_isobaric2)
        print('Combining data')
        theta = xr.concat([theta1, theta2], dim='time')
        d_isobaric = xr.concat([d_isobaric1, d_isobaric2], dim='time')
        print('saving isobaric')
        d_isobaric.to_netcdf('/disco/share/sh1293/EMARS_data/%sIsobaric/isobaric_emars_my%.0f.nc' %(type, year))
        print('interpolating to isentropic')
        d_isentropic = calc.interpolate_to_isentropic(d_isobaric, levels = levels)
        print('saving isentropic')
        d_isentropic.to_netcdf('/disco/share/sh1293/EMARS_data/%sIsentropic/isentropic_emars_my%.0f.nc' %(type, year))
