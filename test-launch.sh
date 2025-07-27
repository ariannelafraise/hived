./hived -s <<EOF
type=SYSCALL msg=audit(1752022100.814:201): arch=c000003e syscall=257 success=yes exit=3 a0=ffffff9c a1=563b51ddd6e0 a2=90800 a3=0 items=1 ppid=10720 pid=11390 auid=1000 uid=1000 gid=1000 euid=1000 suid=1000 fsuid=1000 egid=1000 sgid=1000 fsgid=1000 tty=pts1 ses=1 comm="ls" exe="/usr/bin/ls" key="filesystem"ARCH=x86_64 SYSCALL=openat AUID="arianne" UID="arianne" GID="arianne" EUID="arianne" SUID="arianne" FSUID="arianne" EGID="arianne" SGID="arianne" FSGID="arianne"
type=CWD msg=audit(1752022100.814:201): cwd="/home/arianne"
type=PATH msg=audit(1752022100.814:201): item=0 name="honeypot_folder/" inode=10885709 dev=103:06 mode=040755 ouid=1000 ogid=1000 rdev=00:00 nametype=NORMAL cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0OUID="arianne" OGID="arianne"
type=PROCTITLE msg=audit(1752022100.814:201): proctitle=6C73002D2D636F6C6F723D6175746F00686F6E6579706F745F666F6C6465722F
type=EOE msg=audit(1752022100.814:201):
type=SYSCALL msg=audit(1752022100.814:201): arch=c000003e syscall=257 success=yes exit=3 a0=ffffff9c a1=563b51ddd6e0 a2=90800 a3=0 items=1 ppid=10720 pid=11390 auid=1000 uid=1000 gid=1000 euid=1000 suid=1000 fsuid=1000 egid=1000 sgid=1000 fsgid=1000 tty=pts1 ses=1 comm="ls" exe="/usr/bin/ls" key="filesystem"ARCH=x86_64 SYSCALL=openat AUID="arianne" UID="arianne" GID="arianne" EUID="arianne" SUID="arianne" FSUID="arianne" EGID="arianne" SGID="arianne" FSGID="arianne"
type=CWD msg=audit(1752022100.814:201): cwd="/home/arianne"
type=PATH msg=audit(1752022100.814:201): item=0 name="honeypot_folder/" inode=10885709 dev=103:06 mode=040755 ouid=1000 ogid=1000 rdev=00:00 nametype=NORMAL cap_fp=0 cap_fi=0 cap_fe=0 cap_fver=0 cap_frootid=0OUID="arianne" OGID="arianne"
type=PROCTITLE msg=audit(1752022100.814:201): proctitle=6C73002D2D636F6C6F723D6175746F00686F6E6579706F745F666F6C6465722F
type=EOE msg=audit(1752022100.814:201):
EOF