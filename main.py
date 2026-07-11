import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from recognition.detector import run_detector
from voice.cue_generator import generate_cue
from voice.player import speak

# Person database — hardcoded for Phase 1 demo
# Add photos to data/photos/<Name>/ to activate each person
KNOWN_PEOPLE = {
    "Harvansh": {"relationship": "son",    "context": ""},
    "Japjeet":  {"relationship": "brother", "context": ""},
}

def on_face_detected(name: str, confidence: float):
    print(f"[KINNECT] Face confirmed: {name} ({confidence}%)")

    person = KNOWN_PEOPLE.get(name)
    if not person:
        print(f"[KINNECT] {name} not in database. Skipping voice cue.")
        return

    cue = generate_cue(
        person_name=name,
        relationship=person["relationship"],
        extra_context=person.get("context", "")
    )

    print(f"[KINNECT] Cue: '{cue}'")
    speak(cue)

if __name__ == "__main__":
    print("[KINNECT] Starting. Press Q in camera window to quit.")
    run_detector(on_face_detected)
