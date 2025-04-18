import threading
import queue
import os

speech_queue = queue.Queue()


def setup_voice():
    def speech_worker():
        while True:
            text = speech_queue.get()
            print(f"[?] Saying: {text}")
            os.system(
                f'espeak -w /tmp/say.wav "{text}" 2>/dev/null && aplay -D plughw:1,0 /tmp/say.wav 2>/dev/null'
            )
            speech_queue.task_done()

    threading.Thread(target=speech_worker, daemon=True).start()


def say(text: str):
    speech_queue.put(text)
