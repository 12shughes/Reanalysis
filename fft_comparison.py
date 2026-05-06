import numpy as np
import xarray as xr
import xrft
import matplotlib.pyplot as plt
import matplotlib.path as mpath
from matplotlib import (cm, colors, gridspec)
import matplotlib.ticker as mticker
import matplotlib.patches as patches
from cartopy import crs as ccrs
import functions as fcs

### need to work out which of analysis, background, and control is what I want - I think analysis and control

def fft(da, lat_centre, lat_range, max_wav):
    da_lat = da.where(da.lat<=lat_centre+lat_range/2, drop=True).where(da.lat>=lat_centre-lat_range/2, drop=True)
    da_mean = da_lat.mean(dim='lat')
    fft = np.abs(xrft.fft(da_mean, dim='lon'))
    fft = fft.assign_coords({'freq_lon':fft.freq_lon*360.})
    fft_pos = fft.where(fft.freq_lon>=0, drop=True)
    fft_select = fft_pos.where(fft_pos.freq_lon<=max_wav, drop=True)
    return fft_select


def processing(file, Ls_early, Ls_late):
    ds = xr.open_dataset(file)
    q = ds.PV.sel(level=275)
    # breakpoint()
    qtime = q.where(ds.Ls>=Ls_early, drop=True).where(ds.Ls<=Ls_late, drop=True)
    qzm = qtime.mean(dim='lon').mean(dim='time')
    data_ave = qzm
    # breakpoint()
    maxPV = data_ave.max('lat')
    maxPV_lat_ind = np.where(data_ave == maxPV)[0][0]
    if maxPV_lat_ind != 0:
        try:
            print('trying') 
            PV_nearall = data_ave[maxPV_lat_ind-1:maxPV_lat_ind+2]
            lats_nearall = data_ave.lat[maxPV_lat_ind-1:maxPV_lat_ind+2]
            PV_near = PV_nearall
            lats_near = lats_nearall
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
        except:
            print('except')
            max_lat = data_ave.lat[maxPV_lat_ind]
    elif maxPV_lat_ind == 0:
        max_lat = 87.5
    print(max_lat)
    qzm_maxlat = max_lat

    # qzm_maxlat = 75.
    # breakpoint()
    q_fft = fft(qtime, qzm_maxlat, 10, 100)
    q_fft_mean = q_fft.mean(dim='time')
    q_fft_mean_cut = q_fft_mean[1:11]/q_fft_mean[0]
    return q_fft_mean_cut, qtime.mean(dim='time'), qzm_maxlat


def processing_easy(file, Ls_early, Ls_late, level=300):
    ds = xr.open_dataset(file)
    q = ds.PV.sel(level=level)
    q_lait = q*(level/200)**-5
    qtime = q_lait.where(ds.Ls>=Ls_early, drop=True).where(ds.Ls<=Ls_late, drop=True)
    fftq = fft(qtime, 75., 10, 100)
    fft_mean = fftq.mean(dim='time')
    fft_mean_cut = fft_mean[1:11]/fft_mean[0]
    return fft_mean_cut, qtime


year = 26
type = 'Control'

filea = f'/disco/share/sh1293/EMARS_data/Analysis/Isentropic/isentropic_emars_my{year}.nc'
filec = f'/disco/share/sh1293/EMARS_data/{type}/Isentropic/isentropic_emars_my{year}.nc'

Ls_early = 270
Ls_late = 300

################################
# if doing the mean across the three years
# patha = f'/disco/share/sh1293/EMARS_data/Analysis/Isentropic'
# pathc = f'/disco/share/sh1293/EMARS_data/Control/Isentropic'
# for year in [24, 25, 26]:
#     print(year)
#     dsa = xr.open_dataset(f'{patha}/isentropic_emars_my{year}.nc')
#     qa = dsa.PV.sel(level=300)
#     qtimea = qa.where(dsa.Ls>=Ls_early, drop=True).where(dsa.Ls<=Ls_late, drop=True)
#     dsc = xr.open_dataset(f'{pathc}/isentropic_emars_my{year}.nc')
#     qc = dsc.PV.sel(level=300)
#     qtimec = qc.where(dsc.Ls>=Ls_early, drop=True).where(dsc.Ls<=Ls_late, drop=True)
#     if year == 24:
#         resulta = qtimea
#         resultc = qtimec
#     else:
#         resulta = xr.concat([resulta, qtimea], dim='time')
#         resultc = xr.concat([resultc, qtimec], dim='time')
# # breakpoint()
# ffta = fft(resulta, 75., 10, 100)
# fftc = fft(resultc, 75., 10, 100)
# ffta_mean = ffta.mean(dim='time')
# fftc_mean = fftc.mean(dim='time')
# ffta_mean_cut = ffta_mean[1:11]/ffta_mean[0]
# fftc_mean_cut = fftc_mean[1:11]/fftc_mean[0]

