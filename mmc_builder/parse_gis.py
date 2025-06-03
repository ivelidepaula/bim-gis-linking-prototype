import geopandas as gpd
import os

# File path
file_path = os.path.join("..", "input", "gis", "landuse_residential_berlin.geojson")

# Load geodataframe
gdf = gpd.read_file(file_path)

# Print CRS info
print("CRS:", gdf.crs)

# Print basic geometry info
print("\nTotal features:", len(gdf))
print("Geometry type:", gdf.geom_type.unique())
