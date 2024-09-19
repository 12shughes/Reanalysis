import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

# change both directory and name
directory = 'EMARS_data/Analysis'
name = 'emars'
year = 25
# pressure in Pa
# pressure = 70   

for pressure in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]:
    root_path = '/disco/share/sh1293'
    path = f'{root_path}/{directory}/Isobaric'
    ds = xr.open_dataset(f'{path}/isobaric_{name}_my{year}.nc')
    ds_p = ds.loc[dict(pfull=pressure)]
    min_T = float(np.min(ds_p.temp).values)
    ds_min_T = ds_p.temp.where(ds_p.temp==min_T)
    count_min_T = float(ds_min_T.count())

    fig, axs = plt.subplots(1, 1, figsize=(8,8))
    hist = ds_p.temp.plot.hist(ax=axs, bins=np.arange(np.min(ds_p.temp), np.max(ds_p.temp), 1))
    count, bins = np.histogram(ds_p.temp, bins=np.arange(np.min(ds_p.temp), np.max(ds_p.temp), 1))
    line = plt.plot([149.2+6.48*np.log(0.00135*pressure)]*2, [0, np.max(count)], '--', color='red')
    plt.title(f'At pressure {pressure}Pa \n Min T is {min_T:.4f}, Emily T is {149.2+6.48*np.log(0.00135*pressure):.4f}')
    plt.savefig(f'{path}/hist_p--{pressure}Pa_my{year}.pdf')