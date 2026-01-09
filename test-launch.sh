./hived -s <<EOF
type=SYSCALL msg=audit(1766092657.249:131): arch=c000003e syscall=257 success=yes exit=3 a0=ffffffffffffff9c a1=7fa9efb60b40 a2=80000 a3=0 items=1 ppid=901 pid=906 auid=4294967295 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=(none) ses=4294967295 comm="hived" exe="/usr/bin/python3.13" key="filesystem"
type=CWD msg=audit(1766092657.249:131): cwd="/"
type=PATH msg=audit(1766092657.249:131): item=0 name="/home/arianne/personal_dev/hived/__pycache__/config.cpython-313.pyc" inode=10886263 dev=103:06 mode=0100644 ouid=0 ogid=0 rdev=00:00 nametype=NORMAL cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0
type=PROCTITLE msg=audit(1766092657.249:131): proctitle=2F7573722F62696E2F707974686F6E002F686F6D652F617269616E6E652F706572736F6E616C5F6465762F68697665642F6869766564002D73
type=EOE msg=audit(1766092657.249:131):
EOF
# Put any audit event between EOF to test
