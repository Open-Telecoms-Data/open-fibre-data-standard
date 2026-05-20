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

shutil.rmtree('_nb') if os.path.exists('_nb') else None
os.makedirs('_nb', exist_ok=True)

BASE_URL = 'https://raw.githubusercontent.com/Open-Telecoms-Data/open-fibre-data-standard/298-geojson-guidance'

def get_file(repo_path, dest=None):
    dest_name = dest or os.path.basename(repo_path)
    local = f'../../../../{repo_path}'
    if os.path.exists(local):
        shutil.copy(local, f'_nb/{dest_name}')
    else:
        urllib.request.urlretrieve(f'{BASE_URL}/{repo_path}', f'_nb/{dest_name}')

get_file('examples/geopackage/network.gpkg', 'network.gpkg')
get_file('examples/json/network-package.json', 'network-package.json')
for f in [
    'nodes.csv', 'nodes_networkProviders.csv', 'nodes_internationalConnections.csv',
    'spans.csv', 'spans_networkProviders.csv', 'wayleaves.csv', 'networks.csv'
]:
    get_file(f'examples/csv/{f}')
for f in [
    'dereference_nodes_gpkg.sql', 'dereference_spans_gpkg.sql',
    'dereference_nodes_csv.sql', 'dereference_spans_csv.sql',
    'dereference_nodes.py', 'dereference_spans.py',
]:
    get_file(f'docs/guidance/geojson/prebuilt/{f}')

os.chdir('_nb')
```

OFDS provides pre-built scripts for the `nodes` and `spans` layers that produce a dereferenced GeoJSON output, with organisation names, phase names, codelist values, and address fields already included as properties. The following table shows which combinations of OFDS data format and tool are covered on this page:

| | [ogr2ogr](https://gdal.org/en/stable/programs/ogr2ogr.html) | [GeoPandas](https://geopandas.org/) | [QGIS](https://qgis.org/) |
|---|:---:|:---:|:---:|
| **[GeoPackage](#geopackage)** | [✓](#ogr2ogr) | [✓](#geopandas) | [✓](#qgis) |
| **[CSV](#csv)** | [✓](#ogr2ogr-1) | | |
| **[JSON](#json)** | | [✓](#python) | |

This page also provides an [output field reference](#output-field-reference) that describes how OFDS data is transformed in the output GeoJSON files.

```{tip}
Download this page as an executable Jupyter Notebook:  {nb-download}`index.ipynb`.
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

To execute a sql script and export the output to GeoJSON format, use the following options:

* [`-f GeoJSON`](https://gdal.org/en/stable/programs/ogr2ogr.html#cmdoption-ogr2ogr-f) to set the output format to GeoJSON
* [`-sql` @filename](https://gdal.org/en/stable/programs/ogr2ogr.html#cmdoption-ogr2ogr-sql) to specify the SQL query to execute, using `@filename` to read the query from a file
* [`-lco RFC7946=YES`](https://gdal.org/en/stable/programs/ogr2ogr.html#cmdoption-ogr2ogr-lco) to ensure output is compliant with the GeoJSON specfication (RFC 7946)
- [`-nln` layer_name](https://gdal.org/en/stable/programs/ogr2ogr.html#cmdoption-ogr2ogr-nln) to set the name of the output layer (optional)

For example, to execute `dereference_nodes_gpkg.sql` and export the output to `gpkg_nodes.geojson`:

```{code-cell}
%%bash
ogr2ogr -f GeoJSON gpkg_nodes.geojson network.gpkg \
  -sql @dereference_nodes_gpkg.sql \
  -lco RFC7946=YES \
  -nln nodes

ogr2ogr -f GeoJSON gpkg_spans.geojson network.gpkg \
  -sql @dereference_spans_gpkg.sql \
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

The JSON scripts are Python scripts that read an [OFDS network package JSON file](../../../reference/data_formats/json/index.md) and write a GeoJSON feature collection containing nodes or spans with dereferenced properties.

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

View `json_nodes.geojson`, using [jq](https://jqlang.org/):

```{code-cell}
---
mystnb:
  scroll_outputs: True
---
cat json_nodes.geojson | jq .
```

## Output field reference

The scripts produce a consistent set of output properties across all three formats. Minor differences in how certain value types are represented are described in [Format differences](#format-differences).

**Nodes**

| Output field | Description |
|---|---|
| `network` | Network name |
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
| `network` | Network name |
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
| `capacity` | Capacity |
| `capacityDetails__description` | Capacity description |
| `networkProviders` | Semicolon-separated organisation names |
| `transmissionMedium` | Semicolon-separated codelist codes |
| `deployment` | Semicolon-separated codelist codes |
| `technologies` | Semicolon-separated codelist codes |
| `wayleave_grantor` | Organisation name |
| `wayleave_term` | e.g. `25 years` or `indefinite` |
| `wayleave_cost` | e.g. `1.75 GHS per metre (annual)` |
| `countries` | Semicolon-separated country codes |

### Format differences

The three scripts produce equivalent output, but differ in how certain value types are represented due to differences in the source data formats and the tools and libraries used to convert data.

**Boolean fields**

| Format | Representation |
|---|---|
| GeoPackage | `"true"` / `"false"` (string) |
| CSV | `"True"` / `"False"` (string) |
| JSON | `true` / `false` (native JSON boolean) |

**Numeric fields**

| Format | Representation |
|---|---|
| GeoPackage | Native number (e.g. `24`, `276000.0`, `4.976`) |
| CSV | String (e.g. `"24"`, `"276000"`, `"4.976"`) |
| JSON | Native number (e.g. `24`, `276000`, `4.976`) |

**Missing values**

| Format | Representation |
|---|---|
| GeoPackage | `null` |
| CSV | `""` (empty string) |
| JSON | `null` |
