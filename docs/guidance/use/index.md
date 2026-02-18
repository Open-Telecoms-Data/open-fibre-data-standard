<!-- docs-type: how-to-guides https://diataxis.fr/how-to-guides/ -->

# How to use OFDS data

```{admonition} 0.3.0 release
Welcome to the Open Fibre Data Standard 0.3.0 release.

We want to hear your feedback on the standard and its documentation. For general feedback, questions and suggestions, you can comment on an existing [discussion](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/discussions) or start a new one. For bug reports or feedback on specific elements of the data model and documentation, you can comment on the issues in the [issue tracker](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues) or you can [create a new issue](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/new/choose).

To comment on or create discussions and issues, you need to [sign up for a free GitHub account](https://github.com/signup). If you prefer to provide feedback privately, you can email [info@opentelecomdata.net](mailto:info@opentelecomdata.net).
```

This page provides [examples](#examples) that demonstrate how to use OFDS data in common tools and [how-to guides](#how-to-guides) for specific topics.

## Examples

### Leaflet

The [Leaflet example](leaflet.ipynb) shows how to use Python, Leaflet and Folium to visualise OFDS JSON data.

### QGIS

The [OFDS QGIS plugin](https://github.com/Open-Telecoms-Data/ofds-qgis-plugin) provides support for importing OFDS JSON data into [QGIS](https://qgis.org/):

1. [Install QGIS](https://qgis.org/resources/installation-guide/)
1. [Install the OFDS QGIS plugin](https://github.com/Open-Telecoms-Data/ofds-qgis-plugin?tab=readme-ov-file#installation)
1. Download the [example OFDS JSON file](../../../examples/json/network-package.json)
1. [Create a new project in QGIS and add OFDS layers](https://github.com/Open-Telecoms-Data/ofds-qgis-plugin?tab=readme-ov-file#1-initial-project-setup)
1. [Import](https://github.com/Open-Telecoms-Data/ofds-qgis-plugin?tab=readme-ov-file#workflow-b-edit-an-existing-ofds-dataset) the example OFDS JSON file
1. Explore the [attribute table](https://docs.qgis.org/3.22/en/docs/user_manual/working_with_vector/attribute_table.html) for the nodes and spans layers and use the [GeoPackage reference](../../reference/publication_formats/geopackage/index.md) to understand the layer structure and the meaning of the attributes.

## How to guides

### How to plot coordinates accurately

Coordinates in OFDS data are specified in the `urn:ogc:def:crs:OGC::CRS84` [coordinate reference system](../../reference/crs.md) (CRS). To create accurate maps, you need need to set the correct coordinate reference system when using OFDS data.

You also need to pay careful attention to coordinate ordering. `urn:ogc:def:crs:OGC::CRS84` is equivalent to EPSG:4326 with reversed axes so, if it is not supported by the tool that you are using, you can set your CRS to EPSG:4326 and ensure that you read coordinates in longitude, latitude order.

For more information on transforming coordinates from one CRS to another, see [how to transform coordinates to the correct coordinate reference system](../publication.md#how-to-transform-coordinates-to-the-correct-coordinate-reference-system).

```{eval-rst}
.. toctree::
   :hidden:

   leaflet
```
