# Getting Started: Developing HiveSec Applications

> [!IMPORTANT]
> You are strongly encouraged to read the python package source code (in the `api/` directory) to better understand the classes and methods available.
> It is very well documented and serves as a usage documentation. The following documentation aims to be a simple introduction to help grasp the basics.

## How to make applications
HiveSec applications can contain anything, as long as python files containing event handlers and/or hivectl plugins are present in the codebase.
At boot, the HiveSec daemon will scan each application directory registered in `/etc/hivesec/apps` and load any Python class extending `AuditEventHandler` or `HivectlPlugin`. Your entire application can be in Python, or just the event handling entrypoint. There is no specific application structure: just add a python file with a handler or plugin anywhere in the application's directory and it will be found and loaded by HiveSec.

### Installing dependencies
First, to develop HiveSec applications, install the `hivesec` Python package. It provides the framework and developer interface for building applications on top of HiveSec. Since HiveSec runs the application code in its own virtual environment, it's not actually needed to install it, but it is useful to install it for the language server (LSP).

```bash
pip install hivesec
```

Since HiveSec runs the application code in its own virtual environment, install any Python dependencies like this:
```bash
sudo hivectl -pip <package>
```

> [!IMPORTANT]
> Always use absolute paths, since the application code will be executed from a different working directory.

> [!CAUTION]
> Make sure that the directory containing your application is well protected with permissions to prevent bad
> actors from viewing and altering it, because the whole application will be ran as root.

### Creating an event handler
HiveSec uses the Observer design pattern to distribute events. To register your application as an observer, you need to create a handler class that inherits from `AuditEventHandler`:

```python
from hivesec import AuditEventHandler, AuditEvent

class MyHoneypotHandler(AuditEventHandler):
    
    def matches(self, event: AuditEvent) -> bool: 
        # Gets called by the event dispatcher to verify if the handler wants the event
        for record in event.records:
            if record.has_field("key"):
                if "honeypot" != record.get_field_value("key"):
                    return False
        return True
    
    def handle(self, event: AuditEvent):
        # Gets called by the event dispatcher to give the event to the handler
        print(f"Handling security event with {len(event.records)} records")
```

Event handlers receive `AuditEvent` objects, which are groups of records (`AuditRecord`) belonging to the same security event. `AuditRecord` fields are put into a Python dictionary.

> [!TIP]
> Use `record.json()` to retrieve the record in JSON format.

For example:

`msg=audit(1766092657.249:131): item=0 name="/etc/shadow"`

would give: 

```python
{
  "msg": "audit(1766092657.249:131):",
  "item": "0",
  "name": "/etc/shadow"
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

## Testing
Testing with real event triggers is difficult and time-consuming. Instead, use the `test-launch.sh` script to inject specific log records into HiveSec.

0. If not already done, create a Python virtual environment in `.venv` with `python -m venv .venv`. This will be used/needed by the `test-launch.sh` script. Since the HiveSec daemon will be ran from this venv, install any needed dependencies to it with `.venv/bin/pip install`

1. Create a file containing the sample of logs you want to use to test

sample.txt
```
type=SYSCALL msg=audit(1782085825.872:50): arch=c000003e syscall=257 success=yes exit=3 a0=ffffffffffffff9c a1=7f0d8c7f1ee8 a2=341 a3=1b6 items=1 ppid=300290 pid=300298 auid=1000 uid=1000 gid=1000 euid=1000 suid=1000 fsuid=1000 egid=1000 sgid=1000 fsgid=1000 tty=pts1 ses=3 comm="zsh" exe="/usr/bin/zsh" key="flag_access"
type=PATH msg=audit(1782085825.872:50): item=0 name="flag.txt" inode=49295866 dev=103:03 mode=0100644 ouid=1000 ogid=1000 rdev=00:00 nametype=NORMAL cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0
```

2. Launch the test with it

```bash
sudo ./test-launch.sh sample.txt
```
