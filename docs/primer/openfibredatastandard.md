<!-- docs-type: explanation https://diataxis.fr/explanation/ -->

# The Open Fibre Data Standard

This page provides an introduction to the Open Fibre Data Standard (OFDS), the reasons for using it and what OFDS data looks like.

## What is the Open Fibre Data Standard?

The OFDS is a data standard for publishing, exchanging and storing data about fibre infrastructure. It describes the data needed to satisfy a range of use cases, and how to structure and format that data for publication, exchange and storage.

The OFDS provides:

- A [logical data model](../reference/data_model.md), that defines the entities, relationships and attributes needed to describe fibre infrastructure
- [Schemas](../reference/data_formats/index.md) for publishing, exchanging and storing data in GeoPackage, JSON and CSV format
- [Guidance and tooling](../guidance/index.md) for producing and using OFDS data

The OFDS covers several kinds of data about fibre infrastructure, including:

- Location data, e.g. the coordinates of nodes and the route of fibre spans.
- Technical data, e.g. the a ITU-T standard that a fibre cable conforms to.
- Administrative data, e.g. the organisations that own and operate fibre infrastructure.

## Why use the Open Fibre Data Standard?

Standardised data is easier for people and systems to interpret than non-standardised data because data standards resolve ambiguity by defining the structure and meaning of data.

Without standards, data users or intermediaries have to do the hard work of making sense of different datasets and developing dataset-specific methodologies and tools. But, with standards, users have access to information about the structure and meaning of data and can develop reusable tools and methodologies that can be applied to many different datasets.

```{admonition} Example: Standardising capacity data

There are a variety of units and notations for specifying the capacity of a fibre-optic span, including Mbps, Gbps, STM notation and E-carrier notation. This lack of standardisation presents a challenge to users who want to compare the capacity of different spans and networks.

Since all of the above units can be converted into Gbps, OFDS requires that publishers specify span capacity in Gbps. This approach places the effort of conversion onto the data publisher, where it only needs to happen once, rather than onto data users, each of whom would need to convert the data if it were not standardised.

```

Standards can also ensure that key information is included in a dataset. If data owners do not share key information in their data, then users need to negotiate with each data owner individually.

Using the OFDS to inform the data that you choose to publish, exchange or store helps to ensure that your data meets the needs of a range of users. For example, data on the organisations that own and operate infrastructure can help operators and regulators to understand where different organisations might be reporting on the same fibre cable, making it easier to understand the true extent and resilience of fibre infrastructure.

## What does OFDS data look like?

To meet the needs of different users, OFDS provides schemas for three data formats:

- GeoPackage data is useful to GIS analysts, because it can be imported and edited by common GIS tools, whilst maintaining referential integrity
- JSON data is useful to web developers, because it be easily rendered as a web-map.
- CSV data is useful to spreadsheet users since it can be imported directly into spreadsheet packages.

The following examples show how a single node is represented in each data format. For brevity's sake, only a subset of the possible attributes are shown:

`````{tab-set}

````{tab-item} GeoPackage

```{sqltable}
:connection_string: sqlite:///../examples/geopackage/network.gpkg
SELECT
    id,
    "The node's coordinates as a GeoPackage SQL Geometry Binary Format blob" as geom,
    name,
    status,
    accessPoint
FROM
    nodes
LIMIT
    1
```

````

````{tab-item} JSON

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
    :jsonpointer: /networks/0/nodes/0
    :include_only: id,name,status,location,accessPoint
    :expand: location,coordinates
    :title: JSON
```

````

````{tab-item} CSV

```{csv-filter}
:header-rows: 1
:widths: auto
:file: ../../examples/csv/nodes.csv
:included_cols: 1,2,5,6,19
:include: {1: '1'}
```

````

`````

```{seealso}

* [Data formats reference](../reference/data_formats/index.md)
* [How to format data for publication](../guidance/publication.md#how-to-format-data)

```
