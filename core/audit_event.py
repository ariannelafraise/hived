from __future__ import annotations

import re

from core.hived_logger import Logger

logger = Logger("event.py")


class AuditEvent:
    """
    Represents an audit event. It is formed of multiple audit records

    Attributes:
        records: a list of all records associated with the event
    """

    def __init__(self, records: list[AuditRecord]) -> None:
        self.records = records


class AuditRecord:
    """
    Represents an audit record
    Can be represented as:
        a string (just like in the /var/log/audit/audit.log file)
        or
        a dictionary of key-values

    Attributes:
        _as_string: the record's string representation
        _fields: the record's fields in a dictionary
    """

    def __init__(self, record_string: str) -> None:
        self._as_string = AuditRecord._clean_string(record_string)
        self._fields = AuditRecord._parse_params(self._as_string)

    def __str__(self) -> str:
        return self._as_string

    @staticmethod
    def _clean_string(record_string: str) -> str:
        """
        Cleans a record string by removing all '\n' and trailing white spaces

        Parameters:
            record_string: the string to be cleaned
        """
        cleaned = record_string.replace("\n", "")
        while cleaned[-1] == " ":
            cleaned = cleaned[:-1]
        return cleaned

    @staticmethod
    def _parse_params(record_string: str) -> dict[str, str]:
        """
        Convert a record string to a dictionary of parameters

        A record is formed of multiple key=value fields:
            The values can be wrapped in:
                single-quotes: 'value'
                double-quotes: "value"
                no-quotes: value

        For better clarity and for better consistency with Auditd logs, the values' surrounding quotes are kept.

        Parameters:
            record_string: the string representation of a record that should be parsed
        """

        regex_key = r"\w+"
        regex_single_quotes_value = r"'[^']*?'"
        regex_double_quotes_value = r"\"[^\"]*?\""
        regex_no_quotes_value = r"\S+"
        full_regex = rf"({regex_key})=({regex_single_quotes_value}|{regex_double_quotes_value}|{regex_no_quotes_value})"

        matches = re.findall(full_regex, record_string)
        params = {}
        msg_key_counter = 1
        for match in matches:
            if match[0] == "msg":
                params[f"msg{msg_key_counter}"] = match[1]
                msg_key_counter += 1
            else:
                params[match[0]] = match[1]

        return params

    def get_field_value(self, field: str) -> str:
        """
        Returns the value of a field of the AuditRecord, or None if the field present in the AuditRecord.
        For better clarity and for better consistency with Audit logs, the values' surrounding quotes are kept.

        Parameters:
            field: the queried field
        """
        if field not in self._fields:
            raise ValueError(f"Record is missing '{field}' field: {str(self)}")
        return self._fields[field]

    def has_field(self, field: str) -> bool:
        return field in self._fields
