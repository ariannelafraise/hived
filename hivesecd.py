import argparse
import traceback

import core.logger as logger
from core.audispd_listener import AudispdListener
from core.external import import_event_handlers
from __version__ import __version__

def start_daemon():
    """
    Starts the daemon by creating the listener and loading all
    the audit event handlers into it as observers.
    """
    logger.info("HiveSec has been started", "HiveSec")
    try:
        listener = AudispdListener()
        handlers = import_event_handlers()
        for h in handlers:
            listener.add_observer(h)
        listener.listen()
    except Exception as _:
        logger.error_traceback(
            f"something went wrong: {traceback.format_exc()} --- End of Traceback ---"
        )


def handle_command(arguments: argparse.Namespace):
    """
    Handling command for the args parser
    """
    if arguments.start:
        start_daemon()


if __name__ == "__main__":
    #  Initialize the args parser and handle user input
    parser = argparse.ArgumentParser(description="HiveSec")
    parser.set_defaults(func=handle_command)
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-v",
        "--version",
        help="View currently installed version.",
        action="version",
        version=f"v{__version__}",
    )
    group.add_argument(
        "-s", "--start", help="Start the HiveSec daemon", action="store_true"
    )

    args = parser.parse_args()
    args.func(args)
