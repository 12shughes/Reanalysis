'''
Script to use the EMARS processing functions and create an output netcdf with all EMARS PV data
'''

import n_calculate_PV_EMARS as calc
import glob
import xarray as xr
import numpy as np
import functions as fn
import pdb
import os

datachoice = input('Enter directory code (a - analysis, b - background, c - control, a2 - analysis2): ')
while datachoice not in ['a', 'b', 'c', 'a2']:
    print('Incorrect input')
    datachoice = input('Enter directory code (a - analysis, b - background, c - control, a2 - analysis2): ')

if datachoice == 'a':
    type = 'Analysis/'
elif datachoice == 'b':
    type = 'Background/'
elif datachoice == 'c':
    type = 'Control/'
elif datachoice == 'a2':
    type = 'Analysis2/'

epath = f'/disco/share/sh1293/EMARS_data/{type}Raw/'
if datachoice == 'a2':
    epath = f'/disco/share/sh1293/EMARS_data/{type}Regrid/'

# levels = np.array([200., 250., 275., 300., 310., 320., 330., 340.,
#                     350., 360., 370., 380., 390., 400., 450., 500., 550.,
#                     600., 650., 700., 750., 800., 850., 900., 950.])

levels = np.array([250., 300., 350., 400.])

years = [29]
passcond = True

for year in years:
    print(year)
    print('opening data')
    files = sorted(
        glob.glob(f'{epath}emars*MY{year-1}*360.nc') +
        glob.glob(f'{epath}emars*MY{year}*.nc') +
        glob.glob(f'{epath}emars*MY{year+1}*000*.nc')
    )
    initds = xr.open_mfdataset(files, combine='nested', concat_dim='time')
    initds = initds.astype('float32')
    print('dealing with time')
    times = np.linspace(0,len(initds.time)-1, len(initds.time))
    initds = initds.assign(time=times)
    print('Extracting necessary part of dataset')
    if type == 'Control/':
        initds = initds[['MY', 'Ls', 'time', 't', 'u', 'v', 'ps', 'ak', 'bk', 'lon', 'lat', 'phalf', 'pfull']]
    elif type == 'Analysis/':
        initds = initds[['MY', 'Ls', 'time', 'T', 'U', 'V', 'ps', 'ak', 'bk', 'lon', 'lat', 'phalf', 'pfull']]
    elif type == 'Background/':
        initds = initds[['MY', 'Ls', 'time', 't', 'u', 'v', 'ps', 'ak', 'bk', 'lon', 'lat', 'phalf', 'pfull', 'lheat', 'snow']]

    # pdb.set_trace()
    yeards = initds.where((initds['MY'] == year).compute(), drop = True)
    if datachoice != 'a2':
        nlat = yeards.sizes['lat']
        lats_fixed = np.linspace(87.5, -87.5, nlat)
        yeards = yeards.interp(lat=lats_fixed)
    max = 4
    print('splitting year into %d' %(max))
    for i in np.linspace(1, max, max):
        print(i)
        print('splitting year')
        q0 = yeards.Ls[int((i-1) * len(yeards.Ls)/max)].values
        if i == 1:
            q1 = yeards.Ls[int(i * len(yeards.Ls)/max)].values
            splitds = yeards.where((yeards.Ls<=q1).compute(), drop=True)
        elif i == max:
            splitds = yeards.where((yeards.Ls>q0).compute(), drop=True)
        else:
            q1 = yeards.Ls[int(i * len(yeards.Ls)/max)].values
            splitds = yeards.where((q0<yeards.Ls).compute(), drop=True).where((yeards.Ls<=q1).compute(), drop=True)
        print('prepping ds')
        # pdb.set_trace()
        midds, prs = calc.netcdf_prep_emars(splitds, type)
        splitds.close()
        print('interpolating to isobaric')
        # pdb.set_trace()
        d_isobaric = calc.isobaric_interp(midds, prs)
        midds.close()
        prs.close()
        # pdb.set_trace()
        theta, d_isobaric['PV'] = calc.calculate_PV(d_isobaric)
        print('interpolating to isentropic')
        # pdb.set_trace()
        d_isentropic = calc.interpolate_to_isentropic(d_isobaric, levels = levels).astype('float32')
        d_isentropic['PV_lait'] = fn.lait_scale(d_isentropic)
        #try:
        #    d_isentropic = calc.interpolate_to_isentropic(d_isobaric, levels = levels).astype('float32')
        #except RuntimeError:
        #    print('calculation failed, moving to next segment')
        #    passcond = False
        if passcond:
            print('combining datasets')
            if i ==1:
                t_theta = theta
                t_d_isentropic = d_isentropic
                t_d_isobaric = d_isobaric
            else:
                t_theta = xr.concat([t_theta, theta], dim='time').astype('float32')
                t_d_isobaric = xr.concat([t_d_isobaric, d_isobaric], dim='time').astype('float32')
                t_d_isentropic = xr.concat([t_d_isentropic, d_isentropic], dim='time').astype('float32')
        theta.close()
        d_isobaric.close()
        d_isentropic.close()
    print('saving isobaric')
    if not os.path.exists(f'/disco/share/sh1293/EMARS_data/{type}Isobaric/'):
        os.makedirs(f'/disco/share/sh1293/EMARS_data/{type}Isobaric/')
    t_d_isobaric.to_netcdf(f'/disco/share/sh1293/EMARS_data/{type}Isobaric/isobaric_emars_my{year}.nc')
    print('saving isentropic')
    if not os.path.exists(f'/disco/share/sh1293/EMARS_data/{type}Isentropic/'):
        os.makedirs(f'/disco/share/sh1293/EMARS_data/{type}Isentropic/')
    t_d_isentropic.to_netcdf(f'/disco/share/sh1293/EMARS_data/{type}Isentropic/isentropic_emars_my{year}.nc')
    yeards.close()