import xml.etree.ElementTree as ET
from mmc_builder.config import MMC_FORMAT_VERSION, MM_DOMAIN

def build_multimodel_element(bim_info, gis_info):
    """
    Given dictionaries:
      bim_info = {
        "filename": "Ifc4_SampleHouse.ifc",
        "model_type": "Building Model",
        "format_type": "IFC",
        "format_version": "IFC4",
        "crs": None  # not used for BIM
      }
      gis_info = {
        "filename": "landuse_residential_berlin.geojson",
        "model_type": "GeoData",
        "format_type": "GeoJSON",
        "format_version": "1.0",
        "crs": "EPSG:25833"
      }
    returns an <Element 'MultiModel'> tree root (not yet written to file).
    """
    mm = ET.Element("MultiModel", attrib={
        "formatVersion": MMC_FORMAT_VERSION,
        "mmDomain": MM_DOMAIN
    })

    # Helper to generate (IDs) for each application model
    def gen_ids(prefix):
        model_id = f"{prefix}01"
        return {
            "model_id": model_id,
            "model_data_id": f"{model_id}-md",
            "resource_id": f"{model_id}-dr"
        }

    # BIM entry
    bim_ids = gen_ids("bim")
    bim_app = ET.SubElement(
        mm,
        "ApplicationModel",
        attrib={
            "id": bim_ids["model_id"],
            "modelType": bim_info["model_type"]
        }
    )
    bim_data = ET.SubElement(bim_app, "ModelData", attrib={
        "id": bim_ids["model_data_id"],
        "formatType": bim_info["format_type"],
        "formatVersion": bim_info["format_version"]
    })
    ET.SubElement(bim_data, "DataResource", attrib={
        "id": bim_ids["resource_id"],
        "location": f"models/{bim_info['filename']}"
    })

    # GIS entry
    gis_ids = gen_ids("gis")
    gis_app = ET.SubElement(
        mm,
        "ApplicationModel",
        attrib={
            "id": gis_ids["model_id"],
            "modelType": gis_info["model_type"]
        }
    )
    gis_data = ET.SubElement(gis_app, "ModelData", attrib={
        "id": gis_ids["model_data_id"],
        "formatType": gis_info["format_type"],
        "formatVersion": gis_info["format_version"]
    })
    ET.SubElement(gis_data, "DataResource", attrib={
        "id": gis_ids["resource_id"],
        "location": f"models/{gis_info['filename']}"
    })
    if gis_info.get("crs"):
        ET.SubElement(gis_data, "Meta", attrib={
            "key": "CRS",
            "value": gis_info["crs"]
        })

    return mm, {"bim": bim_ids, "gis": gis_ids}

def write_multimodel_xml(mm_element, output_path):
    """
    Given an <Element 'MultiModel'> object, write it to the specified output_path
    (including XML declaration and UTF-8 encoding).
    """
    ET.ElementTree(mm_element).write(output_path, encoding="utf-8", xml_declaration=True)

def build_linkmodel_element(bim_ids, gis_ids=None, pose_dict=None):
    """
    Builds a <LinkModel> element with a single <Geospatial_Link>:
      - first <Relatum> is the container (modelId="mmc")
      - second <Relatum> is the BIM model (using bim_ids)
      - optional third <Relatum> is the GIS model (using gis_ids) if provided

    pose_dict should be:
      {
        "origin": (tx, ty, tz),
        "x_axis": (x1, x2, x3),
        "z_axis": (z1, z2, z3),
        "scale":  (sx, sy, sz)
      }
    If pose_dict is None, defaults to origin=(0,0,0), x_axis=(1,0,0), z_axis=(0,0,1), scale=(1,1,1).
    """
    lm = ET.Element("LinkModel", attrib={"formatVersion": MMC_FORMAT_VERSION})

    geo_link = ET.SubElement(lm, "Geospatial_Link", attrib={"type": "pose"})
    pose = ET.SubElement(geo_link, "outerPose")

    # Unpack real values if provided, otherwise use defaults
    if pose_dict:
        ox, oy, oz = pose_dict.get("origin", (0.0, 0.0, 0.0))
        x1, x2, x3 = pose_dict.get("x_axis", (1.0, 0.0, 0.0))
        z1, z2, z3 = pose_dict.get("z_axis", (0.0, 0.0, 1.0))
        sx, sy, sz = pose_dict.get("scale",  (1.0, 1.0, 1.0))
    else:
        ox, oy, oz = (0.0, 0.0, 0.0)
        x1, x2, x3 = (1.0, 0.0, 0.0)
        z1, z2, z3 = (0.0, 0.0, 1.0)
        sx, sy, sz = (1.0, 1.0, 1.0)

    ET.SubElement(pose, "origin").text = f"{ox},{oy},{oz}"
    ET.SubElement(pose, "x-axis").text = f"{x1},{x2},{x3}"
    ET.SubElement(pose, "z-axis").text = f"{z1},{z2},{z3}"
    ET.SubElement(pose, "scale").text = f"{sx},{sy},{sz}"

    # The Relatum elements remain unchanged
    ET.SubElement(geo_link, "Relatum", attrib={"modelId": "mmc"})
    ET.SubElement(geo_link, "Relatum", attrib={
        "modelId": bim_ids["model_id"],
        "formatId": bim_ids["model_data_id"],
        "resourceId": bim_ids["resource_id"]
    })

    if gis_ids:
        ET.SubElement(geo_link, "Relatum", attrib={
            "modelId": gis_ids["model_id"],
            "formatId": gis_ids["model_data_id"],
            "resourceId": gis_ids["resource_id"]
        })

    return lm

def write_linkmodel_xml(lm_element, output_path):
    """
    Given an <Element 'LinkModel'> object, write it to output_path.
    """
    ET.ElementTree(lm_element).write(output_path, encoding="utf-8", xml_declaration=True)
