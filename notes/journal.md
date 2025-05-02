# Day 01

- created and activated virtual environment

```
python3.11 -m venv venv
source venv/bin/activate
```


- installed necessary libraries on bash

```
pip install ifcopenshell
pip install geopandas
pip install shapely
pip install pyproj           # library for cartographic transformations
pip install lxml             # processing XML
pip install psycopg2-binary  # for PostGIS later
```
More about the libraries: 

https://docs.ifcopenshell.org/ifcopenshell-python/installation.html
https://pypi.org/project/psycopg2-binary/
- installed homebrew
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Link for Homebrew: https://brew.sh/
- created folder structure

### Learnings: 
- ifcopenshell currently only works until the version 3.11 of python

A way to fix it:
```
# Delete the wrong venv
rm -rf venv

# Create new venv with correct Python
python3.11 -m venv venv

# Activate it
source venv/bin/activate

# Final check to make sure it worked
python --version
```

# Day 2

- Prepare environment on pycharm

```
pip install -r requirements.txt
```

- download ifc sample test files
- 
