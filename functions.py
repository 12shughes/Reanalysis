import xarray as xr
import numpy as np
import matplotlib.pyplot as plt


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


def scaled2_eddy_enstrophy(q, **kwargs):
    '''
    Calculate the eddy enstrophy from dataarray q
    '''
    latmin = kwargs.pop('latmin', 60)

    q = q.where(q.lat >= latmin, drop = True)
    q = q.where(q.lon < 179.5, drop = True)
    qbar = q.mean(dim = 'lon')
    qbar = qbar.expand_dims({'lon':q.lon})

    qprime = (q - qbar)

    cos = np.cos(np.deg2rad(q.lat))

    qp = qprime **2 * cos

    Z = qp.sum(dim = 'lat').sum(dim = 'lon') / (cos.sum(dim = 'lat') * 2 * np.pi * q.mean(dim='lon').mean(dim='lat')**2)
    
    return Z


def eddy_enstrophy_contourf_plot(path, years, **kwargs):
    scaled = kwargs.pop('scaled', 'no')
    Lsmin = kwargs.pop('Lsmin', 200)
    Lsmax = kwargs.pop('Lsmax', 340)
    i = 0
    fig, axs = plt.subplots(len(years),1, figsize = (15,18/8*len(years)), layout = 'constrained')
    fig.suptitle('Eddy enstrophy at varying isentropic levels', fontsize = 16)
    for year in years:
        if scaled == 'yes':
            da = xr.open_dataarray(path + 'scaled_lev000_my%02d.nc' %(year))
            vmin = 0
            vmax = 200
        elif scaled == 'yes2':
            da = xr.open_dataarray(path + 'scaled2_lev000_my%02d.nc' %(year))
            vmin = 0
            vmax = 12
        elif scaled == 'no':
            da = xr.open_dataarray(path + 'lev000_my%02d.nc' %(year))
            vmin = 0
            vmax = 200
        da = da.assign_coords({'MY':year})
        daw = da.where(Lsmin <= da.Ls, drop = True).where(da.Ls <= Lsmax, drop = True)
        plot = daw.plot.contourf(x='Ls', levels = 21, vmin = vmin, vmax = vmax, ax = axs[i], add_colorbar=False)
        axs[i].set_xlabel('Ls')
        axs[i].set_ylabel('Isentropic level')
        axs[i].set_title('My%02d' %(year))
        axs[i].invert_yaxis()
        i+=1
    cax = axs[-1].inset_axes([0.2, -0.6, 0.6, 0.2])
    cbar = fig.colorbar(plot, cax=cax, orientation='horizontal')
    #cbar = fig.colorbar(plot, ax=axs[:], orientation='horizontal', shrink = 0.3, location = 'bottom')
    if scaled == 'yes':
        cbar.set_label('Scaled eddy enstrophy')
        plt.savefig(path + '/Plots/scaled_isen_all_Ls%03d-%03d.pdf' %(Lsmin, Lsmax))
    elif scaled == 'yes2':
        cbar.set_label('Scaled2 eddy enstrophy')
        plt.savefig(path + '/Plots/scaled2_isen_all_Ls%03d-%03d.pdf' %(Lsmin, Lsmax))
    elif scaled == 'no':
        cbar.set_label('Eddy enstrophy')
        plt.savefig(path + '/Plots/isen_all_Ls%03d-%03d.pdf' %(Lsmin, Lsmax))


