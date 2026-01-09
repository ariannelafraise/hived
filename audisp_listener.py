import sys

from core.event import Event, Log
from core.logger import Logger
from core.observer import EventDispatcher
from utils.import_utils import import_event_handlers


class AudispListener(EventDispatcher):
    def __init__(self) -> None:
        super().__init__()
        self._load_event_handlers()
        self.logger = Logger("AudispListener")

    def _load_event_handlers(self) -> None:
        handlers = import_event_handlers()
        for h in handlers:
            self.add_observer(h)

    def _notify_observers(self, event: Event) -> None:
        for o in self._observers:
            o.handle(event)

    def listen(self) -> None:
        logs: list[Log] = []
        first = True

        for line in sys.stdin:
            log = Log(line)
            self.logger.info(str(log), "audit_events")

            if "type" not in log.attributes:  # TODO: make error logging
                self.logger.info(str(log))

            if first and log.attributes["type"] != "EOE":
                logs.append(log)
                first = False

            if not first and log.attributes["type"] != "EOE":
                logs.append(log)

            if not first and log.attributes["type"] == "EOE":
                self._notify_observers(Event(logs))
                logs = []
                first = True
