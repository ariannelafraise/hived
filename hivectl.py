import argparse

from core.external import import_plugins
from __version__ import __version__

def handle_command(arguments: argparse.Namespace):
    """
    Handling command of the args parser.
    """
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hivectl")
    parser.set_defaults(func=handle_command)
    subparsers = parser.add_subparsers(dest="plugin")

    plugins = import_plugins()
    [plugin.init_args_parser(subparsers) for plugin in plugins]

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-v",
        "--version",
        help="View currently installed version.",
        action="version",
        version=f"v{__version__}",
    )

    args = parser.parse_args()
    args.func(args)
