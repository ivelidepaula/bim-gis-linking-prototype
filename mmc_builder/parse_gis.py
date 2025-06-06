import geopandas as gpd
from mmc_builder.config import GIS_INPUT

def get_geojson_crs(geojson_path=None):
    """
    Given a path to a GeoJSON file, return its CRS string (example: "EPSG:25833") or None if unspecified.
    Defaults to GIS_INPUT if no path is provided.
    """
    path = geojson_path or GIS_INPUT
    gdf = gpd.read_file(path)
    return gdf.crs.to_string() if gdf.crs else None

def get_geojson_feature_info(geojson_path=None):
    """
    Given a path to a GeoJSON file, return a tuple:
      (feature_count, list_of_unique_geometry_types).
    Defaults to GIS_INPUT if no path is provided.
    """
    path = geojson_path or GIS_INPUT
    gdf = gpd.read_file(path)
    feature_count = len(gdf)
    geom_types = gdf.geom_type.unique().tolist()
    return feature_count, geom_types
