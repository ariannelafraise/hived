import requests

from core.notifier import Notifier
from config import DiscordWebhookNotifierConfig


class DiscordWebhookNotifier(Notifier):
    @staticmethod
    def notify(message):
        embed = {
            "title": "Honeypot",
            "description": message,
            "color": 16711935
        }
        try:
            response = requests.post(
                DiscordWebhookNotifierConfig.DISCORD_WEBHOOK_URL,
                json={'embeds': [embed]},
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print(f"DiscordWebhookNotifier connection error:\n{e}")
        except requests.exceptions.HTTPError as e:
            print(f"DiscordWebhookNotifier HTTP error:\n{e}")
