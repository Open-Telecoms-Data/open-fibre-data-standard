# Publication formats reference

```{admonition} Alpha consultation
Welcome to the alpha release of the Open Fibre Data Standard.

We want to hear your feedback on the standard and its documentation. To find out how you can provide feedback, read the [alpha release announcement](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/discussions/115).
```

```{admonition} Alpha consultation
The following issues relate to this page:
* [#51 Packaging multiple networks](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/51)
```

OFDS data must be published using at least one of the formats described on this page:

* [JSON](#json)
* [GeoJSON](#geojson)
* [CSV](#csv)

Each format provides containers for publishing one or more networks and options to support pagination and streaming.

To support the widest range of use cases, you should publish your data in all three formats. For more information on choosing a publication format and on publishing data in multiple formats, see [how to format data for publication](../guidance/publication.md#how-to-format-data-for-publication).

## JSON

This section describes how to publish data in JSON format.

If your data is small enough to fit into memory or if you are publishing data via an API, you should use the [small files and API responses option](#small-files-and-api-responses-option). If your data is too large to fit into memory, you should use the [streaming option](#streaming-option).

For guidance on paginating or streaming individual networks, see [how to publish large networks](../guidance/publication.md#how-to-publish-large-networks).

### Small files and API responses option

The network package schema describes the structure of the container for publishing one or more networks in JSON format and for supporting pagination.

For this version of OFDS, the canonical URL of the schema is [https://raw.githubusercontent.com/Open-Telecoms-Data/open-fibre-data-standard/0__1__0__alpha/schema/network-package-schema.json](https://raw.githubusercontent.com/Open-Telecoms-Data/open-fibre-data-standard/0__1__0__alpha/schema/network-package-schema.json). Use the canonical URL to make sure that your software, documentation or other resources refer to the specific version of the schema with which they were tested.

This page presents the schema in an interactive browser. You can also download the canonical version of the schema as [JSON Schema](../../schema/network-package-schema.json).

A network package is a JSON object that must include `.networks`: an array of `Network` objects as described by the [network schema](schema.md). For data published via a paginated API, the optional `.pages` object should be used to provide URLs for the next and previous pages of results.

::::{tab-set}

:::{tab-item} Schema browser
Click on schema elements to expand the tree, or use the '+' icon to expand all elements. Use { } to view the underlying schema for any section. Required fields are indicated in **bold**.

 <script src="../_static/docson/widget.js" data-schema="../network-package-schema.json"></script>
:::

:::{tab-item} Small file example
The following example shows a network package containing two networks:

```{jsoninclude} ../../examples/json/multiple-networks.json
:jsonpointer:
:expand: networks
```

:::

:::{tab-item} API response example
The following example shows a network package containing two networks with URLs for the next and previous pages of results.

```{jsoninclude} ../../examples/json/api-response.json
:jsonpointer:
:expand: networks,pages
```

:::

::::

### Streaming option

The streaming option describes how to package multiple JSON-format networks with support for streaming. You should only use this option if your data is too large to load into memory.

The streaming option is a [JSON Lines](https://jsonlines.org/) file in which each line is a valid OFDS network, as described by the [network schema](schema.md).

The following example shows a JSON Lines file containing two networks:

```
{"id":"fd7b30d6-f514-4cd0-a5ac-29a774f53a43","name":"Ghana Fibre Network"}
{"id":"acafe566-7ffa-416a-b3b4-84a52386a586","name":"Togo Fibre Network"}
```

## GeoJSON

```{admonition} Alpha consultation
This section has [open issues](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues?q=is%3Aopen+is%3Aissue+label%3A%22GeoJSON+format%22+).
```

This section describes how to publish data in GeoJSON format.

If your data is small enough to fit into memory or if you are publishing data via an API, you should use the [small files and API responses option](#small-files-and-api-responses-option-1). If your data is too large to fit into memory, you should use the [streaming option](#streaming-option-1).

### Small files and API responses option

Publish separate GeoJSON [feature collections](https://datatracker.ietf.org/doc/html/rfc7946#section-3.3) for nodes and links, according to the [GeoJSON transformation specification](#geojson-transformation-specification).

::::{tab-set}

:::{tab-item} Nodes feature collection
The following example shows a GeoJSON feature collection containing nodes:

```{jsoninclude} ../../examples/geojson/nodes.geojson
:jsonpointer:
:expand: features
```

:::

:::{tab-item} Links feature collection
The following example shows a GeoJSON feature collection containing links:

```{jsoninclude} ../../examples/geojson/links.geojson
:jsonpointer:
:expand: features
```

:::

::::

Each feature collection may contain features from one or more networks. The network each feature relates to is identified by its `.properties.network.id`.

The following example shows a GeoJSON feature collection containing features from two networks:

```{jsoninclude} ../../examples/geojson/multiple-networks.geojson
:jsonpointer:
:expand: features
```

For data published via a paginated API, you should add a top-level `pages` object to the feature collection to provide URLs for the next and previous pages of results:

::::{tab-set}

:::{tab-item} Pages object schema

```{jsonschema} ../../schema/network-package-schema.json
:pointer: /properties/pages
```

:::

:::{tab-item} API response example
The following example shows a GeoJSON feature collection containing two features with URLS for the next and previous pages of results.

```{jsoninclude} ../../examples/geojson/api-response.geojson
:jsonpointer:
```

:::

::::

### Streaming option

The streaming option describes how to publish multiple networks in GeoJSON format with support for streaming. You should only use this option if your data is too large to load into memory.

The streaming option for GeoJSON is separate [Newline-delimited GeoJSON](https://stevage.github.io/ndgeojson/) files for nodes and links, in which each line is a GeoJSON feature structured according to the [GeoJSON transformation specification](#geojson-transformation-specification).

The following example shows a newline-delimited GeoJSON file containing two features:

```
{"type":"Feature","properties":{"id":"1","name":"Accra POP","network":{"id":"fd7b30d6-f514-4cd0-a5ac-29a774f53a43","name":"Ghana Fibre Network"}}}
{"type":"Feature","properties":{"id":"2","name":"Kumasi POP","network":{"id":"fd7b30d6-f514-4cd0-a5ac-29a774f53a43","name":"Ghana Fibre Network"}}}
```

### GeoJSON transformation specification

This section describes the rules for transforming an OFDS network from JSON format to GeoJSON format.

To transform an OFDS network from JSON format to GeoJSON format, you must:

* Create an empty JSON object for the nodes feature collection and set its `.type` to 'FeatureCollection'.
* Create an empty JSON object for the links feature collection and set its `.type` to 'FeatureCollection'.
* For each contract in `contracts`, [dereference the phase references](#dereference-a-phase-reference) in `.relatedPhases`.
* For each node in `nodes`:
  * Convert the node to a GeoJSON feature:
    * Create an empty JSON object for the feature.
    * Set the feature's:
    * `.type` to 'Feature'.
    * `.geometry` to the node's `.location`, if it exists. Otherwise, set `.geometry` to `Null`.
    * `.properties` to the properties of the node, excluding `.location`.
    * [Dereference the organisation references](#dereference-an-organisation-reference) in `.properties.physicalInfrastructureProvider` and `.networkProvider`.
    * [Dereference the phase reference](#dereference-a-phase-reference) in the feature's `.phase` property.
    * Set `.properties.network` to the properties of the network, excluding `.nodes`, `.links`, `.phases` and `.organisations`.
  * Add the feature to the nodes feature collection.
* For each link in `links`:
  * Convert the link to a GeoJSON Feature:
    * Create an empty JSON object for the feature.
    * Set the feature's:
    * `.type` to 'Feature'.
    * `.geometry` to the link's `.route`, if it exists. Otherwise, set `.geometry` to `Null`.
    * `.properties` to the properties of the link, excluding `.route`.
    * [Dereference the organisation references](#dereference-an-organisation-reference) in `.properties.physicalInfrastructureProvider` and `.networkProvider`.
    * [Dereference the phase reference](#dereference-a-phase-reference) in `.properties.phase`.
    * [Dereference the node ids](#dereference-a-node-id) in `properties.start` and `properties.end`.
    * Set `.properties.network` to the properties of the network, excluding `.nodes`, `.links`, `.phases` and `.organisations`.
  * Add the feature to the links feature collection.

#### Common operations

##### Dereference an organisation reference

Get the `Organisation` object in `organisations` whose `.id` is equal to the `.id` of the `OrganizationReference`.

##### Dereference a phase reference

Get the `Phase` object in `phases` whose `.id` is equal to the `id` of the `PhaseReference`.

##### Dereference a node ID

Get the `Node` object in `nodes` whose `.id` is equal to the ID.

### Reference implementation

A reference implementation of the transformation is [available in Python on Github](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/blob/main/manage.py). We strongly encourage any re-implementations to read its commented code, to ensure correctness.

## CSV

```{admonition} Alpha consultation
This section has [open issues](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues?q=is%3Aopen+is%3Aissue+label%3A%22CSV+format%22).
```

This section describes how to publish data in CSV format.

The CSV format has 10 tables, reflecting the structure of the [schema](schema.md). Arrays of objects in the schema are represented as separate tables:

* [Networks](#table-structure)
  * [Nodes](#nodes)
    * [International connections](#international-connections)
  * [Links](#links)
  * [Phases](#phases)
    * [Funders](#funders)
  * [Organisations](#organisations)
  * [Contracts](#contracts)
    * [Documents](#documents)
    * [Related phases](#related-phases)

The field in the schema that each column represents is identified by the field's [JSON Pointer](https://tools.ietf.org/html/rfc6901). Rows in child tables are related to rows in parent tables using the parent object's `id` field.

The following example shows a network with two nodes represented in JSON format and as tables. Note how the network's `.id` appears in both tables.

::::{tab-set}

:::{tab-item} JSON

```{jsoninclude} ../../examples/json/network-package.json
:jsonpointer: /networks/0
:exclude: links,phases,organisations,contracts
```

:::

:::{tab-item} Networks table

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../examples/csv/networks.csv
```

:::

:::{tab-item} Nodes table

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../examples/csv/nodes.csv
```

:::

::::

### Table structure

This section describes the structure of the tables in the CSV format and the relationship between the tables. Example CSV files and blank templates are provided for each table.

The networks table is the main table. It is related to the following tables:

* [Nodes](#nodes): one-to-many by `id`
* [Links](#links): one-to-many by `id`
* [Phases](#phases): one-to-many by `id`
* [Organisations](#organisations): one-to-many by `id`
* [Contracts](#contracts): one-to-many by `id`

The fields in this table are listed below. You can also download an [example CSV file](../../examples/csv/networks.csv) or a [blank template](../../examples/csv/template/networks.csv) for this table.

```{jsonschema} ../../schema/network-schema.json
:include: id,name,website,publisher,publicationDate,collectionDate,crs,accuracy,accuracyDetails,language
```

#### Nodes

This table is related to the following tables:

* [Networks](#table-structure): many-to-one by `id`
* [International connections](#international-connections): one-to-many by `nodes/0/id`

The fields in this table are listed below. You can also download an [example CSV file](../../examples/csv/nodes.csv) or a [blank template](../../examples/csv/template/nodes.csv).

```{jsonschema} ../../schema/network-schema.json
:include: id,nodes/0/id,nodes/0/name,nodes/0/phase,nodes/0/status,nodes/0/location,nodes/0/address,nodes/0/type,nodes/0/accessPoint,nodes/0/power,nodes/0/technologies,nodes/0/physicalInfrastructureProvider,nodes/0/networkProvider
```

##### International connections

This table is related to the following tables:

* [Nodes](#nodes): many-to-one by `nodes/0/id`

The fields in this table are listed below. You can also download an [example CSV file](../../examples/csv/nodes_internationalConnections.csv) or a [blank template](../../examples/csv/template/nodes_internationalConnections.csv).

```{jsonschema} ../../schema/network-schema.json
:include: id,nodes/0/id,nodes/0/internationalConnections/0/streetAddress,nodes/0/internationalConnections/0/locality,nodes/0/internationalConnections/0/region,nodes/0/internationalConnections/0/postalCode,nodes/0/internationalConnections/0/country
```

#### Links

This table is related to the following tables:

* [Networks](#table-structure): many-to-one by `id`

The fields in this table are listed below. You can also download an [example CSV file](../../examples/csv/links.csv) or a [blank template](../../examples/csv/template/links.csv).

```{jsonschema} ../../schema/network-schema.json
:include: id,links/0/id,links/0/name,links/0/phase,links/0/status,links/0/readyForServiceDate,links/0/start,links/0/end,links/0/route,links/0/physicalInfrastructureProvider,links/0/networkProvider,links/0/supplier,links/0/transmissionMedium,links/0/deployment,links/0/deploymentDetails,links/0/darkFibre,links/0/fibreType,links/0/fibreTypeDetails,links/0/fibreCount,links/0/fibreLength,links/0/technologies,links/0/capacity,links/0/capacityDetails,links/0/countries,links/0/directed
```

#### Phases

This table is related to the following tables:

* [Networks](#table-structure): many-to-one by `id`
* [Funders](#funders): one-to-many by `phases/0/id`

The fields in this table are listed below. You can also download an [example CSV file](../../examples/csv/phases.csv) or a [blank template](../../examples/csv/template/phases.csv).

```{jsonschema} ../../schema/network-schema.json
:include: id,phases/0/name,phases/0/description
```

##### Funders

This table is related to the following tables:

* [Phases](#phases): many-to-one by `phase/0/id`

The fields in this table are listed below. You can also download an [example CSV file](../../examples/csv/phases_funders.csv) or a [blank template](../../examples/csv/template/phases_funders.csv).

```{jsonschema} ../../schema/network-schema.json
:include: id,phases/0/id,phases/0/funders/0/id,phases/0/funders/0/name
```

#### Organisations

This table is related to the following tables:

* [Network](#table-structure): many-to-one by `id`

The fields in this table are listed below. You can also download an [example CSV file](../../examples/csv/organisations.csv) or a [blank template](../../examples/csv/template/organisations.csv).

```{jsonschema} ../../schema/network-schema.json
:include: id,organisations/0/id,organisations/0/name,organisations/0/identifier,organisations/0/country,organisations/0/roles,organisations/0/roleDetails,organisations/0/website,organisations/0/logo
```

#### Contracts

This table is related to the following tables:

* [Network](#table-structure): many-to-one by `id`
* [Documents](#documents): one-to-many by `contracts/0/id`

The fields in this table are listed below. You can also download an [example CSV file](../../examples/csv/contracts.csv) or a [blank template](../../examples/csv/template/contracts.csv).

```{jsonschema} ../../schema/network-schema.json
:include: id,contracts/0/id,contracts/0/title,contracts/0/description,contracts/0/type,contracts/0/value,contracts/0/dateSigned
```

##### Documents

This table is related to the following tables:

* [Contracts](#contracts): many-to-one by `contracts/0/id`

The fields in this table are listed below. You can also download an [example CSV file](../../examples/csv/contracts_documents.csv) or a [blank template](../../examples/csv/template/contracts_documents.csv).

```{jsonschema} ../../schema/network-schema.json
:include: id,contracts/0/id,contracts/0/documents/0/title,contracts/0/documents/0/description,contracts/0/documents/0/url,contracts/0/documents/0/format
```

##### Related phases

This table is related to the following tables:

* [Contracts](#contracts): many-to-one by `contracts/0/id`

The fields in this table are listed below. You can also download an [example CSV file](../../examples/csv/contracts_relatedPhases.csv) or a [blank template](../../examples/csv/template/contracts_relatedPhases.csv).

```{jsonschema} ../../schema/network-schema.json
:include: id,contracts/0/id,contracts/0/relatedPhases/0/id,contracts/0/relatedPhases/0/name
```
