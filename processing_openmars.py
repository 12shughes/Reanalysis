'''
Script to use the OpenMARS processing functions and create an output netcdf with all OpenMARS PV data
'''

import n_calculate_PV_OpenMARS as calc
import glob
import xarray as xr
import numpy as np
import os
import functions as fn
import pdb

opath = '/disco/share/sh1293/OpenMARS_data/Raw/'
print('opening data')
initds = xr.open_mfdataset(opath + 'openmars*.nc').astype('float32')
# pdb.set_trace()

levels = np.array([200., 225., 250., 275., 300., 310., 320., 330., 340.,
                    350., 360., 370., 380., 390., 400., 450., 500., 550.,
                    600., 650., 700., 750., 800., 850., 900., 950.])

print('splitting by year')
years = np.sort(np.unique(initds.MY))
initds.close()
# years = [32]

for year in years:
    year = int(year)
    print('opening data')
    initds = xr.open_mfdataset(f'{opath}openmars*my{year}*.nc').astype('float32')
    passcond = True
    print(year)
    yeards = initds.where((initds['MY'] == year).compute(), drop = True)
    initds.close()
    # pdb.set_trace()
    max = 8
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
        # pdb.set_trace()
        yeards.close()
        print('prepping ds')
        midds, prs = calc.netcdf_prep(splitds)
        splitds.close()
        # pdb.set_trace()
        print('interpolating to isobaric')
        d_isobaric = calc.isobaric_interp(midds, prs)
        midds.close()
        prs.close()
        # pdb.set_trace()
        theta, d_isobaric['PV'] = calc.calculate_PV(d_isobaric)
        print('interpolating to isentropic')
        d_isentropic = calc.interpolate_to_isentropic(d_isobaric, levels = levels).astype('float32')
        d_isentropic['PV_lait'] = fn.lait_scale(d_isentropic)
        # pdb.set_trace()
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
        if not passcond:
            print('saving datasets')
            d_isobaric.to_netcdf(f'/disco/share/sh1293/OpenMARS_data/Isobaric/MY{year}/isobaric_openmars_my{year}_{int(i)}.nc')
            d_isentropic.to_netcdf(f'/disco/share/sh1293/OpenMARS_data/Isentropic/MY{year}/isentropic_openmars_my{year}_{int(i)}.nc')
        # pdb.set_trace()
        theta.close()
        d_isobaric.close()
        d_isentropic.close()
        # pdb.set_trace()
    if passcond:
        print('saving isobaric')
        t_d_isobaric.to_netcdf('/disco/share/sh1293/OpenMARS_data/Isobaric/isobaric_openmars_my%.0f.nc' %(year))
        print('saving isentropic')
        t_d_isentropic.to_netcdf('/disco/share/sh1293/OpenMARS_data/Isentropic/isentropic_openmars_my%.0f.nc' %(year))
    yeards.close()


# for year in years:
#     print(year)
#     splitds = initds.where((initds['MY'] == year).compute(), drop = True)
#     # pdb.set_trace()
#     print('prepping ds')
#     midds, prs = calc.netcdf_prep(splitds)
#     # # pdb.set_trace()
#     splitds.close()
#     # # pdb.set_trace()
#     print('interpolating to isobaric')
#     d_isobaric = calc.isobaric_interp(midds, prs).astype('float32')
#     midds.close()
#     prs.close()
#     theta, d_isobaric['PV'] = calc.calculate_PV(d_isobaric)
#     d_isobaric = d_isobaric.astype('float32')
#     print('saving isobaric')
#     d_isobaric.to_netcdf('/disco/share/sh1293/OpenMARS_data/Isobaric/isobaric_openmars_my%.0f.nc' %(year))
#     print('interpolating to isentropic')
#     d_isentropic = calc.interpolate_to_isentropic(d_isobaric, levels = levels).astype('float32')
#     print('closing isobaric')
#     d_isobaric.close()
#     print('lait scaling')
#     d_isentropic['PV_lait'] = fn.lait_scale(d_isentropic).astype('float32')
#     print('saving isentropic')
#     d_isentropic.to_netcdf('/disco/share/sh1293/OpenMARS_data/Isentropic/isentropic_openmars_my%.0f.nc' %(year))
#     d_isentropic.close()