# CSV

```{admonition} Alpha consultation
This page has [open issues](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues?q=is%3Aopen+is%3Aissue+label%3A%22CSV+format%22).
```

This section describes the structure of the tables in the CSV format and the relationship between the tables. Example CSV files and blank templates are provided for each table.

The CSV format has 10 tables, reflecting the structure of the [schema](../schema.md). The networks table is the main table. Arrays of objects in the schema are represented as separate tables:

```{contents}
---
local: true
```

The field in the schema that each column represents is identified by the field's [JSON Pointer](https://tools.ietf.org/html/rfc6901). Rows in child tables are related to rows in parent tables using the parent object's `id` field.

The following example shows a network with two nodes represented in JSON format and as tables. Note how the network's `.id` appears in both tables.

::::{tab-set}

:::{tab-item} JSON

```{jsoninclude} ../../../examples/json/network-package.json
:jsonpointer: /networks/0
:exclude: spans,phases,organisations,contracts
```

:::

:::{tab-item} Networks table

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../../examples/csv/networks.csv
```

:::

:::{tab-item} Nodes table

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../../examples/csv/nodes.csv
```

:::

::::


## networks

This table is related to the following tables:

 * [nodes](#nodes): one-to-many by `id`
 * [spans](#spans): one-to-many by `id`
 * [phases](#phases): one-to-many by `id`
 * [organisations](#organisations): one-to-many by `id`
 * [contracts](#contracts): one-to-many by `id`
 * [links](#links): one-to-many by `id`

The fields in this table are listed below. You can also download an [example CSV file](../../../examples/csv/networks.csv) or a [blank template](../../../examples/csv/template/networks.csv) for this table.

```{jsonschema} ../../../schema/network-schema.json
:include: id,name,website,publisher,publicationDate,collectionDate,crs,accuracy,accuracyDetails,language
```

### nodes

This table is related to the following tables:

 * [networks](#networks): many-to-one by `id`
 * [internationalConnections](#internationalconnections): one-to-many by `nodes/0/id`

The fields in this table are listed below. You can also download an [example CSV file](../../../examples/csv/nodes.csv) or a [blank template](../../../examples/csv/template/nodes.csv) for this table.

```{jsonschema} ../../../schema/network-schema.json
:include: id,nodes/0/id,nodes/0/name,nodes/0/phase,nodes/0/status,nodes/0/location,nodes/0/address,nodes/0/type,nodes/0/accessPoint,nodes/0/power,nodes/0/technologies,nodes/0/physicalInfrastructureProvider,nodes/0/networkProvider
```

#### internationalConnections

This table is related to the following tables:

 * [nodes](#nodes): many-to-one by `nodes/0/id`

The fields in this table are listed below. You can also download an [example CSV file](../../../examples/csv/nodes_internationalConnections.csv) or a [blank template](../../../examples/csv/template/nodes_internationalConnections.csv) for this table.

```{jsonschema} ../../../schema/network-schema.json
:include: id,nodes/0/id,nodes/0/internationalConnections/0/streetAddress,nodes/0/internationalConnections/0/locality,nodes/0/internationalConnections/0/region,nodes/0/internationalConnections/0/postalCode,nodes/0/internationalConnections/0/country
```

### spans

This table is related to the following tables:

 * [networks](#networks): many-to-one by `id`

The fields in this table are listed below. You can also download an [example CSV file](../../../examples/csv/spans.csv) or a [blank template](../../../examples/csv/template/spans.csv) for this table.

```{jsonschema} ../../../schema/network-schema.json
:include: id,spans/0/id,spans/0/name,spans/0/phase,spans/0/status,spans/0/readyForServiceDate,spans/0/start,spans/0/end,spans/0/directed,spans/0/route,spans/0/physicalInfrastructureProvider,spans/0/networkProvider,spans/0/supplier,spans/0/transmissionMedium,spans/0/deployment,spans/0/deploymentDetails,spans/0/darkFibre,spans/0/fibreType,spans/0/fibreTypeDetails,spans/0/fibreCount,spans/0/fibreLength,spans/0/technologies,spans/0/capacity,spans/0/capacityDetails,spans/0/countries
```

### phases

This table is related to the following tables:

 * [networks](#networks): many-to-one by `id`
 * [funders](#funders): one-to-many by `phases/0/id`

The fields in this table are listed below. You can also download an [example CSV file](../../../examples/csv/phases.csv) or a [blank template](../../../examples/csv/template/phases.csv) for this table.

```{jsonschema} ../../../schema/network-schema.json
:include: id,phases/0/id,phases/0/name,phases/0/description
```

#### funders

This table is related to the following tables:

 * [phases](#phases): many-to-one by `phases/0/id`

The fields in this table are listed below. You can also download an [example CSV file](../../../examples/csv/phases_funders.csv) or a [blank template](../../../examples/csv/template/phases_funders.csv) for this table.

```{jsonschema} ../../../schema/network-schema.json
:include: id,phases/0/id,phases/0/funders/0/id,phases/0/funders/0/name
```

### organisations

This table is related to the following tables:

 * [networks](#networks): many-to-one by `id`

The fields in this table are listed below. You can also download an [example CSV file](../../../examples/csv/organisations.csv) or a [blank template](../../../examples/csv/template/organisations.csv) for this table.

```{jsonschema} ../../../schema/network-schema.json
:include: id,organisations/0/id,organisations/0/name,organisations/0/identifier,organisations/0/country,organisations/0/roles,organisations/0/roleDetails,organisations/0/website,organisations/0/logo
```

### contracts

This table is related to the following tables:

 * [networks](#networks): many-to-one by `id`
 * [documents](#documents): one-to-many by `contracts/0/id`
 * [relatedPhases](#relatedphases): one-to-many by `contracts/0/id`

The fields in this table are listed below. You can also download an [example CSV file](../../../examples/csv/contracts.csv) or a [blank template](../../../examples/csv/template/contracts.csv) for this table.

```{jsonschema} ../../../schema/network-schema.json
:include: id,contracts/0/id,contracts/0/title,contracts/0/description,contracts/0/type,contracts/0/value,contracts/0/dateSigned
```

#### documents

This table is related to the following tables:

 * [contracts](#contracts): many-to-one by `contracts/0/id`

The fields in this table are listed below. You can also download an [example CSV file](../../../examples/csv/contracts_documents.csv) or a [blank template](../../../examples/csv/template/contracts_documents.csv) for this table.

```{jsonschema} ../../../schema/network-schema.json
:include: id,contracts/0/id,contracts/0/documents/0/title,contracts/0/documents/0/description,contracts/0/documents/0/url,contracts/0/documents/0/format
```

#### relatedPhases

This table is related to the following tables:

 * [contracts](#contracts): many-to-one by `contracts/0/id`

The fields in this table are listed below. You can also download an [example CSV file](../../../examples/csv/contracts_relatedPhases.csv) or a [blank template](../../../examples/csv/template/contracts_relatedPhases.csv) for this table.

```{jsonschema} ../../../schema/network-schema.json
:include: id,contracts/0/id,contracts/0/relatedPhases/0/id,contracts/0/relatedPhases/0/name
```

### links

This table is related to the following tables:

 * [networks](#networks): many-to-one by `id`

The fields in this table are listed below. You can also download an [example CSV file](../../../examples/csv/links.csv) or a [blank template](../../../examples/csv/template/links.csv) for this table.

```{jsonschema} ../../../schema/network-schema.json
:include: id,links/0/href,links/0/rel
```
