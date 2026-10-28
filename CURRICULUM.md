# Six-week SQL curriculum

For a project manager in market research or insights; no coding experience assumed. All examples use fictional research operations, not any actual systems or real customer information. The goal is independent reporting and analysis, not database administration.

**Schedule:** four core sessions per week, about 55 minutes each. Allow 5 minutes to recall the last session, 10 minutes for explanation and demonstration, 30 minutes for exercises, and 10 minutes for interpretation/review. This places roughly 20% on instruction, 60% on practice, and 20% on mini-cases/review. Longer cases may spill into the optional review day. Do not speed through a join misconception just to keep the calendar.

Use each session's mini lesson in the browser or below. Predict what the demonstration returns, run it, then change one part. The worked examples demonstrate related ideas without supplying the exercise answers. Exercises WxxEyy have separate optional hints and separate instructor solutions. Passing checks is useful evidence; explain the answer in business language too.

Weekly rhythm: days 1–4 are core sessions; day 5 is an optional 20–30-minute redo of one difficult exercise without hints; days 6–7 are rest or catch-up. No paid subscriptions, Docker or external practice platform is needed.

## Week 1, day 1: Tables, keys and first queries

Prerequisites: None; opening the classroom is enough.

Goals: Describe rows, columns and grain; select columns; take a deterministic preview.

A database is a collection of related tables. One projects row is one project; one invoices row is one invoice. project_id identifies a project; client_id in projects points to its client. SELECT chooses columns, FROM chooses the table. ORDER BY defines order and LIMIT takes a preview. SQL keywords are case-insensitive; quoted text is data. End one query with a semicolon.

Demonstration (run one statement at a time):

```sql
SELECT invoice_id, project_id, amount
FROM invoices
ORDER BY invoice_id
LIMIT 4;
```

Demo practice: Identify the grain of the result, then change the preview to six rows. Open Explore the tables and find the project foreign key.

Independent practice: **W01E01, W01E02, W01E03**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: What does one row mean? Could a client_id appear in several projects without being an error?

## Week 1, day 2: Filters and missing values

Prerequisites: Week 1 session 1.

Goals: Combine filters; recognise inclusive boundaries; test NULL correctly.

WHERE keeps rows whose condition is true. AND requires both conditions; OR accepts either. IN lists alternatives. BETWEEN includes both boundaries. NULL represents a missing or unknown value: use IS NULL or IS NOT NULL, never = NULL. A condition on a missing value usually evaluates to unknown and the row is excluded.

Demonstration (run one statement at a time):

```sql
SELECT invoice_id, amount
FROM invoices
WHERE paid_flag = 0 AND amount >= 15000;
```

Demo practice: Change the threshold, then count how the visible rows change. Predict which side of an exact boundary is included.

Independent practice: **W01E04, W01E05, W01E06**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: Explain why an absent completion date does not, on its own, mean an active project.

## Week 1, day 3: Ordering and unique lists

Prerequisites: Filters and SELECT.

Goals: Sort on multiple keys; deduplicate a selected value.

ORDER BY defaults to ascending. DESC reverses a particular sort key. Use a unique ID as a final tie-breaker when order must be stable. DISTINCT removes identical output rows. DISTINCT status describes status values; DISTINCT status, budget describes distinct pairs. Tables have no guaranteed default row order.

Demonstration (run one statement at a time):

```sql
SELECT DISTINCT sector
FROM clients
ORDER BY sector DESC;
```

Demo practice: Change DESC to ASC. Explain how DISTINCT would change if client_id were included.

Independent practice: **W01E07, W01E08**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: Why is LIMIT without ORDER BY insufficient for a reproducible top-five list?

## Week 1, day 4: Mini-case: portfolio triage

Prerequisites: All Week 1 syntax.

Goals: Translate a delivery question into a precise filter; explain missing dates.

Before typing SQL, state the row grain, selected columns and business definition. Here the reporting date is fixed at 2025-07-01. Active overdue work means status active and planned_end_date before that date. A completed delay instead compares actual and planned delivery dates. Cancelled projects are outside both cohorts.

Demonstration (run one statement at a time):

