import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

directory = 'OpenMARS_data'
name = 'openmars'
year = 29
Ls_early = 270
Ls_late = 300
level = 200
lat = 77.5
thresh = 1

latint, latdec = [int(part) for part in str(lat).split('.')]
root_path = '/disco/share/sh1293'
path = f'{root_path}/{directory}/Isentropic'
ds = xr.open_dataset(f'{path}/isentropic_{name}_my{year}.nc').astype('float32')
dss = ds

ds = ds.sel(lat=lat, method='nearest')
ds = ds.sel(level=level)
ds = ds.reset_coords('lat', drop=True).reset_coords('level', drop=True)
ds['Ls'] = ds.Ls.mean(dim='lon', skipna=True)
ds = ds.where(ds.Ls>=Ls_early).where(ds.Ls<=Ls_late).dropna(dim='time')
ds['T_c'] = 149.2+6.49*np.log(0.00135*ds.pressure*100).astype('float32')
ds['cond_loc'] = xr.where(ds.temp <= ds.T_c+thresh, 1, np.nan)

ti = ds.time[0]
tf = ds.time[-1]
# tick_ls = [240, 270, 300]
tick_ls = [270, 285, 300]
tick_time = [(tick_ls[0]-Ls_early)/(Ls_late-Ls_early)*(tf-ti)+ti,
            (tick_ls[1]-Ls_early)/(Ls_late-Ls_early)*(tf-ti)+ti,
            (tick_ls[2]-Ls_early)/(Ls_late-Ls_early)*(tf-ti)+ti]

fig, ax = plt.subplots(1, 1, figsize=(8,8))
cf = ds.PV.plot.contourf(ax=ax,  x='lon', y='time', cmap='OrRd', levels=21)
# cf1 = ds.cond_loc.plot.contourf(ax=ax, x='lon', y='time', colors='none', levels=[0, 1.5], hatches='xx')
ds['cond_loc_fill'] = ds.cond_loc.fillna(0)
cf1 = ds.cond_loc_fill.plot.contour(ax=ax, x='lon', y='time', levels=[0.5], colors='black', linewidths=1)
cf2 = ds.cond_loc.plot.contourf(ax=ax, x='lon', y='time', colors='black', levels=[0, 1.5], alpha=0.2, add_colorbar=False)
# for contour in cf1.get_paths():
#     # Get the vertices of the path (contour line)
#     vertices = contour.vertices
    
#     # Add lines pointing towards the region of values less than 0
#     for i in range(0, len(vertices), 1):  # Adjust step for density of lines
#         x, y = vertices[i]

#         # Calculate the direction towards lower values
#         if i + 1 < len(vertices):
#             dx = x - vertices[i+1][0]
#             dy = y - vertices[i+1][1]
#         else:
#             dx = vertices[i-1][0] - x
#             dy = vertices[i-1][1] - y
        
#         # Normalize the direction vector
#         norm = np.hypot(dx, dy)
#         dx /= norm
#         dy /= norm

#         # Length of the line pointing towards lower values
#         line_length = 0.5

#         # Draw the line
#         plt.plot([x, x - dx * line_length], [y, y - dy * line_length], color='black')
ax.set_yticks(tick_time, tick_ls)
plt.savefig(f'{path}/Plots/hovmoller_condloc_{level}K_my{year}_Ls{Ls_early}-{Ls_late}_{latint}-{latdec}deg_thresh-{thresh}K.pdf')

