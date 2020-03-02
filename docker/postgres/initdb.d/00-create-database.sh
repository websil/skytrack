#!/bin/bash

set -e

# Load extensions into both template1, $POSTGRES_DB and $POSTGRES_TEST_DB
if [[ -z $(psql -p 5432 -U $POSTGRES_USER postgres -tAc "SELECT 1 from pg_database WHERE datname='$POSTGRES_DB'") ]]; then
  echo "Creating database: $DB"
  psql=(psql -v ON_ERROR_STOP=1)

  "${psql[@]}" --username $POSTGRES_USER <<-EOSQL
      CREATE DATABASE "$DB" TEMPLATE template1;
EOSQL
else
  echo "Database ${DB} already exists"
fi
