import os
import pytest
import xarray as xr
import numpy as np

from cesm import cesm_analyze as ca

# change temp dir one folder down for correct relative path testing
os.chdir('cesm')


##########################################################################
# Declare global variables

# https://docs.pytest.org/en/stable/how-to/capture-warnings.html#warnings
# turns all warnings into errors for this module
pytestmark = pytest.mark.filterwarnings("ignore::DeprecationWarning")


##########################################################################
def test_import():
    scenarios = ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585']
    model_names = ['hist', 'sp1', 'sp2', 'sp3', 'sp5']

    dtest = ca.dictorize(
        func = xr.open_zarr,
        modeldict = dict(zip(model_names, scenarios)),
    )

    assert len(dtest) == 5
    assert list(dtest) == ['hist', 'sp1', 'sp2', 'sp3', 'sp5']
    assert isinstance(dtest['hist'], xr.Dataset)


###########################################################################
def test_sel():
    scenarios = ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585']
    model_names = ['hist', 'sp1', 'sp2', 'sp3', 'sp5']

    dtest = ca.dictorize(
        func = xr.open_zarr,
        modeldict = dict(zip(model_names, scenarios)),
    )

    dtest_s = ca.dictorize(
        func = 'sel',
        modeldict = ca.nest_dicts(
            dtest,
            {'args': {'lat': slice(0, 20)}},
        )
    )

    assert len(dtest_s) == 5
    assert list(dtest_s) == ['hist', 'sp1', 'sp2', 'sp3', 'sp5']
    assert isinstance(dtest_s['hist'], xr.Dataset)


###########################################################################
def test_var():
    scenarios = ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585']
    model_names = ['hist', 'sp1', 'sp2', 'sp3', 'sp5']

    dtest = ca.dictorize(
        func = xr.open_zarr,
        modeldict = dict(zip(model_names, scenarios)),
    )

    dtest_v = ca.dictorize(
        func = 'var',
        modeldict = ca.nest_dicts(
            dtest,
            {'var': 'tas'},
        )
    )

    assert len(dtest_v) == 5
    assert list(dtest_v) == ['hist', 'sp1', 'sp2', 'sp3', 'sp5']
    assert isinstance(dtest_v['hist'], xr.DataArray)


###########################################################################
def test_weight():
    scenarios = ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585']
    model_names = ['hist', 'sp1', 'sp2', 'sp3', 'sp5']

    dtest = ca.dictorize(
        func = xr.open_zarr,
        modeldict = dict(zip(model_names, scenarios)),
    )

    dtest_w = ca.dictorize(
        func = 'weight', 
        modeldict = dtest,
    )

    assert len(dtest_w) == 5
    assert list(dtest_w) == ['hist', 'sp1', 'sp2', 'sp3', 'sp5']
    assert isinstance(dtest_w['hist'], xr.core.weighted.DatasetWeighted)


###########################################################################
def test_agg1():
    scenarios = ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585']
    model_names = ['hist', 'sp1', 'sp2', 'sp3', 'sp5']

    dtest = ca.dictorize(
        func = xr.open_zarr,
        modeldict = dict(zip(model_names, scenarios)),
    )

    dtest_a = ca.dictorize(
        func = 'agg',
        modeldict = ca.nest_dicts(
            dtest,
            {'grps': ['lat', 'lon'], 'aggfunc': np.nanmean, 'roll': {}},
        )
    )

    assert len(dtest_a) == 5
    assert list(dtest_a) == ['hist', 'sp1', 'sp2', 'sp3', 'sp5']
    assert isinstance(dtest_a['hist'], xr.Dataset)


###########################################################################
def test_agg2():
    scenarios = ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585']
    model_names = ['hist', 'sp1', 'sp2', 'sp3', 'sp5']

    dtest = ca.dictorize(
        func = xr.open_zarr,
        modeldict = dict(zip(model_names, scenarios)),
    )

    dtest_a = ca.dictorize(
        func = 'agg',
        modeldict = ca.nest_dicts(
            dtest,
            {'grps': 'time.year', 'aggfunc': np.nanmean, 'roll': {}},
        )
    )

    assert len(dtest_a) == 5
    assert list(dtest_a) == ['hist', 'sp1', 'sp2', 'sp3', 'sp5']
    assert isinstance(dtest_a['hist'], xr.Dataset)


