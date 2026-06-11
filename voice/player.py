import os
import requests
import pygame
import tempfile
import time
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Sarah — Mature, Reassuring, Confident
# Swap this voice_id when you upgrade to paid and clone a real family voice
DEFAULT_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

def speak(text: str, voice_id: str = DEFAULT_VOICE_ID) -> bool:
    """
    Converts text to speech via ElevenLabs and plays it immediately.
    Returns True on success, False on failure.
    """
    print(f"[VOICE] Speaking: '{text}'")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }

    payload = {
        "text": text,
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.85
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            print(f"[VOICE ERROR] Status {response.status_code}: {response.text}")
            return False

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            f.write(response.content)
            temp_path = f.name

        pygame.mixer.init()
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.quit()
        os.unlink(temp_path)

        print("[VOICE] Playback complete.")
        return True

    except Exception as e:
        print(f"[VOICE EXCEPTION] {e}")
        return False


if __name__ == "__main__":
    speak("Hi, it's your son Harvansh. I'm right here with you.")
