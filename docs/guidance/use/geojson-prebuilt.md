---
file_format: mystnb
---

# Convert nodes and spans to GeoJSON

+++{"tags": ["remove-cell"]}
## Setup

To run the commands in this notebook, you'll need to install [GDAL](https://gdal.org/en/stable/index.html) and [jq](https://jqlang.org/), and run the following cell to install Python dependencies:

+++

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

get_file('examples/geopackage/network.gpkg', 'network.gpkg')
get_file('examples/json/network-package.json', 'network-package.json')
for f in [
    'nodes.csv', 'nodes_networkProviders.csv', 'nodes_internationalConnections.csv',
    'spans.csv', 'spans_networkProviders.csv', 'wayleaves.csv',
]:
    get_file(f'examples/csv/{f}')
for f in [
    'dereference_nodes_gpkg.sql', 'dereference_spans_gpkg.sql',
    'dereference_nodes_csv.sql', 'dereference_spans_csv.sql',
    'dereference_nodes.py', 'dereference_spans.py',
]:
    get_file(f'docs/guidance/use/{f}')

os.chdir('_nb')
```

OFDS provides pre-built scripts for the `nodes` and `spans` layers that produce a single, ready-to-use GeoJSON output, with organisation names, phase names, codelist values, and address fields already included as properties. The following table shows which combinations of OFDS data format and tool are supported:

| | [ogr2ogr](https://gdal.org/en/stable/programs/ogr2ogr.html) | [GeoPandas](https://geopandas.org/) | [QGIS](https://qgis.org/) |
|---|:---:|:---:|:---:|
| **[GeoPackage](#geopackage)** | [✓](#ogr2ogr) | [✓](#geopandas) | [✓](#qgis) |
| **[CSV](#csv)** | [✓](#ogr2ogr-1) | | |
| **[JSON](#json)** | | [✓](#python) | |

This page also provides an [output field reference](#output-field-reference) that describes how OFDS data is transformed in the output GeoJSON files.

```{tip}
Download this page as an executable Jupyter Notebook:  {nb-download}`geojson-prebuilt.ipynb`.
```

## GeoPackage

The GeoPackage scripts are SQL queries that run directly against an OFDS GeoPackage file:

* [`dereference_nodes_gpkg.sql`](dereference_nodes_gpkg.sql)
* [`dereference_spans_gpkg.sql`](dereference_spans_gpkg.sql)

This section provides instructions for using the scripts to dereference and convert an OFDS GeoPackage to GeoJSON format using three common GIS tools:

* [QGIS (GIS software)](#qgis)
* [ogr2ogr (command-line tool)](#ogr2ogr)
* [GeoPandas (Python library)](#geopandas)

A GeoPackage is a SQLite database in which geometries are encoded in binary format. Therefore, whilst you can query the database directly from any SQL client, it is recommended to use a GIS tool to convert data that includes geometries to GeoJSON format.

### QGIS

[QGIS](https://qgis.org/) is a popular open-source GIS software that can be used to convert geospatial data between different file formats.

To convert the nodes and spans layers to GeoJSON format in QGIS:

1. Open **Database > DB Manager** in QGIS.
2. Under **GeoPackage** in the left panel, connect to your `.gpkg` file.
3. Open the **SQL Window** and paste the contents of `dereference_nodes.sql` or `dereference_spans.sql`.
4. Click **Execute**, then check **Load as new layer**, set the geometry column to `geom`, and click **Load**.
5. To export: right-click the layer and select **Export > Save Features As**, choosing **GeoJSON**.

### ogr2ogr

[ogr2ogr](https://gdal.org/en/stable/programs/ogr2ogr.html) is a command-line tool that can be used to convert geospatial data between file formats.

Use the following commands to dereference and convert the nodes and spans layers to GeoJSON format:

```{code-cell}
%%bash
ogr2ogr -f GeoJSON gpkg_nodes.geojson network.gpkg \
  -sql "$(cat dereference_nodes_gpkg.sql)" \
  -lco RFC7946=YES \
  -nln nodes

ogr2ogr -f GeoJSON gpkg_spans.geojson network.gpkg \
  -sql "$(cat dereference_spans_gpkg.sql)" \
  -lco RFC7946=YES \
  -nln spans
```

View `gpkg_nodes.geojson`, using [jq](https://jqlang.org/) to filter out properties with `null` values: 

```{code-cell}
---
mystnb:
  scroll_outputs: True
---
cat gpkg_nodes.geojson | jq 'del(..|nulls)'
```

### GeoPandas

[GeoPandas](https://geopandas.org/) is a Python library that can be used to convert geospatial data between different file formats.

Use the following Python script to dereference and convert the nodes and spans layers to GeoJSON format:

```{code-cell}
import geopandas as gpd

def dereference_and_convert(gpkg_file, sql_file, output_file, layer):
    with open(sql_file) as f:
        sql = f.read()

    data = gpd.read_file(gpkg_file, sql=sql)
    data.to_file(output_file, driver='GeoJSON', layer=layer, RFC7946='YES')

dereference_and_convert('network.gpkg', 'dereference_nodes_gpkg.sql', 'gpkg_nodes_gpd.geojson', 'nodes')
dereference_and_convert('network.gpkg', 'dereference_spans_gpkg.sql', 'gpkg_spans_gpd.geojson', 'spans')
```

```{note}
The `sql` parameter requires GeoPandas 1.0 or later with the [pyogrio](https://pyogrio.readthedocs.io/en/latest/) engine.
```

View `gpkg_nodes_gpd.geojson`, using [jq](https://jqlang.org/) to filter out properties with `null` values: 

```{code-cell}
---
mystnb:
  scroll_outputs: True
---
cat gpkg_nodes_gpd.geojson | jq 'del(..|nulls)'
```

## CSV

The CSV scripts are SQL queries designed for use with the ogr2ogr SQLite dialect, which treats each CSV file as a database table.

* [`dereference_nodes_csv.sql`](dereference_nodes_csv.sql)
* [`dereference_spans_csv.sql`](dereference_spans_csv.sql)

### ogr2ogr

[ogr2ogr](https://gdal.org/en/stable/programs/ogr2ogr.html) is a command-line tool that can be used to convert geospatial data between file formats.

Use the following commands to dereference and convert the nodes and spans CSV files to GeoJSON format:

```{code-cell}
%%bash
ogr2ogr -f GeoJSON csv_nodes.geojson nodes.csv \
  -dialect SQLite \
  -sql "$(cat dereference_nodes_csv.sql)" \
  -a_srs EPSG:4326 \
  -lco RFC7946=YES \
  -nln nodes

ogr2ogr -f GeoJSON csv_spans.geojson spans.csv \
  -dialect SQLite \
  -sql "$(cat dereference_spans_csv.sql)" \
  -a_srs EPSG:4326 \
  -lco RFC7946=YES \
  -nln spans
```

View `csv_nodes.geojson`, using [jq](https://jqlang.org/) to filter out properties with `null` values: 

```{code-cell}
---
mystnb:
  scroll_outputs: True
---
cat csv_nodes.geojson | jq 'del(..|nulls)'
```

## JSON

The JSON scripts are Python scripts that read an OFDS network package JSON file. OFDS JSON data is already fully dereferenced — organisation names, phase names, and other attributes are embedded as nested objects — so the scripts focus on extracting and flattening these into a consistent property structure.

Download:

* [`dereference_nodes.py`](dereference_nodes.py)
* [`dereference_spans.py`](dereference_spans.py)

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
