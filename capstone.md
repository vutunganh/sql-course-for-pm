# Monthly account-health and delivery summary

You support a fictional research operations team. Management asks: “Which accounts need attention after June, how reliable was delivery, and where is our financial exposure?” Prepare a briefing at the **2025-07-01** snapshot. Use only the synthetic course database. Work on draft queries during Week 6 sessions 2 and 3, then assemble and present in session 4.

## Deliverables

Submit **4–6 standalone, readable SQL queries**, saved as `query01.sql` and so on, plus a short `briefing.md` (about 300–500 words). Include a definition, source tables, grain, time window, units and denominator beside each metric. Reference query IDs in every finding.

Your four required queries cover:

1. **June commercial health:** for every client, June invoiced EUR and total unpaid EUR across invoices issued before the snapshot. W06E09 can be used as query 1.
2. **June delivery health:** for every client, June completed projects, late completions and late percentage; no June deliveries means a NULL percentage. W06E10 can be used as query 2.
3. **June-closed-wave performance:** for every client, June-closed wave count, total targets, total actual completes and weighted attainment percentage. Include waves with close_date >= '2025-06-01' and < '2025-07-01', regardless of project status. Include all clients; zero-fill counts/complete totals; no qualifying target means NULL attainment. Open waves are excluded. Do not join invoices into the wave aggregation.
4. **Unpaid financial exposure:** show unpaid invoice counts and EUR by issuance-age band (0–30, 31–60, 61+ elapsed days as of the snapshot). Include only nonempty bands. Explain that due dates and past payment states are unavailable. W06E06 provides this query.

Optional queries 5–6 may show May/June calendar-month movement, client concentration or market delivery participation. Do not invent market revenue allocation.

Write **3 key findings, 1 risk, and 1 recommended follow-up**. Give amounts, percentages, cohorts and evidence references. An example sentence shape is “Query 2 shows [n] of [d] June completions late ([p]%), suggesting we should investigate [specific operational question].” Fill this with your own actual results, not invented values.

## Before presenting

Reconcile account invoice totals to source invoice totals for the same period. Check the sum of project counts without market duplication. Verify a client's rate manually. Distinguish invoice-date, delivery-date and wave-close-date cohorts. Ask whether an account with no June deliveries should be interpreted as healthy, unhealthy or simply unassessed on that measure.

## Scoring rubric (100 points)

| Criterion | Points | Full-credit evidence |
|---|---:|---|
| Metric and cohort correctness | 30 | Four required areas; correct periods, boundaries, status filters, weighted rates and rounding |
| Grain, duplicates and missing data | 25 | Independent preaggregation; source reconciliation; all-client retention; meaningful zero/NULL handling |
| Readable queries | 15 | Clear aliases, indentation and named intermediate steps; each query runs independently |
| Interpretation and action | 25 | Three accurate findings tied to query outputs; one supported risk; one specific, feasible follow-up; no causal overclaim |
| Reproducibility and limitations | 5 | Snapshot, currency and definitions stated; unpaid versus overdue and unavailable market allocation acknowledged |

Suggested readiness standard: **80/100**, with no unresolved revenue double-counting, wrong delivery denominator or open-wave inclusion in closed-wave performance. At 60–79, revise the affected queries and explain the correction; below 60, revisit the corresponding weekly checkpoint. Automated checks are a practice aid, not the capstone's full assessment.
