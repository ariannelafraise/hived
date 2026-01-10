from __future__ import annotations

from abc import ABC, abstractmethod

from core.audit_event import AuditEvent

#
# Observer design pattern
#


class AuditEventDispatcher(ABC):
    def __init__(self) -> None:
        self._observers: list[AuditEventObserver] = []

    def add_observer(self, observer: AuditEventObserver) -> None:
        self._observers.append(observer)

    @abstractmethod
    def _notify_observers(self, event: AuditEvent) -> None:
        pass


class AuditEventObserver(ABC):
    @abstractmethod
    def handle(self, event: AuditEvent) -> None:
        pass
