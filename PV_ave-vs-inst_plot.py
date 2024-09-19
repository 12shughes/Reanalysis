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

year = 29
# horizontal or vertical
orientation = 'horizontal'

Ls_early = 270
Ls_late = 300

level = 300

datachoice = input('Enter directory code (o - OpenMARS, ec - EMARS control, ea - EMARS analysis, eb - EMARS background, ead - EMARS analysis different grid m2 - MACDA2): ')
while datachoice not in ['o', 'ec', 'ea', 'eb', 'ead', 'm2']:
    print('Incorrect input')
    datachoice = input('Enter directory code (o - OpenMARS, ec - EMARS control, ea - EMARS analysis, eb - EMARS background, ead - EMARS analysis different grid m2 - MACDA2): ')

if datachoice == 'o':
    dataset = 'OpenMARS_data'
    set = 'openmars'
elif datachoice == 'ec':
    dataset = 'EMARS_data/Control'
    set = 'emars'
elif datachoice == 'ea':
    dataset = 'EMARS_data/Analysis'
    set = 'emars'
elif datachoice == 'eb':
    dataset = 'EMARS_data/Background'
    set = 'emars'
elif datachoice == 'ead':
    dataset = 'EMARS_data/Analysis_diff_grid'
    set = 'emars'
elif datachoice == 'm2':
    dataset = 'MACDA2_data'
    set = 'macda2'

path = f'/disco/share/sh1293/{dataset}/Isentropic/'
print('opening data')
data = xr.open_dataset(f'{path}isentropic_{set}_my{year}.nc').astype('float32')
print('loading PV_lait')
try:
    d = data.where(data.level == level, drop=True).where(data.lat >= 50, drop=True).PV_lait*10**4
except:
    import functions as fn
    data['PV_lait'] = fn.lait_scale(data)
    d = data.where(data.level == level, drop=True).where(data.lat >= 50, drop=True).PV_lait*10**4
print('sorting Ls')
d['Ls'] = data.Ls[:,0].drop_vars('lon')
d = d.set_index(time='Ls')
print('taking time cut')
d = d.where(d.time >= Ls_early, drop = True).where(d.time <= Ls_late, drop = True)
print('taking mean')
d_mean = d.mean('time')
d_inst = d[0,:,:,:]

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
contourplot = ax.contourf(d_mean[0,:,:].lon, d_mean[0,:,:].lat, d_mean[0,:,:].values, vmin = 0, vmax = 6,
                            transform = ccrs.PlateCarree(), cmap='OrRd', levels=np.linspace(0, 6, 13), extend = 'both')
#cbar = plt.colorbar(contourplot, ticks = np.linspace(0,8,11), shrink = 0.5, fraction = 0.075, label = 'PV (MPVU)')

ax1 = fig.add_subplot(spec[1], projection=ccrs.NorthPolarStereo())
gl1 = ax1.gridlines(crs=ccrs.PlateCarree(), linewidth=1, linestyle='--', color='black', alpha=1, draw_labels=False)
gl1.xlocator = mticker.FixedLocator(meridians)
gl1.ylocator = mticker.FixedLocator(parallels)
ax1.set_boundary(circle, transform=ax1.transAxes)
ax1.set_extent([-180,180,50,90], crs=ccrs.PlateCarree())
contourplot1 = ax1.contourf(d_inst[0,:,:].lon, d_inst[0,:,:].lat, d_inst[0,:,:].values, vmin = 0, vmax = 6,
                            transform = ccrs.PlateCarree(), cmap='OrRd', levels=np.linspace(0, 6, 13), extend = 'both')
#cbar1 = plt.colorbar(contourplot1, ticks = np.linspace(0,8,11), shrink = 0.5, fraction = 0.075, label = 'PV (MPVU)')
if orientation == 'horizontal':
    cbar_ax = fig.add_axes([0.375, 0.1, 0.25, 0.03])
    cbar = plt.colorbar(contourplot, cax=cbar_ax, orientation='horizontal', ticks=np.linspace(0,6,7), label='PV (MPVU)')
elif orientation == 'vertical':
    cbar_ax = fig.add_axes([0.87, 0.25, 0.03, 0.5])
    cbar = plt.colorbar(contourplot, cax=cbar_ax, orientation='vertical', ticks=np.linspace(0,6,7), label='PV (MPVU)')


ax.text(0.5, 1.05, f'(a) Ls{Ls_early}-{Ls_late} average', horizontalalignment='center', transform=ax.transAxes)
ax1.text(0.5, 1.05, f'(b) Ls{round(d_inst.time.values.item(),2)} Instantaneous', horizontalalignment='center', transform=ax1.transAxes)


plt.savefig(f'{path}Plots/PV_ave-vs-inst_my{year}{name}_Ls{Ls_early}-{Ls_late}_{set}_{level}K.pdf')