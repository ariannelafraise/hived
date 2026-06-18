# Getting Started: Developing HiveSec Applications

> [!IMPORTANT]
> You are strongly encouraged to read the python package source code (in the `api/` directory) to better understand the classes and methods available.
> It is very well documented and serves as a usage documentation. The following documentation aims to be a simple introduction to help grasp the basics.

## Installing the API
First, to develop HiveSec applications, install the `hivesec` Python package. It provides the framework and developer interface for building applications on top of HiveSec.

```bash
pip install hivesec
```

## How to make applications
HiveSec applications can contain anything, as long as python files containing event handlers and/or hivectl plugins are present in the codebase.
At boot, the HiveSec daemon will scan each application directory registered in `/etc/hivesec/apps` and load any Python class extending `AuditEventHandler` or `HivectlPlugin`. Your entire application can be in Python, or just the event handling entrypoint. There is no specific application structure: just add a python file with a handler or plugin anywhere in the application's directory and it will be found and loaded by HiveSec.

> [!IMPORTANT]
> Make sure to always use absolute paths, since your code will be executed from a different working directory.

> [!CAUTION]
> Make sure that the directory containing your application is well protected with permissions to prevent bad
> actors from viewing and altering it, because the whole application will be ran as root.

### Creating an event handler
HiveSec uses the Observer design pattern to distribute events. To register your application as an observer, you need to create a handler class that inherits from `AuditEventHandler`:

```python
from hivesec import AuditEventHandler, AuditEvent

class MyHoneypotHandler(AuditEventHandler):
    """Example honeypot event handler"""
    
    def _applies_to(self, event: AuditEvent) -> bool:
        """Check if this event should be handled"""
        for record in event.records:
            if "honeypot12" != record.get_field_value("key"):
                return False
        return True
    
    def handle(self, event: AuditEvent):
        """Process the audit event"""
        print(f"Processing security event with {len(event.records)} records")
```

Event handlers receive `AuditEvent` objects, which are groups of records (`AuditRecord`) belonging to the same security event. `AuditRecord` fields are put into a Python dictionary. The keys and values are kept intact from the original log string, only the '=' sign between the two is removed.

For example:

`msg=audit(1766092657.249:131): item=0 name="/etc/shadow"`

would give: 

```python
{
  "msg": "audit(1766092657.249:131):",
  "item": "0",
  "name": '"/etc/shadow"'
}
```

### Creating a hivectl plugin
Plugins extend hivectl with new functionality. They are particularly useful to make commands to interact with your application, such as a command to set up Linux Audit rules needed by your application.

To create a plugin, you need to create a plugin class that inherits from `HivectlPlugin`:

```python
import argparse
from hivesec import HivectlPlugin

class PasswdFilePlugin(HivectlPlugin):
    """Example hivectl plugin"""

    NAME = "passwd-file" 
    # Set a name for your plugin, will be the name 
    # of the file storing the rules associated with it

    def __init__(self) -> None:
        super().__init__(self.NAME)

    def init_args_parser(self, subparsers: argparse._SubParsersAction):
        parser = subparsers.add_parser(
            "passwd",
            help="Manage audit rules for /etc/passwd"
        )

        parser.add_argument("--add-rule", action="store_true")
        parser.add_argument("--remove-rules", action="store_true")

        parser.set_defaults(func=self.handle_command)

    def handle_command(self, args: argparse.Namespace):
        if args.add_rule:
            self._add_rule("-w /etc/passwd -p wa -k mypolicy")
            print("Rule enabled")

        elif args.remove_rules:
            self._clear_rules()
            print("Rules cleared")
```

### Registering the application to HiveSec

1. Add its absolute path directory to `/etc/hivesec/apps`

by editing the file directly:
```
/home/winnie/honeypot-app
```
or by running:
```bash
sudo hivectl --register ABSOLUTE_PATH
```
2. Reboot to let HiveSec detect and load your new application.
