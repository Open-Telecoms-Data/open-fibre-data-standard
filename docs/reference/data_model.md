<!-- docs-type: reference https://diataxis.fr/reference/ -->

# Data model

The OFDS data model is a logical model that sets out the entities, attributes and relationships needed to describe a fibre network, without specifying how to represent them in a particular data format. This page provides an [overview](#overview) of the data model and [reference tables](#entities) for each entity.

```{seealso}
OFDS also defines standardised representations of the data model in different [data formats](data_formats/index.md), which can be used to store, publish or exchange OFDS data.
```

## Overview

The following diagram provides an overview of the key entities and relationships in the OFDS data model.

```{mermaid} data_model.mmd
:zoom:
```

```{seealso}
For an introduction to key concepts and relationships covered in the OFDS data model, read the [scope, focus and key concepts primer](../primer/scopeandkeyconcepts.md).
```

## Entities

This section provides a definition for each entity in the data model, including a description, relationships to other entities, and attributes.

Relationships are listed from the perspective of the entity that holds the reference. Inverse relationships are not shown separately.See the [#overview] diagram for a full view of how entities relate to each other.

Some attributes refer to [codelists](codelists.md) to limit and standardise the possible values of the attribute. In such cases, a link to the codelist is provided in the attribute's description.

### Network

````{dropdown} Description
:open:
:animate: fade-in-slide-down
:chevron: down-up
:icon: book
:name: network-description
```{jsoninclude-quote} ../../_readthedocs/html/network-schema.json
:jsonpointer: /description
```
````

`````{dropdown} Relationships
:animate: fade-in-slide-down
:chevron: down-up
:icon: link
:name: network-relationships
````{csv-table}
:file: network-relationships.csv
:header-rows: 1

````

`````

````{dropdown} Attributes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows
:name: network-attributes
```{jsonschema} ../../_readthedocs/html/network-schema.json
:include: id,identifier,name,website,publicationDate,collectionDate,accuracy,accuracyDetails,language
:nocrossref:
:addtargets:
:prefix: data_model
```

````

### Phase

````{dropdown} Description
:open:
:animate: fade-in-slide-down
:chevron: down-up
:icon: book
:name: phase-description
```{jsoninclude-quote} ../../_readthedocs/html/network-schema.json
:jsonpointer: /$defs/Phase/description
```
````

`````{dropdown} Relationships
:animate: fade-in-slide-down
:chevron: down-up
:icon: link
:name: phase-relationships
````{csv-table}
:file: phase-relationships.csv
:header-rows: 1

````

`````

````{dropdown} Attributes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows
:name: phase-attributes
```{jsonschema} ../../_readthedocs/html/network-schema.json
:pointer: /$defs/Phase
:include: id,name,description
:nocrossref:
:addtargets:
:prefix: data_model
```

````

### Node

````{dropdown} Description
:open:
:animate: fade-in-slide-down
:chevron: down-up
:icon: book
:name: node-description
```{jsoninclude-quote} ../../_readthedocs/html/network-schema.json
:jsonpointer: /$defs/Node/description
```
````

`````{dropdown} Relationships
:animate: fade-in-slide-down
:chevron: down-up
:icon: link
:name: node-relationships

````{csv-table}
:file: node-relationships.csv
:header-rows: 1

````

`````

````{dropdown} Attributes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows
:name: node-attributes
```{jsonschema} ../../_readthedocs/html/network-schema.json
:pointer: /$defs/Node
:include: id,name,status,location,address/streetAddress,address/locality,address/region,address/postalCode,address/country,type,supportingInfrastructure/type,supportingInfrastructure/description,supportingInfrastructure/spareCapacity,accessPoint,internationalConnections,power,technologies
:collapse: location,internationalConnections
:nocrossref:
:addtargets:
:prefix: data_model
```

````

### Span

````{dropdown} Description
:open:
:animate: fade-in-slide-down
:chevron: down-up
:icon: book
:name: span-description
```{jsoninclude-quote} ../../_readthedocs/html/network-schema.json
:jsonpointer: /$defs/Span/description
```
````

`````{dropdown} Relationships
:animate: fade-in-slide-down
:chevron: down-up
:icon: link
:name: span-relationships
````{csv-table}
:file: span-relationships.csv
:header-rows: 1

````

`````

````{dropdown} Attributes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows
:name: span-attributes
```{jsonschema} ../../_readthedocs/html/network-schema.json
:pointer: /$defs/Span
:include: id,name,status,readyForServiceDate,directed,route,transmissionMedium,deployment,supportingInfrastructure/type,supportingInfrastructure/description,supportingInfrastructure/spareCapacity,codeployment,cableType,darkFibre,fibreType,fibreTypeDetails/fibreSubtype,fibreTypeDetails/description,fibreCount,fibreLength,technologies,capacity,capacityDetails/description,countries
:collapse: route
:nocrossref:
:addtargets:
:prefix: data_model
```

````

````{dropdown} Additional information
:animate: fade-in-slide-down
:chevron: down-up
:icon: info
:name: span-additional-information
#### Equipped capacity

`Span.capacity` is defined as the equipped capacity of a span:

```{jsoninclude-quote} ../../_readthedocs/html/network-schema.json
:jsonpointer: /$defs/Span/properties/capacity/description
```

There are several measures of capacity in fibre networks[^itu-attribution]:

* **Potential capacity** refers to the total theoretical bandwidth that is available, including lit (turned on) and unlit (dark fibre) capacity.
* **Equipped capacity**, also known as lit capacity, refers to bandwith that is turned on and ready for use.
* **Purchased capacity**, also known as contracted capacity, covers bandwidth put into service, but not all of which is used; some is held in reserve for restoration or redundancy
* **Used capacity** covers bandwidth that is available to carry traffic.

```{image} ../_static/capacity-diagram.svg
:alt: Capacity diagram
:width: 70%
:align: center
```

[^itu-attribution]: Text and diagram adapted from the [ITU Handbook for the collection of administrative data on telecommunications/ICT, 2020 edition](https://www.itu.int/en/ITU-D/Statistics/Pages/publications/handbook.aspx).

````

### Organisation

````{dropdown} Description
:open:
:animate: fade-in-slide-down
:chevron: down-up
:icon: book
:name: organisation-description
```{jsoninclude-quote} ../../_readthedocs/html/network-schema.json
:jsonpointer: /$defs/Organisation/description
```
````

````{dropdown} Attributes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows
:name: organisation-attributes
```{jsonschema} ../../_readthedocs/html/network-schema.json
:pointer: /$defs/Organisation
:include: id,name,identifier/id,identifier/scheme,identifier/legalName,identifier/uri,country,roles,roleDetails,website,logo
:nocrossref:
:addtargets:
:prefix: data_model
```

````

### Contract

````{dropdown} Description
:open:
:animate: fade-in-slide-down
:chevron: down-up
:icon: book
:name: contract-description
```{jsoninclude-quote} ../../_readthedocs/html/network-schema.json
:jsonpointer: /$defs/Contract/description
```
````

`````{dropdown} Relationships
:animate: fade-in-slide-down
:chevron: down-up
:icon: link
:name: contract-relationships
````{csv-table}
:file: contract-relationships.csv
:header-rows: 1

`````

````{dropdown} Attributes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows
:name: contract-attributes
```{jsonschema} ../../_readthedocs/html/network-schema.json
:pointer: /$defs/Contract
:include: id,title,description,type,value/amount,value/currency,dateSigned
:nocrossref:
:addtargets:
:prefix: data_model
```

````

### Wayleave

````{dropdown} Description
:open:
:animate: fade-in-slide-down
:chevron: down-up
:icon: book
:name: wayleave-description
```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /$defs/Wayleave/description
```
````

`````{dropdown} Relationships
:animate: fade-in-slide-down
:chevron: down-up
:icon: link
:name: wayleave-relationships
````{csv-table}
:file: wayleave-relationships.csv
:header-rows: 1

````

`````

````{dropdown} Attributes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows
:name: wayleave-attributes
```{jsonschema} ../../schema/network-schema.json
:pointer: /$defs/Wayleave
:include: id,yearSigned,term/indefinite,term/years,cost/recurring,cost/perMetre/amount,cost/perMetre/currency
:nocrossref:
:addtargets:
:prefix: data_model
```

````

### Document

````{dropdown} Description
:open:
:animate: fade-in-slide-down
:chevron: down-up
:icon: book
:name: document-description
```{jsoninclude-quote} ../../_readthedocs/html/network-schema.json
:jsonpointer: /$defs/Document/description
```
````

````{dropdown} Attributes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows
:name: document-attributes
```{jsonschema} ../../_readthedocs/html/network-schema.json
:pointer: /$defs/Document
:include: title,description,url,format
:nocrossref:
:addtargets:
:prefix: data_model
```

````
