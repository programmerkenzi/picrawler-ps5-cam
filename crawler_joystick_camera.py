
# crawler_joystick_camera.py (restructured for true camera + recording toggling)
import threading
import pygame
import cv2
import time
from datetime import datetime
from picamera2 import Picamera2
from picrawler import Picrawler

# Initialize the PiCrawler robot
robot = Picrawler()

# Global variables
recording = False
joy_status = {'x': 0.0, 'y': 0.0}
button_pressed = False
show_camera = False
camera_toggle_pressed = False

# Joystick control thread
def joystick_control():
    global joy_status, recording, button_pressed, show_camera, camera_toggle_pressed

    pygame.init()
    pygame.joystick.init()

    try:
        if pygame.joystick.get_count() == 0:
            print("🔌 No controller detected. Attempting to connect via Bluetooth...")
            import subprocess
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
    except pygame.error:
        print("⚠️ No controller found. Please connect your PS5 controller.")
        return

    while True:
        pygame.event.pump()
        x = joystick.get_axis(0)
        y = joystick.get_axis(1)

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

        # Toggle camera display with Y button (index 3)
        if joystick.get_button(3):
            if not camera_toggle_pressed:
                show_camera = not show_camera
                print("📷 Camera display: " + ("ON" if show_camera else "OFF"))
                camera_toggle_pressed = True
        else:
            camera_toggle_pressed = False

        # Toggle recording with X button (index 0)
        if joystick.get_button(0):
            if not button_pressed:
                recording = not recording
                print("🎥 Recording: " + ("STARTED" if recording else "STOPPED"))
                button_pressed = True
        else:
            button_pressed = False

# Camera streaming and recording thread
def camera_stream():
    global joy_status, recording, show_camera

    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (640, 480)
    picam2.preview_configuration.main.format = "BGR888"
    picam2.configure("preview")
    picam2.start()

    out = None
    window_created = False

    while True:
        image = picam2.capture_array()

        if show_camera:
            # Display joystick axis values on frame
            cv2.putText(image, f"X: {joy_status['x']:.2f}  Y: {joy_status['y']:.2f}",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Show recording indicator
            if recording:
                cv2.putText(image, "REC", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            if not window_created:
                cv2.namedWindow("PiCamera2 Live", cv2.WINDOW_AUTOSIZE)
                window_created = True

            cv2.imshow("PiCamera2 Live", image)
        else:
            if window_created:
                try:
                    if cv2.getWindowProperty("PiCamera2 Live", cv2.WND_PROP_VISIBLE) >= 1:
                        cv2.destroyWindow("PiCamera2 Live")
                except:
                    pass
                window_created = False

        # Write frame to video only if recording
        if recording:
            if out is None:
                filename = datetime.now().strftime("record_%Y%m%d_%H%M%S.avi")
                out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))
            out.write(image)
        elif out:
            out.release()
            out = None

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if out:
        out.release()
    cv2.destroyAllWindows()

# Start threads
t1 = threading.Thread(target=joystick_control)
t2 = threading.Thread(target=camera_stream)
t1.start()
t2.start()
t1.join()
t2.join()
