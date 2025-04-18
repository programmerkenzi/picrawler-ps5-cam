# joystick.py with front/back leg height control using L1/L2 and R1/R2, L3 to reset
import pygame
import time
import subprocess
from picrawler import Picrawler
from modules.voice import say
from shared.state import (
    recording,
    show_camera,
    joy_status,
    button_pressed,
    camera_toggle_pressed,
)

robot = Picrawler()

RAISED_MAX = 90
NORMAL_HEIGHT = 20

front_leg_angle = NORMAL_HEIGHT
back_leg_angle = NORMAL_HEIGHT


def clamp(val, min_val, max_val):
    return max(min(val, max_val), min_val)


def joystick_control():
    global recording, show_camera, joy_status, button_pressed, camera_toggle_pressed
    global front_leg_angle, back_leg_angle

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

        # Toggle camera display with Y (button 3)
        if joystick.get_button(3):
            if not camera_toggle_pressed:
                show_camera = not show_camera
                print("📷 Camera display: " + ("ON" if show_camera else "OFF"))
                say("Camera on" if show_camera else "Camera off")
                camera_toggle_pressed = True
        else:
            camera_toggle_pressed = False

        # Toggle recording with X (button 0)
        if joystick.get_button(0):
            if not button_pressed:
                recording = not recording
                print("🎥 Recording: " + ("STARTED" if recording else "STOPPED"))
                say("Recording started" if recording else "Recording stopped")
                button_pressed = True
        else:
            button_pressed = False

        # L1 (button 4) raises front legs, L2 (button 6) lowers them
        if joystick.get_button(4):
            front_leg_angle = clamp(front_leg_angle + 1, NORMAL_HEIGHT, RAISED_MAX)
        elif joystick.get_button(6):
            front_leg_angle = clamp(front_leg_angle - 1, NORMAL_HEIGHT, RAISED_MAX)
        robot.set_leg_angle(0, [90, front_leg_angle, 90])
        robot.set_leg_angle(1, [90, front_leg_angle, 90])

        # R1 (button 5) raises back legs, R2 (button 7) lowers them
        if joystick.get_button(5):
            back_leg_angle = clamp(back_leg_angle + 1, NORMAL_HEIGHT, RAISED_MAX)
        elif joystick.get_button(7):
            back_leg_angle = clamp(back_leg_angle - 1, NORMAL_HEIGHT, RAISED_MAX)
        robot.set_leg_angle(2, [90, back_leg_angle, 90])
        robot.set_leg_angle(3, [90, back_leg_angle, 90])

        # L3 (button 10) resets all legs to normal
        if joystick.get_button(10):
            front_leg_angle = back_leg_angle = NORMAL_HEIGHT
            for i in range(4):
                robot.set_leg_angle(i, [90, NORMAL_HEIGHT, 90])
            say("Legs reset")
            time.sleep(0.3)
