# Schema reference

The schema provides the authoritative definition of the structure of Open Fibre Data Standard (OFDS) data, the meaning of each field, and the rules that must be followed to publish OFDS data. It is used to validate the structure and format of OFDS data.

For this version of OFDS, the canonical URL of the schema is [https://raw.githubusercontent.com/Open-Telecoms-Data/open-fibre-data-standard/0.1.0-alpha/schema/network-schema.json](https://raw.githubusercontent.com/Open-Telecoms-Data/open-fibre-data-standard/0.1.0-alpha/schema/network-schema.json). Use the canonical URL to make sure that your software, documentation or other resources refer to the specific version of the schema with which they were tested.

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

* [Nodes](#nodes)
* [Links](#links)
* [Phases](#phases)
* [Organisations](#organisations)
* [Contracts](#contracts)

In addition to the above sections, there are several top-level metadata fields:

```{jsonschema} ../../schema/network-schema.json
:collapse: nodes,links,phases,organisations,contracts,publisher,crs
```

#### Nodes

The nodes section contains information on the nodes in the network.

For information on the fields that can be provided for each node, see [Node](#node).

#### Links

The links section contains information on the links in the network.

For information on the fields that can be provided for each link, see [Link](#link).

#### Phases

The phases section contains information on the phases in which nodes and links are deployed.

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
```{admonition} Alpha consultation
The following issues relate to this component or its fields:
* `Node`, `.accessPoint`: [#60 Node definition (access points)](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/60)
* `.location`: [#10 Coordinates modelling](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/10)
* `.internationalConnections`: [#72 International connections](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/72)
* `.physicalInfrastructureProvider`, `.networkProvider`: [#47 Link ownership and operation (physical infrastructure provider and network provider)](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/47)
```
`Node` is defined as:
```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/Node/description
```
Each `Node` has the following fields:
```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Node
:collapse: id,name,phase,status,location,address,type,accessPoint,internationalConnections,power,technologies,physicalInfrastructureProvider,networkProvider
```

#### Link
```{admonition} Alpha consultation
The following issues relate to this component or its fields:
* `Link`: [#83 Consider renaming links to spans](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/83)
* `.start`, `.end`: [#25 Link endpoints](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/25)
* `.route`: [#12 Geometry types for link routes](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/12)
* `.route`: [#10 Coordinates modelling](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/10)
* `.physicalInfrastructureProvider`, `.networkProvider`: [#47 Link ownership and operation (physical infrastructure provider and network provider)](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/47)
* `.supplier`: [#87 Clarify semantics around link supplier](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/87)
* `.deployment`, `.deploymentDetails`: [#26 Link deployment](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/26)
* `.capacityDetails`: [#24 Link capacity](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/24)
```
`Link` is defined as:
```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/Link/description
```
Each `Link` has the following fields:
```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Link
:collapse: id,name,phase,status,readyForServiceDate,start,end,route,physicalInfrastructureProvider,networkProvider,supplier,transmissionMedium,deployment,deploymentDetails,darkFibre,fibreType,fibreTypeDetails,fibreCount,fibreLength,technologies,capacity,capacityDetails,countries,directed
```

#### Phase
`Phase` is defined as:
```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/Phase/description
```
Each `Phase` has the following fields:
```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Phase
:collapse: id,name,description,funders
```

#### Organisation
```{admonition} Alpha consultation
The following issues relate to this component or its fields:
* `.roleDetails`: [#47 Link ownership and operation (physical infrastructure provider and network provider)](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/47)
```
`Organisation` is defined as:
```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/Organisation/description
```
Each `Organisation` has the following fields:
```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Organisation
:collapse: id,name,identifier,country,roles,roleDetails,website,logo
```

#### Contract
```{admonition} Alpha consultation
The following issues relate to this component or its fields:
* `Contract`: [#71 Contracts](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/71)
```
`Contract` is defined as:
```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/Contract/description
```
Each `Contract` has the following fields:
```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Contract
:collapse: id,title,description,type,value,dateSigned,documents,relatedPhases
```

#### Geometry
`Geometry` is defined as:
```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/Geometry/description
```
Each `Geometry` has the following fields:
```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Geometry
:collapse: type,coordinates
```

#### OrganisationReference
`OrganisationReference` is defined as:
```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/OrganisationReference/description
```
Each `OrganisationReference` has the following fields:
```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/OrganisationReference
:collapse: id,name
```

#### PhaseReference
`PhaseReference` is defined as:
```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/PhaseReference/description
```
Each `PhaseReference` has the following fields:
```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/PhaseReference
:collapse: id,name
```

#### Address
`Address` is defined as:
```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/Address/description
```
Each `Address` has the following fields:
```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Address
:collapse: streetAddress,locality,region,postalCode,country
```

#### Value
`Value` is defined as:
```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/Value/description
```
Each `Value` has the following fields:
```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Value
:collapse: amount,currency
```

#### Document
`Document` is defined as:
```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/Document/description
```
Each `Document` has the following fields:
```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Document
:collapse: title,description,url,format
```

#### Identifier
`Identifier` is defined as:
```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/Identifier/description
```
Each `Identifier` has the following fields:
```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Identifier
:collapse: id,scheme,legalName,uri
```

#### CoordinateReferenceSystem
Coordinates in all OFDS data must be specified in the coordinate reference system [required by GeoJSON](https://datatracker.ietf.org/doc/html/rfc7946#section-4):

> The coordinate reference system for all GeoJSON coordinates is a geographic coordinate reference system, using the World Geodetic System 1984 (WGS 84) [WGS84] datum, with longitude and latitude units of decimal degrees.  This is equivalent to the coordinate reference system identified by the Open Geospatial Consortium (OGC) URN urn:ogc:def:crs:OGC::CRS84.

The `CoordinateReferenceSystem` object references the CRS by `name` and `uri`. Its properties must be set to the following values:

* `name`: urn:ogc:def:crs:OGC::CRS84
* `uri`: http://www.opengis.net/def/crs/OGC/1.3/CRS84

`urn:ogc:def:crs:OGC::CRS84` denotes WGS84 with the order longitude, latitude. It is equivalent to EPSG:4326 with reversed axes.

For more information, see [How to transform coordinates to the correct coordinate reference system](../guidance/publication.md#how-to-transform-coordinates-to-the-correct-coordinate-reference-system).

```{admonition} Alpha consultation
The following issues relate to this component or its fields:
* `CoordinateReferenceSystem`: [#9 Coordinate reference system](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/9)
```
`CoordinateReferenceSystem` is defined as:
```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/CoordinateReferenceSystem/description
```
Each `CoordinateReferenceSystem` has the following fields:
```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/CoordinateReferenceSystem
:collapse: name,uri
```

#### RelatedResourceReference
```{admonition} Alpha consultation
The following issues relate to this component or its fields:
* `RelatedResourceReference`: [#75 Paginating and streaming nodes and links](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/75)
* `RelatedResourceReference`: [#83 Consider renaming links to spans](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/83)
```
`RelatedResourceReference` is defined as:
```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/RelatedResourceReference/description
```
Each `RelatedResourceReference` has the following fields:
```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/RelatedResourceReference
:collapse: href,rel
```

#### FibreTypeDetails
`FibreTypeDetails` is defined as:
```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/FibreTypeDetails/description
```
Each `FibreTypeDetails` has the following fields:
```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/FibreTypeDetails
:collapse: description
```

#### DeploymentDetails
```{admonition} Alpha consultation
The following issues relate to this component or its fields:
* `DeploymentDetails`: [#26 Link deployment](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/26)
```
`DeploymentDetails` is defined as:
```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/DeploymentDetails/description
```
Each `DeploymentDetails` has the following fields:
```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/DeploymentDetails
:collapse: description
```

#### CapacityDetails
```{admonition} Alpha consultation
The following issues relate to this component or its fields:
* `CapacityDetails`: [#24 Link capacity](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/24)
```
`CapacityDetails` is defined as:
```{jsoninclude-quote} ../../schema/network-schema.json
:jsonpointer: /definitions/CapacityDetails/description
```
Each `CapacityDetails` has the following fields:
```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/CapacityDetails
:collapse: description
```

