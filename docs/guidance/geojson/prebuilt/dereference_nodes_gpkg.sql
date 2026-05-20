-- Dereference the nodes table in an OFDS GeoPackage.
-- Use this script to export nodes in GeoJSON format: https://standard.ofds.info/en/latest/guidance/use/geojson-prebuilt/
-- OFDS GeoPackage reference documentation: https://standard.ofds.info/en/latest/reference/data_formats/geopackage/
-- 
-- Deferencing method:
-- - Replaces all integer FK references with their human-readable labels:
--   - codelist columns → codelist code
--   - organisation FKs → organisation name
--   - phase FKs → phase name
--   - network FKs → network name
--	 - international connection FKs → country names
-- - Aggregates many-to-many relations (type, technologies, networkProviders, international connections)
-- as semicolon-separated strings.
-- - Concatenates address components into comma-separated strings
WITH
    node_types AS (
        SELECT
            base_id,
            GROUP_CONCAT(code, ';') AS type
        FROM
            relation_nodes_type
            JOIN codelist_open_nodeType ON related_id = codelist_open_nodeType.id
        GROUP BY
            base_id
    ),
    node_technologies AS (
        SELECT
            base_id,
            GROUP_CONCAT(code, ';') AS technologies
        FROM
            relation_nodes_technologies
            JOIN codelist_open_nodeTechnologies ON related_id = codelist_open_nodeTechnologies.id
        GROUP BY
            base_id
    ),
    node_network_providers AS (
        SELECT
            base_id,
            GROUP_CONCAT(name, ';') AS networkProviders
        FROM
            relation_nodes_networkProviders
            JOIN organisations ON related_id = organisations.id
        GROUP BY
            base_id
    ),
    node_international_connections AS (
        SELECT
            node_id,
            GROUP_CONCAT(country, ';') AS internationalConnections
        FROM
            nodes_internationalConnections
        GROUP BY
            node_id
    )
SELECT
    n.geom,
    networks.name AS network,
    n.ofds_id AS identifier,
    n.name,
    phases.name AS phase,
    n.status,
    concat_ws (
        ', ',
        n."address__streetAddress",
        n."address__locality",
        n."address__region",
        n."address__postalCode",
        n."address__country"
    ) AS address,
    node_types.type,
    supporting_infrastructure_type.code AS supportingInfrastructure__type,
    n.supportingInfrastructure__description,
    supporting_infrastructure_owner.name AS supportingInfrastructure__owner,
    n.supportingInfrastructure__spareCapacity,
    n.accessPoint,
    n.power,
    node_technologies.technologies,
    transmission_medium_owner.name AS transmissionMediumOwner,
    node_network_providers.networkProviders,
    node_international_connections.internationalConnections
FROM
    nodes n
    LEFT JOIN phases ON n.phase = phases.id
    LEFT JOIN codelist_open_nodeSupportingInfrastructure supporting_infrastructure_type ON n.supportingInfrastructure__type = supporting_infrastructure_type.id
    LEFT JOIN organisations supporting_infrastructure_owner ON n.supportingInfrastructure__owner = supporting_infrastructure_owner.id
    LEFT JOIN organisations transmission_medium_owner ON n.transmissionMediumOwner = transmission_medium_owner.id
    LEFT JOIN networks ON n.network_id = networks.id
    LEFT JOIN node_types ON n.id = node_types.base_id
    LEFT JOIN node_technologies ON n.id = node_technologies.base_id
    LEFT JOIN node_network_providers ON n.id = node_network_providers.base_id
    LEFT JOIN node_international_connections ON n.id = node_international_connections.node_id;
