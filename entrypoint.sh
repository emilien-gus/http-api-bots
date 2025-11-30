#!/bin/sh
set -e

python -m bot.infrastructure.recreate_database_postgres
exec python -m bot