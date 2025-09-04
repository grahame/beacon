import argparse
import uvicorn

from beacon.db import create_db_and_tables, get_parish_subscriptions

DATA_DIR = "data/emergencywa"


def process():
    from .analysis import determine_events
    from .api import get_latest_data

    state = get_latest_data()
    subscriptions = get_parish_subscriptions()
    messages = determine_events(state)
    messages.dispatch(subscriptions)


def serve():
    uvicorn.run("beacon.server:app", port=5961, log_level="info")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("process", help="Scan for events and notify users")
    subparsers.add_parser("serve", help="Serve HTTP requests")

    args = parser.parse_args()
    command_funcs = {"process": process, "serve": serve}
    command_funcs[args.command]()
