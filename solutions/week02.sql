-- Instructor solutions, Week 2. Fictional data; SQLite.
-- Each marked block is one standalone query.

-- BEGIN W02E01
-- Portfolio totals
SELECT COUNT(*) AS project_count, SUM(budget) AS total_budget, ROUND(AVG(budget),2) AS average_budget, MIN(budget) AS min_budget, MAX(budget) AS max_budget
FROM projects;
-- END W02E01

-- BEGIN W02E02
-- Recorded completion dates
SELECT COUNT(*) AS project_count, COUNT(actual_end_date) AS completed_date_count
FROM projects;
-- END W02E02

-- BEGIN W02E03
-- Unpaid invoice summary
SELECT COUNT(*) AS invoice_count, SUM(amount) AS unpaid_eur, ROUND(AVG(amount),2) AS average_unpaid_eur
FROM invoices
WHERE paid_flag=0;
-- END W02E03

-- BEGIN W02E04
-- Projects by account
SELECT client_id, COUNT(*) AS project_count, SUM(budget) AS total_budget
FROM projects
GROUP BY client_id;
-- END W02E04

-- BEGIN W02E05
-- Delivery status summary
SELECT status, COUNT(*) AS project_count
FROM projects
GROUP BY status;
-- END W02E05

-- BEGIN W02E06
-- Wave workload
SELECT project_id, SUM(completes_target) AS target_completes, SUM(completes_actual) AS actual_completes
FROM survey_waves
GROUP BY project_id;
-- END W02E06

-- BEGIN W02E07
-- Large active accounts
SELECT client_id, SUM(budget) AS active_budget
FROM projects
WHERE status='active'
GROUP BY client_id
HAVING SUM(budget)>100000;
-- END W02E07

-- BEGIN W02E08
-- Repeated shortfalls
SELECT project_id, COUNT(*) AS below_target_waves
FROM survey_waves
WHERE close_date IS NOT NULL AND completes_actual<completes_target
GROUP BY project_id
HAVING COUNT(*)>=2;
-- END W02E08

-- BEGIN W02E09
-- Budget bands
SELECT project_id, CASE WHEN budget<30000 THEN 'Small' WHEN budget<70000 THEN 'Medium' ELSE 'Large' END AS budget_band
FROM projects;
-- END W02E09

-- BEGIN W02E10
-- Status dashboard
SELECT status, COUNT(*) AS project_count, SUM(budget) AS total_budget, SUM(CASE WHEN budget>=70000 THEN 1 ELSE 0 END) AS large_project_count
FROM projects
GROUP BY status;
-- END W02E10

