import numpy as np
from scipy import signal
import xarray as xr
import matplotlib.pyplot as plt

directory = 'OpenMARS_data'
name = 'openmars'
year = 29
Ls_early = 270
Ls_late = 300
level = 200
latmin = 50.0
thresh = 1
lagmin = -300
lagmax = 300

latint, latdec = [int(part) for part in str(latmin).split('.')]
root_path = '/disco/share/sh1293'
path = f'{root_path}/{directory}/Isentropic'
ds = xr.open_dataset(f'{path}/isentropic_{name}_my{year}.nc').astype('float32')
ds1 = xr.open_dataset(f'{root_path}/{directory}/CO2_ice/co2ice_openmars_my{year}.nc').astype('float32')

# ds = ds.where(ds.lat>=latmin).dropna(dim='lat')
ds = ds.sel(level=level)
ds = ds.reset_coords('level', drop=True)
ds['Ls'] = ds.Ls.mean(dim='lon', skipna=True)
ds1['Ls'] = ds.Ls
ds = ds.where(ds.Ls>=Ls_early).where(ds.Ls<=Ls_late).dropna(dim='time', how='all')
ds['T_c'] = 149.2+6.49*np.log(0.00135*ds.pressure*100).astype('float32')
ds['cond_loc'] = xr.where(ds.temp <= ds.T_c+thresh, 1, np.nan)

# ds1 = ds1.where(ds1.lat>=latmin).dropna(dim='lat')

ds1 = ds1.where(ds1.Ls>=Ls_early).where(ds1.Ls<=Ls_late).dropna(dim='time', how='all')
ds1['co2grad'] = ds1.co2ice.differentiate(coord='time')
ds1['co2diff'] = ds1.co2ice.diff(dim='time')/ds1.time.diff(dim='time')


x = ds.PV-ds.PV.mean(dim='lon').mean(dim='lat').mean(dim='time')
y = -(ds.T_c+thresh-ds.temp)
xname = 'PV-PV_mean'
yname = 'T-T_CO2'

def lead_lag(x, y, dimension, lag):
    y_shift = y.shift({dimension:lag})
    corr = xr.corr(x, y_shift)
    return corr

def lead_lag_calc_plot(x, y, xname, yname, **kwargs):
    latmin = kwargs.pop('latmin', 0)
    xmod = x.where(x.lat>=latmin).dropna(dim='lat', how='all')
    ymod = y.where(y.lat>=latmin).dropna(dim='lat', how='all')
    lags=[]
    corrs=[]
    for lag in range(lagmin, lagmax+1):
        corrs.append(lead_lag(xmod, ymod, 'time', lag).values.item())
        lags.append(lag)

    fig, ax = plt.subplots(1, 1, figsize=(8,8))
    ln = plt.plot(lags, corrs)
    plt.xlabel('lag')
    plt.ylabel('correlation')
    plt.title(f'Max correlation {xname} vs {yname} at lag {lags[np.argmax(corrs)]} (+ve is corr with older var2)')
    plt.savefig(f'{path}/Plots/leadlag_{xname}_{yname}_{level}K_my{year}_Ls{Ls_early}-{Ls_late}_{latmin}deg.pdf')

lead_lag_calc_plot(x, y, xname, yname)
lead_lag_calc_plot(x, y, xname, yname, latmin=50)

lead_lag_calc_plot(y, y, yname, yname)
lead_lag_calc_plot(y, y, yname, yname, latmin=50)