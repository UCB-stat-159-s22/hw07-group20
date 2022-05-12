import os
import pytest
import xarray as xr
import numpy as np

from cesm import cesm_summarize as cs

# change temp dir one folder down for correct relative path testing
os.chdir('cesm')

##########################################################################

def test_average_and_max():
    models = ['sp1', 'sp2', 'sp3', 'sp5']

	test = cs.average_and_max(USA, 'tas')
	
    assert len(dtest) == 5
    assert list(dtest) == ['hist', 'sp1', 'sp2', 'sp3', 'sp5']
    assert isinstance(dtest['hist'], xr.Dataset)


def average_and_max(data, param):
    summary = pd.DataFrame(columns = list(data), index = ["Mean", "Max"])
    for col in summary.columns:
        mn = data[col][param].mean(("lat","lon")).values[0]
        summary.loc["Mean", col] = mn
        mx = data[col][param].max(("lat","lon")).values[0]
        summary.loc["Max", col] = mx
    return summary
       