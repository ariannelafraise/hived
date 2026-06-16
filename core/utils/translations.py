import codecs
import subprocess


def proctitle_to_readable(proctitle: str) -> str:
    """
    Translates a proctitle from its HEX format to a readable string.

    Parameters:
        proctitle: the proctitle to translate
    """
    # Changes 00 to 20 because Auditd logs 20 as 00
    return codecs.decode(proctitle.replace("00", "20"), "hex").decode("utf-8")


def uid_to_username(uid: str) -> str:
    """
    Translates a user uid to its corresponding username
    in the /etc/passwd file.

    Parameters:
        uid: the uid to translate
    """
    with open("/etc/passwd", "r") as file:
        for line in file:
            fields = line.split(":")
            if fields[2] == uid:
                return fields[0]
        raise ValueError("uid is not associated to any user")


def syscall_number_to_name(number: str) -> str:
    """
    Translates a system call number to its corresponding name using ausyscall.

    Parameters:
        number: the system call number to translate
    """
    return subprocess.run(
        ["ausyscall", number], capture_output=True, text=True, check=True
    ).stdout
