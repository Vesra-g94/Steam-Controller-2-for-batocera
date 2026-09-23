#!/bin/bash
SCRIPT="/userdata/system/sc2bridge.py"
LOG="/userdata/system/logs/sc2bridge.log"
PIDFILE="/tmp/sc2bridge.pid"

mkdir -p "/userdata/system/logs"

if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
    echo "Steam Controller 2 Bridge is already running. PID $(cat "$PIDFILE")"
    exit 0
fi

python3 "$SCRIPT" >> "$LOG" 2>&1 &
echo $! > "$PIDFILE"

sleep 1

if kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
    echo "Steam Controller 2 Bridge started. PID $(cat "$PIDFILE")"
    echo "Log: $LOG"
else
    echo "Bridge failed to start. Check:"
    echo "  $LOG"
    rm -f "$PIDFILE"
    exit 1
fi
