# Week 1 exercises

Use the browser app for Run query and Check answer, or the command-line checker. All data is fictional. Reporting date: **2025-07-01**; amounts: **EUR**. Use SQLite syntax. Column aliases and their order must match the requested output. Row order matters only when explicitly requested.

## W01E01 — Meet the clients

Session 1 · Foundation · Topic: Meet the clients

Preview the first five clients by client_id, smallest first.

Tables: `clients`. Output columns: `client_id`, `client_name`, `sector`.

<details><summary>Hint 1</summary>

Choose only the three requested columns.

</details>

<details><summary>Hint 2</summary>

Sort before taking five rows.

</details>

<details><summary>Common mistake to check after trying</summary>

LIMIT without ORDER BY does not define which five rows you get.

</details>

## W01E02 — Project grain

Session 1 · Foundation · Topic: Project grain

Show the first ten projects by project_id. Each row represents one project, not one client.

Tables: `projects`. Output columns: `project_id`, `client_id`, `status`, `budget`.

<details><summary>Hint 1</summary>

The client_id may repeat across projects.

</details>

<details><summary>Hint 2</summary>

Use ORDER BY and LIMIT.

</details>

<details><summary>Common mistake to check after trying</summary>

Repeated client IDs do not mean repeated project rows.

</details>

## W01E03 — Market directory

Session 1 · Foundation · Topic: Market directory

Show all markets with their IDs and regions, smallest market_id first.

Tables: `markets`. Output columns: `market_id`, `market_name`, `region`.

<details><summary>Hint 1</summary>

A market is a country in this training dataset.

</details>

<details><summary>Hint 2</summary>

Select three columns and order by the key.

</details>

<details><summary>Common mistake to check after trying</summary>

A region contains multiple markets; region is not the key.

</details>

## W01E04 — Active portfolio

Session 2 · Foundation · Topic: Active portfolio

List active projects with budgets of at least EUR 50,000. No sorting required.

Tables: `projects`. Output columns: `project_id`, `budget`.

<details><summary>Hint 1</summary>

Both conditions must be true.

</details>

<details><summary>Hint 2</summary>

Combine filters with AND.

</details>

<details><summary>Common mistake to check after trying</summary>

Using OR includes projects that satisfy only one condition.

</details>

## W01E05 — Selected project types

Session 2 · Foundation · Topic: Selected project types

Find Brand tracking or Concept test projects with budgets from EUR 20,000 through EUR 60,000 inclusive.

Tables: `projects`. Output columns: `project_id`, `project_type`, `budget`.

<details><summary>Hint 1</summary>

IN can match either project type.

</details>

<details><summary>Hint 2</summary>

BETWEEN includes both endpoints.

</details>

<details><summary>Common mistake to check after trying</summary>

AND must apply to both project types; parentheses matter with OR.

</details>

## W01E06 — Missing completion dates

Session 2 · Foundation · Topic: Missing completion dates

List every project whose actual_end_date is missing, including cancellations.

Tables: `projects`. Output columns: `project_id`, `status`.

<details><summary>Hint 1</summary>

NULL means no recorded value.

</details>

<details><summary>Hint 2</summary>

Use IS NULL.

</details>

<details><summary>Common mistake to check after trying</summary>

actual_end_date = NULL never evaluates to true.

</details>

## W01E07 — Prioritise large projects

Session 3 · Foundation · Topic: Prioritise large projects

List active projects by budget descending, with project_id ascending to break ties.

Tables: `projects`. Output columns: `project_id`, `budget`.

<details><summary>Hint 1</summary>

Filter before ordering.

</details>

<details><summary>Hint 2</summary>

Each sort key can have its own direction.

</details>

<details><summary>Common mistake to check after trying</summary>

A stable tie-breaker makes the priority list reproducible.

</details>

## W01E08 — Research menu

Session 3 · Foundation · Topic: Research menu

List the unique project types in alphabetical order.

Tables: `projects`. Output columns: `project_type`.

<details><summary>Hint 1</summary>

One output row per type.

</details>

<details><summary>Hint 2</summary>

Use DISTINCT.

</details>

<details><summary>Common mistake to check after trying</summary>

DISTINCT on several columns deduplicates their combination.

</details>

## W01E09 — Overdue active work

Session 4 · Foundation · Topic: Overdue active work

As of 2025-07-01, list active projects whose planned end date is strictly before that date. Sort by planned_end_date then project_id, ascending.

Tables: `projects`. Output columns: `project_id`, `planned_end_date`, `budget`.

<details><summary>Hint 1</summary>

Overdue here means still active and past the planned end date.

</details>

<details><summary>Hint 2</summary>

ISO date text can be compared with a quoted ISO date.

</details>

<details><summary>Common mistake to check after trying</summary>

A cancelled project is not active overdue work.

</details>

## W01E10 — Late completed work

Session 4 · Foundation · Topic: Late completed work

List completed projects delivered after their planned end date. Exactly on-time delivery is not late.

Tables: `projects`. Output columns: `project_id`, `planned_end_date`, `actual_end_date`.

<details><summary>Hint 1</summary>

Compare two columns.

</details>

<details><summary>Hint 2</summary>

Require actual_end_date > planned_end_date.

</details>

<details><summary>Common mistake to check after trying</summary>

Missing actual dates cannot establish a completed delivery delay.

</details>

