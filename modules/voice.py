from robot_hat import Music, TTS
import threading

music = Music()
tts = TTS()


def setup_voice():
    music.music_set_volume(20)
    tts.lang("en-US")


def say(text: str):
    print(f"[?] Saying: {text}")
    threading.Thread(target=tts.say, args=(text,), daemon=True).start()
