# How to convert OFDS data to GeoJSON format

OFDS data in any of its supported [data formats](../../reference/data_formats/index.md) (GeoPackage, CSV, and JSON) can be converted to GeoJSON using standard tools and libraries.

This page helps you decide which approach is right for your use case, and introduces the key concepts behind converting OFDS data to GeoJSON. Detailed instructions are provided on two separate pages:

* [Use a pre-built script](prebuilt/index.md) - ready-to-use queries and scripts that convert nodes and spans from any OFDS format to a dereferenced GeoJSON output
* [Write a custom script](custom/index.md) - examples showing how to write your own SQL or Python to produce a customised GeoJSON output

## Which approach should I use?

**[Use the pre-built scripts](prebuilt/index.md) if:**

* You want nodes and spans as GeoJSON with all references resolved to human-readable values
* You're working with [GeoPackage](../../reference/data_formats/geopackage/index.md), [CSV](../../reference/data_formats/csv.md) or [JSON](../../reference/data_formats/json/index.md) data
* You want to use ogr2ogr, GeoPandas or QGIS

**[Write a custom script](custom/index.md) if:**

* You need to select a specific subset of fields
* You want to apply filters (e.g. only operational spans)
* You need to customise which fields are returned when resolving references

## Spatial and non-spatial data

The OFDS data model includes both **spatial entities** (represented in GeoJSON as features with an associated geometry) and **non-spatial entities**, which have no associated geometry. For example, nodes and spans are spatial entities and organisations are non-spatial entities.

When converting data to GeoJSON format, you can:

* **Convert both spatial and non-spatial layers**: In this case, non-spatial layers appear as `FeatureCollection` objects where every feature has a `null` geometry.
* **Convert only spatial layers**: You can then keep or export non-spatial layers in a format more suited to non-spatial data, such as CSV or a standard JSON object.

## Relational data and dereferencing

The OFDS data model also includes one-to-many and many-to-many relationships between entities. These are represented as foreign-key relationships in GeoPackage data or identifier references in JSON and CSV data.

Because GeoJSON is a "flat" format, converting OFDS data to GeoJSON typically involves **dereferencing** these relationships. Dereferencing is the process of joining data from separate tables into a single record so that attributes from referenced entities are included directly in the properties of spatial features. 

This ensures that popups, labels, and map legends work immediately in GIS software and web maps without requiring additional lookups.

### Example

In GeoPackage format, `nodes.transmissionMediumOwner` is a reference to the `organisations` table. 

`````{grid} 2
````{grid-item-card} Nodes table
:columns: 8
```{csv-table}
:header-rows: 1
id,name,status,transmissionMediumOwner
1,Accra,operational,1
```
````

````{grid-item-card} Organisations table
:columns: 4
```{csv-table}
:header-rows: 1
id,name
1,FibreCo
```
````
`````

Dereferencing this relationship requires joining the `organisations` table to the `nodes` table in order to return the organisation's name and other details. 

````{card} Dereferenced nodes table
```{csv-table}
:header-rows: 1
id,name,status,transmissionMediumOwner
1,Accra,operational,FibreCo
```
````

```{eval-rst}
.. toctree::
   :hidden:

   prebuilt/index
   custom/index
```