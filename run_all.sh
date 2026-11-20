#!/usr/bin/env bash
# Full pipeline: create venv, install deps, run the agent team end to end.
# Downloads real data at run time (SEC EDGAR company facts + Nasdaq price),
# so no large raw files need to be committed.
set -e
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
.venv/bin/pip install -q -r requirements.txt
.venv/bin/python src/run.py
echo "Done. See results/results.json, results/report.md and REPORT.md"
