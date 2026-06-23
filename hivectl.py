import argparse
from pathlib import Path

from core.external import import_plugins
from __version__ import __version__


def absolute_directory(path: str) -> Path:
    """
    Validate that the given path is an absolute path to an existing directory.
    """
    p = Path(path)

    if not p.is_absolute():
        raise argparse.ArgumentTypeError("must be an absolute path")

    if not p.exists():
        raise argparse.ArgumentTypeError("directory does not exist")

    if not p.is_dir():
        raise argparse.ArgumentTypeError("path is not a directory")

    return path


def register_application(path: str):
    with open("/etc/hivesec/apps", "a") as file:
        file.write(path + "\n")


def handle_command(arguments: argparse.Namespace):
    """
    Handling command of the args parser.
    """
    if arguments.register:
        register_application(arguments.register)
        return


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
    group.add_argument(
        "-r",
        "--register",
        metavar="DIR",
        type=absolute_directory,
        help="Register an HiveSec application.",
    )

    args = parser.parse_args()
    args.func(args)
