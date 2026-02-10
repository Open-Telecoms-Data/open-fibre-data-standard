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

ogr2ogr -f GeoJSON  nodes.geojson network-simple.gpkg nodes
```

View the GeoJSON data, using [jq](https://jqlang.org/) to filter out properties with `null` values, for brevity: 


```{code-cell}
---
mystnb:
  scroll_outputs: True
---
cat nodes.geojson | jq 'del(..|nulls)'
```

Visualise the GeoJSON data using [Folium](https://python-visualization.github.io/folium/latest/index.html), with property values in a popup:


```{code-cell}
import folium

with open('nodes.geojson', 'r') as f:
    data = f.read()

m = folium.Map(location=[5.625,-0.174], zoom_start=12)

popup = folium.GeoJsonPopup(fields=["name", "status"])

folium.GeoJson(data, popup=popup).add_to(m)

m
```

```{seealso}
To learn how to visualise OFDS JSON data in Folium (Leaflet), see the [Leaflet example](leaflet).
```

#### Dereference a one-to-many relationship

A GeoPackage is a SQLite database, so you can use ogr2ogr's [`-sql` option](https://gdal.org/en/stable/programs/ogr2ogr.html#cmdoption-ogr2ogr-sql) to join data from separate tables into a single record.

For example, `nodes.phase` is a foreign key to the `phases` table. To dereference it, you can use the following SQL statement:

```sql
SELECT 
    nodes.*, 
    phases.name AS phase_name 
FROM nodes 
LEFT JOIN phases 
    ON nodes.phase = phases.id
```

Pass the SQL statement to the `-sql` option of `ogr2ogr`:

```{code-cell}
%%bash

ogr2ogr -f GeoJSON nodes_dereferenced.geojson network-simple.gpkg \
  -sql "SELECT \
            nodes.*, \
            phases.name AS phase_name \
        FROM nodes \
        LEFT JOIN phases \
            ON nodes.phase = phases.id"
```

View the GeoJSON data, noting that the feature's properties now include the transmission medium owner's name in `phase_name`:

```{code-cell}
---
mystnb:
  scroll_outputs: True
---
cat nodes_dereferenced.geojson | jq 'del(..|nulls)'
```

Visualise the GeoJSON data, including the phase name in a popup:

```{code-cell}
import folium

with open('nodes_dereferenced.geojson', 'r') as f:
    data = f.read()

m = folium.Map(location=[5.625,-0.174], zoom_start=12)

popup = folium.GeoJsonPopup(fields=["phase_name"])

folium.GeoJson(data, popup=popup).add_to(m)

m
```

#### Dereference a many-to-many relationship

In an OFDS GeoPackage, many-to-many relationships, such as a node having multiple network providers, are represented as join tables (e.g., `relation_nodes_networkProviders`). 

If you use a standard `JOIN`, the output will contain duplicate features for every relationship. To keep your GeoJSON clean, you can use the SQLite `GROUP_CONCAT` function to merge these related values into a single property.

For example, to dereference `nodes.networkProviders`, you can use the following SQL statement:

```sql
SELECT 
    nodes.*, 
    GROUP_CONCAT(organisations.name, ', ') AS networkProvider_names 
FROM nodes 
LEFT JOIN relation_nodes_networkProviders r 
    ON nodes.id = r.base_id 
LEFT JOIN organisations 
    ON r.related_id = organisations.id 
GROUP BY nodes.id
```

Pass the SQL statement to the `-sql` option of `ogr2ogr`:

```{code-cell}
%%bash

ogr2ogr -f GeoJSON nodes_multi_provider.geojson network-simple.gpkg \
  -sql "SELECT \
            nodes.*, \
            GROUP_CONCAT(organisations.name, ', ') AS networkProvider_names \
        FROM nodes \
        LEFT JOIN relation_nodes_networkProviders r \
            ON nodes.id = r.base_id \
        LEFT JOIN organisations \
            ON r.related_id = organisations.id \
        GROUP BY nodes.id"
```

View the GeoJSON data, noting that multiple provider names are now combined into the `networkProvider_names` property:

```{code-cell}
---
mystnb:
  scroll_outputs: True
---
cat nodes_multi_provider.geojson | jq 'del(..|nulls)'
```

### CSV to GeoJSON conversion using ogr2ogr

[OFDS CSV data](../../reference/publication_formats/csv.md) consists of multiple tables and follows a flattened structure where column headers represent nested paths (e.g. `nodes/0/address/streetAddress`).

Node locations and span routes are represented as Well-Known Text (WKT) geometries, in `nodes/0/location` and `spans/0/route`, respectively.

To convert a spatial layer, you need to tell `ogr2ogr` which column contains the geometry, and specify the spatial reference system, using the following command:

`ogr2ogr -f GeoJSON path/to/output.geojson path/to/input.csv -oo GEOM_POSSIBLE_NAMES="geometry/column/name" -oo KEEP_GEOM_COLUMNS=NO -a_srs EPSG:4326`

#### Convert a spatial CSV to GeoJSON

For example, to convert `nodes.csv`, use the `GEOM_POSSIBLE_NAMES` option to point to the `nodes/0/location` column.

```{code-cell}
%%bash
ogr2ogr -f GeoJSON nodes_from_csv.geojson nodes.csv\
  -oo GEOM_POSSIBLE_NAMES="nodes/0/location"\
  -oo KEEP_GEOM_COLUMNS=NO\
  -a_srs EPSG:4326
