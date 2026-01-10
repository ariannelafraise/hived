from abc import ABC, abstractmethod


class Notifier(ABC):
    """
    TODO
    """

    @staticmethod
    @abstractmethod
    def notify(sender: str, message: str) -> None:
        """
        TODO
        """
        pass
