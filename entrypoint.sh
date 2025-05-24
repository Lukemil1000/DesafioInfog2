#!/bin/sh

# Execute migrations
alembic upgrade head

# Start application
uvicorn DesafioInfog2.main:app --host 0.0.0.0 --port 8000

