# Schema reference

The schema provides the authoritative definition of the structure of Open Fibre Data Standard (OFDS) data, the meaning of each field, and the rules that must be followed to publish OFDS data. It is used to validate the structure and format of OFDS data.

For this version of OFDS, the canonical URL of the schema is [https://raw.githubusercontent.com/Open-Telecoms-Data/open-fibre-data-standard/0.1.0-alpha/schema/network-schema.json](https://raw.githubusercontent.com/Open-Telecoms-Data/open-fibre-data-standard/0.1.0-alpha/schema/network-schema.json). Use the canonical URL to make sure that your software, documentation or other resources refer to the specific version of the schema with which they were tested.

This page presents the schema in an [interactive browser](#browser) and in [reference tables](#reference-tables) with additional information in paragraphs. You can also download the canonical version of the schema as [JSON Schema](../../schema/network-schema.json) or download it as a [CSV spreadsheet](../../schema/network-schema.csv).

```{note}
   If any conflicts are found between the text on this page and the text within the schema, the text within the schema takes precedence.
```

## Browser

Click on schema elements to expand the tree, or use the '+' icon to expand all elements. Use { } to view the underlying schema for any section. Required fields are indicated in **bold**.

 <script src="../../_static/docson/widget.js" data-schema="../../_static/network-schema.json"></script> 

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

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Node
:collapse: identifier,name,status,location,address,internationalConnections,accessPoint,physicalInfrastructureProvider,networkProvider,type,technologies,power,rackspace,phase
```

#### Link

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Link
:collapse: identifier,name,status,endpoints,route,physicalInfrastructureProvider,networkProvider,supplier,ownership,transmissionMedium,deployment,darkFibre,fibreType,fibreCount,fibreLength,technologies,capacity,capacityDetails,accuracy,readyForServiceDate,phase,country
```

#### Phase

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Phase
:collapse: identifier,name,funders
```

#### Organisation

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Organisation
:collapse: id,name,identifier,role,classification,country,listing.exchange,listing.symbol,website,logo
```

#### OrganisationReference

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/OrganisationReference
:collapse: id,name
```

#### Value

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Value
:collapse: amount,currency
```

#### Address

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Address
:collapse: streetAddress,locality,region,country,postalCode
```

#### Identifier

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Identifier
:collapse: scheme,id,legalName,uri
```

#### Document

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Document
:collapse: 
```

#### Contract

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Contract
:collapse: identifier,title,description,type,value,dateSigned,documents
```

#### Geometry

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Geometry
:collapse: type,coordinates
```

#### CoordinateReferenceSystem

Coordinates in all OFDS data must be specified in the coordinate reference system required by GeoJSON:

> The coordinate reference system for all GeoJSON coordinates is a geographic coordinate reference system, using the World Geodetic System 1984 (WGS 84) [WGS84] datum, with longitude and latitude units of decimal degrees.  This is equivalent to the coordinate reference system identified by the Open Geospatial Consortium (OGC) URN urn:ogc:def:crs:OGC::CRS84.

The `CoordinateReferenceSystem` object references the CRS by `name` and `uri`. Its properties must be set to the following values:

* `name`: urn:ogc:def:crs:OGC::CRS84
* `uri`: http://www.opengis.net/def/crs/OGC/1.3/CRS84

`urn:ogc:def:crs:OGC::CRS84` denotes WGS84 with the order longitude, latitude. It is equivalent to EPSG:4326 with reversed axes.

For more information, see [How to transform coordinates to the correct coordinate reference system](../guidance/publication.md#how-to-transform-coordinates-to-the-correct-coordinate-reference-system).

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/CoordinateReferenceSystem
:collapse: name,uri
```

