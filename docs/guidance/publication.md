# How to publish OFDS data

This page provides an [overview](#overview) of the process for publishing Open Fibre Data Standard (OFDS) data and [how-to guides](#how-to-guides) for specific topics.

## Overview

The process for publishing OFDS data can be divided into three phases:

* [Plan](#plan)
* [Prepare](#prepare)
* [Publish](#publish)

### Plan

The plan phase covers identifying your priority use cases, deciding what data to publish and identifying your data sources.

#### Identify your priority use cases

There are many [use cases](../primer/openfibredata.md#why-publish-open-fibre-data) for OFDS data, each with their own data needs. You ought to decide which use cases to prioritise so that you can make sure that your data includes the necessary fields and that it is available via suitable publication formats and access methods.

#### Decide what data to publish

Bearing in mind your priority use cases, you ought to review the OFDS [schema](../reference/schema.md) and decide which fields you want to publish.

Most fields in the OFDS schema are optional. However, the more fields you publish, the more useful your data will be.

#### Identify your data sources

Once you have decided what data to publish, you ought to identify your data sources. These will be the systems, databases and documents that contain the data that you will convert to OFDS format for publication.

### Prepare

The prepare phase covers mapping your data to OFDS, collecting missing data and choosing your publication formats and access methods.

#### Map your data to OFDS

Once you have identified your data sources, you ought to map your data to the OFDS schema, that is, identify which data elements within your data sources match which OFDS [fields](../reference/schema.md) and [codes](../reference/codelists.md). If there are data elements that you want to publish but for which you cannot identify a suitable mapping, you can [add additional fields](#how-to-add-additional-fields) to your OFDS data.

Your mapping acts as a blueprint for preparing your data. It will help you to identify the steps involved in converting your data to OFDS format.

#### Collect missing data

Your mapping might identify fields that you want to publish but that are missing from your data sources. If so, you'll need to collect the missing data.

#### Choose your publication formats and access methods

Bearing in mind your priority use cases, you ought to decide which publication formats and access methods you will use to publish your OFDS data.

For more information, see [how to format data for publication](#how-to-format-data-for-publication) and [how to provide access to data](#how-to-provide-access-to-data).

### Publish

The publish phase covers preparing your data, checking your data and publishing your data.

#### Prepare your data

Once you have completed your mapping and decided on your publication formats and access methods, the next step is to convert your data to OFDS format.

The suggested approach is to develop a reproducible data pipeline so that you can easily update your OFDS publication when the data in your data sources is updated. However, you can prepare your data using whichever tools you are most comfortable with.

For guidance on common steps in converting your data to OFDS format, see the following guides:

* [How to transform coordinates to the correct coordinate reference system](#how-to-transform-coordinates-to-the-correct-coordinate-reference-system)
* [How to generate universally unique identifiers](#how-to-generate-universally-unique-identifiers)

#### Check your data

Once you have prepared your data, the next step is to check that it is correctly structured and formatted according to the OFDS schema.

```{admonition} Data Review Tool
An online tool for checking the structure and format of OFDS data is under development and will be released with the Beta version of the standard. In the meantime, you can use a generic tool, like [JSON Schema Validator](https://www.jsonschemavalidator.net/) to check the structure and format of OFDS data.
```

#### Publish your data

Once any issues with the structure and format of your data have been resolved, the next step is to publish your data using your chosen access methods.

For your data to be open, you need to publish it using an open license. For more information, see [how to license your data](#how-to-license-your-data).

## How-to guides

This section contains how-to guides for specific topics. To learn about the process for publishing OFDS data, see the [overview](#overview).

### How to add additional fields

The OFDS schema does not restrict the use of additional fields. If there is a data element that you wish to publish for which you cannot identify a suitable mapping in OFDS, you can add an additional field to your data.

Before adding an additional field, you ought to search the [standard issue tracker](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues) to see if a similar concept has already been discussed. If there are no existing discussions, you ought to open a new issue and describe the concept that you want to publish and your proposed modelling.

If you add an additional field, you ought to describe its structure, format and meaning in your data user guide. For more information, see [how to write a data user guide](#how-to-write-a-data-user-guide).

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

Where resources allow, it is [best practice](https://www.w3.org/TR/dwbp/#MultipleFormats) to provide multiple access methods for your data so that both humans and machines can access it easily.

With respect to your OFDS publication, which best practices are most important will depend on your priority use cases, but you are encouraged to consider providing [bulk downloads](#bulk-downloads) and [API access](#api-access).

#### Bulk downloads

If you are publishing only one network, or a small number of networks, you ought to use the approach described in the small file option for each [publication format](../reference/publication_formats.md).

If you are publishing a large number of networks, you ought to use the approach to streaming multiple networks described in the streaming option for each [publication format](../reference/publication_formats.md).

If you are publishing a network that is very large, you ought to use the approach to streaming nodes and links described in [how to publish large networks](#how-to-publish-large-networks).

##### Compression

OFDS data can be compressed in order to save on disk space and bandwidth.

When compressing packages, use ZIP or GZIP, as these are commonly available, often without additional software. Avoid RAR, which requires additional software.

##### Serving files

The web server providing access to bulk files ought to report the [HTTP Last-Modified](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.29) header correctly, so that consuming applications only need to download updated files.

Also, publishers ought to ensure that the data export is completed successfully, i.e. that no files were truncated.

#### API access

If you are publishing data via an API, you need to consider pagination. If you are publishing multiple networks, you ought to use the pagination method described in the API response option for each [publication format](../reference/publication_formats.md).

If you are publishing a network that is very large, you ought to use the approach to paginating nodes and links described in [how to publish large networks](#how-to-publish-large-networks).

API design is a deep topic. As such, the following guidance is not intended to be comprehensive or prescriptive. Wherever possible, you ought to carry out your own user research.

##### Discoverability

Ensure that the API endpoints and documentation are discoverable. For example, add a link to the footer of your website, and list the API endpoints in your government's open data portal.

##### Documentation

Provide API documentation, with at least the lists of endpoints, methods and parameters. Many open data publishers use [Swagger](https://swagger.io/) to document their APIs.

##### Access control and rate limiting

Avoid adding access controls (like user registration or API keys), in order to maximize the ease of access to the publication.

If access controls are necessary, do not use access tokens that need to be refreshed regularly. For example, every two hours is too frequent.

If the API implements rate limits (throttling):

* Document the rate limits in the API documentation ([example](https://developer.twitter.com/en/docs/twitter-api/rate-limits)).
* When a user exceeds a rate limit, return a [HTTP 429 'Too Many Requests' response status code,](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) and set the [Retry-After](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Retry-After) HTTP header to indicate how long to wait before making a new request.

##### Completeness

Ensure that all OFDS data can be accessed via the API.

##### Response format

* Put the network package or GeoJSON feature collection at the top-level of the JSON data. For example, do not embed it under a results array.
* Use a JSON library instead of implementing JSON serialization yourself. This also guarantees that the encoding is UTF-8.
* Remove NULL characters (\u0000) from the JSON response. These characters cannot be imported by users into some SQL databases.
* If results cannot be returned, use an appropriate HTTP error code (400-599); do not return a JSON object with an error message and a 200 HTTP status code. That said, if a search request returns no results, it is appropriate to use a 200 HTTP status code, with an empty result set.

##### Monitoring

Set up error monitoring, so that if a request causes an HTTP 500 Internal Server Error, you can investigate.

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

### How to write a data user guide

Publishing OFDS data involves making choices about what data to include and exclude, and how to map existing data elements to the fields in OFDS.

In order for users to interpret data correctly and make effective use of it, it's important to describe your decisions and to provide guidance to data users. Your data user guide ought to include:

* [why you are publishing the data](../primer/openfibredata.md#why-publish-open-fibre-data)
* [how you prepared the data](#prepare-your-data) and how frequently it is updated
* the scope of the data
* the meaning, structure and format of any [additional fields](#how-to-add-additional-fields)
* the available [publication formats](#how-to-format-data-for-publication) and [access methods](#how-to-provide-access-to-data)
* [license information](#how-to-license-your-data) for data reuse
* any plans for changes to your publication
* your contact details

Your data user guide ought to be made available as a public web page. You ought to link to the web page wherever you publish links to your data.

### How to license your data

Publishing your data under an open license is important because it prevents restrictions on re-use, which could limit the usefulness of the data.

You are encouraged to use either a public domain dedication/certification or an attribution-only license:

* A public domain dedication asserts no copyright, database rights or contractual rights over the data. For example, [Creative Commons' public domain tools](https://creativecommons.org/publicdomain/).
* Attribution-only licenses allow for use and reuse, with the only restriction being that attribution (credit) be given to the original publisher. For example, [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0/).

The Open Knowledge Foundation maintains a list of [licenses that conform to the open definition](https://opendefinition.org/licenses/). If you use a custom license, you ought to check that it conforms to the [open definition](https://opendefinition.org/od/2.1/en/).

You need to ensure that a clear license statement is provided wherever publish links to your data.
