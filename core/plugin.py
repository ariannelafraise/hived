import argparse
import subprocess
from abc import ABC, abstractmethod


class Plugin(ABC):
    """
    A plugin extends the functionalities of hivectl (using argparse).
    """

    def __init__(self, name: str) -> None:
        # self._args_parser = None # idea from autocomplete
        self.name = name
        self.rules_file_path = f"/etc/audit/rules.d/{self.name}.rules"

    @abstractmethod
    def init_args_parser(self, subparser: argparse._SubParsersAction) -> None:
        """
        Add an args parser to hivectl's subparser. Must register handle_command() as its
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
        with open(self.rules_file_path, "r") as rules_file:
            rules = rules_file.read()
            if rule in rules:
                raise ValueError("Rule already exists.")

        with open(self.rules_file_path, "a") as rules_file:
            rules_file.write("\n" + rule)

        self._reload_rules()

    def _clear_rules(
        self,
    ) -> None:  # SHOULD INSTEAD REMOVE ITS OWN RULES AND NOT ALL RULES!
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
