---
file_format: mystnb
---

# Convert nodes and spans to GeoJSON

```{code-cell}
---
tags: [remove-cell, skip-execution]
---
!pip install geopandas
```

```{code-cell}
---
tags: [remove-cell]
---
import shutil

# GeoPackage: copy database and SQL scripts to the working directory
shutil.copy('../../../examples/geopackage/network.gpkg', 'network.gpkg')
shutil.copy('../../../examples/geopackage/dereference_nodes.sql', 'dereference_nodes.sql')
shutil.copy('../../../examples/geopackage/dereference_spans.sql', 'dereference_spans.sql')

# Uncomment the geometry column in each GeoPackage SQL script
with open('dereference_nodes.sql') as f:
    sql = f.read()
sql = sql.replace('    -- n.geom,  -- uncomment to include geometry', '    n.geom,')
with open('dereference_nodes.sql', 'w') as f:
    f.write(sql)

with open('dereference_spans.sql') as f:
    sql = f.read()
sql = sql.replace('    -- s.geom,  -- uncomment to include geometry', '    s.geom,')
with open('dereference_spans.sql', 'w') as f:
    f.write(sql)

# CSV: copy the full example CSV files (which include all required fields)
for csv_file in [
    'nodes.csv', 'nodes_networkProviders.csv', 'nodes_internationalConnections.csv',
    'spans.csv', 'spans_networkProviders.csv', 'wayleaves.csv',
]:
    shutil.copy(f'../../../examples/csv/{csv_file}', csv_file)

# JSON: copy dereference scripts and example data
for py_file in ['dereference_nodes.py', 'dereference_spans.py']:
    shutil.copy(f'../../../examples/json/{py_file}', py_file)
shutil.copy('../../../examples/json/network-package.json', 'network-package.json')
```

OFDS provides pre-built scripts for the `nodes` and `spans` layers that produce a single, ready-to-use GeoJSON output — with organisation names, phase names, codelist values, and address fields already included as properties. Scripts are available for all three OFDS data formats.

