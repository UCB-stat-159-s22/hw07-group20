import xarray as xr
from cesm import cesm_analyze as ca


##########################################################################
# Declare clobal variables
scenarios = ['ssp126', 'ssp245', 'ssp370', 'ssp585']
s_names = [i[1:4] for i in scenarios]
model_names = ['hist'] + s_names


##########################################################################

def test_something1():
    dtest = ca.dictorize(
        func = xr.open_zarr, 
        modeldict = dict(zip(model_names, ['historical']+scenarios)),
    )
    
    assert True
    
    
# dtest = dictorize(
#     func = xr.open_zarr, 
#     modeldict = dict(zip(model_names, ['historical']+scenarios)),
# )
###########################################################################
# dtest_w = dictorize(
#     func = 'weight', 
#     modeldict = dtest,
# )
###########################################################################
# dtest_s = dictorize(
#     func = 'sel',
#     modeldict = nest_dicts(
#         dtest, 
#         ##{k: {'args': {'lat': slice(0, 20)}} for k in model_names},
#         {'args': {'lat': slice(0, 20)}},
#     ),
# )
###########################################################################
# dtest_v = dictorize(
#     func = 'var',
#     modeldict = nest_dicts(
#         dtest, 
#         {'var': 'tas'},
#     ),
# )
###########################################################################
# dtest_a = dictorize(
#     func = 'agg',
#     modeldict = nest_dicts(
#         dtest,
#         {'grps': ['lat', 'lon'], 'aggfunc': np.nanmean, 'roll': {}},
#     ),
# )
###########################################################################
# dtest_a1 = dictorize(
#     func = 'agg',
#     modeldict = nest_dicts(
#         dtest,
#         {'grps': 'time.year', 'aggfunc': np.nanmean, 'roll': {}},
#     ),
# )
###########################################################################
# dtest_a2 = dictorize(
#     func = 'agg',
#     modeldict = nest_dicts(
#         dtest_w,
#         {'grps': 'time.year', 'aggfunc': np.nanmean, 'roll': {}},
#     ),
# )
###########################################################################
# dtest_a3 = dictorize(
#     func = 'agg',
#     modeldict = nest_dicts(
#         dtest,
#         {'grps': ['lat', 'lon'], 'aggfunc': np.nanmean, 'roll': {}},
#     ),
# )
###########################################################################
# dtest_a4 = dictorize(
#     func = 'agg',
#     modeldict = nest_dicts(
#         dtest,
#         {'grps': ['lat', 'lon'], 'aggfunc': np.nanmean, 'roll': {'time': 120}}, # time only works in original units
#     ),
# )
###########################################################################
# print(dtest_a4.keys())
# dtest_a4['hist']