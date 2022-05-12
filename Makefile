# Make environment from scratch
.PHONY : env
env :
	chmod a+x make_scripts/envsetup.sh
	bash -ic make_scripts/envsetup.sh


# Build the JupyterBook locally
.PHONY : html
html :
	chmod a+x make_scripts/bookgen.sh
	bash -ic make_scripts/bookgen.sh


# Build the JupyterBook with URL Hub proxy
.PHONY : html-hub
html-hub :
	pip install ghp-import
	ghp-import -n -p -f _build/html


# Clean everything
.PHONY : clean
clean :
	rm -r figures/*
	rm -rf _build


# Rerun all notebooks and save newly made figures
.PHONY : all
all : 
	chmod a+x make_scripts/runall.sh
	bash -ic make_scripts/runall.sh
