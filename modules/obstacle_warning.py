import time
from modules.voice import say
from modules.ultrasonic import get_distance

DISTANCE_THRESHOLD = 5  # cm


def monitor_obstacles():
    while True:
        distance = get_distance()
        print(f"[📏] Distance: {distance:.1f} cm")

        if distance < DISTANCE_THRESHOLD:
            say("Warning. Obstacle ahead.")
            time.sleep(2)  # prevent spam

        time.sleep(0.1)
