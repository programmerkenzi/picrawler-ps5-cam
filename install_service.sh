#!/bin/bash

SERVICE_NAME=picrawler.service
SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME"

# Auto-detect current user if not explicitly set
USER=${1:-$(whoami)}
SCRIPT_DIR="/home/$USER/picrawler-ps5-cam"
SCRIPT_PATH="$SCRIPT_DIR/main.py"

echo "[🔧] Creating systemd service for PiCrawler..."

sudo tee $SERVICE_PATH > /dev/null <<EOF
[Unit]
Description=PiCrawler PS5 Camera Control Service
After=multi-user.target
Wants=network.target bluetooth.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$SCRIPT_DIR
ExecStart=/usr/bin/python3 $SCRIPT_PATH
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

echo "[✅] Service '$SERVICE_NAME' installed and started successfully."
