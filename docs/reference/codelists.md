# Codelists reference

Some schema fields refer to codelists, to limit and standardize the possible values of the fields, in order to promote data interoperability.

Codelists can either be open or closed. **Closed codelists** are intended to be comprehensive; for example, the currency codelist covers all currencies in the world. **Open codelists** are intended to be representative, but not comprehensive.

Publishers must use the codes in the codelists, unless no code is appropriate. If no code is appropriate and the codelist is **open**, then a publisher may use a new code outside those in the codelist. If no code is appropriate and the codelist is **closed**, then a publisher should instead create an issue in the [OFDS GitHub repository](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues).

```{admonition} Extending open codelists
:class: Tip

If you use new codes outside those in an open codelist, please create an issue in the [OFDS GitHub repository](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues), so that the codes can be considered for inclusion in the codelist.
```

The [schema](schema.md) has a `codelist` property to indicate the CSV File that defines the codes in the codelist (shown as tables below). It also has an `openCodelist` property, to indicate whether the codelist is open or closed.

Codes are case-sensitive, and are generally provided as English language camelCase. Codes must not be translated, though the OFDS team will work with publishers to translate code titles and definitions.

## Open codelists

## Closed codelists


### transmissionMedium

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/transmissionMedium.csv
```

### ownershipStructure

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/ownershipStructure.csv
```

### nodeType

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/nodeType.csv
```

### deployment

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/deployment.csv
```

### organisationClassification

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/organisationClassification.csv
```

### nodeTechnologies

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/nodeTechnologies.csv
```

### linkTechnologies

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/linkTechnologies.csv
```

### nodeStatus

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/nodeStatus.csv
```

### linkStatus

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/linkStatus.csv
```

### geometryType

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/geometryType.csv
```

### organisationRole

```{csv-table-no-translate}
:header-rows: 1
:widths: auto
:file: ../../codelists/organisationRole.csv
```

