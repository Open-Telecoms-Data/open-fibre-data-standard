SELECT
    ST_GeomFromText ("nodes/0/location") AS geometry,
    n.*,
    p."phases/0/description" AS phase_description
FROM
    "nodes.csv".nodes n
    LEFT JOIN "phases.csv".phases p ON n."nodes/0/phase/id" = p."phases/0/id"