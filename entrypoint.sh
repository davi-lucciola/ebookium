#!/bin/sh
set -e

RETRIES="${DB_HEALTHCHECK_RETRIES:-30}"
DELAY="${DB_HEALTHCHECK_DELAY:-2}"

# `psycopg` does not understand the SQLAlchemy driver suffix
# (`postgresql+psycopg://`). The URL is normalized only for the health check.
export PG_URL
PG_URL=$(echo "$APP_DATABASE_URL" | sed 's|^postgresql+[a-z0-9]*://|postgresql://|')

echo "🔍 Checking database connection..."
attempt=1
until python -c "import os, psycopg; conn = psycopg.connect(os.environ['PG_URL']); conn.execute('SELECT 1'); conn.close()"; do
  if [ "$attempt" -ge "$RETRIES" ]; then
    echo "❌ Database unavailable after $RETRIES attempts. Aborting." >&2
    exit 1
  fi
  echo "⏳ Database unavailable (attempt $attempt/$RETRIES). Retrying in ${DELAY}s..."
  attempt=$((attempt + 1))
  sleep "$DELAY"
done
echo "✅ Database is available."

echo "📦 Running migrations..."
alembic upgrade head
echo "✅ Migrations applied."

echo "🚀 Starting the application..."
exec "$@"
