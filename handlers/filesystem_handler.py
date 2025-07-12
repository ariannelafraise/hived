import binascii
import codecs

from core.event_handler import EventHandler
from core.event import Event
import utils.path_utils as path_utils
from config import NotifierConfig

def _proctitle_to_command(proctitle: str) -> str:
    try:
        return codecs.decode(
            proctitle.replace('00', '20'),
            'hex'
        ).decode('utf-8')
    except binascii.Error:
        return proctitle


class HoneypotFileHandler(EventHandler):
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

        file_path = path_utils.get_file_path(path.attributes['name'], cwd['cwd'])
        command = _proctitle_to_command(proctitle['proctitle'])
        alert = file_path + " has been accessed by " + syscall['UID'] + " using: `" + command + "`"
        NotifierConfig.NOTIFIER.notify("File System", alert)
