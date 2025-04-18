import threading
import os


def say(text: str):
    def speak():
        os.system(f'espeak "{text}"')

    print(f"[🔊] Saying: {text}")
    threading.Thread(target=speak, daemon=True).start()
