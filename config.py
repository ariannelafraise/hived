import os
from dotenv import load_dotenv

from notifiers.discord_webhook_notifier import DiscordWebhookNotifier

load_dotenv()

class GeneralConfig:
    VERSION = '0.0.2'


class PathConfig:
    RULES_FILE_PATH = '/etc/audit/rules.d/honeypot.rules'
    LOG_FILE_PATH = '/var/log/audit/audit.log'
    CWD = os.getcwd()
    PLUGINS_DIR = '/home/arianne/personal_dev/hived/plugins'
    HANDLERS_DIR = '/home/arianne/personal_dev/hived/handlers'


class NotifierConfig:
    NOTIFIER = DiscordWebhookNotifier


class DiscordWebhookNotifierConfig:
    DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK')
