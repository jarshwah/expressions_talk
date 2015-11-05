-- Add Team (Expressions)

SELECT
    "cdr_callrecord"."id",
    ..
    "cdr_callrecord"."start_time",
    COALESCE(
        "cdr_team"."name",
        'No Team') AS "team"
FROM "cdr_callrecord"
INNER JOIN "cdr_agent" ON ..
LEFT OUTER JOIN "cdr_team" ON ..

-- Add Team (Extra)
SELECT
    COALESCE(
        cdr_team.name,
        'No Team') AS "team",
    "cdr_callrecord"."id",
    "cdr_callrecord"."agent_id",
    ..
    "cdr_callrecord"."start_time",
    "cdr_agent"."name",
    ..
    "cdr_team"."name"
    ..
FROM "cdr_callrecord"
INNER JOIN "cdr_agent" ON ..
LEFT OUTER JOIN "cdr_team" ON ..

-- Team AHT

SELECT
    COALESCE("cdr_team"."name", 'No Team') AS "team",
    AVG(
        "cdr_callrecord"."talk_time" +
        "cdr_callrecord"."hold_time" +
        "cdr_callrecord"."wrap_time"
    ) AS "aht"
FROM    "cdr_callrecord"
INNER JOIN   "cdr_agent"
ON ( "cdr_callrecord"."agent_id" = "cdr_agent"."id" )
LEFT OUTER JOIN "cdr_team"
ON ( "cdr_agent"."team_id" = "cdr_team"."id" )
GROUP BY
    COALESCE("cdr_team"."name", 'No Team')
ORDER BY "team" ASC

-- Date based aggregate

SELECT
    DATE("cdr_callrecord"."start_time")
        AS "start_date",
    COUNT("cdr_callrecord"."id")
        AS "call_count"
FROM "cdr_callrecord"
GROUP BY
    DATE("cdr_callrecord"."start_time")

-- Conditional Aggregation
SELECT
    "cdr_agent"."id",
    "cdr_agent"."name",
    "cdr_agent"."team_id",
    COUNT(
        CASE WHEN "cdr_callrecord"."start_time"
        BETWEEN 2014-01-01 ..
        AND 2014-12-31.. THEN 1 ELSE NULL END)
        AS "count_2014",
    COUNT(
        CASE WHEN "cdr_callrecord"."start_time"
        BETWEEN 2015-01-01 ..
        AND 2015-12-31 .. THEN 1 ELSE NULL END)
        AS "count_2015"
FROM "cdr_agent"
LEFT OUTER JOIN "cdr_callrecord" ON ..
GROUP BY
    "cdr_agent"."id",
    "cdr_agent"."name",
    "cdr_agent"."team_id"

-- relabeled example

SELECT
    "cdr_callrecord"."id",
    "cdr_callrecord"."agent_id",
    "cdr_callrecord"."talk_time",
    "cdr_callrecord"."hold_time",
    "cdr_callrecord"."wrap_time",
    "cdr_callrecord"."start_time"
FROM "cdr_callrecord"
WHERE
    "cdr_callrecord"."talk_time" >
    "cdr_callrecord"."hold_time"
AND "cdr_callrecord"."id" IN (
    SELECT U0."id"
    FROM "cdr_callrecord" U0
    WHERE U0."wrap_time" > U0."hold_time"
)