```

View the GeoJSON data, using [jq](https://jqlang.org/) to format the output:

```{code-cell}
---
mystnb:
  scroll_outputs: True
---
cat nodes_from_csv.geojson | jq .
```

Visualise the GeoJSON data using [Folium](https://python-visualization.github.io/folium/latest/index.html):


```{code-cell}
import folium

with open('nodes_from_csv.geojson', 'r') as f:
    data = f.read()

m = folium.Map(location=[5.625,-0.174], zoom_start=12)

popup = folium.GeoJsonPopup(fields=["nodes/0/name", "nodes/0/status"],
                            aliases=["Name", "Status"])

folium.GeoJson(data, popup=popup).add_to(m)

m
```

```{seealso}
To learn how to visualise OFDS JSON data in Folium (Leaflet), see the [Leaflet example](leaflet).
```

#### Dereference a one-to-many relationship

Joining CSV files requires using the **SQLite dialect** in `ogr2ogr`. This allows you to treat the CSV files as tables in a virtual database. Note that the headers in the SQL statement must match the CSV headers exactly, requiring double quotes for paths containing slashes.

Also, when using the SQLite dialect with CSV files, the spatial column is treated as a text string. To ensure the output GeoJSON has a valid geometry, you need to use the `ST_GeomFromText()` function to convert the WKT string into a geometry object.

For example, `nodes/0/phase/id` is a foreign key to the `phases` table. To dereference it, you can use the following SQL statement:

```sql
SELECT 
    ST_GeomFromText("nodes/0/location") AS geometry, 
    n.*, 
    p.'phases/0/description' as phase_description
FROM 
    'nodes.csv'.nodes n
LEFT JOIN 
    'phases.csv'.phases p
    ON n.'nodes/0/phase/id' = p.'phases/0/id'
```

Pass the SQL statement to the `-sql` option of `ogr2ogr`, with `-dialect` set to `SQLite`:

```{code-cell}
%%bash
ogr2ogr -f GeoJSON nodes_csv_dereferenced.geojson nodes.csv \
  -dialect SQLite \
  -sql "SELECT 
            ST_GeomFromText(\"nodes/0/location\") AS geometry, 
            n.*, 
            p.\"phases/0/description\" AS phase_description 
        FROM \"nodes.csv\".nodes n 
        LEFT JOIN \"phases.csv\".phases p 
            ON n.\"nodes/0/phase/id\" = p.\"phases/0/id\"" \
  -a_srs EPSG:4326

```

View the GeoJSON data:

```{code-cell}
---
mystnb:
  scroll_outputs: True
---
cat nodes_csv_dereferenced.geojson | jq .
```

Visualise the GeoJSON data, including the phase description in a popup:

```{code-cell}
import folium

with open('nodes_csv_dereferenced.geojson', 'r') as f:
    data = f.read()

m = folium.Map(location=[5.625,-0.174], zoom_start=12)

popup = folium.GeoJsonPopup(fields=["phase_description"])

folium.GeoJson(data, popup=popup).add_to(m)

m
```

#### Dereference a many-to-many relationship

For many-to-many relationships (like a node's network providers), you can join the base CSV with the join table CSV (e.g. nodes_networkProviders) and the related CSV (e.g. organisations).

For example, in `nodes_networkProviders.csv`, `nodes/0/id` is a foreign key to `nodes.csv`, and `nodes/0/networkProviders/0/id` is a foreign key to `organisations.csv` table.

`nodes_networkProviders.csv` is partially dereferenced (it already contains the organisation's name), but to dereference other fields from `organisations.csv`, like `organisations/0/website`, you can use the following SQL statement:

```sql
SELECT
    ST_GeomFromText(n."nodes/0/location") AS geometry,
    n.*,
    GROUP_CONCAT(o."organisations/0/website", ", ") AS networkProvider_websites
FROM "nodes.csv".nodes n
LEFT JOIN "nodes_networkProviders.csv"."nodes_networkProviders" nnp
    ON n."nodes/0/id" = nnp."nodes/0/id"
LEFT JOIN "organisations.csv".organisations o
    ON nnp."nodes/0/networkProviders/0/id" = o."organisations/0/id"
GROUP BY 
    n."nodes/0/id";
```

Pass the SQL statement to the `-sql` option of `ogr2ogr`, with `-dialect` set to `SQLite`:

```{code-cell}
%%bash
ogr2ogr -f GeoJSON nodes_csv_multi_provider.geojson nodes.csv\
  -dialect SQLite\
  -sql "SELECT\
            ST_GeomFromText(\"nodes/0/location\") AS geometry, 
            n.*,\
            GROUP_CONCAT(o.'organisations/0/website', ', ') AS networkProvider_websites\
        FROM 'nodes.csv'.nodes n\
        LEFT JOIN 'nodes_networkProviders.csv'.'nodes_networkProviders' nnp\
            ON n.'nodes/0/id' = nnp.'nodes/0/id'\
        LEFT JOIN 'organisations.csv'.organisations o\
            ON nnp.'nodes/0/networkProviders/0/id' = o.'organisations/0/id'\
        GROUP BY n.'nodes/0/id'"\
  -a_srs EPSG:4326

```

View the result to confirm the network provider's websites are concatenated:

```{code-cell}
---
mystnb:
  scroll_outputs: True
---
cat nodes_csv_multi_provider.geojson | jq .

```