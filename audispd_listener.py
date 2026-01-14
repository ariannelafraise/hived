import sys

from core.audit_event import AuditEvent, AuditRecord
from core.observer import AuditEventDispatcher
from utils.import_utils import import_event_handlers


class AudispdListener(AuditEventDispatcher):
    def __init__(self) -> None:
        super().__init__()
        self._load_event_handlers()

    def _load_event_handlers(self) -> None:
        handlers = import_event_handlers()
        for h in handlers:
            self.add_observer(h)

    def listen(self) -> None:
        records: list[AuditRecord] = []
        first = True
        current_event_timestamp = ""
        current_event_id = ""

        for line in sys.stdin:
            record = AuditRecord(line)

            type = record.get_field_value("type")
            msg1 = record.get_field_value("msg1")

            if type == "EOE":
                continue

            current_record_timestamp_id = msg1.split(":")
            current_record_timestamp = current_record_timestamp_id[0]
            current_record_id = current_record_timestamp_id[1]

            if first:
                print(1)
                records.append(record)
                current_event_timestamp = current_record_timestamp
                current_event_id = current_record_id
                first = False
                continue

            if not first and (
                current_event_timestamp == current_record_timestamp
                and current_event_id == current_record_id
            ):
                print(2)
                records.append(record)
                continue

            if not first and (
                current_event_timestamp != current_record_timestamp
                and current_event_id != current_record_id
            ):
                print(3)
                self._notify_observers(AuditEvent(records))
                records = []
                records.append(record)
                current_event_timestamp = current_record_timestamp
                current_event_id = current_record_id
                continue
