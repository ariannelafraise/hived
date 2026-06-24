if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

if [[ -z $1 ]]; then
    echo "usage: ./test-launch.sh <path-to-sample-file-to-test>"
    exit 2
fi

cat $1 | .venv/bin/python hivesecd.py -s
