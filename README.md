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
python3 main.py
```

Press `q` in the OpenCV window to quit. Recordings are saved as `record_YYYYMMDD_HHMMSS.avi`.

---

## 📦 Dependencies

```bash
sudo apt update
sudo apt install -y python3-picamera2 python3-opencv python3-pygame picrawler espeak
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

## ⚙️ Auto Start Instructions

This repository includes `systemd` service support to auto-run the PiCrawler joystick + camera control on boot.

### ▶️ Install the service on boot

```bash
chmod +x install_service.sh
./install_service.sh
```

This will:

- Register a `systemd` unit at `/etc/systemd/system/picrawler.service`
- Start the service immediately
- Enable it on system boot

---

### 🗑 Uninstall the service

```bash
chmod +x uninstall_service.sh
./uninstall_service.sh
```

This will:

- Stop the service
- Disable auto-start on boot
- Remove the `systemd` unit file

---

### 💡 Notes

- The service runs the `main.py` script using `python3`
- It is executed under the `pi` user by default (or current user if customized)
- You can check the service logs using:
  ```bash
  journalctl -u picrawler.service -f
  ```

---

## 🕹 Joystick Control Reference

| Input                 | Action                      |
| --------------------- | --------------------------- |
| Left Stick Up/Down    | Move Forward / Backward     |
| Left Stick Left/Right | Turn Left / Right           |
| X Button (Button 0)   | Toggle Start/Stop Recording |
| ⬜ Button (Button 3)  | Toggle Camera Display       |

---

## 💡 Notes

- The script must be run from a desktop environment (not over SSH) to show the OpenCV window.
- For headless use, consider remote desktop tools like VNC.
