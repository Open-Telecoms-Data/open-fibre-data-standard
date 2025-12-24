# GeoPackage

This page describes a standardised representation of the [OFDS data model](../schema.md) as a [GeoPackage](https://www.geopackage.org/). A GeoPackage is a [SQLite](https://sqlite.org/) database. This page provides an [overview](#overview) of the structure of an OFDS GeoPackage, and detailed [definitions](#table-definitions) for each of the tables in the database.

The OFDS GeoPackage format is based on [GeoPackage 1.4.0](https://www.geopackage.org/spec140/), including the [GeoPackage Schema Extension](https://www.geopackage.org/spec140/#extension_schema) and [GeoPackage Related Tables Extension](https://docs.ogc.org/is/18-000/18-000.html).

## Template

The [OFDS GeoPackage template](../../../schema/geopackage/network-schema.gpkg) implements the structure described on this page.

```{tip}
You can explore the structure of the OFDS GeoPackage template in common GIS tools such as [QGIS](https://qgis.org/), or you can connect directly to the SQLite database using your preferred SQL client. 
```

## Overview

The following diagram illustrates how the main entities and relationships in the OFDS data model are represented in an OFDS GeoPackage. Features (spatial entities) are coloured yellow, non-spatial entities are coloured blue, and associative tables (M:N relationships) are coloured grey.

```{mermaid} geopackage.mmd
:zoom:
```

### Features (spatial entities)

Nodes and spans are represented as features in [Vector Feature User Data Tables](https://www.geopackage.org/spec140/#feature_user_tables), which contain both geometries and attributes.

```{dropdown} Example: Nodes
:animate: fade-in-slide-down
:chevron: down-up

[Nodes](../schema.md#node) are spatial entities with a Point geometry so they are represented as spatial features in the [`nodes` vector feature user data table](#nodes).

```

### Non-spatial entities

Non-spatial entities, such as organisations, are represented as non-spatial attribute sets in [Attributes User Data Tables](https://www.geopackage.org/spec140/#attributes_user_tables), which contain only attributes and no geometries.

```{dropdown} Example: Organisations
:animate: fade-in-slide-down
:chevron: down-up

[Organisations](../schema.md#organisation) are non-spatial entities (they have no associated geometry) so they are represented as non-spatial attribute sets in the [`organisations` attributes user data table](#organisations).

```

### One-to-many relationships

One-to-many (1:N) relationships between entities in the OFDS data model, such as a [network](../schema.md#network) with many [nodes](../schema.md#node), are represented as [foreign key](https://en.wikipedia.org/wiki/Foreign_key) relationships. Attributes of type array in the OFDS data model, such as a [span](../schema.md#span)'s transmission medium are also represented as foreign key relationships.


````{dropdown} Example: Networks and nodes
:animate: fade-in-slide-down
:chevron: down-up

The 1:N relationship between a network and the nodes that belong to it is represented as a foreign key (`network_id`) in the [`nodes` table](#nodes) that references the `id` field in the [`networks` table](#networks).

```{mermaid}

    erDiagram
        direction TB
        networks ||--o{ nodes : ""
        networks {
            INTEGER id PK
            TEXT name
    
        }
        nodes {
            INTEGER id PK
            INTEGER network_id FK
            BLOB geom
        }

```

````

### Many-to-many relationships

Many-to-many (M:N) relationships, such as a node with many network providers, are represented as [User-Defined Mapping Tables](https://docs.ogc.org/is/18-000/18-000.html#user_defined_mapping_table).

````{dropdown} Example: M:N relationships
:animate: fade-in-slide-down
:chevron: down-up

The M:N relationship between a [node](../schema.md#node) and its network providers (the organisations that operate active network infrastructure located at the node) is represented by the `relation_nodes_networkProviders` user-defined mapping table, which relates records in the [`nodes` table](#nodes) to records in the [`organisations` table](#organisations).  

```{mermaid}

    erDiagram
        direction TB
        nodes ||--o{ relation_nodes_networkProviders : ""
        relation_nodes_networkProviders }o--|| organisations : ""
        nodes {
            INTEGER id PK
            BLOB geom
        }
        relation_nodes_networkProviders {
            INTEGER base_id FK
            INTEGER related_id FK
        }
        organisations {
            INTEGER id PK
            TEXT name
        }

```

````

### Codelists

Some attributes in the OFDS data model refer to [codelists](../codelists.md) to limit and standardise the possible values of the attribute. 

The representation of attributes that reference a codelist depends on whether the attribute takes a single value or an array of values from the codelist, and on whether the codelist is closed (i.e. the attributes value must belong to the codelist) or open (i.e. the attribute can take values that do not belong to the codelist):

Attribute data type | Codelist type | Representation | Example
--- | --- | --- | ---
Text | Closed | A column whose value is constrained to the codelist by an enum defined using the GeoPackage Schema Extension. | The Node Status attribute is represented by the `status` column in the [`nodes` table](#nodes), with an enum defined for the codes in the [nodeStatus codelist](../codelists.md#nodestatus).
Text | Open | A column with a foreign key relationship to a table containing the values in the codelist. | The Contract Type attribute is represented by the `type` column in the [`contracts` table](#contracts), with a foreign key to the `codelist_open_contractType` [codelist table](#codelist-tables), which contains the codes in the [contractType codelist](../codelists.md#contracttype).
Array | Open or Closed | An M:N relationship between the Vector Feature or Attributes User Data Table that represents the entity to which it belongs, and a table containing the values in the codelist. | The Node Type attribute is represented by the `type` column in the [`nodes` table](#nodes), with an M:N relationship (`relation_nodes_type`) to the `codelist_open_nodeType` [codelist table](#codelist-tables), which contains the codes in the [nodeType codelist](../codelists.md#nodetype).

## Table definitions

### Vector feature user data tables

Vector Feature User Data Tables represent spatial entities in the OFDS data model.

````{dropdown} nodes
:name: nodes
:color: primary
:animate: fade-in-slide-down
:chevron: down-up

Entity: [Node](../schema.md#node)

```{csv-table}
:file: ../../../schema/geopackage/table_definitions/nodes.csv
```
````

````{dropdown} spans
:name: spans
:color: primary
:animate: fade-in-slide-down
:chevron: down-up

Entity: [Span](../schema.md#span)

```{csv-table}
:file: ../../../schema/geopackage/table_definitions/spans.csv
```
````

### Attributes user data tables

Attributes User Data Tables represent non-spatial entities in the OFDS data model.

````{dropdown} networks
:name: networks
:color: info
:animate: fade-in-slide-down
:chevron: down-up

Entity: [Network](../schema.md#network)

```{csv-table}
:file: ../../../schema/geopackage/table_definitions/networks.csv
```
````

````{dropdown} phases
:name: phases
:color: info
:animate: fade-in-slide-down
:chevron: down-up

Entity: [Phase](../schema.md#phase)

```{csv-table}
:file: ../../../schema/geopackage/table_definitions/phases.csv
```
````

````{dropdown} organisations
:name: organisations
:color: info
:animate: fade-in-slide-down
:chevron: down-up

Entity: [Organisation](../schema.md#organisation)

```{csv-table}
:file: ../../../schema/geopackage/table_definitions/organisations.csv
```
````

````{dropdown} contracts
:name: contracts
:color: info
:animate: fade-in-slide-down
:chevron: down-up

Entity: [Contract](../schema.md#contract)

```{csv-table}
:file: ../../../schema/geopackage/table_definitions/contracts.csv
```
````

````{dropdown} contracts_documents
:name: contracts_documents
:color: info
:animate: fade-in-slide-down
:chevron: down-up

Entity: [Document](../schema.md#document)

```{csv-table}
:file: ../../../schema/geopackage/table_definitions/contracts_documents.csv
```
````

````{dropdown} nodes_internationalConnections
:name: nodes_internationalConnections
:color: info
:animate: fade-in-slide-down
:chevron: down-up

Entity: [International connection](../schema.md#international-connection)

```{csv-table}
:file: ../../../schema/geopackage/table_definitions/nodes_internationalConnections.csv
```
````

### Codelist tables

Each codelist table has the following columns:

```{csv-table}
:header: Name,Type,Not Null,Auto Increment

id,INTEGER,FALSE,TRUE
code,TEXT,FALSE,FALSE
description,TEXT,FALSE,FALSE
```

An OFDS GeoPackage includes the following codelist tables:

```{csv-table}
:header: Table,Codelist
:file: ../../../schema/geopackage/table_definitions/codelist_tables.csv

```

### User-defined mapping tables

Each user defined mapping table has the following columns:

```{csv-table}
:header: Name,Type,Not Null,Auto Increment

base_id,INTEGER,TRUE,TRUE
related_id,INTEGER,TRUE,TRUE

```

An OFDS GeoPackage includes the following user-defined mapping tables:

```{csv-table}
:header: Table,base_id FK,related_id FK
:file: ../../../schema/geopackage/table_definitions/mapping_tables.csv


```
