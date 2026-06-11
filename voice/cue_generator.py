def generate_cue(person_name: str, relationship: str, extra_context: str = "") -> str:
    """
    Generates a short, natural spoken cue for the patient.
    Warm, simple, non-alarming.
    """
    cues = {
        "son":           f"Hi, it's your son {person_name}. I'm right here with you.",
        "daughter":      f"Hi, it's your daughter {person_name}. So good to see you.",
        "grandson":      f"Hey, it's me, {person_name}, your grandson.",
        "granddaughter": f"Hi, it's {person_name}, your granddaughter. I love you.",
        "husband":       f"It's your husband {person_name}. I'm right here.",
        "wife":          f"It's your wife {person_name}. Everything is okay.",
        "friend":        f"Hi, it's your friend {person_name}. Great to see you.",
        "caregiver":     f"Hi, it's {person_name}, your caregiver. You're in good hands.",
        "doctor":        f"Hello, it's Dr. {person_name}. You're doing wonderfully.",
    }

    key = relationship.lower().strip()
    base = cues.get(key, f"Hi, it's {person_name}. {relationship}.")

    if extra_context:
        base += f" {extra_context}"

    return base


if __name__ == "__main__":
    print(generate_cue("Harvansh", "son"))
    print(generate_cue("Priya", "daughter"))
    print(generate_cue("Dr. Mehta", "doctor"))
