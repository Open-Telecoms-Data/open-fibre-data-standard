# The Open Fibre Data Standard

## What is the Open Fibre Data Standard?

The Open Fibre Data Standard (OFDS) is a data standard for the publication of open fibre data. It describes what data to publish about fibre optic networks in order to meet a range of use cases and how to structure and format that data for publication and use.

The OFDS provides:
- A common structured data model, including a schema, codelists, definitions and rules that need to be followed.
- Publication formats to meet a range of use cases.
- Guidance and tooling to support the publication and use of data

## Why use the Open Fibre Data Standard?

Data standards resolve ambiguity by defining the structure and meaning of data. Standardised data is easier for people and systems to interpret than non-standardised data:

- Without standards, data users or intermediaries have to do the hard work of making sense of different datasets and developing dataset-specific methodologies and tools.

- With standards, users have access to information about the structure and meaning of data and can develop reusable tools and methodologies that can be applied to many different datasets.

Standards can also ensure that key information is included in a dataset. If data owners do not share key information in their data, then users need to negotiate with each data owner individually.

## What does OFDS data look like?

OFDS data is open fibre data that validates against the OFDS [schema](../reference/index.md). The 'base' format for OFDS data is [JSON](https://www.json.org/json-en.html), as this reflects the structure of the schema. OFDS data in JSON format is a list of network objects. Each object contains the geospatial, technical and administrative data about a single network.

OFDS data can also be published in [GeoJSON](https://geojson.org/) format to be useful for analysts who want to use GIS tools, and in CSV format to be useful to analysts who want to use spreadsheet tools. The tabs below contains examples of OFDS data in each of these three formats.

::::{tab-set}

:::{tab-item} JSON format
The following example shows OFDS data containing a single network in JSON format:

```{eval-rst} 
.. jsoninclude:: ../../examples/json/network-package.json
    :jsonpointer:
    :expand: networks
    :title: JSON
```
:::

:::{tab-item} GeoJSON format
The following example shows OFDS data containing a single network in GeoJSON format. OFDS GeoJSON data consists of separate files for nodes and links. Use the dropdown menu to explore these two examples:

```{eval-rst} 
.. jsoninclude:: ../../examples/geojson/nodes.geojson
    :jsonpointer:
    :expand: features
    :title: Nodes

.. jsoninclude:: ../../examples/geojson/links.geojson
    :jsonpointer:
    :expand: features
    :title: Links

```
:::

:::{tab-item} CSV Format
The following example shows OFDS data containing a single network in CSV format. OFDS CSV data consists of multiple files to reflect the nested nature of the schema. Only the network level data are shown here:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../examples/csv/networks.csv
```
```
:::

::::

You can find out more about how to publish and use OFDS data in the [guidance](../guidance/index.md). You can read the rules and specifications for publishing OFDS data in different formats in the [publication formats reference](../reference/publication_formats.md).