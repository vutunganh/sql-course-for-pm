"""Compare query results, not SQL spelling; checks run on two datasets."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sqlite3
from contextlib import closing
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from query import DB_PATH, run
from seed import build


def catalog():
    return json.loads((ROOT / 'exercises' / 'catalog.json').read_text())


def reference(exercise):
    text = (ROOT / 'solutions' / f"week{exercise['week']:02}.sql").read_text()
    marker = exercise['id']
    block = text.split(f'-- BEGIN {marker}\n')[1].split(f'-- END {marker}')[0]
    return block


def make_variation(path):
    build(path, seed=73)
    # Deliberate traps: equal invoice values; two market rows; unequal wave targets;
    # account without June completions. These are test fixtures, never learner DML.
    with closing(sqlite3.connect(path)) as db:
        db.execute("INSERT INTO clients VALUES (21, 'Boundary Demo', 'Retail', 'Central Europe')")
        db.execute("INSERT INTO projects VALUES (101,21,'Concept test','2025-04-01','2025-05-01','2025-05-01','completed',50000)")
        db.executemany('INSERT INTO project_markets VALUES (101,?)', [(1,), (2,)])
        db.executemany('INSERT INTO invoices VALUES (?,101,?,?,?)', [
            (301, '2025-05-01', 10000, 0), (302, '2025-06-01', 10000, 1)])
        db.executemany('INSERT INTO survey_waves VALUES (?,101,?,?,?,?,?)', [
            (201, 1, '2025-04-01', '2025-04-12', 100, 100),
            (202, 2, '2025-04-15', '2025-04-26', 1000, 500)])
        db.commit()
    return path


def normalized(rows):
    # SQLite may return 1 or 1.0 for equivalent expressions. Keep NULL distinct.
    return [tuple(round(v, 6) if isinstance(v, float) else v for v in row) for row in rows]


def compare(exercise, sql, path):
    wanted_columns, wanted_rows = run(reference(exercise), path)
    columns, rows = run(sql, path)
    if columns != wanted_columns:
        return False, 'Expected columns in this order: ' + ', '.join(wanted_columns)
    actual, expected = normalized(rows), normalized(wanted_rows)
    equal = actual == expected if exercise['ordered'] else Counter(actual) == Counter(expected)
    if equal:
        return True, f'{len(rows)} rows match.'
    if len(rows) != len(wanted_rows):
        return False, f'Expected {len(wanted_rows)} rows; got {len(rows)}. Check filters, grouping and join grain.'
    if exercise['ordered'] and Counter(actual) == Counter(expected):
        return False, 'Values match, but ordering differs. Check all requested sort keys and directions.'
    return False, 'Row count matches, but values differ. ' + exercise['pitfall']


def check_answer(exercise_id, sql, paths):
    exercise = next((e for e in catalog() if e['id'] == exercise_id.upper()), None)
    if exercise is None:
        raise ValueError('Unknown exercise ID; use W01E01 through W06E10.')
    tests = []
    for label, path in paths:
        try:
            passed, detail = compare(exercise, sql, path)
        except (sqlite3.Error, ValueError) as error:
            passed, detail = False, f'Query could not run: {error}'
        tests.append({'dataset': label, 'passed': passed, 'detail': detail})
    return {'passed': all(t['passed'] for t in tests), 'tests': tests,
            'note': 'Result checks pass; also explain the grain and business meaning to your instructor.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('exercise', help='For example W01E01')
    parser.add_argument('file', type=Path, help='File containing one query')
    args = parser.parse_args()
    try:
        sql = args.file.read_text(encoding='utf-8')
        with tempfile.TemporaryDirectory(prefix='sql-course-check-') as folder:
            variation = make_variation(Path(folder) / 'variation.sqlite3')
            result = check_answer(args.exercise, sql, [('Practice', DB_PATH), ('Variation', variation)])
        for test in result['tests']:
            print(f"{'PASS' if test['passed'] else 'FAIL'} {test['dataset']}: {test['detail']}")
        if result['passed']:
            print(result['note'])
        return 0 if result['passed'] else 1
    except (OSError, ValueError, sqlite3.Error) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
