import re
from typing import Any


def clean_audit_event_string(record_string: str) -> str:
    """
    Cleans a record string by removing all '\\n' and trailing white spaces
    and returns it.

    Parameters:
        record_string: the string to be cleaned
    """
    cleaned = record_string.replace("\n", "")
    while cleaned[-1] == " ":
        cleaned = cleaned[:-1]
    return cleaned


def remove_surrounding_quotes(v: str) -> str:
    if len(v) >= 2 and v[0] in ("'", '"') and v[0] == v[-1]:
        return v[1:-1]
    return v


def parse_value(v: str):
    v = remove_surrounding_quotes(v)

    if "=" in v and " " in v:
        return parse_audit_event_fields(v)

    return v


def parse_audit_event_fields(record_string: str) -> dict[str, Any]:
    """
    Convert a record string to a dictionary of fields.

    A record is formed of multiple key=value fields:
        The values can be wrapped in:
            single-quotes: 'value'
            double-quotes: "value"
            no-quotes: value

    Parameters:
        record_string: the string representation of a record that should be parsed
    """

    record_string = remove_surrounding_quotes(record_string)

    regex_key = r"\w+"
    regex_single_quotes_value = r"'[^']*?'"
    regex_double_quotes_value = r"\"[^\"]*?\""
    regex_no_quotes_value = r"\S+"
    full_regex = rf"({regex_key})=({regex_single_quotes_value}|{regex_double_quotes_value}|{regex_no_quotes_value})"

    matches = re.findall(full_regex, record_string)

    fields: dict[str, Any] = {}
    msg_key_counter = 1
    for k, v in matches:
        if k == "msg":  # there can be one or two 'msg' fields
            k = f"msg{msg_key_counter}"
            msg_key_counter += 1

        fields[k] = parse_value(v)

    return fields
