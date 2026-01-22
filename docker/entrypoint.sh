#!/bin/sh
set -e

echo "Starting application..."

if [ -n "${DB_HOST}" ] && [ -n "${DB_PORT}" ]; then
  echo "Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT}..."
  until python - <<EOF
import socket
s = socket.socket()
s.settimeout(1)
s.connect(("${DB_HOST}", int("${DB_PORT}")))
s.close()
EOF
  do
    sleep 1
  done
  echo "PostgreSQL is available."
fi

if [ "${RUN_MIGRATIONS}" = "1" ]; then
  echo "Running Alembic migrations..."
  alembic upgrade head
fi

exec "$@"
