# Codelists reference

```{admonition} 0.3.0 release
Welcome to the Open Fibre Data Standard 0.3.0 release.

We want to hear your feedback on the standard and its documentation. For general feedback, questions and suggestions, you can comment on an existing [discussion](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/discussions) or start a new one. For bug reports or feedback on specific elements of the data model and documentation, you can comment on the issues in the [issue tracker](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues) or you can [create a new issue](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/new/choose).

To comment on or create discussions and issues, you need to [sign up for a free GitHub account](https://github.com/signup). If you prefer to provide feedback privately, you can email [info@opentelecomdata.net](mailto:info@opentelecomdata.net).
```

Some schema fields refer to codelists, to limit and standardise the possible values of the fields, in order to promote data interoperability.

Codelists can either be open or closed. **Closed codelists** are intended to be comprehensive; for example, the currency codelist covers all currencies in the world. **Open codelists** are intended to be representative, but not comprehensive.

Publishers must use the codes in the codelists, unless no code is appropriate. If no code is appropriate and the codelist is **open**, then a publisher may use a new code outside those in the codelist. If no code is appropriate and the codelist is **closed**, then a publisher should instead create an issue in the [OFDS GitHub repository](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues).

```{admonition} Extending open codelists
:class: Tip

If you use new codes outside those in an open codelist, please create an issue in the [OFDS GitHub repository](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues), so that the codes can be considered for inclusion in the codelist.
```

The [schema](schema.md) has a `codelist` property to indicate the CSV file that defines the codes in the codelist (shown as tables below). It also has an `openCodelist` property, to indicate whether the codelist is open or closed.

Codes are case-sensitive, and are generally provided as English language camelCase. Codes must not be translated.

## Open codelists

### contractType

The contract type codelist is used to categorise contracts based on the World Bank PPPLRC's [types of PPP arrangement](https://ppp.worldbank.org/public-private-partnership/agreements).

This codelist is referenced by the following properties:

- [`Contract/type`](network-schema.json,/$defs/Contract,type)

This codelist has the following codes:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/contractType.csv
```

### language

The language codelist is used to provide the default language used in text fields and the language of linked documents, using two-letter codes from ISO639-1.

This codelist is referenced by the following properties:

- [`language`](network-schema.json,,language)

This codelist has the following codes:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/language.csv
```

### linkRelationType

The link relation type codelist consists of extensions to the [IANA Link Relationship Types](https://www.iana.org/assignments/link-relations/link-relations.xhtml#link-relations-1) constructed according to the [tag URI scheme](https://www.rfc-editor.org/rfc/rfc4151).

This codelist is referenced by the following properties:

- [`Link/rel`](network-schema.json,/$defs/Link,rel)

This codelist has the following codes:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/linkRelationType.csv
```

### mediaType

The mediaType codelist is based on the [IANA Media Types list](https://www.iana.org/assignments/media-types/media-types.xhtml). The media type codelist adds an exceptional code for printed documents ('offline/print'), and omits any media type that is marked as deprecated or obsolete by IANA.

This codelist is referenced by the following properties:

- [`Document/format`](network-schema.json,/$defs/Document,format)

This codelist has the following codes:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/mediaType.csv
```

### nodeTechnologies

The node technologies codelist is used to indicate the technologies used in a node.

This codelist is referenced by the following properties:

- [`Node/technologies`](network-schema.json,/$defs/Node,technologies)

This codelist has the following codes:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/nodeTechnologies.csv
```

### nodeType

The node type codelist is used to categorise the nodes in a network.

This codelist is referenced by the following properties:

- [`Node/type`](network-schema.json,/$defs/Node,type)

This codelist has the following codes:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/nodeType.csv
```

### organisationIdentifierScheme

The organisation identifier scheme codelist uses the codes from [org-id.guide](http://org-id.guide/) to identify the register from which an organisation's identifier is drawn. You can search for codes by browsing the website or you can download the latest version of the codelist as a [CSV file](http://org-id.guide/download.csv).

This codelist is referenced by the following properties:

- [`Identifier/scheme`](network-schema.json,/$defs/Identifier,scheme)

This codelist has the following codes:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/organisationIdentifierScheme.csv
```

### organisationRole

The organisation role codelist is used to identify an organisation's roles in a network. An organisation can have one or more roles.

This codelist is referenced by the following properties:

- [`Organisation/roles`](network-schema.json,/$defs/Organisation,roles)

This codelist has the following codes:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/organisationRole.csv
```

### spanTechnologies

The span technologies codelist is used to indicate the technologies used on a span.

This codelist is referenced by the following properties:

- [`Span/technologies`](network-schema.json,/$defs/Span,technologies)

This codelist has the following codes:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/spanTechnologies.csv
```

## Closed codelists

### country

The country codelist uses uppercase two-letter codes from [ISO3166-1](https://www.iso.org/iso-3166-country-codes.html). The country codelist adds a user-assigned code for Kosovo ('XK').

This codelist is referenced by the following properties:

- [`Span/countries`](network-schema.json,/$defs/Span,countries)
- [`Organisation/country`](network-schema.json,/$defs/Organisation,country)
- [`Address/country`](network-schema.json,/$defs/Address,country)

This codelist has the following codes:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/country.csv
```

### currency

The currency codelist uses uppercase 3-letter codes from [ISO4217](https://www.iso.org/iso-4217-currency-codes.html).

This codelist is referenced by the following properties:

- [`Value/currency`](network-schema.json,/$defs/Value,currency)

This codelist has the following codes:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/currency.csv
```

### deployment

The deployment codelist is used to categorise the deployment of spans.

This codelist is referenced by the following properties:

- [`Span/deployment`](network-schema.json,/$defs/Span,deployment)

This codelist has the following codes:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/deployment.csv
```

### fibreType

The fibre type codelist is a subset of [ITU-T recommendations](https://www.itu.int/rec/T-REC-G/en) that describe characteristics of optical fibre and cables. It is used to categorise the type of fibre used in a span.

This codelist is referenced by the following properties:

- [`Span/fibreType`](network-schema.json,/$defs/Span,fibreType)

This codelist has the following codes:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/fibreType.csv
```

### geometryType

The geometry type codelist is used to categorise the type of geometry represented by the geometry object.

This codelist is referenced by the following properties:

- [`Geometry/type`](network-schema.json,/$defs/Geometry,type)

This codelist has the following codes:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/geometryType.csv
```

### nodeStatus

The node status codelist is used to identify the operational status of a node.

This codelist is referenced by the following properties:

- [`Node/status`](network-schema.json,/$defs/Node,status)

This codelist has the following codes:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/nodeStatus.csv
```

### spanStatus

The span status codelist is used to indicate the operational status of a span.

This codelist is referenced by the following properties:

- [`Span/status`](network-schema.json,/$defs/Span,status)

This codelist has the following codes:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/spanStatus.csv
```

### transmissionMedium

The transmission medium codelist is used to categorise the physical media of a span.

This codelist is referenced by the following properties:

- [`Span/transmissionMedium`](network-schema.json,/$defs/Span,transmissionMedium)

This codelist has the following codes:

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/transmissionMedium.csv
```
