#!/bin/bash

echo "[🔵] Starting Bluetooth scan for PS5 controller..."

bluetoothctl << EOF | tee /tmp/bt_scan.log
power on
agent on
default-agent
scan on
EOF

sleep 6

# 取得 MAC 位址
MAC=$(grep -i "Wireless Controller" /tmp/bt_scan.log | tail -n1 | awk '{print $3}')

if [ -z "$MAC" ]; then
  echo "[❌] No PS5 controller found. Make sure it's in pairing mode (PS + Share)..."
  exit 1
fi

echo "[🎮] Found PS5 controller at $MAC. Connecting..."

bluetoothctl << EOF
scan off
pair $MAC
trust $MAC
connect $MAC
EOF

echo "[✅] Controller connected."
