"""Local browser classroom. Launch with python3 scripts/app.py."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import secrets
import sqlite3
import sys
import tempfile
import threading
import webbrowser

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'checks'))
from check import catalog, check_answer, make_variation
from query import DB_PATH, run
from seed import build

SOURCE_TABLES = {
    'clients': ('one client', 'client_id'),
    'projects': ('one project', 'project_id'),
    'markets': ('one country market', 'market_id'),
    'project_markets': ('one project-market assignment', 'project_id, market_id'),
    'invoices': ('one invoice', 'invoice_id'),
    'survey_waves': ('one survey wave within a project', 'wave_id'),
}


def source_tables():
    """All columns and rows of the practice tables, ordered by their primary keys."""
    tables = {}
    # Identifiers come only from this fixed dictionary, never from a request.
    for name, (grain, ordering) in SOURCE_TABLES.items():
        columns, rows = run(f'SELECT * FROM {name} ORDER BY {ordering}', DB_PATH)
        tables[name] = {'columns': columns, 'rows': rows, 'grain': grain}
    return tables


def handler_for(variation):
    token = secrets.token_urlsafe(32)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def reply(self, status, body, content_type='application/json; charset=utf-8'):
            payload = body.encode('utf-8') if isinstance(body, str) else json.dumps(body).encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(payload)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self):
            if self.path == '/':
                html = (ROOT / 'scripts' / 'classroom.html').read_text()
                self.reply(200, html.replace('__TOKEN__', token), 'text/html; charset=utf-8')
            elif self.path == '/api/course':
                self.reply(200, {'exercises': catalog(),
                                'lessons': json.loads((ROOT / 'exercises' / 'lessons.json').read_text())})
            elif self.path == '/api/schema':
                columns, rows = run("SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name")
                self.reply(200, {'columns': columns, 'rows': rows})
            elif self.path == '/api/tables':
                try:
                    self.reply(200, source_tables())
                except (ValueError, sqlite3.Error) as error:
                    self.reply(500, {'error': str(error)})
            elif self.path == '/api/notes':
                self.reply(200, {name: (ROOT / file).read_text() for name, file in [
                    ('Learning plan', 'CURRICULUM.md'),
                    ('Final briefing', 'capstone.md'), ('Glossary', 'glossary.md')]})
            else:
                self.reply(404, {'error': 'Page not found.'})

        def do_POST(self):
            # The token is available only to this local page, not cross-origin forms.
            if self.headers.get('X-Classroom-Token') != token:
                self.reply(403, {'error': 'Reload the classroom page and try again.'})
                return
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if length <= 0 or length > 50000:
                    raise ValueError('Enter a query shorter than 50,000 bytes.')
                data = json.loads(self.rfile.read(length))
                if not isinstance(data, dict) or not isinstance(data.get('sql'), str):
                    raise ValueError('A SQL query is required.')
                if self.path == '/api/run':
                    columns, rows = run(data['sql'])
                    self.reply(200, {'columns': columns, 'rows': rows})
                elif self.path == '/api/check':
                    self.reply(200, check_answer(str(data.get('id', '')), data['sql'],
                               [('Practice', DB_PATH), ('Variation', variation)]))
                else:
                    self.reply(404, {'error': 'Action not found.'})
            except (ValueError, sqlite3.Error, TypeError) as error:
                self.reply(400, {'error': str(error)})

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    if sys.version_info < (3, 10):
        parser.error('Python 3.10 or newer is required.')
    if sqlite3.sqlite_version_info < (3, 25, 0):
        parser.error('SQLite 3.25+ is required for window functions; use a newer Python 3.')
    if not DB_PATH.exists():
        build()
    with tempfile.TemporaryDirectory(prefix='sql-classroom-') as folder:
        variation = make_variation(Path(folder) / 'variation.sqlite3')
        try:
            server = ThreadingHTTPServer(('127.0.0.1', args.port), handler_for(variation))
        except OSError as error:
            parser.exit(1, f'Could not start: {error}. Try --port 8766.\n')
        url = f'http://127.0.0.1:{server.server_port}'
        print(f'SQL classroom: {url}\nKeep this terminal open. Press Ctrl+C to stop.', flush=True)
        if not args.no_browser:
            threading.Timer(0.5, lambda: webbrowser.open(url)).start()
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print('\nClassroom stopped. Your browser keeps your saved drafts.')
        finally:
            server.server_close()


if __name__ == '__main__':
    main()
