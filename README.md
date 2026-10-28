# SQL for research project managers

A six-week, practice-first course for answering business questions with read-only SQL. Built for project management, research operations and insights work. It uses **fictional synthetic data only** and does not describe any actual internal systems or clients.

The course includes 24 guided sessions, 60 checked exercises, a browser classroom, separate instructor answers, and a management-briefing capstone. The dialect is **SQLite**, including all date and window-function examples. No Docker, paid service, Python packages or internet connection is needed after Python is available.

## Start on macOS

You need Python **3.10 or newer**, built with SQLite **3.25 or newer**, and a browser. Check in Terminal:

```bash
python3 --version
```

If `python3` is unavailable, install Python 3 first. In Terminal, type `cd `, drag the `sql-for-research-pm` folder into the window to fill in its path, and press Return. Then run:

```bash
python3 scripts/app.py
```

The app creates the practice database on its first launch and opens **http://127.0.0.1:8765**. Keep Terminal open while practising; press Ctrl+C there to stop. This runs locally on your computer. If the browser does not open, enter that address manually. If the port is busy, run `python3 scripts/app.py --port 8766` and use the printed address.

You can also double-click **Start Classroom.command** on macOS. If your machine does not allow that launcher, use the Terminal command above.

## Your first session

1. Select **Week 1**, then **Meet the clients** (W01E01).
2. Open **Explore the tables** and identify what one row in `clients` represents.
3. Open the mini lesson, read the short example, and write your own answer in **Your SQL**.
4. Click **Run query** to inspect the table. Click **Check answer** to test it.
5. If needed, expand Hint 1, revise and check again. Continue to the next exercise when you can explain why the answer is correct.

The session is about 55 minutes. There are four sessions per week. See [CURRICULUM.md](CURRICULUM.md) for the full day-by-day teaching plan, demonstrations, review questions and weekly checkpoints.

The browser's **Course notes** button also contains the full learning plan, final briefing instructions and glossary.

The **Source tables** panel automatically shows the tables used in the current exercise. Choose a table button to inspect **every row and column** of the practice data, including NULLs. Scroll within the table; the preview has no row sampling or pagination. It stays alongside your work on larger screens and appears above the exercise on smaller screens. Running a query displays its results separately, so the source data remains available while you work.

Drafts and passes are saved in this browser's local storage. Return using the **same browser and address/port**. Editing a passed answer clears its pass until it is checked again. Private browsing, clearing site data, a different port, or switching between `localhost` and `127.0.0.1` may give you a separate or empty progress store. Use **Export .sql** to keep portable copies of your work. There is no account or cloud sync.

## What a passing answer means

Check answer runs the query against the practice data and a second synthetic dataset with different values and deliberate edge cases. It compares output columns, values, NULLs and duplicate-row counts. Row order matters only when requested. Different valid SQL approaches can pass; exact SQL text is never compared. Use the requested column aliases and column order. Numeric results allow differences below the six-decimal comparison precision; requested rounding remains part of the problem.

Feedback distinguishes column mismatches, row-count differences, sorting errors and incorrect values. It does not display solution SQL. The local files in `solutions/` contain instructor answers; these are separated for teaching convenience, not an exam-security boundary. Passing the fixtures is evidence of correctness, not a proof for every possible dataset. Business reasoning and the written briefing need human review.

The app accepts one read-only `SELECT` or `WITH` statement per action. Writes, attachments and extension loading are blocked. Runaway queries and outputs above 5,000 rows are stopped, so an accidental cross join does not overwhelm the classroom.

## Six-week roadmap

| Week | Main work | Evidence of readiness |
|---|---|---|
| 1 | Tables, grain, filters, missing values, sorting | Triage active and late work with precise definitions |
| 2 | Counts, totals, grouping, HAVING, CASE | Build a small status dashboard |
| 3 | Joins, missing relations, many-to-many data | Repair inflated revenue and reconcile totals |
| 4 | Dates, text, subqueries, readable CTEs | Produce a monthly delivery report |
| 5 | Rankings, LAG, cumulative totals and shares | Explain account growth and decline |
| 6 | Delivery, survey and commercial cases | Present 4–6 queries and a short management briefing |

## Data and definitions

The reporting date is fixed at **2025-07-01**. All amounts are whole **EUR**, with no tax or currency conversion model. Projects, invoices and waves cover the first half of 2025. Clients and market labels are invented examples; real country names provide geographic context. See [data/README.md](data/README.md) for grains, keys and metric definitions, and [glossary.md](glossary.md) for plain-English SQL terms.

There are 20 clients, 100 projects, 10 markets, 300 invoices, 200 survey waves and a project-market bridge. Two clients have no projects, some projects have no invoices or market assignments, and the data includes late deliveries, active overdue work, unpaid invoices and waves above/below target. Missing market assignments are intentional data-quality examples. Cancelled projects may have historical invoices and survey activity.

Revenue means **invoiced EUR** when used informally here. Budget, invoiced value and paid value are separate. A project may have multiple invoices and multiple markets: joining them directly multiplies amounts. No rule allocates project revenue to markets; market questions use participation counts instead.

## Terminal alternative

From this course folder:

```bash
# Rebuild the exact deterministic practice data (overwrites that generated DB).
python3 scripts/seed.py

# Run one query directly.
python3 scripts/query.py --sql "SELECT project_id, status FROM projects LIMIT 5;"

# Or run/check one answer file you created in your editor.
python3 scripts/query.py --file my_answer.sql
python3 checks/check.py W01E01 my_answer.sql

# Instructor: validate the dataset, reference queries, checker and app routes.
python3 checks/validate.py
```

Optional developer UI behavior checks use `node checks/frontend.cjs` if Node is available. Node is not needed to use the course. These checks use a DOM adapter and mocked network responses; they do not replace a visual browser smoke test. In environments that prohibit sockets, the Python suite tests HTTP handlers in memory and explicitly skips its live-server test.

The checker returns exit code 0 for a pass and 1 for a failure. It creates its test variation temporarily and leaves the practice database unchanged. Query files should be UTF-8. Prompts also exist in `exercises/week01.md` through `week06.md`; reference answers are in `solutions/week01.sql` through `week06.sql`.

## For the instructor

Read [INSTRUCTOR.md](INSTRUCTOR.md) and [capstone.md](capstone.md). Let the learner explain the population, grain, unit and denominator before showing answers. Run the validation suite after changing data or questions. You do not need to teach table creation, data modification, indexes, stored procedures or database administration; the setup script handles database creation behind the scenes.
