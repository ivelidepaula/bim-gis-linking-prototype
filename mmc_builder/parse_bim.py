import ifcopenshell
from mmc_builder.config import BIM_INPUT
import math

def get_ifc_schema_version(ifc_path=None):
    """
    Open the IFC file at `ifc_path` (defaults to BIM_INPUT) and return its schema version,
    for example "IFC4" or "IFC2X3". Raises an exception if the file cannot be opened.
    """
    path = ifc_path or BIM_INPUT
    model = ifcopenshell.open(path)
    return model.schema

def get_site_info(ifc_path=None):
    """
    Returns a tuple (latitude, longitude, elevation) extracted from the first IfcSite in the model.
    Raises ValueError if no IfcSite is found.
    """
    path = ifc_path or BIM_INPUT
    model = ifcopenshell.open(path)
    sites = model.by_type("IfcSite")
    if not sites:
        raise ValueError(f"No IfcSite found in {path}")
    site = sites[0]
    return site.RefLatitude, site.RefLongitude, site.RefElevation

def get_map_conversion(ifc_path=None):
    """
    Returns a dictionary of IfcMapConversion parameters if present; otherwise returns None.
    Example return value:
      {
        "Eastings": ...,
        "Northings": ...,
        "Scale": ...,
        "XAxisAbscissa": ...,
        "XAxisOrdinate": ...,
        "YAxisAbscissa": ...,
        "YAxisOrdinate": ...
      }
    Raises no exception if none exist; simply returns None.
    """
    path = ifc_path or BIM_INPUT
    model = ifcopenshell.open(path)
    conversions = model.by_type("IfcMapConversion")
    if not conversions:
        return None

    mc = conversions[0]
    return {
        "Eastings": mc.Eastings,
        "Northings": mc.Northings,
        "Scale": mc.Scale,
        "XAxisAbscissa": mc.XAxisAbscissa,
        "XAxisOrdinate": mc.XAxisOrdinate,
        "YAxisAbscissa": mc.YAxisAbscissa,
        "YAxisOrdinate": mc.YAxisOrdinate
    }

def get_ifc_outerpose(ifc_path=None):
    """
    Returns a dict with keys:
      - "origin": Tuple[float, float, float]
      - "x_axis": Tuple[float, float, float]
      - "z_axis": Tuple[float, float, float]
      - "scale":  Tuple[float, float, float]

    If an IfcMapConversion is present, uses its Eastings/Northings/OrthogonalHeight,
    ScaleX/ScaleY/ScaleZ, and RotationInPlane to build those four tuples. Otherwise
    falls back to the first IfcSite: (lon, lat, elev) and uses identity axes+scale.
    """
    path = ifc_path or BIM_INPUT
    model = ifcopenshell.open(path)

    # Try to read an IfcMapConversion
    conversions = model.by_type("IfcMapConversion")
    if conversions:
        mc = conversions[0]

        # Translation = (Eastings, Northings, OrthogonalHeight)
        tx = mc.Eastings or 0.0
        ty = mc.Northings or 0.0
        tz = mc.OrthogonalHeight or 0.0

        # Scale factors (ScaleX, ScaleY, ScaleZ). Some IFCs only define Scale (uniform),
        # but if ScaleX/Y/Z exist, use them; otherwise fall back to mc.Scale for all three.
        sx = getattr(mc, "ScaleX", None) or (mc.Scale or 1.0)
        sy = getattr(mc, "ScaleY", None) or (mc.Scale or 1.0)
        sz = getattr(mc, "ScaleZ", None) or (mc.Scale or 1.0)

        # RotationInPlane is in degrees around the global Z axis
        rotation_deg = getattr(mc, "RotationInPlane", 0.0) or 0.0
        rotation_rad = math.radians(rotation_deg)

        # Compute rotated X-axis from unit X=(1,0,0) by angle θ:
        x1 = math.cos(rotation_rad)
        x2 = math.sin(rotation_rad)
        x3 = 0.0

        # Z axis is usually (0,0,1) if there is no tilt in IFC
        z1, z2, z3 = (0.0, 0.0, 1.0)

        return {
            "origin": (tx, ty, tz),
            "x_axis": (x1, x2, x3),
            "z_axis": (z1, z2, z3),
            "scale":  (sx, sy, sz)
        }

    # Fallback: read first IfcSite
    sites = model.by_type("IfcSite")
    if sites:
        site = sites[0]

        # Convert DMS→decimal degrees, if needed
        def dms_to_dec(dms_list):
            if not dms_list:
                return 0.0
            deg, minute, sec, _ = dms_list
            return deg + minute / 60.0 + sec / 3600.0

        lat = dms_to_dec(site.RefLatitude) if hasattr(site, "RefLatitude") else 0.0
        lon = dms_to_dec(site.RefLongitude) if hasattr(site, "RefLongitude") else 0.0
        elev = site.RefElevation or 0.0

        # Assuming EPSG:4326.
        return {
            "origin": (lon, lat, elev),
            "x_axis": (1.0, 0.0, 0.0),
            "z_axis": (0.0, 0.0, 1.0),
            "scale":  (1.0, 1.0, 1.0)
        }

    # No MapConversion or Site = default identity
    return {
        "origin": (0.0, 0.0, 0.0),
        "x_axis": (1.0, 0.0, 0.0),
        "z_axis": (0.0, 0.0, 1.0),
        "scale":  (1.0, 1.0, 1.0)
    }
