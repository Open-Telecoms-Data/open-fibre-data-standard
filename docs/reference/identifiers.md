# Identifiers

```{admonition} Alpha consultation
Welcome to the alpha release of the Open Fibre Data Standard.

We want to hear your feedback on the standard and its documentation. To find out how you can provide feedback, read the [alpha release announcement](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/discussions/115).
```

In OFDS, there are two types of identifier: global identifiers and local identifiers.

## Global identifiers

The following identifiers are globally unique:

* [Network identifier](#network-identifier)
* [Organisation identifiers](#organisation-identifiers)

### Network identifier

To ensure that a network's `.id` is globally unique, it must be a universally unique identifier as defined by [RFC 4122](https://datatracker.ietf.org/doc/html/rfc4122).

Network identifiers should be consistent across each version of the data about a network.

For more information, see [how to generate universally unique identifiers](../guidance/publication.md#how-to-generate-universally-unique-identifiers).

### Organisation identifiers

To ensure that an organisation's `.identifier` is globally unique, it has two components:

::::{tab-set}

:::{tab-item} Schema

```{jsonschema} ../_build/dirhtml/_schema/network-schema.json
:pointer: /definitions/Organisation
:include: identifier/scheme,identifier/id
```

:::

:::{tab-item} Example
The following example shows the `.identifier` for an organisation registered at Ghana's Registrar General's Department, the scheme code for which is [GH-RGD](https://org-id.guide/list/GH-RGD):

```{jsoninclude} ../../examples/json/network-package.json
:jsonpointer: /networks/0/organisations/0/identifier
```

:::

::::

The `.identifier.scheme` field ensures that the identifier is globally unique, even if the same identifier appears in more than one scheme.

## Local identifiers

Most identifiers in OFDS only need to be unique among the identifiers used for the same type of object within the same scope. For example, node identifiers only need to be unique with the scope of the `.nodes` array. Uniqueness constraints are specified in the description of each identifier.

Some local identifiers are used for cross-referencing. For example, an organisation's `.id` is a local identifier used for cross-referencing from fields such as `Node.physicalInfrastructureProvider.id`.
