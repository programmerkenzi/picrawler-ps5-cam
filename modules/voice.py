from robot_hat import Music, TTS

music = Music()
tts = TTS()


def setup_voice():
    music.music_set_volume(20)
    tts.lang("en-US")


def say(text: str):
    tts.say(text)
