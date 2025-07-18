import argparse
import datetime
import json
import os


def update():
    from .emergencywa import get_latest_data

    timestamp = int(1000 * datetime.datetime.now(datetime.timezone.utc).timestamp())
    pfx = f"data/emergencywa/{timestamp}"
    tmpf = pfx + ".tmp"
    outf = pfx + ".json"
    with open(tmpf, "w") as fd:
        json.dump(get_latest_data(), fd)
        os.rename(tmpf, outf)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("update", help="Get latest data from Emergency WA")

    args = parser.parse_args()
    if args.command == "update":
        update()
