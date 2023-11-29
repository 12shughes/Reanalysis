'''
rsync -a sh1293@maths2:/disco/share/sh1293/OpenMARS_data/Isentropic/Plots/ /Users/sh1293/Documents/PhD/Plots/
ffmpeg -framerate 1 -pattern_type glob -i '/Users/sh1293/Documents/PhD/Plots/*.png' -c:v libx264 -r 30 output.mp4
'''


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import xarray as xr
import glob
from cartopy import crs as ccrs
import matplotlib.path as mpath
import matplotlib.ticker as ticker
import math
from matplotlib import (cm, colors)

path = '/disco/share/sh1293/OpenMARS_data/Isentropic/'
my = 28
files = glob.glob(path + '*my%.0f.nc' %(my))
list = range(361)
for file in files:
    ds = xr.open_dataset(file)
    ds['PV'] = ds['PV'] * (ds['level'] / 200)**(-(1+1/0.25))
    d = ds.PV[:,4,:9,:]*10**4
    d['Ls'] = ds.Ls[:,0].drop_vars('lon')
    d = d.set_index(time='Ls')


fig, ax = plt.subplots(figsize = (10,10), subplot_kw={'projection':ccrs.NorthPolarStereo()})

theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)
gl = ax.gridlines(crs = ccrs.PlateCarree(), linewidth = 1, linestyle = '-', color = 'black', alpha = 1, draw_labels=True)
ax.set_boundary(circle, transform=ax.transAxes)
ax.set_extent([-180,180,50,90], crs=ccrs.PlateCarree())



#vmin = 1
#vmax = 6.6
#step = 0.5


# contourf or pcolormesh
type = 'contourf'

if type == 'contourf':
    for i in range(len(d[:,0,0].values)):
        fig, ax = plt.subplots(figsize = (10,10), subplot_kw={'projection':ccrs.NorthPolarStereo()})
        gl = ax.gridlines(crs = ccrs.PlateCarree(), linewidth = 1, linestyle = '-', color = 'black', alpha = 1, draw_labels=True)
        ax.set_boundary(circle, transform=ax.transAxes)
        ax.set_extent([-180,180,50,90], crs=ccrs.PlateCarree())
        contourplot = ax.contourf(d[i,:,:].lon, d[i,:,:].lat, d[i,:,:].values, vmin = 0, vmax = 8,
                                    transform = ccrs.PlateCarree(), cmap='viridis', levels=np.linspace(0, 8, 21), extend = 'both')
        cbar = plt.colorbar(contourplot, ticks = np.linspace(0,8,11), shrink = 0.5, fraction = 0.075)
        plt.title('MY%02d Ls%.4f' %(my, d.time[i].values))
        fig.tight_layout()
        plt.savefig(path + '/Plots/MY%02d/ctf_my%02dLs%03d_%04d.png' %(my, my, math.modf(d.time[i].values)[1], (math.modf(d.time[i].values)[0])*10**4))
elif type == 'pcolormesh':
    i = 0
    #for i in range(len(d[:,0,0].values)):
    fig, ax = plt.subplots(figsize = (10,10), subplot_kw={'projection':ccrs.NorthPolarStereo()})
    gl = ax.gridlines(crs = ccrs.PlateCarree(), linewidth = 1, linestyle = '-', color = 'black', alpha = 1, draw_labels=True)
    ax.set_boundary(circle, transform=ax.transAxes)
    ax.set_extent([-180,180,50,90], crs=ccrs.PlateCarree())
    X, Y = np.meshgrid(d[i,:,:].lon, d[i,:,:].lat)
    contourplot = ax.pcolormesh(X, Y, d[i,:,:].values, transform = ccrs.PlateCarree())# vmin = 0, vmax = 8,
                                #transform = ccrs.PlateCarree(), cmap='viridis')
    cbar = plt.colorbar(contourplot, ticks = np.linspace(0,8,11), shrink = 0.5, fraction = 0.075, extend = 'both')
    plt.title('MY%02d Ls%.4f' %(my, d.time[i].values))
    fig.tight_layout()
    plt.savefig(path + '/Plots/MY%02d/pcm_my%02dLs%03d_%04d.png' %(my, my, math.modf(d.time[i].values)[1], (math.modf(d.time[i].values)[0])*10**4))

