import requests

from core.notifier import Notifier
from modules.discord_notifier.config import DiscordNotifierConfig


class DiscordWebhookNotifier(Notifier):
    def notify(self, sender: str, message: str):
        """
        Sends a Discord Webhook notification.
        """
        embed = {"title": sender, "description": message, "color": 16711935}

        try:
            response = requests.post(
                DiscordNotifierConfig.webhook_url,
                json={"embeds": [embed]},
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print(f"DiscordWebhookNotifier: Connection error:\n{e}")
        except requests.exceptions.HTTPError as e:
            print(f"DiscordWebhookNotifier: HTTP error:\n{e}")
