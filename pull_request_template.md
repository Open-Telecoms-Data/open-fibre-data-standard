**Related issues**
*Add links to related issues here. Use [keywords](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword) if you want an issue to be automatically closed when the PR is merged.*

**Description**
*If the changes in the PR are not sufficiently explained by the related issues and commit messages, add a description here*

**Checklist**
- [ ] Update the changelog ([style guide](https://ofds-standard-development-handbook.readthedocs.io/en/latest/style/changelog_style_guide.html))
- [ ] Run `./manage.py pre-commit` to update derivative schema files, reference documentation and examples
- [ ] If there are changes to `examples/geojson/nodes.geojson` or `examples/geojson/spans.geojson`, check and update the data use examples:
  - [ ] `examples/leaflet/leaflet.ipynb`
  - [ ] `examples/qgis/geojson.qgs`
