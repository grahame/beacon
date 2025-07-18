import argparse
import datetime
import json
import os
from glob import glob
from itertools import pairwise

DATA_DIR = "data/emergencywa"


def update():
    from .api import get_latest_data

    timestamp = int(1000 * datetime.datetime.now(datetime.timezone.utc).timestamp())
    pfx = f"{DATA_DIR}/{timestamp}"
    tmpf = pfx + ".tmp"
    outf = pfx + ".json"
    with open(tmpf, "w") as fd:
        json.dump(get_latest_data(), fd)
        os.rename(tmpf, outf)


def events():
    from .analysis import determine_events

    for from_file, to_file in pairwise(sorted(glob(f"{DATA_DIR}/*.json"))):
        with open(from_file, "r") as fd:
            from_data = json.load(fd)
        with open(to_file, "r") as fd:
            to_data = json.load(fd)
        determine_events(from_data, to_data)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("update", help="Get latest data from Emergency WA")
    subparsers.add_parser("events", help="List all events")

    args = parser.parse_args()
    if args.command == "update":
        update()
    elif args.command == "events":
        events()