```sql
SELECT project_id, planned_end_date
FROM projects
WHERE status = 'active'
ORDER BY planned_end_date, project_id
LIMIT 5;
```

Demo practice: Read the five projects as a PM. Which need a date check before calling them overdue? Date strings in this course are ISO YYYY-MM-DD.

Independent practice: **W01E09, W01E10**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: Write a two-sentence status update referencing your results. Which definition did you use?

Weekly checkpoint: Without hints, filter active work, identify a missing date and explain a tie-breaker. Explain the grain of three tables. If you cannot explain this yet, redo the demonstration and the week's last two exercises with your instructor.

## Week 2, day 1: Metrics and NULL-aware counts

Prerequisites: Week 1.

Goals: Use COUNT, SUM, AVG, MIN and MAX; distinguish a row count from a non-null count.

Aggregates turn many rows into a summary. COUNT(*) counts rows; COUNT(column) ignores NULL. SUM and AVG also ignore NULL rather than treating it as zero. Budget is planned value; invoiced EUR is the sum of invoices; paid EUR includes only paid_flag 1. ROUND(value, 2) controls displayed precision.

Demonstration (run one statement at a time):

```sql
SELECT COUNT(*) AS wave_count,
       MIN(completes_target) AS smallest_target,
       MAX(completes_target) AS largest_target
FROM survey_waves;
```

Demo practice: Add average target with a clear alias. Explain why counting actual_end_date differs from counting projects.

Independent practice: **W02E01, W02E02, W02E03**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: Name the unit, time scope and grain for every metric you calculated.

## Week 2, day 2: Grouping and segmentation

Prerequisites: Aggregate functions.

Goals: Create one summary row per segment; select only grouping keys and metrics.

GROUP BY creates a separate aggregate for each key value. Grouping projects by client_id gives account grain. Every non-aggregated selected column should be a grouping key. SQLite sometimes allows other columns, but the chosen value may be arbitrary: avoid that shortcut. A sum of wave targets answers a different question from a count of waves.

Demonstration (run one statement at a time):

```sql
SELECT project_type, AVG(budget) AS average_budget
FROM projects
GROUP BY project_type;
```

Demo practice: Add project count and predict the number of output rows before running.

Independent practice: **W02E04, W02E05, W02E06**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: How did the grain change between the source table and the result?

## Week 2, day 3: Filtering rows versus groups

Prerequisites: GROUP BY and WHERE.

Goals: Apply WHERE before aggregation and HAVING after aggregation.

WHERE removes source rows before grouping; HAVING removes groups after their metrics are calculated. Write the cohort first, then the grouping, then the threshold. A client with a combined budget above a threshold may have no individual project above it.

Demonstration (run one statement at a time):

```sql
SELECT project_type, COUNT(*) AS active_projects
FROM projects
WHERE status = 'active'
GROUP BY project_type
HAVING COUNT(*) >= 2;
```

Demo practice: Predict what happens if the status filter is removed. Decide whether the threshold belongs in WHERE or HAVING.

Independent practice: **W02E07, W02E08**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: Explain, in business terms, the population being counted and the group selection rule.

## Week 2, day 4: CASE and a simple dashboard

Prerequisites: Week 2 aggregates and filters.

Goals: Build categories and conditional metrics; test category boundaries.

CASE WHEN condition THEN value ELSE other END creates a derived value. Branches are tested in order and the first true branch wins. SUM(CASE WHEN condition THEN 1 ELSE 0 END) counts matching rows. COUNT of that expression would also count its zero values, giving the wrong metric.

Demonstration (run one statement at a time):

```sql
SELECT invoice_id,
       CASE WHEN paid_flag = 1 THEN 'Paid' ELSE 'Unpaid' END AS payment_status
FROM invoices
LIMIT 5;
```

Demo practice: Explain the label for each displayed row. Then sketch a three-band budget definition on paper.

Independent practice: **W02E09, W02E10**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: Build a brief dashboard statement with one count and one currency total. Are the units explicit?

Weekly checkpoint: Produce one grouped metric and one conditional count. Explain COUNT(*) versus COUNT(nullable_column), and WHERE versus HAVING. If you cannot explain this yet, redo the demonstration and the week's last two exercises with your instructor.

