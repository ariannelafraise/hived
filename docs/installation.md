## Installation (WIP)

### 1. Clone this repository

### 2. Boot configuration (optional)
For best results, Linux Audit should be enabled at boot-time by setting `audit=1` as a kernel parameter.

#### For GRUB
edit `/etc/default/grub`
```
GRUB_CMDLINE_LINUX_DEFAULT="[other options ...] audit=1"
```
Load config:
```bash
grub-mkconfig -o /boot/grub/grub.cfg
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
### 4. Make `hivesecd.py` owned by root (needed for it to be run by Audispd)
```bash
chown root hivesecd.py
```
### 5. Make sure config.py has the right absolute paths for your machine.
### 6. Make sure that the .env file has the needed variables for your plugins, event handlers and notifiers.
