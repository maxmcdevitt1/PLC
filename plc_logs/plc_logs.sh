#!/usr/bin/env bash
PLC_IP="192.168.10.10"
LOG_FILE="$HOME/plc/plc_logs/plc_ping.csv"

if [ ! -f "$LOG_FILE" ]; then
	echo "timestamp,status" > "$LOG_FILE"
fi

while true; do
	if ping -c 1 -W 1 "$PLC_IP" > /dev/null 2>&1; then
		echo "$(date -Iseconds),up" >> "$LOG_FILE"
	else

		echo "$(date -Iseconds),down" >> "$LOG_FILE"
	fi
	sleep 1
done