## Week 3, day 1: Keys and INNER JOIN

Prerequisites: Week 2; primary and foreign keys.

Goals: Join on keys; predict one-to-many row counts.

JOIN matches rows using an ON condition. A project belongs to one client, so projects joined to clients stays at project grain. One project may have multiple invoices, so joining invoices creates invoice grain. Never join names merely because they look similar; use the documented keys.

Demonstration (run one statement at a time):

```sql
SELECT i.invoice_id, p.project_type, i.amount
FROM invoices i
JOIN projects p ON p.project_id = i.project_id
LIMIT 5;
```

Demo practice: Identify each table alias and the output grain. Predict whether this join can repeat a project ID.

Independent practice: **W03E01, W03E02, W03E03**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: Which side must have a unique key to avoid multiplying rows?

## Week 3, day 2: LEFT JOIN and missing relations

Prerequisites: INNER JOIN and NULL.

Goals: Retain unmatched records; count matches correctly.

LEFT JOIN retains every left-hand row. When there is no match, right-hand columns are NULL. Count a right-hand primary key to count real matches, rather than COUNT(*). A right-table filter in WHERE can accidentally discard unmatched rows; move it into ON if those left rows must remain.

Demonstration (run one statement at a time):

```sql
SELECT c.client_id, COUNT(p.project_id) AS active_projects
FROM clients c
LEFT JOIN projects p ON p.client_id = c.client_id
  AND p.status = 'active'
GROUP BY c.client_id;
```

Demo practice: Locate zero counts. Explain what changes if the active-status condition moves to WHERE.

Independent practice: **W03E04, W03E05, W03E06**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: What is the difference between a missing relationship and a numeric zero?

## Week 3, day 3: Several tables, several grains

Prerequisites: INNER/LEFT JOIN and aggregation.

Goals: Follow a key path; distinguish project-market participation from financial attribution.

A bridge row in project_markets is one assignment, and its two-column key is unique. Projects can span several markets; invoices belong to projects, not markets. Therefore the data cannot identify actual revenue earned in each market. Report market participation counts, or agree an explicit allocation rule before allocating money. COALESCE(value, 0) supplies zero for a missing financial total when that meaning is justified.

Demonstration (run one statement at a time):

```sql
SELECT p.project_id, m.market_name
FROM projects p
JOIN project_markets pm ON pm.project_id = p.project_id
JOIN markets m ON m.market_id = pm.market_id
WHERE p.project_id = 1;
```

Demo practice: Count project 1 market assignments. Predict what happens if its invoices are added to this join.

Independent practice: **W03E07, W03E08**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: Can you sum market participation counts into a unique portfolio project count? Why?

## Week 3, day 4: Mini-case: repair inflated totals

Prerequisites: Week 3 joins; use the supplied CTE rescue pattern.

Goals: Detect join fan-out; preaggregate independent one-to-many tables.

Two invoice rows joined to three market assignments produce six rows, repeating the money three times. SUM(DISTINCT amount) also fails if two real invoices have equal values. Rescue pattern: WITH names a temporary query result for this one statement. GROUP BY project_id inside each CTE creates one row per project before joining. Week 4 explores WITH in more detail. For the final exercise, use the same pattern at client grain.

Demonstration (run one statement at a time):

```sql
WITH invoice_counts AS (
  SELECT project_id, COUNT(*) AS invoice_count
  FROM invoices GROUP BY project_id
), wave_counts AS (
  SELECT project_id, COUNT(*) AS wave_count
  FROM survey_waves GROUP BY project_id
)
SELECT p.project_id, COALESCE(i.invoice_count, 0) AS invoice_count,
       COALESCE(w.wave_count, 0) AS wave_count
FROM projects p
LEFT JOIN invoice_counts i ON i.project_id = p.project_id
LEFT JOIN wave_counts w ON w.project_id = p.project_id;
```

Demo practice: Draw the 2-by-3 fan-out on paper. Trace why each CTE output is now unique by project_id.

Independent practice: **W03E09, W03E10**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: Reconcile your account revenue sum to the invoice-table total before trusting the report.

