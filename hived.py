#!/usr/bin/python

import argparse
import traceback

from config.config import GeneralConfig
from audispd_listener import AudispdListener

def start_daemon():
    try:
        AudispdListener().listen()
    except:
        print(traceback.format_exc())

def handle_command(arguments: argparse.Namespace):
    if arguments.start:
        start_daemon()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Hived')
    parser.set_defaults(func=handle_command)
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-v', '--version', help='View currently installed version.', action='version',
                       version=f"v{GeneralConfig.VERSION}")
    group.add_argument('-s', '--start', help="Start the hived daemon", action='store_true')

    args = parser.parse_args()
    args.func(args)
