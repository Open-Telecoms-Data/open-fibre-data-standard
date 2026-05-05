-- database: network.gpkg
-- Full dereference of the spans table in network.gpkg.
-- Replaces all integer FK references with their semantic identifiers:
--   - codelist columns → codelist code
--   - organisation FKs → organisations.name
--   - node FKs → nodes.ofds_id
--   - phase FK → phases.name
--   - network FK → networks.name
--   - wayleave FKs → wayleaves.ofds_id
-- Many-to-many relations (networkProviders, transmissionMedium, deployment,
-- technologies, wayleaves, countries) are aggregated as semicolon-separated strings.

WITH
    span_network_providers AS (
        SELECT
            base_id,
            GROUP_CONCAT(name, ';') AS networkProviders
        FROM
            relation_spans_networkProviders
            JOIN organisations ON related_id = organisations.id
        GROUP BY
            base_id
    ),
    span_transmission_medium AS (
        SELECT
            base_id,
            GROUP_CONCAT(code, ';') AS transmissionMedium
        FROM
            relation_spans_transmissionMedium
            JOIN codelist_closed_transmissionMedium ON related_id = codelist_closed_transmissionMedium.id
        GROUP BY
            base_id
    ),
    span_deployment AS (
        SELECT
            base_id,
            GROUP_CONCAT(code, ';') AS deployment
        FROM
            relation_spans_deployment
            JOIN codelist_closed_deployment ON related_id = codelist_closed_deployment.id
        GROUP BY
            base_id
    ),
    span_technologies AS (
        SELECT
            base_id,
            GROUP_CONCAT(code, ';') AS technologies
        FROM
            relation_spans_technologies
            JOIN codelist_open_spanTechnologies ON related_id = codelist_open_spanTechnologies.id
        GROUP BY
            base_id
    ),
    span_wayleaves AS (
        SELECT
            base_id,
            GROUP_CONCAT(organisations.name, ';') AS wayleave_grantor,
            GROUP_CONCAT(
                CASE WHEN wayleaves.term__indefinite = 'true'
                    THEN 'indefinite'
                    ELSE wayleaves.term__years || ' years'
                END, ';'
            ) AS wayleave_term,
            GROUP_CONCAT(
                wayleaves.cost__perMetre__amount || ' ' ||
                wayleaves.cost__perMetre__currency || ' per metre (' ||
                CASE WHEN wayleaves.cost__recurring = 'true' THEN 'annual' ELSE 'one off' END ||
                ')', ';'
            ) AS wayleave_cost
        FROM
            relation_spans_wayleaves
            JOIN wayleaves ON related_id = wayleaves.id
            LEFT JOIN organisations ON wayleaves.grantor = organisations.id
        GROUP BY
            base_id
    ),
    span_countries AS (
        SELECT
            base_id,
            GROUP_CONCAT(code, ';') AS countries
        FROM
            relation_spans_countries
            JOIN codelist_closed_country ON related_id = codelist_closed_country.id
        GROUP BY
            base_id
    )

SELECT
    s.geom,
    s.ofds_id                                                       AS identifier,
    s.name,
    phases.name                                                     AS phase,
    s.status,
    s.readyForServiceDate,
    start_node.name || ' (' || start_node.ofds_id || ')'            AS start,
    end_node.name || ' (' || end_node.ofds_id || ')'                AS end,
    s.directed,
    transmission_medium_owner.name                                  AS transmissionMediumOwner,
    supplier.name                                                   AS supplier,
    supporting_infrastructure_type.code                             AS supportingInfrastructure__type,
    s.supportingInfrastructure__description,
    supporting_infrastructure_owner.name                            AS supportingInfrastructure__owner,
    s.supportingInfrastructure__spareCapacity,
    codelist_open_codeployment.code                                 AS codeployment,
    codelist_open_cableType.code                                    AS cableType,
    s.darkFibre,
    s.fibreType,
    s.fibreTypeDetails__fibreSubtype,
    s.fibreTypeDetails__description,
    s.fibreCount,
    s.fibreLength,
    s.capacity,
    s.capacityDetails__description,
    networks.name                                                   AS network,
    span_network_providers.networkProviders,
    span_transmission_medium.transmissionMedium,
    span_deployment.deployment,
    span_technologies.technologies,
    span_wayleaves.wayleave_grantor,
    span_wayleaves.wayleave_term,
    span_wayleaves.wayleave_cost,
    span_countries.countries

FROM spans s
LEFT JOIN phases                                    ON s.phase                          = phases.id
LEFT JOIN nodes                         start_node  ON s."start"                        = start_node.id
LEFT JOIN nodes                         end_node    ON s."end"                          = end_node.id
LEFT JOIN organisations transmission_medium_owner   ON s.transmissionMediumOwner        = transmission_medium_owner.id
LEFT JOIN organisations                 supplier    ON s.supplier                       = supplier.id
LEFT JOIN codelist_open_spanSupportingInfrastructure supporting_infrastructure_type
                                                    ON s.supportingInfrastructure__type = supporting_infrastructure_type.id
LEFT JOIN organisations supporting_infrastructure_owner
                                                    ON s.supportingInfrastructure__owner = supporting_infrastructure_owner.id
LEFT JOIN codelist_open_codeployment                ON s.codeployment                  = codelist_open_codeployment.id
LEFT JOIN codelist_open_cableType                   ON s.cableType                     = codelist_open_cableType.id
LEFT JOIN networks                                  ON s.network_id                    = networks.id
LEFT JOIN span_network_providers                    ON s.id = span_network_providers.base_id
LEFT JOIN span_transmission_medium                  ON s.id = span_transmission_medium.base_id
LEFT JOIN span_deployment                           ON s.id = span_deployment.base_id
LEFT JOIN span_technologies                         ON s.id = span_technologies.base_id
LEFT JOIN span_wayleaves                            ON s.id = span_wayleaves.base_id
LEFT JOIN span_countries                            ON s.id = span_countries.base_id;
