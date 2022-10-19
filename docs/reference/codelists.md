# Codelists reference

```{admonition} Alpha consultation
Welcome to the alpha release of the Open Fibre Data Standard.

We want to hear your feedback on the standard and its documentation. To find out how you can provide feedback, read the [alpha release announcement](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/discussions/115).
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

### nodeTechnologies

The node technologies codelist is used to indicate the technologies used in a node.

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/nodeTechnologies.csv
```

### organisationRole

The organisation role codelist is used to identify an organisation's roles in a network. An organisation can have one or more roles.

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/organisationRole.csv
```

### language

The language codelist is used to provide the default language used in text fields and the language of linked documents, using two-letter codes from ISO639-1.

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/language.csv
```

### linkTechnologies

The link technologies codelist is used to indicate the technologies used on a link.

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/linkTechnologies.csv
```

### nodeType

The node type codelist is used to categorise the nodes in a network.

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/nodeType.csv
```

### referenceRelationType

The reference relation type codelist consists of extensions to the [IANA Link Relationship Types](https://www.iana.org/assignments/link-relations/link-relations.xhtml#link-relations-1) constructed according to the [tag URI scheme](https://www.rfc-editor.org/rfc/rfc4151).

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/referenceRelationType.csv
```

### mediaType

The mediaType codelist is based on the [IANA Media Types list](https://www.iana.org/assignments/media-types/media-types.xhtml). The media type codelist adds an exceptional code for printed documents ('offline/print'), and omits any media type that is marked as deprecated or obsolete by IANA.

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/mediaType.csv
```

### contractType

The contract type codelist is used to categorise contracts based on the World Bank PPPLRC's [types of PPP arrangement](https://ppp.worldbank.org/public-private-partnership/agreements).

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/open/contractType.csv
```

## Closed codelists

### geometryType

The geometry type codelist is used to categorise the type of geometry represented by the geometry object.

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/geometryType.csv
```
### transmissionMedium

The transmission medium codelist is used to categorise the physical media of a link.

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/transmissionMedium.csv
```

### deployment

The deployment codelist is used to categorise the deployment of links.

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/deployment.csv
```

### currency

The currency codelist uses uppercase 3-letter codes from [ISO4217](https://www.iso.org/iso-4217-currency-codes.html).

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/currency.csv
```

### nodeStatus

The node status codelist is used to identify the operational status of a node.

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/nodeStatus.csv
```

### linkStatus

The link status codelist is used to indicate the operational status of a link.

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/linkStatus.csv
```

### country

The country codelist uses uppercase two-letter codes from [ISO3166-1](https://www.iso.org/iso-3166-country-codes.html). The country codelist adds a user-assigned code for Kosovo ('XK').

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/country.csv
```

### fibreType

The fibre type codelist is a subset of [ITU-T recommendations](https://www.itu.int/rec/T-REC-G/en) that describe characteristics of optical fibre and cables. It is used to categorise the type of fibre used in a link.

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/closed/fibreType.csv
```

