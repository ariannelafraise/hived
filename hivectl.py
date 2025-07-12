#!/usr/bin/python

import argparse

from config import GeneralConfig, PathConfig
from core.plugin import Plugin
from utils.import_utils import dynamic_import

def handle_command(arguments: argparse.Namespace):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hivectl')
    parser.set_defaults(func=handle_command)
    subparsers = parser.add_subparsers(dest='plugin')

    plugins = dynamic_import(Plugin, PathConfig.PLUGINS_DIR)
    [plugin.init_args_parser(subparsers) for plugin in plugins]

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-v', '--version', help='View currently installed version.', action='version',
                       version=f"v{GeneralConfig.VERSION}")

    args = parser.parse_args()
    args.func(args)
