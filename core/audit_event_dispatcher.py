from __future__ import annotations

from abc import ABC

from hivesec import AuditEvent, AuditEventHandler


class AuditEventDispatcher(ABC):
    """
    Abstract class defining the behaviour of an audit event dispatcher.
    In the observer design pattern, it represents the subject.

    Attributes:
        _observers: the list of attached audit event observers
    """

    def __init__(self) -> None:
        self._observers: list[AuditEventHandler] = []

    def add_observer(self, observer: AuditEventHandler) -> None:
        """
        Add an audit event handler (observer).

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
            if o.matches(event):
                o.handle(event)
