from abc import ABC, abstractmethod

from .audit_event import AuditEvent


class AuditEventHandler(ABC):
    """
    Defines the interface of an audit event handler.
    In the observer design pattern, it represents the observer.

    Also referred to as module.
    """

    @abstractmethod
    def matches(self, event: AuditEvent) -> bool:
        """
        Verify that the received audit event should be acted upon.

        The audit event dispatcher will send the event to the handle()
        function only if this function returns True.

        Parameters:
            event: the audit event to check
        """
        pass

    @abstractmethod
    def handle(self, event: AuditEvent) -> None:
        """
        Handles a received event.

        Parameters:
            event: any audit event received by any AuditEventDispatcher
        """
        pass
