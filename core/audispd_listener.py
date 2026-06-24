import sys
import select

import core.utils.parsing as parsing
from core.audit_event_dispatcher import AuditEventDispatcher
from hivesec import AuditEvent, AuditRecord

TIMEOUT = 1 # 50 ms

class AudispdListener(AuditEventDispatcher):
    def __init__(self) -> None:
        super().__init__()

    def listen(self) -> None:
        """
        Listens for audit logs sent by Audispd in stdin and forwards them to its observers.
        Logically ties records of the same event.
        """
        records: list[AuditRecord] = []
        first = True # First record received total, not for specific event
        current_event_id = ""

        while True:
            ready, _, _ = select.select([sys.stdin], [], [], TIMEOUT)

            if not ready: 
                # after TIMEOUT, send the event. this is needed because HiveSec know the event ended only when a new one starts.
                # since event records are sent almost simultaneously, HiveSec can know that after a 
                # certain period of time without new records, the event must have ended.
                if records:
                    self._notify_observers(AuditEvent(records))
                    records = []
                continue

            line = sys.stdin.readline()

            if not line: # happens when testing: EOF occurs, which would never happen in real usage
                if records:
                    self._notify_observers(AuditEvent(records))
                

            cleaned_event_string = parsing.clean_audit_event_string(line)
            fields = parsing.parse_audit_event_fields(cleaned_event_string)
            record = AuditRecord(cleaned_event_string, fields)

            type = record.get_field_value("type")
            msg1 = record.get_field_value("msg1")

            if type == "EOE":
                continue

            current_record_id = msg1.split(":")[1]

            if first:
                records.append(record)
                current_event_id = current_record_id
                first = False
                continue

            if not first and current_event_id == current_record_id:
                records.append(record)
                continue

            if not first and current_event_id != current_record_id:
                self._notify_observers(AuditEvent(records))
                records = []
                records.append(record)
                current_event_id = current_record_id
                continue
