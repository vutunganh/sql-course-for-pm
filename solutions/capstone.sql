-- Instructor supplement: required query 3, June-closed waves by client.
-- Queries 1, 2 and 4 can use W06E09, W06E10 and W06E06 respectively.
-- Closed-wave performance is not restricted to completed projects.
WITH june_wave_totals AS (
    SELECT p.client_id,
           COUNT(*) AS closed_waves,
           SUM(w.completes_target) AS target_completes,
           SUM(w.completes_actual) AS actual_completes
    FROM survey_waves w
    JOIN projects p ON p.project_id = w.project_id
    WHERE w.close_date >= '2025-06-01'
      AND w.close_date < '2025-07-01'
    GROUP BY p.client_id
)
SELECT c.client_id,
       c.client_name,
       COALESCE(j.closed_waves, 0) AS closed_waves,
       COALESCE(j.target_completes, 0) AS target_completes,
       COALESCE(j.actual_completes, 0) AS actual_completes,
       ROUND(100.0 * j.actual_completes / NULLIF(j.target_completes, 0), 1) AS attainment_pct
FROM clients c
LEFT JOIN june_wave_totals j ON j.client_id = c.client_id;
