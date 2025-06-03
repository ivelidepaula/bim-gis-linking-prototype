# create_mmc.py

# import os
# import xml.etree.ElementTree as ET      # creates the xml files
# import zipfile                          # creates the final .mmc zip archive
# import shutil                           # copies input inside the models/ folder inside the MMC
# import ifcopenshell
# import geopandas as gpd
#
# # --- Input Files
# bim_input = "../input/bim/Ifc4_SampleHouse.bim"
# gis_input = "../input/gis/landuse_residential_berlin.geojson"
#
# # --- Output Structure
# output_dir = "../output/mmc"
# models_dir = os.path.join(output_dir, "models")
# os.makedirs(models_dir, exist_ok=True)
#
# # --- Copy Input Files into models/
# bim_filename = os.path.basename(bim_input)
# gis_filename = os.path.basename(gis_input)
#
# shutil.copy(bim_input, os.path.join(models_dir, bim_filename))
# shutil.copy(gis_input, os.path.join(models_dir, gis_filename))
#
# # --- Extract IFC Metadata
# model = ifcopenshell.open(bim_input)
# ifc_version = model.schema
#
# # --- Extract GIS Metadata
# gdf = gpd.read_file(gis_input)
# crs_string = gdf.crs.to_string() if gdf.crs else "Unknown"
#
# # --- 1. MultiModel.xml
# mm = ET.Element("MultiModel", attrib={
#     "formatVersion": "2.1.0",
#     "mmDomain": "urn:demo:bim-gis-mmc"
# })
#
# # Part 2:
# # TODO: Define a helper function to derive modelType and formatType from file extension
# # TODO: Generate dynamic IDs for each model: model_id, model_data_id, resource_id
# # TODO: Add the BIM model entry to MultiModel.xml using extracted IFC version and dynamic IDs
# # TODO: Add the GIS model entry to MultiModel.xml using extracted CRS and dynamic IDs
#
# # Part 3:
# # TODO: Define a helper function to derive modelType and formatType from file extension
# # TODO: Generate dynamic IDs for each model: model_id, model_data_id, resource_id
# # TODO: Add the BIM model entry to MultiModel.xml using extracted IFC version and dynamic IDs
# # TODO: Add the GIS model entry to MultiModel.xml using extracted CRS and dynamic IDs
#
# # Part 4:
# # TODO: Start LinkModel.xml with formatVersion 2.1.0
# # TODO: Create a basic Geospatial_Link (type="pose") with dummy outerPose (e.g. origin: 0,0,0)
# # TODO: Add two <Relatum> tags:
# #       - one with modelId="mmc" (refers to the container)
# #       - one pointing to the BIM model using the same IDs as in MultiModel.xml
# # TODO: Optionally extract real geolocation from IfcSite or IfcMapConversion (if available)
# # TODO: Write LinkModel.xml to the output_dir
#
# # Part 5:
# # TODO: Walk through the output_dir and zip everything (preserve structure under folder "mmc/")
# # TODO: Write the final .mmc file (e.g., my_container.mmc) to output/


import os
import xml.etree.ElementTree as ET
import zipfile
import shutil
import ifcopenshell
import geopandas as gpd

# ──────────────────────────────────────────────────────────────────────────────────────
# Configuration: adjust these if your folder structure changes
# ──────────────────────────────────────────────────────────────────────────────────────

# 1) Input BIM (IFC) and GIS (GeoJSON) file paths (relative to this script)
bim_input = "../input/bim/Ifc4_SampleHouse.ifc"
gis_input = "../input/gis/landuse_residential_berlin.geojson"

# 2) Output base folder for the MMC container
output_dir = "../output/mmc"
models_dir = os.path.join(output_dir, "models")

# 3) Final .mmc zip file path
mmc_output_path = "../output/my_container.mmc"

# 4) The `mmDomain` URN—must be unique per project
mm_domain = "urn:demo:bim-gis-mmc"

# ──────────────────────────────────────────────────────────────────────────────────────
# Step 0: Ensure output directories exist
# ──────────────────────────────────────────────────────────────────────────────────────

os.makedirs(models_dir, exist_ok=True)

# ──────────────────────────────────────────────────────────────────────────────────────
# Helper Functions
# ──────────────────────────────────────────────────────────────────────────────────────

