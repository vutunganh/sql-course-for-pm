-- Instructor solutions, Week 6. Fictional data; SQLite.
-- Each marked block is one standalone query.

-- BEGIN W06E01
-- Verify the bridge grain
SELECT project_id,market_id,COUNT(*) AS row_count
FROM project_markets
GROUP BY project_id,market_id
HAVING COUNT(*)>1;
-- END W06E01

-- BEGIN W06E02
-- Pre-join audit
SELECT (
    SELECT COUNT(*)
    FROM projects) AS project_count,(
    SELECT COUNT(*)
    FROM invoices) AS invoice_count,(
    SELECT COUNT(*)
    FROM survey_waves) AS wave_count,(
    SELECT COUNT(*)
    FROM project_markets) AS assignment_count;
-- END W06E02

-- BEGIN W06E03
-- Active overdue rate by account
SELECT client_id,COUNT(*) AS active_projects,SUM(CASE WHEN planned_end_date<'2025-07-01' THEN 1 ELSE 0 END) AS overdue_projects,ROUND(100.0*SUM(CASE WHEN planned_end_date<'2025-07-01' THEN 1 ELSE 0 END)/COUNT(*),1) AS overdue_pct
FROM projects
WHERE status='active'
GROUP BY client_id;
-- END W06E03

-- BEGIN W06E04
-- Closed-wave attainment
SELECT project_id,SUM(completes_target) AS target_completes,SUM(completes_actual) AS actual_completes,ROUND(100.0*SUM(completes_actual)/SUM(completes_target),1) AS attainment_pct
FROM survey_waves
WHERE close_date IS NOT NULL
GROUP BY project_id;
-- END W06E04

-- BEGIN W06E05
-- Market delivery participation
SELECT m.market_name,COUNT(DISTINCT CASE WHEN p.status='completed' THEN p.project_id END) AS completed_projects,COUNT(DISTINCT CASE WHEN p.status='completed' AND p.actual_end_date>p.planned_end_date THEN p.project_id END) AS late_projects
FROM markets m
LEFT JOIN project_markets pm ON pm.market_id=m.market_id
LEFT JOIN projects p ON p.project_id=pm.project_id
GROUP BY m.market_id,m.market_name;
-- END W06E05

-- BEGIN W06E06
-- Unpaid balance ageing
WITH aged AS (
    SELECT amount,CASE WHEN julianday('2025-07-01')-julianday(invoice_date)<=30 THEN '0-30' WHEN julianday('2025-07-01')-julianday(invoice_date)<=60 THEN '31-60' ELSE '61+' END AS age_band
    FROM invoices
    WHERE paid_flag=0)
SELECT age_band,COUNT(*) AS invoice_count,SUM(amount) AS unpaid_eur
FROM aged
GROUP BY age_band;
-- END W06E06

-- BEGIN W06E07
-- Sector budgets and billing
WITH billed AS (
    SELECT project_id,SUM(amount) AS eur
    FROM invoices
    GROUP BY project_id)
SELECT c.sector,COALESCE(SUM(p.budget),0) AS total_budget,COALESCE(SUM(b.eur),0) AS invoiced_eur
FROM clients c
LEFT JOIN projects p ON p.client_id=c.client_id
LEFT JOIN billed b ON b.project_id=p.project_id
GROUP BY c.sector;
-- END W06E07

-- BEGIN W06E08
-- June revenue concentration
WITH june AS (
    SELECT p.client_id,SUM(i.amount) AS june_eur
    FROM projects p
    JOIN invoices i ON i.project_id=p.project_id
    WHERE i.invoice_date>='2025-06-01' AND i.invoice_date<'2025-07-01'
    GROUP BY p.client_id)
SELECT client_id,june_eur,ROUND(100.0*june_eur/SUM(june_eur) OVER (),1) AS share_pct,RANK() OVER (
    ORDER BY june_eur DESC) AS revenue_rank
FROM june;
-- END W06E08

-- BEGIN W06E09
-- Briefing table: June commercial health
SELECT c.client_id,c.client_name,SUM(CASE WHEN i.invoice_date>='2025-06-01' AND i.invoice_date<'2025-07-01' THEN i.amount ELSE 0 END) AS june_invoiced_eur,SUM(CASE WHEN i.invoice_date<'2025-07-01' AND i.paid_flag=0 THEN i.amount ELSE 0 END) AS unpaid_eur
FROM clients c
LEFT JOIN projects p ON p.client_id=c.client_id
LEFT JOIN invoices i ON i.project_id=p.project_id
GROUP BY c.client_id,c.client_name;
-- END W06E09

-- BEGIN W06E10
-- Briefing table: June delivery health
WITH june AS (
    SELECT client_id,COUNT(*) AS n,SUM(CASE WHEN actual_end_date>planned_end_date THEN 1 ELSE 0 END) AS late
    FROM projects
    WHERE status='completed' AND actual_end_date>='2025-06-01' AND actual_end_date<'2025-07-01'
    GROUP BY client_id)
SELECT c.client_id,COALESCE(j.n,0) AS completed_projects,COALESCE(j.late,0) AS late_projects,ROUND(100.0*j.late/NULLIF(j.n,0),1) AS late_pct
FROM clients c
LEFT JOIN june j ON j.client_id=c.client_id;
-- END W06E10

