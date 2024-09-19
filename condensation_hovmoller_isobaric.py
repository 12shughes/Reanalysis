import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

directory = 'OpenMARS_data'
name = 'openmars'
year = 29
Ls_early = 240
Ls_late = 330
pressure = 100
lat = 77.5

latint, latdec = [int(part) for part in str(lat).split('.')]
root_path = '/disco/share/sh1293'
path = f'{root_path}/{directory}/Isobaric'
ds = xr.open_dataset(f'{path}/isobaric_{name}_my{year}.nc').astype('float32')


ds = ds.sel(lat=lat, method='nearest')
ds = ds.loc[dict(pfull=pressure)]
ds = ds.reset_coords('lat', drop=True).reset_coords('pfull', drop=True)
ds['Ls'] = ds.Ls.mean(dim='lon', skipna=True)
ds = ds.where(ds.Ls>=Ls_early).where(ds.Ls<=Ls_late).dropna(dim='time')
ds['T_c'] = 149.2+6.49*np.log(0.00135*pressure).astype('float32')
ds['cond_loc'] = xr.where(ds.temp <= ds.T_c+2, 1, np.nan)

ti = ds.time[0]
tf = ds.time[-1]
tick_ls = [240, 270, 300]
tick_time = [(tick_ls[0]-Ls_early)/(Ls_late-Ls_early)*(tf-ti)+ti,
            (tick_ls[1]-Ls_early)/(Ls_late-Ls_early)*(tf-ti)+ti,
            (tick_ls[2]-Ls_early)/(Ls_late-Ls_early)*(tf-ti)+ti]

fig, ax = plt.subplots(1, 1, figsize=(8,8))
cf = ds.PV.plot.contourf(ax=ax,  x='lon', y='time', cmap='OrRd', levels=21)
cf1 = ds.cond_loc.plot.contourf(ax=ax, x='lon', y='time', colors='none', levels=[0,1.5], hatches=['xx'])
ax.set_yticks(tick_time, tick_ls)
plt.savefig(f'{path}/Plots/hovmoller_condloc_{pressure}Pa_my{year}_Ls{Ls_early}-{Ls_late}_{latint}-{latdec}deg.pdf')

