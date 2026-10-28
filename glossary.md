# Plain-English SQL glossary

| Term | Meaning in this course |
|---|---|
| Database | A collection of related tables stored here in one SQLite file |
| Table | Rows with the same set of named columns |
| Row / record | One occurrence of the thing represented by a table |
| Column | A named attribute, such as project status or invoice amount |
| Grain | What exactly one row represents; write it down before joining |
| Primary key | Column(s) uniquely identifying a row; project_id identifies a project |
| Foreign key | A stored reference to a row in another table; projects.client_id refers to clients |
| Composite key | A key with several columns, such as project_id plus market_id |
| Cardinality | How many rows can match a row on the other side of a relationship |
| One-to-many | One project can have several invoices |
| Many-to-many | A project can span markets and a market can contain projects; a bridge stores the pairs |
| SELECT | Choose output values and columns |
| WHERE | Filter source rows before aggregation |
| AND / OR | Require both conditions / allow either; use parentheses to clarify combinations |
| IN / BETWEEN | Match a list / match an inclusive range |
| NULL | Missing, unknown or not applicable; not the same as zero or an empty string |
| IS NULL | Test for a missing value; = NULL does not do this |
| ORDER BY | Define output ordering, with ASC or DESC on each key |
| Tie-breaker | An additional sort key that defines an unambiguous order for equal values |
| LIMIT | Restrict the number of returned rows |
| DISTINCT | Remove identical selected rows; does not automatically fix a bad join |
| Aggregate | Collapse several rows into a metric, such as COUNT, SUM or AVG |
| GROUP BY | Make a separate summary for each group key |
| HAVING | Filter groups after aggregation |
| CASE | Choose a value according to a sequence of conditions |
| Alias | A temporary output/table name; AS invoiced_eur labels a metric |
| INNER JOIN | Keep matching row pairs from both tables |
| LEFT JOIN | Keep all left-hand rows, with NULL right-hand values for unmatched rows |
| Bridge table | A table of relationship pairs, such as project_markets |
| Fan-out / row multiplication | Several matches repeat source values, potentially inflating sums |
| Preaggregation | Summarise each source to a shared grain before combining it |
| COALESCE | Return the first non-NULL argument; use zero only if it means no matching amount |
| NULLIF | Return NULL if two values are equal; NULLIF(denominator, 0) guards undefined rates |
| Subquery | A SELECT inside another query; a scalar subquery returns one value |
| CTE / WITH | A named intermediate query result, lasting for one statement |
| Cohort | The precisely defined set of records included in a metric |
| Half-open interval | Include the starting date and exclude the next period's starting date |
| strftime | SQLite date-formatting function; '%Y-%m' gives a year-month label |
| julianday | SQLite numeric date representation, useful for elapsed-day differences |
| LIKE | Match text patterns with % (any sequence) and _ (one character) |
| CAST | Explicitly convert a value to another data type |
| Window function | Compute a value across related rows while keeping individual output rows |
| PARTITION BY | Restart a window calculation for each segment |
| ROW_NUMBER | Give each row a unique position in a defined ordering |
| RANK | Give ties the same rank and leave gaps after ties |
| LAG | Read a preceding observed row in a window; not necessarily a preceding calendar month |
| Running frame | The rows included in a cumulative window, here start through current row |
| Denominator | The population or total by which a metric is divided |
| Weighted attainment | Summed completes divided by summed targets, giving larger waves proportional weight |
| Reconciliation | Check that a report total agrees with a trusted source-table total |
| Read-only | Queries retrieve information without changing the stored data |
| Dialect | A database's particular SQL syntax; this course uses SQLite throughout |
| Fixture | A reproducible test dataset with known properties and edge cases |

Budget is planned value, invoiced EUR is issued billing, paid EUR is billed value marked paid, and unpaid EUR is outstanding billing. None of these alone establishes profit, cash-payment dates, or contractual overdue debt.
