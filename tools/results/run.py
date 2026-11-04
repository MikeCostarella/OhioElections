"""Refresh every results file: the Secretary of State feed (sos.py) for all 88 counties' statewide and
district races, then each county Board module for its local races and issues.

Refresh every county's results file. Each county module fetches its Board's report itself;
a county whose site refuses scripted downloads is skipped with a message, and can be run by hand
with --pdf / --text (see README).

    python run.py            # every county listed below
    python run.py trumbull   # one county
"""
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# "sos" first: it writes every county the Board modules below do not cover, plus results/state/.
COUNTIES = ["sos", "trumbull", "mahoning"]

# Exit codes from a county module: 0 written, 1 written but with unmatched titles (fails the run so
# the map gets fixed), 2 the Board's report could not be downloaded (skipped: the previous file stands).
bad = 0
for m in sys.argv[1:] or COUNTIES:
    rc = importlib.import_module(m).main([])
    if rc == 1:
        bad += 1
    elif rc == 2:
        print(f"{m}: skipped (report not downloadable from here)")
sys.exit(1 if bad else 0)
