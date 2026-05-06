import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from cartopy import crs as ccrs
import matplotlib.path as mpath
import math
from matplotlib import (cm, colors)
from matplotlib import gridspec
import pdb
import matplotlib.ticker as mticker

datachoice = input('Enter directory code (a - analysis, b - background, c - control, ad - analysis different grid): ')
while datachoice not in ['a', 'b', 'c', 'ad']:
    print('Incorrect input')
    datachoice = input('Enter directory code (a - analysis, b - background, c - control, ad - analysis different grid): ')

if datachoice == 'a':
    type = 'Analysis/'
elif datachoice == 'b':
    type = 'Background/'
elif datachoice == 'c':
    type = 'Control/'
elif datachoice == 'ad':
    type = 'Analysis_diff_grid/'

directory = 'EMARS_data'
name = 'emars'
year = 29
Ls_early = 240
Ls_late = 330
level = 200
# timeind = 1002

root_path = '/disco/share/sh1293'
path = f'{root_path}/{directory}/{type}/Isentropic'
ds = xr.open_dataset(f'{path}/isentropic_{name}_my{year}.nc').astype('float32')

ds = ds.sel(level=level)
ds = ds.reset_coords('level', drop=True)
ds = ds.where(ds.Ls>=Ls_early, drop=True).where(ds.Ls<=Ls_late, drop=True)
ds['T_c'] = 149.2+6.49*np.log(0.00135*ds.pressure*100).astype('float32') 
ds['cond_loc'] = xr.where(ds.temp <= ds.T_c+2, 1, 0)

ds['co2grad'] = ds.snow.differentiate(coord='time')
ds['co2diff'] = ds.snow.diff(dim='time')/ds1.time.diff(dim='time')


theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)

# for timeind in range(900, 1111):
for timeind in range(1000, 1002):
    fig = plt.figure(figsize = (8, 8))
    #fig.suptitle('MY%02d Ls%.4f' %(my, d.time[i].values))
    spec = gridspec.GridSpec(ncols=1, nrows=1, width_ratios=[1], figure=fig)
    ax = fig.add_subplot(spec[0], projection = ccrs.NorthPolarStereo())
    gl = ax.gridlines(crs = ccrs.PlateCarree(), linewidth = 1, linestyle = '--', color = 'black', alpha = 1, draw_labels=False)
    meridians = [0, 60, 120, 180, -60, -120]
    parallels = [50, 60, 70, 80]
    gl.xlocator = mticker.FixedLocator(meridians)
    gl.ylocator = mticker.FixedLocator(parallels)
    gl.xlabels = False
    #gl.ylabels = [True if parallel in [50] else False]
    ax.set_boundary(circle, transform=ax.transAxes)
    ax.set_extent([-180,180,50,90], crs=ccrs.PlateCarree())
    # pdb.set_trace()


    Ls = round(float(ds.Ls[timeind,0].values), 2)
    Lsint, Lsdec = [int(part) for part in str(Ls).split('.')]
    print(f'{Lsint}-{Lsdec}')
    cf = ds.PV_lait[timeind,:,:].plot.contourf(ax=ax, transform=ccrs.PlateCarree(), cmap='OrRd', vmin=0, vmax=0.00035,
                                                levels=22, extend='both', add_colobar=True)
    save = f'stereo_condloc_{level}K_my{year}_Ls{Lsint}-{Lsdec}.pdf'
    # cf = ds.co2diff[timeind,:,:].plot.contourf(ax=ax, transform=ccrs.PlateCarree(), cmap='OrRd', vmin=-20, vmax=20,
    #                                             levels=21, extend='both')
    save = f'stereo_condloc_{level}K_my{year}_Ls{Lsint}-{Lsdec}.pdf'


    # contourplot1 = ax.contourf(ds.cond_loc[timeind,:,:].lon, ds.cond_loc[timeind,:,:].lat, ds.cond_loc[timeind,:,:].values,
    #                             colors='none', levels=[0,1.5], hatches=['xx'], zorder=2)
    cf1 = ds.cond_loc[timeind,:,:].plot.contour(ax=ax, transform=ccrs.PlateCarree(), colors='green', levels=[0.5],
                                                    add_colorbar=False)


    plt.savefig(f'{root_path}/{directory}/{type}/CO2_ice/Plots/stereo_cond/{save}')

