# PiCrawler + PS5 Controller + PiCamera Control

Control SunFounder PiCrawler and view real-time camera feed using a PS5 DualSense controller (Bluetooth or USB). Supports live video, joystick axis display, and real-time video recording.

## Features
- 🎮 Use PS5 joystick to control forward/backward/left/right
- 📷 Display real-time video feed using PiCamera
- 🔴 Press X button to start/stop recording, videos saved automatically
- 🧭 Display joystick input (X/Y) on screen

## How to Run
```bash
python3 crawler_joystick_camera.py
```

Press `q` in the OpenCV window to quit. Recordings are saved as `record_YYYYMMDD_HHMMSS.avi`.

## Dependencies
```bash
sudo apt update
sudo apt install python3-pip python3-opencv python3-pygame -y
pip3 install picamera[array]
```

## Connect PS5 Controller via Bluetooth
You can use the provided script `connect_dualsense.sh` to pair automatically.

## Joystick Controls
| Input | Action |
|-------|--------|
| Left Stick Up/Down | Move Forward / Backward |
| Left Stick Left/Right | Turn Left / Right |
| X Button | Toggle Recording |
