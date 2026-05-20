SELECT
    ST_GeomFromText (n."nodes/0/location") AS geometry,
    n.*,
    GROUP_CONCAT (o."organisations/0/website", ', ') AS networkProvider_websites
FROM
    "nodes.csv".nodes n
    LEFT JOIN "nodes_networkProviders.csv"."nodes_networkProviders" nnp ON n."nodes/0/id" = nnp."nodes/0/id"
    LEFT JOIN "organisations.csv".organisations o ON nnp."nodes/0/networkProviders/0/id" = o."organisations/0/id"
GROUP BY
    n."nodes/0/id"