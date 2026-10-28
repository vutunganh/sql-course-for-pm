# Fictional training data dictionary

Snapshot date: **2025-07-01**. All dates are ISO `YYYY-MM-DD`. All money is integer EUR. The generator uses seed 42 and can be rerun with `python3 scripts/seed.py`. The database is generated and ignored by version control. Test variations are temporary and not used for ordinary practice.

| Table | One row represents | Key | Relationships and fields |
|---|---|---|---|
| clients | One fictional client account | client_id | client_name, sector, region |
| projects | One research project | project_id | client_id → clients; project_type; start_date; planned_end_date; nullable actual_end_date; status; budget |
| markets | One country market | market_id | market_name, region |
| project_markets | One project participating in one market | (project_id, market_id) | Each ID refers to its parent table; a project may span several markets |
| invoices | One invoice issued for one project | invoice_id | project_id → projects; invoice_date; amount; paid_flag 0/1 |
| survey_waves | One numbered survey wave within a project | wave_id | project_id → projects; unique (project_id, wave_number); launch_date; nullable close_date; completes_target; completes_actual |

`project_type` values: Brand tracking, Customer experience, Concept test, Usage study. `status` values: active, completed, cancelled. Only completed projects have an actual_end_date. Status and paid_flag describe the snapshot; no status-history or payment-history table exists. Open wave counts are progress to date, not final delivery outcomes. Clients with no projects and projects with no invoices remain valid report rows when an exercise asks for all accounts/projects.

## Definitions used in the course

| Metric | Definition |
|---|---|
| Budget | Sum of projects.budget at project grain; planned value, not recognized revenue |
| Invoiced EUR | SUM(invoices.amount) for the specified invoice-date period |
| Paid / unpaid EUR | Invoice sums where paid_flag = 1 / 0 at the snapshot |
| Active overdue project | status = 'active' and planned_end_date < '2025-07-01' |
| Late completed project | status = 'completed' and actual_end_date > planned_end_date |
| Late completion percentage | 100.0 × late completed projects / completed projects in the delivery-date cohort |
| Closed wave | close_date IS NOT NULL; all recorded closures precede the snapshot |
| Weighted attainment percentage | 100.0 × SUM(completes_actual) / SUM(completes_target) for the stated closed-wave cohort |
| Below-target wave | A closed wave with completes_actual < completes_target |
| Unpaid age | Elapsed days from invoice_date to the snapshot; not contractual overdue days |
| Project duration | Elapsed days from start_date to actual_end_date; same-day duration is zero |
| June | Dates >= '2025-06-01' and < '2025-07-01', using the event date named in the question |

An undefined rate (zero denominator) should be NULL unless a question explicitly specifies another presentation. A missing financial total becomes zero only when a retained account genuinely has no matching invoices. Do not automatically turn every unknown value into zero.

## Cardinality and double counting

One client has zero or many projects; each project has one client. Each project has zero or many invoices, waves and market assignments. Each market has zero or many assignments. A direct join of 2 invoices × 3 markets × 2 waves gives 12 rows for that one project. Its invoice amounts are each repeated six times.

Reduce each independent child table to one row per required parent key **before** joining financial and operational summaries. Audit uniqueness at that key. Reconcile totals to each source table. `SUM(DISTINCT amount)` is not a repair because different real invoices can have equal amounts. Market participation counts overlap across markets; project revenue cannot be accurately assigned to a market from this schema without an additional agreed allocation rule.
