"""Read-only SQLite query runner, shared by the learner CLI and checks."""
import argparse
from pathlib import Path
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / 'data' / 'research_pm.sqlite3'


def connect(path=DB_PATH):
    if not Path(path).exists():
        raise ValueError('Database missing. Run: python3 scripts/seed.py')
    db = sqlite3.connect(Path(path).resolve().as_uri() + '?mode=ro', uri=True)
    allowed = {sqlite3.SQLITE_SELECT, sqlite3.SQLITE_READ, sqlite3.SQLITE_FUNCTION,
               sqlite3.SQLITE_RECURSIVE}
    db.set_authorizer(lambda action, *args: sqlite3.SQLITE_OK
                      if action in allowed else sqlite3.SQLITE_DENY)
    # Stop accidental runaway joins/recursive queries without extra dependencies.
    remaining = 20000

    def progress():
        nonlocal remaining
        remaining -= 1
        return int(remaining <= 0)

    db.set_progress_handler(progress, 1000)
    return db


def run(sql, path=DB_PATH):
    db = connect(path)
    try:
        cursor = db.execute(sql)
        if cursor.description is None:
            raise ValueError('Enter one SELECT or WITH query.')
        rows = cursor.fetchmany(5001)
        if len(rows) > 5000:
            raise ValueError('Result exceeds 5,000 rows. Check join keys or add a filter.')
        return [column[0] for column in cursor.description], rows
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description='Run one read-only SQLite query.')
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--sql', help='SQL in quotes')
    source.add_argument('--file', type=Path, help='UTF-8 file with one query')
    args = parser.parse_args()
    sql = args.sql if args.sql is not None else args.file.read_text(encoding='utf-8')
    try:
        columns, rows = run(sql)
    except (sqlite3.Error, ValueError) as error:
        print(f'Query could not run: {error}', file=sys.stderr)
        return 1
    print(' | '.join(columns))
    for row in rows:
        print(' | '.join('NULL' if value is None else str(value) for value in row))
    print(f'({len(rows)} rows)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
