from __future__ import annotations
from abc import ABC, abstractmethod


class Subject(ABC):
    def __init__(self):
        self._observers = []

    def add_observer(self, observer : Observer):
        self._observers.append(observer)

    @abstractmethod
    def _notify_observers(self, subject):
        pass


class Observer(ABC):
    @abstractmethod
    def handle(self, subject):
        pass