###########################################################################
def test_agg3():
    scenarios = ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585']
    model_names = ['hist', 'sp1', 'sp2', 'sp3', 'sp5']

    dtest = ca.dictorize(
        func = xr.open_zarr,
        modeldict = dict(zip(model_names, scenarios)),
    )

    dtest_w = ca.dictorize(
        func = 'weight', 
        modeldict = dtest,
    )

    dtest_a = ca.dictorize(
        func = 'agg',
        modeldict = ca.nest_dicts(
            dtest_w,
            {'grps': ['lat', 'lon'], 'aggfunc': np.nanmean, 'roll': {}},
        )
    )

    assert len(dtest_a) == 5
    assert list(dtest_a) == ['hist', 'sp1', 'sp2', 'sp3', 'sp5']
    assert isinstance(dtest_a['hist'], xr.Dataset)


###########################################################################
def test_agg4():
    scenarios = ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585']
    model_names = ['hist', 'sp1', 'sp2', 'sp3', 'sp5']

    dtest = ca.dictorize(
        func = xr.open_zarr,
        modeldict = dict(zip(model_names, scenarios)),
    )

    dtest_a = ca.dictorize(
        func = 'agg',
        modeldict = ca.nest_dicts(
            dtest,
            {'grps': ['lat', 'lon'], 'aggfunc': np.nanmean, 'roll': {'time': 120}},
        )
    )

    assert len(dtest_a) == 5
    assert list(dtest_a) == ['hist', 'sp1', 'sp2', 'sp3', 'sp5']
    assert isinstance(dtest_a['hist'], xr.Dataset)


###########################################################################
def test_facet1():
    scenarios = ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585']
    model_names = ['hist', 'sp1', 'sp2', 'sp3', 'sp5']

    dtest = ca.dictorize(
        func = xr.open_zarr,
        modeldict = dict(zip(model_names, scenarios)),
    )

    ds_w = ca.dictorize(
        func = 'weight', 
        modeldict = dtest,
    )

    ds_mt = ca.dictorize(
        func = 'agg',
        modeldict = ca.nest_dicts(
            ds_w,
            {'grps': ('lat', 'lon'), 'aggfunc': np.nanmean, 'roll': {}},
        ),
    )


    # "_my" for mean of each year
    ds_my = ca.dictorize(
        func = 'agg',
        modeldict = ca.nest_dicts(
            ds_mt,
            {'grps': 'time.year', 'aggfunc': np.nanmean, 'roll': {}},
        ),
    )

    dfacet = ca.facet_ds(ds_my, 'tas')
    
    assert isinstance(dfacet, xr.Dataset)
    assert len(dfacet.dims) == 2


###########################################################################
def test_facet2():
    scenarios = ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585']
    model_names = ['hist', 'sp1', 'sp2', 'sp3', 'sp5']

    dtest = ca.dictorize(
        func = xr.open_zarr,
        modeldict = dict(zip(model_names, scenarios)),
    )

    baseline = (
        dtest['hist']
        .sel(time=slice('1850', '1980'))
        .mean('time')
    )

    ds_diffs = dtest.copy()
    ds_diffs['hist'] = baseline.copy()

    ds_diffs = ca.dictorize(
        func = 'diff',
        modeldict = ca.nest_dicts(
            ds_diffs,
        ),
    )

    d2100 = ca.dictorize(
        func = 'sel',
        modeldict = ca.nest_dicts(
            ds_diffs,
            {'args': {'time': '2100-12-15'}},
        ),
    )

    dfacet = ca.facet_ds(d2100, 'tas')
    
    assert isinstance(dfacet, xr.Dataset)
    assert len(dfacet.dims) == 3


###########################################################################
