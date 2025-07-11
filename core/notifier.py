from abc import ABC, abstractmethod

class Notifier(ABC):
    """
    Gets called by handlers to send notifications.
    TODO: different handlers could have different notifiers. Right now its global in config file.
    """
    @staticmethod
    @abstractmethod
    def notify(sender: str, message: str):
        """
        :param sender: sender's name (such as handler's name)
        :param message: the notification message
        """
        pass
