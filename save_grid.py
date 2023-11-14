import xarray as xr
import glob
import os
ompath = '/disco/share/sh1293/OpenMars_data/openmars_my28_ls109_my28_ls124.nc'
empath = '/disco/share/sh1293/EMARS_data/'
ds = xr.open_dataset(ompath)
lats = ds['lat'].values.flatten()
lons = ds['lon'].values.flatten()
#with open('/disco/share/sh1293/OpenMars_data/gridfile.txt', 'w') as f:
#    f.write('# lon lat\n')
#    for lon, lat in zip(lons, lats):
#        f.write(f'{lon} {lat}\n')
home = os.getenv("HOME")
os.chdir(empath + 'Raw/')
infiles = glob.glob('emars*.nc')
os.chdir(home)
for infile in infiles:
    ds = xr.open_dataset(empath + 'Raw/' + infile)
    outfile = ds.interp(lat=lats, lon=lons)
    outfile.to_netcdf(empath + 'Regrid/' + infile)