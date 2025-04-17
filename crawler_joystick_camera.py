
# crawler_joystick_camera.py
import threading
import pygame
import cv2
import time
from datetime import datetime
from picamera import PiCamera
from picamera.array import PiRGBArray
from picrawler import Picrawler

# Initialize the PiCrawler robot
robot = Picrawler()

# Global variables
recording = False
joy_status = {'x': 0.0, 'y': 0.0}

# Joystick control thread
def joystick_control():
    global joy_status, recording

    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    while True:
        pygame.event.pump()
        x = joystick.get_axis(0)
        y = joystick.get_axis(1)
        joy_status['x'] = x
        joy_status['y'] = y

        speed = 30

        if y < -0.5:
            robot.forward(speed)
        elif y > 0.5:
            robot.backward(speed)
        elif x < -0.5:
            robot.left(speed)
        elif x > 0.5:
            robot.right(speed)
        else:
            robot.stop()

        # Press X button (index 0) to toggle recording
        if joystick.get_button(0):
            recording = not recording
            time.sleep(0.5)  # Debounce delay

        time.sleep(0.1)

# Camera streaming and recording thread
def camera_stream():
    global joy_status, recording

    camera = PiCamera()
    camera.resolution = (640, 480)
    raw_capture = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.1)

    out = None

    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array

        # Display joystick axis values
        cv2.putText(image, f"X: {joy_status['x']:.2f}  Y: {joy_status['y']:.2f}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Show recording status and write video
        if recording:
            if out is None:
                filename = datetime.now().strftime("record_%Y%m%d_%H%M%S.avi")
                out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))
            cv2.putText(image, "REC", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            out.write(image)
        elif out:
            out.release()
            out = None

        cv2.imshow("Pi Camera Live", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        raw_capture.truncate(0)

    camera.close()
    if out:
        out.release()
    cv2.destroyAllWindows()

# Start both threads
t1 = threading.Thread(target=joystick_control)
t2 = threading.Thread(target=camera_stream)
t1.start()
t2.start()
t1.join()
t2.join()
