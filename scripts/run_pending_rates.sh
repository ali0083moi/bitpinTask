#!/bin/bash
cd "$(dirname "$0")/.."
source venv/bin/activate
python manage.py process_pending_rates 