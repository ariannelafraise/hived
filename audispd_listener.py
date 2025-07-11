from config import PathConfig
from core.event_handler import EventHandler
from core.observer import Subject
from core.log import Log
from utils.import_utils import dynamic_import

import sys


class AudispdListener(Subject):
    def __init__(self):
        super().__init__()
        self._load_handlers()

    def _notify_observers(self, subject : list[Log]):
        for o in self._observers:
            o.handle(subject)

    def _load_handlers(self):
        handlers = dynamic_import(EventHandler, PathConfig.HANDLERS_DIR)
        [self.add_observer(h()) for h in handlers]

    def listen(self):
        logs = ""
        first = True
        for line in sys.stdin:
            if first and 'type=SYSCALL' not in line:
                continue
            if first and 'type=SYSCALL' in line:
                first = False
                logs += line
                continue
            if not first and 'type=EOE' in line:
                self.handle_event(logs)
                logs = ""
                first = True
                continue
            if not first and 'type=EOE' not in line:
                logs += line
                continue

    def handle_event(self, logs: str):
        new_logs : list[Log] = []
        for log in logs.split('\n'):
            if log == '': continue
            new_logs.append(Log(log))
        self._notify_observers(new_logs)
