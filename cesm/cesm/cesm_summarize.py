import pandas as pd

def average_and_max(data, param):
    """
    data: dictionary of xarray datasets
    param: desired key (tas, huss, pr) 
    """
    summary = pd.DataFrame(columns = list(data), index = ["Mean", "Max"])
    for col in summary.columns:
        mn = data[col][param].mean(("lat","lon")).values[0]
        summary.loc["Mean", col] = mn
        mx = data[col][param].max(("lat","lon")).values[0]
        summary.loc["Max", col] = mx
    return summary
       
