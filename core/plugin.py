from abc import ABC, abstractmethod
import argparse


class Plugin(ABC):
    """
    A plugin extends the functionalities of hivectl (using argparse).
    """
    @staticmethod
    @abstractmethod
    def init_args_parser(subparser: argparse._SubParsersAction):
        """
        Add an args parser to hivectl's subparser. Must register handle_command() as its
        handling function.
        :param subparser: The plugins subparser from hivectl
        """
        pass

    @staticmethod
    @abstractmethod
    def handle_command(args: argparse.Namespace):
        """
        Handling function of the args parser.
        :param args: the args that were given to the parser
        """
        pass
