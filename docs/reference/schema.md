# Schema reference

```{admonition} 0.2.0 release
Welcome to the Open Fibre Data Standard 0.2.0 release.

We want to hear your feedback on the standard and its documentation. For general feedback, questions and suggestions, you can comment on an existing [discussion](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/discussions) or start a new one. For bug reports or feedback on specific elements of the data model and documentation, you can comment on the issues in the [issue tracker](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues) or you can [create a new issue](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/new/choose).

To comment on or create discussions and issues, you need to [sign up for a free GitHub account](https://github.com/signup). If you prefer to provide feedback privately, you can email [info@opentelecomdata.net](mailto:info@opentelecomdata.net).
```

The schema provides the authoritative definition of the structure of Open Fibre Data Standard (OFDS) data, the meaning of each field, and the rules that must be followed to publish OFDS data. It is used to validate the structure and format of OFDS data.

For this version of OFDS, the canonical URL of the schema is [https://raw.githubusercontent.com/Open-Telecoms-Data/open-fibre-data-standard/0\_\_2\_\_0/schema/network-schema.json](https://raw.githubusercontent.com/Open-Telecoms-Data/open-fibre-data-standard/0__2__0/schema/network-schema.json). Use the canonical URL to make sure that your software, documentation or other resources refer to the specific version of the schema with which they were tested.

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
:collapse: nodes,spans,phases,organisations,contracts,crs,links
:addtargets:
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

`Node` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /$defs/Node/description
```

This component is referenced by the following properties:

- [`nodes`](network-schema.json,,nodes)

Each `Node` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /$defs/Node
:collapse: id,name,phase,status,location,address,type,accessPoint,internationalConnections,power,technologies,physicalInfrastructureProvider,networkProviders
:addtargets:
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

`Span` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /$defs/Span/description
```

This component is referenced by the following properties:

- [`spans`](network-schema.json,,spans)

Each `Span` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /$defs/Span
:collapse: id,name,phase,status,readyForServiceDate,start,end,directed,route,physicalInfrastructureProvider,networkProviders,supplier,transmissionMedium,deployment,deploymentDetails,darkFibre,fibreType,fibreTypeDetails,fibreCount,fibreLength,technologies,capacity,capacityDetails,countries
:addtargets:
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
:jsonpointer: /$defs/Phase/description
```

This component is referenced by the following properties:

- [`phases`](network-schema.json,,phases)

Each `Phase` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /$defs/Phase
:collapse: id,name,description,funders
:addtargets:
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

`Organisation` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /$defs/Organisation/description
```

This component is referenced by the following properties:

- [`organisations`](network-schema.json,,organisations)

Each `Organisation` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /$defs/Organisation
:collapse: id,name,identifier,country,roles,roleDetails,website,logo
:addtargets:
```

:::

:::{tab-item} Examples

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/organisations
 :title: organisations
```

:::

::::

#### Contract

`Contract` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /$defs/Contract/description
```

This component is referenced by the following properties:

- [`contracts`](network-schema.json,,contracts)

Each `Contract` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /$defs/Contract
:collapse: id,title,description,type,value,dateSigned,documents,relatedPhases
:addtargets:
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
:jsonpointer: /$defs/Geometry/description
```

This component is referenced by the following properties:

- [`Node/location`](network-schema.json,/$defs/Node,location)
- [`Span/route`](network-schema.json,/$defs/Span,route)

Each `Geometry` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /$defs/Geometry
:collapse: type,coordinates
:addtargets:
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
:jsonpointer: /$defs/OrganisationReference/description
```

This component is referenced by the following properties:

- [`Node/physicalInfrastructureProvider`](network-schema.json,/$defs/Node,physicalInfrastructureProvider)
- [`Node/networkProviders`](network-schema.json,/$defs/Node,networkProviders)
- [`Span/physicalInfrastructureProvider`](network-schema.json,/$defs/Span,physicalInfrastructureProvider)
- [`Span/networkProviders`](network-schema.json,/$defs/Span,networkProviders)
- [`Span/supplier`](network-schema.json,/$defs/Span,supplier)
- [`Phase/funders`](network-schema.json,/$defs/Phase,funders)

Each `OrganisationReference` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /$defs/OrganisationReference
:collapse: id,name
:addtargets:
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
 :jsonpointer: /networks/0/nodes/0/networkProviders
 :title: nodes/0/networkProviders
```

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/spans/0/physicalInfrastructureProvider
 :title: spans/0/physicalInfrastructureProvider
```

```{eval-rst}
.. jsoninclude:: ../../examples/json/network-package.json
 :jsonpointer: /networks/0/spans/0/networkProviders
 :title: spans/0/networkProviders
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
:jsonpointer: /$defs/PhaseReference/description
```

This component is referenced by the following properties:

- [`Node/phase`](network-schema.json,/$defs/Node,phase)
- [`Span/phase`](network-schema.json,/$defs/Span,phase)
- [`Contract/relatedPhases`](network-schema.json,/$defs/Contract,relatedPhases)

Each `PhaseReference` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /$defs/PhaseReference
:collapse: id,name
:addtargets:
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
:jsonpointer: /$defs/Address/description
```

This component is referenced by the following properties:

- [`Node/address`](network-schema.json,/$defs/Node,address)
- [`Node/internationalConnections`](network-schema.json,/$defs/Node,internationalConnections)

Each `Address` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /$defs/Address
:collapse: streetAddress,locality,region,postalCode,country
:addtargets:
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
:jsonpointer: /$defs/Value/description
```

This component is referenced by the following properties:

- [`Contract/value`](network-schema.json,/$defs/Contract,value)

Each `Value` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /$defs/Value
:collapse: amount,currency
:addtargets:
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
:jsonpointer: /$defs/Document/description
```

This component is referenced by the following properties:

- [`Contract/documents`](network-schema.json,/$defs/Contract,documents)

Each `Document` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /$defs/Document
:collapse: title,description,url,format
:addtargets:
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
:jsonpointer: /$defs/Identifier/description
```

This component is referenced by the following properties:

- [`Organisation/identifier`](network-schema.json,/$defs/Organisation,identifier)

Each `Identifier` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /$defs/Identifier
:collapse: id,scheme,legalName,uri
:addtargets:
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

> The coordinate reference system for all GeoJSON coordinates is a geographic coordinate reference system, using the World Geodetic System 1984 [WGS 84](https://datatracker.ietf.org/doc/html/rfc7946#ref-WGS84) datum, with longitude and latitude units of decimal degrees.  This is equivalent to the coordinate reference system identified by the Open Geospatial Consortium (OGC) URN urn:ogc:def:crs:OGC::CRS84.

The `CoordinateReferenceSystem` object references the CRS by `name` and `uri`. Its properties must be set to the following values:

- `name`: urn:ogc:def:crs:OGC::CRS84
- `uri`: <http://www.opengis.net/def/crs/OGC/1.3/CRS84>

`urn:ogc:def:crs:OGC::CRS84` denotes WGS84 with the order longitude, latitude. It is equivalent to EPSG:4326 with reversed axes.

For more information, see [How to transform coordinates to the correct coordinate reference system](../guidance/publication.md#how-to-transform-coordinates-to-the-correct-coordinate-reference-system).

`CoordinateReferenceSystem` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /$defs/CoordinateReferenceSystem/description
```

This component is referenced by the following properties:

- [`crs`](network-schema.json,,crs)

Each `CoordinateReferenceSystem` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /$defs/CoordinateReferenceSystem
:collapse: name,uri
:addtargets:
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

`Link` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /$defs/Link/description
```

This component is referenced by the following properties:

- [`links`](network-schema.json,,links)

Each `Link` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /$defs/Link
:collapse: href,rel
:addtargets:
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
:jsonpointer: /$defs/FibreTypeDetails/description
```

This component is referenced by the following properties:

- [`Span/fibreTypeDetails`](network-schema.json,/$defs/Span,fibreTypeDetails)

Each `FibreTypeDetails` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /$defs/FibreTypeDetails
:collapse: fibreSubtype,description
:addtargets:
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

`DeploymentDetails` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /$defs/DeploymentDetails/description
```

This component is referenced by the following properties:

- [`Span/deploymentDetails`](network-schema.json,/$defs/Span,deploymentDetails)

Each `DeploymentDetails` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /$defs/DeploymentDetails
:collapse: description
:addtargets:
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

`CapacityDetails` is defined as:

```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /$defs/CapacityDetails/description
```

This component is referenced by the following properties:

- [`Span/capacityDetails`](network-schema.json,/$defs/Span,capacityDetails)

Each `CapacityDetails` has the following fields:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../../schema/network-schema.json
:pointer: /$defs/CapacityDetails
:collapse: description
:addtargets:
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
