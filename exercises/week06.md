# Week 6 exercises

Use the browser app for Run query and Check answer, or the command-line checker. All data is fictional. Reporting date: **2025-07-01**; amounts: **EUR**. Use SQLite syntax. Column aliases and their order must match the requested output. Row order matters only when explicitly requested.

## W06E01 — Verify the bridge grain

Session 1 · Stretch · Topic: Verify the bridge grain

Find duplicate project-market pairs, returning each repeated pair and its row count. The correct result is empty. Explain outside SQL why the primary key prevents these duplicates.

Tables: `project_markets`. Output columns: `project_id`, `market_id`, `row_count`.

<details><summary>Hint 1</summary>

Group by both parts of the key.

</details>

<details><summary>Hint 2</summary>

HAVING COUNT(*) > 1 identifies repeated pairs.

</details>

<details><summary>Common mistake to check after trying</summary>

Grouping only by project_id would mistake legitimate multiple markets for duplicate pairs.

</details>

## W06E02 — Pre-join audit

Session 1 · Stretch · Topic: Pre-join audit

Return one row with counts of projects, invoices, waves and project-market pairs before joining anything.

Tables: `projects, invoices, survey_waves, project_markets`. Output columns: `project_count`, `invoice_count`, `wave_count`, `assignment_count`.

<details><summary>Hint 1</summary>

Each count has its own grain.

</details>

<details><summary>Hint 2</summary>

Independent scalar subqueries avoid multiplying rows.

</details>

<details><summary>Common mistake to check after trying</summary>

A four-way join count does not describe any one source table.

</details>

## W06E03 — Active overdue rate by account

Session 2 · Stretch · Topic: Active overdue rate by account

For clients with active projects, return active project count, overdue active count and overdue percentage rounded to one decimal as of 2025-07-01.

Tables: `projects`. Output columns: `client_id`, `active_projects`, `overdue_projects`, `overdue_pct`.

<details><summary>Hint 1</summary>

The denominator is active projects for that client.

</details>

<details><summary>Hint 2</summary>

Overdue means planned_end_date < 2025-07-01.

</details>

<details><summary>Common mistake to check after trying</summary>

Cancelled projects and completed late deliveries are outside this metric.

</details>

## W06E04 — Closed-wave attainment

Session 2 · Stretch · Topic: Closed-wave attainment

For each project with closed waves, return total target, actual completes and weighted attainment percentage rounded to one decimal. Include only closed waves.

Tables: `survey_waves`. Output columns: `project_id`, `target_completes`, `actual_completes`, `attainment_pct`.

<details><summary>Hint 1</summary>

Weighted attainment = summed actual / summed target.

</details>

<details><summary>Hint 2</summary>

Use 100.0 and group by project.

</details>

<details><summary>Common mistake to check after trying</summary>

An average of wave percentages assigns equal weight to different-size targets.

</details>

## W06E05 — Market delivery participation

Session 2 · Stretch · Topic: Market delivery participation

For each market, count distinct completed projects participating and completed late projects participating. Markets with no completed projects should show zero.

Tables: `markets, project_markets, projects`. Output columns: `market_name`, `completed_projects`, `late_projects`.

<details><summary>Hint 1</summary>

Keep markets even when their projects are not completed.

</details>

<details><summary>Hint 2</summary>

COUNT DISTINCT CASE can count conditional project IDs.

</details>

<details><summary>Common mistake to check after trying</summary>

These participation counts overlap across markets and must not be summed into a portfolio count.

</details>

## W06E06 — Unpaid balance ageing

Session 3 · Stretch · Topic: Unpaid balance ageing

As of 2025-07-01, return unpaid invoice amounts in age bands 0-30, 31-60 and 61+ days, with invoice counts. Include only bands with invoices. Age is elapsed days since invoice_date.

Tables: `invoices`. Output columns: `age_band`, `invoice_count`, `unpaid_eur`.

<details><summary>Hint 1</summary>

Use julianday to calculate calendar age.

</details>

<details><summary>Hint 2</summary>

CASE boundaries are <=30, <=60, else 61+.

</details>

<details><summary>Common mistake to check after trying</summary>

Age since issuance does not establish overdue payment without agreed due dates.

</details>

## W06E07 — Sector budgets and billing

Session 3 · Stretch · Topic: Sector budgets and billing

Return every sector with total project budget and invoiced EUR. Ensure every project budget is counted once.

Tables: `clients, projects, invoices`. Output columns: `sector`, `total_budget`, `invoiced_eur`.

<details><summary>Hint 1</summary>

Preaggregate invoices to project grain before joining.

</details>

<details><summary>Hint 2</summary>

A LEFT JOIN retains projects with no invoices.

</details>

<details><summary>Common mistake to check after trying</summary>

SUM(DISTINCT budget) loses separate projects that happen to share a budget.

</details>

## W06E08 — June revenue concentration

Session 3 · Stretch · Topic: June revenue concentration

For clients with invoices dated in June, show June invoiced EUR, share of all June invoicing rounded to one decimal and competition rank by June EUR descending.

Tables: `projects, invoices`. Output columns: `client_id`, `june_eur`, `share_pct`, `revenue_rank`.

<details><summary>Hint 1</summary>

Use a June-only client summary as input.

</details>

<details><summary>Hint 2</summary>

Use SUM OVER () and RANK OVER (ORDER BY june_eur DESC).

</details>

<details><summary>Common mistake to check after trying</summary>

The denominator must contain June invoicing only.

</details>

## W06E09 — Briefing table: June commercial health

Session 4 · Stretch · Topic: Briefing table: June commercial health

For every client, return client name, June invoiced EUR, and total unpaid EUR across all invoice dates before 2025-07-01. Zero-fill absent values. Save this as query 1 in the capstone.

Tables: `clients, projects, invoices`. Output columns: `client_id`, `client_name`, `june_invoiced_eur`, `unpaid_eur`.

<details><summary>Hint 1</summary>

The two measures use different time windows.

</details>

<details><summary>Hint 2</summary>

Conditional sums can preserve all clients with LEFT JOINs.

</details>

<details><summary>Common mistake to check after trying</summary>

Current paid_flag is the snapshot payment state; historic month-end payment states are unavailable.

</details>

## W06E10 — Briefing table: June delivery health

Session 4 · Stretch · Topic: Briefing table: June delivery health

For every client, show June completed project count, June late completed project count and late percentage rounded to one decimal. Return NULL percentage when no projects were completed in June. Save as query 2 in the capstone.

Tables: `clients, projects`. Output columns: `client_id`, `completed_projects`, `late_projects`, `late_pct`.

<details><summary>Hint 1</summary>

Filter the completed-June cohort in a CTE or JOIN condition.

</details>

<details><summary>Hint 2</summary>

Use NULLIF(count,0) to protect an undefined rate.

</details>

<details><summary>Common mistake to check after trying</summary>

Zero late deliveries out of zero deliveries is an undefined rate, not 0% success.

</details>

