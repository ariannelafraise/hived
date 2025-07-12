import os
from dotenv import load_dotenv

load_dotenv()

class GeneralConfig:
    VERSION = '0.0.1'


class PathConfig:
    RULES_FILE_PATH = '/etc/audit/rules.d/honeypot.rules'
    LOG_FILE_PATH = '/var/log/audit/audit.log'
    CWD = os.getcwd()
    PLUGINS_DIR = '/home/arianne/personal_dev/hived/plugins'
    HANDLERS_DIR = '/home/arianne/personal_dev/hived/handlers'


class DiscordWebhookNotifierConfig:
    DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK')
