# Schema reference

## Structure

## Components

### CoordinateReferenceSystem

Coordinates in all OFDS data must be specified in the coordinate reference system required by GeoJSON:

> The coordinate reference system for all GeoJSON coordinates is a geographic coordinate reference system, using the World Geodetic System 1984 (WGS 84) [WGS84] datum, with longitude and latitude units of decimal degrees.  This is equivalent to the coordinate reference system identified by the Open Geospatial Consortium (OGC) URN urn:ogc:def:crs:OGC::CRS84.

The `CoordinateReferenceSystem` object references the CRS by `name` and `uri`. Its properties must be set to the following values:

* `name`: urn:ogc:def:crs:OGC::CRS84
* `uri`: http://www.opengis.net/def/crs/OGC/1.3/CRS84

`urn:ogc:def:crs:OGC::CRS84` denotes WGS84 with the order longitude, latitude. It is equivalent to EPSG:4326 with reversed axes.

For more information, see [How to transform coordinates to the correct coordinate reference system](../guidance/publication.md#how-to-transform-coordinates-to-the-correct-coordinate-reference-system).