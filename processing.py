'''
script to use the OpenMARS processing functions and create an output netcdf with all OpenMARS PV data
'''

import n_calculate_PV_OpenMARS as calc
import glob
import xarray as xr

opath = '/disco/share/sh1293/OpenMARS_data/Raw/'
print('opening data')
initds = xr.open_mfdataset(opath + '*.nc')
print('prepping ds')
midds, prs = calc.netcdf_prep(initds)
print('interpolating to isobaric')
d_isobaric = calc.isobaric_interp(midds, prs)
theta, d_isobaric['PV'] = calc.calculate_PV(d_isobaric)
print('interpolating to isentropic')
d_isentropic = calc.interpolate_to_isentropic(d_isobaric)
d_isentropic.to_netcdf('/disco/share/sh1293/OpenMARS_data/' + file + '.nc')