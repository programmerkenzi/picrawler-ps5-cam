import threading
from modules.joystick import joystick_control
from modules.camera import camera_stream
from modules.voice import setup_voice, say

if __name__ == "__main__":
    setup_voice()
    say("Hello! This is PiCrawler.")
    t1 = threading.Thread(target=joystick_control)
    t2 = threading.Thread(target=camera_stream)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
