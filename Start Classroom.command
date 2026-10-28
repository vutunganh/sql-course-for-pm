#!/bin/bash
# Double-click on macOS, or use python3 scripts/app.py from the course folder.
cd -- "$(dirname -- "$0")" || exit 1
if ! command -v python3 >/dev/null 2>&1; then
    echo 'Python 3 is required. Install Python 3.10 or newer, then try again.'
    read -r -p 'Press Return to close. '
    exit 1
fi
python3 scripts/app.py
