---
name: hivesec-development
description: Develop HiveSec applications
---

# HiveSec Development Skill

## Overview

HiveSec is an open-source Linux audit event processing framework built on top of the Linux Audit subsystem. It enables developers to build Python applications that monitor, analyze, and respond to Linux audit events in real-time through an Observer design pattern.

## Scope 
This skill is strictly used to enable LLMs to understand the HiveSec framework for making applications. Application-specific information is out-of-scope.

## Architecture

### Data Flow
```
Linux Audit (audispd) → HiveSec Daemon → AuditEventHandlers → Applications
```

1. **AudispdListener** reads audit logs from audispd daemon via stdin
2. **Audit Event Dispatcher** groups related records into complete `AuditEvent` objects using the Observer pattern
3. **HiveSec applications** register handlers that receive and process events

### Core Components

- **hivesecd**: The daemon subscribed to Audispd as a plugin, distributes events to registered applications
- **hivectl**: CLI tool for administrative tasks (registering apps, managing audit rules)

## API Reference

### Essential Classes (`from hivesec import ...`)

#### `AuditEventHandler` - Event Processing

```python
class AuditEventHandler(ABC):
    @abstractmethod
    def matches(self, event: AuditEvent) -> bool:
        """Filter events - return True if handler should process this event"""
        
    @abstractmethod  
    def handle(self, event: AuditEvent) -> None:
        """Process the audit event. Verify with has_field() checks first."""
```

The `matches()` method determines whether an event should trigger the handler. The `handle()` method processes events that pass the filter. There is NO `_applies_to()` method - use `matches()` for filtering instead.

#### `AuditEvent` and `AuditRecord` - Event Data

- **AuditEvent**: Container for multiple related records (same timestamp/ID)
  ```python
  event.records  # list[AuditRecord]
  ```
  
- **AuditRecord**: Individual log entry, accessible as:
  ```python
  record.has_field("field_name")        # Check if field exists FIRST
  record.get_field_value("field_name")  # Get value ONLY after has_field() returns True
  record.json()                         # Get records fields as JSON
  str(record)                           # String representation (log format)
  ```

**⚠️ CRITICAL: CORRECT FIELD ACCESS PATTERN**
- `get_field_value(field)` takes **ONE PARAMETER only**: the field name as string
- `get_field_value()` **RAISES ValueError** if field doesn't exist - it does NOT have a `.get()` method!
- **ALWAYS check with `has_field()` before calling `get_field_value()`**:
  ```python
  # CORRECT:
  if record.has_field("key"):
      key = record.get_field_value("key").strip('"\'')  # Strip quotes manually
  
  # WRONG - common mistakes:
  # ❌ record._fields["key"]                    # Direct dict access bypasses API
  # ❌ record._fields.get("key", "default")     # AuditRecord has no .get() method!
  # ❌ record.get_field_value("key", "default") # get_field_value only takes ONE parameter!
  ```

Field parsing strips the `=` sign but keeps surrounding quotes:
- Log: `msg=audit(1766092657.249:131): item=0 name="/etc/shadow"`
- Dict: `{"msg": "audit(1766092657.249:131):", "item": "0", "name": '"/etc/shadow"'}`

#### Audit Record Fields (Common Linux Audit fields)

- `key`: Audit rule key identifier
- `name`: File path being accessed/modified
- `inode`: File inode number
- `type`: Event type
- `msg1`: Message field containing audit serial (format: `audit(TIMESTAMP.SECS:SERIAL)`)
  - Split on `:` to extract serial number: `msg1.split(":")[1]`

### Plugin System (`HivectlPlugin`)

Extend hivectl with new commands for managing audit rules and application configuration:

```python
class HivectlPlugin(ABC):
    NAME = "my-plugin"  # Corresponds to /etc/audit/rules.d/my-plugin.rules
    
    def __init__(self, name: str) -> None
    
    @abstractmethod
    def init_args_parser(self, subparsers: argparse._SubParsersAction) -> None:
        """Define CLI arguments using argparse"""
        
    @abstractmethod
    def handle_command(self, args: argparse.Namespace) -> None:
        """Handle the command execution"""
    
    # Available helper methods
    self._add_rule("rule-string")      # Add rule to auditd
    self._clear_rules()                # Remove all rules for this plugin
```

Rules stored at `/etc/audit/rules.d/{NAME}.rules` and reloaded via `augenrules --load`.

## Application Development Workflow

### 1. Create Handler or Plugin File

Place Python files containing classes extending `AuditEventHandler` or `HivectlPlugin`:
- No specific structure required
- Can be standalone `.py` files in the application directory
- All paths must be **absolute** (code runs as root from different working dir)

### 2. Register Application

Add absolute path to `/etc/hivesec/apps`:
```bash
# Edit file directly or use CLI:
sudo hivectl --register /home/user/my-app
```

### 3. Reboot System

Restart for HiveSec daemon to detect and load new applications:
```bash
sudo reboot
```

## Error Handling

