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

    def _notify_observers(self, event: AuditEvent) -> None:
        for o in self._observers:
            o.handle(event)


class AuditEventObserver(ABC):
    @abstractmethod
    def handle(self, event: AuditEvent) -> None:
        pass
