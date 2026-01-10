import binascii
import codecs
import subprocess

import core.hived_logger as hived_logger
import utils.path_utils as path_utils
from core.audit_event import AuditEvent, AuditRecord
from core.audit_event_handler import AuditEventHandler
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


def _syscall_number_to_name(number: str) -> str:
    return subprocess.run(
        ["ausyscall", number], capture_output=True, text=True, check=True
    ).stdout


class FileSystemEvent:
    def __init__(self, event: AuditEvent) -> None:
        syscall: AuditRecord | None = None
        cwd: AuditRecord | None = None
        path1: AuditRecord | None = None
        path2: AuditRecord | None = None
        proctitle: AuditRecord | None = None
        for record in event.records:
            type = record.get_field_value("type")
            if not type:
                raise ValueError("Received a record that is missing the 'type' field")

            match type:
                case "SYSCALL":
                    if syscall:
                        raise ValueError("Received multiple SYSCALL records")
                    syscall = record
                case "CWD":
                    if cwd:
                        raise ValueError("Received multiple CWD records")
                    cwd = record
                case "PATH":
                    if not path1:
                        path1 = record
                    else:
                        path2 = record
                    if path1 and path2:
                        raise ValueError("Received more than two PATH records")

                case "PROCTITLE":
                    if proctitle:
                        raise ValueError("Received multiple PROCTITLE records")
                    proctitle = record
        if not syscall or not cwd or not path1 or not proctitle:
            raise ValueError(
                f"Received incomplete event: syscall={syscall}, cwd={cwd}, path1={path1}, proctitle={proctitle}"
            )
        self.syscall = syscall
        self.cwd = cwd
        self.path1 = path1
        self.path2 = path2
        self.proctitle = proctitle

    def __str__(self) -> str:
        path1_name = self.path1.get_field_value("name")
        path1_nametype = self.path1.get_field_value("nametype")
        cwd_cwd = self.cwd.get_field_value("cwd")
        proctitle_proctitle = self.proctitle.get_field_value("proctitle")
        syscall_uid = self.syscall.get_field_value("uid")
        syscall_syscall = self.syscall.get_field_value("syscall")

        command = _proctitle_to_command(proctitle_proctitle)
        username = _uid_to_username(syscall_uid)
        syscall_name = _syscall_number_to_name(syscall_syscall)
        path = ""

        if path1_nametype == "PARENT":
            if not self.path2:
                raise ValueError("Missing second PATH record")

            path2_name = self.path2.get_field_value("name")
            path = path2_name
        else:
            path = path1_name

        path = path_utils.get_file_path(
            path.replace('"', ""),
            cwd_cwd.replace('"', ""),
        )

        return f"{path} has been hit with syscall {syscall_name} ({syscall_syscall}) by {username} using: `{command}`"


class FileSystemEventHandler(AuditEventHandler):
    def __init__(self) -> None:
        super().__init__()

    def _applies_to(self, event: AuditEvent) -> bool:
        keyIsValid = False
        isNotConfigChange = True
        for record in event.records:
            if (
                record.has_field("key")
                and record.get_field_value("key") == '"filesystem"'
            ):
                keyIsValid = True
            if record.get_field_value("type") == "CONFIG_CHANGE":
                isNotConfigChange = False

        return keyIsValid and isNotConfigChange

    def handle(self, event: AuditEvent) -> None:
        if not self._applies_to(event):
            return

        hived_logger.info(
            f"received event: {[str(x) for x in event.records]}",
            "FileSystemEventHandler",
        )

        DiscordWebhookNotifier.notify("File System", str(FileSystemEvent(event)))
