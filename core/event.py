class Log:
    """
    A log is formed as follows: "key=value key2=value2". They all have their own type to differentiate them.
    ex: SYSCALL, CWD, PATH, EOE. A set of logs forms an event
    """
    def __init__(self, log_string : str):
        self.as_string = log_string
        self.attributes = self._parse_params()

    def _parse_params(self) -> dict:
        """
        Convert a log string to a dictionary of parameters.
        """
        params = {}
        for param in self.as_string.split(' '):
            key_value = param.replace('\"', '').split('=')
            if key_value[0] != 'key':
                params[key_value[0]] = key_value[1]
        return params

    def get_type(self) -> str:
        return self.attributes['type']
