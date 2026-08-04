# Network schema

The network schema provides the authoritative definition of the structure of a network object, the meaning of each property, and the rules that must be followed to publish, store or exchange data that conforms to the OFDS data model as JSON data. The schema is used to validate the structure and format of OFDS JSON data.

```{note}

Use the canonical schema URL to make sure that your software, documentation or other resources refer to the specific version of the schema with which they were tested. The canonical URL for version 0.4.0 is:

[https://standard.ofds.info/en/0\_\_4\_\_0/network-schema.json](https://standard.ofds.info/en/0__4__0/network-schema.json)

```

This page presents the schema in an [interactive browser](#browser) and in [reference tables](#reference-tables) with additional information in paragraphs. You can also download the canonical version of the schema as [JSON Schema](../../../../_readthedocs/html/network-schema.json) or download it as a [CSV spreadsheet](../../../../schema/network-schema.csv).

```{note}
   If any conflicts are found between the text on this page and the text within the schema, the text within the schema takes precedence.
```

```{seealso}
   For more information on the data types, string formats and other validation keywords used in the network schema, refer to the JSON Schema Reference documentation:

   - [Data types](https://json-schema.org/understanding-json-schema/reference/type)
   - [String formats](https://json-schema.org/understanding-json-schema/reference/type#built-in-formats)
   - [Validation keywords](https://json-schema.org/understanding-json-schema/keywords)
```

## Browser

Click on schema elements to expand the tree, or use the '+' icon to expand all elements. Use { } to view the underlying schema for any section. Required properties are indicated in **bold**.

<script src="../../../../_static/docson/widget.js" data-schema="../../network-schema.json"></script>

## Reference tables

This section presents each property in the schema in tables with additional information in paragraphs. Required properties are indicated in the **Required** column. For properties that reference sub-schemas, a link is provided to a table with details of the sub-schema.

### Network

The top-level object in the network schema is a network, defined as:

```{jsoninclude-quote} ../../../../_readthedocs/html/network-schema.json
:jsonpointer: /description
```

A network has the following properties:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../../../_readthedocs/html/network-schema.json
:collapse: nodes,spans,phases,organisations,contracts,links,wayleaves
:include: id,identifier,name,nodes,spans,phases,organisations,contracts,website,publisher/name,publisher/identifier/id,publisher/identifier/scheme,publisher/identifier/legalName,publicationDate,collectionDate,crs/name,crs/uri,accuracy,accuracyDetails,language,links,wayleaves
:addtargets:
:prefix: json
```

:::

:::{tab-item} Example

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
   :jsonpointer: /networks/0
   :title: Example
```

:::

::::

### Node

`Node` is defined as:

```{jsoninclude-quote} ../../../../_readthedocs/html/network-schema.json
:jsonpointer: /$defs/Node/description
```

This sub-schema is referenced by the following properties:

- [`nodes`](json,network-schema.json,,nodes)

Each `Node` has the following properties:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../../../_readthedocs/html/network-schema.json
:pointer: /$defs/Node
:addtargets:
:prefix: json
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
 :jsonpointer: /networks/0/nodes
 :title: nodes
```

:::

::::

### Span

`Span` is defined as:

```{jsoninclude-quote} ../../../../_readthedocs/html/network-schema.json
:jsonpointer: /$defs/Span/description
```

This sub-schema is referenced by the following properties:

- [`spans`](json,network-schema.json,,spans)

Each `Span` has the following properties:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../../../_readthedocs/html/network-schema.json
:pointer: /$defs/Span
:collapse: id,name,phase,status,readyForServiceDate,start,end,directed,route,transmissionMediumOwner,networkProviders,supplier,transmissionMedium,deployment,darkFibre,fibreType,fibreTypeDetails,fibreCount,fibreLength,technologies,capacity,capacityDetails,countries
:addtargets:
:prefix: json
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
 :jsonpointer: /networks/0/spans
 :title: spans
```

:::

::::

### Phase

`Phase` is defined as:

```{jsoninclude-quote} ../../../../_readthedocs/html/network-schema.json
:jsonpointer: /$defs/Phase/description
```

This sub-schema is referenced by the following properties:

- [`phases`](json,network-schema.json,,phases)

Each `Phase` has the following properties:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../../../_readthedocs/html/network-schema.json
:pointer: /$defs/Phase
:collapse: id,name,description,funders
:addtargets:
:prefix: json
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
 :jsonpointer: /networks/0/phases
 :title: phases
```

:::

::::

### Organisation

`Organisation` is defined as:

```{jsoninclude-quote} ../../../../_readthedocs/html/network-schema.json
:jsonpointer: /$defs/Organisation/description
```

This sub-schema is referenced by the following properties:

- [`organisations`](json,network-schema.json,,organisations)

Each `Organisation` has the following properties:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../../../_readthedocs/html/network-schema.json
:pointer: /$defs/Organisation
:collapse: id,name,country,roles,roleDetails,website,logo
:addtargets:
:prefix: json
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
 :jsonpointer: /networks/0/organisations
 :title: organisations
```

:::

::::

### Contract

`Contract` is defined as:

```{jsoninclude-quote} ../../../../_readthedocs/html/network-schema.json
:jsonpointer: /$defs/Contract/description
```

This sub-schema is referenced by the following properties:

- [`contracts`](json,network-schema.json,,contracts)

Each `Contract` has the following properties:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../../../_readthedocs/html/network-schema.json
:pointer: /$defs/Contract
:collapse: id,title,description,type,dateSigned,documents,relatedPhases,value
:addtargets:
:prefix: json
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
 :jsonpointer: /networks/0/contracts
 :title: contracts
```

:::

::::

### Wayleave

`Wayleave` is defined as:

```{jsoninclude-quote} ../../../../_readthedocs/html/network-schema.json
:jsonpointer: /$defs/Wayleave/description
```

This sub-schema is referenced by the following properties:

- [`wayleaves`](json,network-schema.json,,wayleaves)

Each `Wayleave` has the following properties:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../../../_readthedocs/html/network-schema.json
:pointer: /$defs/Wayleave
:addtargets:
:prefix: json
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
 :jsonpointer: /networks/0/wayleaves
 :title: wayleaves
```

:::

::::

### Other sub-schemas

This section lists each sub-schema in the OFDS schema. Sub-schemas are reused in multiple places in the schema. For information on how the sub-schemas fit together, see the [network object](#network) section or the [schema browser](#browser).

#### PointGeometry

`PointGeometry` is defined as:

```{jsoninclude-quote} ../../../../schema/network-schema.json
:jsonpointer: /$defs/PointGeometry/description
```

This sub-schema is referenced by the following properties:

- [`Node/location`](json,network-schema.json,/$defs/Node,location)

Additional properties are not permitted within `PointGeometry` objects.

Each `PointGeometry` has the following properties:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../../../schema/network-schema.json
:pointer: /$defs/PointGeometry
:collapse: type,coordinates
:addtargets:
:prefix: json
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
 :jsonpointer: /networks/0/nodes/0/location
 :title: nodes/0/location
```

:::

::::

#### LineStringGeometry

`LineStringGeometry` is defined as:

```{jsoninclude-quote} ../../../../schema/network-schema.json
:jsonpointer: /$defs/LineStringGeometry/description
```

This sub-schema is referenced by the following properties:

- [`Span/route`](json,network-schema.json,/$defs/Span,route)

Additional properties are not permitted within `LineStringGeometry` objects.

Each `LineStringGeometry` has the following properties:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../../../schema/network-schema.json
:pointer: /$defs/LineStringGeometry
:collapse: type,coordinates
:addtargets:
:prefix: json
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
 :jsonpointer: /networks/0/spans/0/route
 :title: spans/0/route
```

:::

::::

#### OrganisationReference

`OrganisationReference` is defined as:

```{jsoninclude-quote} ../../../../_readthedocs/html/network-schema.json
:jsonpointer: /$defs/OrganisationReference/description
```

This sub-schema is referenced by the following properties:

- [`Node/transmissionMediumOwner`](json,network-schema.json,/$defs/Node,transmissionMediumOwner)
- [`Node/supportingInfrastructure/owner`](json,network-schema.json,/$defs/Node,supportingInfrastructure/owner)
- [`Node/networkProviders`](json,network-schema.json,/$defs/Node,networkProviders)
- [`Span/transmissionMediumOwner`](json,network-schema.json,/$defs/Span,transmissionMediumOwner)
- [`Span/supportingInfrastructure/owner`](json,network-schema.json,/$defs/Span,supportingInfrastructure/owner)
- [`Span/networkProviders`](json,network-schema.json,/$defs/Span,networkProviders)
- [`Span/supplier`](json,network-schema.json,/$defs/Span,supplier)
- [`Phase/funders`](json,network-schema.json,/$defs/Phase,funders)

Additional properties are not permitted within `OrganisationReference` objects.

Each `OrganisationReference` has the following properties:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../../../_readthedocs/html/network-schema.json
:pointer: /$defs/OrganisationReference
:collapse: id,name
:addtargets:
:prefix: json
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
 :jsonpointer: /networks/0/nodes/0/transmissionMediumOwner
 :title: nodes/0/transmissionMediumOwner
```

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
 :jsonpointer: /networks/0/nodes/0/networkProviders
 :title: nodes/0/networkProviders
```

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
 :jsonpointer: /networks/0/spans/0/transmissionMediumOwner
 :title: spans/0/transmissionMediumOwner
```

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
 :jsonpointer: /networks/0/spans/0/networkProviders
 :title: spans/0/networkProviders
```

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
 :jsonpointer: /networks/0/spans/0/supplier
 :title: spans/0/supplier
```

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
 :jsonpointer: /networks/0/phases/0/funders
 :title: phases/0/funders
```

:::

::::

#### PhaseReference

`PhaseReference` is defined as:

```{jsoninclude-quote} ../../../../_readthedocs/html/network-schema.json
:jsonpointer: /$defs/PhaseReference/description
```

This sub-schema is referenced by the following properties:

- [`Node/phase`](json,network-schema.json,/$defs/Node,phase)
- [`Span/phase`](json,network-schema.json,/$defs/Span,phase)
- [`Contract/relatedPhases`](json,network-schema.json,/$defs/Contract,relatedPhases)

Additional properties are not permitted within `PhaseReference` objects.

Each `PhaseReference` has the following properties:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../../../_readthedocs/html/network-schema.json
:pointer: /$defs/PhaseReference
:collapse: id,name
:addtargets:
:prefix: json
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
 :jsonpointer: /networks/0/nodes/0/phase
 :title: nodes/0/phase
```

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
 :jsonpointer: /networks/0/spans/0/phase
 :title: spans/0/phase
```

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
 :jsonpointer: /networks/0/contracts/0/relatedPhases
 :title: contracts/0/relatedPhases
```

:::

::::

#### Address

`Address` is defined as:

```{jsoninclude-quote} ../../../../_readthedocs/html/network-schema.json
:jsonpointer: /$defs/Address/description
```

This sub-schema is referenced by the following properties:

- [`Node/address`](json,network-schema.json,/$defs/Node,address)
- [`Node/internationalConnections`](json,network-schema.json,/$defs/Node,internationalConnections)

Each `Address` has the following properties:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../../../_readthedocs/html/network-schema.json
:pointer: /$defs/Address
:collapse: streetAddress,locality,region,postalCode,country
:addtargets:
:prefix: json
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
 :jsonpointer: /networks/0/nodes/0/address
 :title: nodes/0/address
```

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
 :jsonpointer: /networks/0/nodes/0/internationalConnections
 :title: nodes/0/internationalConnections
```

:::

::::

#### Value

`Value` is defined as:

```{jsoninclude-quote} ../../../../schema/network-schema.json
:jsonpointer: /$defs/Value/description
```

This sub-schema is referenced by the following properties:

- [`Contract/value`](json,network-schema.json,/$defs/Contract,documents)
- [`Wayleave/cost/perMetre`](json,network-schema.json,/$defs/Wayleave,cost/perMetre)

Each `Value` has the following properties:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../../../schema/network-schema.json
:pointer: /$defs/Value
:addtargets:
:prefix: json
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
 :jsonpointer: /networks/0/contracts/0/documents
 :title: contracts/0/documents
```

:::

::::

#### Document

`Document` is defined as:

```{jsoninclude-quote} ../../../../_readthedocs/html/network-schema.json
:jsonpointer: /$defs/Document/description
```

This sub-schema is referenced by the following properties:

- [`Contract/documents`](json,network-schema.json,/$defs/Contract,documents)

Each `Document` has the following properties:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../../../_readthedocs/html/network-schema.json
:pointer: /$defs/Document
:collapse: title,description,url,format
:addtargets:
:prefix: json
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
 :jsonpointer: /networks/0/contracts/0/documents
 :title: contracts/0/documents
```

:::

::::

#### Link

`Link` is defined as:

```{jsoninclude-quote} ../../../../_readthedocs/html/network-schema.json
:jsonpointer: /$defs/Link/description
```

This sub-schema is referenced by the following properties:

- [`links`](json,network-schema.json,,links)

Each `Link` has the following properties:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../../../_readthedocs/html/network-schema.json
:pointer: /$defs/Link
:collapse: href,rel
:addtargets:
:prefix: json
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../../../examples/json/network-package.json
 :jsonpointer: /networks/0/links
 :title: links
```

:::

::::
