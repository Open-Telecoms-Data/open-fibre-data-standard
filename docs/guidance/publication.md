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

## How to provide access to data

## How to add additional fields

## How to write a data user guide