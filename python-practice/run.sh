#!/bin/sh
set -eu

cd -- "$(dirname -- "$0")"

docker compose up -d --wait db

docker compose exec -T db sh -c \
  'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"' \
  < sql/schema.sql

docker compose exec -T db sh -c \
  'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"' \
  < sql/indexes.sql

. ./.env

export DB_HOST=127.0.0.1
export DB_PORT=5432
export DB_NAME="$POSTGRES_DB"
export DB_USER="$POSTGRES_USER"
export DB_PASSWORD="$POSTGRES_PASSWORD"

exec ./.venv/bin/python -m src.cli \
  --students data/students.json \
  --rooms data/rooms.json \
  "$@"
