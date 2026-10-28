-- Instructor solutions, Week 4. Fictional data; SQLite.
-- Each marked block is one standalone query.

-- BEGIN W04E01
-- June delivery cohort
SELECT project_id,actual_end_date
FROM projects
WHERE status='completed' AND actual_end_date>='2025-06-01' AND actual_end_date<'2025-07-01';
-- END W04E01

-- BEGIN W04E02
-- Monthly launches
SELECT strftime('%Y-%m',start_date) AS month,COUNT(*) AS launched_projects
FROM projects
GROUP BY strftime('%Y-%m',start_date)
ORDER BY month;
-- END W04E02

-- BEGIN W04E03
-- Quarterly invoices
SELECT CASE WHEN invoice_date<'2025-04-01' THEN '2025-Q1' ELSE '2025-Q2' END AS quarter,SUM(amount) AS invoiced_eur
FROM invoices
WHERE invoice_date>='2025-01-01' AND invoice_date<'2025-07-01'
GROUP BY quarter
ORDER BY quarter;
-- END W04E03

-- BEGIN W04E04
-- Find tracking work
SELECT project_id,project_type
FROM projects
WHERE LOWER(project_type) LIKE '%tracking%';
-- END W04E04

-- BEGIN W04E05
-- Export client labels
SELECT client_id,UPPER(client_name) AS client_label,LENGTH(client_name) AS label_length
FROM clients;
-- END W04E05

-- BEGIN W04E06
-- Completed duration
SELECT project_id,CAST(julianday(actual_end_date)-julianday(start_date) AS INTEGER) AS duration_days
FROM projects
WHERE status='completed';
-- END W04E06

-- BEGIN W04E07
-- Above-average budgets
SELECT project_id,budget
FROM projects
WHERE budget>(
    SELECT AVG(budget)
    FROM projects);
-- END W04E07

-- BEGIN W04E08
-- Account balances with a CTE
WITH balances AS (
    SELECT p.client_id,SUM(CASE WHEN i.paid_flag=1 THEN i.amount ELSE 0 END) AS paid,SUM(CASE WHEN i.paid_flag=0 THEN i.amount ELSE 0 END) AS unpaid
    FROM projects p
    JOIN invoices i ON i.project_id=p.project_id
    GROUP BY p.client_id)
SELECT c.client_id,COALESCE(b.paid,0) AS paid_eur,COALESCE(b.unpaid,0) AS unpaid_eur
FROM clients c
LEFT JOIN balances b ON b.client_id=c.client_id;
-- END W04E08

-- BEGIN W04E09
-- Monthly delivery report
SELECT strftime('%Y-%m',actual_end_date) AS month,COUNT(*) AS completed_projects,SUM(CASE WHEN actual_end_date>planned_end_date THEN 1 ELSE 0 END) AS late_projects,ROUND(100.0*SUM(CASE WHEN actual_end_date>planned_end_date THEN 1 ELSE 0 END)/COUNT(*),1) AS late_pct
FROM projects
WHERE status='completed'
GROUP BY month
ORDER BY month;
-- END W04E09

-- BEGIN W04E10
-- June monthly summary
SELECT (
    SELECT COUNT(*)
    FROM projects
    WHERE start_date>='2025-06-01' AND start_date<'2025-07-01') AS launched_projects,(
    SELECT COUNT(*)
    FROM projects
    WHERE status='completed' AND actual_end_date>='2025-06-01' AND actual_end_date<'2025-07-01') AS completed_projects,(
    SELECT COUNT(*)
    FROM projects
    WHERE status='completed' AND actual_end_date>planned_end_date AND actual_end_date>='2025-06-01' AND actual_end_date<'2025-07-01') AS late_projects,(
    SELECT COALESCE(SUM(amount),0)
    FROM invoices
    WHERE invoice_date>='2025-06-01' AND invoice_date<'2025-07-01') AS invoiced_eur;
-- END W04E10

