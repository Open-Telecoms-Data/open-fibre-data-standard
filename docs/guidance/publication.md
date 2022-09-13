# How to publish OFDS data

## How to transform coordinates to the correct coordinate reference system

To publish OFDS data, you need to specify coordinates in the `urn:ogc:def:crs:OGC::CRS84` [coordinate reference system](../reference/schema.md#coordinatereferencesystem) (CRS). If the coordinates in your data sources are specified in a different CRS, before publishing your data in OFDS format, you first need to transform the coordinates to the correct CRS.

If your data pipeline includes a Geographic Information System such as ArcGIS or QGIS, these tools can transform coordinates from one CRS to another. If you are writing your own software, or if you prefer to use the command line, several libraries and tools are available, for example:

* [PROJ](https://proj.org/) and its associated Python interface ([PYPROJ](https://pyproj4.github.io/pyproj/stable/)) and Javascript implementation ([PROJ4JS](http://proj4js.org/) are generic coordinate transformation tools that transform geospatial coordinates from one coordinate reference system (CRS) to another. They include command-line applications and an application programming interface. 
* [GDAL](https://gdal.org/) is a translator library for raster and vector geospatial data formats. It also comes with a variety of useful command line utilities for data translation and processing.
* [Apache SIS](https://sis.apache.org/) is a free software, Java language library for developing geospatial applications. SIS provides data structures for geographic features and associated metadata along with methods to manipulate those data structures.

If you prefer to use a graphical user interface, several web-based tools are available, for example:

* [MyGeodata Cloud](https://mygeodata.cloud/cs2cs/)
* [epsg.io](https://epsg.io/transform)

The `urn:ogc:def:crs:OGC::CRS84` CRS is equivalent to EPSG:4326 with reversed axes so, if it is not supported by your chosen transformation tool, you can instead transform your coordinates to EPSG:4326 and manually order your coordinates in longitude, latitude order.

## How to format data for publication

```{admonition} Alpha consultation
There are [open issues](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues?q=is%3Aopen+is%3Aissue+label%3ATooling) related to tooling for transforming data between publication formats.
```

OFDS data can be published in three [publication formats](../reference/publication_formats.md):

* The [JSON format](../reference/publication_formats.md#json) reflects the structure of the [schema](../reference/schema.md), is useful to developers who want to use the data to build web apps, and offers a ‘base’ format that other publication formats can be converted to and from.
* The [GeoJSON format](../reference/publication_formats.md#geojson) is useful to GIS analysts who want to import the data directly into GIS tools without any pre-processing.
* The [CSV format](../reference/publication_formats.md#csv) is useful to data analysts who want to import data directly into databases and other tabular analysis tools, and to users who want to explore the data in spreadsheet tools.

To meet the widest range of use cases, you ought to publish data in all three formats. The suggested approach is to export your data in the JSON format and to use the following tools to transform it to the GeoJSON and CSV formats:

::::{tab-set}

:::{tab-item} JSON to GeoJSON
The standard repository's [`manage.py`](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/blob/main/manage.py) file provides a command-line interface for transforming OFDS data from JSON to GeoJSON format.

To convert a network to GeoJSON format:

* Clone the [repository](https://github.com/Open-Telecoms-Data/open-fibre-data-standard)
* Create a virtual environment:
```bash
sudo apt-get install python3-venv
python3 -m venv .ve    
source .ve/bin/activate
```
* Install requirements
```bash
pip install -r requirements.txt
```
* Run the following command:

```bash
./manage.py convert-to-geojson network.json
```

:::

:::{tab-item} JSON to CSV
[Flatten Tool](https://flatten-tool.readthedocs.io/en/latest/) provides a command-line interface for transforming OFDS data from JSON to CSV format.

To convert data to CSV format:

* [Install Flatten Tool](https://flatten-tool.readthedocs.io/en/latest/getting-started/#getting-started)
* Download the [network schema](../../schema/network-schema.json)
* If your data is a [JSON Lines file](../reference/publication_formats.md#streaming-option), segment it into appropriately sized [network packages](../reference/publication_formats.md#small-files-and-api-responses-option)
* Run the following command for each network package:

```bash
flatten-tool flatten --truncation-length=9 --root-list-path=networks --main-sheet-name=networks --schema=network-schema.json network-package.json -f csv
```
:::

::::

### How to publish large networks

This section describes how to:

* Use [pagination](#pagination) to publish an **individual** network that is too large to return in a single API response
* Use [streaming](#streaming) to publish an **individual** network that is too large to load into memory.

For information on how to use pagination and streaming to publish **multiple** networks, see the [publication formats reference](../reference/publication_formats.md).

This guidance is applicable to the [JSON publication format](../reference/publication_formats.md#json), for information on pagination and streaming for the GeoJSON format see the [GeoJSON publication format reference](../reference/publication_formats.md#geojson).

#### Pagination

The preferred approach is to publish embedded nodes and links in `.nodes` and `.links`, respectively. If your network is too large to return in a single API response, you ought to use `.relatedResources` to point to separate endpoints for nodes and links. Each endpoint ought to return a top-level JSON object with a `nodes` or a `links` array, respectively, and a `pages` object with links to the next and previous pages of results:

::::{tab-set}

:::{tab-item} Embedded data
The following example shows a network with embedded nodes and links:
```{jsoninclude} ../../examples/json/network-embedded.json
:jsonpointer:
```
:::

:::{tab-item} Links to endpoints
The following example shows a network with links to separate endpoints for nodes and links:
```{jsoninclude} ../../examples/json/network-separate-endpoints.json
:jsonpointer:
```
:::

:::{tab-item} Nodes endpoint
The following example shows the response returned by the nodes endpoint with links to the next and previous pages of results.
```{jsoninclude} ../../examples/json/nodes-endpoint.json
:jsonpointer:
```
:::

:::{tab-item} Links endpoint
The following example shows the response returned by the links endpoint with links to the next and previous pages of results.
```{jsoninclude} ../../examples/json/links-endpoint.json
:jsonpointer:
```
:::

::::

#### Streaming

The preferred approach is to publish embedded nodes and links. If your network is too large to load into memory, you ought to use `.relatedResources`to provide links to separate files for nodes and links. Each file ought to be formatted as a [JSON Lines](https://jsonlines.org/) file in which each line is a valid [`Node`](../reference/schema.md#node) or [`Link`](../reference/schema.md#link), respectively.

::::{tab-set}

:::{tab-item} Embedded data
The following example shows a network with embedded nodes and links:
```{jsoninclude} ../../examples/json/network-embedded.json
:jsonpointer:
```
:::

:::{tab-item} Links to files
The following example shows a network with links to separate files for nodes and links:
```{jsoninclude} ../../examples/json/network-separate-files.json
:jsonpointer:
```
:::

:::{tab-item} Nodes file
The following example shows a nodes file in JSON Lines format.
```
{}
{}
```
:::

:::{tab-item} Links file
The following example shows a links file in JSON Lines format.
```
{}
{}
```
:::

::::

## How to provide access to data

## How to add additional fields

## How to write a data user guide