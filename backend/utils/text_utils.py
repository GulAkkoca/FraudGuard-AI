def contains_any(text: str, needles: list[str]) -> bool:
    normalized = text.lower()
    return any(needle.lower() in normalized for needle in needles)

