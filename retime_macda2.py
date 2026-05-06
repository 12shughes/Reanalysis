import numpy as np
import xarray as xr
import glob
import pdb

path = '/disco/share/sh1293/MACDA2_data/Raw/*.nc'
savepath = '/disco/share/sh1293/MACDA2_data/Raw_time'

files = glob.glob(path)
for file in files:
    ds = xr.open_dataset(file, decode_times=False)
    if len(file)==52:
        part1 = int(file[-12:-8])
        year = int(24+part1/669)
    elif len(file)==51:
        part1 = int(file[-11:-8])
        year = int(24+part1/669)
    elif len(file)==50:
        part1 = int(file[-10:-7])
        year = int(24+part1/669)
    print(part1)
    # pdb.set_trace()
    ds['MY'] = year
    ds['time'] = ds.time+part1
    ds['time'] = ds.time.assign_attrs(units='Sol', long_name='sol since start of MY24')
    name = file[36:]
    ds.to_netcdf(f'{savepath}/{name}')
    ds.close()