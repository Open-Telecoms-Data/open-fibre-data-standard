---
file_format: mystnb
---

# Writing a custom query

```{code-cell}
---
tags: [remove-cell, skip-execution]
---

!pip install folium geopandas

```

```{code-cell}
---
tags: [remove-cell]
---
import os, shutil, urllib.request

os.makedirs('_nb', exist_ok=True)

BASE_URL = 'https://raw.githubusercontent.com/Open-Telecoms-Data/open-fibre-data-standard/298-geojson-guidance'

def get_file(repo_path, dest=None):
    dest_name = dest or os.path.basename(repo_path)
    local = f'../../../{repo_path}'
    if os.path.exists(local):
        shutil.copy(local, f'_nb/{dest_name}')
    else:
        urllib.request.urlretrieve(f'{BASE_URL}/{repo_path}', f'_nb/{dest_name}')

for f in ['network-simple.gpkg', 'nodes.csv', 'nodes_networkProviders.csv', 'phases.csv', 'organisations.csv']:
    get_file(f'docs/guidance/use/{f}')

os.chdir('_nb')
```

The following examples show how to write custom SQL or Python to dereference specific relationships in an OFDS dataset. Use these as a starting point when the [pre-built scripts](geojson-prebuilt.md) don't cover your exact requirements — for example, if you need to select a specific subset of fields, apply filters, or join to tables not covered by the pre-built scripts.

All examples use the `nodes` layer, but the same approaches apply equally to `spans`.

## GeoPackage

A GeoPackage is a SQLite database, so you can use ogr2ogr's [`-sql` option](https://gdal.org/en/stable/programs/ogr2ogr.html#cmdoption-ogr2ogr-sql) to join data from separate tables into a single record.

### ogr2ogr

#### Dereference a one-to-many relationship

`nodes.phase` is a foreign key to the `phases` table. To dereference it:

```sql
SELECT
    nodes.*,
    phases.name AS phase_name
FROM nodes
LEFT JOIN phases ON nodes.phase = phases.id
```

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

```{code-cell}
---
mystnb:
  scroll_outputs: True
---
cat nodes_dereferenced.geojson | jq 'del(..|nulls)'
```

#### Dereference a many-to-many relationship

Many-to-many relationships are stored in join tables (e.g. `relation_nodes_networkProviders`). Use `GROUP_CONCAT` to merge related values into a single property:

```sql
SELECT
    nodes.*,
    GROUP_CONCAT(organisations.name, ', ') AS networkProvider_names
FROM nodes
LEFT JOIN relation_nodes_networkProviders r ON nodes.id = r.base_id
LEFT JOIN organisations ON r.related_id = organisations.id
GROUP BY nodes.id
```

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

```{code-cell}
---
mystnb:
  scroll_outputs: True
---
cat nodes_multi_provider.geojson | jq 'del(..|nulls)'
```

### GeoPandas

Pass any SQL query to `gpd.read_file` using the `sql` parameter:

```python
import geopandas as gpd

nodes = gpd.read_file('network.gpkg', sql="""
    SELECT nodes.*, phases.name AS phase_name
    FROM nodes
    LEFT JOIN phases ON nodes.phase = phases.id
""")
nodes.to_file('nodes.geojson', driver='GeoJSON')
```

### QGIS

Use **Database > DB Manager** to run custom SQL against the GeoPackage, as described in the [pre-built queries section](geojson-prebuilt.md#geopackage).

## CSV

Joining CSV files in ogr2ogr requires the **SQLite dialect**, which lets you treat CSV files as tables in a virtual database. Column names must match the CSV headers exactly, using double quotes for paths containing slashes. Use `ST_GeomFromText()` to convert the WKT geometry column.

### ogr2ogr

#### Dereference a one-to-many relationship

`nodes/0/phase/id` references the phases table. To join `nodes.csv` with `phases.csv`:

```sql
SELECT
    ST_GeomFromText("nodes/0/location") AS geometry,
    n.*,
    p."phases/0/description" AS phase_description
FROM "nodes.csv".nodes n
LEFT JOIN "phases.csv".phases p
    ON n."nodes/0/phase/id" = p."phases/0/id"
```

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

```{code-cell}
---
mystnb:
  scroll_outputs: True
---
cat nodes_csv_dereferenced.geojson | jq .
```

#### Dereference a many-to-many relationship

`nodes_networkProviders.csv` links nodes to their network providers. Use `GROUP_CONCAT` to combine multiple providers into a single property:

```sql
SELECT
    ST_GeomFromText(n."nodes/0/location") AS geometry,
    n.*,
    GROUP_CONCAT(o."organisations/0/website", ', ') AS networkProvider_websites
FROM "nodes.csv".nodes n
LEFT JOIN "nodes_networkProviders.csv"."nodes_networkProviders" nnp
    ON n."nodes/0/id" = nnp."nodes/0/id"
LEFT JOIN "organisations.csv".organisations o
    ON nnp."nodes/0/networkProviders/0/id" = o."organisations/0/id"
GROUP BY n."nodes/0/id"
```

```{code-cell}
%%bash
ogr2ogr -f GeoJSON nodes_csv_multi_provider.geojson nodes.csv \
  -dialect SQLite \
  -sql "SELECT \
            ST_GeomFromText(\"nodes/0/location\") AS geometry,
            n.*,\
            GROUP_CONCAT(o.'organisations/0/website', ', ') AS networkProvider_websites\
        FROM 'nodes.csv'.nodes n\
        LEFT JOIN 'nodes_networkProviders.csv'.'nodes_networkProviders' nnp\
            ON n.'nodes/0/id' = nnp.'nodes/0/id'\
        LEFT JOIN 'organisations.csv'.organisations o\
            ON nnp.'nodes/0/networkProviders/0/id' = o.'organisations/0/id'\
        GROUP BY n.'nodes/0/id'" \
  -a_srs EPSG:4326

```

```{code-cell}
---
mystnb:
  scroll_outputs: True
---
cat nodes_csv_multi_provider.geojson | jq .

```

### GeoPandas

This example joins nodes with the phases table to dereference the one-to-many `phase` relationship:

```python
import pandas as pd
import geopandas as gpd
from shapely import wkt

nodes = pd.read_csv('nodes.csv')
phases = pd.read_csv('phases.csv')

nodes = nodes.merge(
    phases[['phases/0/id', 'phases/0/description']],
    left_on='nodes/0/phase/id',
    right_on='phases/0/id',
    how='left'
)
nodes['geometry'] = nodes['nodes/0/location'].apply(wkt.loads)
gdf = gpd.GeoDataFrame(nodes, crs='EPSG:4326')
gdf.to_file('nodes.geojson', driver='GeoJSON')
```

## JSON

OFDS JSON data is already fully dereferenced, so custom queries are mainly about selecting or renaming fields. Use Python to load the JSON, transform properties as needed, and write to GeoJSON:

```python
import json
import geopandas as gpd
from shapely.geometry import shape

with open('network-package.json') as f:
    data = json.load(f)

rows = []
for network in data['networks']:
    for node in network.get('nodes', []):
        rows.append({
            'geometry': shape(node['location']),
            'name': node.get('name'),
            'status': node.get('status'),
            # add or remove fields as needed
        })

gdf = gpd.GeoDataFrame(rows, crs='EPSG:4326')
gdf.to_file('nodes.geojson', driver='GeoJSON')
```