Weekly checkpoint: Explain a 2-by-3 join fan-out and repair it by preaggregation. Reconcile invoiced EUR to the invoice source; preserve clients with no projects. If you cannot explain this yet, redo the demonstration and the week's last two exercises with your instructor.

## Week 4, day 1: Dates and reporting periods

Prerequisites: Week 3.

Goals: Use half-open date ranges; group by month and quarter with SQLite.

This dataset stores ISO date text, so date-only comparisons sort correctly. Define months with date >= first day AND date < next month. SQLite strftime('%Y-%m', date_column) returns a month key. Use julianday for elapsed-day arithmetic, never subtraction of date strings. The reporting snapshot is fixed; do not use date('now').

Demonstration (run one statement at a time):

```sql
SELECT invoice_id, invoice_date, amount
FROM invoices
WHERE invoice_date >= '2025-05-01'
  AND invoice_date < '2025-06-01';
```

Demo practice: Change the period to April. Identify which business event controls this report date.

Independent practice: **W04E01, W04E02, W04E03**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: When should a monthly report use start_date, actual_end_date or invoice_date?

## Week 4, day 2: Text and elapsed time

Prerequisites: Date filters; ordinary SELECT expressions.

Goals: Match text with LIKE; transform labels; calculate day differences.

LIKE uses % for any sequence of characters and _ for a single character. LOWER and UPPER transform text; LENGTH counts characters. Keep IDs for relationships even when labels are cleaned. For dates, julianday(end) - julianday(start) gives elapsed days. CAST(value AS INTEGER) converts a whole-day result to an integer.

Demonstration (run one statement at a time):

```sql
SELECT client_id, LOWER(client_name) AS search_label
FROM clients
WHERE LOWER(client_name) LIKE 'a%';

-- Separate example; run one query at a time:
-- SELECT julianday('2025-06-10') - julianday('2025-06-01') AS elapsed_days;
```

Demo practice: Change the search to names containing e. Run the separate date example and predict its answer first.

Independent practice: **W04E04, W04E05, W04E06**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: Would elapsed duration include both endpoint dates? Our definition uses elapsed days, so no.

## Week 4, day 3: Subqueries and readable steps

Prerequisites: Aggregates, joins and the Week 3 rescue card.

Goals: Use a scalar benchmark; name intermediate summaries with WITH.

A scalar subquery returns one value, such as a portfolio average. A CTE begins WITH name AS (...) and can be read as a named intermediate table. Multiple CTEs are separated by commas, and a final SELECT consumes them. They do not create or change permanent tables. Write and run each intermediate SELECT first, checking its grain.

Demonstration (run one statement at a time):

```sql
WITH type_summary AS (
  SELECT project_type, COUNT(*) AS project_count
  FROM projects GROUP BY project_type
)
SELECT project_type, project_count
FROM type_summary
WHERE project_count >= 10;
```

Demo practice: Run just the inner SELECT, then the whole query. Give the summary grain a plain-English name.

Independent practice: **W04E07, W04E08**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: Which intermediate result needs to be unique before the next join?

## Week 4, day 4: Mini-case: monthly delivery report

Prerequisites: Dates, CASE, CTEs and safe joins.

Goals: Separate report cohorts; compute defensible rates; reconcile independent totals.

A report can contain several metrics without sharing one source cohort. June starts use start_date; June deliveries use actual_end_date and completed status; June invoicing uses invoice_date. Late share is late completed projects divided by completed projects, multiplied by 100.0. Integer division can silently truncate a rate. NULLIF(denominator, 0) returns NULL for an undefined rate.

Demonstration (run one statement at a time):

```sql
SELECT COUNT(*) AS completed_projects,
       ROUND(100.0 * SUM(CASE WHEN actual_end_date > planned_end_date
                    THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 1) AS late_pct
FROM projects
WHERE status = 'completed';
```

Demo practice: Compare the all-time metric with a June-only cohort. Write the denominator beside the output.

Independent practice: **W04E09, W04E10**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: How would you explain an undefined rate to a stakeholder without implying success?

Weekly checkpoint: Define a June cohort using half-open boundaries, calculate a late-delivery rate and explain a zero denominator. If you cannot explain this yet, redo the demonstration and the week's last two exercises with your instructor.

## Week 5, day 1: Rankings and top N per group

