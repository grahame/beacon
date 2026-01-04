import argparse
import json
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
    uvicorn.run("beacon.server:app", port=5961, log_level="info", reload=True, reload_dirs=["./beacon"])


def sync_boundaries(path: str):
    from sqlalchemy import delete, select
    from sqlalchemy.orm import Session

    from beacon.db import Parish, engine

    with open(path) as f:
        geojson = json.load(f)

    features = geojson["features"]
    parish_data = {}
    for feature in features:
        name = feature["properties"]["parish"]
        parish_data[name] = {"properties": feature["properties"], "geometry": feature["geometry"]}

    with Session(engine) as session:
        existing_parishes = {p.name: p for p in session.execute(select(Parish)).scalars()}

        existing_names = set(existing_parishes.keys())
        new_names = set(parish_data.keys())

        # Remove parishes that no longer exist (cascade will remove subscriptions)
        to_remove = existing_names - new_names
        if to_remove:
            session.execute(delete(Parish).where(Parish.name.in_(to_remove)))
            print(f"Removed {len(to_remove)} parishes: {', '.join(sorted(to_remove))}")

        # Update existing parishes
        to_update = existing_names & new_names
        for name in to_update:
            existing_parishes[name].properties = parish_data[name]["properties"]
            existing_parishes[name].geometry = parish_data[name]["geometry"]
        if to_update:
            print(f"Updated {len(to_update)} parishes")

        # Add new parishes
        to_add = new_names - existing_names
        for name in to_add:
            session.add(Parish(name=name, properties=parish_data[name]["properties"], geometry=parish_data[name]["geometry"]))
        if to_add:
            print(f"Added {len(to_add)} parishes: {', '.join(sorted(to_add))}")

        session.commit()


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("process", help="Scan for events and notify users")
    subparsers.add_parser("serve", help="Serve HTTP requests")
    sync_parser = subparsers.add_parser("sync_boundaries", help="Sync parish boundaries from GeoJSON file")
    sync_parser.add_argument("path", help="Path to parish_boundaries.json GeoJSON file")

    args = parser.parse_args()
    command_funcs = {"process": process, "serve": serve, "sync_boundaries": lambda: sync_boundaries(args.path)}
    command_funcs[args.command]()


if __name__ == '__main__':
    main()
