import argparse
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path

from config import PathConfig


class Plugin(ABC):
    """
    A plugin extends the functionalities of hivectl (using argparse).
    """

    def __init__(self, name: str) -> None:
        self.name = name
        rules_folder_path = PathConfig.RULES_DIR
        if rules_folder_path[-1] == "/":
            rules_folder_path = rules_folder_path[:-1]
        self.rules_file_path = f"{rules_folder_path}/{self.name}.rules"
        if not self._rules_file_exists:
            self._create_rules_file

    @abstractmethod
    def init_args_parser(self, subparser: argparse._SubParsersAction) -> None:
        """
        Add an args parser to hivectl's subparser. Must register self.handle_command as its
        handling function.
        :param subparser: The plugins subparser from hivectl
        """
        pass

    @abstractmethod
    def handle_command(self, args: argparse.Namespace) -> None:
        """
        Handling function of the args parser.
        :param args: the args that were given to the parser
        """
        pass

    def _add_rule(self, rule: str) -> None:
        if self._rules_file_exists():
            with open(self.rules_file_path, "r") as rules_file:
                rules = rules_file.read()
                if rule in rules:
                    raise ValueError("Rule already exists.")

        with open(self.rules_file_path, "a") as rules_file:
            rules_file.write("\n" + rule)

        self._reload_rules()

    def _clear_rules(self) -> None:
        if not self._rules_file_exists():
            return
        with open(self.rules_file_path, "w") as rules_file:
            rules_file.write("")
        subprocess.run(
            ["auditctl", "-D"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
        self._reload_rules()

    def _reload_rules(self) -> None:
        subprocess.run(
            ["augenrules", "--load"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )

    def _rules_file_exists(self) -> bool:
        file_path = Path(self.rules_file_path)
        return file_path.is_file()

    def _create_rules_file(self) -> None:
        open(self.rules_file_path, "x").close()
