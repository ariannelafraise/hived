from abc import ABC, abstractmethod

from core.log import Log
from core.observer import Observer


class EventHandler(Observer, ABC):
    @abstractmethod
    def _applies_to(self, logs : list[Log]) -> bool:
        pass

    @abstractmethod
    def handle(self, logs : list[Log]):
        pass
