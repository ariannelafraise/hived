# Installation

## Requirements
To use HiveSec you need a Linux system with:
- Bash
- Git
- Python 3.10 or higher
- Linux Audit

## Installation

> [!IMPORTANT]
> Make sure to use the right version script depending on the version you wish to install/uninstall

To install HiveSec, simply run the installation script:
```bash
curl -sL https://raw.githubusercontent.com/ariannelafraise/hivesec/refs/heads/main/install.sh | sudo bash
```

To uninstall, use this script:
```bash
curl -sL https://raw.githubusercontent.com/ariannelafraise/hivesec/refs/heads/main/uninstall.sh | sudo bash
```

## Boot configuration (optional)
For best results, Linux Audit should be enabled at boot-time by setting `audit=1` as a kernel parameter.

### For GRUB
edit `/etc/default/grub`
```
GRUB_CMDLINE_LINUX_DEFAULT="[other options ...] audit=1"
```
Load config:
```bash
grub-mkconfig -o /boot/grub/grub.cfg
```
