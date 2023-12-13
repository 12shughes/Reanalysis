import xarray as xr
path = '/disco/share/sh1293/OpenMARS_data/Raw/openmars_my28_ls109_my28_ls124.nc'
ds = xr.open_dataset(path)
lats = ds['lat'].values.flatten()
lons = ds['lon'].values.flatten()
with open('/disco/share/sh1293/OpenMARS_data/gridfile.txt', 'w') as f:
    f.write('# lon lat\n')
    for lon, lat in zip(lons, lats):
        f.write(f'{lon} {lat}\n')
