
#%%
import xarray as xr
import numpy as np
import os, sys

sys.path.append('../')
import atmospy
import pot_vort

from multiprocessing import Pool, cpu_count
import windspharm.xarray as windx


def calculate_pfull(psurf, ak, bk):
    r"""Calculates full pressures using surface pressures and sigma coordinates

    psurf  : array-like
            Surface pressures
    siglev : array-like
            Sigma-levels
    """

    ph = psurf * bk + ak
    ps = ph.shift(phalf = -1)
    pf = (ps-ph)/np.log(ps/ph)

    return pf


def netcdf_prep(ds, type):
    '''
    Appends longitude 360 to file and reduces file to only variables necessary
    for PV calculation. Also converts pressure to Pa.
    '''
    ens_list = []
    tmp1 = ds.sel(lon=-180.)
    tmp1 = tmp1.assign_coords({'lon':179.9999})
    ens_list.append(ds)
    ens_list.append(tmp1)

    d = xr.concat(ens_list, dim='lon')
    d = d.astype('float32')
    
    # pressure is in hPa, must be in Pa for calculations - need to do this for EMARS as pressure (pfull) is in mb
    d["pfull"] = d.pfull*100

    if type == 'Control/':
        d = d.rename_vars({'t':'temp'})
    elif type == 'Analysis/':
        d = d.rename_vars({'T':'temp','U':'u','V':'v'})


    prs = calculate_pfull(d.ps, d.ak, d.bk).dropna('phalf')
    prsset = prs.to_dataset(name = 'prs')
    prsset = prsset.assign_coords({'pfull':d.pfull})
    prsset['prs'] = prsset['prs'].swap_dims({'phalf':'pfull'})
    prsset = prsset.drop_dims('phalf')
    prs = prsset.prs
    prs = prs.transpose('time','pfull','lat','lon')


    d = d[['Ls','MY','ps','temp','u','v']]

    return d, prs


def isobaric_interp(ds, prs):
    '''
    Takes the prepped netCDF4 and interps it to isobaric levels
    '''
    plev1 = [float(i/10) for i in range(1,100,5)]
    plev2 = [float(i) for i in range(10,100,10)]
    plev3 = [float(i) for i in range(100,650,50)]
    plevs = plev1+plev2+plev3

    tmp, uwnd, vwnd = pot_vort.log_interpolate_1d(plevs, prs.compute(),
                                                    ds.temp, ds.u, ds.v,
                                                    axis = 1)
    d_iso = xr.Dataset({"temp"  : (("time", "pfull", "lat", "lon"), tmp), 
                        "ucomp" : (("time", "pfull", "lat", "lon"), uwnd),
                        "vcomp" : (("time", "pfull", "lat", "lon"), vwnd),},
                        coords = {"time": ds.time,
                                "pfull": plevs,
                                "lat" : ds.lat,
                                "lon" : ds.lon})
    d_iso['Ls'] = ds.Ls
    d_iso.transpose('lat','lon','pfull','time')
    d_iso.sortby('lat', ascending=False)
    return d_iso

def calculate_PV(d, **kwargs):
    if d.pfull.max().values < 10:
        raise ValueError('Just double check your pressure is in Pascals here!')
    if d.pfull.max().values > 1000000:
        raise ValueError('Just double check your pressure is in Pascals here!')
    if d.pfull.max().values > 800 and d.pfull.max().values < 1200:
        raise ValueError('Just double check your pressure is in Pascals here!')

    theta0  = kwargs.pop( 'theta0', 200.)        # reference temperature
    kappa   = kwargs.pop(  'kappa', 0.25)        # ratio of specific heats
    p0      = kwargs.pop(     'p0', 610.)        # reference pressure
    omega   = kwargs.pop(  'omega', 7.08822e-05) # planetary rotation rate
    g       = kwargs.pop(      'g', 3.72076)     # gravitational acceleration
    rsphere = kwargs.pop('rsphere', 3.3962e6)    # mean planetary radius
    dim     = kwargs.pop(    'dim', 'pfull')

    print('calculating theta')
    theta = pot_vort.potential_temperature(
        d.pfull, d.temp, kappa=kappa, p0=p0,
    )

    print('calculating PV')
    PV_isobaric = pot_vort.potential_vorticity_baroclinic(
        d.ucomp, d.vcomp, theta, dim, omega=omega, g=g, rsphere=rsphere,
    )
    return theta, PV_isobaric

