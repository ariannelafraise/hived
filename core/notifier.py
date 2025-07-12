from abc import ABC, abstractmethod

class Notifier(ABC):
    @staticmethod
    @abstractmethod
    def notify(sender: str, message: str):
        """
        :param sender: sender's name (such as handler's name)
        :param message: the notification message
        """
        pass
