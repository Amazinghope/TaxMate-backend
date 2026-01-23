BANNED_TOPICS = [
  "calculate", "upload", "file my tax", "bank statement",
  "how much tax", "submit returns"
]

def validate_message(text: str) -> bool:
    t = text.lower()
    return not any(word in t for word in BANNED_TOPICS)
