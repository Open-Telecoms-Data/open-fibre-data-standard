SELECT
    nodes.*,
    phases.name AS phase_name
FROM
    nodes
    LEFT JOIN phases ON nodes.phase = phases.id