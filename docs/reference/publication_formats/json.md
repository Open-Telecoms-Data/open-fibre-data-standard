# JSON

```{admonition} Beta development version
Welcome to the development version of the Open Fibre Data Standard beta.

We want to hear your feedback on the standard and its documentation. For general feedback, questions and suggestions, you can comment on an existing [discussion](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/discussions) or start a new one. For bug reports or feedback on specific elements of the data model and documentation, you can comment on the issues linked in the documentation or you can [create a new issue](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/new/choose).

To comment on or create discussions and issues, you need to [sign up for a free GitHub account](https://github.com/signup). If you prefer to provide feedback privately, you can email [info@opentelecomdata.net](mailto:info@opentelecomdata.net).
```

This page describes how to publish data in JSON format.

If your data is small enough to fit into memory or if you are publishing data via an API, you should use the [small files and API responses option](#small-files-and-api-responses-option). If your data is too large to fit into memory, you should use the [streaming option](#streaming-option).

For guidance on paginating or streaming individual networks, see [how to publish large networks](../../guidance/publication.md#how-to-publish-large-networks).

## Small files and API responses option

The network package schema describes the structure of the container for publishing one or more networks in JSON format and for supporting pagination.

For this version of OFDS, the canonical URL of the schema is [https://raw.githubusercontent.com/Open-Telecoms-Data/open-fibre-data-standard/0__1__0__beta/schema/network-package-schema.json](https://raw.githubusercontent.com/Open-Telecoms-Data/open-fibre-data-standard/0__1__0__beta/schema/network-package-schema.json). Use the canonical URL to make sure that your software, documentation or other resources refer to the specific version of the schema with which they were tested.

This page presents the schema in an interactive browser. You can also download the canonical version of the schema as [JSON Schema](../../../schema/network-package-schema.json).

A network package is a JSON object that must include `.networks`: an array of `Network` objects as described by the [network schema](../schema.md). For data published via a paginated API, the optional `.links` object should be used to provide URLs for the next and previous pages of results.

::::{tab-set}

:::{tab-item} Schema browser
Click on schema elements to expand the tree, or use the '+' icon to expand all elements. Use { } to view the underlying schema for any section. Required fields are indicated in **bold**.

 <script src="../_static/docson/widget.js" data-schema="../network-schema.json"></script>
:::

:::{tab-item} Small file example
The following example shows a network package containing two networks:

```{jsoninclude} ../../../examples/json/multiple-networks.json
:jsonpointer:
:expand: networks
```

:::

:::{tab-item} API response example
The following example shows a network package containing two networks with URLs for the next and previous pages of results.

```{jsoninclude} ../../../examples/json/api-response.json
:jsonpointer:
:expand: networks,links
```

:::

::::

## Streaming option

The streaming option describes how to package multiple JSON-format networks with support for streaming. You should only use this option if your data is too large to load into memory.

The streaming option is a [JSON Lines](https://jsonlines.org/) file in which each line is a valid OFDS network, as described by the [network schema](../schema.md).

The following example shows a JSON Lines file containing two networks:

```
{"id":"fd7b30d6-f514-4cd0-a5ac-29a774f53a43","name":"Ghana Fibre Network"}
{"id":"acafe566-7ffa-416a-b3b4-84a52386a586","name":"Togo Fibre Network"}
```
