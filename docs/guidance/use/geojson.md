# How to convert OFDS data to GeoJSON format

OFDS does not define a schema for GeoJSON data. However, OFDS data in any of its supported formats can be converted to GeoJSON using standard tools and libraries.

This page introduces the key concepts behind converting OFDS data to GeoJSON and helps you decide which approach is right for your use case. Detailed instructions are provided on two separate pages:

* [Convert nodes and spans to GeoJSON](geojson-prebuilt.md) — ready-to-use scripts that convert nodes and spans from any OFDS format to a fully-dereferenced GeoJSON output
* [Writing a custom query](geojson-custom.md) — examples showing how to write your own SQL or Python to select specific fields or handle formats the pre-built scripts don't cover

## Which approach should I use?

**Use the [pre-built scripts](geojson-prebuilt.md) if:**

* You want nodes and spans as GeoJSON with all fields resolved to human-readable values
* You're working with [GeoPackage](../../reference/data_formats/geopackage/index.md), [CSV](../../reference/data_formats/csv.md) or [JSON](../../reference/data_formats/json/index.md) data
* You want to use ogr2ogr, GeoPandas or QGIS

**[Write a custom query](geojson-custom.md) if:**

* You need to select a specific subset of fields
* You want to apply filters (e.g. only operational spans)
* You need to join to tables or fields not covered by the pre-built scripts

## Introduction

The OFDS data model includes both **spatial entities** (represented in GeoJSON as features with an associated geometry) and **non-spatial entities**, which have no associated geometry. For example, nodes and spans are spatial entities and organisations are non-spatial entities.

When converting data to GeoJSON format, you can either:

* **Convert both spatial and non-spatial layers**: In this case, non-spatial layers appear as `FeatureCollection` objects where every feature has a `null` geometry.
* **Convert only spatial layers**: You can then keep or export non-spatial layers in a format more suited to non-spatial data, such as CSV or a standard JSON object.

### Relational data and dereferencing

The OFDS data model also includes one-to-many and many-to-many relationships between entities. These are represented as foreign-key relationships in GeoPackage data or identifier references in JSON and CSV data.

Because GeoJSON is a "flat" format, you might want to **dereference** these relationships before converting your data to GeoJSON format. Dereferencing is the process of joining data from separate tables into a single record so that attributes from referenced entities (such as an organisation's name) are included directly in the properties of spatial features.

This ensures that popups, labels, and map legends work immediately in GIS software and web maps without requiring additional lookups.
