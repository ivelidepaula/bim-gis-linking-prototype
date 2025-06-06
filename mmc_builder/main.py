import os
import shutil
import zipfile

from mmc_builder.config import BIM_INPUT, GIS_INPUT, OUTPUT_DIR, MMC_ARCHIVE
from mmc_builder.parse_bim import get_ifc_schema_version, get_ifc_outerpose
from mmc_builder.parse_gis import get_geojson_crs
from mmc_builder.xml_builder import (
    build_multimodel_element, write_multimodel_xml,
    build_linkmodel_element, write_linkmodel_xml
)

def ensure_output_dirs():
    """
    Ensures that OUTPUT_DIR and OUTPUT_DIR/models exist.
    """
    models_dir = os.path.join(OUTPUT_DIR, "models")
    os.makedirs(models_dir, exist_ok=True)
    return models_dir

def copy_input_files(models_dir):
    """
    Copy BIM_INPUT and GIS_INPUT into models_dir.
    Returns filenames (without path).
    """
    bim_filename = os.path.basename(BIM_INPUT)
    gis_filename = os.path.basename(GIS_INPUT)
    shutil.copy(BIM_INPUT, os.path.join(models_dir, bim_filename))
    shutil.copy(GIS_INPUT, os.path.join(models_dir, gis_filename))
    return bim_filename, gis_filename

def create_mmc_container():
    # Prepare folders
    models_dir = ensure_output_dirs()

    # Copy files in the folder
    bim_filename, gis_filename = copy_input_files(models_dir)

    # Gather Metadata
    # BIM Metadata
    bim_format_version = get_ifc_schema_version(os.path.join(models_dir, bim_filename))
    bim_info = {
        "filename": bim_filename,
        "model_type": "Building Model",
        "format_type": "IFC",
        "format_version": bim_format_version,
        "crs": None         # Since IFC doesn’t have “CRS” the same way GeoJSON does
    }

    # GIS Metadata
    gis_crs = get_geojson_crs(os.path.join(models_dir, gis_filename))
    gis_info = {
        "filename": gis_filename,
        "model_type": "GeoData",
        "format_type": "GeoJSON",
        "format_version": "1.0",
        "crs": gis_crs
    }

    # Build and write MultiModel.xml
    mm_element, ids = build_multimodel_element(bim_info, gis_info)
    mm_path = os.path.join(OUTPUT_DIR, "MultiModel.xml")
    write_multimodel_xml(mm_element, mm_path)
    print(f"MultiModel.xml written to {mm_path}")


    # Get IFC outerPose dictionary
    ifc_path = os.path.join(models_dir, bim_filename)
    pose_dict = get_ifc_outerpose(ifc_path)

    # Build and write LinkModel.xml
    lm_element = build_linkmodel_element(ids["bim"], ids.get("gis"), pose_dict=pose_dict)
    lm_path = os.path.join(OUTPUT_DIR, "LinkModel.xml")
    write_linkmodel_xml(lm_element, lm_path)
    print(f"LinkModel.xml written to {lm_path}")

    # Package everything into a .mmc
    with zipfile.ZipFile(MMC_ARCHIVE, 'w') as zipf:
        for dirpath, _, filenames in os.walk(OUTPUT_DIR):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                rel = os.path.relpath(full_path, OUTPUT_DIR)
                zipf.write(full_path, arcname=os.path.join("mmc", rel))
    print(f"MMC container created: {MMC_ARCHIVE}")


if __name__ == "__main__":
    create_mmc_container()
