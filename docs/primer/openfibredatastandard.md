# The Open Fibre Data Standard

This page provides an introduction to the Open Fibre Data Standard (OFDS), the reasons for using it and what OFDS data looks like.

## What is the Open Fibre Data Standard?

The OFDS is a data standard for the publication of open fibre data. It describes what data to publish about fibre optic networks in order to meet a range of use cases and how to structure and format that data for publication and use.

The OFDS provides:
- A common structured data model, including a schema, codelists, definitions and rules that need to be followed.
- Publication formats to meet a range of use cases.
- Guidance and tooling to support the publication and use of data

## Why use the Open Fibre Data Standard?

Data standards resolve ambiguity by defining the structure and meaning of data. Standardised data is easier for people and systems to interpret than non-standardised data:

- Without standards, data users or intermediaries have to do the hard work of making sense of different datasets and developing dataset-specific methodologies and tools.

- With standards, users have access to information about the structure and meaning of data and can develop reusable tools and methodologies that can be applied to many different datasets.

```{admonition} Standardisation in the fibre context
The [supply-side research](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/discussions/5) identified a variety of units and notations for specifying the capacity of a fibre-optic link: Mbps, Gbps, STM notation and E-carrier notation. This lack of standardisation presents a challenge to users who want to compare the capacity of different links and networks.

Since all of the above units can be converted into Gbps, OFDS requires that publishers specify link capacity in Gbps. This approach places the effort of conversion onto the data publisher, where it only needs to happen once, rather than onto data users, each of whom would need to convert the data if it were not standardised.
```

Standards can also ensure that key information is included in a dataset. If data owners do not share key information in their data, then users need to negotiate with each data owner individually.

## What does OFDS data look like?

To meet the needs of different users, OFDS data can be published in three formats: JSON, GeoJSON and CSV. The tabs below provide examples of OFDS data in each format:

::::{tab-set}

:::{tab-item} JSON
The following example shows OFDS data containing a single network in JSON format:

```{eval-rst} 
.. jsoninclude:: ../../examples/json/network-package.json
    :jsonpointer:
    :expand: networks
    :title: JSON
```
:::

:::{tab-item} GeoJSON
The following example shows OFDS data containing a single network in GeoJSON format. OFDS GeoJSON data consists of separate files for nodes and links. Use the dropdown menu to explore an example nodes file and an example links file:

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

:::{tab-item} CSV
The following example shows OFDS data containing a single network in CSV format. OFDS CSV data consists of multiple tables to reflect the nested nature of the schema. Only the network table is shown here:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../examples/csv/networks.csv
```
:::

::::

To learn more about the use cases for each format, read the [guidance on how to format data for publication](../guidance/publication.md#how-to-format-data-for-publication). For details of the structure of the OFDS schema, read the [schema reference](../reference/schema.md). For details of the rules and specifications for publishing OFDS data in each format, read the [publication formats reference](../reference/publication_formats.md).