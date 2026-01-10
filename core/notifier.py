from abc import ABC, abstractmethod


class Notifier(ABC):
    """
    Interface for creating notifiers.

    Also referred to as module.
    """

    @abstractmethod
    def notify(self, sender: str, message: str) -> None:
        """
        Sends a notification.

        Parameters:
            sender: the sender of the notification
            message: the message of the notification
        """
        pass
