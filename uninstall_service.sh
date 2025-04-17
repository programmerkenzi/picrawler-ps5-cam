#!/bin/bash
SERVICE_PATH="/etc/systemd/system/picrawler.service"

echo "[🧹] Stopping and disabling PiCrawler service..."

sudo systemctl stop picrawler.service
sudo systemctl disable picrawler.service
sudo rm -f $SERVICE_PATH
sudo systemctl daemon-reload

echo "[✅] Service removed successfully."
