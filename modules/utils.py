import subprocess
import time


def wait_for_audio_ready(timeout=10):
    print("[🔍] Waiting for audio device to be listed...")
    for _ in range(timeout):
        try:
            out = subprocess.check_output(["aplay", "-l"]).decode()
            if "card" in out:
                print("[✅] Audio device ready.")
                return True
        except subprocess.CalledProcessError:
            pass
        time.sleep(1)
    print("[❌] No audio device found within timeout.")
    return False