def get_model_info(file_path):
    """
    Given a filepath, return a tuple (model_type, format_type, format_version).
    - model_type is a human‐readable string (e.g., "Building Model", "GeoData", "Document").
    - format_type is the file format (e.g., "IFC", "GeoJSON", "PDF", etc.).
    - format_version is either extracted from file content (IFC) or a default/"Unknown".
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".ifc":
        # IFC: use ifcopenshell to get schema/version
        ifc_model = ifcopenshell.open(file_path)
        return "Building Model", "IFC", ifc_model.schema  # e.g. ("Building Model","IFC","IFC4")
    elif ext in [".geojson", ".json"]:
        # GeoJSON: use geopandas to get CRS (formatVersion = "1.0" since GeoJSON is typically v1.0)
        return "GeoData", "GeoJSON", "1.0"
    elif ext == ".shp":
        return "GeoData", "SHP", "Unknown"
    elif ext == ".gml":
        return "GeoData", "GML", "Unknown"
    elif ext == ".pdf":
        return "Document", "PDF", "1.7"
    else:
        return "Document", ext[1:].upper(), "Unknown"

def generate_ids(prefix):
    """
    Given a prefix (e.g. "bim", "gis"), generate a dictionary of consistent IDs:
    - model_id: e.g. "bim01"
    - model_data_id: e.g. "bim01-md"
    - resource_id: e.g. "bim01-dr"
    """
    model_id = f"{prefix}01"
    return {
        "model_id": model_id,
        "model_data_id": f"{model_id}-md",
        "resource_id": f"{model_id}-dr"
    }

# ──────────────────────────────────────────────────────────────────────────────────────
# Step 1: Copy the BIM and GIS input files into the "models/" folder inside the MMC container
# ──────────────────────────────────────────────────────────────────────────────────────

bim_filename = os.path.basename(bim_input)
gis_filename = os.path.basename(gis_input)

shutil.copy(bim_input, os.path.join(models_dir, bim_filename))
shutil.copy(gis_input, os.path.join(models_dir, gis_filename))

# ──────────────────────────────────────────────────────────────────────────────────────
# Step 2: Extract any needed metadata from the BIM and GIS files
# ──────────────────────────────────────────────────────────────────────────────────────

# 2a) BIM metadata: get IFC schema version
# get_model_info returns ("Building Model", "IFC", "IFC4") for an IFC
bim_model_type, bim_format_type, bim_format_version = get_model_info(os.path.join(models_dir, bim_filename))

# 2b) GIS metadata: get CRS if available
# For GeoJSON/GIS, we mostly need CRS (we'll store it as Meta in MultiModel.xml)
gdf = gpd.read_file(os.path.join(models_dir, gis_filename))
crs_string = gdf.crs.to_string() if gdf.crs else "Unknown"

# ──────────────────────────────────────────────────────────────────────────────────────
# Step 3: Build MultiModel.xml
# ──────────────────────────────────────────────────────────────────────────────────────

# 3a) Create root element
mm = ET.Element("MultiModel", attrib={
    "formatVersion": "2.1.0",
    "mmDomain": mm_domain
})

# 3b) BIM entry
bim_ids = generate_ids("bim")
bim_app = ET.SubElement(mm, "ApplicationModel", attrib={
    "id": bim_ids["model_id"],
    "modelType": bim_model_type
})
bim_data = ET.SubElement(bim_app, "ModelData", attrib={
    "id": bim_ids["model_data_id"],
    "formatType": bim_format_type,
    "formatVersion": bim_format_version
})
ET.SubElement(bim_data, "DataResource", attrib={
    "id": bim_ids["resource_id"],
    "location": f"models/{bim_filename}"
})
# Optionally add more IFC metadata if needed (e.g., ViewDefinition or fileFormat):
# ET.SubElement(bim_data, "Meta", attrib={"key": "fileFormat", "value": ".ifc"})

# 3c) GIS entry
gis_ids = generate_ids("gis")
gis_model = ET.SubElement(mm, "ApplicationModel", attrib={
    "id": gis_ids["model_id"],
    "modelType": "GeoData"
})
gis_data = ET.SubElement(gis_model, "ModelData", attrib={
    "id": gis_ids["model_data_id"],
    "formatType": "GeoJSON",
    "formatVersion": "1.0"
})
ET.SubElement(gis_data, "DataResource", attrib={
    "id": gis_ids["resource_id"],
    "location": f"models/{gis_filename}"
})
if crs_string != "Unknown":
    ET.SubElement(gis_data, "Meta", attrib={"key": "CRS", "value": crs_string})

# 3d) Write MultiModel.xml to output_dir
mm_path = os.path.join(output_dir, "MultiModel.xml")
ET.ElementTree(mm).write(mm_path, encoding="utf-8", xml_declaration=True)

print(f"Written MultiModel.xml to: {mm_path}")

# ──────────────────────────────────────────────────────────────────────────────────────
# Step 4: Build LinkModel.xml
# ──────────────────────────────────────────────────────────────────────────────────────

link_model = ET.Element("LinkModel", attrib={"formatVersion": "2.1.0"})

# 4a) Create a single Geospatial_Link with placeholder pose
geo_link = ET.SubElement(link_model, "Geospatial_Link", attrib={"type": "pose"})
pose = ET.SubElement(geo_link, "outerPose")
ET.SubElement(pose, "origin").text = "0,0,0"
ET.SubElement(pose, "x-axis").text = "1,0,0"
ET.SubElement(pose, "z-axis").text = "0,0,1"
ET.SubElement(pose, "scale").text = "1,1,1"

# 4b) Relatum for the container itself
ET.SubElement(geo_link, "Relatum", attrib={"modelId": "mmc"})

# 4c) Relatum for the BIM model (use IDs we generated above)
ET.SubElement(geo_link, "Relatum", attrib={
    "modelId": bim_ids["model_id"],
    "formatId": bim_ids["model_data_id"],
    "resourceId": bim_ids["resource_id"]
})

# 4d) (Optional) If you want a Geo Relatum to GIS as well, add another Relatum:
ET.SubElement(geo_link, "Relatum", attrib={
    "modelId": gis_ids["model_id"],
    "formatId": gis_ids["model_data_id"],
    "resourceId": gis_ids["resource_id"]
})

# 4e) Write LinkModel.xml to output_dir
link_path = os.path.join(output_dir, "LinkModel.xml")
ET.ElementTree(link_model).write(link_path, encoding="utf-8", xml_declaration=True)

print(f"Written LinkModel.xml to: {link_path}")

# ──────────────────────────────────────────────────────────────────────────────────────
# Step 5: Package Everything into a .mmc Zip Archive
# ──────────────────────────────────────────────────────────────────────────────────────

with zipfile.ZipFile(mmc_output_path, 'w') as zipf:
    for dirpath, _, filenames in os.walk(output_dir):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            # We want paths inside the zip to be under a top‐level "mmc/" folder
            rel_path = os.path.relpath(full_path, output_dir)
            zipf.write(full_path, arcname=os.path.join("mmc", rel_path))

print(f"MMC container created at: {mmc_output_path}")
