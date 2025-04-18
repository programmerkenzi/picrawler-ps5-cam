from robot_hat import Music, TTS
import threading

music = Music()


def setup_voice():
    music.music_set_volume(20)


def say(text: str):
    def speak():
        tts = TTS()
        tts.lang("en-US")
        tts.say(text)

    print(f"[🔊] Saying: {text}")
    threading.Thread(target=speak, daemon=True).start()
