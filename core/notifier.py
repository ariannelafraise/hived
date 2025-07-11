from abc import ABC, abstractmethod

class Notifier(ABC):
    @staticmethod
    @abstractmethod
    def notify(content):
        pass
