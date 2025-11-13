import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import functions as fcs

year = 29

Ls_early = 270
Ls_late = 330

max = 6

path = f'/disco/share/sh1293/EMARS_data/Analysis/Isobaric-v2'
print('opening data')
data = xr.open_dataset(f'{path}/isobaric-v2_emars_my{year}.nc').astype('float32')
data_winter = data.where(data.Ls >= Ls_early, drop=True).where(data.Ls <= Ls_late, drop=True)
data_winter['theta'] = fcs.calculate_theta(data_winter.temp, data_winter.pfull)
data_winter_ave = data_winter.mean('time')
data_ave = data_winter_ave.mean('lon')
print('Lait scaling')
data_ave['PV'] = fcs.lait_scale(data_ave, theta=True)/10**-4
data_ave = data_ave.where(data_ave != np.nan, drop=True)
maxPV = data_ave.max('lat')
maxPV_lat_ind = np.where(data_ave.PV_lait == maxPV.PV_lait)[1]
max_lats = []
for levind in range(len(data_ave.pfull)):
    print(levind)
    if maxPV_lat_ind[levind] != 0:
        try:
            PV_nearall = data_ave.PV_lait[levind, maxPV_lat_ind[levind]-1:maxPV_lat_ind[levind]+2]
            lats_nearall = data_ave.lat[maxPV_lat_ind[levind]-1:maxPV_lat_ind[levind]+2]
            PV_near = PV_nearall#[~np.isnan(PV_nearall)]
            lats_near = lats_nearall#[~np.isnan(PV_nearall)]
            fine_lats = np.linspace(lats_near[0], lats_near[-1], 200)
        #elif maxPV_lat_ind[levind] == 0:
        #    PV_nearall  = data_ave.PV[levind, maxPV_lat_ind[levind]:maxPV_lat_ind[levind]+3]
        #    lats_nearall = data_ave.lat[maxPV_lat_ind[levind]:maxPV_lat_ind[levind]+3]
        #    PV_near = PV_nearall[~np.isnan(PV_nearall)]
        #    lats_near = lats_nearall[~np.isnan(PV_nearall)]
        #    fine_lats = np.linspace(90., lats_near[-1], 200)
        #if len(PV_near) == 3:
            coefs = np.ma.polyfit(lats_near, PV_near, 2)
            quad = coefs[2] + coefs[1]*fine_lats + coefs[0]*fine_lats**2
        #elif len(PV_near) == 2:
        #    coefs = np.ma.polyfit(lats_near, PV_near, 1)
        #    quad = coefs[1] + coefs[0]*fine_lats
            max_lat = fine_lats[np.where(quad == max(quad))][0]
            max_lats.append(max_lat)
        except:
            max_lats.append(np.nan)
    elif maxPV_lat_ind[levind] == 0:
        max_lats.append(87.5)
i+=1



    
im = data_ave.PV_lait.plot.contourf(x='lat', y='pfull', ax=axs[r, c], cmap='OrRd', levels=[-0.5,0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7],
                                extend = 'max', vmin = -0.5, vmax = 7., add_colorbar=False)
im1 = data_ave.theta.plot.contour(x='lat', y='pfull', ax=axs[r,c], levels=[200,300,400,500,600,700,800,900,1000,1100], linestyles='--', colors='black', linewidths=1)
axs[r,c].set_title('%s MY%d' %(title, my))
axs[r,c].set_xlabel('Latitude')
axs[r,c].set_ylabel('Pressure (Pa)')
axs[r,c].set_xlim([0,90])
axs[r,c].set_ylim([610, 0.1])
axs[r,c].set_yscale('log')
axs[r,c].plot(max_lats, data_ave.pfull.values, color = 'blue')
    

fig.colorbar(im, ax=axs.ravel().tolist(), ticks=[1,2,3,4,5,6,7], label='PV (MPVU)')
fig.suptitle('Ls%d-%d' %(Lsmin, Lsmax))
plt.savefig(f'/disco/share/sh1293/EMARS_data/new-pres_PV_plot_my{year}_Ls{Ls_early}-{Ls_late}.pdf')