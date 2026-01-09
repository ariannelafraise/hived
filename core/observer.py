from __future__ import annotations

from abc import ABC, abstractmethod

from core.event import Event

#
# Observer design pattern
#


class EventDispatcher(ABC):
    def __init__(self) -> None:
        self._observers: list[EventObserver] = []

    def add_observer(self, observer: EventObserver) -> None:
        self._observers.append(observer)

    @abstractmethod
    def _notify_observers(self, event: Event) -> None:
        pass


class EventObserver(ABC):
    @abstractmethod
    def handle(self, event: Event) -> None:
        pass
