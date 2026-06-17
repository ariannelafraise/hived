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

printf "%b==>%b Removing audit plugin...\n" "$C_MAGENTA" "$C_RESET"
rm -f /etc/audit/plugins.d/hivesec.conf
printf "%b[ OK ]%b Plugin removed\n" "$C_GREEN" "$C_RESET"

printf "%b==>%b Removing hivectl command...\n" "$C_MAGENTA" "$C_RESET"
rm -f /usr/local/bin/hivectl
printf "%b[ OK ]%b hivectl removed\n" "$C_GREEN" "$C_RESET"

printf "%b==>%b Removing HiveSec application files...\n" "$C_MAGENTA" "$C_RESET"
rm -rf /usr/local/lib/hivesec
printf "%b[ OK ]%b Files removed\n" "$C_GREEN" "$C_RESET"

printf "%b==>%b Removing system directories...\n" "$C_MAGENTA" "$C_RESET"
rm -rf /etc/hivesec
rm -rf /var/log/hivesec
printf "%b[ OK ]%b System directories removed\n" "$C_GREEN" "$C_RESET"

printf "%bUninstall complete.%b\n" "$C_GREEN" "$C_RESET"