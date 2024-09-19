import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

year = 29
pressure = 100

root_path = '/disco/share/sh1293/OpenMARS_data'

# ds1 = xr.open_dataset(f'{root_path}/Isobaric/isobaric_openmars_my{year}.nc').astype('float32')
ds1 = xr.open_dataset(f'{root_path}/Isentropic/isentropic_openmars_my{year}.nc').astype('float32')
ds2 = xr.open_dataset(f'{root_path}/CO2_ice/co2ice_openmars_my{year}.nc').astype('float32')

# ds1['T_c'] = 149.2+6.49*np.log(0.00135*ds1.pfull).astype('float32')
ds1['T_c'] = 149.2+6.49*np.log(0.00135*ds1.pressure).astype('float32')
ds1['T_diff'] = ds1.temp-ds1.T_c
ds2['co2grad'] = ds2.co2ice.differentiate(coord='time')
ds2['co2diff'] = ds2.co2ice.diff(dim='time')/ds2.time.diff(dim='time')

# ds3 = xr.merge([ds1.T_diff, ds2.co2grad])

# for pressure in ds1.pfull.values:
for lev in ds1.level.values:
    x = ds2.co2diff.values
    # y = ds1.loc[dict(pfull=pressure)].T_diff.values
    y = ds1.loc[dict(level=lev)].T_diff.values

    fig, ax = plt.subplots(1, 1)
    # ds3.plot.scatter(x='co2grad', y='T_diff')
    pl = plt.scatter(x=x, y=y, marker='x', s=1)
    # plt.savefig(f'{root_path}/CO2_ice/co2scatter1_my{year}_{int(pressure)}Pa.pdf')
    plt.ylabel('T diff')
    plt.xlabel('co2ice diff')
    plt.savefig(f'{root_path}/CO2_ice/co2scatter1_my{year}_{int(lev)}K.pdf')