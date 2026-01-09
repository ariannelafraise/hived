from __future__ import annotations

import re

from core.logger import Logger

logger = Logger("event.py")


class LogParsingError(Exception):
    pass


class Event:  # AuditEvent?
    """
    An Auditd event, formed of multiple logs.
    """

    def __init__(self, logs: list[Log]) -> None:
        self.logs = logs


class Log:  # AuditLog?
    """
    A log is formed as follows: "key=value key2=value2...". They all have their own type to differentiate them.
    ex: SYSCALL, CWD, PATH, EOE.
    """

    def __init__(self, log_string: str) -> None:
        self._as_string = Log._clean_string(log_string)
        self.attributes = Log._parse_params(self._as_string)

    def __str__(self) -> str:
        return self._as_string

    @staticmethod
    def _clean_string(log_string: str) -> str:
        cleaned = log_string.replace("\n", "")
        if cleaned[-1] == " ":
            return cleaned[:-1]
        else:
            return cleaned

    @staticmethod
    def _parse_params(log_string: str) -> dict[str, str]:
        """
        Convert a log string to a dictionary of parameters.
        """

        regex_key = r"\w+"
        regex_single_quotes_value = r"'[^']*?'"
        regex_double_quotes_value = r"\"[^\"]*?\""
        regex_no_quotes_value = r"\S+"
        full_regex = rf"({regex_key})=({regex_single_quotes_value}|{regex_double_quotes_value}|{regex_no_quotes_value})"

        matches = re.findall(full_regex, log_string)
        params = {}
        for match in matches:
            params[match[0]] = match[1]

        return params
