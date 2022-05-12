#!/bin/bash -i

# Declare environment storage location
env_loc="~/envs"
env_name="cesm" # or "notebook" if in Binder

env_loc_full=$env_loc/$env_name


# Activate environment and rerun all notebooks
conda activate $env_loc_full

# Re-run all notebooks, and convert latest output to scripts
# for importing in final reproducibility_attempt.ipynb
python make_scripts/nbexecute.py Pangeo_data_selection.ipynb $env_name

python make_scripts/nbexecute.py CESM_EDA.ipynb $env_name

python scripts/nbexecute.py United_States.ipynb $env_name

python scripts/nbexecute.py main.ipynb $env_name
