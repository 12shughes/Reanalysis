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

Ls_early = 270
Ls_late = 300

level = 300

datachoice = input('Enter directory code (o - OpenMARS, ec - EMARS control, ea - EMARS analysis, eb - EMARS background, ead - EMARS analysis different grid, m2 - MACDA2, m2o - MACDA2_old): ')
while datachoice not in ['o', 'ec', 'ea', 'eb', 'ead', 'm2', 'm2o']:
    print('Incorrect input')
    datachoice = input('Enter directory code (o - OpenMARS, ec - EMARS control, ea - EMARS analysis, eb - EMARS background, ead - EMARS analysis different grid, m2 - MACDA2, m2o - MACDA2_old): ')

max = 6

if datachoice == 'o':
    dataset = 'OpenMARS_data'
    set = 'openmars'
    set1 = set
elif datachoice == 'ec':
    dataset = 'EMARS_data/Control'
    set = 'emars'
    set1 = set
elif datachoice == 'ea':
    dataset = 'EMARS_data/Analysis'
    set = 'emars'
    set1 = set
elif datachoice == 'eb':
    dataset = 'EMARS_data/Background'
    set = 'emars'
    set1 = set
elif datachoice == 'ead':
    dataset = 'EMARS_data/Analysis_diff_grid'
    set = 'emars'
    set1 = set
elif datachoice == 'm2':
    dataset = 'MACDA2_data'
    set = 'macda2'
    set1 = set
    max = 12
elif datachoice == 'm2o':
    dataset = 'MACDA2_data_old'
    set = 'macda2'
    set1 = 'macda2_old'

path = f'/disco/share/sh1293/{dataset}/Isentropic/'
print('opening data')
data = xr.open_dataset(f'{path}isentropic_{set}_my{year}.nc').astype('float32')
print('loading PV_lait')
try:
    d = data.where(data.level == level, drop=True).where(data.lat >= 45, drop=True).PV_lait*10**4
except:
    import functions as fn
    data['PV_lait'] = fn.lait_scale(data)
    d = data.where(data.level == level, drop=True).where(data.lat >= 50, drop=True).PV_lait*10**4
print('sorting Ls')
d['Ls'] = data.Ls[:,0].drop_vars('lon')
d = d.set_index(time='Ls')
print('taking time cut')
d = d.where(d.time >= Ls_early, drop = True).where(d.time <= Ls_late, drop = True)
d_inst = d[0,:,:,:]

# fig, ax = plt.subplots(figsize = (10,10), subplot_kw={'projection':ccrs.NorthPolarStereo()})

plt.rcParams.update({'font.size': 20})


theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)
# gl = ax.gridlines(crs = ccrs.PlateCarree(), linewidth = 1, linestyle = '-', color = 'black', alpha = 1, draw_labels=True)
# ax.set_boundary(circle, transform=ax.transAxes)
# ax.set_extent([-180,180,50,90], crs=ccrs.PlateCarree())


fig = plt.figure(figsize = (7, 8))
spec = gridspec.GridSpec(ncols=1, nrows=1, figure=fig)


#fig.suptitle('MY%02d Ls%.4f' %(my, d.time[i].values))
ax = fig.add_subplot(spec[0], projection = ccrs.NorthPolarStereo())
gl = ax.gridlines(crs = ccrs.PlateCarree(), linewidth = 1, linestyle = '--', color = 'black', alpha = 1, draw_labels=False)
meridians = [0, 60, 120, 180, -60, -120]
parallels = [50, 60, 70, 80]
gl.xlocator = mticker.FixedLocator(meridians)
gl.ylocator = mticker.FixedLocator(parallels)
gl.top_labels = False
gl.bottom_labels = False
gl.right_labels = False
gl.left_labels = False
gl.xlabels = False
# gl.ylabels = [50, 60, 70, 80]
# for parallel in parallels:
#     ax.text(0, parallel*0.995, f'{parallel}' + r'$\mathrm{\degree N}$', transform=ccrs.PlateCarree(),
#             horizontalalignment='left', verticalalignment='top',
#             fontsize=15, color='black')
ax.set_boundary(circle, transform=ax.transAxes)
ax.set_extent([-180,180,50,90], crs=ccrs.PlateCarree())
contourplot = ax.contourf(d_inst[0,:,:].lon, d_inst[0,:,:].lat, d_inst[0,:,:].values, vmin = 0, vmax = max,
                            transform = ccrs.PlateCarree(), cmap='OrRd', levels=np.linspace(0, max, 2*max+1), extend = 'both')
#cbar1 = plt.colorbar(contourplot1, ticks = np.linspace(0,8,11), shrink = 0.5, fraction = 0.075, label = 'PV (MPVU)')
# [left, bottom, width, height] 
cbar_ax = fig.add_axes([0.25, 0.1, 0.5, 0.03])
cbar = plt.colorbar(contourplot, cax=cbar_ax, orientation='horizontal', ticks=np.linspace(0,max,max+1), label=r'PV [${10^{-10}}\mathrm{m^2~s^{-1}~K~{kg}^{-1}}$]')


ax.set_title(r'North pole, $L_s=270\mathrm{\degree}$', y=1.0, pad=20)


plt.savefig(f'{path}Plots/PV_inst_my{year}_Ls{Ls_early}_{set1}_{level}K.pdf')

# print(f'{d_inst.time}')

print(f'Plot made:\n {path}Plots/PV_inst_my{year}_Ls{Ls_early}_{set1}_{level}K.pdf')