def interpolate_to_isentropic(d, **kwargs):

    theta0  = kwargs.pop( 'theta0', 200.)        # reference temperature
    kappa   = kwargs.pop(  'kappa', 0.25)        # ratio of specific heats
    p0      = kwargs.pop(     'p0', 610.)        # reference pressure
    omega   = kwargs.pop(  'omega', 7.08822e-05) # planetary rotation rate
    g       = kwargs.pop(      'g', 3.72076)     # gravitational acceleration
    rsphere = kwargs.pop('rsphere', 3.3962e6)    # mean planetary radius
    dim     = kwargs.pop(    'dim', 'pfull')

    if d.pfull.max().values < 10:
        raise ValueError('Just double check your pressure is in Pascals here!')
    if d.pfull.max().values > 1000000:
        raise ValueError('Just double check your pressure is in Pascals here!')
    if d.pfull.max().values > 800 and d.pfull.max().values < 1200:
        raise ValueError('Just double check your pressure is in Pascals here!')
    thetalevs = np.array(kwargs.pop('levels',
        [200., 225., 250., 275., 300., 310., 320., 330., 340.,
         350., 360., 370., 380., 390., 400., 425., 450., 475.,
         500., 525., 550., 575., 600., 625., 650., 675., 700.,
         725., 750., 775., 800., 850., 900., 950.]
        ))
    if kappa == 0.25:
        d = d.transpose('time', 'pfull', 'lat', 'lon')

        pres, PV_i, u_i, v_i, \
         = pot_vort.isent_interp(
            thetalevs, d.pfull, d.temp, d.PV,
            d.ucomp, d.vcomp,
            axis = 1)

        d_isentropic = xr.Dataset({
            "pressure"             : (("time","level","lat","lon"), pres/100),
            "PV"                   : (("time","level","lat","lon"), PV_i),
            #"grdSpv"               : (("time","level","lat","lon"), grdSpv_i),
            "ucomp"                : (("time","level","lat","lon"), u_i),
            "vcomp"                : (("time","level","lat","lon"), v_i),
            #"Ls"                   : (("time"), d.Ls),
            #"omega"                : (("time","level","lat","lon"), omega_i),
            #"test_tracer"          : (("time","level","lat","lon"), tracer_i),
            #"grdStr"               : (("time","level","lat","lon"), grd_tr_i),
            #"lh_rel"               : (("time","level","lat","lon"), lh_rel_i),
            #"dt_tg_lh_condensation": (("time","level","lat","lon"), dt_tg_lh_condensation_i),
            },
            coords = {
                "level": thetalevs,
                "time" : d.time,
                "lat"  : d.lat,
                "lon"  : d.lon
                })
        d_isentropic['Ls'] = d.Ls
    else: ## just simple way to choose between earth and mars for now
        d = d.transpose('pfull', 'latitude', 'longitude')

        pres, PV_i, grdSpv_i, u_i, v_i = atmospy.isent_interp(
            thetalevs, d.pfull, d.temp, d.PV,
            d.grdSpv, d.ucomp,
            d.vcomp, axis = 0, p0=p0, kappa=kappa)

        d_isentropic = xr.Dataset({
            "pressure"             : (("level","latitude","longitude"), pres),
            "PV"                   : (("level","latitude","longitude"), PV_i),
            "grdSpv"               : (("level","latitude","longitude"), grdSpv_i),
            "ucomp"                : (("level","latitude","longitude"), u_i),
            "vcomp"                : (("level","latitude","longitude"), v_i),
            },
            coords = {
                "level"     : thetalevs,
                "latitude"  : d.latitude,
                "longitude" : d.longitude,
                })

    
    
    
    return d_isentropic

# %%
