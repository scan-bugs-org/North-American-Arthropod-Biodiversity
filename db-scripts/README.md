# SQLite Database Generation Scripts
This directory contains the code to pull a subset of the SCAN
database consisting of all North American occurrences records

### To build (all paths relative to this directory):
1. Make sure connection to the SCAN database is configured
in $HOME/my.cnf with hostname, username, and password:
```
[client]
user = ...
password = ...
host = ...
```
2. Make sure [conda](https://conda.io/en/latest) is installed and
run `conda env create -f environment.yml` to create the python environment
nesscessary for running the scripts
3. Activate the conda environment: `conda activate arthropod_biodiversity`
4. Run `jupyter notebook` to open the browser-based processing notebook
5. Edit the notebook cells as necessary
6. Run all cells in the notebook to generate YY-mm-dd_symbscan.sqlite for today's date

