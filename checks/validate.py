"""Instructor validation: python3 checks/validate.py (stdlib only)."""
from http.server import ThreadingHTTPServer
import io
import json
from pathlib import Path
import re
import sqlite3
from contextlib import closing
import sys
import tempfile
import threading
import unittest
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'checks'))
from check import catalog, check_answer, compare, make_variation, reference
from query import run
from seed import build
from app import handler_for


class CourseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = tempfile.TemporaryDirectory(prefix='sql-course-validation-')
        cls.practice = build(Path(cls.folder.name) / 'practice.sqlite3')
        cls.variation = make_variation(Path(cls.folder.name) / 'variation.sqlite3')
        cls.items = {e['id']: e for e in catalog()}

    @classmethod
    def tearDownClass(cls):
        cls.folder.cleanup()

    def test_course_completeness_and_all_reference_queries(self):
        lessons = json.loads((ROOT / 'exercises' / 'lessons.json').read_text())
        self.assertEqual(len(self.items), 60)
        self.assertEqual(len({(l['week'], l['session']) for l in lessons}), 24)
        self.assertEqual({(e['week'], e['session']) for e in self.items.values()},
                         {(w, s) for w in range(1, 7) for s in range(1, 5)})
        for path in (self.practice, self.variation):
            for e in self.items.values():
                with self.subTest(dataset=path.name, exercise=e['id']):
                    columns, rows = run(reference(e), path)
                    self.assertEqual(columns, e['columns'])
                    if e['id'] != 'W06E01':
                        self.assertTrue(rows, 'Exercise must have a meaningful nonempty answer.')
                    else:
                        self.assertEqual(rows, [])

    def test_reproducible_seed_and_integrity(self):
        clone = build(Path(self.folder.name) / 'clone.sqlite3')
        with closing(sqlite3.connect(clone)) as a, closing(sqlite3.connect(self.practice)) as b:
            self.assertEqual(list(a.iterdump()), list(b.iterdump()))
            self.assertEqual(b.execute('PRAGMA integrity_check').fetchone()[0], 'ok')
            self.assertEqual(b.execute('PRAGMA foreign_key_check').fetchall(), [])
            counts = [b.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]
                      for t in ('clients', 'projects', 'markets', 'invoices', 'survey_waves')]
            self.assertEqual(counts, [20, 100, 10, 300, 200])
            for table, column in [('projects', 'start_date'), ('invoices', 'invoice_date'),
                                  ('survey_waves', 'launch_date')]:
                self.assertEqual(b.execute(f"SELECT COUNT(*) FROM {table} WHERE {column}>='2025-07-01'").fetchone()[0], 0)
            months = b.execute("SELECT DISTINCT strftime('%Y-%m',invoice_date) FROM invoices ORDER BY 1").fetchall()
            self.assertEqual([r[0] for r in months], [f'2025-{m:02}' for m in range(1, 7)])

    def test_financial_totals_with_independent_python_aggregation(self):
        with closing(sqlite3.connect(self.practice)) as db:
            invoices = db.execute('SELECT project_id,amount,paid_flag FROM invoices').fetchall()
            project_client = dict(db.execute('SELECT project_id,client_id FROM projects'))
        expected = {n: 0 for n in range(1, 21)}
        for pid, amount, _ in invoices:
            expected[project_client[pid]] += amount
        _, rows = run(reference(self.items['W03E07']), self.practice)
        self.assertEqual({r[0]: r[2] for r in rows}, expected)
        _, rows = run(reference(self.items['W03E10']), self.practice)
        self.assertEqual({r[0]: r[3] for r in rows}, expected)
        self.assertEqual(sum(r[3] for r in rows), sum(i[1] for i in invoices))

    def test_weighted_rate_and_zero_denominator(self):
        _, rows = run(reference(self.items['W06E04']), self.variation)
        # Boundary Demo: 600 actual / 1100 target, not average(100%,50%).
        self.assertEqual(next(r for r in rows if r[0] == 101), (101, 1100, 600, 54.5))
        _, rows = run(reference(self.items['W06E10']), self.variation)
        self.assertEqual(next(r for r in rows if r[0] == 21), (21, 0, 0, None))

    def test_capstone_supplement_reconciles_to_june_wave_source(self):
        columns, rows = run((ROOT / 'solutions' / 'capstone.sql').read_text(), self.practice)
        self.assertEqual(len(rows), 20)
        with closing(sqlite3.connect(self.practice)) as db:
            source = db.execute("SELECT COUNT(*),SUM(completes_target),SUM(completes_actual) FROM survey_waves WHERE close_date>='2025-06-01' AND close_date<'2025-07-01'").fetchone()
        self.assertEqual(tuple(sum(row[index] for row in rows) for index in (2, 3, 4)), source)

    def test_rejects_join_inflation_and_distinct_shortcut(self):
        bad = '''SELECT p.project_id,COALESCE(SUM(i.amount),0) AS invoiced_eur,
                 COUNT(DISTINCT pm.market_id) AS market_count FROM projects p
                 LEFT JOIN invoices i ON i.project_id=p.project_id
                 LEFT JOIN project_markets pm ON pm.project_id=p.project_id
                 GROUP BY p.project_id'''
        for sql in (bad, bad.replace('SUM(i.amount)', 'SUM(DISTINCT i.amount)')):
            ok, _ = compare(self.items['W03E09'], sql, self.variation)
            self.assertFalse(ok)

    def test_accepts_different_valid_sql(self):
        alternative = "SELECT client_id, client_name, sector FROM clients WHERE client_id <= 5 ORDER BY client_id ASC"
        self.assertTrue(compare(self.items['W01E01'], alternative, self.practice)[0])

    def test_order_aliases_and_null_errors_are_detected(self):
        base = reference(self.items['W01E03'])
        self.assertFalse(compare(self.items['W01E03'], base.replace('ORDER BY market_id', 'ORDER BY market_id DESC'), self.practice)[0])
        self.assertFalse(compare(self.items['W01E06'], 'SELECT project_id,status FROM projects WHERE actual_end_date = NULL', self.practice)[0])
        self.assertFalse(compare(self.items['W03E05'], reference(self.items['W03E05']).replace('COUNT(i.invoice_id)', 'COUNT(*)'), self.practice)[0])
        self.assertFalse(compare(self.items['W02E05'], 'SELECT status, COUNT(*) AS wrong_alias FROM projects GROUP BY status', self.practice)[0])

    def test_unordered_exercise_accepts_reverse_order(self):
        query = reference(self.items['W01E04']).rstrip().rstrip(';') + ' ORDER BY project_id DESC'
        self.assertTrue(compare(self.items['W01E04'], query, self.practice)[0])

    def test_variation_catches_hardcoded_values(self):
        _, rows = run(reference(self.items['W02E01']), self.practice)
        sql = 'SELECT ' + ','.join(f'{value} AS {alias}' for value, alias in zip(rows[0], self.items['W02E01']['columns']))
        result = check_answer('W02E01', sql, [('Practice', self.practice), ('Variation', self.variation)])
        self.assertTrue(result['tests'][0]['passed'])
        self.assertFalse(result['tests'][1]['passed'])

    def test_readonly_runner_blocks_writes_and_multiple_statements(self):
        for sql in ('DELETE FROM projects', 'DROP TABLE clients', 'PRAGMA user_version=5',
                    "ATTACH DATABASE ':memory:' AS extra", 'SELECT 1; SELECT 2;',
                    "SELECT load_extension('missing')"):
            with self.subTest(sql=sql), self.assertRaises((sqlite3.Error, ValueError)):
                run(sql, self.practice)
        self.assertEqual(run('SELECT COUNT(*) FROM projects', self.practice)[1], [(100,)])

    def test_fanout_and_equal_invoice_traps_are_present(self):
        with closing(sqlite3.connect(self.variation)) as db:
            raw = db.execute('SELECT SUM(i.amount) FROM invoices i JOIN project_markets pm ON pm.project_id=i.project_id WHERE i.project_id=101').fetchone()[0]
            real = db.execute('SELECT SUM(amount) FROM invoices WHERE project_id=101').fetchone()[0]
            distinct = db.execute('SELECT SUM(DISTINCT amount) FROM invoices WHERE project_id=101').fetchone()[0]
            self.assertEqual((raw, real, distinct), (40000, 20000, 10000))

    def test_http_classroom_routes_in_memory(self):
        # Exercise the actual HTTP parser/handler without needing socket privileges.
        import app
        old_db = app.DB_PATH
        app.DB_PATH = self.practice
        handler = handler_for(self.variation)

        class MemorySocket:
            def __init__(self, raw):
                self.input = io.BytesIO(raw)
                self.output = bytearray()

            def makefile(self, *args):
                return self.input

            def sendall(self, data):
                self.output.extend(data)

        def request(path, body=None, token=None):
            payload = json.dumps(body).encode() if body is not None else b''
            headers = [f"{'POST' if body is not None else 'GET'} {path} HTTP/1.0",
                       'Host: 127.0.0.1', f'Content-Length: {len(payload)}']
            if token:
                headers.append('X-Classroom-Token: ' + token)
            wire = ('\r\n'.join(headers) + '\r\n\r\n').encode() + payload
            socket = MemorySocket(wire)
            handler(socket, ('127.0.0.1', 0), None)
            header, data = bytes(socket.output).split(b'\r\n\r\n', 1)
            return int(header.split()[1]), data

        try:
            status, html = request('/')
            self.assertEqual(status, 200)
            token = re.search("const token='([^']+)'", html.decode())[1]
            status, data = request('/api/course')
            self.assertEqual(status, 200)
            course = json.loads(data)
            self.assertEqual(len(course['exercises']), 60)
            self.assertNotIn('sql', course['exercises'][0])
            self.assertEqual(len(json.loads(request('/api/schema')[1])['rows']), 6)
            status, data = request('/api/tables')
            self.assertEqual(status, 200)
            tables = json.loads(data)
            self.assertEqual(set(tables), set(app.SOURCE_TABLES))
            with closing(sqlite3.connect(self.practice)) as db:
                for name, (_, ordering) in app.SOURCE_TABLES.items():
                    cursor = db.execute(f'SELECT * FROM {name} ORDER BY {ordering}')
                    self.assertEqual(tables[name]['columns'], [c[0] for c in cursor.description])
                    # Every row and column, including NULLs, not a LIMIT preview.
                    self.assertEqual(tables[name]['rows'], [list(row) for row in cursor])
            self.assertEqual(len(tables['clients']['rows']), 20)
            self.assertEqual(len(tables['projects']['rows']), 100)
            self.assertEqual(len(tables['invoices']['rows']), 300)
            self.assertNotIn(21, [row[0] for row in tables['clients']['rows']])
            self.assertIn('Final briefing', json.loads(request('/api/notes')[1]))
            status, data = request('/api/run', {'sql': 'SELECT COUNT(*) AS n FROM projects'}, token)
            self.assertEqual(status, 200)
            self.assertEqual(json.loads(data)['rows'], [[100]])
            status, data = request('/api/check', {'id': 'W01E01', 'sql': reference(self.items['W01E01'])}, token)
            self.assertEqual(status, 200)
            self.assertTrue(json.loads(data)['passed'])
            self.assertEqual(request('/api/run', {'sql': 'SELECT 1'})[0], 403)
            self.assertEqual(request('/api/run', {'sql': 'DELETE FROM projects'}, token)[0], 400)
            self.assertEqual(request('/api/run', {'sql': 'broken'}, token)[0], 400)
            self.assertEqual(request('/api/check', {'id': 'unknown', 'sql': 'SELECT 1'}, token)[0], 400)
            for path in ('/solutions/week01.sql', '/../../schema.sql'):
                self.assertEqual(request(path)[0], 404)
        finally:
            app.DB_PATH = old_db

    def test_live_local_http(self):
        try:
            server = ThreadingHTTPServer(('127.0.0.1', 0), handler_for(self.variation))
        except PermissionError:
            self.skipTest('Environment prohibits binding sockets; HTTP handlers tested in memory.')
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            url = f'http://127.0.0.1:{server.server_port}'
            self.assertEqual(len(json.load(urlopen(url + '/api/course', timeout=5))['exercises']), 60)
        finally:
            server.shutdown()
            server.server_close()
            worker.join(timeout=5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
