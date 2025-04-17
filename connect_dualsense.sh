#!/bin/bash
# Auto connect PS5 DualSense controller

MAC_ADDRESS="12:34:56:78:9A:BC"  # Replace with your controller's MAC

bluetoothctl <<EOF
power on
agent on
default-agent
connect $MAC_ADDRESS
EOF
