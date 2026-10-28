"""Generate an instructor-only practice-result snapshot."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check import catalog, reference
from query import run

if __name__ == '__main__':
    results = {}
    for exercise in catalog():
        columns, rows = run(reference(exercise))
        results[exercise['id']] = {'columns': columns, 'rows': rows}
    target = ROOT / 'solutions' / 'expected_results.json'
    target.write_text(json.dumps(results, indent=2) + '\n')
    print(f'Exported expected results for {len(results)} exercises to {target}')
