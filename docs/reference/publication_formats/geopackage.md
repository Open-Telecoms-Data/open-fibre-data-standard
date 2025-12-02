# GeoPackage

This page describes how to represent the [OFDS data model](../schema.md) as a [GeoPackage](https://www.geopackage.org/). It provides an [overview](#overview) of the structure of an OFDS GeoPackage, and detailed [definitions](#table-definitions) for each of the tables in the GeoPackage.

We provide an empty [OFDS GeoPackage template](../../../schema/template.gpkg) that implements the relationships and enums described on this page. The OFDS GeoPackage format is based on GeoPackage 1.Y.Z and uses the [GeoPackage Schema Extension](https://www.geopackage.org/spec140/#extension_schema) and [GeoPackage Related Tables Extension](https://docs.ogc.org/is/18-000/18-000.html).

## Overview

The following diagram illustrates the structure of an OFDS GeoPackage.

Spatial entities in the OFDS data model (nodes and spans) are represented as features in [Vector Feature User Data Tables](https://www.geopackage.org/spec140/#feature_user_tables). Non-spatial entities in the OFDS data model are represented as non-spatial attribute sets in [Attributes User Data Tables](https://www.geopackage.org/spec140/#attributes_user_tables).

One-to-many relationships and array attributes are represented as separate tables with foreign key relationships and many-to-many relationships are represented as [User-Defined Mapping Tables](https://docs.ogc.org/is/18-000/18-000.html#user_defined_mapping_table).

Note that a single OFDS GeoPackage can contain multiple networks.

![OFDS GeoPackage structure](../../_static/geopackage_structure.png)

## Table definitions

### Vector Feature User Data Tables

````{dropdown} nodes
:name: nodes
:color: primary
:animate: fade-in-slide-down
:chevron: down-up

```{csv-table}
:file: ../../../metadata_reports/nodes.csv
```
````

````{dropdown} spans
:name: spans
:color: primary
:animate: fade-in-slide-down
:chevron: down-up

```{csv-table}
:file: ../../../metadata_reports/spans.csv
```
````

### Attributes User Data Tables

````{dropdown} networks
:name: networks
:color: info
:animate: fade-in-slide-down
:chevron: down-up

```{csv-table}
:file: ../../../metadata_reports/networks.csv
```
````

````{dropdown} phases
:name: phases
:color: info
:animate: fade-in-slide-down
:chevron: down-up

```{csv-table}
:file: ../../../metadata_reports/phases.csv
```
````

````{dropdown} organisations
:name: organisations
:color: info
:animate: fade-in-slide-down
:chevron: down-up

```{csv-table}
:file: ../../../metadata_reports/organisations.csv
```
````

````{dropdown} contracts
:name: contracts
:color: info
:animate: fade-in-slide-down
:chevron: down-up

```{csv-table}
:file: ../../../metadata_reports/contracts.csv
```
````

````{dropdown} contracts_documents
:name: contracts_documents
:color: info
:animate: fade-in-slide-down
:chevron: down-up

```{csv-table}
:file: ../../../metadata_reports/contracts_documents.csv
```
````

````{dropdown} nodes_internationalConnections
:name: nodes_internationalConnections
:color: info
:animate: fade-in-slide-down
:chevron: down-up

```{csv-table}
:file: ../../../metadata_reports/nodes_internationalConnections.csv
```
````

### User-Defined Mapping Tables

````{dropdown} relation_nodes_networkProviders
:name: relation_nodes_networkProviders
:color: secondary
:animate: fade-in-slide-down
:chevron: down-up

```{csv-table}
:file: ../../../metadata_reports/relation_nodes_networkProviders.csv
```
````

````{dropdown} relation_spans_networkProviders
:name: relation_spans_networkProviders
:color: secondary
:animate: fade-in-slide-down
:chevron: down-up

```{csv-table}
:file: ../../../metadata_reports/relation_spans_networkProviders.csv
```
````

````{dropdown} relation_phases_funders
:name: relation_phases_funders
:color: secondary
:animate: fade-in-slide-down
:chevron: down-up

```{csv-table}
:file: ../../../metadata_reports/relation_phases_funders.csv
```
````

````{dropdown} relation_contracts_relatedPhases
:name: relation_contracts_relatedPhases
:color: secondary
:animate: fade-in-slide-down
:chevron: down-up

```{csv-table}
:file: ../../../metadata_reports/relation_contracts_relatedPhases.csv
```
````

## TO DO

- add link to GeoPackage template
- specify GeoPackage version
- add diagram
- integrate metadata script into manage.py, check that foreign keys and enums are pulled in correctly.
