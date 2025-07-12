from abc import ABC, abstractmethod

from core.notifier import Notifier
from core.event import Event
from core.observer import Observer


class EventHandler(Observer, ABC):
    """
    Interface for creating event handlers. They are automatically loaded by AudispdListener.
    """

    def __init__(self, notifier: Notifier):
        self._notifier = notifier

    @abstractmethod
    def _applies_to(self, event: Event) -> bool:
        """
        Verify that the received event should be acted upon.
        :param event: the event to check
        """
        pass

    @abstractmethod
    def handle(self, event: Event):
        """
        Called by AudispdListener on every event. Must call _applies_to().
        :param event: an event received by AudispdListener
        """
        pass
