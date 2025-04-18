import threading
from modules.joystick import joystick_control
from modules.camera import camera_stream
from modules.utils import wait_for_audio_ready
from modules.voice import say

if __name__ == "__main__":
    if wait_for_audio_ready():
        say("Hello! This is PiCrawler.")
        t1 = threading.Thread(target=joystick_control)
        t2 = threading.Thread(target=camera_stream)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
