WITH -- See end of file for comments (the ogr2ogr SQLite dialect does not support files that begin with a comment)
    node_network_providers AS (
        SELECT
            "nodes/0/id",
            GROUP_CONCAT ("nodes/0/networkProviders/0/name", ';') AS networkProviders
        FROM
            "nodes_networkProviders.csv"."nodes_networkProviders"
        GROUP BY
            "nodes/0/id"
    ),
    node_international_connections AS (
        SELECT
            "nodes/0/id",
            GROUP_CONCAT ("nodes/0/internationalConnections/0/country", ';') AS internationalConnections
        FROM
            "nodes_internationalConnections.csv"."nodes_internationalConnections"
        GROUP BY
            "nodes/0/id"
    )
SELECT
    ST_GeomFromText (n."nodes/0/location") AS geometry,
    networks."name" AS network,
    n."nodes/0/id" AS identifier,
    n."nodes/0/name" AS name,
    n."nodes/0/phase/name" AS phase,
    n."nodes/0/status" AS status,
    TRIM(
        COALESCE(
            NULLIF(n."nodes/0/address/streetAddress", '') || ', ',
            ''
        ) || COALESCE(
            NULLIF(n."nodes/0/address/locality", '') || ', ',
            ''
        ) || COALESCE(
            NULLIF(n."nodes/0/address/region", '') || ', ',
            ''
        ) || COALESCE(
            NULLIF(n."nodes/0/address/postalCode", '') || ', ',
            ''
        ) || COALESCE(NULLIF(n."nodes/0/address/country", ''), '')
    ) AS address,
    n."nodes/0/type" AS type,
    n."nodes/0/supportingInfrastructure/type" AS supportingInfrastructure__type,
    n."nodes/0/supportingInfrastructure/description" AS supportingInfrastructure__description,
    n."nodes/0/supportingInfrastructure/owner/name" AS supportingInfrastructure__owner,
    n."nodes/0/supportingInfrastructure/spareCapacity" AS supportingInfrastructure__spareCapacity,
    n."nodes/0/accessPoint" AS accessPoint,
    n."nodes/0/power" AS power,
    n."nodes/0/technologies" AS technologies,
    n."nodes/0/transmissionMediumOwner/name" AS transmissionMediumOwner,
    node_network_providers.networkProviders,
    node_international_connections.internationalConnections
FROM
    "nodes.csv".nodes n
    LEFT JOIN "networks.csv".networks networks ON n."id" = networks."id"
    LEFT JOIN node_network_providers ON n."nodes/0/id" = node_network_providers."nodes/0/id"
    LEFT JOIN node_international_connections ON n."nodes/0/id" = node_international_connections."nodes/0/id";

-- Dereference the nodes table in an OFDS CSV data.
-- Use this script to export nodes in GeoJSON format: https://standard.ofds.info/en/latest/guidance/use/geojson-prebuilt/
-- OFDS CSV format reference documentation: https://standard.ofds.info/en/latest/reference/data_formats/csv/
--
-- Deferencing method:
-- - Replaces identifier references with their human-readable labels:
--   - organisation identifiers → organisation name
--   - network identifiers → network name
--	 - international connections → country names
-- - Aggregates many-to-many relations (networkProviders, international connections)
-- as semicolon-separated strings.
-- - Concatenates address components into comma-separated strings