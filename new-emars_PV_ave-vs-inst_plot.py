import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import xarray as xr
import glob
from cartopy import crs as ccrs
import matplotlib.path as mpath
import math
from matplotlib import (cm, colors)
from matplotlib import gridspec
import pdb
import matplotlib.ticker as mticker
import functions as fcs
import os

year = 29
# horizontal or vertical
orientation = 'horizontal'

Ls_early = 270
Ls_late = 300

level = 300

max = 6

path = f'/disco/share/sh1293/EMARS_data/Analysis/Isentropic-v2'
print('opening data')
data = xr.open_dataset(f'{path}/isentropic-v2_emars_my{year}.nc').astype('float32')
print('selecting time')
d3 = data#.where(data.MY==year, drop=True)
d2 = d3.where(d3.Ls>=Ls_early, drop=True)
d1 = d2.where(d2.Ls<=Ls_late, drop=True)
print('loading PV_lait')
d = d1.where(d1.lat>=45, drop=True).sel(level=level)
print('taking mean')
d = d.PV_lait*10**4
d_mean = d.mean('time')
d_inst = d[0,:,:]
# pdb.set_trace()

# fig, ax = plt.subplots(figsize = (10,10), subplot_kw={'projection':ccrs.NorthPolarStereo()})

plt.rcParams.update({'font.size': 25})


theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)
# gl = ax.gridlines(crs = ccrs.PlateCarree(), linewidth = 1, linestyle = '-', color = 'black', alpha = 1, draw_labels=True)
# ax.set_boundary(circle, transform=ax.transAxes)
# ax.set_extent([-180,180,50,90], crs=ccrs.PlateCarree())

if orientation == 'horizontal':
    fig = plt.figure(figsize = (14, 8))
    spec = gridspec.GridSpec(ncols=2, nrows=1, width_ratios=[1, 1], figure=fig)
    name = ''
elif orientation == 'vertical':
    fig = plt.figure(figsize = (8, 14))
    spec = gridspec.GridSpec(ncols=1, nrows=2, height_ratios=[1, 1], figure=fig)
    name = '_vert'
#fig.suptitle('MY%02d Ls%.4f' %(my, d.time[i].values))
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
contourplot = ax.contourf(d_mean.lon, d_mean.lat, d_mean.values, vmin = 0, vmax = max,
                            transform = ccrs.PlateCarree(), cmap='OrRd', levels=np.linspace(0, max, 13), extend = 'both')
#cbar = plt.colorbar(contourplot, ticks = np.linspace(0,8,11), shrink = 0.5, fraction = 0.075, label = 'PV (MPVU)')

ax1 = fig.add_subplot(spec[1], projection=ccrs.NorthPolarStereo())
gl1 = ax1.gridlines(crs=ccrs.PlateCarree(), linewidth=1, linestyle='--', color='black', alpha=1, draw_labels=False)
gl1.xlocator = mticker.FixedLocator(meridians)
gl1.ylocator = mticker.FixedLocator(parallels)
ax1.set_boundary(circle, transform=ax1.transAxes)
ax1.set_extent([-180,180,50,90], crs=ccrs.PlateCarree())
contourplot1 = ax1.contourf(d_inst.lon, d_inst.lat, d_inst.values, vmin = 0, vmax = max,
                            transform = ccrs.PlateCarree(), cmap='OrRd', levels=np.linspace(0, max, 13), extend = 'both')
#cbar1 = plt.colorbar(contourplot1, ticks = np.linspace(0,8,11), shrink = 0.5, fraction = 0.075, label = 'PV (MPVU)')
if orientation == 'horizontal':
    cbar_ax = fig.add_axes([0.375, 0.1, 0.25, 0.03])
    cbar = plt.colorbar(contourplot, cax=cbar_ax, orientation='horizontal', ticks=np.linspace(0,max,7), label='Lait-scaled PV (MPVU)')
elif orientation == 'vertical':
    cbar_ax = fig.add_axes([0.87, 0.25, 0.03, 0.5])
    cbar = plt.colorbar(contourplot, cax=cbar_ax, orientation='vertical', ticks=np.linspace(0,max,7), label='Lait-scaled PV (MPVU)')


# ax.text(0.5, 1.05, f'(a) Ls{Ls_early}-{Ls_late} average', horizontalalignment='center', transform=ax.transAxes)
# ax1.text(0.5, 1.05, f'(b) Ls{round(d_inst.time.values.item(),2)} Instantaneous', horizontalalignment='center', transform=ax1.transAxes)

ax.text(0.5, 1.05, f'(a) 30 sol average', horizontalalignment='center', transform=ax.transAxes)
ax1.text(0.5, 1.05, f'(b) Instantaneous', horizontalalignment='center', transform=ax1.transAxes)

if not os.path.exists(f'{path}/Plots/'):
    os.makedirs(f'{path}/Plots/')

plt.savefig(f'{path}/Plots/PV_ave-vs-inst_my{year}{name}_Ls{Ls_early}-{Ls_late}.pdf')

print(f'Plot made: \n {path}/Plots/PV_ave-vs-inst_my{year}{name}_Ls{Ls_early}-{Ls_late}.pdf')