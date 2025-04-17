#!/bin/bash
# Auto-run PiCrawler joystick + camera control

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Starting PiCrawler Joystick + Camera Control..."
python3 crawler_joystick_camera.py