Prerequisites: Week 4 CTEs and ordering.

Goals: Use ROW_NUMBER and RANK; filter a window result in an outer query.

Window functions keep individual rows while calculating over a partition. ROW_NUMBER gives each row a unique position; add a unique tie-breaker for deterministic selection. RANK gives equal values equal rank and leaves gaps. PARTITION BY restarts the calculation for each segment. Window results cannot be filtered in the same SELECT WHERE; use a CTE and filter outside.

Demonstration (run one statement at a time):

```sql
SELECT client_id, project_id, start_date,
       ROW_NUMBER() OVER (PARTITION BY client_id
         ORDER BY start_date, project_id) AS start_position
FROM projects;
```

Demo practice: Find each account’s first start. Predict how budget ties should behave under ROW_NUMBER versus RANK.

Independent practice: **W05E01, W05E02, W05E03**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: What distinction determines whether to use ROW_NUMBER or RANK?

## Week 5, day 2: Change over time with LAG

Prerequisites: Window partitions and monthly aggregation.

Goals: Compare successive observations; distinguish missing months from zero activity.

LAG(value) reads the previous row in the window ordering. Aggregate invoices to month grain before comparing months. With PARTITION BY client_id, each account has its own history. The first observation has no predecessor, so the result is NULL. If a calendar month is missing, LAG skips it; use a calendar spine and zero-fill when true calendar-month comparison is required. This week explicitly states which definition each exercise uses.

Demonstration (run one statement at a time):

```sql
SELECT project_id, wave_number, completes_target,
       LAG(completes_target) OVER (PARTITION BY project_id
         ORDER BY wave_number) AS previous_target
FROM survey_waves;
```

Demo practice: Explain the first-row NULLs. Is a change in raw completes a quality change if targets also changed?

Independent practice: **W05E04, W05E05, W05E06**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: When can previous observed month be misread as previous calendar month?

## Week 5, day 3: Cumulative totals and share of total

Prerequisites: SUM, window functions and monthly grain.

Goals: Use an explicit running frame; keep the right percentage denominator.

SUM(value) OVER () produces the overall total without collapsing rows. Add ORDER BY and an explicit ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW frame for a running total. Calculate at the grain required by the report, then apply the window. Round only final percentages; early rounding can distort totals.

Demonstration (run one statement at a time):

```sql
SELECT invoice_id, amount,
       SUM(amount) OVER (ORDER BY invoice_date, invoice_id
         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_eur
FROM invoices
ORDER BY invoice_date, invoice_id
LIMIT 10;
```

Demo practice: Predict what the final running total would equal if LIMIT were removed. Contrast invoice grain with monthly grain.

Independent practice: **W05E07, W05E08**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: Can rounded client shares sum to 99.99% rather than 100% without an error?

## Week 5, day 4: Mini-case: account growth and decline

Prerequisites: Week 5 functions, CASE and LEFT JOIN.

Goals: Compare fixed calendar months; zero-fill absent activity; avoid causal overclaims.

For account movement, compare May and June explicitly, not just successive observed rows. All clients must remain visible, including those with no invoices in June. A decline in invoicing can reflect timing rather than loss of business. Quantify the change, state the period and suggest a follow-up rather than claiming a cause from these tables.

Demonstration (run one statement at a time):

```sql
SELECT strftime('%Y-%m', invoice_date) AS month,
       SUM(amount) AS invoiced_eur
FROM invoices
WHERE invoice_date >= '2025-05-01' AND invoice_date < '2025-07-01'
GROUP BY month
ORDER BY month;
```

Demo practice: Predict how monthly totals can fall while a particular client grows. Draft a factual headline.

Independent practice: **W05E09, W05E10**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: What additional information would distinguish billing timing from client churn?

Weekly checkpoint: Choose ranking semantics for ties; distinguish previous observation from previous calendar month; interpret a decline without inventing its cause. If you cannot explain this yet, redo the demonstration and the week's last two exercises with your instructor.

## Week 6, day 1: Schema walkthrough and audit

Prerequisites: Weeks 1–5.

Goals: State table grains and key paths unaided; validate input counts before joins.

