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

shutil.rmtree('_nb', ignore_errors=True)
os.makedirs('_nb', exist_ok=True)

BASE_URL = 'https://raw.githubusercontent.com/Open-Telecoms-Data/open-fibre-data-standard/298-geojson-guidance'

def get_file(repo_path, dest=None):
    dest_name = dest or os.path.basename(repo_path)
    local = f'../../../{repo_path}'
    if os.path.exists(local):
        shutil.copy(local, f'_nb/{dest_name}')
    else:
        urllib.request.urlretrieve(f'{BASE_URL}/{repo_path}', f'_nb/{dest_name}')

get_file('examples/json/network-package.json', 'network-package.json')

os.chdir('_nb')
```

This page shows how to write custom SQL or Python to dereference relationships in an OFDS dataset and export it as GeoJSON, when the [pre-built scripts](../prebuilt/index.md) don't cover your exact requirements. You can either use this guidance as a starting point for adapting the pre-built scripts to meet your needs, or you can author your own scripts from scratch.

All examples on this page use the `nodes` layer, but the same approaches apply equally to `spans`.

## GeoPackage

A GeoPackage is a SQLite database, so you can use a SQL query to build a table suitable for export in GeoJSON format. This section describes how to write SQL queries to dereference relationships in a GeoPackage.

```{seealso}
To learn how to execute SQL queries against an OFDS GeoPackage and export the output to GeoJSON, see the tool-specific guidance in the [pre-built scripts](../prebuilt/index.md) section for:

