import xarray as xr
import numpy as np
import pandas as pd
import os

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


##########################################################################
def plot_lines(
    data,
    var='',
    path='', 
    varlabs={},
    xlab='', 
    ylab='', 
    title='', 
    fs=(10,4), 
    kwargs={},
    savefig=True,
    save_kwargs={},
):
    """
    
    """
    fig, ax = plt.subplots(figsize=fs, **kwargs)
    
    
    if isinstance(data, dict):
        for model in data.keys():
            data[model][var].plot(
                ax=ax,
                label=varlabs[model]['name']
            )

        ax.legend(title='Model')
    
    else:
        data.plot(ax=ax)
    
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    ax.set_title(title)
    
    if savefig:
        if not os.path.exists(path):
            print('Saving figure...')
            plt.savefig(path, **save_kwargs)


##########################################################################
def plot_map(
    data,
    var,
    proj,
    varlab='',
    cpad=0.1,
    title='', 
    titlesize=18,
    titlex=0.5,
    titley=1,
    fs=(10,10),
    extent=(),
    use_coasts=True,
    use_states=False,
    path='', 
    kwargs={}, 
    savefig=True,
    save_kwargs={},
):
    """
    See: https://github.com/SciTools/cartopy/blob/main/lib/cartopy/mpl/geoaxes.py
    
    """
    fig, ax = plt.subplots(
        figsize=fs, 
        subplot_kw=dict(projection=proj), 
        **kwargs,
    )
    
    data[var].plot(
        ax=ax,
        transform=proj,
        cbar_kwargs={
            # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.colorbar.html
            'orientation': 'horizontal',
            'label': varlab,
            'pad': cpad,
        }
    )
    
    if len(extent)>0:
        ax.set_extent(extent)
    if use_coasts:
        ax.coastlines("110m", color="k")
    if use_states:
        ax.add_feature(cfeature.STATES.with_scale("110m"))
    
    ax.set_xticks(list(range(-180, 181, 60)))
    ax.set_yticks(list(range(-90, 91, 30)))
    ax.set_title(title, x=titlex, y=titley, fontsize=titlesize)
    
    if savefig:
        if not os.path.exists(path):
            print('Saving figure...')
            plt.savefig(path, **save_kwargs)


##########################################################################




##########################################################################




##########################################################################