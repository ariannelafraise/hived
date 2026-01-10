# Hived
Hived is a extensible tool built on top of the Linux Audit framework that helps to setup honeypots on your linux machines.
It provides an extension/plugin API, to add custom features.

## Context
The Linux Audit framework records various system events and logs them.
The Auditd daemon sends these logs to either the `audit.log` file or Audispd.
The latter feeds those logs to registered plugins. This is where Hived comes in.
It forwards those events to audit event handlers that analyze them and act accordingly.

![audit framework diagram](./documentation/linux-audit-architecture.png)

[(source)](https://www.researchgate.net/figure/Linux-Auditd-Architecture_fig2_355181208)

### Interesting resources to better understand the Audit Framework
- [Red Hat Documentation - Chapter 7. System Auditing](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/security_guide/chap-system_auditing)
- [The Linux Audit Project (Github organization)](https://github.com/linux-audit)

## How does Hived function?
There are two main components: Hived and Hivectl.

### Hived
The daemon (registered as a plugin to Audispd) that receives all logged events and forwards them to audit event handlers.

> [!IMPORTANT]
> Running Hived on its own has no effect, it **needs** to be run by Audispd to receive events.
> However, it allows you to feed it your own logs for testing purposes.

> [!NOTE]
> You can create your own custom event handlers and notifiers by referring to the Plugin/Extension API section.

### Hivectl
A CLI tool to configure Hived.

> [!IMPORTANT]
> Hivectl needs to be run as root since it performs administrative tasks such as configuring the audit framework.

## Installation
### 1. Clone this repository
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
