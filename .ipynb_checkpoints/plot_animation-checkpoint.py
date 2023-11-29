import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import xarray as xr
import glob
from cartopy import crs as ccrs
import matplotlib.path as mpath
import matplotlib.ticker as ticker

path = '/disco/share/sh1293/OpenMARS_data/Isentropic/'
my = 27
files = glob.glob(path + '*my%.0f.nc' %(my))
for file in files:
    ds = xr.open_dataset(file)
    d = ds.PV[:,4,:9,:]
    d['Ls'] = ds.Ls[:,:]

def animate(i):
    #ax.clear()
    cf = ax.contourf(d[i,:,:].lon, d[i,:,:].lat, d[i,:,:].values, transform = ccrs.PlateCarree(), levels = 21,
                     vmax = zmax, vmin = zmin)
    plt.title('My%.0f Ls%.2f' %(my, d.Ls[i,0].values))
    #plt.colorbar(cf, ax = ax)
    return cf

fig, ax = plt.subplots(figsize = (10,10), subplot_kw={'projection':ccrs.NorthPolarStereo()})

theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)
gl = ax.gridlines(crs = ccrs.PlateCarree(), linewidth = 1, linestyle = '-', color = 'black', alpha = 1, draw_labels=True)
ax.set_boundary(circle, transform=ax.transAxes)
ax.set_extent([-180,180,50,90], crs=ccrs.PlateCarree())

zmax = np.max(d.values)
zmin = np.min(d.values)

contourplot = ax.contourf(d[0,:,:].lon, d[0,:,:].lat, d[0,:,:].values, transform = ccrs.PlateCarree(), levels = 21,
                          vmax = zmax, vmin = zmin)
cbar = plt.colorbar(contourplot)

print('creating animation')
ani = animation.FuncAnimation(fig=fig, func=animate, frames = int(len(d[:,0,0])/4), interval = 0.1)

fig.tight_layout()

print('saving animation')
ani.save('/home/links/sh1293/Reanalysis/plot.gif', writer = 'pillow')