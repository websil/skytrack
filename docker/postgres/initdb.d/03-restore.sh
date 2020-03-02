#!/bin/bash

set -e

if [ -f /backup/backup.dump ]; then
  echo "restore database: $POSTGRES_DB"
  pg_restore --username $POSTGRES_USER --no-owner -d $POSTGRES_DB /backup/backup.dump
fi
