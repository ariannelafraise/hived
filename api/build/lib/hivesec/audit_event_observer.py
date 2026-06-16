from __future__ import annotations

from abc import ABC, abstractmethod

from .audit_event import AuditEvent


class AuditEventObserver(ABC):
    """
    Defines the interface of an audit event observer.
    In the observer design pattern, it represents the observer.

    Attributes:
        threaded: whether the handle method should be called on a new thread by the AuditEventDispatcher or not
    """

    def __init__(self, threaded: bool = False) -> None:
        self.threaded = threaded

    @abstractmethod
    def handle(self, event: AuditEvent) -> None:
        """
        Handle an audit event.
        """
        pass
