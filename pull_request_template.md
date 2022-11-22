**Related issues**

<!-- Add links to related issues here. If you want an issue to be automatically closed when the PR is merged, use keywords (https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword) -->

**Description**

<!-- If the changes in the PR are not sufficiently explained by the related issues and commit messages, add a description here -->

**Merge checklist**

<!-- Complete the checklist before requesting a review. -->

- [ ] Update the changelog ([style guide](https://ofds-standard-development-handbook.readthedocs.io/en/latest/style/changelog_style_guide.html))
- [ ] Run `./manage.py pre-commit` to update derivative schema files, reference documentation and examples

If there are changes to `network-schema.json`, `network-package-schema.json`, `reference/publication_formats/json.md`, `reference/publication_formats/geojson.md` or `guidance/publication.md#how-to-publish-large-networks`, update the relevant manually authored examples:

- [ ] `examples/json/`:
  - [ ] `network-package.json`
  - [ ] `api-response.json`
  - [ ] `multiple-networks.json`
  - [ ] `network-embedded.json`
  - [ ] `network-separate-endpoints.json`
  - [ ] `network-separate-files.json`
  - [ ] `nodes-endpoint.json`
  - [ ] `spans-endpoint.json`
- [ ] `examples/geojson/`:
  - [ ] `api-response.geojson`
  - [ ] `multiple-networks.geojson`

If you used a validation keyword, type or format that is not [already used in the schema](https://ofds-standard-development-handbook.readthedocs.io/en/latest/standard/schema.html#json-schema-usage):

- [ ] Update the list of validation keywords, types or formats in [JSON Schema usage](https://ofds-standard-development-handbook.readthedocs.io/en/latest/standard/schema.html#json-schema-usage).
- [ ] Add a field that fails validation against the new keyword, type or format to [`network-package-invalid.json`](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/blob/0.1-dev/examples/json/network-package-invalid.json).
- [ ] Check that [OFDS CoVE](https://ofds.cove.opendataservices.coop/) reports an appropriate validation error.

If you added a normative rule that is not encoded in JSON Schema:

- [ ] Update the list of [other normative rules](https://ofds-standard-development-handbook.readthedocs.io/en/latest/standard/schema.html#other-normative-rules).
- [ ] Add a field that does not conform to the rule to [`network-package-additional-checks.json`](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/blob/0.1-dev/examples/json/network-package-additional-checks.json).
- [ ] Open a [new issue](https://github.com/Open-Telecoms-Data/lib-cove-ofds/issues/new/choose) to add an additional check to Lib Cove OFDS.

If there are changes to `examples/geojson/nodes.geojson` or `examples/geojson/spans.geojson`, check and update the data use examples:

- [ ] `examples/leaflet/leaflet.ipynb`
- [ ] `examples/qgis/geojson.qgs`
