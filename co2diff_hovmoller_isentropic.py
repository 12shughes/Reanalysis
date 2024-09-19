import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors

directory = 'OpenMARS_data'
name = 'openmars'
year = 29
Ls_early = 180
Ls_late = 360
level = 200
lat = 77.5
thresh = 1

latint, latdec = [int(part) for part in str(lat).split('.')]
root_path = '/disco/share/sh1293'
path = f'{root_path}/{directory}/Isentropic'
ds = xr.open_dataset(f'{path}/isentropic_{name}_my{year}.nc').astype('float32')
ds1 = xr.open_dataset(f'{root_path}/{directory}/CO2_ice/co2ice_openmars_my{year}.nc').astype('float32')

ds = ds.sel(lat=lat, method='nearest')
ds = ds.sel(level=level)
ds = ds.reset_coords('lat', drop=True).reset_coords('level', drop=True)
ds['Ls'] = ds.Ls.mean(dim='lon', skipna=True)
ds1['Ls'] = ds.Ls
ds = ds.where(ds.Ls>=Ls_early).where(ds.Ls<=Ls_late).dropna(dim='time')
# ds['T_c'] = 149.2+6.49*np.log(0.00135*ds.pressure*100).astype('float32')
# ds['cond_loc'] = xr.where(ds.temp <= ds.T_c+thresh, 1, np.nan)

ds1 = ds1.sel(lat=lat, method='nearest')
ds1 = ds1.reset_coords('lat', drop=True)

ds1 = ds1.where(ds1.Ls>=Ls_early).where(ds1.Ls<=Ls_late).dropna(dim='time')
ds1['co2grad'] = ds1.co2ice.differentiate(coord='time')
ds1['co2diff'] = ds1.co2ice.diff(dim='time')/ds1.time.diff(dim='time')

ti = ds.time[0]
tf = ds.time[-1]
# tick_ls = [240, 270, 300]
# tick_ls = [270, 285, 300]
tick_ls = [Ls_early, (Ls_early+Ls_late)/2, Ls_late]
tick_time = [(tick_ls[0]-Ls_early)/(Ls_late-Ls_early)*(tf-ti)+ti,
            (tick_ls[1]-Ls_early)/(Ls_late-Ls_early)*(tf-ti)+ti,
            (tick_ls[2]-Ls_early)/(Ls_late-Ls_early)*(tf-ti)+ti]

fig, ax = plt.subplots(1, 1, figsize=(8,8))
cf = ds.PV.plot.contourf(ax=ax,  x='lon', y='time', cmap='OrRd', levels=21)
# ds['cond_loc_fill'] = ds.cond_loc.fillna(0)
ds1['co2_down'] = xr.where(ds1.co2diff>0, 1, np.nan)
ds1['co2_down_fill'] = ds1.co2_down.fillna(0)

# cf1 = ds1.co2_down.plot.contourf(ax=ax, x='lon', y='time', colors='none', levels=[0, 1.5], hatches='xx', add_colorbar=False)
# cf1 = ds1.co2diff.plot.contour(ax=ax, x='lon', y='time', levels=[0, 1, 2, 3, 4, 5], colors=['darkslategrey', 'darkcyan', 'darkturquoise', 'deepskyblue', 'aqua'], linewidths=1)

cf1 = ds1.co2diff.plot.contour(ax=ax, x='lon', y='time', levels=[0, 3, 5], colors=['darkslategrey', 'darkturquoise', 'aqua'], linewidths=1, labels = ['0', '3', '5'])
nm, lbl = cf1.legend_elements()
lbl_ = ['0', '3', '5']
plt.legend(nm, lbl_)

# cf2 = ds1.co2_down.plot.contourf(ax=ax, x='lon', y='time', colors='black', levels=[0, 1.5], alpha=0.2, add_colorbar=False)
ax.set_yticks(tick_time, tick_ls)
plt.savefig(f'{path}/Plots/hovmoller_co2diff_{level}K_my{year}_Ls{Ls_early}-{Ls_late}_{latint}-{latdec}deg.pdf')

