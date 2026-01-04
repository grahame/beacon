#!/bin/bash

alembic upgrade head
uvicorn beacon.server.app:app --host 0.0.0.0 --port 8000 --reload

