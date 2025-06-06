# BIM-GIS MMC Container Prototype

## Overview
This project produces an MMC container (`.mmc`) linking one IFC (BIM) model and one GeoJSON (GIS) model, using a geometrical link, as proposed by Krischner et al (2025). 
It dynamically extracts metadata from the source files and builds the required `MultiModel.xml` and `LinkModel.xml` according to the DIN 18290-1.

## Repository Structure


3. Output `.mmc` archive appears at `../output/my_container.mmc`.

## Code Organization
- **config.py**: All paths, URNs, and version flags.  
- **parse_bim.py**: Extracts IFC schema & geolocation.  
- **parse_gis.py**: Extracts GeoJSON CRS & feature info.  
- **xml_builder.py**: Builds and writes `MultiModel.xml` and `LinkModel.xml` elements.  
- **main.py**: Orchestrates folder creation, file copying, parsing, XML building, and final zipping.

## Extending the Prototype
- To add **topological** or **geometric** links, modify `xml_builder.build_linkmodel_element(...)`.  
- To support new file formats (e.g., Shapefile), update `get_model_info()` in `parse_bim.py` or create new parsing functions.


Original inspiration for this project come from:

> Krischler, J., Schuler, P. C., Taraben, J., & Koch, C. (2024).  
> *Using ICDD for BIM and GIS Integration in Infrastructure*.  
> LDAC2024 – Linked Data in Architecture and Construction Workshop.

> Krischler, J., Schilling, S., Taraben, J., Sternal, M., Koch, C., & Clemen, C. (2025).  
> *A Standards-Based Approach to BIM-GIS Integration: Extending the Multi-Model Container Schema*.  
> LDAC2025 – Linked Data in Architecture and Construction Workshop.
