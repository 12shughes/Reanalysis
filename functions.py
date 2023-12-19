import xarray as xr
import numpy as np


def lait_scale(q, **kwargs):
    '''
    Lait-scale the PV in datarray q
    '''
    theta0 = kwargs.pop('theta0', 200)
    kappa = kwargs.pop('kappa', 1/4.)

    scaled = q * (q.level / theta0)**(-(1+1/kappa))
    return scaled


def eddy_enstrophy(q, **kwargs):
    '''
    Calculate the eddy enstrophy from dataarray q
    '''
    latmin = kwargs.pop('latmin', 60)

    q = q.where(q.lat >= latmin, drop = True)
    q = q.where(q.lon < 179.5, drop = True)
    qbar = q.mean(dim = 'lon')
    qbar = qbar.expand_dims({'lon':q.lon})

    qprime = q - qbar

    cos = np.cos(np.deg2rad(q.lat))

    qp = qprime **2 * cos

    Z = qp.sum(dim = 'lat').sum(dim = 'lon') / (cos.sum(dim = 'lat') * 2 * np.pi)
    
    return Z


def scaled_eddy_enstrophy(q, **kwargs):
    '''
    Calculate the eddy enstrophy from dataarray q
    '''
    latmin = kwargs.pop('latmin', 60)

    q = q.where(q.lat >= latmin, drop = True)
    q = q.where(q.lon < 179.5, drop = True)
    qbar = q.mean(dim = 'lon')
    qbar = qbar.expand_dims({'lon':q.lon})

    qprime = (q - qbar) / qbar

    cos = np.cos(np.deg2rad(q.lat))

    qp = qprime **2 * cos

    Z = qp.sum(dim = 'lat').sum(dim = 'lon') / (cos.sum(dim = 'lat') * 2 * np.pi)
    
    return Z