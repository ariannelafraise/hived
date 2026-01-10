from abc import ABC, abstractmethod

from core.audit_event import AuditEvent
from core.observer import AuditEventObserver


class AuditEventHandler(AuditEventObserver, ABC):
    """
    Interface for creating audit event handlers. They are automatically and dynamically loaded by AudispdListener
    """

    @abstractmethod
    def _applies_to(self, event: AuditEvent) -> bool:
        """
        Verify that the received audit event should be acted upon

        Parameters:
            event: the audit event to check
        """
        pass

    @abstractmethod
    def handle(self, event: AuditEvent) -> None:
        """
        Handles a received event
        Called by AudispdListener on every Auditd event; it is recommended to verify
        if the event should be handled with self._applies_to()

        Parameters:
            event: an audit event received by AudispdListener
        """
        pass
