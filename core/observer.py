from __future__ import annotations

from abc import ABC, abstractmethod

from core.audit_event import AuditEvent
from core.modules import import_event_handlers


class AuditEventDispatcher(ABC):
    """
    Abstract class defining the behaviour of an audit event dispatcher.
    In the observer design pattern, it represents the subject.

    Attributes:
        _observers: the list of attached audit event observers
    """

    def __init__(self) -> None:
        """
        Initializes the audit event dispatcher by loading all event handlers.
        """
        self._observers: list[AuditEventObserver] = []
        self._load_event_handlers()

    def _add_observer(self, observer: AuditEventObserver) -> None:
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

    def _load_event_handlers(self) -> None:
        """
        Load all event handlers.
        """
        handlers = import_event_handlers()
        for h in handlers:
            self._add_observer(h)


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
        pass
