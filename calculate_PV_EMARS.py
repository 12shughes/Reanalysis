'''
Calculates PV from EMARS data.
'''

import numpy as np
import xarray as xr
import os, sys
import glob
import analysis_functions as funcs
import PVmodule as PV

def calculate_pfull(psurf, ak, bk):
    r"""Calculates full pressures using surface pressures and sigma coordinates

    psurf  : array-like
            Surface pressures
    siglev : array-like
            Sigma-levels
    """

    p_i = psurf*bk + ak

    p = xr.zeros_like(ak)
    p[k] = (p_i[k+1]-p_i[k])/np.log(p_i[k+1]/p_i[k])
    return p

if __name__ == "__main__":
    ### choose your desired isobaric levels, in Pascals
    plev1 = [float(i/10) for i in range(1,100,5)]
    plev2 = [float(i) for i in range(10,100,10)]
    plev3 = [float(i) for i in range(100,650,50)]
    
    ### choose desired isentropic levels, in Kelvins
    thetalevs=[200., 250., 300., 350., 400., 450., 500., 550., 600., 650., 700., 750., 800., 850., 900., 950.]
    
    save_PV_isobaric=True
    save_PV_isentropic=True
    interpolate_isentropic=True
    
    Lsmin = 255
    Lsmax = 285
    
    theta0 = 200.
    kappa = 1/4.0
    p0 = 610.
    
    inpath = '/disco/share/sh1293/EMARS_data/'
    #infiles = os.listdir(inpath)
    home = os.getenv("HOME")
    os.chdir(inpath)
    infiles = glob.glob('emars*0.nc')
    for f in infiles:
        print(f)
    os.chdir(home)
    isenpath = inpath
    isopath = inpath
    #inpath = ''
    #outpath = 'MACDA_data/'
    #figpath = 'OpenMARS_figs/'
    
    plevs = plev1+plev2+plev3
    
    for f in infiles:
        d = xr.open_mfdataset(inpath+f, decode_times=False, concat_dim='time',
                               combine='nested',chunks={'time':'auto'})
    
        ens_list = []
        #tmp1 = ds.sel(lon=-180.)
        #tmp1 = tmp1.assign_coords({'lon':179.9999})
        #ens_list.append(ds)
        #ens_list.append(tmp1)
        #d = xr.concat(ens_list, dim='lon')
    
        d = d.astype('float32')
        d = d[['Ls','MY','ps','T','U','V','ak','bk']]
        d = d.rename_vars({'T':'temp','U':'u','V':'v'})
    
#need to adjust this to give the EMARS version
        #print(d)
        prs = calculate_pfull(d.ps, d.ak, d.bk).dropna('phalf')
        prsset = prs.to_dataset(name = 'prs')
        prsset = prsset.assign_coords({'pfull':d.pfull})
        prsset['prs'] = prsset['prs'].swap_dims({'phalf':'pfull'})
        prsset = prsset.drop_dims('phalf')
        #prs = d.drop('Surface_geopotential')
        #prs = prs.reset_coords('variables', drop = True)
        #prs = prs.to_array()
        #prs = prs['pfull']
        #prs = d.pfull
        #print(np.shape(prs))
        prs = prsset.prs
        print(prs)
        prs = prs.transpose('time','pfull','lat','lon')
        #prs = prs.reset_coords('variables', drop = True)
    
        temp = d[["temp"]].to_array().squeeze()
        uwind = d[["u"]].to_array().squeeze()
        vwind = d[["v"]].to_array().squeeze()
    
        print('Calculating potential temperature...')
        thta = PV.potential_temperature(d.temp, d.pfull,
                                             kappa = kappa, p0 = p0)
    
        print('Interpolating variables onto isobaric levels...')
        print('dims of xp')
        print(np.shape(prs.compute()))
        print('dims of var')
        print(np.shape(temp))
        tmp, uwnd, vwnd, theta = PV.log_interpolate_1d(plevs, prs.compute(),
                                                        temp, uwind, vwind, thta,
                                                        axis = 1)
    
        d_iso = xr.Dataset({"tmp"  : (("time", "plev", "lat", "lon"), tmp),
                            "uwnd" : (("time", "plev", "lat", "lon"), uwnd),
                            "vwnd" : (("time", "plev", "lat", "lon"), vwnd),
                            "theta": (("time", "plev", "lat", "lon"), theta)},
                            coords = {"time": d.time,
                                      "plev": plevs,
                                      "lat" : d.lat,
                                      "lon" : d.lon})
    
    
        uwnd_trans = d_iso.uwnd.transpose('lat','lon','plev','time')
        vwnd_trans = d_iso.vwnd.transpose('lat','lon','plev','time')
        tmp_trans = d_iso.tmp.transpose('lat','lon','plev','time')
    
        print('Calculating potential vorticity on isobaric levels...')
        PV_iso = PV.potential_vorticity_baroclinic(uwnd_trans, vwnd_trans,
                      d_iso.theta, 'plev', omega = omega, g = g, rsphere = rsphere)
        PV_iso = PV_iso.transpose('time','plev','lat','lon')
    
        d_iso["PV"] = PV_iso
    
        if save_PV_isobaric == True:
            print('Saving PV on isobaric levels to '+isopath)
            d_iso["Ls"]=d.Ls
            d_iso["MY"]=d.MY
            path = isopath+'isobaric_'+f
            d_iso.to_netcdf(path)
    
        isentlevs = np.array(thetalevs)
    
        if interpolate_isentropic==True:
            print('Interpolating variables onto isentropic levels...')
            
            isent_prs, isent_PV, isent_u, isent_tmp = PV.isent_interp(isentlevs, d_iso.plev,
                                                            d_iso.tmp, PV_iso, d_iso.uwnd,
                                                            axis = 1,temperature_out=True)
    
            d_isent = xr.Dataset({"prs" : (("time","ilev","lat","lon"), isent_prs),
                                  "PV"  : (("time","ilev","lat","lon"), isent_PV),
                                  "uwnd": (("time","ilev","lat","lon"), isent_u),
                                  "tmp" : (("time","ilev","lat","lon"), isent_tmp)},
                                  coords = {"time": d_iso.time,
                                            "ilev": isentlevs,
                                            "lat" : d_iso.lat,
                                            "lon" : d_iso.lon})
    
        if save_PV_isentropic == True:
            print('Saving PV on isentropic levels to '+isenpath)
            d_isent["Ls"]=d.Ls
            d_isent["MY"]=d.MY
            d_isent.to_netcdf(isenpath+'isentropic_'+f)
    
