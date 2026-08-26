SELECT
    nodes.*,
    GROUP_CONCAT (organisations.name, ', ') AS networkProvider_names
FROM
    nodes
    LEFT JOIN relation_nodes_networkProviders r ON nodes.id = r.base_id
    LEFT JOIN organisations ON r.related_id = organisations.id
GROUP BY
    nodes.id