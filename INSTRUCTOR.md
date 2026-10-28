# Teaching and assessment notes

The learner is a research project manager building independent reporting skills. Ask “What decision does this support?” before syntax. Keep the focus on SQL retrieval and interpretation. Database creation and fixture modifications are setup infrastructure, not learner material.

Use the 24-session plan in CURRICULUM.md. Session demos also appear in the classroom; prompts contain optional hints. Solutions live separately in solutions/week01.sql through week06.sql, with BEGIN/END markers so the checker can load each query. Never remove or rename a marker without updating exercise IDs. Student endpoints do not serve solution files. Someone with filesystem access can read them; this is a teaching tool, not a secure testing platform.

## Feedback loop

Ask the learner to state the desired output grain and cohort; predict a row count or property; write the query; inspect results; then run checks. A syntax error needs a syntax correction. A running but incorrect query needs a reasoning correction. Compare source counts, inspect a single key, and reconcile totals rather than merely copying the answer. Use the weekly checkpoint to decide when to revisit a topic.

Week 3 session 4 intentionally introduces a scaffolded WITH pattern before the full Week 4 CTE lesson. Walk through the supplied invoice-count/wave-count demo first. Spend extra time here if needed. The important insight is one row per shared key before joining; memorising WITH syntax is secondary.

## Checks and expected results

Run `python3 scripts/seed.py`, then `python3 checks/validate.py`. The validation suite executes all 60 reference queries on both datasets, verifies declared output columns and meaningful answers, independently reconciles account invoice totals in Python, and checks edge cases. W06E01 intentionally returns no rows because the bridge composite primary key prohibits duplicate pairs. Its conceptual explanation is assessed by the instructor.

For an individual answer, use `python3 checks/check.py W03E09 answer.sql`. The checker compares multisets (including duplicates), or ordered sequences when a prompt asks for sorting. It requires output aliases and their order and treats NULL separately from zero. The practice DB has seed 42; the second dataset uses seed 73 plus a special account with two equal-value invoices, two market assignments and unequally sized survey targets. This exposes DISTINCT-sum repairs, join fan-out, unweighted percentage averages and undefined denominators. Additional dataset variations do not prove every query correct, so inspect reasoning too.

Generate a complete instructor-only expected-results snapshot after dataset changes:

```bash
python3 checks/export_expected.py
```

The generated `solutions/expected_results.json` includes columns and full results for the practice dataset. The checker instead calculates reference results at runtime so data changes are reflected. Generated snapshots are for inspection and should be regenerated if the data or solutions change.

The final four-query capstone combines W06E09, W06E10, a new June-closed-wave client summary, and W06E06. An instructor example for the new summary is in `solutions/capstone.sql`; use the rubric to assess the written briefing. There is no single required narrative: accept any defensible findings grounded in actual outputs.

## Readiness assessment

Use 10 minutes at each weekly checkpoint for explanation without hints. A passing query accompanied by an incorrect account of its grain is not yet ready. The final assessment should verify that she can frame a new stakeholder question, write 4–6 readable queries, reconcile money without duplication, explain undefined rates, and recommend a sensible follow-up while acknowledging missing information.

If confidence is low, redo one similar exercise without viewing the solution, then ask a small variation (another month, threshold or segment). Never use the unit-test display alone to infer readiness for independent business reporting.
