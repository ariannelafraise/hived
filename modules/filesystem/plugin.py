import argparse
import re

from core.plugin import Plugin

VERSION = "0.0.2"
PLUGIN_NAME = "FileSystem"


def _check_path_arg(value: str) -> str:
    """
    TODO: better validation, more options of valid paths (relative, absolute, ~/...)
    :param value:
    :return
    """
    valid = re.search("^(/[^/\0]+)+/?$", value)
    if not valid:
        raise argparse.ArgumentTypeError(value + " is not a valid path")
    return value


class FileSystemPlugin(Plugin):
    def init_args_parser(self, subparser: argparse._SubParsersAction):
        parser = subparser.add_parser(PLUGIN_NAME.lower())
        parser.set_defaults(func=self.handle_command)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "-v",
            "--version",
            help="View currently installed version.",
            action="version",
            version=f"{PLUGIN_NAME} v{VERSION}",
        )
        group.add_argument(
            "-af", "--add-file", type=_check_path_arg, help="Add a honeypot file rule."
        )
        group.add_argument(
            "-ad",
            "--add-directory",
            type=_check_path_arg,
            help="Add a honeypot directory rule.",
        )
        group.add_argument(
            "-r",
            "--remove",
            type=_check_path_arg,
            help="Remove a honeypot filesystem rule.",
        )
        group.add_argument(
            "-c", "--clear", help="Clear the honeypot file rules.", action="store_true"
        )

    def handle_command(self, args: argparse.Namespace) -> None:
        if args.add_file:
            self._add_rule(
                f"-a always,exit -F arch=b64 -F path={args.add} -F perm=rw -k filesystem"
            )
        if args.add_directory:
            self._add_rule(
                f"-a always,exit -F arch=b64 -F dir={args.add_directory} -F perm=rw -F key=filesystem"
            )
        if args.clear:
            self._clear_rules()
