WITH -- See end of file for comments (the ogr2ogr SQLite dialect does not support files that begin with a comment)
    networkProviders as (
        SELECT
            "spans/0/id",
            GROUP_CONCAT ("spans/0/networkProviders/0/name", ';') AS networkProviders
        FROM
            "spans_networkProviders.csv"."spans_networkProviders"
        GROUP BY
            "spans/0/id"
    )
SELECT
    ST_GeomFromText (s."spans/0/route") AS geometry,
    networks."name" AS network,
    s."spans/0/id" AS identifier,
    s."spans/0/name" AS name,
    s."spans/0/phase/name" AS phase,
    s."spans/0/status" AS status,
    s."spans/0/readyForServiceDate" AS readyForServiceDate,
    start_node."nodes/0/name" || ' (' || s."spans/0/start" || ')' AS start,
    end_node."nodes/0/name" || ' (' || s."spans/0/end" || ')' AS end,
    s."spans/0/directed" AS directed,
    s."spans/0/transmissionMediumOwner/name" AS transmissionMediumOwner,
    s."spans/0/supplier/name" AS supplier,
    s."spans/0/supportingInfrastructure/type" AS supportingInfrastructure__type,
    s."spans/0/supportingInfrastructure/description" AS supportingInfrastructure__description,
    s."spans/0/supportingInfrastructure/owner/name" AS supportingInfrastructure__owner,
    s."spans/0/supportingInfrastructure/spareCapacity" AS supportingInfrastructure__spareCapacity,
    s."spans/0/codeployment" AS codeployment,
    s."spans/0/cableType" AS cableType,
    s."spans/0/darkFibre" AS darkFibre,
    s."spans/0/fibreType" AS fibreType,
    s."spans/0/fibreTypeDetails/fibreSubtype" AS fibreTypeDetails__fibreSubtype,
    s."spans/0/fibreTypeDetails/description" AS fibreTypeDetails__description,
    s."spans/0/fibreCount" AS fibreCount,
    s."spans/0/fibreLength" AS fibreLength,
    s."spans/0/capacity" AS capacity,
    s."spans/0/capacityDetails/description" AS capacityDetails__description,
    networkProviders.networkProviders AS networkProviders,
    s."spans/0/transmissionMedium" AS transmissionMedium,
    s."spans/0/deployment" AS deployment,
    s."spans/0/technologies" AS technologies,
    w."wayleaves/0/grantor/name" AS wayleave_grantor,
    CASE
        WHEN w."wayleaves/0/term/indefinite" = 'True' THEN 'indefinite'
        ELSE w."wayleaves/0/term/years" || ' years'
    END AS wayleave_term,
    w."wayleaves/0/cost/perMetre/amount" || ' ' || w."wayleaves/0/cost/perMetre/currency" || ' per metre (' || CASE
        WHEN w."wayleaves/0/cost/recurring" = 'True' THEN 'annual'
        ELSE 'one off'
    END || ')' AS wayleave_cost,
    s."spans/0/countries" AS countries
FROM
    "spans.csv".spans s
    LEFT JOIN "networks.csv".networks networks ON s."id" = networks."id"
    LEFT JOIN networkProviders ON s."spans/0/id" = networkProviders."spans/0/id"
    LEFT JOIN "nodes.csv".nodes start_node ON s."spans/0/start" = start_node."nodes/0/id"
    LEFT JOIN "nodes.csv".nodes end_node ON s."spans/0/end" = end_node."nodes/0/id"
    LEFT JOIN "wayleaves.csv".wayleaves w ON s."spans/0/wayleaves" = w."wayleaves/0/id";

-- Dereference the spans table in an OFDS CSV data.
-- Use this script to export spans in GeoJSON format: https://standard.ofds.info/en/latest/guidance/use/geojson-prebuilt/
-- OFDS CSV format reference documentation: https://standard.ofds.info/en/latest/reference/data_formats/csv/
--
-- Deferencing method:
-- - Replaces identifier references with their human-readable labels:
--   - organisation identifiers → organisation name
--   - network identifiers → network name
--   - wayleave FKs → wayleave grantor, term, and cost
-- - Aggregates many-to-many relations (networkProviders)
-- as semicolon-separated strings.