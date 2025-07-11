# import requests
#
# from core.notifier import Notifier
# from config import DiscordWebhookNotifierConfig
#
#
# class DiscordWebhookNotifier(Notifier):
#     @staticmethod
#     def notify(message):
#         embed = {
#             "title": "Honeypot",
#             "description": message,
#             "color": 16711935
#         }
#         requests.post(
#             DiscordWebhookNotifierConfig.DISCORD_WEBHOOK_URL,
#             json={'embeds': [embed]},
#             headers={'Content-Type': 'application/json'}
#         )
#

import requests
import socket
import time

from core.notifier import Notifier
from config import DiscordWebhookNotifierConfig


class DiscordWebhookNotifier(Notifier):
    @staticmethod
    def is_connected(host="8.8.8.8", port=53, timeout=3):
        """Check for internet connectivity by trying to connect to a known IP."""
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error:
            return False

    @staticmethod
    def notify(message):
        # Retry up to 5 times if there's no network
        for attempt in range(5):
            if DiscordWebhookNotifier.is_connected():
                break
            time.sleep(5)
        else:
            # No network after retries
            print("DiscordWebhookNotifier: No network, skipping notification.")
            return

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
        except requests.exceptions.RequestException as e:
            print(f"DiscordWebhookNotifier: Failed to send webhook: {e}")
