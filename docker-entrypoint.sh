#!/bin/bash

alembic upgrade head

while true; do
    beacon serve
    sleep 60
done
