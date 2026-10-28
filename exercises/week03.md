# Week 3 exercises

Use the browser app for Run query and Check answer, or the command-line checker. All data is fictional. Reporting date: **2025-07-01**; amounts: **EUR**. Use SQLite syntax. Column aliases and their order must match the requested output. Row order matters only when explicitly requested.

## W03E01 — Account names

Session 1 · Practice · Topic: Account names

List every project with its client name and status.

Tables: `projects, clients`. Output columns: `project_id`, `client_name`, `status`.

<details><summary>Hint 1</summary>

The foreign key links each project to one client.

</details>

<details><summary>Hint 2</summary>

Join on client_id.

</details>

<details><summary>Common mistake to check after trying</summary>

Joining without ON creates every project/client combination.

</details>

## W03E02 — Sector portfolio

Session 1 · Practice · Topic: Sector portfolio

Count projects and sum budgets by client sector.

Tables: `projects, clients`. Output columns: `sector`, `project_count`, `total_budget`.

<details><summary>Hint 1</summary>

Each project matches exactly one client.

</details>

<details><summary>Hint 2</summary>

Join then group by sector.

</details>

<details><summary>Common mistake to check after trying</summary>

Group by sector rather than client_name to answer a sector question.

</details>

## W03E03 — Market participation

Session 1 · Practice · Topic: Market participation

Show each assigned project and market name, one row per project-market pair.

Tables: `project_markets, markets`. Output columns: `project_id`, `market_name`.

<details><summary>Hint 1</summary>

Start at the bridge table.

</details>

<details><summary>Hint 2</summary>

Join market_id to the markets key.

</details>

<details><summary>Common mistake to check after trying</summary>

A multi-market project is supposed to appear several times here.

</details>

## W03E04 — Accounts without projects

Session 2 · Practice · Topic: Accounts without projects

Find clients that have no projects.

Tables: `clients, projects`. Output columns: `client_id`, `client_name`.

<details><summary>Hint 1</summary>

Keep all rows from clients with LEFT JOIN.

</details>

<details><summary>Hint 2</summary>

A missing match has NULL in projects.project_id.

</details>

<details><summary>Common mistake to check after trying</summary>

An INNER JOIN cannot retain an unmatched client.

</details>

## W03E05 — Invoice coverage

Session 2 · Practice · Topic: Invoice coverage

Return every project with its invoice count, including a zero count for projects with no invoices.

Tables: `projects, invoices`. Output columns: `project_id`, `invoice_count`.

<details><summary>Hint 1</summary>

Use projects as the left-hand table.

</details>

<details><summary>Hint 2</summary>

COUNT(invoice_id) ignores the NULL placeholder row.

</details>

<details><summary>Common mistake to check after trying</summary>

COUNT(*) incorrectly reports one for a project with no invoices.

</details>

## W03E06 — Unassigned markets

Session 2 · Practice · Topic: Unassigned markets

Find projects with no market assignment.

Tables: `projects, project_markets`. Output columns: `project_id`, `status`.

<details><summary>Hint 1</summary>

An unassigned project is different from a project assigned to one market.

</details>

<details><summary>Hint 2</summary>

LEFT JOIN and test the bridge key for NULL.

</details>

<details><summary>Common mistake to check after trying</summary>

Missing market assignment is a data-quality finding, not evidence of zero commercial value.

</details>

## W03E07 — Client invoice totals

Session 3 · Practice · Topic: Client invoice totals

For every client, show invoiced EUR, with zero for clients without invoices.

Tables: `clients, projects, invoices`. Output columns: `client_id`, `client_name`, `invoiced_eur`.

<details><summary>Hint 1</summary>

Follow client → project → invoice using LEFT JOINs.

</details>

<details><summary>Hint 2</summary>

COALESCE turns a missing SUM into zero.

</details>

<details><summary>Common mistake to check after trying</summary>

SUM(project budget) after joining invoices would repeat each budget.

</details>

## W03E08 — Projects participating by market

Session 3 · Practice · Topic: Projects participating by market

For each market, count assigned projects, including markets with zero assignments.

Tables: `markets, project_markets`. Output columns: `market_name`, `project_count`.

<details><summary>Hint 1</summary>

One bridge row represents one project participating in one market.

</details>

<details><summary>Hint 2</summary>

Count the non-null bridge project_id.

</details>

<details><summary>Common mistake to check after trying</summary>

Adding counts across markets can exceed the total number of projects.

</details>

## W03E09 — Repair multiplied totals

Session 4 · Practice · Topic: Repair multiplied totals

An analyst joined invoices and project_markets and inflated totals. Return every project with its true invoiced EUR and number of assigned markets. Zero-fill both metrics.

Tables: `projects, invoices, project_markets`. Output columns: `project_id`, `invoiced_eur`, `market_count`.

<details><summary>Hint 1</summary>

Aggregate invoices and market assignments separately to project grain.

</details>

<details><summary>Hint 2</summary>

Join those two summaries to projects using CTEs; see the rescue card.

</details>

<details><summary>Common mistake to check after trying</summary>

SUM(DISTINCT amount) is also wrong: separate invoices can have equal amounts.

</details>

## W03E10 — Client and market management view

Session 4 · Practice · Topic: Client and market management view

Return every client with project count, total project budget, invoiced EUR and distinct participating market count. No market-level revenue allocation is defined.

Tables: `clients, projects, invoices, project_markets`. Output columns: `client_id`, `project_count`, `total_budget`, `invoiced_eur`, `market_count`.

<details><summary>Hint 1</summary>

Summarise project values, invoices and market coverage independently by client.

</details>

<details><summary>Hint 2</summary>

Join the three account-grain summaries to clients and zero-fill.

</details>

<details><summary>Common mistake to check after trying</summary>

Neither DISTINCT budget nor assigning all revenue to every market repairs duplicated totals.

</details>

