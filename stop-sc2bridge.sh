#!/bin/bash
PIDFILE="/tmp/sc2bridge.pid"

if [ ! -f "$PIDFILE" ]; then
    echo "Steam Controller 2 Bridge does not appear to be running."
    exit 0
fi

PID="$(cat "$PIDFILE")"

if kill -0 "$PID" 2>/dev/null; then
    kill "$PID"
    sleep 1
fi

rm -f "$PIDFILE"
echo "Steam Controller 2 Bridge stopped."
