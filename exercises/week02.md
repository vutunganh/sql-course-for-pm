# Week 2 exercises

Use the browser app for Run query and Check answer, or the command-line checker. All data is fictional. Reporting date: **2025-07-01**; amounts: **EUR**. Use SQLite syntax. Column aliases and their order must match the requested output. Row order matters only when explicitly requested.

## W02E01 — Portfolio totals

Session 1 · Foundation · Topic: Portfolio totals

Return one row with project count, total budget, average budget rounded to two decimals, smallest budget and largest budget.

Tables: `projects`. Output columns: `project_count`, `total_budget`, `average_budget`, `min_budget`, `max_budget`.

<details><summary>Hint 1</summary>

Aggregate functions collapse rows.

</details>

<details><summary>Hint 2</summary>

COUNT(*) counts every project.

</details>

<details><summary>Common mistake to check after trying</summary>

Budget is planned commercial value; it is not invoiced revenue.

</details>

## W02E02 — Recorded completion dates

Session 1 · Foundation · Topic: Recorded completion dates

Return total project rows and number of recorded actual end dates.

Tables: `projects`. Output columns: `project_count`, `completed_date_count`.

<details><summary>Hint 1</summary>

COUNT(column) ignores NULL.

</details>

<details><summary>Hint 2</summary>

Compare COUNT(*) and COUNT(actual_end_date).

</details>

<details><summary>Common mistake to check after trying</summary>

Counting a nullable column does not count every row.

</details>

## W02E03 — Unpaid invoice summary

Session 1 · Foundation · Topic: Unpaid invoice summary

Return one row with unpaid invoice count, total unpaid EUR and average unpaid invoice amount rounded to two decimals. Unpaid means paid_flag = 0.

Tables: `invoices`. Output columns: `invoice_count`, `unpaid_eur`, `average_unpaid_eur`.

<details><summary>Hint 1</summary>

Filter to unpaid invoices before aggregating.

</details>

<details><summary>Hint 2</summary>

Use COUNT(*), SUM(amount), and ROUND(AVG(amount),2).

</details>

<details><summary>Common mistake to check after trying</summary>

Unpaid is a balance; it is not necessarily overdue because no due date is recorded.

</details>

## W02E04 — Projects by account

Session 2 · Foundation · Topic: Projects by account

Count projects and sum budgets by client_id. Include only clients represented in projects.

Tables: `projects`. Output columns: `client_id`, `project_count`, `total_budget`.

<details><summary>Hint 1</summary>

Each group is one client.

</details>

<details><summary>Hint 2</summary>

Group by client_id.

</details>

<details><summary>Common mistake to check after trying</summary>

Selecting project_id would mix project grain with account grain.

</details>

## W02E05 — Delivery status summary

Session 2 · Foundation · Topic: Delivery status summary

Count projects by status.

Tables: `projects`. Output columns: `status`, `project_count`.

<details><summary>Hint 1</summary>

Create one group for each status value.

</details>

<details><summary>Hint 2</summary>

COUNT(*) counts rows within each group.

</details>

<details><summary>Common mistake to check after trying</summary>

Filtering to one status would omit the other groups.

</details>

## W02E06 — Wave workload

Session 2 · Foundation · Topic: Wave workload

For each project, total target completes and actual completes across all survey waves, including any open waves.

Tables: `survey_waves`. Output columns: `project_id`, `target_completes`, `actual_completes`.

<details><summary>Hint 1</summary>

A wave is not a project.

</details>

<details><summary>Hint 2</summary>

Sum both columns grouped by project_id.

</details>

<details><summary>Common mistake to check after trying</summary>

AVG(completes_actual) would describe an average wave, not total workload.

</details>

## W02E07 — Large active accounts

Session 3 · Foundation · Topic: Large active accounts

Among active projects only, find client IDs whose combined active budget exceeds EUR 100,000.

Tables: `projects`. Output columns: `client_id`, `active_budget`.

<details><summary>Hint 1</summary>

WHERE filters the input rows.

</details>

<details><summary>Hint 2</summary>

HAVING filters the grouped total.

</details>

<details><summary>Common mistake to check after trying</summary>

Filtering individual budgets above 100000 answers a different question.

</details>

## W02E08 — Repeated shortfalls

Session 3 · Foundation · Topic: Repeated shortfalls

For closed waves below target only, show projects with two or more such waves. Closed means close_date IS NOT NULL.

Tables: `survey_waves`. Output columns: `project_id`, `below_target_waves`.

<details><summary>Hint 1</summary>

First exclude open waves and waves at or above target.

</details>

<details><summary>Hint 2</summary>

Count the remaining rows per project and apply HAVING.

</details>

<details><summary>Common mistake to check after trying</summary>

A total shortfall can hide one wave that exceeded target.

</details>

## W02E09 — Budget bands

Session 4 · Foundation · Topic: Budget bands

Label every project: Small for budget <30000, Medium for budget >=30000 and <70000, Large otherwise.

Tables: `projects`. Output columns: `project_id`, `budget_band`.

<details><summary>Hint 1</summary>

CASE evaluates branches in order.

</details>

<details><summary>Hint 2</summary>

After testing <30000, the next branch only needs <70000.

</details>

<details><summary>Common mistake to check after trying</summary>

Check exact boundaries at 30000 and 70000.

</details>

## W02E10 — Status dashboard

Session 4 · Foundation · Topic: Status dashboard

For each status, show project count, total budget, and count of projects with budget at least EUR 70,000.

Tables: `projects`. Output columns: `status`, `project_count`, `total_budget`, `large_project_count`.

<details><summary>Hint 1</summary>

A conditional CASE can produce 1 or 0 for every row.

</details>

<details><summary>Hint 2</summary>

SUM the conditional values within each status.

</details>

<details><summary>Common mistake to check after trying</summary>

COUNT(CASE ... ELSE 0 END) counts zero values too.

</details>