- **ExternalApplicationImportError**: Module loading failures (import error)
- **ValueError**: Missing fields in AuditRecord (use `has_field()` before `get_field_value()`)
- **InvalidPluginNameException**: Empty plugin name in HivectlPlugin (`NAME` must be non-empty string)
- **Runtime errors logged to `/var/log/hivesec/error_traceback.log`**: Wrap exceptions in try/except and call `error_traceback(traceback.format_exc())`

## Logging

Use Python's built-in `print()` for debugging, or HiveSec logger API:

```python
# Simple print() for debugging (recommended)
print(f"[DEBUG] Handler initialized")
print(f"[INFO] Event matched: key={key}, action={action}")

# HiveSec logger API
from core.logger import info, error_traceback
info("Application started", __name__)
error_traceback(traceback.format_exc())
```

Log files stored in `/var/log/hivesec/` when using HiveSec logger.

## Linux Audit Integration

- Requires `auditctl` for runtime rule management
- Uses `augenrules` to reload rules from `.rules` files
- Events originate from audispd (Audispd daemon)
- Kernel boot parameter: `audit=1` enables audit at boot

## Best Practices

1. Always use `has_field(field)` to check field existence BEFORE accessing it
2. Use absolute paths for all file operations
3. Implement proper event filtering in `matches()` to handle high-volume logs efficiently
4. Consider threading (`threaded`) for blocking operations
5. Handle errors gracefully and log appropriately
6. Test handlers with sample audit events before deployment
7. Never access `_fields` directly - use the public API methods

### CORRECT FIELD ACCESS PATTERN (MUST FOLLOW)

**NEVER access `_fields` directly.** Always use the public API:

```python
# CORRECT pattern in matches() or _applies_to():
for record in event.records:
    # Check field exists FIRST, then get value
    if not record.has_field("key"):
        continue
    
    key = record.get_field_value("key").strip('"\'')  # Strip quotes manually
    
    if key != "flag_access":
        continue
    
    # Check name field exists before accessing it
    if not record.has_field("name"):
        continue
    
    if self.FLAG_FILE_PATH in record.get_field_value("name"):
        return True

return False  # Return False if NO records matched
```

**Common Mistakes to Avoid:**
- ❌ `record._fields["key"]` - Direct dict access bypasses API validation
- ❌ `record._fields.get("field", "default")` - AuditRecord has no `.get()` method!
- ❌ `record.get_field_value("field", "default")` - Only takes ONE parameter!
- ⚠️ Returning `True` when loop finds NO matching record
- ⚠️ Accessing `event.records[0]._fields` directly instead of using public API

## Testing Applications

After registration and reboot:
1. Add test rules via `hivectl` or your plugin
2. Trigger events (file access, config changes, etc.)
3. Check `/var/log/hivesec/hivesec.log` for handler logs
4. Verify response actions in application output

## Python Dependencies

To use Python libraries in an HiveSec application, install the base API first:
```bash
pip install hivesec
```

Then install additional dependencies in the HiveSec virtual environment:
```bash
sudo /usr/local/lib/hivesec/.venv/bin/pip install <package>
```

For installing dependencies via hivectl CLI:
```bash
sudo hivectl --install-dependency requests,pki
```

## Common Patterns

### Event Handler Example with Field Validation
```python
from hivesec import AuditEventHandler, AuditEvent

class FileAccessHandler(AuditEventHandler):
    def __init__(self):
        self.FLAG_FILE_PATH = "/path/to/file"
    
    def matches(self, event: AuditEvent) -> bool:
        try:
            for record in event.records:
                # Check key field exists and matches "flag_access"
                if not record.has_field("key"):
                    return False
                
                key = record.get_field_value("key").strip('"\'')
                if key != "flag_access":
                    return False
            
            return True  # All records matched criteria
        except ValueError:
            return False
    
    def handle(self, event: AuditEvent) -> None:
        try:
            record = event.records[0]
            
            # Check msg1 field exists before accessing it
            if not record.has_field("msg1"):
                raise ValueError("Missing msg1 field")
                
            # Extract serial number from audit message
            msg1_serial = record.get_field_value("msg1").split(":")[1]
            
            # Process the event...
            print(f"Processing event with serial: {msg1_serial}")
            
        except Exception as e:
            print(f"[ERROR] Failed to process event: {e}")

# Use in handler file without __init__ method if no extra state needed
```

### Rule Management Plugin Example
```python
import argparse
from hivesec import HivectlPlugin

class PasswdFilePlugin(HivectlPlugin):
    """Example hivectl plugin for /etc/passwd audit rules"""

    NAME = "passwd-file" 
    
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def init_args_parser(self, subparsers: argparse._SubParsersAction) -> None:
        parser = subparsers.add_parser(
            "passwd",
            help="Manage audit rules for /etc/passwd"
        )

        parser.add_argument("--add-rule", action="store_true")
        parser.add_argument("--remove-rules", action="store_true")

        parser.set_defaults(func=self.handle_command)

    def handle_command(self, args: argparse.Namespace) -> None:
        if args.add_rule:
            self._add_rule("-w /etc/passwd -p wa -k mypolicy")
            print("Rule enabled")

        elif args.remove_rules:
            self._clear_rules()
            print("Rules cleared")
```
