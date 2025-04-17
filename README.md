# PiCrawler + PS5 Controller + PiCamera Control

Control SunFounder PiCrawler and view real-time camera feed using a PS5 DualSense controller (Bluetooth or USB). Supports live video, joystick axis display, and real-time video recording.

---

## 🔧 Features

- 🎮 Use PS5 joystick to control forward/backward/left/right
- 📷 Display real-time video feed using PiCamera
- 🔴 Press X button to start/stop recording, videos saved automatically
- 🧭 Display joystick input (X/Y) on screen overlay

---

## ▶️ How to Run

```bash
python3 crawler_joystick_camera.py
```

Press `q` in the OpenCV window to quit. Recordings are saved as `record_YYYYMMDD_HHMMSS.avi`.

---

## 📦 Dependencies

```bash
sudo apt update
sudo apt install -y python3-picamera2 python3-opencv python3-pygame picrawler

```

---

## 🎮 Connecting PS5 Controller via Bluetooth

To automatically scan and connect your PS5 DualSense controller:

1. Put your controller in pairing mode (hold **PS + Share** until light bar flashes).
2. Run the provided script:

```bash
chmod +x connect_dualsense.sh
./connect_dualsense.sh
```

This script will:

- Power on Bluetooth
- Scan for nearby devices
- Auto-detect the controller named `"Wireless Controller"`
- Pair, trust, and connect to it

If the controller is not detected, make sure it's in pairing mode and try again.

---

## 🕹 Joystick Control Reference

| Input                 | Action                      |
| --------------------- | --------------------------- |
| Left Stick Up/Down    | Move Forward / Backward     |
| Left Stick Left/Right | Turn Left / Right           |
| X Button (Button 0)   | Toggle Start/Stop Recording |

---

## 💡 Notes

- The script must be run from a desktop environment (not over SSH) to show the OpenCV window.
- For headless use, consider remote desktop tools like VNC.
