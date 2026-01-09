from abc import ABC, abstractmethod

from core.event import Event
from core.observer import EventObserver


class EventHandler(EventObserver, ABC):
    """
    Interface for creating event handlers. They are automatically loaded by AudispdListener.
    """

    @abstractmethod
    def _applies_to(self, event: Event) -> bool:
        """
        Verify that the received event should be acted upon.
        :param event: the event to check
        """
        pass

    @abstractmethod
    def handle(self, event: Event) -> None:
        """
        Called by AudispdListener on every event. Must call _applies_to().
        :param event: an event received by AudispdListener
        """
        pass
