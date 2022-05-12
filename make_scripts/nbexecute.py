# Generic script to re-run a Jupyter notebook and save it in place
# 
# from https://nbclient.readthedocs.io/en/latest/client.html#using-a-command-line-interface
# and https://swcarpentry.github.io/make-novice/
import nbformat
from nbclient import NotebookClient
import os
import sys


def nbexecute(fn, kernel_name='cesm'):
    # fn in format 'main.ipynb'
    full_path = os.path.join(r'notebooks', fn)

    nb = nbformat.read(full_path, 4, nbformat.NO_CONVERT)

    client = NotebookClient(nb, timeout=600, kernel_name=kernel_name, resources={'metadata': {'path': r'notebooks/'}})
    client.execute()
    
    nbformat.write(nb, full_path)


if __name__ == '__main__':
    fn = sys.argv[1]
    kernel_name = sys.argv[2]
    nbexecute(fn, kernel_name)
