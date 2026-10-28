-- Instructor solutions, Week 1. Fictional data; SQLite.
-- Each marked block is one standalone query.

-- BEGIN W01E01
-- Meet the clients
SELECT client_id, client_name, sector
FROM clients
ORDER BY client_id
LIMIT 5;
-- END W01E01

-- BEGIN W01E02
-- Project grain
SELECT project_id, client_id, status, budget
FROM projects
ORDER BY project_id
LIMIT 10;
-- END W01E02

-- BEGIN W01E03
-- Market directory
SELECT market_id, market_name, region
FROM markets
ORDER BY market_id;
-- END W01E03

-- BEGIN W01E04
-- Active portfolio
SELECT project_id, budget
FROM projects
WHERE status = 'active' AND budget >= 50000;
-- END W01E04

-- BEGIN W01E05
-- Selected project types
SELECT project_id, project_type, budget
FROM projects
WHERE project_type IN ('Brand tracking','Concept test') AND budget BETWEEN 20000 AND 60000;
-- END W01E05

-- BEGIN W01E06
-- Missing completion dates
SELECT project_id, status
FROM projects
WHERE actual_end_date IS NULL;
-- END W01E06

-- BEGIN W01E07
-- Prioritise large projects
SELECT project_id, budget
FROM projects
WHERE status='active'
ORDER BY budget DESC, project_id ASC;
-- END W01E07

-- BEGIN W01E08
-- Research menu
SELECT DISTINCT project_type
FROM projects
ORDER BY project_type;
-- END W01E08

-- BEGIN W01E09
-- Overdue active work
SELECT project_id, planned_end_date, budget
FROM projects
WHERE status='active' AND planned_end_date < '2025-07-01'
ORDER BY planned_end_date, project_id;
-- END W01E09

-- BEGIN W01E10
-- Late completed work
SELECT project_id, planned_end_date, actual_end_date
FROM projects
WHERE status='completed' AND actual_end_date > planned_end_date;
-- END W01E10

