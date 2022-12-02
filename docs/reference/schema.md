# Schema reference

```{admonition} 0.1.0-beta release
Welcome to the Open Fibre Data Standard 0.1.0-beta release.

We want to hear your feedback on the standard and its documentation. For general feedback, questions and suggestions, you can comment on an existing [discussion](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/discussions) or start a new one. For bug reports or feedback on specific elements of the data model and documentation, you can comment on the issues linked in the documentation or you can [create a new issue](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/new/choose).

To comment on or create discussions and issues, you need to [sign up for a free GitHub account](https://github.com/signup). If you prefer to provide feedback privately, you can email [info@opentelecomdata.net](mailto:info@opentelecomdata.net).
```

The schema provides the authoritative definition of the structure of Open Fibre Data Standard (OFDS) data, the meaning of each field, and the rules that must be followed to publish OFDS data. It is used to validate the structure and format of OFDS data.

For this version of OFDS, the canonical URL of the schema is [https://raw.githubusercontent.com/Open-Telecoms-Data/open-fibre-data-standard/0\_\_1\_\_0\_\_beta/schema/network-schema.json](https://raw.githubusercontent.com/Open-Telecoms-Data/open-fibre-data-standard/0__1__0__beta/schema/network-schema.json). Use the canonical URL to make sure that your software, documentation or other resources refer to the specific version of the schema with which they were tested.

This page presents the schema in an [interactive browser](#browser) and in [reference tables](#reference-tables) with additional information in paragraphs. You can also download the canonical version of the schema as [JSON Schema](../../schema/network-schema.json) or download it as a [CSV spreadsheet](../../schema/network-schema.csv).

```{note}
   If any conflicts are found between the text on this page and the text within the schema, the text within the schema takes precedence.
```

## Browser

Click on schema elements to expand the tree, or use the '+' icon to expand all elements. Use { } to view the underlying schema for any section. Required fields are indicated in **bold**.

<script src="../_static/docson/widget.js" data-schema="../network-schema.json"></script>

## Reference tables

This section presents each field in the schema in tables with additional information in paragraphs. Required fields are indicated in the **Required** column. For fields that reference components, a link is provided to a table with details of the component.

### Structure

This section describes the overall structure of the OFDS schema. The top-level object in OFDS data is a `Network`. A network has the following sections:

- [Nodes](#nodes)
- [Spans](#spans)
- [Phases](#phases)
- [Organisations](#organisations)
- [Contracts](#contracts)

In addition to the above sections, there are several top-level metadata fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:collapse: nodes,spans,phases,organisations,contracts,publisher,crs,links
```

:::

:::{tab-item} Example

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
   :jsonpointer: /networks/0
   :title: Example
```

:::

::::

#### Nodes

The nodes section contains information on the nodes in the network.

For information on the fields that can be provided for each node, see [Node](#node).

#### Spans

The spans section contains information on the spans in the network.

For information on the fields that can be provided for each span, see [Span](#span).

#### Phases

The phases section contains information on the phases in which nodes and spans are deployed.

For information on the fields that can be provided for each phase, see [Phase](#phase).

#### Organisations

Each organisation referenced in a network must be included in the organisations section.

For information on the fields that can be provided for each organisation, see [Organisation](#organisation).

#### Contracts

The contracts section contains information on contracts relating to the network.

For information on the fields that can be provided for each contract, see [Contract](#contract).

### Components

This section lists each component in the OFDS schema. Some components are reused in multiple places in the schema. For information on how the components fit together, see the [structure](#structure) section or the [schema browser](#browser).

#### Node

```{admonition} Consultation
The following issues relate to this component or its fields:
* `Node`, `.accessPoint`: [#60 Node definition (access points)](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/60)
* `.location`: [#10 Coordinates modelling (add support for WKT to Flatten Tool)](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/10)
* `.internationalConnections`: [#72 International connections](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/72)
* `.physicalInfrastructureProvider`, `.networkProvider`: [#47 Link ownership and operation (physical infrastructure provider and network provider)](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/47)
```

`Node` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/Node/description
```

This component is referenced by the following properties:

- [`nodes`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,,nodes)

Each `Node` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Node
:collapse: id,name,phase,status,location,address,type,accessPoint,internationalConnections,power,technologies,physicalInfrastructureProvider,networkProvider
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/nodes
 :title: nodes
```

:::

::::

#### Span

```{admonition} Consultation
The following issues relate to this component or its fields:
* `Span`: [#83 Consider renaming links to spans](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/83)
* `.start`, `.end`: [#25 Link endpoints](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/25)
* `.route`: [#12 Geometry types for link routes](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/12)
* `.route`: [#10 Coordinates modelling (add support for WKT to Flatten Tool)](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/10)
* `.physicalInfrastructureProvider`, `.networkProvider`: [#47 Link ownership and operation (physical infrastructure provider and network provider)](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/47)
* `.supplier`: [#87 Clarify semantics around link supplier](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/87)
* `.deployment`, `.deploymentDetails`: [#26 Link deployment](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/26)
* `.capacityDetails`: [#24 Link capacity](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/24)
```

`Span` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/Span/description
```

This component is referenced by the following properties:

- [`spans`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,,spans)

Each `Span` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Span
:collapse: id,name,phase,status,readyForServiceDate,start,end,directed,route,physicalInfrastructureProvider,networkProvider,supplier,transmissionMedium,deployment,deploymentDetails,darkFibre,fibreType,fibreTypeDetails,fibreCount,fibreLength,technologies,capacity,capacityDetails,countries
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/spans
 :title: spans
```

:::

::::

#### Phase

`Phase` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/Phase/description
```

This component is referenced by the following properties:

- [`phases`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,,phases)

Each `Phase` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Phase
:collapse: id,name,description,funders
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/phases
 :title: phases
```

:::

::::

#### Organisation

```{admonition} Consultation
The following issues relate to this component or its fields:
* `.roleDetails`: [#47 Link ownership and operation (physical infrastructure provider and network provider)](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/47)
```

`Organisation` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/Organisation/description
```

This component is referenced by the following properties:

- [`organisations`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,,organisations)
- [`publisher`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,,publisher)

Each `Organisation` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Organisation
:collapse: id,name,identifier,country,roles,roleDetails,website,logo
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/organisations
 :title: organisations
```

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/publisher
 :title: publisher
```

:::

::::

#### Contract

```{admonition} Consultation
The following issues relate to this component or its fields:
* `Contract`: [#71 Contracts](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/71)
```

`Contract` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/Contract/description
```

This component is referenced by the following properties:

- [`contracts`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,,contracts)

Each `Contract` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Contract
:collapse: id,title,description,type,value,dateSigned,documents,relatedPhases
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/contracts
 :title: contracts
```

:::

::::

#### Geometry

`Geometry` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/Geometry/description
```

This component is referenced by the following properties:

- [`Node/location`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,/definitions/Node,location)
- [`Span/route`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,/definitions/Span,route)

Each `Geometry` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Geometry
:collapse: type,coordinates
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/nodes/0/location
 :title: nodes/0/location
```

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/spans/0/route
 :title: spans/0/route
```

:::

::::

#### OrganisationReference

`OrganisationReference` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/OrganisationReference/description
```

This component is referenced by the following properties:

- [`Node/physicalInfrastructureProvider`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,/definitions/Node,physicalInfrastructureProvider)
- [`Node/networkProvider`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,/definitions/Node,networkProvider)
- [`Span/physicalInfrastructureProvider`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,/definitions/Span,physicalInfrastructureProvider)
- [`Span/networkProvider`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,/definitions/Span,networkProvider)
- [`Span/supplier`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,/definitions/Span,supplier)
- [`Phase/funders`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,/definitions/Phase,funders)

Each `OrganisationReference` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/OrganisationReference
:collapse: id,name
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/nodes/0/physicalInfrastructureProvider
 :title: nodes/0/physicalInfrastructureProvider
```

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/nodes/0/networkProvider
 :title: nodes/0/networkProvider
```

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/spans/0/physicalInfrastructureProvider
 :title: spans/0/physicalInfrastructureProvider
```

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/spans/0/networkProvider
 :title: spans/0/networkProvider
```

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/spans/0/supplier
 :title: spans/0/supplier
```

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/phases/0/funders
 :title: phases/0/funders
```

:::

::::

#### PhaseReference

`PhaseReference` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/PhaseReference/description
```

This component is referenced by the following properties:

- [`Node/phase`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,/definitions/Node,phase)
- [`Span/phase`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,/definitions/Span,phase)
- [`Contract/relatedPhases`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,/definitions/Contract,relatedPhases)

Each `PhaseReference` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/PhaseReference
:collapse: id,name
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/nodes/0/phase
 :title: nodes/0/phase
```

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/spans/0/phase
 :title: spans/0/phase
```

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/contracts/0/relatedPhases
 :title: contracts/0/relatedPhases
```

:::

::::

#### Address

`Address` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/Address/description
```

This component is referenced by the following properties:

- [`Node/address`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,/definitions/Node,address)
- [`Node/internationalConnections`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,/definitions/Node,internationalConnections)

Each `Address` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Address
:collapse: streetAddress,locality,region,postalCode,country
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/nodes/0/address
 :title: nodes/0/address
```

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/nodes/0/internationalConnections
 :title: nodes/0/internationalConnections
```

:::

::::

#### Value

`Value` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/Value/description
```

This component is referenced by the following properties:

- [`Contract/value`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,/definitions/Contract,value)

Each `Value` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Value
:collapse: amount,currency
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/contracts/0/value
 :title: contracts/0/value
```

:::

::::

#### Document

`Document` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/Document/description
```

This component is referenced by the following properties:

- [`Contract/documents`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,/definitions/Contract,documents)

Each `Document` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Document
:collapse: title,description,url,format
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/contracts/0/documents
 :title: contracts/0/documents
```

:::

::::

#### Identifier

`Identifier` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/Identifier/description
```

This component is referenced by the following properties:

- [`Organisation/identifier`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,/definitions/Organisation,identifier)

Each `Identifier` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Identifier
:collapse: id,scheme,legalName,uri
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/organisations/0/identifier
 :title: organisations/0/identifier
```

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/publisher/identifier
 :title: publisher/identifier
```

:::

::::

#### CoordinateReferenceSystem

Coordinates in all OFDS data must be specified in the coordinate reference system [required by GeoJSON](https://datatracker.ietf.org/doc/html/rfc7946#section-4):

> The coordinate reference system for all GeoJSON coordinates is a geographic coordinate reference system, using the World Geodetic System 1984 (WGS 84) \[WGS84\] datum, with longitude and latitude units of decimal degrees.  This is equivalent to the coordinate reference system identified by the Open Geospatial Consortium (OGC) URN urn:ogc:def:crs:OGC::CRS84.

The `CoordinateReferenceSystem` object references the CRS by `name` and `uri`. Its properties must be set to the following values:

- `name`: urn:ogc:def:crs:OGC::CRS84
- `uri`: <http://www.opengis.net/def/crs/OGC/1.3/CRS84>

`urn:ogc:def:crs:OGC::CRS84` denotes WGS84 with the order longitude, latitude. It is equivalent to EPSG:4326 with reversed axes.

For more information, see [How to transform coordinates to the correct coordinate reference system](../guidance/publication.md#how-to-transform-coordinates-to-the-correct-coordinate-reference-system).

```{admonition} Consultation
The following issues relate to this component or its fields:
* `CoordinateReferenceSystem`: [#9 Coordinate reference system](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/9)
```

`CoordinateReferenceSystem` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/CoordinateReferenceSystem/description
```

This component is referenced by the following properties:

- [`crs`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,,crs)

Each `CoordinateReferenceSystem` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/CoordinateReferenceSystem
:collapse: name,uri
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/crs
 :title: crs
```

:::

::::

#### Link

```{admonition} Consultation
The following issues relate to this component or its fields:
* `Link`: [#83 Consider renaming links to spans](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/83)
* `Link`: [#75 Paginating and streaming nodes and links](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/75)
```

`Link` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/Link/description
```

This component is referenced by the following properties:

- [`links`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,,links)

Each `Link` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Link
:collapse: href,rel
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/links
 :title: links
```

:::

::::

#### FibreTypeDetails

`FibreTypeDetails` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/FibreTypeDetails/description
```

This component is referenced by the following properties:

- [`Span/fibreTypeDetails`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,/definitions/Span,fibreTypeDetails)

Each `FibreTypeDetails` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/FibreTypeDetails
:collapse: fibreSubtype,description
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/spans/0/fibreTypeDetails
 :title: spans/0/fibreTypeDetails
```

:::

::::

#### DeploymentDetails

```{admonition} Consultation
The following issues relate to this component or its fields:
* `DeploymentDetails`: [#26 Link deployment](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/26)
```

`DeploymentDetails` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/DeploymentDetails/description
```

This component is referenced by the following properties:

- [`Span/deploymentDetails`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,/definitions/Span,deploymentDetails)

Each `DeploymentDetails` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/DeploymentDetails
:collapse: description
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/spans/0/deploymentDetails
 :title: spans/0/deploymentDetails
```

:::

::::

#### CapacityDetails

```{admonition} Consultation
The following issues relate to this component or its fields:
* `CapacityDetails`: [#24 Link capacity](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/24)
```

`CapacityDetails` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/CapacityDetails/description
```

This component is referenced by the following properties:

- [`Span/capacityDetails`](https://open-fibre-data-standard.readthedocs.io/en/latest/reference/schema.html#network-schema.json,/definitions/Span,capacityDetails)

Each `CapacityDetails` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/CapacityDetails
:collapse: description
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/spans/0/capacityDetails
 :title: spans/0/capacityDetails
```

:::

::::
