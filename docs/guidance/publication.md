# How to publish OFDS data

This page provides an [overview](#overview) of the process for publishing OFDS data and [how-to guides](#how-to-guides) for specific topics.

## Overview

The process for publishing OFDS data can be divided into three phases:

* [Plan](#plan)
* [Prepare](#prepare)
* [Publish](#publish)

### Plan

#### Identify your priority use cases

There are many [use cases](../primer/openfibredata.md#why-publish-open-fibre-data) for OFDS data, each with their own data needs. You ought to decide which use cases to prioritise so that you can make sure that your data includes the necessary fields and that it is available via suitable publication formats and access methods.

#### Decide what data to publish

Bearing in mind your priority use cases, you ought to review the OFDS [schema](../reference/schema.md) and decide which fields you want to publish.

Most fields in the OFDS schema are optional. However, the more fields you publish, the more useful your data will be.

#### Identify your data sources

Once you have decided what data to publish, you ought to identify your data sources, i.e. the systems, databases or documents that contain the data that you will convert to OFDS format for publication.

### Prepare

#### Map your data to OFDS

Once you have identified your data sources, you ought to map your data to the OFDS schema, that is, identify which data elements within your data sources match which OFDS [fields](../reference/schema.md) and [codes](../reference/codelists.md).

Your mapping acts as a blueprint for preparing your data. It will help you to identify the steps involved in converting your data to OFDS format.

#### Collect missing data

Your mapping might identify fields that you want to publish but that are missing from your data sources. If so, you'll need to collect the missing data.

#### Choose your publication formats and access methods

Bearing in mind your priority use cases, you ought to decide which publication formats and access methods you will use to publish your OFDS data.

For more information, see [how to format data for publication](#how-to-format-data-for-publication) and [how to provide access to data](#how-to-provide-access-to-data).

### Publish

#### Prepare your data

Once you have completed your mapping and decided on your publication formats and access methods, the next step is to convert your data to OFDS format.

The suggested approach is to develop a reproducible data pipeline so that you can easily update your OFDS publication when the data in your data sources is updated. However, you can prepare your data using whichever tools you are most comfortable with. 

#### Check your data

```{admonition} Alpha consultation
An online tool for checking the structure and format of OFDS data is under development and will be released with the Beta version of the standard. In the meantime, you can use a generic tool, like [JSON Schema Validator](https://www.jsonschemavalidator.net/) to check the structure and format of OFDS data.
```

Once you have prepared your data, the next step is to check that it is correctly structured and formatted according to the OFDS schema.

#### Publish your data

Once any issues with the structure and format of your data have been resolved, the next step is to publish your data using your chosen access methods.

For your data to be open, you need to publish it using an open license. For more information, see [how to license your data](#how-to-license-your-data).

## How-to guides

This section contains how-to guides for specific topics. To learn about the process for publishing OFDS data, see the [overview](#overview).

### How to transform coordinates to the correct coordinate reference system

To publish OFDS data, you need to specify coordinates in the `urn:ogc:def:crs:OGC::CRS84` [coordinate reference system](../reference/schema.md#coordinatereferencesystem) (CRS). If the coordinates in your data sources are specified in a different CRS, before publishing your data in OFDS format, you first need to transform the coordinates to the correct CRS.

If your data pipeline includes a Geographic Information System such as ArcGIS or QGIS, these tools can transform coordinates from one CRS to another. If you are writing your own software, or if you prefer to use the command line, several libraries and tools are available, for example:

* [PROJ](https://proj.org/) and its associated Python interface ([PYPROJ](https://pyproj4.github.io/pyproj/stable/)) and Javascript implementation ([PROJ4JS](http://proj4js.org/) are generic coordinate transformation tools that transform geospatial coordinates from one coordinate reference system (CRS) to another. They include command-line applications and an application programming interface. 
* [GDAL](https://gdal.org/) is a translator library for raster and vector geospatial data formats. It also comes with a variety of useful command line utilities for data translation and processing.
* [Apache SIS](https://sis.apache.org/) is a free software, Java language library for developing geospatial applications. SIS provides data structures for geographic features and associated metadata along with methods to manipulate those data structures.

If you prefer to use a graphical user interface, several web-based tools are available, for example:

* [MyGeodata Cloud](https://mygeodata.cloud/cs2cs/)
* [epsg.io](https://epsg.io/transform)

The `urn:ogc:def:crs:OGC::CRS84` CRS is equivalent to EPSG:4326 with reversed axes so, if it is not supported by your chosen transformation tool, you can instead transform your coordinates to EPSG:4326 and manually order your coordinates in longitude, latitude order.

### How to generate universally unique identifiers

If you are writing your own software or if you prefer to use the command line, several libraries and tools are available to generate universally unique identifiers (UUIDS), for example:

* Golang - [google/uuid](https://pkg.go.dev/github.com/google/uuid)
* PHP - [ramsey/uuid](https://github.com/ramsey/uuid)
* C++ - [Boost UUID](https://www.boost.org/doc/libs/1_65_0/libs/uuid/uuid.html)
* Linux or C - [libuuid](https://linux.die.net/man/3/libuuid)
* Python - [uuid.py](https://docs.python.org/3/library/uuid.html)
* Java - [java.util.UUID](https://docs.oracle.com/javase/7/docs/api/java/util/UUID.html)
* C# - [System.Guid](https://docs.microsoft.com/en-us/dotnet/api/system.guid)
* Javascript - [Crypto.randomUUID](https://www.moreonfew.com/how-to-generate-uuid-in-javascript/)
* R - [uuid](https://cran.r-project.org/web/packages/uuid/index.html)

If you prefer to use a graphical user interface, several web-based tools are available, for example [Online UUID Generator](https://www.uuidgenerator.net/).

### How to format data for publication

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

To convert a network package to GeoJSON format:

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
./manage.py convert-to-geojson network-package.json
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

#### How to publish large networks

This section describes how to:

* Use [pagination](#pagination) to publish an **individual** network that is too large to return in a single API response
* Use [streaming](#streaming) to publish an **individual** network that is too large to load into memory.

For information on how to use pagination and streaming to publish **multiple** networks, see the [publication formats reference](../reference/publication_formats.md).

This guidance is applicable to the [JSON publication format](../reference/publication_formats.md#json), for information on pagination and streaming for the GeoJSON format see the [GeoJSON publication format reference](../reference/publication_formats.md#geojson).

##### Pagination

The preferred approach is to publish embedded nodes and links in `.nodes` and `.links`, respectively. If your network is too large to return in a single API response, you ought to use `.relatedResources` to reference separate endpoints for nodes and links. Each endpoint ought to return a top-level JSON object with a `nodes` or a `links` array, respectively, and a `pages` object with URLs for the next and previous pages of results:

::::{tab-set}

:::{tab-item} Embedded data
The following example shows a network with embedded nodes and links:
```{jsoninclude} ../../examples/json/network-package.json
:jsonpointer: /networks/0
:expand: nodes,links
```
:::

:::{tab-item} References to endpoints
The following example shows a network with references to separate endpoints for nodes and links:
```{jsoninclude} ../../examples/json/network-separate-endpoints.json
:jsonpointer: /networks/0
:expand: relatedResources
```
:::

:::{tab-item} Nodes endpoint
The following example shows the response returned by the nodes endpoint with URLs for the next and previous pages of results.
```{jsoninclude} ../../examples/json/nodes-endpoint.json
:jsonpointer:
```
:::

:::{tab-item} Links endpoint
The following example shows the response returned by the links endpoint with URLs for the next and previous pages of results.
```{jsoninclude} ../../examples/json/links-endpoint.json
:jsonpointer:
```
:::

::::

##### Streaming

The preferred approach is to publish embedded nodes and links. If your network is too large to load into memory, you ought to use `.relatedResources` to reference separate files for nodes and links. Each file ought to be formatted as a [JSON Lines](https://jsonlines.org/) file in which each line is a valid [`Node`](../reference/schema.md#node) or [`Link`](../reference/schema.md#link), respectively.

::::{tab-set}

:::{tab-item} Embedded data
The following example shows a network with embedded nodes and links:
```{jsoninclude} ../../examples/json/network-package.json
:jsonpointer: /networks/0
```
:::

:::{tab-item} References to files
The following example shows a network with references to separate files for nodes and links:
```{jsoninclude} ../../examples/json/network-separate-files.json
:jsonpointer: /networks/0
:expand: relatedResources
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

### How to provide access to data

### How to add additional fields

### How to write a data user guide

### How to license your data