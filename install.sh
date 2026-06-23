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

printf "%b==>%b Cloning source repository...\n" "$C_MAGENTA" "$C_RESET"
cd /usr/local/src
rm -rf hivesec
git clone https://github.com/ariannelafraise/hivesec.git
cd hivesec
printf "%b[ OK ]%b Repository ready\n" "$C_GREEN" "$C_RESET"

printf "%b==>%b Installing application files...\n" "$C_MAGENTA" "$C_RESET"
rm -rf /usr/local/lib/hivesec
mkdir -p /usr/local/lib/hivesec
cp -r core /usr/local/lib/hivesec/
cp __version__.py hivectl.py hivesecd.py /usr/local/lib/hivesec/
printf "%b[ OK ]%b Files copied\n" "$C_GREEN" "$C_RESET"

printf "%b==>%b Creating Python virtual environment...\n" "$C_MAGENTA" "$C_RESET"
python3 -m venv /usr/local/lib/hivesec/.venv
/usr/local/lib/hivesec/.venv/bin/pip install hivesec
printf "%b[ OK ]%b Virtual environment ready\n" "$C_GREEN" "$C_RESET"

printf "\033[38;5;183m==>\033[0m Writing audisp configuration...\n"
echo "" > /etc/audit/audisp.conf
cat >/etc/audit/audisp.conf <<'EOF'
q_depth = 80
overflow_action = syslog
priority_boost = 4
max_restarts = 10
name_format = hostname
EOF
printf "\033[38;5;150m[ OK ]\033[0m audisp.conf written\n"

printf "\033[38;5;183m==>\033[0m Installing HiveSec audit plugin...\n"
echo "" > /etc/audit/plugins.d/hivesec.conf
cat >/etc/audit/plugins.d/hivesec.conf <<'EOF'
active = yes
direction = out
path = /usr/local/lib/hivesec/.venv/bin/python
type = always
args = /usr/local/lib/hivesec/hivesecd.py -s
format = string
EOF
printf "\033[38;5;150m[ OK ]\033[0m HiveSec plugin configured\n"

printf "\033[38;5;183m==>\033[0m Configuring Auditd to log in raw format...\n"
sed -i "s/log_format = ENRICHED/log_format = RAW/g" /etc/audit/auditd.conf
printf "\033[38;5;150m[ OK ]\033[0m Auditd configured to log in raw format\n"

printf "%b==>%b Creating hivectl command...\n" "$C_MAGENTA" "$C_RESET"
echo "" > /usr/local/bin/hivectl
cat >/usr/local/bin/hivectl <<'EOF'
#!/usr/bin/env bash
exec /usr/local/lib/hivesec/.venv/bin/python /usr/local/lib/hivesec/hivectl.py "$@"
EOF
chmod 700 /usr/local/bin/hivectl
printf "%b[ OK ]%b hivectl command ready\n" "$C_GREEN" "$C_RESET"

printf "%b==>%b Setting up system directories...\n" "$C_MAGENTA" "$C_RESET"
mkdir -p /var/log/hivesec
mkdir -p /etc/hivesec

if [[ ! -f /etc/hivesec/apps ]]; then
    echo "# Add external applications' absolute paths here to register them." >/etc/hivesec/apps
fi
printf "%b[ OK ]%b System directories ready\n" "$C_GREEN" "$C_RESET"

printf "\033[38;5;183m==>\033[0m Setting secure permissions...\n"
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
printf "\033[38;5;150m[ OK ]\033[0m Permissions applied\n"

printf "%b==>%b Cleaning up...\n" "$C_MAGENTA" "$C_RESET"
cd /
rm -rf /usr/local/src/hivesec
printf "%b[ OK ]%b Cleanup complete\n" "$C_GREEN" "$C_RESET"

printf "%bInstallation complete.%b\n" "$C_GREEN" "$C_RESET"
