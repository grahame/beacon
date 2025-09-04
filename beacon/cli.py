import argparse
import uvicorn
import asyncio

from beacon.db import create_db_and_tables

DATA_DIR = "data/emergencywa"


def process():
    from .analysis import determine_events
    from .api import get_latest_data

    state = get_latest_data()
    determine_events(state)


def serve():
    uvicorn.run("beacon.server:app", port=5961, log_level="info")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("process", help="Scan for events and notify users")
    subparsers.add_parser("serve", help="Serve HTTP requests")

    asyncio.run(create_db_and_tables())

    args = parser.parse_args()
    command_funcs = {"process": process, "serve": serve}
    command_funcs[args.command]()
