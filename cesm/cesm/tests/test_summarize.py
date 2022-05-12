#imports 
import xarray as xr
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from cesm import cesm_analyze as ca
from cesm import cesm_summarize as cs
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import shelve


##########################################################################

def test_average_and_max():
    with shelve.open('../analysis_data/descriptors') as db:
        vardict = db['vardict']
        modeldict = db['modeldict']

    #Opening each of the Xarray datasets
    ds = ca.dictorize(
        func = xr.open_zarr, 
        modeldict = {k: v['code'] for k, v in modeldict.items()},
    )

    baseline = (
        ds['hist']
        .sel(time=slice('1850', '1980'))
        .mean('time')
    )

    ds_diffs = ds.copy()
    ds_diffs['hist'] = baseline
    ds_diffs = ca.dictorize(
        func = 'diff',
        modeldict = ca.nest_dicts(
            ds_diffs,
        ),
    )

    USA = ca.dictorize(
        func = 'sel',
        modeldict = ca.nest_dicts(
            ds_diffs,
            {'args': {'time': '2100',
                     'lat': slice(0, 70),
                     'lon': slice(225,300)}},
        ),
    )

    USA = ca.dictorize(
        func = 'agg',
        modeldict = ca.nest_dicts(
            USA,
            {'grps': 'time.year', 'aggfunc': np.nanmean, 'roll': {}},
        ),
    )



    test = cs.average_and_max(USA, 'tas')

    assert len(test.columns) == 4
    assert isinstance(test, pd.DataFrame)

