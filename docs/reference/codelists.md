<!-- docs-type: reference https://diataxis.fr/reference/ -->

# Codelists

```{admonition} 0.3.0 release
Welcome to the Open Fibre Data Standard 0.3.0 release.

We want to hear your feedback on the standard and its documentation. For general feedback, questions and suggestions, you can comment on an existing [discussion](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/discussions) or start a new one. For bug reports or feedback on specific elements of the data model and documentation, you can comment on the issues in the [issue tracker](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues) or you can [create a new issue](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/new/choose).

To comment on or create discussions and issues, you need to [sign up for a free GitHub account](https://github.com/signup). If you prefer to provide feedback privately, you can email [info@opentelecomdata.net](mailto:info@opentelecomdata.net).
```

Some attributes in the OFDS [data model](data_model.md) and [formats](publication_formats/index.md) refer to codelists, to limit and standardise the possible values of the attribute, in order to promote data interoperability.

Codelists can either be open or closed. [**Closed codelists**](#closed-codelists) are intended to be comprehensive; for example, the currency codelist covers all currencies in the world. [**Open codelists**](#open-codelists) are intended to be representative, but not comprehensive.

Implementers must use the codes in the codelists, unless no code is appropriate. If no code is appropriate and the codelist is **open**, you may use a new code outside those in the codelist. If no code is appropriate and the codelist is **closed**, you should instead create an issue in the [OFDS GitHub repository](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues).

```{admonition} Extending open codelists
:class: Tip

If you use new codes outside those in an open codelist, please create an issue in the [OFDS GitHub repository](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues), so that the codes can be considered for inclusion in the codelist.
```

Codes are case-sensitive, and are generally provided as English language camelCase. Codes must not be translated.

Some codelists are specific to particular data formats. These are listed in the [format-specific codelists](#format-specific-codelists) section.

## Open codelists

### contractType

The contract type codelist is used to categorise contracts based on the World Bank PPPLRC's [types of PPP arrangement](https://ppp.worldbank.org/public-private-partnership/agreements).

This codelist is referenced by the following attributes:

- [`Contract/type`](data_model,network-schema.json,/$defs/Contract,type)

This codelist has the following codes:

````{dropdown} Codes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows
:open:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/contractType.csv
```

````

### language

The language codelist is used to provide the default language used in text attributes and the language of linked documents, using two-letter codes from ISO639-1.

This codelist is referenced by the following attributes:

- [`language`](json,network-schema.json,,language)

This codelist has the following codes:

````{dropdown} Codes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/language.csv
```

````

### mediaType

The mediaType codelist is based on the [IANA Media Types list](https://www.iana.org/assignments/media-types/media-types.xhtml). The media type codelist adds an exceptional code for printed documents ('offline/print'), and omits any media type that is marked as deprecated or obsolete by IANA.

This codelist is referenced by the following attributes:

- [`Document/format`](data_model,network-schema.json,/$defs/Document,format)

This codelist has the following codes:

````{dropdown} Codes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/mediaType.csv
```
````

### nodeSupportingInfrastructure

This codelist is referenced by the following properties:

- [`Node/supportingInfrastructure/type`](data_model,network-schema.json,/$defs/Node,supportingInfrastructure/type)

This codelist has the following codes:

````{dropdown} Codes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/nodeSupportingInfrastructure.csv
```
````

### nodeTechnologies

The node technologies codelist is used to indicate the technologies used in a node.

This codelist is referenced by the following attributes:

- [`Node/technologies`](data_model,network-schema.json,/$defs/Node,technologies)

This codelist has the following codes:

````{dropdown} Codes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows
:open:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/nodeTechnologies.csv
```

````

### nodeType

The node type codelist is used to categorise the nodes in a network.

This codelist is referenced by the following attributes:

- [`Node/type`](data_model,network-schema.json,/$defs/Node,type)

This codelist has the following codes:

````{dropdown} Codes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows
:open:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/nodeType.csv
```

````

### organisationIdentifierScheme

The organisation identifier scheme codelist uses the codes from [org-id.guide](http://org-id.guide/) to identify the register from which an organisation's identifier is drawn. You can search for codes by browsing the website or you can download the latest version of the codelist as a [CSV file](http://org-id.guide/download.csv).

This codelist is referenced by the following attributes:

- [`Identifier/scheme`](data_model,network-schema.json,/$defs/Organisation,identifier/scheme)

This codelist has the following codes:

````{dropdown} Codes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/organisationIdentifierScheme.csv
```

````

### organisationRole

The organisation role codelist is used to identify an organisation's roles in a network. An organisation can have one or more roles.

This codelist is referenced by the following attributes:

- [`Organisation/roles`](data_model,network-schema.json,/$defs/Organisation,roles)

This codelist has the following codes:

````{dropdown} Codes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows
:open:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/organisationRole.csv
```
````

### spanSupportingInfrastructure

This codelist is referenced by the following properties:

* [`Span/supportingInfrastructure/type`](data_model,network-schema.json,/$defs/Span,supportingInfrastructure/type)

This codelist has the following codes:

````{dropdown} Codes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows
:open:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/spanSupportingInfrastructure.csv
```
````

### spanTechnologies

The span technologies codelist is used to indicate the technologies used on a span.

This codelist is referenced by the following attributes:

- [`Span/technologies`](data_model,network-schema.json,/$defs/Span,technologies)

This codelist has the following codes:

````{dropdown} Codes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows
:open:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/spanTechnologies.csv
```

````

## Closed codelists

### country

The country codelist uses uppercase two-letter codes from [ISO3166-1](https://www.iso.org/iso-3166-country-codes.html). The country codelist adds a user-assigned code for Kosovo ('XK').

This codelist is referenced by the following attributes:

- [`Span/countries`](data_model,network-schema.json,/$defs/Span,countries)
- [`Organisation/country`](data_model,network-schema.json,/$defs/Organisation,country)
- [`Node/address/country`](data_model,network-schema.json,/$defs/Node,address/country)

This codelist has the following codes:

````{dropdown} Codes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/country.csv
```

````

### currency

The currency codelist uses uppercase 3-letter codes from [ISO4217](https://www.iso.org/iso-4217-currency-codes.html).

This codelist is referenced by the following attributes:

- [`Value/currency`](data_model,network-schema.json,/$defs/Contract,value/currency)

This codelist has the following codes:

````{dropdown} Codes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/currency.csv
```

````

### deployment

The deployment codelist is used to categorise the deployment of spans.

This codelist is referenced by the following attributes:

- [`Span/deployment`](data_model,network-schema.json,/$defs/Span,deployment)

This codelist has the following codes:

````{dropdown} Codes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows
:open:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/deployment.csv
```

````

### fibreType

The fibre type codelist is a subset of [ITU-T recommendations](https://www.itu.int/rec/T-REC-G/en) that describe characteristics of optical fibre and cables. It is used to categorise the type of fibre used in a span.

This codelist is referenced by the following attributes:

- [`Span/fibreType`](data_model,network-schema.json,/$defs/Span,fibreType)

This codelist has the following codes:

````{dropdown} Codes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows
:open:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/fibreType.csv
```

````

### nodeStatus

The node status codelist is used to identify the operational status of a node.

This codelist is referenced by the following attributes:

- [`Node/status`](data_model,network-schema.json,/$defs/Node,status)

This codelist has the following codes:

````{dropdown} Codes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows
:open:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/nodeStatus.csv
```

````

### spanStatus

The span status codelist is used to indicate the operational status of a span.

This codelist is referenced by the following attributes:

- [`Span/status`](data_model,network-schema.json,/$defs/Span,status)

This codelist has the following codes:

````{dropdown} Codes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows
:open:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/spanStatus.csv
```

````

### transmissionMedium

The transmission medium codelist is used to categorise the physical media of a span.

This codelist is referenced by the following attributes:

- [`Span/transmissionMedium`](data_model,network-schema.json,/$defs/Span,transmissionMedium)

This codelist has the following codes:

````{dropdown} Codes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows
:open:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/transmissionMedium.csv
```

````

## Format-specific codelists

### JSON

The following codelists are specific to the [JSON format](publication_formats/json/index.md).

#### geometryType

The geometry type codelist is used to categorise the type of geometry represented by the geometry object.

This codelist is referenced by the following attributes:

- [`Geometry/type`](json,network-schema.json,/$defs/Geometry,type)

This codelist has the following codes:

````{dropdown} Codes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows
:open:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/geometryType.csv
```

````

#### linkRelationType

The link relation type codelist consists of extensions to the [IANA Link Relationship Types](https://www.iana.org/assignments/link-relations/link-relations.xhtml#link-relations-1) constructed according to the [tag URI scheme](https://www.rfc-editor.org/rfc/rfc4151).

This codelist is referenced by the following attributes:

- [`Link/rel`](json,network-schema.json,/$defs/Link,rel)

This codelist has the following codes:

````{dropdown} Codes
:animate: fade-in-slide-down
:chevron: down-up
:icon: rows
:open:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/linkRelationType.csv
```

````
