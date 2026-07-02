#!/usr/bin/env bash
set -e

C_RESET="\033[0m"
C_DIM="\033[2m"
C_BLUE="\033[38;5;111m"
C_GREEN="\033[38;5;150m"
C_YELLOW="\033[38;5;229m"
C_MAGENTA="\033[38;5;183m"
C_CYAN="\033[38;5;159m"
C_RED="\033[38;5;174m"

printf "%b==>%b Checking privileges...\n" "$C_MAGENTA" "$C_RESET"
if [ "$EUID" -ne 0 ]; then
    printf "%b[ WARN ]%b Please run as root\n" "$C_YELLOW" "$C_RESET"
    exit 1
fi
printf "%b[ OK ]%b Root confirmed\n" "$C_GREEN" "$C_RESET"

printf "%b==>%b Pulling changes from source repository...\n" "$C_MAGENTA" "$C_RESET"
if [[ $1 == "local" ]]; then
    cp -r ../hivesec /usr/local/src/hivesec
else
    git -C /usr/local/src/hivesec pull
fi
printf "%b[ OK ]%b Changes pulled\n" "$C_GREEN" "$C_RESET"

printf "%b==>%b Installing application files...\n" "$C_MAGENTA" "$C_RESET"
cp -r /usr/local/src/hivesec /usr/local/lib/hivesec
printf "%b[ OK ]%b Files copied\n" "$C_GREEN" "$C_RESET"

printf "%b==>%b Updating Python virtual environment...\n" "$C_MAGENTA" "$C_RESET"
/usr/local/lib/hivesec/.venv/bin/pip install -e /usr/local/lib/hivesec/api
printf "%b[ OK ]%b Virtual environment updated\n" "$C_GREEN" "$C_RESET"

printf "%b==>%b Ensuring secure permissions...\n" "$C_MAGENTA" "$C_RESET"
# Ensure root ownership
chown -R root:root /usr/local/lib/hivesec
chown root:root /usr/local/bin/hivectl
chown -R root:root /etc/hivesec
chown -R root:root /var/log/hivesec

# Base permissions
find /usr/local/lib/hivesec -type d -exec chmod 755 {} \;
find /usr/local/lib/hivesec -type f -exec chmod 644 {} \;

# Executables
chmod 755 /usr/local/lib/hivesec/.venv
chmod 755 /usr/local/lib/hivesec/.venv/bin
chmod 755 /usr/local/lib/hivesec/.venv/bin/python
chmod 755 /usr/local/lib/hivesec/.venv/bin/pip
chmod 755 /usr/local/bin/hivectl

# Root only
chmod 700 /etc/hivesec
chmod 600 /etc/hivesec/apps
chmod 700 /var/log/hivesec
printf "%b[ OK ]%b Secure permissions ensured\n" "$C_GREEN" "$C_RESET"

printf "%bUpdate complete.%b\n" "$C_GREEN" "$C_RESET"