# dataa = ffta_mean_cut
# datac = fftc_mean_cut
# maxlata = 75.
# maxlatc = 75.
# qmeana = resulta.mean(dim='time')
# qmeanc = resultc.mean(dim='time')




##################
# if doing individual years
dataa, qa = processing_easy(filea, Ls_early, Ls_late)
datac, qc = processing_easy(filec, Ls_early, Ls_late)

plt.rcParams.update({'font.size': 16})

fig = plt.figure(figsize=(10, 12))

gs = gridspec.GridSpec(3, 2, figure=fig, height_ratios=[10,1,15])

theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)

ax0 = fig.add_subplot(gs[0,0], projection=ccrs.NorthPolarStereo())
ax1 = fig.add_subplot(gs[0,1], projection=ccrs.NorthPolarStereo())
# cbarax = fig.add_subplot(gs[1,:])
ax2 = fig.add_subplot(gs[2,:])

meridians = [0, 60, 120, 180, -60, -120]
parallels = [50, 60, 70, 80]
for ax in [ax0, ax1]:
    gl = ax.gridlines(crs = ccrs.PlateCarree(), linewidth = 1, linestyle = '--', color = 'black', alpha = 1, draw_labels=False)
    gl.xlocator = mticker.FixedLocator(meridians)
    gl.ylocator = mticker.FixedLocator(parallels)
    gl.xlabels = False
    ax.set_boundary(circle, transform=ax.transAxes)
    ax.set_extent([-180,180,50,90], crs=ccrs.PlateCarree())

max = 7

contourplot = ax0.contourf(qa[0,:,:].lon, qa[0,:,:].lat, qa[0,:,:].values/10**-4, vmin = 0, vmax = max,
                            transform = ccrs.PlateCarree(), cmap='OrRd', levels=np.linspace(0, max, max+1), extend = 'both')
contourplot1 = ax1.contourf(qc[0,:,:].lon, qc[0,:,:].lat, qc[0,:,:].values/10**-4, vmin = 0, vmax = max,
                            transform = ccrs.PlateCarree(), cmap='OrRd', levels=np.linspace(0, max, max+1), extend = 'both')


# plota = dataa.plot(ax=ax2, label=f'Analysis', color='k', marker='o')
# plotc = datac.plot(ax=ax2, label=f'{type}', linestyle='--', color='k', marker='x')
ax2.plot(dataa.freq_lon, dataa, color='k', marker='o', label='Reanalysis')
ax2.plot(datac.freq_lon, datac, color='k', marker='x', label='Free-running MGCM', linestyle='--')
ax2.set_ylabel('Amplitude')
ax2.set_xlabel('Zonal wavenumber')
ax2.set_title('(c) Fourier decomposition into zonal wavenumbers')
ax2.set_xticks(ticks=dataa.freq_lon, labels=['', 2, '', 4, '', 6, '', 8, '', 10])
plt.legend()

pos0 = ax0.get_position()
pos1 = ax1.get_position()
center_x = (pos0.x0+pos1.x1)/2
width = 0.25
cbar_ax = fig.add_axes([center_x-width/2, 0.585, 0.25, 0.03])
cbar = plt.colorbar(contourplot, cax=cbar_ax, orientation='horizontal', ticks=np.linspace(0,max,max+1), label='Lait-scaled PV (MPVU)')


# ax0.text(0.5, 1.05, f'(a) Reanalysis', horizontalalignment='center', transform=ax0.transAxes)
# ax1.text(0.5, 1.05, f'(b) Free-running MGCM', horizontalalignment='center', transform=ax1.transAxes)

ax0.set_title(f'(a) Reanalysis')
ax1.set_title(f'(b) Free-running MGCM')


plt.savefig(f'/disco/share/sh1293/EMARS_data/Plots/FFT/fft-comp-{year}.pdf', bbox_inches='tight')
print(f' Fig made:\n/disco/share/sh1293/EMARS_data/Plots/FFT/fft-comp-{year}.pdf')


########################################################



# plota = dataa.plot(ax=axs[1], label=f'Analysis {maxlata:.1f}')
# plotc = datac.plot(ax=axs[1], label=f'{type} {maxlatc:.1f}', linestyle='--')
# plt.legend()

