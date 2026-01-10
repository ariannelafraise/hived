from __future__ import annotations

from abc import ABC, abstractmethod

from core.audit_event import AuditEvent


class AuditEventDispatcher(ABC):
    """
    Abstract class defining the behaviour of an audit event dispatcher.
    In the observer design pattern, it represents the subject.

    Attributes:
        _observers: the list of attached audit event observers
    """

    def __init__(self) -> None:
        self._observers: list[AuditEventObserver] = []

    def add_observer(self, observer: AuditEventObserver) -> None:
        """
        Add an audit event observer.

        Parameters:
            observer: the audit event observer to add
        """
        self._observers.append(observer)

    def _notify_observers(self, event: AuditEvent) -> None:
        """
        Notify all observers of a new audit event.

        Parameters:
            event: the new audit event
        """
        for o in self._observers:
            o.handle(event)


class AuditEventObserver(ABC):
    """
    Defines the interface of an audit event observer.
    In the observer design pattern, it represents the observer.
    """

    @abstractmethod
    def handle(self, event: AuditEvent) -> None:
        """
        Handle an audit event.
        """
        print("test")
        pass
