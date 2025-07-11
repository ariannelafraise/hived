import binascii
import codecs

from core.event_handler import EventHandler
from core.log import Log
import utils.path_utils as path_utils
from notifiers.discord_webhook_notifier import DiscordWebhookNotifier


class HoneypotFileHandler(EventHandler):
    def _applies_to(self, logs: list[Log]) -> bool:
        logs_str = ""
        for log in logs:
            logs_str += log.as_string
        if "key=\"honeypot_file\"" in logs_str and "type=CONFIG_CHANGE" not in logs_str:
            return True
        return False

    def handle(self, logs : list[Log]):
        if not self._applies_to(logs):
            return
        syscall_log = ""
        syscall_params = {}
        cwd_log = ""
        cwd_params = {}
        path_log = ""
        path_params = {}
        file_path = ""
        proctitle_log = ""
        proctitle_params = {}

        for log in logs:
            log_str = log.as_string
            params = log.attributes
            if 'type=SYSCALL' in log_str:
                syscall_log = log_str
                syscall_params = params
            if 'type=CWD' in log_str:
                cwd_log = log_str
                cwd_params = params
            if 'type=PATH' in log_str:
                path_log = log_str
                path_params = params
            if 'type=PROCTITLE' in log_str:
                proctitle_log = log_str
                proctitle_params = params

        file_path = path_utils.get_file_path(path_params['name'], cwd_params['cwd'])
        try:
            command = codecs.decode(
                # type=PROCTITLE msg=audit(1750954490.074:216): proctitle=636174002F686F6D652F617269616E6E652F446F776E6C6F6164732F2E2E2F617269616E6E652E747874
                # proctile: command that was used, in hex. 00 = NUL -> switch to 20 = Space
                proctitle_params['proctitle'].replace('00', '20'),
                'hex'
            ).decode('utf-8')
        except binascii.Error:
            command = proctitle_params['proctitle']
        alert = "honeypot hit! " + file_path + " by " + syscall_params['UID'] + " using: `" + command + "`"
        DiscordWebhookNotifier.notify(alert)
