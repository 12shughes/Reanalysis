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
        theta, d_isobaric['PV'] = calc.calculate_PV(d_isobaric)
        print('saving isobaric')
        d_isobaric.to_netcdf('/disco/share/sh1293/EMARS_data/%sIsobaric/isobaric_emars_my%.0f.nc' %(type, year))
        print('interpolating to isentropic')
        d_isentropic = calc.interpolate_to_isentropic(d_isobaric, levels = levels)
        print('saving isentropic')
        d_isentropic.to_netcdf('/disco/share/sh1293/EMARS_data/%sIsentropic/isentropic_emars_my%.0f.nc' %(type, year))
