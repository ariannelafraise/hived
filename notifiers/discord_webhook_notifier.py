import os

import requests
from dotenv import load_dotenv

from core.notifier import Notifier

load_dotenv()
URL = os.getenv("DISCORD_WEBHOOK_URL")


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
                "icon_url": "https://cdn.wallpapersafari.com/34/84/xkItg7.jpg",
            },
        }

        try:
            if not URL:
                raise ValueError("Discord Webhook URL not set")
            response = requests.post(
                URL,
                json={"embeds": [embed]},
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print(f"DiscordWebhookNotifier: Connection error:\n{e}")
        except requests.exceptions.HTTPError as e:
            print(f"DiscordWebhookNotifier: HTTP error:\n{e}")
