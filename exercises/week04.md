# Week 4 exercises

Use the browser app for Run query and Check answer, or the command-line checker. All data is fictional. Reporting date: **2025-07-01**; amounts: **EUR**. Use SQLite syntax. Column aliases and their order must match the requested output. Row order matters only when explicitly requested.

## W04E01 — June delivery cohort

Session 1 · Practice · Topic: June delivery cohort

List completed projects delivered during June 2025. Include June 1 and exclude July 1.

Tables: `projects`. Output columns: `project_id`, `actual_end_date`.

<details><summary>Hint 1</summary>

Use an inclusive lower bound and exclusive upper bound.

</details>

<details><summary>Hint 2</summary>

Compare actual_end_date to 2025-06-01 and 2025-07-01.

</details>

<details><summary>Common mistake to check after trying</summary>

The cohort is defined by delivery date, not start date.

</details>

## W04E02 — Monthly launches

Session 1 · Practice · Topic: Monthly launches

Count project starts by month across all projects. Return month as YYYY-MM and sort oldest first.

Tables: `projects`. Output columns: `month`, `launched_projects`.

<details><summary>Hint 1</summary>

strftime formats ISO dates in SQLite.

</details>

<details><summary>Hint 2</summary>

Group by strftime('%Y-%m',start_date).

</details>

<details><summary>Common mistake to check after trying</summary>

These are project launches; survey wave launches are a different event.

</details>

## W04E03 — Quarterly invoices

Session 1 · Practice · Topic: Quarterly invoices

Summarise invoice amounts for Q1 and Q2 2025, one row per quarter labeled 2025-Q1 or 2025-Q2, sorted by quarter.

Tables: `invoices`. Output columns: `quarter`, `invoiced_eur`.

<details><summary>Hint 1</summary>

Filter to [2025-01-01,2025-07-01).

</details>

<details><summary>Hint 2</summary>

CASE can split months before April from the rest.

</details>

<details><summary>Common mistake to check after trying</summary>

Do not use PostgreSQL DATE_TRUNC in SQLite.

</details>

## W04E04 — Find tracking work

Session 2 · Practice · Topic: Find tracking work

Find projects whose project_type contains the text tracking. Match case-insensitively.

Tables: `projects`. Output columns: `project_id`, `project_type`.

<details><summary>Hint 1</summary>

Use LIKE and wildcard characters.

</details>

<details><summary>Hint 2</summary>

LOWER(project_type) makes the intended matching explicit.

</details>

<details><summary>Common mistake to check after trying</summary>

An underscore wildcard means one character; percent means any sequence.

</details>

## W04E05 — Export client labels

Session 2 · Practice · Topic: Export client labels

Return every client ID with an uppercase client label and the label length.

Tables: `clients`. Output columns: `client_id`, `client_label`, `label_length`.

<details><summary>Hint 1</summary>

SQLite provides UPPER and LENGTH.

</details>

<details><summary>Hint 2</summary>

Apply both functions to client_name.

</details>

<details><summary>Common mistake to check after trying</summary>

LENGTH counts characters, not words.

</details>

## W04E06 — Completed duration

Session 2 · Practice · Topic: Completed duration

For each completed project, return elapsed calendar days from start to actual end as an integer. Same-day delivery would be zero days.

Tables: `projects`. Output columns: `project_id`, `duration_days`.

<details><summary>Hint 1</summary>

Subtract julianday values.

</details>

<details><summary>Hint 2</summary>

CAST the difference AS INTEGER.

</details>

<details><summary>Common mistake to check after trying</summary>

Subtracting ISO date text directly does not calculate elapsed days.

</details>

## W04E07 — Above-average budgets

Session 3 · Practice · Topic: Above-average budgets

List projects whose budget exceeds the average budget across all projects.

Tables: `projects`. Output columns: `project_id`, `budget`.

<details><summary>Hint 1</summary>

A scalar subquery can calculate a single benchmark.

</details>

<details><summary>Hint 2</summary>

Compare budget with (SELECT AVG(budget) FROM projects).

</details>

<details><summary>Common mistake to check after trying</summary>

A per-client average would change the comparison group.

</details>

## W04E08 — Account balances with a CTE

Session 3 · Practice · Topic: Account balances with a CTE

Show every client with paid EUR and unpaid EUR, using a readable invoice summary. Fill missing balances with zero.

Tables: `clients, projects, invoices`. Output columns: `client_id`, `paid_eur`, `unpaid_eur`.

<details><summary>Hint 1</summary>

Build a CTE at client grain with conditional sums.

</details>

<details><summary>Hint 2</summary>

Join it to all clients.

</details>

<details><summary>Common mistake to check after trying</summary>

Filtering paid_flag in WHERE would remove one side of the balance.

</details>

## W04E09 — Monthly delivery report

Session 4 · Practice · Topic: Monthly delivery report

By actual delivery month, show completed projects, late completions and late percentage rounded to one decimal. Sort by month. Only completed projects belong in the denominator.

Tables: `projects`. Output columns: `month`, `completed_projects`, `late_projects`, `late_pct`.

<details><summary>Hint 1</summary>

A late completion has actual_end_date > planned_end_date.

</details>

<details><summary>Hint 2</summary>

Use 100.0 to avoid integer division.

</details>

<details><summary>Common mistake to check after trying</summary>

Active overdue projects are a different metric and must not enter this denominator.

</details>

## W04E10 — June monthly summary

Session 4 · Practice · Topic: June monthly summary

Return one row: projects started in June, projects completed in June, late completions among those June completions, and invoiced EUR dated in June.

Tables: `projects, invoices`. Output columns: `launched_projects`, `completed_projects`, `late_projects`, `invoiced_eur`.

<details><summary>Hint 1</summary>

These four metrics have different date/cohort definitions.

</details>

<details><summary>Hint 2</summary>

Use independent scalar subqueries or one-row CTEs.

</details>

<details><summary>Common mistake to check after trying</summary>

Joining project and invoice rows directly can multiply delivery counts.

</details>

