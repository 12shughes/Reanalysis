import xarray as xr
import glob
import os
ompath = '/disco/share/sh1293/OpenMars_data/openmars_my28_ls109_my28_ls124.nc'
empath = '/disco/share/sh1293/EMARS_data/'
d = xr.open_dataset(ompath)
lats = d['lat'].values.flatten()
lons = d['lon'].values.flatten()
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
    ds = ds.assign_coords(lon=(((ds.lon + 180) % 360) - 180)).sortby('lon')
    ds = ds.assign_coords(lonv=(((ds.lonv + 180) % 360) - 180)).sortby('lonv')
    outfile = ds.interp(lon=lons, lonv = lons, wrap=True)
    outfile = outfile.interp(lat=lats, latu=lats)
    #outfile = outfile.transpose('time', 'lat', 'lon', 'ilev', 'latu', 'lonv')
    outfile.to_netcdf(empath + 'Regrid/' + infile)