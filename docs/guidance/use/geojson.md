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

This page provides an [introduction](#introduction) to converting OFDS data to GeoJSON format, and demonstrates how to convert data using:

* [ogr2ogr (command-line interface)](#ogr2ogr)
* GeoPandas (Python library)
* QGIS (GIS software)

```{tip}
Download this page as an executable Jupyter Notebook:  {nb-download}`geojson.ipynb`.
```

## Introduction

The OFDS data model includes both **spatial entities** (represented in GeoJSON as features with an associated geometry) and **non-spatial entities**, which have no associated geometry. For example, nodes and spans are spatial entities and organisations are non-spatial entities.

When converting data to GeoJSON format, you can either:

* **Convert both spatial and non-spatial layers**: In this case, non-spatial layers appear as `FeatureCollection` objects where every feature has a `null` geometry.
* **Convert only spatial layers**: You can then keep or export non-spatial layers in a format more suited to non-spatial data, such as CSV or a standard JSON object.

### Relational data and dereferencing

The OFDS data model also includes one-to-many and many-to-many relationships between entities. These are represented as foreign-key relationships in GeoPackage data or identifier references in JSON and CSV data. 

Because GeoJSON is a "flat" format, you might want to **dereference** these relationships before converting your data to GeoJSON format. Dereferencing is the process of joining data from separate tables into a single record so that attributes from referenced entities (such as an organisation's name) are included directly in the properties of spatial features. 

This ensures that popups, labels, and map legends work immediately in GIS software and web maps without requiring additional lookups.

## ogr2ogr

[`ogr2ogr`](https://gdal.org/en/stable/programs/ogr2ogr.html) is a command-line tool that can be used to convert geospatial data between file formats.

### GeoPackage to GeoJSON conversion using ogr2ogr 

An [OFDS GeoPackage](../../reference/publication_formats/geopackage/index.md) contains many layers (tables). To convert a specific layer to GeoJSON format, use the following command:

`ogr2ogr -f GeoJSON path/to/output.json path/to/input.gpkg layer_name`

For a list of layer (table) names in an OFDS GeoPackage, refer to the [table definitions](../../reference/publication_formats/index.md#), or 
use GDAL's `ogrinfo` command:

`ogrinfo -al -so path/to/input.gpkg`

#### Convert a spatial layer to GeoJSON

For example, to convert the `nodes` layer to GeoJSON format: 

```{code-cell}
%%bash

ogr2ogr -f GeoJSON  nodes.geojson /vsicurl/https://standard.ofds.info/en/298-remove-geojson/geopackage/network.gpkg nodes
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

A GeoPackage is a SQLite database, so you can use ogr2ogr's [`-sql` option](https://gdal.org/en/stable/programs/ogr2ogr.html#cmdoption-ogr2ogr-sql) to join data from separate tables into a single record.

For example, to dereference `nodes.physicalInfrastructureProvider`, you can use the following SQL statement:

```sql
SELECT 
    nodes.*, 
    organisations.name AS physicalInfrastructureProvider_name 
FROM nodes 
LEFT JOIN organisations 
    ON nodes.physicalInfrastructureProvider = organisations.id
```

Pass the SQL statement to the `-sql` option of `ogr2ogr`:

```{code-cell}
%%bash

ogr2ogr -f GeoJSON nodes_dereferenced.geojson /vsicurl/https://standard.ofds.info/en/298-remove-geojson/geopackage/network.gpkg \
  -sql "SELECT \
          nodes.*, \
          organisations.name AS physicalInfrastructureProvider_name \
      FROM nodes \
      LEFT JOIN organisations \
          ON nodes.physicalInfrastructureProvider = organisations.id"
```

View the GeoJSON data, noting that the feature's properties now include the physical infrastructure provider's name (`physicalInfrastructureProvider_name`):

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

In an OFDS GeoPackage, many-to-many relationships, such as a node having multiple network providers, are represented as join tables (e.g., `relation_nodes_networkProviders`). 

If you use a standard `JOIN`, the output will contain duplicate features for every relationship. To keep your GeoJSON clean, you can use the SQLite `GROUP_CONCAT` function to merge these related values into a single property.

For example, to dereference `nodes.networkProviders`, you can use the following SQL statement:

```sql
SELECT 
    n.*, 
    GROUP_CONCAT(o.name, ', ') AS networkProvider_names 
FROM nodes n 
LEFT JOIN relation_nodes_networkProviders nnp 
    ON n.id = nnp.base_id 
LEFT JOIN organisations o 
    ON nnp.related_id = o.id 
GROUP BY n.id
```

Pass the SQL statement to the `-sql` option of `ogr2ogr`:

```{code-cell}
%%bash

ogr2ogr -f GeoJSON nodes_multi_provider.geojson /vsicurl/https://standard.ofds.info/en/298-remove-geojson/geopackage/network.gpkg \
  -sql "SELECT \
            n.*, \
            GROUP_CONCAT(o.name, ', ') AS networkProvider_names \
        FROM nodes n \
        LEFT JOIN relation_nodes_networkProviders nnp ON n.id = nnp.base_id \
        LEFT JOIN organisations o ON nnp.related_id = o.id \
        GROUP BY n.id"
```

View the GeoJSON data, noting that multiple provider names are now combined into the `networkProvider_names` property:

```{code-cell}
---
mystnb:
  scroll_outputs: True
---
cat nodes_multi_provider.geojson | jq .
```

