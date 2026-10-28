"""Create a deterministic fictional training database. Python 3.10+; no packages."""
from datetime import date, timedelta
from pathlib import Path
import random
import sqlite3
from contextlib import closing

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / 'data' / 'research_pm.sqlite3'
AS_OF = date(2025, 7, 1)


def build(path=DB_PATH, seed=42):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Build separately so a failed seed does not destroy an existing database.
    temporary = path.with_suffix('.building')
    temporary.unlink(missing_ok=True)
    rng = random.Random(seed)
    with closing(sqlite3.connect(temporary)) as db:
        db.executescript((ROOT / 'schema.sql').read_text())
        names = ['Amber', 'Birch', 'Cedar', 'Dawn', 'Elm', 'Fern', 'Grove',
                 'Harbor', 'Iris', 'Juniper', 'Kite', 'Linden', 'Meadow',
                 'Northstar', 'Orchard', 'Pebble', 'Quartz', 'Reed', 'Spruce', 'Willow']
        sectors = ['Retail', 'Technology', 'Finance', 'Consumer goods', 'Healthcare']
        for n, name in enumerate(names, 1):
            db.execute('INSERT INTO clients VALUES (?, ?, ?, ?)',
                       (n, f'{name} Insights Demo', sectors[(n-1) % 5],
                        ['Central Europe', 'Western Europe', 'Nordics'][(n-1) % 3]))
        markets = ['Czechia', 'Slovakia', 'Poland', 'Germany', 'Austria',
                   'France', 'United Kingdom', 'Sweden', 'Denmark', 'Netherlands']
        for n, name in enumerate(markets, 1):
            db.execute('INSERT INTO markets VALUES (?, ?, ?)',
                       (n, name, 'Central Europe' if n <= 5 else 'Western / Northern Europe'))
        invoice_id = wave_id = 0
        for pid in range(1, 101):
            # Clients 19 and 20 deliberately have no projects.
            client = (pid - 1) % 18 + 1
            start = date(2025, 1, 1) + timedelta(days=(pid * 7) % 165)
            planned = start + timedelta(days=rng.randint(35, 70))
            if pid % 13 == 0:
                status, actual = 'cancelled', None
            elif pid % 5 == 0 or planned >= AS_OF:
                status, actual = 'active', None
            else:
                status = 'completed'
                actual = min(planned + timedelta(days=[-5, 0, 8, 14][pid % 4]), AS_OF - timedelta(days=1))
            budget = rng.randrange(10, 101) * 1000
            db.execute('INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                       (pid, client, ['Brand tracking', 'Customer experience',
                        'Concept test', 'Usage study'][pid % 4], start.isoformat(),
                        planned.isoformat(), actual.isoformat() if actual else None, status, budget))
            # Some projects lack market assignments: a deliberate quality issue.
            if pid % 17:
                for market in rng.sample(range(1, 11), 1 + pid % 3):
                    db.execute('INSERT INTO project_markets VALUES (?, ?)', (pid, market))
            # 90 projects with 3 or 4 invoices: exactly 300 in total.
            if pid % 10:
                count = 4 if pid % 3 == 0 else 3
                for part in range(count):
                    invoice_id += 1
                    day = min(start + timedelta(days=part * 12), AS_OF - timedelta(days=1))
                    amount = budget // count + (part - 1) * 100
                    db.execute('INSERT INTO invoices VALUES (?, ?, ?, ?, ?)',
                               (invoice_id, pid, day.isoformat(), amount,
                                int((pid + part) % 4 != 0)))
            # Exactly 200 successive waves, all launched before the reporting date.
            for number in (1, 2):
                wave_id += 1
                launch = start + timedelta(days=(number - 1) * 14)
                close = launch + timedelta(days=12)
                close = close if close < AS_OF else None
                target = rng.choice([250, 500, 800, 1000])
                completes = int(target * rng.choice([0.6, 0.8, 1, 1.1, 1.2]))
                if close is None:
                    completes = int(target * 0.4)
                db.execute('INSERT INTO survey_waves VALUES (?, ?, ?, ?, ?, ?, ?)',
                           (wave_id, pid, number, launch.isoformat(),
                            close.isoformat() if close else None, target, completes))
        assert not db.execute('PRAGMA foreign_key_check').fetchall()
        db.commit()
    temporary.replace(path)
    return path


if __name__ == '__main__':
    path = build()
    print(f'Created {path}\nFictional data; reporting date: {AS_OF}; all amounts EUR.')
