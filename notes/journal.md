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

# Day 3
- reread both papers

Add some sample IFC files from:
https://github.com/youshengCode/IfcSampleFiles/tree/main

# Day 4
- read IfcOpenShell Documentation https://docs.ifcopenshell.org/index.html
- read DIN 18290-1
- create ifc parser
- read https://www.buildingsmart.org/wp-content/uploads/2020/02/User-Guide-for-Geo-referencing-in-IFC-v2.0.pdf
- install QuickOSM to create query to overpass turbo (https://overpass-turbo.eu/)
- Notes to myself: explain later about 
  - What RefLatitude and RefLongitude Are
  - What IfcMapConversion Does