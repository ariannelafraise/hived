# Hived
Hived is a extensible tool built on top of the Linux Audit framework that helps to setup honeypots on your linux machines.
It provides an extension/plugin API, to add custom features.

## Context
The Linux Audit framework records various system calls and logs them.
The Auditd daemon sends logs to either the `audit.log` file or Audispd.
The latter feeds those logs to registered plugins. This is where Hived comes in.
It forwards those events to **event handlers** that analyze them and act accordingly.
They could send email notifications to sysadmins, or even take proper action to eliminate a threat.
If it can be programmed, it can be done. That is the goal of Hived: Intrusion Detection and Prevention (IPS/IDS).

Other more fun idea of Hived usage: perhaps a tool to put in place in a CTF box to add more challenge?
What if, when the player does certain actions like accessing an honey pot file, the box would harden its security?
Or cut the connection and reset progress? That'd be interesting! :p

![audit framework diagram](./documentation/linux-audit-architecture.png)

[(source)](https://www.researchgate.net/figure/Linux-Auditd-Architecture_fig2_355181208)

### Interesting resources to better understand the Audit Framework
[Red Hat Documentation - Chapter 7. System Auditing](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/security_guide/chap-system_auditing)

### Where do events come from?
The Audit Framework uses rules to know which events it should record, and in what way.
You can also associate keys to rules to better identify events that were recorded thanks to the rules.
Here is an example:

`-a always,exit -F arch=b64 -F dir=/home/arianne/honeypot_folder -F perm=rw -F key=filesystem`

You can better understand rules with [this incredible article from Red Hat](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/security_guide/sec-Defining_Audit_Rules_and_Controls#sec-Defining_Audit_Rules_with_auditctl).

> [!NOTE]
> Hivectl plugins can add their own rules.

### Understanding events and logs
Events are composed of logically tied logs. Those logs are strings composed of key/value
entries separated by white spaces. Here is an example:

`type=CWD msg=audit(1752022100.814:201): cwd="/home/arianne"`

As you can see, logs have different types. The most important ones are `SYSCALL` and `EOE`.
SYSCALL usually marks the start of an event, while EOE (End Of Event) marks,
you guessed it, the end of and event. That is how we can identify all the logs tied to a specific event.
A full event would look like this:

```text
type=SYSCALL msg=audit(1752022100.814:201): arch=c000003e syscall=257 success=yes exit=3 a0=ffffff9c a1=563b51ddd6e0 a2=90800 a3=0 items=1 ppid=10720 pid=11390 auid=1000 uid=1000 gid=1000 euid=1000 suid=1000 fsuid=1000 egid=1000 sgid=1000 fsgid=1000 tty=pts1 ses=1 comm="ls" exe="/usr/bin/ls" key="filesystem"ARCH=x86_64 SYSCALL=openat AUID="arianne" UID="arianne" GID="arianne" EUID="arianne" SUID="arianne" FSUID="arianne" EGID="arianne" SGID="arianne" FSGID="arianne"
type=CWD msg=audit(1752022100.814:201): cwd="/home/arianne"
type=PATH msg=audit(1752022100.814:201): item=0 name="honeypot_folder/" inode=10885709 dev=103:06 mode=040755 ouid=1000 ogid=1000 rdev=00:00 nametype=NORMAL cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0OUID="arianne" OGID="arianne"
type=PROCTITLE msg=audit(1752022100.814:201): proctitle=6C73002D2D636F6C6F723D6175746F00686F6E6579706F745F666F6C6465722F
type=EOE msg=audit(1752022100.814:201):
```

This is an event that was triggered by accessing a folder using the `ls` command.
We can see that this event was recorded by the rule that we defined earlier, thanks to the key.

> [!TIP]
> the PROCTITLE log gives the command that was executed in an HEX format.
> You can replace '00' with '20' to have valid white spaces.
> 6C73002D2D636F6C6F723D6175746F00686F6E6579706F745F666F6C6465722F = ls --color=auto honeypot_folder/

## How does Hived function?
> [!IMPORTANT]
> Refer to this UML class diagram to better understand this section.
> ![uml diagram](./documentation/hived.drawio.png)

There are two main components: Hived and Hivectl.
### Hived
The daemon ran by Audispd that receives all events recorded by the framework.
All events are listened by the AudispdListener, which dynamically loads all event handlers
defined in the `event_handlers` directory and alerts them of new events by following the Observer design pattern.
These event handlers can also use notifiers to send out notifications, like emails.
> [!IMPORTANT]
> Running Hived on its own has no effect, it **needs** to be run by Audispd to receive events.
> However, it allows you to feed it your own logs for testing purposes.

> [!NOTE]
> You can create your own custom event handlers and notifiers by referring to the Plugin/Extension API section.

### Hivectl
A CLI tool to configure Hived and the Audit framework. It dynamically loads plugins defined in the `plugins` directory.
Specific plugin commands can be accessed by specifying the name of the plugin as such:
```bash
# hivectl [plugin name] [command]
```

Get help on Hivectl usage:
```bash
# hivectl -h
# hivectl [plugin name] -h
```

> [!IMPORTANT]
> Hivectl needs to be run as root since it performs administrative tasks such as configuring the audit framework.

> [!NOTE]
> You can create your own custom plugins by referring to the Plugin/Extension API section.

## Plugin/Extension API
> [!IMPORTANT]
> Refer to the UML class diagram shown earlier to better understand this section.

There are three ways of adding your own functionalities: event handlers, notifiers and hivectl plugins.
### Event handlers
These are loaded dynamically by AudispdListener from the `event_handlers` directory. The Observer design pattern is used 
to feed every new event received by AudispdListener all event handlers. 

They should implement the EventHandler interface that defines two methods: applies_to(e: Event) and handle(e: Event).

- handle() is the method that will be called on each new event.
- applies_to() should be called at the beginning of handle() to decide if the event handler should act on or ignore the event.

Code example:
```python
class ExampleEventHandler(EventHandler):
    def _applies_to(self, event: Event) -> bool:
        logs_str = ""
        for log in event.logs:
            logs_str += log.as_string
        if "key=\"example\"" in logs_str:
            return True
        return False

    def handle(self, event: Event):
        if not self._applies_to(event):
            return

        [do stuff]
```
### Notifiers
These can be used by event handlers to send out notifications, like emails.

They should implement the Notifier interface, as utility classes (they are not meant to be instantiated).
It defines the notify(sender: str, message: str) method, which fires the notification.

Code example:
```python
class ExampleNotifier(Notifier):
    @staticmethod
    def notify(sender: str, message: str):
        [send out notification]
```
### Hivectl plugins
These are loaded dynamically by Hivectl from the `plugins` directory. They extend Hivectl's functionalities by adding
commands using the argparse library. Hivectl calls the init_args_parser 

They should implement the Plugin interface, as utility classes (they are not meant to be instantiated).
It defines two methods: init_args_parser(subparser: argparse._SubParsersAction) and handle_command(args: argparse.Namespace).

- init_args_parser() adds its own command subparser Hivectl's main parser. Hivectl calls this function for each plugin and feeds it its main parser.
- handle_command() handles all commands received by the plugins subparser.

Code example:
```python
class ExamplePlugin(Plugin):
    @staticmethod
    def init_args_parser(subparser: argparse._SubParsersAction):
        parser = subparser.add_parser("example-plugin")
        parser.set_defaults(func=ExamplePlugin.handle_command) # Defines the handle_command() method as the handling function
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-v', '--version', help='View currently installed version.', action='version', version=f"example-plugin v1")
        group.add_argument('-w', '--hello', help='Say hello', action="store_true")

    @staticmethod
    def handle_command(args: argparse.Namespace):
        if args.hello:
            print("Hello, World!")
```
## Installation
### 1. Clone the repository or download one of the releases.
### 2. Boot configuration
For best results, the Audit framework should be enabled at boot-time by setting `audit=1` as a kernel parameter.
#### For GRUB
edit /etc/default/grub
```
GRUB_CMDLINE_LINUX_DEFAULT="[other options ...] audit=1"
```
Load config:
```bash
# grub-mkconfig -o /boot/grub/grub.cfg
```
### 3. Audispd configuration
create /etc/audit/audisp.conf
```
q_depth = 80
overflow_action = syslog
priority_boost = 4
max_restarts = 10
name_format = hostname
```
create /etc/audit/plugins.d/hived.conf
```
active = yes
direction = out
path = [absolute path to hived python executable]
type = always
args = -s
format = string
```
### 4. Make `hived` owned by root (needed for it to be run by Audispd)
```bash
# chown root hived
```
### 5. Make sure config.py has the right absolute paths for your machine.
### 6. Make sure that the .env file has the needed variables for your plugins, event handlers and notifiers.

## Troubleshooting
Some useful commands:
```bash
# systemctl status auditd
list active rules
# auditctl -l
```