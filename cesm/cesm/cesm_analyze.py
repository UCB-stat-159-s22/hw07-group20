# https://clipc-services.ceda.ac.uk/dreq/index.html
import xarray as xr
import numpy as np
import pandas as pd


##########################################################################

def dictorize(func, modeldict):
    """
    performs a function on all provided 
    xarray datasets.
    inputs:
        - func: function or str of desired func.
            - options are:
                - xr.open_zarr
                - 'weight' for ds.weighted
                - 'sel' for ds.sel(...)
                - 'agg' for ds.groupby(...).agg(...)
                - 'var' for ds[var]
        ##- models: list of model names
        - modeldict: dictionary of format
            - key: model names (informal)
            - values: str or dictionary of values
                      to pass to func. Specific to
                      each func. If dataset provided,
                      use key['data'] as storage location.
                - values with unnested dict:
                    - [xr.open_zarr, 'weight']
                - values with nested dict:
                    - [all others]
    output:
        - dictionary of xarray datasets
        - dict will be of xarray dataarrays if 'var' func is used
    """
    if func == xr.open_zarr:
        d = {
            k: func(f'../data/{v}.zarr') for k, v in modeldict.items()
        }

    if func == 'sel':
        d = {
            k: v['data'].sel(
                v['args']
            ) for k, v in modeldict.items()
        }

    if func == 'var':
        d = {
            k: ds['data'][ds['var']] for k, ds in modeldict.items()
        }

    if func == 'weight':
        keys = list(modeldict)
        first_ds = modeldict[keys[0]]#['data']

        weights = np.cos(np.deg2rad(first_ds['lat']))
        weights.name = 'weights'

        d = {
            k: ds.weighted(weights) for k, ds in modeldict.items()
        }

    if func == 'agg':
        d = {}

        for k, v in modeldict.items():
            ds_temp = agg_ds(
                v['data'], 
                v['aggfunc'], v['grps'],
                v['roll'],
            )
            d[k] = ds_temp.copy()
            
    if func == 'diff':
        d = {}
        
        for k, v in modeldict.items():
            if k != 'hist':
                d[k] = base_sub(
                    v['data'], 
                    modeldict['hist']['data']
                )

    return d


##########################################################################

def agg_ds(ds, aggfunc, dims, roll={}):
    """
    
    """
    if isinstance(ds, xr.core.weighted.DatasetWeighted):
        # # ds_agg = ds.mean(('lat', 'lon'))
        # if pd.isnull(dims):
        #     return ds_agg
        return ds.mean(dims)


    else:
        ds_agg = ds.copy()

    if len(roll.keys()) > 0:
        ds_agg = ds_agg.roll(roll)
    else:
        if isinstance(dims, str):
            ds_agg = ds_agg.groupby(dims).reduce(aggfunc)
        else:
            ds_agg = ds_agg.reduce(aggfunc, dims)

    return ds_agg


##########################################################################

def nest_dicts(d, d_args={}):
    """
    take output from dictorize() and
    nest (sometimes with additional args)
    for input into dictorize() again.
    inputs:
        - d: dict of xarray datasets
             (directly output from dictorize() )
        - d_args: dict, additional args to add
            - can be nested dict of k[arg] = val
            - can be unnested dict of {arg: val}
                (if so, will be broadcast to all ds in d)
    output:
        - nested dict of xarray datasets and
          associated args for input into dictorize()
            - dataset under k['data']
            - args under k[...]
    """
    dn = {}
    for k in d.keys():
        dn[k] = {}

    for k, v in d.items():
        dn[k]['data'] = v

    if len(d_args.keys()) > 0:
        same_keys = set(list(d)) == set(list(d_args))

        if not same_keys:
            # then assume d_args is for all ds in d,
            # and nest

            # create new dict
            d_args_old = {
                argk: argv for argk, argv in d_args.items()
            }
            d_args = {}

            # replace input dict
            for k in d.keys():
                d_args[k] = {}
                for argk, argv in d_args_old.items():
                    d_args[k][argk] = argv

        # Proceed with d_args as nested dict (from input or transform)
        for k, args in d_args.items():
            for arg_key, arg_val in args.items():
                dn[k][arg_key] = arg_val

    return dn


##########################################################################

def base_sub(ds, hist):
    """
    ds has 3 dims (time included)
    hist has 2 dims (lat, lon... time only 1 value)
    """
    ds_cols = list(ds)
    hist_cols = list(hist)
    
    cols = list(set(ds_cols).intersection(set(hist_cols)))
    
    return ds[cols] - hist[cols]
    

##########################################################################

def facet_ds(d, var):
    """
    requires a ds with at least n-1 dimensions
        (either (lat/lon) remain, or only time remains)
    coords are by default ordered by
        time, lat, lon
    """
    d = d.copy() # to prevent_modifying in-place
    
    ################################
    # Metadata extraction
    models = np.array(list(d.keys()))
    n_models = len(models)
    
    modeldims = {}
    for k in models:
        modeldims.update(dict(d[k].dims))
    
    try:
        modeldims.pop('nbnd')
    except KeyError:
        pass
    
    n_dims = len(modeldims)
    datadims = [k for k, v in modeldims.items() if v!=1]
    framedims = [k for k, v in modeldims.items() if v==1]
        
    ################################
    # Check suitability for faceting
    if n_dims > 2:        
        if len(datadims) > 2:
            raise KeyError
        else:
            for k in models:
                d[k] = d[k].mean(framedims)

    ################################
    # Data clean in prep for faceting
    
    # Create new DataArrays in each ds 
    #  as their own model names (to avoid all names of var)
    for m in models:
        d[m][m] = d[m][var].copy()
        
    ################################
    # 2 dimensions cleaning
    if len(datadims) == 2:
        # assume lat/lon only dims
        newdims = ['lat', 'lon', 'model']
        
        newcoords = {
            'lat': d[models[-1]]['lat'],
            'lon': d[models[-1]]['lon'],
            'model': models,
        }
        
        model_data = np.dstack(tuple([d[m][var].values for m in models]))
                
    ################################
    # 1 dimension cleaning
    else:
        # assume time only dim
        dimname = list(modeldims)[0]
        newdims = ['model', dimname]
        
        # Fix issue where hist is overwritten due to diff in time dim
        data_lens = set([len(d[m][var].values) for m in models])
        
        if len(data_lens) != 1:
            h_excess = len(d[models[-1]][var].values)
            sp_excess = len(d['hist'][var].values)

            time_data = list(np.repeat(np.nan, n_models))

            for i, m in enumerate(models):
                if m == 'hist':
                    time_data[0] = np.concatenate([
                        d['hist'][var].values,
                        np.repeat(np.nan, h_excess),
                    ])
                else:        
                    time_data[i] = np.concatenate([
                        np.repeat(np.nan, sp_excess),
                        d[m][var].values,
                    ])

            model_data = np.vstack(tuple(time_data))
            
            newcoords = {
                'model': models,
                dimname: np.concatenate([
                    d['hist'][dimname].values, 
                    d[models[-1]][dimname].values
                ])
            }

        else:
            model_data = np.vstack(tuple([d[m][var].values for m in models]))
            
            newcoords = {
                'model': models,
                dimname: d[models[-1]][dimname] 
            }

    ################################
    # Last check before faceting
    # if model_data.shape[0] != n_models:
    #     print(models)
    #     print(n_dims)
    #     return model_data
    #     raise KeyError
        
    ################################
    # Facet datasets!
    dfacet = xr.Dataset(
        data_vars = {var: (newdims, model_data)},
        coords = newcoords,
    )

    return dfacet


##########################################################################
    
        

    
    