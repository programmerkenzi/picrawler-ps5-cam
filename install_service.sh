#!/bin/bash
SERVICE_PATH="/etc/systemd/system/picrawler.service"
SCRIPT_PATH="/home/pi/picrawler-ps5-cam/crawler_joystick_camera.py"

echo "[🔧] Creating systemd service for PiCrawler..."

sudo tee $SERVICE_PATH > /dev/null <<EOF
[Unit]
Description=PiCrawler PS5 Camera Control Service
After=multi-user.target
Wants=network.target bluetooth.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/picrawler-ps5-cam
ExecStart=/usr/bin/python3 $SCRIPT_PATH
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable picrawler.service
sudo systemctl start picrawler.service

echo "[✅] Service installed and started successfully."
