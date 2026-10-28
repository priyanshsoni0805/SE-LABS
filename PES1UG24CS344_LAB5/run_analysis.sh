#!/usr/bin/env bash
# Generates the BEFORE/AFTER reports required by Lab 5.
# Usage:  bash run_analysis.sh        (run from the repo root)
# Author: Priyansh Soni (PES1UG24CS344)
set -u
python3 -m venv venv 2>/dev/null || true
# shellcheck disable=SC1091
source venv/bin/activate
pip install -q pylint bandit flake8

mkdir -p reports/before reports/after
# BEFORE = original starter code (kept as smart_home_original.py)
pylint smart_home_original.py > reports/before/pylint_report.txt
bandit -r smart_home_original.py > reports/before/bandit_report.txt
flake8 smart_home_original.py > reports/before/flake8_report.txt
# AFTER = fixed code
pylint smart_home.py > reports/after/pylint_report.txt
bandit -r smart_home.py > reports/after/bandit_report.txt
flake8 smart_home.py > reports/after/flake8_report.txt

echo "== BEFORE =="; tail -n 3 reports/before/pylint_report.txt
echo "== AFTER  =="; tail -n 3 reports/after/pylint_report.txt
echo "flake8 after: $(wc -l < reports/after/flake8_report.txt) issues"
grep -E "Total issues|Issue:" reports/after/bandit_report.txt || true
