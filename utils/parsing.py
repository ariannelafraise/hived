import re


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


def parse_audit_event_fields(record_string: str) -> dict[str, str]:
    """
    Convert a record string to a dictionary of fields.

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
    fields = {}
    msg_key_counter = 1
    for match in matches:
        if match[0] == "msg":  # there can be one or two 'msg' fields
            fields[f"msg{msg_key_counter}"] = match[1]
            msg_key_counter += 1
        else:
            fields[match[0]] = match[1]

    return fields