# plt.savefig(f'/disco/share/sh1293/EMARS_data/Plots/FFT/fft_comparison_{type}_{year}.pdf')
# print(f' Fig made:\n/disco/share/sh1293/EMARS_data/Plots/FFT/fft_comparison_{type}_{year}.pdf')

# plt.clf()

# theta = np.linspace(0, 2*np.pi, 100)
# center, radius = [0.5, 0.5], 0.5
# verts = np.vstack([np.sin(theta), np.cos(theta)]).T
# circle = mpath.Path(verts * radius + center)

# # breakpoint()

# max = np.max([qmeana, qmeanc])

# fig = plt.figure(figsize = (14, 8))
# spec = gridspec.GridSpec(ncols=2, nrows=1, width_ratios=[1, 1], figure=fig)
# ax = fig.add_subplot(spec[0], projection = ccrs.NorthPolarStereo())
# gl = ax.gridlines(crs = ccrs.PlateCarree(), linewidth = 1, linestyle = '--', color = 'black', alpha = 1, draw_labels=False)
# meridians = [0, 60, 120, 180, -60, -120]
# parallels = [50, 60, 70, 80]
# gl.xlocator = mticker.FixedLocator(meridians)
# gl.ylocator = mticker.FixedLocator(parallels)
# gl.xlabels = False
# #gl.ylabels = [True if parallel in [50] else False]
# ax.set_boundary(circle, transform=ax.transAxes)
# ax.set_extent([-180,180,50,90], crs=ccrs.PlateCarree())
# contourplot = ax.contourf(qmeana.lon, qmeana.lat, qmeana.values, vmin = 0, vmax = max,
#                             transform = ccrs.PlateCarree(), cmap='OrRd', levels=np.linspace(0, max, 13), extend = 'both')
# gla = ax.gridlines(crs=ccrs.PlateCarree(), linewidth=1, linestyle='-', color='deepskyblue', alpha=1, draw_labels=False)
# gla.ylocator = mticker.FixedLocator([maxlata])
# gla.xlocator = mticker.FixedLocator([])
# #cbar = plt.colorbar(contourplot, ticks = np.linspace(0,8,11), shrink = 0.5, fraction = 0.075, label = 'PV (MPVU)')

# ax1 = fig.add_subplot(spec[1], projection=ccrs.NorthPolarStereo())
# gl1 = ax1.gridlines(crs=ccrs.PlateCarree(), linewidth=1, linestyle='--', color='black', alpha=1, draw_labels=False)
# gl1.xlocator = mticker.FixedLocator(meridians)
# gl1.ylocator = mticker.FixedLocator(parallels)
# ax1.set_boundary(circle, transform=ax1.transAxes)
# ax1.set_extent([-180,180,50,90], crs=ccrs.PlateCarree())
# contourplot1 = ax1.contourf(qmeanc.lon, qmeanc.lat, qmeanc.values, vmin = 0, vmax = max,
#                             transform = ccrs.PlateCarree(), cmap='OrRd', levels=np.linspace(0, max, 13), extend = 'both')
# glc = ax1.gridlines(crs=ccrs.PlateCarree(), linewidth=1, linestyle='-', color='deepskyblue', alpha=1, draw_labels=False)
# glc.ylocator = mticker.FixedLocator([maxlatc])
# glc.xlocator = mticker.FixedLocator([])

# #cbar1 = plt.colorbar(contourplot1, ticks = np.linspace(0,8,11), shrink = 0.5, fraction = 0.075, label = 'PV (MPVU)')
# cbar_ax = fig.add_axes([0.375, 0.1, 0.25, 0.03])
# cbar = plt.colorbar(contourplot, cax=cbar_ax, orientation='horizontal', ticks=np.linspace(0,max,7), label='Lait-scaled PV (MPVU)')



# # ax.text(0.5, 1.05, f'(a) Ls{Ls_early}-{Ls_late} average', horizontalalignment='center', transform=ax.transAxes)
# # ax1.text(0.5, 1.05, f'(b) Ls{round(qmeanc.time.values.item(),2)} Instantaneous', horizontalalignment='center', transform=ax1.transAxes)

# ax.text(0.5, 1.05, f'(a) Analysis', horizontalalignment='center', transform=ax.transAxes)
# ax1.text(0.5, 1.05, f'(b) {type}', horizontalalignment='center', transform=ax1.transAxes)

# plt.savefig(f'/disco/share/sh1293/EMARS_data/Plots/FFT/fft_stereo_{type}_{year}.pdf')
# print(f' Fig made:\n/disco/share/sh1293/EMARS_data/Plots/FFT/fft_stereo_{type}_{year}.pdf')