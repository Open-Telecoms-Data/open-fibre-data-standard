<!-- docs-type: reference https://diataxis.fr/reference/ -->

# Data model

The OFDS data model is a logical model that sets out the entities, attributes and relationships needed to describe a fibre network, without specifying how to represent them in a particular data format. This page provides an [overview](#overview) of the data model and [reference tables](#entities) for each entity.

```{seealso}
OFDS also defines standardised representations of the data model in different [data formats](publication_formats/index.md), which can be used to store, publish or exchange OFDS data.
```

## Overview

The following diagram provides an overview of the key entities and relationships in the OFDS data model.

```{mermaid} data_model.mmd
:zoom:
```

<br>The network entity is omitted from the diagram for brevity. However, all entities in the data model are associated with a network.

```{seealso}
For an introduction to key concepts and relationships covered in the OFDS data model, read the [scope, focus and key concepts primer](../primer/scopeandkeyconcepts.md).
```

## Entities

This section provides a definition for each entity in the data model, including a description, relationships to other entities, and attributes.

Some attributes refer to [codelists](codelists.md) to limit and standardise the possible values of the attribute. In such cases, a link to the codelist is provided in the attribute's description.

### Network

````{dropdown} Description
:open:
:animate: fade-in-slide-down
:chevron: down-up
:icon: book
```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /description
```
````

`````{dropdown} Relationships
:animate: fade-in-slide-down
:chevron: down-up
:icon: link

````{list-table}
:header-rows: 1
*  - Entity
   - Cardinality
   - Description
*  - [Node](#node)
   - 1:N
   - ```{jsoninclude-quote} ../../schema/network-schema.json
      :jsonpointer: /properties/nodes/description
      ```
*  - [Span](#span)
   - 1:N
   - ```{jsoninclude-quote} ../../schema/network-schema.json
      :jsonpointer: /properties/spans/description
      ```
*  - [Phase](#phase)
   - 1:N
   - ```{jsoninclude-quote} ../../schema/network-schema.json
      :jsonpointer: /properties/phases/description
      ```
*  - [Organisation](#organisation)
   - 1:N
   - ```{jsoninclude-quote} ../../schema/network-schema.json
      :jsonpointer: /properties/organisations/description
      ```
*  - [Contract](#contract)
   - 1:N
   - ```{jsoninclude-quote} ../../schema/network-schema.json
      :jsonpointer: /properties/contracts/description
      ```

````

`````

````{dropdown} Attributes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows

```{jsonschema} ../../schema/network-schema.json
:include: id,name,website,language
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

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /$defs/Phase/description
```
````

`````{dropdown} Relationships
:animate: fade-in-slide-down
:chevron: down-up
:icon: link

````{list-table}
:header-rows: 1
*  - Entity
   - Cardinality
   - Description
*  - [Network](#network)
   - N:1
   -
*  - [Node](#node)
   - 1:N
   -
*  - [Span](#span)
   - 1:N
   -
*  - [Organisation](#organisation)
   - 1:N
   - ```{jsoninclude-quote} ../../schema/network-schema.json
      :jsonpointer: /$defs/Phase/properties/funders/description
      ```
*  - [Contract](#contract)
   - N:1
   -

````

`````

````{dropdown} Attributes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows

```{jsonschema} ../../schema/network-schema.json
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

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /$defs/Node/description
```
````

`````{dropdown} Relationships
:animate: fade-in-slide-down
:chevron: down-up
:icon: link

````{list-table}
:header-rows: 1
*  - Entity
   - Cardinality
   - Description
*  - [Network](#network)
   - N:1
   -
*  - [Phase](#phase)
   - N:1
   - ```{jsoninclude-quote} ../../schema/network-schema.json
      :jsonpointer: /$defs/Node/properties/phase/description
      ```
*  - [Span](#span)
   - M:N
   -
*  - [Organisation](#organisation) (Physical infrastructure provider)
   - N:1
   - ```{jsoninclude-quote} ../../schema/network-schema.json
      :jsonpointer: /$defs/Node/properties/physicalInfrastructureProvider/description
      ```
*  - [Organisation](#organisation) (Network provider)
   - N:M
   - ```{jsoninclude-quote} ../../schema/network-schema.json
      :jsonpointer: /$defs/Node/properties/networkProviders/description
      ```

````

`````

````{dropdown} Attributes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows

```{jsonschema} ../../schema/network-schema.json
:pointer: /$defs/Node
:include: id,name,status,location,address/streetAddress,address/locality,address/region,address/postalCode,address/country,type,accessPoint,power,technologies,internationalConnections
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

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /$defs/Span/description
```
````

`````{dropdown} Relationships
:animate: fade-in-slide-down
:chevron: down-up
:icon: link

````{list-table}
:header-rows: 1
*  - Entity
   - Cardinality
   - Description
*  - [Network](#network)
   - N:1
   -
*  - [Phase](#phase)
   - N:1
   - ```{jsoninclude-quote} ../../schema/network-schema.json
      :jsonpointer: /$defs/Span/properties/phase/description
      ```
*  - [Node](#node) (start)
   - N:1
   - ```{jsoninclude-quote} ../../schema/network-schema.json
      :jsonpointer: /$defs/Span/properties/start/description
      ```
*  - [Node](#node) (end)
   - N:1
   - ```{jsoninclude-quote} ../../schema/network-schema.json
      :jsonpointer: /$defs/Span/properties/end/description
      ```
*  - [Organisation](#organisation) (Physical infrastructure provider)
   - N:1
   - ```{jsoninclude-quote} ../../schema/network-schema.json
      :jsonpointer: /$defs/Span/properties/physicalInfrastructureProvider/description
      ```
*  - [Organisation](#organisation) (Network provider)
   - N:M
   - ```{jsoninclude-quote} ../../schema/network-schema.json
      :jsonpointer: /$defs/Span/properties/networkProviders/description
      ```
*  - [Organisation](#organisation) (Supplier)
   - N:1
   - ```{jsoninclude-quote} ../../schema/network-schema.json
      :jsonpointer: /$defs/Span/properties/supplier/description
      ```

````

`````

````{dropdown} Attributes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows

```{jsonschema} ../../schema/network-schema.json
:pointer: /$defs/Span
:include: id,name,status,readyForServiceDate,directed,route,transmissionMedium,deployment,deploymentDetails/description,darkFibre,fibreType,fibreTypeDetails/fibreSubtype,fibreTypeDetails/description,fibreCount,fibreLength,technologies,capacity,capacityDetails/description,countries
:collapse: route
:nocrossref:
:addtargets:
:prefix: data_model
```

````

### Organisation

````{dropdown} Description
:open:
:animate: fade-in-slide-down
:chevron: down-up
:icon: book

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /$defs/Organisation/description
```
````

`````{dropdown} Relationships
:animate: fade-in-slide-down
:chevron: down-up
:icon: link

````{list-table}
:header-rows: 1
*  - Entity
   - Cardinality
   - Description
*  - [Network](#network)
   - N:1
   -
*  - [Phase](#phase)
   - N:1
   - 
*  - [Node](#node) (Physical infrastructure provider)
   - 1:N
   - 
*  - [Node](#node) (Network provider)
   - M:N
   - 
*  - [Span](#span) (Physical infrastructure provider)
   - 1:N
   - 
*  - [Span](#span) (Network provider)
   - M:N
   - 
*  - [Span](#span) (Supplier)
   - 1:N
   - 

````

`````

````{dropdown} Attributes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows

```{jsonschema} ../../schema/network-schema.json
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

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /$defs/Contract/description
```
````

`````{dropdown} Relationships
:animate: fade-in-slide-down
:chevron: down-up
:icon: link

````{list-table}
:header-rows: 1
*  - Entity
   - Cardinality
   - Description
*  - [Network](#network)
   - N:1
   -
*  - [Phase](#phase)
   - 1:N
   - ```{jsoninclude-quote} ../../schema/network-schema.json
      :jsonpointer: /$defs/Contract/properties/relatedPhases/description
      ```

````

`````

````{dropdown} Attributes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows

```{jsonschema} ../../schema/network-schema.json
:pointer: /$defs/Contract
:include: id,title,description,type,value/amount,value/currency,dateSigned
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

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /$defs/Document/description
```
````

`````{dropdown} Relationships
:animate: fade-in-slide-down
:chevron: down-up
:icon: link

````{list-table}
:header-rows: 1
*  - Entity
   - Cardinality
   - Description
*  - [Network](#network)
   - N:1
   -
*  - [Contract](#contract)
   - N:1
   -

````

`````

````{dropdown} Attributes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows

```{jsonschema} ../../schema/network-schema.json
:pointer: /$defs/Document
:nocrossref:
:addtargets:
:prefix: data_model
```

````
