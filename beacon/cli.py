import argparse
import json
import sys
import traceback
import uvicorn

from beacon.db import get_parish_subscriptions

DATA_DIR = "data/emergencywa"


def process():
    try:
        from .analysis import determine_events
        from .emwa import get_latest_data

        state = get_latest_data()
        subscriptions = get_parish_subscriptions()
        messages = determine_events(state)
        messages.dispatch(subscriptions)
    except Exception:
        from .mailgun import send_message

        traceback_string = traceback.format_exc()
        send_message(
            "frgrahame@bowland.au",
            "Processing failed with exception:\n\n{}".format(traceback_string),
            "Exception while processing data",
        )


def serve():
    uvicorn.run(
        "beacon.server:app",
        port=5961,
        log_level="info",
        reload=True,
        reload_dirs=["./beacon"],
    )


def clear_cache():
    from beacon.redis import get_redis

    redis_client = get_redis()
    redis_client.flushdb()
    print("Redis cache cleared", file=sys.stderr)


def sync_boundaries(path: str):
    from sqlalchemy import delete, select
    from sqlalchemy.orm import Session

    from beacon.db import Parish, engine

    with open(path) as f:
        geojson = json.load(f)
        parish_data = {}
        for feature in geojson["features"]:
            name = feature["properties"]["parish"]
            parish_data[name] = feature

    with Session(engine) as session:
        existing_parishes = {
            p.name: p for p in session.execute(select(Parish)).scalars()
        }

        existing_names = set(existing_parishes.keys())
        new_names = set(parish_data.keys())

        # Remove parishes that no longer exist (cascade will remove subscriptions)
        to_remove = existing_names - new_names
        if to_remove:
            session.execute(delete(Parish).where(Parish.name.in_(to_remove)))

        # Update existing parishes
        to_update = existing_names & new_names
        for name in to_update:
            parish = existing_parishes[name]
            if parish.geojson != parish_data[name]:
                parish.geojson = parish_data[name]
                session.add(parish)

        # Add new parishes
        to_add = new_names - existing_names
        for name in to_add:
            session.add(Parish(name=name, geojson=parish_data[name]))

        session.commit()


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("process", help="Scan for events and notify users")
    subparsers.add_parser("serve", help="Serve HTTP requests")
    subparsers.add_parser("clear_cache", help="Clear the Redis cache")
    sync_parser = subparsers.add_parser(
        "sync_boundaries", help="Sync parish boundaries from GeoJSON file"
    )
    sync_parser.add_argument("path", help="Path to parish_boundaries.json GeoJSON file")

    args = parser.parse_args()
    command_funcs = {
        "process": process,
        "serve": serve,
        "clear_cache": clear_cache,
        "sync_boundaries": lambda: sync_boundaries(args.path),
    }
    command_funcs[args.command]()


if __name__ == "__main__":
    main()
