#!/bin/bash -i

# Declare local place to save environments
##  $CONDA_PREFIX=/srv/conda 
##  to confirm, check "env | grep CONDA" and look for CONDA_PREFIX
## 
### !! Despite env_loc_full specified in -p flag, env_lov seems to be
### !! assigned preferentially from the values in envs_dirs in ~/.condarc file
### !!  (Solution for now is to include $HOME/envs here, repeating value in .condarc file)
env_loc=$HOME/envs # $CONDA_PREFIX/envs 

# Declare file to use for environment name and libraries
env_file=environment.yml

## Get name from environment.yml
# Steps:
#  1) Get "name: envname" from environment.yml
#  2) Separate string by ":" delimeter and select second item
#  3) Trim whitespace
env_name="$(grep name $env_file | cut -d ':' -f2 | xargs)"

# # Tests
# echo $env_name
# echo ${#env_name}

# Declare full directory for environment storage
### !! Perhaps ~/ not needed at start here?
env_loc_full=$env_loc/$env_name

########################################################################################

# Create new environment, if it doesn't exist yet
#  Also includes if-statement to ensure 'remove' not specified
#  --> helps prevent double-jeopardy of running both if- blocks
# TODO: generalize to check if $CONDA_PREFIX location (and subdir of env) exists, if not create each
if [[ ! -d $env_loc_full ]]; then
	if [[ $1 != "remove" ]]; then
		# conda deactivate # for sanity
		# conda activate notebook # hopefully works
		mamba env create -f $env_file -p $env_loc_full # not "mamba env create" but depends on mamba version
		# mamba env update --file $env_file --prune
		conda activate $env_name
		
		# Install pytest to enable installing ligotools
		conda install -c anaconda pytest -y
		
		python2 -m ipykernel install --user --name $env_name --display-name "IPython - $env_name"
	fi
fi

#########################################################################################

# Kill environment if it exists (and 'remove' is specified)
if [[ -d $env_loc_full ]]; then
	if [[ $1 = "remove" ]]; then
		conda deactivate
		mamba env remove -p $env_loc_full # -n $env_name
		jupyter kernelspec remove $env_name -y
	fi
fi

# #########################################################################################
