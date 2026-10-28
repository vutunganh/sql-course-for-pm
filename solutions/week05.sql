-- Instructor solutions, Week 5. Fictional data; SQLite.
-- Each marked block is one standalone query.

-- BEGIN W05E01
-- Two biggest projects per account
WITH ranked AS (
    SELECT client_id,project_id,budget,ROW_NUMBER() OVER (PARTITION BY client_id
        ORDER BY budget DESC,project_id) AS position
    FROM projects)
SELECT client_id,project_id,budget,position
FROM ranked
WHERE position<=2;
-- END W05E01

-- BEGIN W05E02
-- Tied budget rankings
SELECT project_type,project_id,budget,RANK() OVER (PARTITION BY project_type
    ORDER BY budget DESC) AS budget_rank
FROM projects;
-- END W05E02

-- BEGIN W05E03
-- Latest survey wave
WITH ranked AS (
    SELECT project_id,wave_number,completes_actual,ROW_NUMBER() OVER (PARTITION BY project_id
        ORDER BY wave_number DESC) AS position
    FROM survey_waves)
SELECT project_id,wave_number,completes_actual
FROM ranked
WHERE position=1;
-- END W05E03

-- BEGIN W05E04
-- Portfolio month-on-month
WITH monthly AS (
    SELECT strftime('%Y-%m',invoice_date) AS month,SUM(amount) AS invoiced_eur
    FROM invoices
    GROUP BY month)
SELECT month,invoiced_eur,invoiced_eur-LAG(invoiced_eur) OVER (
    ORDER BY month) AS change_eur
FROM monthly
ORDER BY month;
-- END W05E04

-- BEGIN W05E05
-- Wave-to-wave change
SELECT project_id,wave_number,completes_actual,completes_actual-LAG(completes_actual) OVER (PARTITION BY project_id
    ORDER BY wave_number) AS change_completes
FROM survey_waves;
-- END W05E05

-- BEGIN W05E06
-- Previous observed month per client
WITH monthly AS (
    SELECT p.client_id,strftime('%Y-%m',i.invoice_date) AS month,SUM(i.amount) AS invoiced_eur
    FROM projects p
    JOIN invoices i ON i.project_id=p.project_id
    GROUP BY p.client_id,month)
SELECT client_id,month,invoiced_eur,LAG(invoiced_eur) OVER (PARTITION BY client_id
    ORDER BY month) AS previous_eur
FROM monthly;
-- END W05E06

-- BEGIN W05E07
-- Cumulative invoicing
WITH monthly AS (
    SELECT strftime('%Y-%m',invoice_date) AS month,SUM(amount) AS invoiced_eur
    FROM invoices
    GROUP BY month)
SELECT month,invoiced_eur,SUM(invoiced_eur) OVER (
    ORDER BY month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_eur
FROM monthly
ORDER BY month;
-- END W05E07

-- BEGIN W05E08
-- Client revenue share
WITH revenue AS (
    SELECT p.client_id,SUM(i.amount) AS invoiced_eur
    FROM projects p
    JOIN invoices i ON i.project_id=p.project_id
    GROUP BY p.client_id)
SELECT client_id,invoiced_eur,ROUND(100.0*invoiced_eur/SUM(invoiced_eur) OVER (),2) AS share_pct
FROM revenue;
-- END W05E08

-- BEGIN W05E09
-- May to June account movement
WITH monthly AS (
    SELECT c.client_id,SUM(CASE WHEN i.invoice_date>='2025-05-01' AND i.invoice_date<'2025-06-01' THEN i.amount ELSE 0 END) AS may_eur,SUM(CASE WHEN i.invoice_date>='2025-06-01' AND i.invoice_date<'2025-07-01' THEN i.amount ELSE 0 END) AS june_eur
    FROM clients c
    LEFT JOIN projects p ON p.client_id=c.client_id
    LEFT JOIN invoices i ON i.project_id=p.project_id
    GROUP BY c.client_id)
SELECT client_id,may_eur,june_eur,june_eur-may_eur AS change_eur,CASE WHEN june_eur>may_eur THEN 'growth' WHEN june_eur<may_eur THEN 'decline' ELSE 'flat' END AS movement
FROM monthly;
-- END W05E09

-- BEGIN W05E10
-- Three largest account declines
WITH change AS (
    SELECT c.client_id,c.client_name,SUM(CASE WHEN i.invoice_date>='2025-06-01' AND i.invoice_date<'2025-07-01' THEN i.amount ELSE 0 END)-SUM(CASE WHEN i.invoice_date>='2025-05-01' AND i.invoice_date<'2025-06-01' THEN i.amount ELSE 0 END) AS change_eur
    FROM clients c
    LEFT JOIN projects p ON p.client_id=c.client_id
    LEFT JOIN invoices i ON i.project_id=p.project_id
    GROUP BY c.client_id,c.client_name)
SELECT client_id,client_name,change_eur
FROM change
WHERE change_eur<0
ORDER BY change_eur,client_id
LIMIT 3;
-- END W05E10

