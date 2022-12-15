# GeoJSON

```{admonition} 0.1.0-beta release
Welcome to the Open Fibre Data Standard 0.1.0-beta release.

We want to hear your feedback on the standard and its documentation. For general feedback, questions and suggestions, you can comment on an existing [discussion](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/discussions) or start a new one. For bug reports or feedback on specific elements of the data model and documentation, you can comment on the issues linked in the documentation or you can [create a new issue](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/new/choose).

To comment on or create discussions and issues, you need to [sign up for a free GitHub account](https://github.com/signup). If you prefer to provide feedback privately, you can email [info@opentelecomdata.net](mailto:info@opentelecomdata.net).
```

```{admonition} Consultation
This page has [open issues](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues?q=is%3Aopen+is%3Aissue+label%3A%22GeoJSON+format%22+).
```

This page describes how to publish data in GeoJSON format.

If your data is small enough to fit into memory or if you are publishing data via an API, you should use the [small files and API responses option](#small-files-and-api-responses-option). If your data is too large to fit into memory, you should use the [streaming option](#streaming-option).

## Small files and API responses option

Publish separate GeoJSON [feature collections](https://datatracker.ietf.org/doc/html/rfc7946#section-3.3) for nodes and spans, according to the [GeoJSON transformation specification](#geojson-transformation-specification).

::::{tab-set}

:::{tab-item} Nodes feature collection
The following example shows a GeoJSON feature collection containing nodes:

```{jsoninclude} ../../../examples/geojson/nodes.geojson
:jsonpointer:
:expand: features
```

:::

:::{tab-item} Spans feature collection
The following example shows a GeoJSON feature collection containing spans:

```{jsoninclude} ../../../examples/geojson/spans.geojson
:jsonpointer:
:expand: features
```

:::

::::

Each feature collection may contain features from one or more networks. The network each feature relates to is identified by its `.properties.network.id`.

The following example shows a GeoJSON feature collection containing features from two networks:

```{jsoninclude} ../../../examples/geojson/multiple-networks.geojson
:jsonpointer:
:expand: features
```

For data published via a paginated API, you should add a top-level `links` object to the feature collection to provide URLs for the next and previous pages of results:

::::{tab-set}

:::{tab-item} Links object schema

```{jsonschema} ../../../schema/network-package-schema.json
:pointer: /properties/links
```

:::

:::{tab-item} API response example
The following example shows a GeoJSON feature collection containing two features with URLS for the next and previous pages of results.

```{jsoninclude} ../../../examples/geojson/api-response.geojson
:jsonpointer:
```

:::

::::

## Streaming option

The streaming option describes how to publish multiple networks in GeoJSON format with support for streaming. You should only use this option if your data is too large to load into memory.

The streaming option for GeoJSON is separate [Newline-delimited GeoJSON](https://stevage.github.io/ndgeojson/) files for nodes and spans, in which each line is a GeoJSON feature structured according to the [GeoJSON transformation specification](#geojson-transformation-specification).

The following example shows a newline-delimited GeoJSON file containing two features:

```
{"type":"Feature","properties":{"id":"1","name":"Accra POP","network":{"id":"fd7b30d6-f514-4cd0-a5ac-29a774f53a43","name":"Ghana Fibre Network"}}}
{"type":"Feature","properties":{"id":"2","name":"Kumasi POP","network":{"id":"fd7b30d6-f514-4cd0-a5ac-29a774f53a43","name":"Ghana Fibre Network"}}}
```

## GeoJSON transformation specification

This section describes the rules for transforming an OFDS network from JSON format to GeoJSON format.

To transform an OFDS network from JSON format to GeoJSON format, you must:

- Create an empty JSON object for the nodes feature collection and set its `.type` to 'FeatureCollection'.
- Create an empty JSON object for the spans feature collection and set its `.type` to 'FeatureCollection'.
- For each contract in `contracts`, [dereference the phase references](#dereference-a-phase-reference) in `.relatedPhases`.
- For each node in `nodes`:
  - Convert the node to a GeoJSON feature:
    - Create an empty JSON object for the feature.
    - Set the feature's:
    - `.type` to 'Feature'.
    - `.geometry` to the node's `.location`, if it exists. Otherwise, set `.geometry` to `Null`.
    - `.properties` to the properties of the node, excluding `.location`.
    - [Dereference the organisation references](#dereference-an-organisation-reference) in `.properties.physicalInfrastructureProvider` and `.networkProviders`.
    - [Dereference the phase reference](#dereference-a-phase-reference) in the feature's `.phase` property.
    - Set `.properties.network` to the properties of the network, excluding `.nodes`, `.spans`, `.phases` and `.organisations`.
  - Add the feature to the nodes feature collection.
- For each span in `spans`:
  - Convert the span to a GeoJSON Feature:
    - Create an empty JSON object for the feature.
    - Set the feature's:
    - `.type` to 'Feature'.
    - `.geometry` to the span's `.route`, if it exists. Otherwise, set `.geometry` to `Null`.
    - `.properties` to the properties of the span, excluding `.route`.
    - [Dereference the organisation references](#dereference-an-organisation-reference) in `.properties.physicalInfrastructureProvider` and `.networkProviders`.
    - [Dereference the phase reference](#dereference-a-phase-reference) in `.properties.phase`.
    - [Dereference the node ids](#dereference-a-node-id) in `properties.start` and `properties.end`.
    - Set `.properties.network` to the properties of the network, excluding `.nodes`, `.spans`, `.phases` and `.organisations`.
  - Add the feature to the spans feature collection.

### Common operations

#### Dereference an organisation reference

Get the `Organisation` object in `organisations` whose `.id` is equal to the `.id` of the `OrganizationReference`.

#### Dereference a phase reference

Get the `Phase` object in `phases` whose `.id` is equal to the `id` of the `PhaseReference`.

#### Dereference a node ID

Get the `Node` object in `nodes` whose `.id` is equal to the ID.

### Reference implementation

A reference implementation of the transformation is [available in Python on Github](https://github.com/Open-Telecoms-Data/lib-cove-ofds). We strongly encourage any re-implementations to read its commented code, to ensure correctness.
