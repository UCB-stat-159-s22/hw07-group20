import gcsfs
import xarray as xr
# import cftime
# from datetime import datetime# as datetime

import pandas as pd


##########################################################################

def find_available_data(filts=None):
    """
	Finds data csv from the cmip6 google storage. 
	
    Input: 
		-filts: an optional input filter for certain parameters 
	Output:
		-A dataframe of studies and various features attributed to them 
    """
    df = pd.read_csv("https://cmip6.storage.googleapis.com/pangeo-cmip6.csv")

    if pd.notnull(filts):
        df = df[filts]
    else:
        cols = ['tas', 'tasmax', 'tasmin', 'clr', 'hurs', 'huss', 'pr']
        
        df = df[
            (df['activity_id'].isin(['CMIP', 'ScenarioMIP'])) & 
            (df['institution_id'].isin(['NOAA-GFDL', 'NCAR'])) & # really only NCAR
            (df['source_id'] == 'CESM2') & 
           # (df['experiment_id'] == 'ssp245') & 
            (df['member_id'] == 'r11i1p1f1') & 
            (df['table_id'] == 'Amon') &
            (df['variable_id'].isin(cols))
        ]

    return df


##########################################################################

def model_eval(df):
    """
    Asses the unique values of model given. 
	
    Input:
		-df: a specific model df 
	Output:
		-A summary of the df attributes and unique column values
    """
    print(df.shape)

    for c in df.columns:
        if c != 'zstore' and c != 'dcpp_init_year':
            print(c, ": ", list(set(df[c])), '\n')

    return df[::6]


##########################################################################
def grab_data(df, ind):
    """
	Checks the output of one model variable. 
	
	Input:
		-df: A specific model df
		-ind: the study to check
	Output:
		-an xarray output summary
    """
    fs = gcsfs.GCSFileSystem(token='anon', access='read_only')

    # create a MutableMapping from a store URL
    mapper = fs.get_mapper(df.loc[ind, 'zstore'])

    # make sure to specify that metadata is consolidated
    ds = xr.open_zarr(mapper, consolidated=True)

    return ds


##########################################################################

def build_data(df, mip, exp, writeout=False):
    """
    Used in the function model_pull below to build models data into one xarray.
	
    Input:
		-df: A specifc model dataframe
		mip: Activity_id group
		exp: experiment_id group
		writeout: converts the data to zarr
	Output:
		-An xarray composed of mip and exp data. 
    """
    df = df[
        (df['activity_id'] == mip) &
        (df['experiment_id'] == exp)
    ].copy()

    for i, (ind, row) in enumerate(df.iterrows()):
        ds_temp = grab_data(df, ind)
        var = row['variable_id']

        if i == 0:
            ds = ds_temp.copy()
        else:
            ds[var] = ds_temp[var]

    if writeout:
        ds.to_zarr(f'../data/{exp}.zarr', mode='w')
    else:
        return ds


##########################################################################

def data_eval(df):
    """
    Returns a df of the selected model variables. Usefull to check for consistensy in dim/coors.
	
    Input:
		-df: A specific model df
	Output:
		-dataframe of selecrted model variables
    """
    x = {}

    drop_cols = ['institution_id', 'source_id', 'member_id', 
                 'table_id', 'grid_label', 'dcpp_init_year',
                ]

    cols = [
        'activity_id', 'experiment_id', 'variable_id', 
        'lat_size', 'lat_min', 'lat_max', 
        'lon_size', 'lon_min', 'lon_max',
        'time_size', 'time_min', 'time_max'
    ]

    for ind, row in df.iterrows():
        ds_temp = grab_data(df, ind)

        x[ind] = row.drop(drop_cols).to_dict()

        for coord in ['lat', 'lon', 'time']:
            x[ind][f'{coord}_size'] = ds_temp.coords[coord].size
            x[ind][f'{coord}_min'] = ds_temp.coords[coord].min().values
            x[ind][f'{coord}_max'] = ds_temp.coords[coord].max().values

        x[ind]['coords'] = ds_temp.coords

    xdf = pd.DataFrame.from_records(x).T
    xdf = xdf.sort_values('zstore')

    return xdf[cols]


##########################################################################

def model_pull(filts=None, writeout=True):
    """
    Reads in the selected models data from a directory. 
	
    Input:
		-filts: optional filter by variable
		-writeout: converts the data to zarr, default true 
	Output:
		-Downloads the data and prints a statement about status
    """
    ncar_models = find_available_data(filts)

    model_groups = pd.DataFrame({
        '# variables': ncar_models.groupby(['activity_id', 'experiment_id']).size()
    })

    for grp in model_groups.index:
        mip = grp[0]
        exp = grp[1]
        build_data(ncar_models, mip, exp, writeout=writeout)
        print(f'Completed downloading {grp}!')


##########################################################################
