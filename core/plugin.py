from abc import ABC, abstractmethod
import argparse


class Plugin(ABC):
    @staticmethod
    @abstractmethod
    def init_args_parser(subparser: argparse._SubParsersAction):
        pass

    @staticmethod
    @abstractmethod
    def handle_command(args: argparse.Namespace):
        pass
