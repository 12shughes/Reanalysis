import xarray as xr
import numpy as np


max = 8
years = [30]
for year in years:
    print(year)
    #for i in np.linspace(1, max, max):
    for i in [5,6,7,8]:
        print(i)
        print('opening data')
        d_isobaric = xr.open_dataset(f'/disco/share/sh1293/OpenMARS_data/Isobaric/MY{year}/isobaric_openmars_my{year}_{int(i)}.nc').astype('float32')
        d_isentropic = xr.open_dataset(f'/disco/share/sh1293/OpenMARS_data/Isentropic/MY{year}/isentropic_openmars_my{year}_{int(i)}.nc').astype('float32')
        print('combining data')
        if i == 5:
            t_d_isentropic = d_isentropic
            t_d_isobaric = d_isobaric
        else:
            t_d_isobaric = xr.concat([t_d_isobaric, d_isobaric], dim='time').astype('float32')
            t_d_isentropic = xr.concat([t_d_isentropic, d_isentropic], dim='time').astype('float32')
        d_isobaric.close()
        d_isentropic.close()
    print('saving isobaric')
    t_d_isobaric.to_netcdf(f'/disco/share/sh1293/OpenMARS_data/Isobaric/isobaric_openmars_my{year}.nc')
    t_d_isobaric.close()
    print('saving isentropic')
    t_d_isentropic.to_netcdf(f'/disco/share/sh1293/OpenMARS_data/Isentropic/isentropic_openmars_my{year}.nc')