**Jump to:** [GeoPackage](#geopackage) · [CSV](#csv) · [JSON](#json) · [Output field reference](#output-field-reference)

## GeoPackage

The GeoPackage scripts use SQL with CTEs and are run directly against the GeoPackage file. Download:

* [`dereference_nodes.sql`](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/blob/0.3-dev/examples/geopackage/dereference_nodes.sql)
* [`dereference_spans.sql`](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/blob/0.3-dev/examples/geopackage/dereference_spans.sql)

```{note}
Both scripts include a commented-out geometry column (`-- n.geom` / `-- s.geom`). Uncomment this line before running if you want the output to include geometry.
```

### ogr2ogr

```{code-cell}
%%bash
ogr2ogr -f GeoJSON gpkg_nodes.geojson network.gpkg \
  -sql "$(cat dereference_nodes.sql)"

ogr2ogr -f GeoJSON gpkg_spans.geojson network.gpkg \
  -sql "$(cat dereference_spans.sql)"
```

```{code-cell}
---
mystnb:
  scroll_outputs: True
---
import json

with open('gpkg_nodes.geojson') as f:
    data = json.load(f)

for feature in data['features']:
    props = {k: v for k, v in feature['properties'].items() if v is not None and v != ''}
    print(json.dumps(props, indent=2))
    print()
```

### GeoPandas

```{code-cell}
import geopandas as gpd

with open('dereference_nodes.sql') as f:
    sql = f.read()

nodes = gpd.read_file('network.gpkg', sql=sql)
nodes.to_file('gpkg_nodes_gpd.geojson', driver='GeoJSON')
nodes[['identifier', 'name', 'phase', 'status', 'address', 'networkProviders']]
```

```{note}
The `sql` parameter requires GeoPandas 1.0 or later with the [pyogrio](https://pyogrio.readthedocs.io/en/latest/) engine.
```

### QGIS

1. Open **Database > DB Manager** in QGIS.
2. Under **GeoPackage** in the left panel, connect to your `.gpkg` file.
3. Open the **SQL Window**, paste the script contents, and uncomment the `geom` line.
4. Click **Execute**, then check **Load as new layer**, set the geometry column to `geom`, and click **Load**.
5. To export: right-click the layer and select **Export > Save Features As**, choosing **GeoJSON**.

## CSV

```{code-cell}
---
tags: [remove-cell]
---
import shutil

# Switch to the CSV versions of the dereference scripts
shutil.copy('../../../examples/csv/dereference_nodes.sql', 'dereference_nodes.sql')
shutil.copy('../../../examples/csv/dereference_spans.sql', 'dereference_spans.sql')
```

The CSV scripts use SQL with the ogr2ogr SQLite dialect, which treats each CSV file as a database table. Download:

* [`dereference_nodes.sql`](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/blob/0.3-dev/examples/csv/dereference_nodes.sql)
* [`dereference_spans.sql`](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/blob/0.3-dev/examples/csv/dereference_spans.sql)

### ogr2ogr

Run from the directory containing your CSV files:

```{code-cell}
%%bash
ogr2ogr -f GeoJSON csv_nodes.geojson nodes.csv \
  -dialect SQLite \
  -sql "$(cat dereference_nodes.sql)" \
  -a_srs EPSG:4326

ogr2ogr -f GeoJSON csv_spans.geojson spans.csv \
  -dialect SQLite \
  -sql "$(cat dereference_spans.sql)" \
  -a_srs EPSG:4326
```

```{code-cell}
---
mystnb:
  scroll_outputs: True
---
import json

with open('csv_nodes.geojson') as f:
    data = json.load(f)

for feature in data['features']:
    props = {k: v for k, v in feature['properties'].items() if v is not None and v != ''}
    print(json.dumps(props, indent=2))
    print()
```

### GeoPandas

```{code-cell}
import pandas as pd
import geopandas as gpd
from shapely import wkt

nodes = pd.read_csv('nodes.csv')
providers = pd.read_csv('nodes_networkProviders.csv')
network_providers = (
    providers.groupby('nodes/0/id')['nodes/0/networkProviders/0/name']
    .apply(';'.join)
    .reset_index()
)
nodes = nodes.merge(network_providers, on='nodes/0/id', how='left')
nodes['geometry'] = nodes['nodes/0/location'].apply(wkt.loads)
gdf = gpd.GeoDataFrame(nodes, crs='EPSG:4326')
gdf.to_file('csv_nodes_gpd.geojson', driver='GeoJSON')
gdf[['nodes/0/id', 'nodes/0/name', 'nodes/0/status', 'nodes/0/networkProviders/0/name']]
```

```{note}
This GeoPandas example joins only the network providers relationship. For a full dereference equivalent to the SQL script, use the ogr2ogr approach above.
```

### QGIS

1. Use **Layer > Add Layer > Add Delimited Text Layer**.
2. Select `nodes.csv`, set **Geometry field** to `nodes/0/location`, **Geometry type** to `Point`, and **CRS** to `EPSG:4326`.
3. To join network providers: use **Layer Properties > Joins** to join `nodes_networkProviders.csv` on the node ID field.
4. To export: right-click the layer and select **Export > Save Features As**, choosing **GeoJSON**.

## JSON

The JSON scripts are Python scripts that read an OFDS network package JSON file. OFDS JSON data is already fully dereferenced — organisation names, phase names, and other attributes are embedded as nested objects — so the scripts focus on extracting and flattening these into a consistent property structure.

Download:

* [`dereference_nodes.py`](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/blob/0.3-dev/examples/json/dereference_nodes.py)
* [`dereference_spans.py`](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/blob/0.3-dev/examples/json/dereference_spans.py)

Requires [GeoPandas](https://geopandas.org/) and [Shapely](https://shapely.readthedocs.io/).

### Python

```{code-cell}
%%bash
python dereference_nodes.py network-package.json json_nodes.geojson
python dereference_spans.py network-package.json json_spans.geojson
```

Or import directly into your own script:

```{code-cell}
from dereference_nodes import dereference_nodes
from dereference_spans import dereference_spans

dereference_nodes('network-package.json', 'json_nodes2.geojson')
dereference_spans('network-package.json', 'json_spans2.geojson')
```

```{code-cell}
---
mystnb:
  scroll_outputs: True
---
import json

with open('json_nodes.geojson') as f:
    data = json.load(f)

for feature in data['features']:
    props = {k: v for k, v in feature['properties'].items() if v is not None and v != ''}
    print(json.dumps(props, indent=2))
    print()
```

### QGIS

Run the Python script first to produce a GeoJSON file, then load it in QGIS via **Layer > Add Layer > Add Vector Layer**.

## Output field reference

All three format-specific scripts produce a consistent set of output properties. The tables below describe the output fields.

**Nodes**

| Output field | Description |
|---|---|
| `identifier` | Node identifier |
| `name` | Node name |
| `phase` | Phase name |
| `status` | Status |
| `address` | Comma-separated address |
| `type` | Semicolon-separated node type codelist codes |
| `supportingInfrastructure__type` | Codelist code |
| `supportingInfrastructure__description` | Description |
| `supportingInfrastructure__owner` | Organisation name |
| `supportingInfrastructure__spareCapacity` | Spare capacity |
| `accessPoint` | Access point |
| `power` | Power available |
| `technologies` | Semicolon-separated technology codelist codes |
| `transmissionMediumOwner` | Organisation name |
| `networkProviders` | Semicolon-separated organisation names |
| `internationalConnections` | Semicolon-separated country codes |

**Spans**

| Output field | Description |
|---|---|
| `identifier` | Span identifier |
| `name` | Span name |
| `phase` | Phase name |
| `status` | Status |
| `readyForServiceDate` | Ready for service date |
| `start` | Start node name and identifier, e.g. `Accra (1)` |
| `end` | End node name and identifier |
| `directed` | Whether the span is directed |
| `transmissionMediumOwner` | Organisation name |
| `supplier` | Organisation name |
| `supportingInfrastructure__type` | Codelist code |
| `supportingInfrastructure__description` | Description |
| `supportingInfrastructure__owner` | Organisation name |
| `supportingInfrastructure__spareCapacity` | Spare capacity |
| `codeployment` | Codelist code |
| `cableType` | Codelist code |
| `darkFibre` | Dark fibre available |
| `fibreType` | Fibre type |
| `fibreTypeDetails__fibreSubtype` | Fibre subtype |
| `fibreTypeDetails__description` | Fibre type description |
| `fibreCount` | Number of fibres |
| `fibreLength` | Fibre length (metres) |
| `transmissionMedium` | Semicolon-separated codelist codes |
| `deployment` | Semicolon-separated codelist codes |
| `technologies` | Semicolon-separated codelist codes |
| `capacity` | Capacity |
| `capacityDetails__description` | Capacity description |
| `networkProviders` | Semicolon-separated organisation names |
| `countries` | Semicolon-separated country codes |
| `wayleave_grantor` | Organisation name |
| `wayleave_term` | e.g. `25 years` or `indefinite` |
| `wayleave_cost` | e.g. `1.75 GHS per metre (annual)` |
