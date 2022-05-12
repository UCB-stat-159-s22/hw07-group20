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
    fig_out=False,
):
    """
    
    """
    ################################
    # Plotting
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
    
    ################################
    # Formatting
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    ax.set_title(title)
    
    ################################
    # Outputs
    if savefig:
        if not os.path.exists(path):
            print('Saving figure...')
            plt.savefig(path, **save_kwargs)
    
    if fig_out:
        return fig


##########################################################################
def plot_map(
    data,
    var,
    proj,
    varlab='',
    xticks=list(range(-180, 181, 60)),
    yticks=list(range(-90, 91, 30)),
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
    fig_out=False,
):
    """
    See: https://github.com/SciTools/cartopy/blob/main/lib/cartopy/mpl/geoaxes.py
    
    """
    data = data.copy()
    
    ################################
    # Plotting
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
    
    ################################
    # Formatting
    format_ax(
        ax,
        xticks, yticks,
        extent,
        use_coasts,
        use_states,
    )

    ################################
    # Outputs
    if savefig:
        if not os.path.exists(path):
            print('Saving figure...')
            plt.savefig(path, **save_kwargs)
    if fig_out:
        return fig


##########################################################################
from matplotlib.offsetbox import AnchoredText

def plot_facetmap(
    ds,
    var,
    proj,
    vardict,
    modeldict,
    lvl='model',
    xticks=list(range(-180, 181, 60)),
    yticks=list(range(-90, 91, 30)),
    corient='horizontal',
    cpad=0.07,
    axlabcoords=(-170, -40), # in lat, lon
    axlabsize=10,
    title='', 
    titlesize=18,
    titlex=0.5,
    titley=0.85,
    fs=(10,10),
    extent=(),
    use_coasts=True,
    use_states=False,
    path='', 
    kwargs={}, 
    savefig=True,
    save_kwargs={},
    fig_out=False,
):
    """
    Plots facet of xarray DataArray 
    for different models
    """
    ################################
    # Cleaning inputs
    ds = ds.copy()
    
    if isinstance(ds, dict):
        ds = ca.facet_ds(ds, var)
    
    ################################
    # Managing plot inputs
    models = ds[lvl].values # for subplot label writing below
    
    clab = '{} {}'.format(
        vardict[var]['name'],
        vardict[var]['units'],
    )
    
    # Cbar options: shrink, ticks,
    cbar_kws = {
        'orientation': corient,
        'aspect': 20,
        'label': clab,
        # 'labelsize': 16,
        # 'size': 20,
        'spacing': 'proportional',
        'pad': cpad, # distance between cbar and ax
    }
    
    subplot_kws = {
        'projection': proj,
    }
    
    ################################
    # Plotting facet plot

    # Options: cmap='RdYlBu_r', vmin=-30, vmax=30, extend='neither',
    
    dplot = ds[var].plot(
        col = lvl,
        col_wrap = 2,
        transform = proj,
        # robust=True,
        figsize = fs,
        cbar_kwargs = cbar_kws,
        subplot_kws = subplot_kws,
        **kwargs,
    )
    
    ################################
    # Formatting

    for model, ax in zip(models, dplot.axes.flatten()):
        if model == 'sp1':
            xs = ''
            ys = yticks
        if model == 'sp2':
            xs = ''
            ys = ''
        if model == 'sp3':
            xs = xticks
            ys = yticks
        if model == 'sp5':
            xs = xticks
            ys = ''

        format_ax(
            ax,
            xs, ys,
            extent,
            use_coasts,
            use_states,
        )

        # Get scenario label for subplot
        # (r'$' included to reconstruct LaTeX after splicing)
        m_name = modeldict[model]['name']
        scenario = m_name.split(':')[0] + r'$'
        sc_rcp = r'$' + m_name.split(':')[1]

        axlab = '{}\n{}'.format(scenario, sc_rcp)

        ax.add_artist(
            AnchoredText(
                axlab, 
                loc='lower left',
            )
        )

    dplot.set_xlabels('longitude [degrees]')
    dplot.set_ylabels('latitude [degrees]')

    plt.subplots_adjust(
        left=0, right=0.99,
        bottom=0.25, top=0.99,
        wspace=0.1, hspace=-0.4,
    )

    plt.suptitle(
        title, 
        x = titlex, y = titley,
        ha = 'center', va = 'center',
        fontsize = titlesize,
    )

    ################################
    # Outputs
    if savefig:
        if not os.path.exists(path):
            print('Saving figure...')
            plt.savefig(path, **save_kwargs)
    if fig_out:
        return dplot




##########################################################################
def format_ax(
    ax,
    xticks=list(range(-180, 181, 60)),
    yticks=list(range(-90, 91, 30)),
    extent=(),
    use_coasts=True,
    use_states=False,
    title='', 
    titlesize=18,
    titlex=0.5,
    titley=1,

):
    """
    
    """
    if len(extent)>0:
        ax.set_extent(extent)
    else:
        ax.set_xlim(-180, 180)
        ax.set_ylim(-90, 90)
    if use_coasts:
        ax.coastlines("110m", color="k")
    if use_states:
        ax.add_feature(cfeature.STATES.with_scale("110m"))
    
    if len(xticks)>0:
        ax.set_xticks(xticks)
    if len(yticks)>0:
        ax.set_yticks(yticks)
    ax.set_title(title, x=titlex, y=titley, fontsize=titlesize)


##########################################################################