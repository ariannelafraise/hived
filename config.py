import os


class GeneralConfig:
    VERSION = "0.0.2"


class PathConfig:
    RULES_FILE_PATH = "/etc/audit/rules.d/honeypot.rules"
    LOG_FILE_PATH = "/var/log/audit/audit.log"
    CWD = os.getcwd()
    PLUGINS_DIR = "/home/arianne/personal_dev/hived/plugins"
    HANDLERS_DIR = "/home/arianne/personal_dev/hived/plugins"
