---
file_format: mystnb
---

# How to convert OFDS data to GeoJSON format

+++{"tags": ["remove-cell"]}
## Setup

To run the commands in this notebook, you'll need to install [GDAL](https://gdal.org/en/stable/index.html) and [jq](https://jqlang.org/), and run the following cell to install Python dependencies:

+++

```{code-cell}
---
tags: [remove-cell, skip-execution]
---

!pip install folium

```

OFDS does not define a schema for GeoJSON data. However, OFDS can be converted to GeoJSON format using standard conversion tools and libraries.

This page demonstrates how to convert OFDS to GeoJSON format using:

* ogr2ogr (command-line interface)
* QGIS (GIS software)
* GeoPandas (Python library)

```{tip}
Download this page as an executable Jupyter Notebook:  {nb-download}`geojson.ipynb`.
```

The OFDS data model includes both spatial entities (represented in GeoJSON as features with an associated geometry) and non-spatial entities, with no associated geometry.

When converting data to GeoJSON format, you can either convert both spatial and non-spatial layers to GeoJSON format, or you can convert only spatial layers and keep or export non-spatial layers in a format more suited to tabular data, like CSV.

The OFDS data model also includes both one-to-many relationships and many-to-many relationships between layers. These relationships are represented as foreign-key relationships (in GeoPackage data) or identifier references (in JSON and CSV). You might wish to dereference some of these relationships before exporting your data to GeoJSON format so that attributes belonging to the referenced entities are included in the properties of features in your GeoJSON data.

## ogr2ogr

[`ogr2ogr`](https://gdal.org/en/stable/programs/ogr2ogr.html) is a command-line tool that can be used to convert geospatial data between file formats.

### GeoPackage to GeoJSON conversion using ogr2ogr 

An [OFDS GeoPackage](../../reference/publication_formats/geopackage/index.md) contains many layers (tables). To convert a specific layer to GeoJSON format, use the following command:

`ogr2ogr -f GeoJSON path/to/output.json path/to/input.gpkg layer_name`

#### Convert a spatial layer to GeoJSON

For example, to convert the `nodes` layer to GeoJSON format: 

```{code-cell}
%%bash

ogr2ogr -f GeoJSON  nodes.geojson /vsicurl/https://standard.ofds.info/en/298-remove-geojson/network.gpkg nodes
```

```{note}
The above command uses the [vsicurl](https://gdal.org/en/stable/user/virtual_file_systems.html#vsicurl-http-https-ftp-files-random-access) network-based file system handler to connect to the example OFDS GeoPackage.
```

View the GeoJSON data:


```{code-cell}
---
mystnb:
  scroll_outputs: True
---
cat nodes.geojson | jq .
```

Visualise the GeoJSON data using [Folium](https://python-visualization.github.io/folium/latest/index.html):


```{code-cell}
import folium

with open('nodes.geojson', 'r') as f:
    data = f.read()

m = folium.Map(location=[6.4363794,-1.547332], zoom_start=8)

popup = folium.GeoJsonPopup(fields=["name", "status", "accessPoint", "power"])

folium.GeoJson(data, popup=popup).add_to(m)

m
```

```{seealso}
To learn how to visualise OFDS JSON data in Folium (Leaflet), see the [Leaflet example](leaflet).
```

#### Dereference a one-to-many relationship

For example, to dereference `nodes.physicalInfrastructureProvider`: 

```{code-cell}
%%bash

ogr2ogr -f GeoJSON nodes_dereferenced.geojson /vsicurl/https://standard.ofds.info/en/298-remove-geojson/network.gpkg \
  -sql "SELECT n.*, o.name AS physicalInfrastructureProvider_name \
        FROM nodes n \
        LEFT JOIN organisations o ON n.physicalInfrastructureProvider = o.id"
```

View the GeoJSON data, note that the feature's properties now include the physical infrastructure provider's name (`physicalInfrastructureProvider_name`):


```{code-cell}
---
mystnb:
  scroll_outputs: True
---
cat nodes_dereferenced.geojson | jq .
```

Visualise the GeoJSON data, including the physical infrastructure provider's name in a popup:

```{code-cell}
import folium

with open('nodes_dereferenced.geojson', 'r') as f:
    data = f.read()

m = folium.Map(location=[6.4363794,-1.547332], zoom_start=8)

popup = folium.GeoJsonPopup(fields=["physicalInfrastructureProvider_name"])

folium.GeoJson(data, popup=popup).add_to(m)

m
```

#### Dereference a many-to-many relationship

TO DO