# Changelog

```{admonition} 0.1.0-beta release
Welcome to the Open Fibre Data Standard 0.1.0-beta release.

We want to hear your feedback on the standard and its documentation. For general feedback, questions and suggestions, you can comment on an existing [discussion](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/discussions) or start a new one. For bug reports or feedback on specific elements of the data model and documentation, you can comment on the issues linked in the documentation or you can [create a new issue](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/issues/new/choose).

To comment on or create discussions and issues, you need to [sign up for a free GitHub account](https://github.com/signup). If you prefer to provide feedback privately, you can email [info@opentelecomdata.net](mailto:info@opentelecomdata.net).
```
This page lists the changes in each version of the Open Fibre Data Standard.

## 0.1.0-beta - 2022-11-10

### Schema
* [#141](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/141) - Add `Span.fibreTypeDetails.fibreSubtype` field.
* [#144](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/144) - Clarify norms in the description of `links.start` and `links.end`.
* [#154](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/154) - Rename links to spans, related resources to links and pages to links.
* [#158](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/158) - Correct erroneous reference in `Span.capacityDetails`.
* [#157](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/157) - Use `links` to identify the version of the standard that describes the structure of the data.
* [#145](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/145) - Add validation rule for additional properties of `Geometry`.
* [#168](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/168), [#173](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/173), [#180](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/180) - Update schema URLs.

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
* [#180](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/180) - Collapse links in top-level schema reference table.

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
* [#168](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/168) - Update release and issue admonitions.
* [#177](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/177):
  * Add an invalid network package that fails validation against an instance of each validation keyword, type and format used in the schema
  * Add a network package that does not conform to each normative rule that is not encoded in the schema
* [#180](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/180) - Update release admonition, fix notebook viewer link, fix links in Leaflet notebook.

### Build

* [#158](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/158) - Update `manage.py`:
  * Generate CSV publication format reference docs.
  * Generate CSV template and examples.
  * Generate schema reference documentation.
  * Refactor
  * Use OFDS Kit to generate GeoJSON examples.
* [#168](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/pull/168) - Update version in `conf.py`.

## 0.1.0-alpha - 2022-09-22

`0.1.0-alpha` was the first version of the standard.