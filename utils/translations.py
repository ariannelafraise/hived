import binascii
import codecs
import subprocess


def proctitle_to_command(proctitle: str) -> str:
    try:
        return codecs.decode(proctitle.replace("00", "20"), "hex").decode("utf-8")
    except binascii.Error:
        return proctitle


def uid_to_username(uid: str) -> str:
    with open("/etc/passwd", "r") as file:
        for line in file:
            fields = line.split(":")
            if fields[2] == uid:
                return fields[0]
        raise ValueError("uid is not associated to any user")


def syscall_number_to_name(number: str) -> str:
    return subprocess.run(
        ["ausyscall", number], capture_output=True, text=True, check=True
    ).stdout
