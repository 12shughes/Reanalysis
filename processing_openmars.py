'''
Script to use the OpenMARS processing functions and create an output netcdf with all OpenMARS PV data
'''

import n_calculate_PV_OpenMARS as calc
import glob
import xarray as xr
import numpy as np

opath = '/disco/share/sh1293/OpenMARS_data/Raw/'
print('opening data')
initds = xr.open_mfdataset(opath + 'openmars*.nc')

levels = np.array([200., 225., 250., 275., 300., 310., 320., 330., 340.,
                    350., 360., 370., 380., 390., 400., 450., 500., 550.,
                    600., 650., 700., 750., 800., 850., 900., 950.])

print('splitting by year')
years = np.sort(np.unique(initds.MY))
#years = [27]
for year in years:
    print(year)
    splitds = initds.where((initds['MY'] == year).compute(), drop = True)
    print('prepping ds')
    midds, prs = calc.netcdf_prep(splitds)
    print('interpolating to isobaric')
    d_isobaric = calc.isobaric_interp(midds, prs)
    theta, d_isobaric['PV'] = calc.calculate_PV(d_isobaric)
    print('saving isobaric')
    d_isobaric.to_netcdf('/disco/share/sh1293/OpenMARS_data/Isobaric/isobaric_openmars_my%.0f.nc' %(year))
    print('interpolating to isentropic')
    d_isentropic = calc.interpolate_to_isentropic(d_isobaric, levels = levels)
    print('saving isentropic')
    d_isentropic.to_netcdf('/disco/share/sh1293/OpenMARS_data/Isentropic/isentropic_openmars_my%.0f.nc' %(year))
