# Week 5 exercises

Use the browser app for Run query and Check answer, or the command-line checker. All data is fictional. Reporting date: **2025-07-01**; amounts: **EUR**. Use SQLite syntax. Column aliases and their order must match the requested output. Row order matters only when explicitly requested.

## W05E01 — Two biggest projects per account

Session 1 · Stretch · Topic: Two biggest projects per account

Return up to two projects per client by budget descending. Break ties by project_id ascending. Include position numbered 1 or 2.

Tables: `projects`. Output columns: `client_id`, `project_id`, `budget`, `position`.

<details><summary>Hint 1</summary>

Use ROW_NUMBER partitioned by client_id.

</details>

<details><summary>Hint 2</summary>

Filter the window result in an outer query.

</details>

<details><summary>Common mistake to check after trying</summary>

LIMIT 2 would select two projects globally, not per account.

</details>

## W05E02 — Tied budget rankings

Session 1 · Stretch · Topic: Tied budget rankings

Rank all projects within each project_type by budget descending using competition rank: equal budgets share rank and the next rank skips places.

Tables: `projects`. Output columns: `project_type`, `project_id`, `budget`, `budget_rank`.

<details><summary>Hint 1</summary>

RANK differs from ROW_NUMBER and DENSE_RANK.

</details>

<details><summary>Hint 2</summary>

Do not put project_id in the window ordering because that would break budget ties.

</details>

<details><summary>Common mistake to check after trying</summary>

Output ordering and window ranking are separate choices.

</details>

## W05E03 — Latest survey wave

Session 1 · Stretch · Topic: Latest survey wave

For every project, return its latest wave by wave_number along with actual completes.

Tables: `survey_waves`. Output columns: `project_id`, `wave_number`, `completes_actual`.

<details><summary>Hint 1</summary>

Rank wave numbers descending within each project.

</details>

<details><summary>Hint 2</summary>

Keep ROW_NUMBER = 1 in an outer query.

</details>

<details><summary>Common mistake to check after trying</summary>

MAX(wave_number) next to an ungrouped actual count is not portable or clear SQL.

</details>

## W05E04 — Portfolio month-on-month

Session 2 · Stretch · Topic: Portfolio month-on-month

For each invoicing month, return invoice total and change in EUR from the previous month. The first change is NULL. Every calendar month Jan–Jun is present in this dataset. Sort by month.

Tables: `invoices`. Output columns: `month`, `invoiced_eur`, `change_eur`.

<details><summary>Hint 1</summary>

Aggregate to one row per month first.

</details>

<details><summary>Hint 2</summary>

Subtract LAG(invoiced_eur) ordered by month.

</details>

<details><summary>Common mistake to check after trying</summary>

LAG on raw invoices compares invoices, not months.

</details>

## W05E05 — Wave-to-wave change

Session 2 · Stretch · Topic: Wave-to-wave change

For each project wave, show actual completes and change versus the preceding wave number. The first wave change is NULL.

Tables: `survey_waves`. Output columns: `project_id`, `wave_number`, `completes_actual`, `change_completes`.

<details><summary>Hint 1</summary>

Partition by project so accounts are not mixed.

</details>

<details><summary>Hint 2</summary>

Order the window by wave_number.

</details>

<details><summary>Common mistake to check after trying</summary>

Zero is an observed change; NULL means no previous observation.

</details>

## W05E06 — Previous observed month per client

Session 2 · Stretch · Topic: Previous observed month per client

For every client-month with invoices, return total EUR and previous observed month total for that same client. First observation is NULL. Missing months are skipped in this exercise.

Tables: `projects, invoices`. Output columns: `client_id`, `month`, `invoiced_eur`, `previous_eur`.

<details><summary>Hint 1</summary>

Aggregate by client and month, then use LAG.

</details>

<details><summary>Hint 2</summary>

Partition the window by client_id.

</details>

<details><summary>Common mistake to check after trying</summary>

Previous observed month need not be the previous calendar month.

</details>

## W05E07 — Cumulative invoicing

Session 3 · Stretch · Topic: Cumulative invoicing

Return monthly invoice totals and cumulative invoiced EUR, oldest month first.

Tables: `invoices`. Output columns: `month`, `invoiced_eur`, `cumulative_eur`.

<details><summary>Hint 1</summary>

Build a monthly summary first.

</details>

<details><summary>Hint 2</summary>

SUM over ORDER BY month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW.

</details>

<details><summary>Common mistake to check after trying</summary>

A cumulative total on raw invoice rows has invoice grain, not month grain.

</details>

## W05E08 — Client revenue share

Session 3 · Stretch · Topic: Client revenue share

For clients with invoices, return total invoiced EUR and their percentage of all invoiced EUR rounded to two decimals.

Tables: `projects, invoices`. Output columns: `client_id`, `invoiced_eur`, `share_pct`.

<details><summary>Hint 1</summary>

Summarise each account first.

</details>

<details><summary>Hint 2</summary>

SUM(invoiced_eur) OVER () gives the full-account denominator.

</details>

<details><summary>Common mistake to check after trying</summary>

Average invoice share is not the same as account share of total revenue.

</details>

## W05E09 — May to June account movement

Session 4 · Stretch · Topic: May to June account movement

Return every client with May EUR, June EUR, June-minus-May change, and movement labeled growth, decline or flat. Treat absent months as zero.

Tables: `clients, projects, invoices`. Output columns: `client_id`, `may_eur`, `june_eur`, `change_eur`, `movement`.

<details><summary>Hint 1</summary>

Use conditional sums per client for May and June.

</details>

<details><summary>Hint 2</summary>

LEFT JOIN all clients; compute labels from the difference.

</details>

<details><summary>Common mistake to check after trying</summary>

Filtering invoice dates in WHERE after LEFT JOIN can drop inactive clients.

</details>

## W05E10 — Three largest account declines

Session 4 · Stretch · Topic: Three largest account declines

Using the same May/June definition, return up to three declining clients with the most negative EUR changes first, ties by client_id. Include client names.

Tables: `clients, projects, invoices`. Output columns: `client_id`, `client_name`, `change_eur`.

<details><summary>Hint 1</summary>

Exclude flat or growing accounts before selecting three.

</details>

<details><summary>Hint 2</summary>

Calculate monthly totals before ranking or sorting.

</details>

<details><summary>Common mistake to check after trying</summary>

A zero June total is a decline if May was positive; do not lose that account.

</details>

