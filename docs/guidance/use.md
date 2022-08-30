# How to use OFDS data

## How to find data

## How to access data

## How to create maps

### How to use the correct coordinate reference system

Coordinates in OFDS data are specified in the `urn:ogc:def:crs:OGC::CRS84` [coordinate reference system](../reference/schema.md#coordinatereferencesystem) (CRS). To create accurate maps, you need need to set the correct coordinate reference system when using OFDS data. 

If you are using OFDS data published in GeoJSON format, then the tool that you are using is likely to default to the correct CRS because `urn:ogc:def:crs:OGC::CRS84` is the default CRS for GeoJSON data.

If you are using OFDS data published in other formats, then you need to pay careful attention to coordinate ordering. `urn:ogc:def:crs:OGC::CRS84` is equivalent to EPSG:4326 with reversed axes so, if it is not supported by the tool that you are using, you can set your CRS to EPSG:4326 and ensure that you read coordinates in longitude, latitude order.

For more information on transforming coordinates from one CRS to another, see [how to transform coordinates to the correct coordinate reference system](publication.md#how-to-transform-coordinates-to-the-correct-coordinate-reference-system).

### How to join links to nodes

## How to analyse data