import os


class GeneralConfig:
    VERSION = '0.01'


class PathConfig:
    RULES_FILE_PATH = '/etc/audit/rules.d/honeypot.rules'
    LOG_FILE_PATH = '/var/log/audit/audit.log'
    CWD = os.getcwd()
    PLUGINS_DIR = '/home/arianne/personal_dev/hived/plugins'
    HANDLERS_DIR = '/home/arianne/personal_dev/hived/handlers'


class DiscordWebhookNotifierConfig:
    DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1343394186401021992/vFurn7zdOnh04Ce7KBJa-o6KsFAstKQMLnNiWoguTy4iQO9LI3ZSHlgmHddAZTSkylDE"
