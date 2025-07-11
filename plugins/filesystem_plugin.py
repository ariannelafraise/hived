import argparse
import re
import sys
import subprocess

from core.plugin import Plugin
from config import PathConfig

VERSION = "0.0.2"
PLUGIN_NAME = "FileSystem"

def _check_path_arg(value: str) -> str:
    """
    TODO: better validation, more options of valid paths (relative, absolute, ~/...)
    :param value:
    :return
    """
    valid = re.search('^(/[^/\0]+)+/?$', value)
    if not valid:
        raise argparse.ArgumentTypeError(value  + " is not a valid path")
    return value

def _add_rule(rule: str):
    separator = '\n'
    with open(PathConfig.RULES_FILE_PATH, 'r') as rules_file:
        rules = rules_file.read()
        if rule in rules:
            print("rule already exists.")
            sys.exit(1)

    with open(PathConfig.RULES_FILE_PATH, 'a') as rules_file:
        rules_file.write(separator + rule)
    subprocess.run(['augenrules', '--load'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def _clear_rules():
    with open(PathConfig.RULES_FILE_PATH, 'w') as rules_file:
        rules_file.write('')
    subprocess.run(['auditctl', '-D'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    subprocess.run(['augenrules', '--load'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


class FileSystemPlugin(Plugin):
    @staticmethod
    def init_args_parser(subparser):
        parser = subparser.add_parser(PLUGIN_NAME.lower())
        parser.set_defaults(func=FileSystemPlugin.handle_command)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-v', '--version', help='View currently installed version.', action='version', version=f"{PLUGIN_NAME} v{VERSION}")
        group.add_argument('-af', '--add-file', type=_check_path_arg, help='Add a honeypot file rule.')
        group.add_argument('-ad', '--add-directory', type=_check_path_arg, help='Add a honeypot directory rule.')
        group.add_argument('-r', '--remove', type=_check_path_arg, help='Remove a honeypot filesystem rule.')
        group.add_argument('-c', '--clear', help='Clear the honeypot file rules.', action="store_true")

    @staticmethod
    def handle_command(args: argparse.Namespace):
        if args.add_file:
            _add_rule(f"-a always,exit -F arch=b64 -F path={args.add} -F perm=rw -k filesystem")
        if args.add_directory:
            _add_rule(f"-a always,exit -F arch=b64 -F dir={args.add_directory} -F perm=rw -F key=filesystem")
        if args.clear:
            _clear_rules()
