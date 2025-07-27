from __future__ import annotations

class Event:
    """
    An Auditd event, formed of multiple logs.
    """
    def __init__(self, logs: list[Log]):
        self.logs = logs


class Log:
    """
    A log is formed as follows: "key=value key2=value2". They all have their own type to differentiate them.
    ex: SYSCALL, CWD, PATH, EOE.
    """
    def __init__(self, log_string : str):
        self.as_string = Log._clean_string(log_string)
        self.attributes = Log._parse_params(log_string)

    @staticmethod
    def _clean_string(log_string : str) -> str:
        return log_string.replace('\n', '')

    @staticmethod
    def _parse_params(log_string : str) -> dict:
        """
        Convert a log string to a dictionary of parameters.
        """
        params = {}
        for param in log_string.split(' '):
            key_value = param.replace('\"', '').split('=')
            if key_value[0] != 'key':
                params[key_value[0]] = key_value[1]
        return params

    def get_type(self) -> str:
        return self.attributes['type']
