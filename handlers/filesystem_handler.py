import binascii
import codecs

from core.event_handler import EventHandler
from core.event import Event
import utils.path_utils as path_utils
from core.notifier import Notifier


def _proctitle_to_command(proctitle: str) -> str:
    try:
        return codecs.decode(
            proctitle.replace('00', '20'),
            'hex'
        ).decode('utf-8')
    except binascii.Error as e:
        print(e)
        return proctitle


class HoneypotFileHandler(EventHandler):
    def __init__(self, notifier: Notifier):
        super().__init__(notifier)

    def _applies_to(self, event: Event) -> bool:
        logs_str = ""
        for log in event.logs:
            logs_str += log.as_string
        if "key=\"filesystem\"" in logs_str and "type=CONFIG_CHANGE" not in logs_str:
            return True
        return False

    def handle(self, event: Event):
        if not self._applies_to(event):
            return

        syscall = None
        cwd = None
        path = None
        proctitle = None
        for log in event.logs:
            match log.get_type():
                case "SYSCALL":
                    syscall = log
                case "CWD":
                    cwd = log
                case "PATH":
                    path = log
                case "PROCTITLE":
                    proctitle = log
        file_path = path_utils.get_file_path(path.attributes['name'], cwd.attributes['cwd'])
        command = _proctitle_to_command(proctitle.attributes['proctitle'])
        alert = file_path + " has been accessed by " + syscall.attributes['UID'] + " using: `" + command + "`"
        self._notifier.notify("File System", alert)
