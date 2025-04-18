import pygame
import time
import subprocess
from picrawler import Picrawler
from shared.state import (
    recording,
    show_camera,
    joy_status,
    button_pressed,
    camera_toggle_pressed,
)
from modules.voice import say

robot = Picrawler()


def joystick_control():
    global recording, show_camera, joy_status, button_pressed, camera_toggle_pressed

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
        joy_status["x"] = x
        joy_status["y"] = y

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
            if not camera_toggle_pressed:
                show_camera = not show_camera
                print("📷 Camera display: " + ("ON" if show_camera else "OFF"))
                say("Camera on" if show_camera else "Camera off")
                camera_toggle_pressed = True
        else:
            camera_toggle_pressed = False

        if joystick.get_button(0):
            if not button_pressed:
                recording = not recording
                print("🎥 Recording: " + ("STARTED" if recording else "STOPPED"))
                say("Recording started" if recording else "Recording stopped")
                button_pressed = True
        else:
            button_pressed = False
