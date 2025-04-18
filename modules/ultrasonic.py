import RPi.GPIO as GPIO
import time

# Pin config (BCM mode)
TRIG_PIN = 23
ECHO_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Ensure trigger is low
GPIO.output(TRIG_PIN, False)
time.sleep(0.1)


def get_distance():
    # Send 10us pulse to trigger
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    start_time = time.time()
    stop_time = time.time()

    # Wait for echo start
    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()

    # Wait for echo end
    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()

    # Time difference
    elapsed = stop_time - start_time
    # Distance calculation (cm)
    distance = (elapsed * 34300) / 2
    return round(distance, 1)


if __name__ == "__main__":
    try:
        while True:
            d = get_distance()
            print(f"Distance: {d} cm")
            time.sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()
