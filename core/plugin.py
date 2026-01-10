import argparse
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path

from config import PathConfig


class Plugin(ABC):
    """
    Base abstract class for defining a plugin.
    A plugin extends the functionalities of hivectl (using argparse).

    Also referred to as module.

    Attributes:
        _name: the name of the plugin. taken from the name of the directory
        containing the plugin in the 'modules' directory
        _rules_file_path: the path to the rules file: rules file format: <self._name>.rules
    """

    def __init__(self, name: str) -> None:
        """
        Initializes the plugin by setting its name and rules file path.

        Parameters:
            name: the name of the plugin
        """
        self._name = name
        rules_dir_path = PathConfig.RULES_DIR
        if rules_dir_path[-1] == "/":
            rules_dir_path = rules_dir_path[:-1]
        self._rules_file_path = f"{rules_dir_path}/{self._name}.rules"
        if not self._rules_file_exists:
            self._create_rules_file

    @abstractmethod
    def init_args_parser(self, subparser: argparse._SubParsersAction) -> None:
        """
        Add an args parser to hivectl's plugins subparsers collection. Must register self.handle_command as its
        handling function.

        Parameters:
            subparser: The plugins subparsers collection from hivectl
        """
        pass

    @abstractmethod
    def handle_command(self, args: argparse.Namespace) -> None:
        """
        Handling function of the plugin's args parser.

        Parameters:
            args: the arguments that were given to the parser during hivectl execution
        """
        pass

    def _add_rule(self, rule: str) -> None:
        """
        Internal plugin method for adding rules to auditd.
        Adds a rule to the plugin's rules file and loads the change into auditd.

        Parameters:
            rule: the rule to be added
        """
        if self._rules_file_exists():
            with open(self._rules_file_path, "r") as rules_file:
                rules = rules_file.read()
                if rule in rules:
                    raise ValueError("Rule already exists.")

        with open(self._rules_file_path, "a") as rules_file:
            rules_file.write("\n" + rule)

        self._reload_rules()

    def _clear_rules(self) -> None:
        """
        Internal plugin method for clearing its defined rules.
        Clears the plugin's rules file and loads the change into auditd.
        """
        if not self._rules_file_exists():
            return
        with open(self._rules_file_path, "w") as rules_file:
            rules_file.write("")
        subprocess.run(
            ["auditctl", "-D"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
        self._reload_rules()

    def _reload_rules(self) -> None:
        """
        Internal plugin method for reloading the rules into auditd using augenrules.
        Since augenrules processes all the rules in Auditd's rules directory, it reloads
        the rules for all plugins.
        """
        subprocess.run(
            ["augenrules", "--load"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )

    def _rules_file_exists(self) -> bool:
        """
        Verifies if the plugin's rules file exists.
        """
        file_path = Path(self._rules_file_path)
        return file_path.is_file()

    def _create_rules_file(self) -> None:
        """
        Creates the plugin's rules file.
        """
        open(self._rules_file_path, "x").close()
