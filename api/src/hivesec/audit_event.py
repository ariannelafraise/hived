from __future__ import annotations

import json


class AuditEvent:
    """
    Represents an audit event. It is formed of multiple audit records.

    Attributes:
        records: a list of all records associated with the event
    """

    def __init__(self, records: list[AuditRecord]) -> None:
        self.records = records


class AuditRecord:
    """
    Represents an audit record.

    Can be represented as:
        a string (just like in the /var/log/audit/audit.log file)
        or
        a dictionary of key-values

    Attributes:
        _as_string: the record's string representation
        _fields: the record's fields in a dictionary
    """

    def __init__(self, record_string: str, fields: dict[str, str]) -> None:
        self._as_string = record_string
        self._fields = fields

    def __str__(self) -> str:
        return self._as_string
    
    def json(self):
        return json.dumps(self._fields, indent=4)

    def get_field_value(self, field: str) -> str:
        """
        Returns the value of a field, or None if the field is not present in the record.
        For better clarity and for better consistency with Audit logs, the values' surrounding quotes are kept.

        Parameters:
            field: the queried field
        """
        if field not in self._fields:
            raise ValueError(f"Record is missing '{field}' field: {str(self)}")
        return self._fields[field]

    def has_field(self, field: str) -> bool:
        """
        Checks whether a field exists in the record.

        Parameters:
            field: the field to check
        """
        return field in self._fields
