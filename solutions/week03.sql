-- Instructor solutions, Week 3. Fictional data; SQLite.
-- Each marked block is one standalone query.

-- BEGIN W03E01
-- Account names
SELECT p.project_id, c.client_name, p.status
FROM projects p
JOIN clients c ON c.client_id=p.client_id;
-- END W03E01

-- BEGIN W03E02
-- Sector portfolio
SELECT c.sector, COUNT(*) AS project_count, SUM(p.budget) AS total_budget
FROM projects p
JOIN clients c ON c.client_id=p.client_id
GROUP BY c.sector;
-- END W03E02

-- BEGIN W03E03
-- Market participation
SELECT pm.project_id, m.market_name
FROM project_markets pm
JOIN markets m ON m.market_id=pm.market_id;
-- END W03E03

-- BEGIN W03E04
-- Accounts without projects
SELECT c.client_id, c.client_name
FROM clients c
LEFT JOIN projects p ON p.client_id=c.client_id
WHERE p.project_id IS NULL;
-- END W03E04

-- BEGIN W03E05
-- Invoice coverage
SELECT p.project_id, COUNT(i.invoice_id) AS invoice_count
FROM projects p
LEFT JOIN invoices i ON i.project_id=p.project_id
GROUP BY p.project_id;
-- END W03E05

-- BEGIN W03E06
-- Unassigned markets
SELECT p.project_id, p.status
FROM projects p
LEFT JOIN project_markets pm ON pm.project_id=p.project_id
WHERE pm.project_id IS NULL;
-- END W03E06

-- BEGIN W03E07
-- Client invoice totals
SELECT c.client_id, c.client_name, COALESCE(SUM(i.amount),0) AS invoiced_eur
FROM clients c
LEFT JOIN projects p ON p.client_id=c.client_id
LEFT JOIN invoices i ON i.project_id=p.project_id
GROUP BY c.client_id,c.client_name;
-- END W03E07

-- BEGIN W03E08
-- Projects participating by market
SELECT m.market_name, COUNT(pm.project_id) AS project_count
FROM markets m
LEFT JOIN project_markets pm ON pm.market_id=m.market_id
GROUP BY m.market_id,m.market_name;
-- END W03E08

-- BEGIN W03E09
-- Repair multiplied totals
WITH revenue AS (
    SELECT project_id,SUM(amount) AS eur
    FROM invoices
    GROUP BY project_id), coverage AS (
    SELECT project_id,COUNT(*) AS markets
    FROM project_markets
    GROUP BY project_id)
SELECT p.project_id,COALESCE(r.eur,0) AS invoiced_eur,COALESCE(c.markets,0) AS market_count
FROM projects p
LEFT JOIN revenue r ON r.project_id=p.project_id
LEFT JOIN coverage c ON c.project_id=p.project_id;
-- END W03E09

-- BEGIN W03E10
-- Client and market management view
WITH portfolio AS (
    SELECT client_id,COUNT(*) AS n,SUM(budget) AS budget
    FROM projects
    GROUP BY client_id), revenue AS (
    SELECT p.client_id,SUM(i.amount) AS eur
    FROM projects p
    JOIN invoices i ON i.project_id=p.project_id
    GROUP BY p.client_id), coverage AS (
    SELECT p.client_id,COUNT(DISTINCT pm.market_id) AS n
    FROM projects p
    JOIN project_markets pm ON pm.project_id=p.project_id
    GROUP BY p.client_id)
SELECT c.client_id,COALESCE(p.n,0) AS project_count,COALESCE(p.budget,0) AS total_budget,COALESCE(r.eur,0) AS invoiced_eur,COALESCE(m.n,0) AS market_count
FROM clients c
LEFT JOIN portfolio p ON p.client_id=c.client_id
LEFT JOIN revenue r ON r.client_id=c.client_id
LEFT JOIN coverage m ON m.client_id=c.client_id;
-- END W03E10