* [QGIS](../prebuilt/index.md#qgis)
* [ogr2ogr](../prebuilt/index.md#ogr2ogr)
* [GeoPandas](../prebuilt/index.md#geopandas)
```

### Dereference a one-to-many relationship

[One-to-many relationships](../../../reference/data_formats/geopackage/index.md#one-to-many-relationships) are modelled as [foreign key relationships](https://en.wikipedia.org/wiki/Foreign_key), which link related tables. For example, `nodes.phase` is a foreign key to the `phases` table.

To dereference a one-to-many relationship, join the two tables and select the desired fields from each:

```{literalinclude} one_to_many_example_gpkg.sql
:language: sql
```

```{note}
Fields that reference an open [codelist](../../../reference/codelists.md) (e.g. `nodes.supportingInfrastructure__type`) are also modelled as foreign keys, with the codelist values stored in a codelist table (e.g. `codelist_open_nodeSupportingInfrastructure`). So the same approach applies to dereferencing these fields to obtain human-readable values instead of identifiers.
```

### Dereference a many-to-many relationship

[Many-to-many relationships](../../../reference/data_formats/geopackage/index.md#many-to-many-relationships) are modelled as [associative tables](https://en.wikipedia.org/wiki/Associative_entity), which link a base table and a related table. For example, the `relation_nodes_networkProviders` table associates nodes in the `nodes` table with network providers in the `organisations` table.

To dereference many-to-many relationship:

- join the base table to the associative table, and the associative table to the related table
- select the desired fields from the base and related tables
- decide how to merge or aggregate the values of selected fields from the related table.

The example below dereferences the relationship between `nodes` and `organisations`, and uses `GROUP_CONCAT` to merge network provider names into a comma-separated string:

```{literalinclude} many_to_many_example_gpkg.sql
:language: sql
```

```{note}
Fields that reference a [codelist](../../../reference/codelists.md) and allow multiple values (e.g. `nodes/0/type`) are also modelled as many-to-many relationships, with the codelist values stored in a codelist table (e.g. `codelist_open_nodeType`) and linked via an associative table (e.g. `relation_nodes_type`). So the same approach applies to dereferencing these fields to obtain human-readable values instead of identifiers.
```

## CSV

The OFDS CSV format consists of multiple CSV files. This section describes how to write SQL queries to dereference relationships between the CSV files. The queries are intended for use with ogr2ogr's SQLite dialect, which treats CSV files as tables in a virtual database.

```{seealso}
To learn how to use ogr2ogr to execute a SQL query against OFDS CSV files and export the output to GeoJSON, see [CSV > ogr2ogr](../prebuilt/index.md#ogr2ogr-1) in the [pre-built scripts](../prebuilt/index.md) section
```

Node locations and span routes are represented as WKT strings in the `nodes/0/location` and `spans/0/route` columns of the `nodes.csv` and `spans.csv` files respectively. To convert these to GeoJSON geometries, use the `ST_GeomFromText` function in your SQL query.

When authoring a SQL query for use with ogr2ogr's SQLite dialect, column names must match the CSV headers exactly, using double quotes for paths containing slashes. For example, the `nodes/0/location` column must be referenced in SQL as `"nodes/0/location"`.

The [CSV format reference documentation](../../../reference/data_formats/csv.md) lists the relationships between the tables in the CSV format.

### Dereference a one-to-many relationship

One-to-many relationships are modelled as references to identifiers in other tables. To dereference a one-to-many relationship, join the two tables and select the desired fields from each.

For example, the `nodes/0/phase/id` column in the `nodes` table references the `phases/0/id` column in the `phases` table. To dereference this relationship, join `nodes.csv` with `phases.csv` on these columns, and select the desired fields from each table:

```{literalinclude} one_to_many_example_csv.sql
:language: sql
```

### Dereference a many-to-many relationship

One-to-many relationships are modelled as separate CSV files linking identifiers in the base and related tables. To dereference a many-to-many relationship:

- join the base table to the associative table, and the associative table to the related table
- select the desired fields from the base and related tables
- decide how to merge or aggregate the values of selected fields from the related table.

For example, the `nodes_networkProviders.csv` file links nodes to their network providers in the `organisations.csv` file. To dereference this relationship, join `nodes.csv` with `nodes_networkProviders.csv` on `nodes/0/id` and join `nodes_networkProviders.csv` with `organisations.csv` on `nodes/0/networkProviders/0/id` and `organisations/0/id`. This example uses `GROUP_CONCAT` to merge multiple network provider websites into a comma-separated string, but you could select different fields or use a different aggregation method depending on your needs.

```{literalinclude} many_to_many_example_csv.sql
:language: sql

```

## JSON

OFDS JSON data is already partly dereferenced. However, some properties are modelled as [`OrganisationReference`](../../../reference/data_formats/json/network_schema.md#organisationreference) and [`PhaseReference`](../../../reference/data_formats/json/network_schema.md#phasereference) objects, which refer to the identifiers of objects in the `organisations` and `phases` arrays respectively. For convenience, these objects include both the `id` and `name` of the referenced object, but you may want to dereference other properties.

To dereference these properties, you can write a Python script to load the JSON data, look up the referenced objects in the `organisations` and `phases` arrays, and construct a GeoDataFrame for export to GeoJSON format. The example below:

- maps the name of the phase to which a node belongs from `.phase.name` to `.phase_name`
- dereferences the phase identifier referenced in `.phase.id` and returns the `.description` of the referenced phase
- joins the names of the node's network providers from `.networkProviders.name` into a single comma-separated string in `.networkProvider_names`
- dereferences the organisation identifiers referenced in `.networkProviders.id` and joins the websites of the referenced organisations into a single comma-separated string in `.networkProvider_websites`.

```{code-cell}
import json
import geopandas as gpd
from shapely.geometry import shape

with open('network-package.json') as f:
    data = json.load(f)

rows = []
for network in data['networks']:
    phases = {phase['id']: phase for phase in network.get('phases', [])}
    organisations = {org['id']: org for org in network.get('organisations', [])}

    for node in network.get('nodes', []):
        rows.append({
            'geometry': shape(node['location']),
            'name': node.get('name'),
            'status': node.get('status'),
            'phase_name': node.get('phase', {}).get('name'),
            'phase_description': phases.get(node.get('phase',{}).get('id'), {}).get('description'),
            'networkProvider_names': ', '.join([ref.get('name') for ref in node.get('networkProviders', [])]),
            'networkProvider_websites': ', '.join([organisations.get(ref.get('id'), {}).get('website') for ref in node.get('networkProviders', [])])
        })

gdf = gpd.GeoDataFrame(rows, crs='EPSG:4326')
gdf.to_file('json_nodes_example.geojson', driver='GeoJSON')
```

View `json_nodes_example.geojson`, using [jq](https://jqlang.org/) to filter out properties with `null` values:

```{code-cell}
---
mystnb:
  scroll_outputs: True
---
cat json_nodes_example.geojson | jq 'del(..|nulls)'
```