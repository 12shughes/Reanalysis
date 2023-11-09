from plevel_fn import plevel_call
import sys
import os
import time
import pdb
import xarray as xr
import subprocess
import numpy as np
import dask
from dask.distributed import Client, progress
from tqdm import tqdm


# not sure what pk stands for, but this seems to save variables with different names - presumably to make the isca process work
def add_pk(nc_file_in_orig, nc_file_pk_sorted, reference_lon, reference_lat, reference_lonb, reference_latb ):
    print(f'sorting pk for {nc_file_in_orig}')
    # open dataset
    dataset = xr.open_dataset(nc_file_in_orig, decode_times=False)
    # save phalf and ak values, assign ak attributes
    dataset['pk'] = ('phalf', dataset['ak'].values)
    dataset['pk'].attrs = dataset['ak'].attrs

    # comparison of old and new lon lat (and lonb and latb) values - need to look into this
    try:
        lonb = dataset['lonb'].values
    except:
        if np.all(dataset['lon'].values == reference_lon):
            dataset.coords['lonb'] = ('lonb', reference_lonb)
        else:
            raise NotImplementedError('new lon and old lon do not match')
        if np.all(dataset['lat'].values == reference_lat):
            dataset.coords['latb'] = ('latb', reference_latb)            
        else:
            raise NotImplementedError('new lat and old lat do not match')            

    # save file
    dataset.to_netcdf(nc_file_pk_sorted) 

# save start time
start_time=time.time()

#base directory for data
base_dir='/disco/share/sh1293/EMARS_data'

#list of experiment names to loop over back data and analysis data
exp_name_list = ['anal', 'back']

# something to do with calling the required plevs and variables - list the different dictionaries of variables to use
avg_or_daily_list=['mars']

# range of martian years required
my_start = 24
my_end = 33

# set Ls range for each file, and hence number of files in a year
delta_ls = 30
nfiles_per_year = int(np.around(360/delta_ls))

# choose which set of pressure levels to use
level_set='standard' 
mask_below_surface_set=' ' #Default is to mask values that lie below the surface pressure when interpolated. For some applications, you want to have values interpolated below ground, i.e. as if the ground wasn't there. To use this option, this value should be set to '-x '. 

# client = Client(threads_per_worker=1, n_workers=1)

# set an output directory if not done already
try:
    out_dir
except:
    out_dir = base_dir

# set empty dictionaries
plevs={}
var_names={}

# raise NotImplementedError('Something fishy is happening in that none of the data seems to be masked out even after interpolation. Is there a units problem or similar?')


# define the standard mars pressure levels, save in the dicionaries. Set file suffix based on if pressure levels go below ground
if level_set=='standard':

    plevs['mars']  =' -p "1 3 6 12 19 30 45 68 99 140 191 250 317 386 454 519 576 625 665 696 721 739 752 761 767" '

    var_names['mars']='-a "MY"'

    if '-x' in mask_below_surface_set:
        file_suffix='_interp'
    else:
        file_suffix='_interp_not_bg'        


# empty lists of files
files_to_adjust = []
files_to_interpolate = []


# open up one file as the reference file, save reference lat, lon, latb, lonb values
reference_file =  xr.open_dataset('/disco/share/sh1293/EMARS_data/emars_v1.0_back_mean_MY27_Ls030-060.nc', decode_times=False)
reference_lon, reference_lat, reference_lonb, reference_latb = reference_file['lon'].values, reference_file['lat'].values, reference_file['lonb'].values, reference_file['latb'].values

# loop over choice of analysis, back data etc.
for exp_name in exp_name_list:
    # loop over the martian years chosen
    for my_val in range(my_start, my_end+1):
        print(f'running MY {my_val}')
        # loop over all the files in a year, and show a progress bar for each year
        for ls_tick in tqdm(range(nfiles_per_year)):


            # loop over all the variables sets required
            for avg_or_daily in avg_or_daily_list:

                # create strings of the file names - the file to be rearranged and where to save it
                nc_file_in_orig = f'{base_dir}/emars_v1.0_{exp_name}_mean_MY{my_val}_Ls{ls_tick*delta_ls:03}-{(ls_tick+1)*delta_ls:03}.nc'
                nc_file_pk_sorted = f'{base_dir}/emars_v1.0_{exp_name}_mean_MY{my_val}_Ls{ls_tick*delta_ls:03}-{(ls_tick+1)*delta_ls:03}_pk.nc'

                # check if the required file exists
                does_file_exist = os.path.isfile(nc_file_in_orig)    
                if does_file_exist:
                    # check it hasn't already been rearranged
                    if not os.path.isfile(nc_file_pk_sorted):
                        # files_to_adjust.append(dask.delayed(add_pk)(nc_file_in_orig, nc_file_pk_sorted))        
                        # do the processing
                        add_pk(nc_file_in_orig, nc_file_pk_sorted, reference_lon, reference_lat, reference_lonb, reference_latb )

                    # create strings of file names for pressure level interpolation
                    nc_file_in = f'{base_dir}/emars_v1.0_{exp_name}_mean_MY{my_val}_Ls{ls_tick*delta_ls:03}-{(ls_tick+1)*delta_ls:03}_pk.nc'
                    nc_file_out = f'{base_dir}/emars_v1.0_{exp_name}_mean_MY{my_val}_Ls{ls_tick*delta_ls:03}-{(ls_tick+1)*delta_ls:03}{file_suffix}.nc'

                    #check it hasn't already been done, and then apply the isca function to process the data
                    if not os.path.isfile(nc_file_out):
                        # files_to_interpolate.append(dask.delayed(plevel_call)(nc_file_in,nc_file_out, var_names = var_names[avg_or_daily], p_levels = plevs[avg_or_daily], mask_below_surface_option=mask_below_surface_set))                        
                        plevel_call(nc_file_in,nc_file_out, var_names = var_names[avg_or_daily], p_levels = plevs[avg_or_daily], mask_below_surface_option=mask_below_surface_set)
                    # else:
                    #     try:
                    #         dataset = xr.open_dataset(nc_file_out, decode_times=False)
                    #     except:
                    #         pdb.set_trace()

# progress(files_to_adjust=dask.compute(*files_to_adjust))
# progress(files_to_interpolate=dask.compute(*files_to_interpolate))

print('execution time', time.time()-start_time)
