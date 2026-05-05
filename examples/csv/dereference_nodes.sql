SELECT
    ST_GeomFromText(n."nodes/0/location")                           AS geometry,
    n."nodes/0/id"                                                  AS identifier,
    n."nodes/0/name"                                                AS name,
    n."nodes/0/phase/name"                                          AS phase,
    n."nodes/0/status"                                              AS status,

    -- address (comma-separated concatenation of non-null, non-empty parts)
    TRIM(
        COALESCE(NULLIF(n."nodes/0/address/streetAddress", '') || ', ', '') ||
        COALESCE(NULLIF(n."nodes/0/address/locality",      '') || ', ', '') ||
        COALESCE(NULLIF(n."nodes/0/address/region",        '') || ', ', '') ||
        COALESCE(NULLIF(n."nodes/0/address/postalCode",    '') || ', ', '') ||
        COALESCE(NULLIF(n."nodes/0/address/country",       ''), '')
    )                                                               AS address,

    n."nodes/0/type"                                                AS type,
    n."nodes/0/supportingInfrastructure/type"                       AS supportingInfrastructure__type,
    n."nodes/0/supportingInfrastructure/description"                AS supportingInfrastructure__description,
    n."nodes/0/supportingInfrastructure/owner/name"                 AS supportingInfrastructure__owner,
    n."nodes/0/supportingInfrastructure/spareCapacity"              AS supportingInfrastructure__spareCapacity,
    n."nodes/0/accessPoint"                                         AS accessPoint,
    n."nodes/0/power"                                               AS power,
    n."nodes/0/technologies"                                        AS technologies,
    n."nodes/0/transmissionMediumOwner/name"                        AS transmissionMediumOwner,

    -- networkProviders (many-to-many → semicolon-separated names)
    (
        SELECT GROUP_CONCAT("nodes/0/networkProviders/0/name", ';')
        FROM "nodes_networkProviders.csv"."nodes_networkProviders"
        WHERE "nodes/0/id" = n."nodes/0/id"
    )                                                               AS networkProviders,

    -- internationalConnections (child rows → semicolon-separated countries)
    (
        SELECT GROUP_CONCAT("nodes/0/internationalConnections/0/country", ';')
        FROM "nodes_internationalConnections.csv"."nodes_internationalConnections"
        WHERE "nodes/0/id" = n."nodes/0/id"
    )                                                               AS internationalConnections

FROM "nodes.csv".nodes n;
