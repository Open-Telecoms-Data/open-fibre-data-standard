# Schema reference

The schema provides the authoritative definition of the structure of Open Fibre Data Standard (OFDS) data, the meaning of each field and the rules that must be followed to publish OFDS data. It is used to validate the structure and format of OFDS data.

For this version of OFDS, the canonical URL of the schema is [https://raw.githubusercontent.com/Open-Telecoms-Data/open-fibre-data-standard/0.1.0-alpha/schema/network-schema.json](https://raw.githubusercontent.com/Open-Telecoms-Data/open-fibre-data-standard/0.1.0-alpha/schema/network-schema.json). Use the canonical URL to make sure that your software, documentation or other resources refer to the specific version of the schema with which they were tested.

This page presents the schema in an [interactive browser](#browser) and in [reference tables](#reference-tables) with additional information in paragraphs. You can also download the canonical version of the schema as [JSON Schema](../../schema/network-schema.json) or download it as a [CSV spreadsheet](../../schema/network-schema.csv).

```{note}
   If any conflicts are found between the text on this page and the text within the schema, the text within the schema takes precedence.
```

## Browser

Click on schema elements to expand the tree, or use the '+' icon to expand all elements. Use { } to view the underlying schema for any section. Required fields are indicated in **bold**.

 <script src="../../_static/docson/widget.js" data-schema="../../_static/network-schema.json"></script> 

## Reference tables

### Structure

The top-level object in OFDS data is a `Network`.

#### Nodes

#### Links

#### Phases

#### Organisations

#### Contracts

### Components

#### Node

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Node
:collapse: address,rackspace,identifier,phase,accessPoint,networkProvider,status,technologies,internationalConnections,type,power,location,name,physicalInfrastructureProvider
```

#### Link

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Link
:collapse: accuracy,networkProvider,fibreType,readyForServiceDate,ownership,phase,fibreCount,supplier,country,fibreLength,technologies,capacity,endpoints,name,transmissionMedium,darkFibre,identifier,physicalInfrastructureProvider,deployment,capacityDetails,status,route
```

#### Phase

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Phase
:collapse: name,funders,identifier
```

#### Organisation

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Organisation
:collapse: identifier,listing.exchange,logo,classification,listing.symbol,id,website,country,role,name
```

#### OrganisationReference

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/OrganisationReference
:collapse: name,id
```

#### Value

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Value
:collapse: currency,amount
```

#### Address

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Address
:collapse: postalCode,locality,streetAddress,region,country
```

#### Identifier

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Identifier
:collapse: id,legalName,uri,scheme
```

#### Document

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Document
:collapse: 
```

#### Contract

```{jsonschema} ../../schema/network-schema.json
:pointer: /definitions/Contract
:collapse: description,type,value,dateSigned,documents,title,identifier
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

