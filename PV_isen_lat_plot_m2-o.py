import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import functions as fcs

Lsmin = 240
Lsmax = 300

i = 0
fig, axs = plt.subplots(2, 8, sharex=True, sharey=True, figsize = (60,10))
while i<=15:
    c = int(i/2)
    r = np.remainder(i, 2)
    if r == 0:
        type = 'MACDA2_data/'
        dataset = 'macda2'
        title = 'MACDA2'
    elif r == 1:
        type = 'OpenMARS_data/'
        dataset = 'openmars'
        title = 'OpenMARS'
    path = '/disco/share/sh1293/%s/Isentropic/' %(type)
    if c == 0:
        my = 28
    elif c == 1:
        my = 29
    elif c == 2:
        my = 30
    elif c == 3:
        my = 31
    elif c == 4:
        my = 32
    elif c == 5:
        my = 33
    elif c == 6:
        my = 34
    elif c == 7:
        my = 35
    
    print('%s MY%d' %(type[:-1], my))
    data = xr.open_dataset(path + 'isentropic_%s_my%d.nc' %(dataset, my))
    data_winter = data.where(data.Ls >= Lsmin, drop=True)
    data_winter = data_winter.where(data_winter.Ls <= Lsmax, drop=True)
    data_winter_ave = data_winter.mean('time')
    data_ave = data_winter_ave.mean('lon')
    if dataset == 'openmars':
        print('Lait scaling')
        data_ave['PV_lait'] = fcs.lait_scale(data_ave)
    data_ave['PV'] = data_ave.PV_lait
    maxPV = data_ave.max('lat')
    maxPV_lat_ind = np.where(data_ave.PV == maxPV.PV)[1]
    max_lats = []
    for levind in range(len(data_ave.level)):
        print(levind)
        if maxPV_lat_ind[levind] != 0:
            PV_nearall = data_ave.PV[levind, maxPV_lat_ind[levind]-1:maxPV_lat_ind[levind]+2]
            lats_nearall = data_ave.lat[maxPV_lat_ind[levind]-1:maxPV_lat_ind[levind]+2]
            PV_near = PV_nearall[~np.isnan(PV_nearall)]
            lats_near = lats_nearall[~np.isnan(PV_nearall)]
            fine_lats = np.linspace(lats_near[0], lats_near[-1], 200)
        elif maxPV_lat_ind[levind] == 0:
            PV_nearall  = data_ave.PV[levind, maxPV_lat_ind[levind]:maxPV_lat_ind[levind]+3]
            lats_nearall = data_ave.lat[maxPV_lat_ind[levind]:maxPV_lat_ind[levind]+3]
            PV_near = PV_nearall[~np.isnan(PV_nearall)]
            lats_near = lats_nearall[~np.isnan(PV_nearall)]
            fine_lats = np.linspace(90., lats_near[-1], 200)
        if len(PV_near) == 3:
            coefs = np.ma.polyfit(lats_near, PV_near, 2)
            quad = coefs[2] + coefs[1]*fine_lats + coefs[0]*fine_lats**2
        elif len(PV_near) == 2:
            coefs = np.ma.polyfit(lats_near, PV_near, 1)
            quad = coefs[1] + coefs[0]*fine_lats
        max_lat = fine_lats[np.where(quad == max(quad))][0]
        max_lats.append(max_lat)
    i+=1



    
    im = data_ave.PV.plot.contourf(x='lat', ax = axs[r, c], cmap='viridis', levels=21, extend = 'both', vmin = 0., vmax = 0.0015, add_colorbar=False)
    axs[r,c].set_title('%s MY%d' %(title, my))
    axs[r,c].set_xlabel('Latitude')
    axs[r,c].set_ylabel('Potential temperature')
    axs[r,c].set_xlim([0,90])
    axs[r,c].plot(max_lats, data_ave.level.values, color = 'red')

fig.colorbar(im, ax=axs.ravel().tolist())
fig.suptitle('Ls%d-%d' %(Lsmin, Lsmax))
plt.savefig('/disco/share/sh1293/MACDA2_data/all_data_grid_PV_Ls%d-%d.pdf' %(Lsmin, Lsmax))
