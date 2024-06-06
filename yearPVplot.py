import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import functions as fcs

root = '/disco/share/sh1293/EMARS_data/Analysis/Isentropic/'
print('loading data')
data1 = xr.open_dataset(root + 'isentropic_emars_my24.nc')
data2 = xr.open_dataset(root + 'isentropic_emars_my25.nc')
print('splitting data')
data1 = data1.where(data1.Ls >= 141, drop=True)
data2 = data2.where(data2.Ls <= 140, drop=True)
print('joining data')
data = xr.concat([data1, data2], dim='time')
print('zonal average')
data = data.mean(dim='lon')
print('lait scale')
data['PV'] = fcs.lait_scale(data)
print('assign coords')
data = data.assign_coords({'Ls':data.Ls})
#data = data.swap_dims({'time':'Ls'})
print('select level')
data = data.where(data.level == 300, drop=True).mean(dim='level')
print('making plot')
fig, ax = plt.subplots(1, 1, figsize = (10,7))
#ax.set_xlim([141, 140])
ax.set_ylim([-90, 90])
Lslist = [150,180,210,240,270,300,330,360,30,60,90,120]
Lslabels = ['150','180','210','240','270','300','330','360','30','60','90','120']
timelist = Lslist
for i in range(len(Lslist)):
    timelist[i] = data.where(data.Ls >= Lslist[i]-0.01, drop=True).where(data.Ls <= Lslist[i]+0.01, drop=True).time.values[0]
PVim = data.PV.plot.contourf(x='time', y='lat', ax=ax, cmap='RdBu_r', levels=17, vmin=-0.00045, vmax=0.00045, extend='both')
ax.set_xticks(ticks=timelist, labels=Lslabels)
ax.set_yticks([-90,-60,-30,0,30,60,90])
#uim1 = data.ucomp.plot.contour(x='Ls', y='lat', levels=[20,40,60,100], linestyles='-', colors='black')
#uim2 = data.ucomp.plot.contour(x='Ls', y='lat', levels=[-20,-40,-60,-100], linestyles='--', colors='black')
#uim2 = data.ucomp.plot.contour(x='time', y='lat', levels=[0], linestyles='-', colors='black')
plt.savefig('/disco/share/sh1293/EMARS_data/Analysis/u_PV_year.pdf')