def eddy_enstrophy_climatology_plot(path, years, **kwargs):
    scaled = kwargs.pop('scaled', 'no')
    Lsmin = kwargs.pop('Lsmin', 200)
    Lsmax = kwargs.pop('Lsmax', 340)
    if scaled == 'yes2exc':
        years = [29, 30, 31, 32, 33, 35]
    i = 0
    for year in years:
        if scaled == 'yes':
            da = xr.open_dataarray(path + 'scaled_lev000_my%02d.nc' %(year))
            top = 93
            bottom = -23
        elif scaled == 'yes2':
            da = xr.open_dataarray(path + 'scaled2_lev000_my%02d.nc' %(year))
            top = 5
            bottom = -2
        elif scaled == 'yes2exc':
            da = xr.open_dataarray(path + 'scaled2_lev000_my%02d.nc' %(year))
            top = 5
            bottom = -2
        elif scaled == 'no':
            da = xr.open_dataarray(path + 'lev000_my%02d.nc' %(year))
            top = 93
            bottom = -23
        da = da.assign_coords({'MY':year})
        #daw = da.where(Lsmin <= da.Ls, drop = True).where(da.Ls <= Lsmax, drop = True)
        da['Ls_int'] = np.floor(da['Ls'])
        if i == 0:
            d = da
        else:
            d = xr.concat([d, da], dim = 'time')
        i+=1
    d1_mean = d.groupby('Ls_int').mean()
    d1_std = d.groupby('Ls_int').std()
    d1_mean = d1_mean.to_dataset(name = 'eemean')
    d1_std = d1_std.to_dataset(name = 'eestd')
    d1 = xr.merge([d1_mean, d1_std])
    d1['upper'] = d1.eemean + d1.eestd
    d1['lower'] = d1.eemean - d1.eestd
    fig, axs = plt.subplots(len(d1.level), 1, figsize = (12, 4 * len(d1.level)), sharey = True)
    plt.suptitle('Eddy enstrophy climatology, averaged per Ls for MY27-35', fontsize = 12)
    j = 0
    axs[j].set_ylim(top = top, bottom = bottom)
    for lev in d1.level:
        d2 = d1.where(d1.level == lev, drop = True)
        d2 = d2.where(Lsmin <= d2.Ls_int, drop = True).where(d2.Ls_int <= Lsmax, drop = True)
        plot = axs[j].plot(d2.Ls_int, d2.eemean[:,0], color = 'red', label = 'mean')
        shade = axs[j].fill_between(d2.Ls_int, d2.lower[:,0], d2.upper[:,0],
                                    color = 'pink', alpha = 0.5, edgecolor = 'None', label = 'mean±1std')
        dash = axs[j].plot([270, 270], [-100, 800], '--', color = 'black')
        axs[j].set_xlabel('Ls')
        if scaled == 'yes':
            axs[j].set_ylabel('Scaled eddy enstrophy')
        elif scaled == 'yes2':
            axs[j].set_ylabel('Scaled2 eddy enstrophy')
        elif scaled == 'yes2exc':
            axs[j].set_ylabel('Scaled2 eddy enstrophy')
        elif scaled == 'no':
            axs[j].set_ylabel('Eddy enstrophy')
        axs[j].set_title('Isentropic level %03dK' %(lev))
        axs[j].legend()
        j+=1
    fig.tight_layout()
    fig.subplots_adjust(top=0.97)
    if scaled == 'yes':
        plt.savefig(path + '/Plots/scaled_climatology_Ls%03d-%03d.pdf' %(Lsmin, Lsmax))
    elif scaled == 'yes2':
        plt.savefig(path + '/Plots/scaled2_climatology_Ls%03d-%03d.pdf' %(Lsmin, Lsmax))
    elif scaled == 'yes2exc':
        plt.savefig(path + '/Plots/scaled2_climatology_exc28&34_Ls%03d-%03d.pdf' %(Lsmin, Lsmax))
    elif scaled == 'no':
        plt.savefig(path + '/Plots/climatology_Ls%03d-%03d.pdf' %(Lsmin, Lsmax))


def eddy_enstrophy_time_series(path, years, islev, **kwargs):
    scaled = kwargs.pop('scaled', 'no')
    Lsmin = kwargs.pop('Lsmin', 200)
    Lsmax = kwargs.pop('Lsmax', 340)
    i = 0
    fig, axs = plt.subplots(len(years),1, figsize = (15,30/8*len(years)), sharey = True)
    fig.suptitle('Eddy enstrophy at %03dK isentropic level' %(islev), fontsize = 16)
    for year in years:
        if scaled == 'yes':
            da = xr.open_dataarray(path + 'scaled_lev000_my%02d.nc' %(year))
        elif scaled == 'yes2':
            da = xr.open_dataarray(path + 'scaled2_lev000_my%02d.nc' %(year))
        elif scaled == 'no':
            da = xr.open_dataarray(path + 'lev000_my%02d.nc' %(year))
        da = da.assign_coords({'MY':year})
        daw = da.where(Lsmin <= da.Ls, drop = True).where(da.Ls <= Lsmax, drop = True).where(da.level == islev, drop = True)
        plot = axs[i].plot(daw.Ls, daw.values)
        #plot = axs[i].scatter(daw.Ls, daw.values, marker = 'x', s = 0.5)
        axs[i].set_xlabel('Ls')
        if scaled == 'yes':
            axs[i].set_ylabel('Scaled eddy enstrophy')
        elif scaled == 'yes2':
            axs[i].set_ylabel('Scaled2 eddy enstrophy')
        elif scaled == 'no':
            axs[i].set_ylabel('Eddy enstrophy')
        axs[i].set_title('My%02d' %(year))
        i+=1
    fig.tight_layout()
    fig.subplots_adjust(top=0.96)
    if scaled == 'yes':
        plt.savefig(path + '/Plots/scaled_lev%03d_scatter_all.pdf' %(islev))
    elif scaled == 'yes2':
        plt.savefig(path + '/Plots/scaled2_lev%03d_scatter_all.pdf' %(islev))
    elif scaled == 'no':
        plt.savefig(path + '/Plots/lev%03d_scatter_all.pdf' %(islev))