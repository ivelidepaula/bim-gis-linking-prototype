import ifcopenshell
import os

# location
file_path = os.path.join("..", "input", "ifc", "Ifc4_SampleHouse.ifc")

# Open IFC file
model = ifcopenshell.open(file_path)
print("Schema:", model.schema)

# Site info
site = model.by_type("IfcSite")[0]
print("\nLatitude:", site.RefLatitude)
print("Longitude:", site.RefLongitude)
print("Elevation:", site.RefElevation)

# Map conversion
map_conversion = model.by_type("IfcMapConversion")
print(map_conversion)
if map_conversion:
    mc = map_conversion[0]
    print("\nEastings:", mc.Eastings)
    print("Northings:", mc.Northings)
    print("Scale:", mc.Scale)
else:
    print("\nNo IfcMapConversion found")

# TODO: parse metadata?

# TODO: parse globalID