#! /bin/bash
set -e

# Let the DB start
poetry run python ./app/backend_pre_start.py

# Run migrations
poetry run alembic upgrade head

# Create initial data in DB
poetry run python ./app/initial_data.py

exec "$@"
