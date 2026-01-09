import binascii
import codecs

import utils.path_utils as path_utils
from core.event import Event, Log
from core.event_handler import EventHandler
from core.logger import Logger
from notifiers.discord_webhook_notifier import DiscordWebhookNotifier


def _proctitle_to_command(proctitle: str) -> str:
    try:
        return codecs.decode(proctitle.replace("00", "20"), "hex").decode("utf-8")
    except binascii.Error:
        return proctitle


def _uid_to_username(uid: str) -> str:
    with open("/etc/passwd", "r") as file:
        for line in file:
            fields = line.split(":")
            if fields[2] == uid:
                return fields[0]
        raise ValueError("uid is not associated to any user")


class FileSystemEventHandler(EventHandler):
    def __init__(self) -> None:
        super().__init__()
        self.logger = Logger("File system plugin event handler")

    def _applies_to(self, event: Event) -> bool:
        keyIsValid = False
        isNotConfigChange = True
        for log in event.logs:
            if "key" in log.attributes:
                if log.attributes["key"] == '"filesystem"':
                    keyIsValid = True
            if log.attributes["type"] == "CONFIG_CHANGE":
                isNotConfigChange = False

        return keyIsValid and isNotConfigChange

    def handle(self, event: Event) -> None:
        if not self._applies_to(event):
            return

        self.logger.info(f"received event: {[str(x) for x in event.logs]}")

        syscall: Log | None = None
        cwd: Log | None = None
        path: Log | None = None
        proctitle: Log | None = None
        for log in event.logs:
            match log.attributes["type"]:
                case "SYSCALL":
                    syscall = log
                case "CWD":
                    cwd = log
                case "PATH":
                    path = log
                case "PROCTITLE":
                    proctitle = log

        if not syscall or not cwd or not path or not proctitle:
            raise ValueError("Received incomplete event")

        file_path = path_utils.get_file_path(
            path.attributes["name"].replace('"', ""),
            cwd.attributes["cwd"].replace('"', ""),
        )
        command = _proctitle_to_command(proctitle.attributes["proctitle"])
        alert = (
            file_path
            + " has been accessed by "
            + _uid_to_username(syscall.attributes["uid"])
            + " using: `"
            + command
            + "`"
        )
        DiscordWebhookNotifier.notify("File System", alert)
