import pandas as pd

def average_and_max(data, param):
    """
	Gets the average and maximum values for each study and returns as a dataframe.
	
	Input: 
		-data: dictionary of xarray datasets
		-param: desired key (tas, huss, pr) 
	Output: 
		-A dataframe containing average and max param values for each study in data
    """
    summary = pd.DataFrame(columns = list(data), index = ["Mean", "Max"])
    for col in summary.columns:
        mn = data[col][param].mean(("lat","lon")).values[0]
        summary.loc["Mean", col] = mn
        mx = data[col][param].max(("lat","lon")).values[0]
        summary.loc["Max", col] = mx
    return summary
       
