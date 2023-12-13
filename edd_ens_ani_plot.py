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
from matplotlib import gridspec

path = '/disco/share/sh1293/OpenMARS_data/'

years = [28, 29, 30, 31, 32, 33, 34, 35]

Lsmin = 200
Lsmax = 340
islev = 300

#my = 28

for my in years:
    print(my)
    files = glob.glob(path + '/Isentropic/*my%.0f.nc' %(my))
    list = range(361)
    print('opening PV')
    for file in files:
        ds = xr.open_dataset(file)
        ds['PV'] = ds['PV'] * (ds['level'] / 200)**(-(1+1/0.25))
        d = ds.PV[:,4,:9,:]*10**4
        d['Ls'] = ds.Ls[:,0].drop_vars('lon')
        d = d.set_index(time='Ls')
        d = d.where(d.time >= Lsmin, drop = True).where(d.time <= Lsmax, drop = True)
    print('opening eddy enstrophy')
    edfile = xr.open_dataarray('/disco/share/sh1293/OpenMARS_data/Eddy_enstrophy/lev000_my%02d.nc' %(my))
    edfile = edfile.where(edfile.Ls >= Lsmin, drop=True).where(edfile.Ls <= Lsmax, drop=True)
    edfile = edfile.where(edfile.level == islev, drop = True)

    fig, ax = plt.subplots(figsize = (10,10), subplot_kw={'projection':ccrs.NorthPolarStereo()})

    theta = np.linspace(0, 2*np.pi, 100)
    center, radius = [0.5, 0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpath.Path(verts * radius + center)
    gl = ax.gridlines(crs = ccrs.PlateCarree(), linewidth = 1, linestyle = '-', color = 'black', alpha = 1, draw_labels=True)
    ax.set_boundary(circle, transform=ax.transAxes)
    ax.set_extent([-180,180,50,90], crs=ccrs.PlateCarree())



    xmin = Lsmin - 10
    xmax = Lsmax + 10
    #ymin = edfile.min - 3
    ymax = np.max(edfile) + 3.


    # contourf or pcolormesh
    type = 'contourf'

    if type == 'contourf':
        for i in range(len(d[:,0,0].values)):
            print('Making plot MY%02dLs%04f' %(my, d.time[i].values))
            #fig, ax = plt.subplots(figsize = (10,10), subplot_kw={'projection':ccrs.NorthPolarStereo()})
            #fig, (ax, ax1) = plt.subplots(1, 2, figsize = (15,10), gridspec_kw={'width_ratios': [1,2]}, subplot_kw={'projection':ccrs.NorthPolarStereo()})
            fig = plt.figure(figsize = (20, 8))
            fig.suptitle('MY%02d Ls%.4f' %(my, d.time[i].values))
            spec = gridspec.GridSpec(ncols=2, nrows=1, width_ratios=[1, 1.5])
            ax = fig.add_subplot(spec[0], projection = ccrs.NorthPolarStereo())
            gl = ax.gridlines(crs = ccrs.PlateCarree(), linewidth = 1, linestyle = '-', color = 'black', alpha = 1, draw_labels=True)
            ax.set_boundary(circle, transform=ax.transAxes)
            ax.set_extent([-180,180,50,90], crs=ccrs.PlateCarree())
            contourplot = ax.contourf(d[i,:,:].lon, d[i,:,:].lat, d[i,:,:].values, vmin = 0, vmax = 8,
                                        transform = ccrs.PlateCarree(), cmap='viridis', levels=np.linspace(0, 8, 21), extend = 'both')
            cbar = plt.colorbar(contourplot, ticks = np.linspace(0,8,11), shrink = 0.5, fraction = 0.075)
            

            ax1 = fig.add_subplot(spec[1])
            ax1.plot(edfile.Ls[:i+1], edfile.values[:i+1])
            ax1.set_xlim(left = xmin, right = xmax)
            ax1.set_ylim(bottom = -3, top = ymax)
            ax1.set_ylabel('Eddy enstrophy')
            ax1.set_xlabel('Ls')
            ax1.plot(edfile.Ls[i], edfile.values[i], marker = '.', color = 'red', ms = 10)
            ax1.plot([xmin - 10, edfile.Ls[i]], [edfile.values[i]] * 2, color = 'red', alpha = 0.5, linestyle = '--')

            fig.tight_layout()
            plt.savefig(path + '/Eddy_enstrophy/Ani_plots/MY%02d/edd_ens_my%02dLs%03d_%04d.png' %(my, my, math.modf(d.time[i].values)[1], (
                math.modf(d.time[i].values)[0])*10**4))
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

