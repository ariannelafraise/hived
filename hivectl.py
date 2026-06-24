import argparse
import subprocess
from pathlib import Path

from core.external import import_plugins
from __version__ import __version__

RESET = "\033[0m"

PASTEL_RED     = "\033[38;2;255;179;186m"
PASTEL_ORANGE  = "\033[38;2;255;223;186m"
PASTEL_YELLOW  = "\033[38;2;255;255;186m"
PASTEL_GREEN   = "\033[38;2;186;255;201m"
PASTEL_CYAN    = "\033[38;2;186;255;255m"
PASTEL_BLUE    = "\033[38;2;186;225;255m"
PASTEL_PURPLE  = "\033[38;2;218;191;255m"
PASTEL_PINK    = "\033[38;2;255;209;220m"
PASTEL_LAVENDER = "\033[38;2;230;230;250m"
PASTEL_MINT    = "\033[38;2;189;252;201m"

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
    
    if path[-1] == "/":
        return path[:-1]
    else:
        return path


def register_application(path: str):
    with open("/etc/hivesec/apps", "a") as file:
        file.write(path + "\n")


def unregister_application(path: str):
    with open("/etc/hivesec/apps", "r") as file:
        lines = file.readlines()
    with open("/etc/hivesec/apps", "w") as file:
        for line in lines:
            if line.strip("\n") != path:
                file.write(line)


def list_apps():
    with open("/etc/hivesec/apps", "r") as file:
        for line in file:
            if not line.startswith("#"):
                print(line)


def install_dependency(packages):
    packages = packages.split(",")
    process = subprocess.Popen(
        ["/usr/local/lib/hivesec/.venv/bin/pip", "install", "--", *packages],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for line in process.stdout:
        print(line, end="")


def handle_command(arguments: argparse.Namespace):
    """
    Handling command of the args parser.
    """
    if arguments.register:
        register_application(arguments.register)
        return
    if arguments.unregister:
        unregister_application(arguments.unregister)
        return
    if arguments.list_apps:
        list_apps()
        return
    if arguments.install_dependency:
        install_dependency(arguments.install_dependency)
        return



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hivectl")
    parser.set_defaults(func=handle_command)
    subparsers = parser.add_subparsers(dest="plugin")

    try:
        plugins = import_plugins()
        [plugin.init_args_parser(subparsers) for plugin in plugins]
    except ModuleNotFoundError:
        print(PASTEL_RED, end="")
        print("Warning: Some dependencies are missing. Make sure to install dependencies needed for HiveSec apps with 'sudo hivectl --install-dependency <packages>'")
        print("Skipping plugins loading.\n")
        print(RESET, end="")
        pass

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
    group.add_argument(
        "-ur",
        "--unregister",
        metavar="DIR",
        type=absolute_directory,
        help="Unregister an HiveSec application.",
    )
    group.add_argument(
        "-l",
        "--list-apps",
        action="store_true",
        help="List the currently registered apps.",
    )
    group.add_argument(
        "-pip",
        "--install-dependency",
        metavar="PACKAGES",
        type=str,
        help="Install PyPi dependency. PACKAGES = comma-separated list of packages to install.",
    )

    args = parser.parse_args()
    args.func(args)
