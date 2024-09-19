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

directory = 'OpenMARS_data'
name = 'openmars'
year = 29
Ls_early = 240
Ls_late = 330
level = 200
# timeind = 1002

root_path = '/disco/share/sh1293'
path = f'{root_path}/{directory}/Isentropic'
ds = xr.open_dataset(f'{path}/isentropic_{name}_my{year}.nc').astype('float32')
dss = ds

ds = ds.sel(level=level)
ds = ds.reset_coords('level', drop=True)
ds = ds.where(ds.Ls>=Ls_early, drop=True).where(ds.Ls<=Ls_late, drop=True)
ds['T_c'] = 149.2+6.49*np.log(0.00135*ds.pressure*100).astype('float32') 
ds['cond_loc'] = xr.where(ds.temp <= ds.T_c+2, 1, np.nan)

# Ls = round(float(ds.Ls[timeind,0].values), 2)
# Lsint, Lsdec = [int(part) for part in str(Ls).split('.')]
# print(f'{Lsint}-{Lsdec}')

# plt.rcParams.update({'font.size': 25})


theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)
# gl = ax.gridlines(crs = ccrs.PlateCarree(), linewidth = 1, linestyle = '-', color = 'black', alpha = 1, draw_labels=True)
# ax.set_boundary(circle, transform=ax.transAxes)
# ax.set_extent([-180,180,50,90], crs=ccrs.PlateCarree())

for timeind in range(900, 1111):
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


    Ls = round(float(ds.Ls[timeind,0].values), 2)
    Lsint, Lsdec = [int(part) for part in str(Ls).split('.')]
    print(f'{Lsint}-{Lsdec}')
    # contourplot = ax.contourf(ds.PV_lait[timeind,:,:].lon, ds.PV_lait[timeind,:,:].lat, ds.PV_lait[timeind,:,:].values, vmin = 0, vmax = 0.0018,
    #                             transform = ccrs.PlateCarree(), cmap='OrRd', levels=np.linspace(0, 0.0018, 13), extend = 'both', zorder=1)
    cf = ds.PV_lait[timeind,:,:].plot.contourf(ax=ax, transform=ccrs.PlateCarree(), cmap='OrRd', vmin=0, vmax=0.00035,
                                                levels=22, extend='both')


    # contourplot1 = ax.contourf(ds.cond_loc[timeind,:,:].lon, ds.cond_loc[timeind,:,:].lat, ds.cond_loc[timeind,:,:].values,
    #                             colors='none', levels=[0,1.5], hatches=['xx'], zorder=2)
    cf1 = ds.cond_loc[timeind,:,:].plot.contourf(ax=ax, transform=ccrs.PlateCarree(), colors='none', levels=[0,1.5], hatches=['xx'],
                                                    add_colorbar=False)


    plt.savefig(f'{path}/Plots/stereo_cond/stereo_condloc_{level}K_my{year}_Ls{Lsint}-{Lsdec}.pdf')

