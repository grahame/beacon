import argparse
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
    uvicorn.run("beacon.server:app", port=5961, log_level="info", reload=True)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("process", help="Scan for events and notify users")
    subparsers.add_parser("serve", help="Serve HTTP requests")

    args = parser.parse_args()
    command_funcs = {"process": process, "serve": serve}
    command_funcs[args.command]()
