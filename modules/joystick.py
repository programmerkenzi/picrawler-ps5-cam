import pygame
import time
import subprocess
from picrawler import Picrawler
import shared.state as state  # ✅ 重點
from modules.voice import say

robot = Picrawler()


def joystick_control():
    pygame.init()
    pygame.joystick.init()

    try:
        if pygame.joystick.get_count() == 0:
            print("🔌 No controller detected. Attempting to connect via Bluetooth...")
            retry_limit = 3
            for attempt in range(retry_limit):
                print(f"🔄 Attempt {attempt + 1} to connect controller...")
                subprocess.call(["./connect_dualsense.sh"])
                time.sleep(3)
                pygame.joystick.quit()
                pygame.joystick.init()
                if pygame.joystick.get_count() > 0:
                    break
            if pygame.joystick.get_count() == 0:
                print("❌ Failed to connect controller after multiple attempts.")
                return

        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print(f"🎮 Controller connected: {joystick.get_name()}")
        say("Controller connected")
    except pygame.error:
        print("⚠️ No controller found. Please connect your PS5 controller.")
        return

    while True:
        pygame.event.pump()
        x = joystick.get_axis(0)
        y = joystick.get_axis(1)
        state.joy_status["x"] = x
        state.joy_status["y"] = y

        max_speed = 100
        axis_magnitude = max(abs(x), abs(y))
        speed = int(max_speed * axis_magnitude)
        deadzone = 0.3

        try:
            if y < -deadzone:
                robot.do_action("forward", 1, speed)
            elif y > deadzone:
                robot.do_action("backward", 1, speed)
            elif x < -deadzone:
                robot.do_action("turn left", 1, speed)
            elif x > deadzone:
                robot.do_action("turn right", 1, speed)
            else:
                time.sleep(0.1)
        except Exception as e:
            print(f"[Error] {e}")

        if joystick.get_button(3):
            if not state.camera_toggle_pressed:
                state.show_camera = not state.show_camera
                print("📷 Camera display: " + ("ON" if state.show_camera else "OFF"))
                say("Camera on" if state.show_camera else "Camera off")
                state.camera_toggle_pressed = True
        else:
            state.camera_toggle_pressed = False

        if joystick.get_button(0):
            if not state.button_pressed:
                state.recording = not state.recording
                print("🎥 Recording: " + ("STARTED" if state.recording else "STOPPED"))
                say("Recording started" if state.recording else "Recording stopped")
                state.button_pressed = True
        else:
            state.button_pressed = False
