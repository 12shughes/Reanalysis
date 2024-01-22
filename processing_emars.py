'''
Script to use the EMARS processing functions and create an output netcdf with all EMARS PV data
'''

import n_calculate_PV_EMARS as calc
import glob
import xarray as xr
import numpy as np

for type in ['Control/', 'Analysis/']:
    print(type)

    epath = '/disco/share/sh1293/EMARS_data/' + type + 'Regrid/'
    print('opening data')
    initds = xr.open_mfdataset(epath + 'emars*.nc', combine='nested', concat_dim='time')
    initds = initds.astype('float32')
    print('dealing with time')
    times = np.linspace(0,len(initds.time)-1, len(initds.time))
    initds = initds.assign(time=times)
    print('Extracting necessary part of dataset')
    if type == 'Control/':
        initds = initds[['MY', 'Ls', 'time', 't', 'u', 'v', 'ps', 'ak', 'bk', 'lon', 'lat', 'phalf', 'pfull']]
    elif type == 'Analysis/':
        initds = initds[['MY', 'Ls', 'time', 'T', 'U', 'V', 'ps', 'ak', 'bk', 'lon', 'lat', 'phalf', 'pfull']]

    #levels = np.array([200., 225., 250., 275., 300., 310., 320., 330., 340.,
    #                    350., 360., 370., 380., 390., 400., 450., 500., 550.,
    #                    600., 650., 700., 750., 800., 850., 900., 950.])
    #levels = np.array([310.])
    levels = np.array([200., 250., 275., 300., 310., 320., 330., 340.,
                        350., 360., 370., 380., 390., 400., 450., 500., 550.,
                        600., 650., 700., 750., 800., 850., 900., 950.])

    print('splitting by year')
    years = np.sort(np.unique(initds.MY))
    #years = [25]
    print(years)
    for year in years:
        passcond = True
        print(year)
        yeards = initds.where((initds['MY'] == year).compute(), drop = True)
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
            print('prepping ds')
            midds, prs = calc.netcdf_prep(splitds, type)
            print('interpolating to isobaric')
            d_isobaric = calc.isobaric_interp(midds, prs)
            theta, d_isobaric['PV'] = calc.calculate_PV(d_isobaric)
            print('interpolating to isentropic')
            d_isentropic = calc.interpolate_to_isentropic(d_isobaric, levels = levels).astype('float32')
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
        print('saving isobaric')
        t_d_isobaric.to_netcdf('/disco/share/sh1293/EMARS_data/%sIsobaric/isobaric_emars_my%.0f.nc' %(type, year))
        print('saving isentropic')
        t_d_isentropic.to_netcdf('/disco/share/sh1293/EMARS_data/%sIsentropic/isentropic_emars_my%.0f.nc' %(type, year))
#        q1 = yeards.Ls[int(len(yeards.Ls)/4)].values
#        q3 = yeards.Ls[int(3 * len(yeards.Ls)/4)].values
#        q2 = yeards.Ls[int(2 * len(yeards.Ls)/4)].values
#        splitds1 = yeards.where((yeards.Ls<=q1).compute(), drop=True)
#        splitds2 = yeards.where((q1<yeards.Ls).compute(), drop=True).where((yeards.Ls<=q2).compute(), drop=True)
#        splitds3 = yeards.where((q2<yeards.Ls).compute(), drop=True).where((yeards.Ls<=q3).compute(), drop=True)
#        splitds4 = yeards.where((yeards.Ls>q3).compute(), drop=True)
#        print('prepping ds')
#        midds1, prs1 = calc.netcdf_prep(splitds1, type)
#        midds2, prs2 = calc.netcdf_prep(splitds2, type)
#        midds3, prs3 = calc.netcdf_prep(splitds3, type)
#        midds4, prs4 = calc.netcdf_prep(splitds4, type)
#        print('interpolating to isobaric')
#        d_isobaric1 = calc.isobaric_interp(midds1, prs1)
#        d_isobaric2 = calc.isobaric_interp(midds2, prs2)
#        d_isobaric3 = calc.isobaric_interp(midds3, prs3)
#        d_isobaric4 = calc.isobaric_interp(midds4, prs4)
#        print('First quarter of year')
#        theta1, d_isobaric1['PV'] = calc.calculate_PV(d_isobaric1)
#        print('interpolating to isentropic')
#        d_isentropic1 = calc.interpolate_to_isentropic(d_isobaric1, levels = levels).astype('float32')
#        print('Second quarter of year')
#        theta2, d_isobaric2['PV'] = calc.calculate_PV(d_isobaric2)
#        print('interpolating to isentropic')
#        d_isentropic2 = calc.interpolate_to_isentropic(d_isobaric2, levels = levels).astype('float32')
#        print('Third quarter of year')
#        theta3, d_isobaric3['PV'] = calc.calculate_PV(d_isobaric3)
#        print('interpolating to isentropic')
#        d_isentropic3 = calc.interpolate_to_isentropic(d_isobaric3, levels = levels).astype('float32')
#        print('Fourth quarter of year')
#        theta4, d_isobaric4['PV'] = calc.calculate_PV(d_isobaric4)
#        print('interpolating to isentropic')
#        print('Combining data')
#        theta = xr.concat([theta1, theta2, theta3, theta4], dim='time').astype('float32')
#        d_isentropic4 = calc.interpolate_to_isentropic(d_isobaric4, levels = levels).astype('float32')
#        d_isobaric = xr.concat([d_isobaric1, d_isobaric2, d_isobaric3, d_isobaric4], dim='time').astype('float32')
#        d_isentropic = xr.concat([d_isentropic1, d_isentropic2, d_isentropic3, d_isentropic4], dim='time').astype('float32')
#        print('saving isobaric')
#        d_isobaric.to_netcdf('/disco/share/sh1293/EMARS_data/%sIsobaric/isobaric_emars_my%.0f.nc' %(type, year))
#        print('saving isentropic')
#        d_isentropic.to_netcdf('/disco/share/sh1293/EMARS_data/%sIsentropic/isentropic_emars_my%.0f.nc' %(type, year))
