# Publication formats reference

## JSON

## GeoJSON

### Transformation specification

To transform a JSON-format OFDS network to GeoJSON format, you must:

* Create an empty JSON object for the nodes feature collection and set its `.type` to 'FeatureCollection'.
* Create an empty JSON object for the links feature collection and set its `.type` to 'FeatureCollection'.
* For each contract in `contracts`, [dereference the phase references](#dereference-a-phase-reference) in `.relatedPhases`.
* For each node in `nodes`:
    * Convert the node to a GeoJSON feature:
        * Create an empty JSON object for the feature.
        * Set the feature's:
        * `.type` to 'Feature'.
        * `.geometry` to the node's `.location`, if it exists. Otherwise, set `.geometry` to `Null`.
        * `.properties` to the properties of the node, excluding `.location`.
        * [Dereference the organisation references](#dereference-an-organisation-reference) in `.properties.physicalInfrastructureProvider` and `.networkProvider`.
        * [Dereference the phase reference](#dereference-a-phase-reference) in the feature's `.phase` property.
        * Set `.properties.network` to the properties of the network, excluding `.nodes`, `.links`, `.phases` and `.organisations`.
    * Add the feature to the nodes feature collection.
* For each link in `links`:
    * Convert the link to a GeoJSON Feature:
        * Create an empty JSON object for the feature.
        * Set the feature's:
        * `.type` to 'Feature'.
        * `.geometry` to the link's `.route`, if it exists. Otherwise, set `.geometry` to `Null`.
        * `.properties` to the properties of the link, excluding `.route`.
        * [Dereference the organisation references](#dereference-an-organisation-reference) in `.properties.physicalInfrastructureProvider` and `.networkProvider`.
        * [Dereference the phase reference](#dereference-a-phase-reference) in `.properties.phase`.
        * [Dereference the node ids](#dereference-a-node-id) in `properties.start` and `properties.end`.
        * Set `.properties.network` to the properties of the network, excluding `.nodes`, `.links`, `.phases` and `.organisations`.
    * Add the feature to the links feature collection.

#### Common operations

##### Dereference an organisation reference

Get the `Organisation` object in `organisations` whose `.id` is equal to the `.id` of the `OrganizationReference`.

##### Dereference a phase reference

Get the `Phase` object in `phases` whose `.id` is equal to the `id` of the `PhaseReference`.

##### Dereference a node ID

Get the `Node` object in `nodes` whose `.id` is equal to the ID.

### Reference implementation

A reference implementation of the transformation is [available in Python on Github](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/blob/main/manage.py). We strongly encourage any re-implementations to read its commented code, to ensure correctness.

## CSV