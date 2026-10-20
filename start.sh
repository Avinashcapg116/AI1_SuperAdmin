#!/bin/bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "=========================================================="
echo "🇮🇳  Ai1 Super App - India's First Modular Super App"
echo "=========================================================="

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    venv/bin/pip install -r requirements.txt
fi

echo "Running verification test suite..."
PYTHONPATH=. venv/bin/pytest tests/test_all_modules.py -q

echo "=========================================================="
echo "🚀 Starting Ai1 Super App on http://localhost:8000"
echo "📖 Swagger API Docs available at http://localhost:8000/docs"
echo "=========================================================="

export PYTHONPATH=.
exec venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
