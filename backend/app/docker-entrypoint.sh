#!/bin/sh

set -e

# activate our virtual environment here
. /opt/pysetup/.venv/bin/activate

# Let the DB start
python ./backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python ./initial_data.py

# Evaluating passed command:
exec "$@"