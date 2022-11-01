# Changelog

```{admonition} Alpha consultation
Welcome to the alpha release of the Open Fibre Data Standard.

We want to hear your feedback on the standard and its documentation. To find out how you can provide feedback, read the [alpha release announcement](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/discussions/115).
```
This page lists the changes in each version of the Open Fibre Data Standard.

## 0.1.0-beta - YYYY-MM-DD

### Schema
* [#141](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/141) - Add `Span.fibreTypeDetails.fibreSubtype` field.
* [#144](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/144) - Clarify norms in the description of `links.start` and `links.end`.
* [#154](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/154) - Rename links to spans, related resources to links and pages to links.
* [#158](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/158) - Correct erroneous reference in `Span.capacityDetails`.
* [#157](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/157) - Use `links` to identify the version of the standard that describes the structure of the data.

### Codelists

* [#158](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/158) - Add CSV file for organisationIdentifierScheme.

### Normative documentation
* [#141](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/141):
  * Update for latest schema.
* [#158](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/158):
  * Refactor publication formats reference to reduce page length.
  * Update schema reference:
    * Add list of referencing properties for each component.
    * Add more examples to schema reference.
    * Update for latest schema.
  * Add list of referencing properties for each codelist in codelist reference

### Non-normative documentation

* [#140](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/140) - Update actor definitions in the primer, and include translatable text in SVGs.
* [#141](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/141):
  * Update CSV template and examples to match latest schema.
  * Update network package for latest schema.
  * Update GeoJSON examples.
* [#158](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/158):
  * Update CSV template and examples to match latest schema.
  * Update network package for latest schema.
  * Update GeoJSON examples.
  * Remove unused blank JSON example.

### Build

* [#158](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/158) - Update `manage.py`:
  * Generate CSV publication format reference docs.
  * Generate CSV template and examples.
  * Generate schema reference documentation.
  * Refactor
  * Use OFDS Kit to generate GeoJSON examples.

## 0.1.0-alpha - 2022-09-22

`0.1.0-alpha` was the first version of the standard.