# obstacle_warning.py (uses native ultrasonic with cooldown)
import time
from modules.voice import say
from modules.ultrasonic import get_distance

DISTANCE_THRESHOLD = 5  # cm
WARN_COOLDOWN = 5  # seconds
STABLE_CHECKS = 3


def monitor_obstacles():
    last_warn_time = 0

    while True:
        now = time.time()
        distances = [get_distance() for _ in range(STABLE_CHECKS)]
        avg_distance = sum(distances) / STABLE_CHECKS
        print(f"[📏] Distance: {avg_distance:.1f} cm")

        if avg_distance < DISTANCE_THRESHOLD and (now - last_warn_time > WARN_COOLDOWN):
            say("Warning. Obstacle ahead.")
            last_warn_time = now

        time.sleep(0.1)


if __name__ == "__main__":
    monitor_obstacles()
