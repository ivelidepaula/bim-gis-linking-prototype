import os

# Input folder locations
BIM_INPUT = os.path.join(os.path.dirname(__file__), "..", "input", "bim", "Ifc4_SampleHouse.ifc")
GIS_INPUT = os.path.join(os.path.dirname(__file__), "..", "input", "gis", "landuse_residential_berlin.geojson")

# Output folder for MMC
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output", "mmc")

# MMC archive path
MMC_ARCHIVE = os.path.join(os.path.dirname(__file__), "..", "output", "my_container.mmc")

# URN Domain for container
MM_DOMAIN = "urn:demo:bim-gis-mmc"

# MMC schema version
MMC_FORMAT_VERSION = "2.1.0"