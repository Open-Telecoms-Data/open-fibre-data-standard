# Publication formats reference

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

For this version of OFDS, the canonical URL of the schema is [https://raw.githubusercontent.com/Open-Telecoms-Data/open-fibre-data-standard/0.1.0-alpha/schema/network-package-schema.json](https://raw.githubusercontent.com/Open-Telecoms-Data/open-fibre-data-standard/0.1.0-alpha/schema/network-package-schema.json). Use the canonical URL to make sure that your software, documentation or other resources refer to the specific version of the schema with which they were tested.

This page presents the schema in an interactive browser, you can also download the canonical version of the schema as [JSON Schema](../../schema/network-package-schema.json).

A network package is a JSON object that must include `.networks`, an array of `Network` objects as described by the [network schema](schema.md). For data published via a paginated API, the optional `.pages` object should be used to provide links to the next and previous pages of results.

::::{tab-set}

:::{tab-item} Schema browser
Click on schema elements to expand the tree, or use the '+' icon to expand all elements. Use { } to view the underlying schema for any section. Required fields are indicated in **bold**.

 <script src="../_static/docson/widget.js" data-schema="../network-schema.json"></script> 
:::

:::{tab-item} Small file example
The following example shows a network package containing two networks:
```{jsoninclude} ../../examples/json/network-package.json
:jsonpointer:
```
:::

:::{tab-item} API response example
The following example shows a network package containing two networks with links to the next and previous pages of results.
```{jsoninclude} ../../examples/json/api-response.json
:jsonpointer:
```
:::

::::

### Streaming option

The streaming option describes how to package multiple JSON-format networks with support for streaming. You should only use this option if your data is too large to load into memory.

The streaming option is a [JSON Lines](https://jsonlines.org/) file in which each line is a valid OFDS network, as described by the [network schema](schema.md).

The following example shows a JSON Lines file containing two networks:

```
{"id": "1"}
{"id": "2"}
```

## GeoJSON

This section describes how to publish data in GeoJSON format.

If your data is small enough to fit into memory or if you are publishing data via an API, you should use the [small files and API responses option](#small-files-and-api-responses-option-1). If your data is too large to fit into memory, you should use the [streaming option](#streaming-option-1).

### Small files and API responses option

Publish separate GeoJSON [feature collections](https://datatracker.ietf.org/doc/html/rfc7946#section-3.3) for nodes and links, according to the [GeoJSON transformation specification](#geojson-transformation-specification).

::::{tab-set}

:::{tab-item} Nodes feature collection
The following example shows a GeoJSON feature collection containing nodes:
```{jsoninclude} ../../examples/geojson/nodes.geojson
:jsonpointer:
```
:::

:::{tab-item} Links feature collection
The following example shows a GeoJSON feature collection containing links:
```{jsoninclude} ../../examples/geojson/links.geojson
:jsonpointer:
```
:::

::::

Each feature collection may contain features from one or more networks. The network each feature relates to is identified by its `.properties.network.id`.

The following example shows a GeoJSON feature collection containing features from two networks:

```{jsoninclude} ../../examples/geojson/multiple-networks.geojson
:jsonpointer:
```

For data published via a paginated API, you should add a top-level `pages` object to the feature collection to provide links to the next and previous pages of results:

::::{tab-set}

:::{tab-item} Pages object schema
```{jsonschema} ../../schema/network-package-schema.json
:pointer: /properties/pages
```
:::

:::{tab-item} API response example
The following example shows a GeoJSON feature collection containing two features with links to the next and previous pages of results.
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
{"type": "Feature"}
{"type": "Feature"}
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

This section describes how to publish data in CSV format.

