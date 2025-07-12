import sys

from config import PathConfig
from core.event_handler import EventHandler
from core.observer import Subject
from core.event import Log, Event
from utils.import_utils import dynamic_import


class AudispdListener(Subject):
    def __init__(self):
        super().__init__()
        self._load_handlers()

    def _load_handlers(self):
        handlers = dynamic_import(EventHandler, PathConfig.HANDLERS_DIR)
        [self.add_observer(h()) for h in handlers]

    def _notify_observers(self, event: Event):
        for o in self._observers:
            o.handle(event)

    def listen(self):
        logs: list[Log] = []
        first = True
        for line in sys.stdin:
            log = Log(line)
            if first and log.get_type() == 'SYSCALL':
                continue
            if first and log.get_type() == 'SYSCALL':
                first = False
                logs.append(log)
                continue
            if not first and log.get_type() == 'EOE':
                self._notify_observers(Event(logs))
                logs = []
                first = True
                continue
            if not first and log.get_type() == 'EOE':
                logs.append(log)
                continue
