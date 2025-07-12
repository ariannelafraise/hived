import requests

from core.notifier import Notifier
from config import DiscordWebhookNotifierConfig


class DiscordWebhookNotifier(Notifier):
    @staticmethod
    def notify(sender: str, message: str):
        """
        Sends a Discord Webhook notification.
        """
        embed = {
            "title": sender,
            "description": message,
            "color": 16711935,
            "author": {
                "name": "Hived",
                "url": "https://github.com/ariannelafraise/hived",
                "icon_url": "https://cdn.wallpapersafari.com/34/84/xkItg7.jpg"
            }
        }

        try:
            response = requests.post(
                DiscordWebhookNotifierConfig.DISCORD_WEBHOOK_URL,
                json={'embeds': [embed]},
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print(f"DiscordWebhookNotifier: Connection error:\n{e}")
        except requests.exceptions.HTTPError as e:
            print(f"DiscordWebhookNotifier: HTTP error:\n{e}")