Rebuild the schema map from memory, then compare it with Explore the tables. Note the two independent one-to-many links from projects to invoices and waves, plus many-to-many market participation. A count audit and key uniqueness check are small safeguards before a management report. A passing empty-result check needs a conceptual explanation: the bridge primary key enforces uniqueness.

Demonstration (run one statement at a time):

```sql
SELECT project_id, COUNT(*) AS waves_per_project
FROM survey_waves
GROUP BY project_id
ORDER BY project_id
LIMIT 5;
```

Demo practice: Draw the clients → projects → invoices and projects → waves paths. Mark each grain and cardinality.

Independent practice: **W06E01, W06E02**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: Before joining two summaries, what uniqueness property must each have?

## Week 6, day 2: Delivery and survey operations

Prerequisites: Date cohorts, safe aggregation and rates.

Goals: Define overdue rates; compute weighted attainment; interpret overlapping market counts.

Active overdue and completed late are separate delivery measures. Wave attainment should use closed waves so an in-progress wave is not judged prematurely. A weighted completion rate is SUM(actual) / SUM(target), not an average of percentages when targets differ. Market delivery participation overlaps because projects can span markets.

Demonstration (run one statement at a time):

```sql
SELECT COUNT(*) AS closed_waves,
       ROUND(100.0 * SUM(completes_actual) / SUM(completes_target), 1) AS attainment_pct
FROM survey_waves
WHERE close_date IS NOT NULL;
```

Demo practice: Explain why over 100% attainment is possible. Save a draft capstone query for June-closed waves by client.

Independent practice: **W06E03, W06E04, W06E05**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: Which exclusions and denominators must appear in a delivery summary footnote?

## Week 6, day 3: Commercial health and exposure

Prerequisites: Cohorts, preaggregation and rankings.

Goals: Separate budget, invoiced and paid value; age unpaid balances without calling them overdue.

All amounts are EUR and payment flags describe the snapshot as of 2025-07-01. No payment dates, due dates, taxes or exchange rates are modeled. You can calculate outstanding invoiced value and age since issuance; you cannot infer contractual overdue debt or reconstruct past payment status. Financial totals must reconcile to invoices before adding segment labels.

Demonstration (run one statement at a time):

```sql
SELECT paid_flag, COUNT(*) AS invoice_count, SUM(amount) AS invoiced_eur
FROM invoices
GROUP BY paid_flag;
```

Demo practice: Reconcile paid plus unpaid to total invoiced EUR. Save an unpaid-ageing query for the capstone.

Independent practice: **W06E06, W06E07, W06E08**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: What would you need before describing an unpaid balance as overdue or a budget as revenue?

## Week 6, day 4: Management briefing

Prerequisites: All prior sessions; bring draft queries from sessions 2 and 3.

Goals: Deliver 4–6 queries with definitions; write evidence-linked findings, a risk and an action.

The final two checked exercises supply the June commercial and delivery tables. Add your June-closed-wave attainment and unpaid-ageing queries for a four-query briefing; optional queries may explore trends or market participation. Every finding must name its query and period. Automated result checks assess the SQL; an instructor separately reviews definitions, clarity and interpretation using capstone.md.

Demonstration (run one statement at a time):

```sql
-- A reconciliation to run before writing the briefing:
SELECT SUM(amount) AS total_invoiced_eur,
       SUM(CASE WHEN paid_flag = 1 THEN amount ELSE 0 END) AS paid_eur,
       SUM(CASE WHEN paid_flag = 0 THEN amount ELSE 0 END) AS unpaid_eur
FROM invoices;
```

Demo practice: Use 15 minutes to finish the two checked tables, 25 minutes to assemble 4–6 queries and 15 minutes to write and discuss the briefing.

Independent practice: **W06E09, W06E10**. Read the question, state the grain and output, predict a result property, then write SQL. Use Hint 1 only after a first attempt; Hint 2 if still stuck. Run query to inspect, then Check answer to test.

Review: Can someone unfamiliar with your SQL identify each metric, denominator, date cohort and recommended follow-up?

Weekly checkpoint: Complete the capstone rubric. Explain each query without reading a solution and identify one limitation of the data. If you cannot explain this yet, redo the demonstration and the week's last two exercises with your instructor.

