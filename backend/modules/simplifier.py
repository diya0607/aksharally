# modules/simplifier.py

# Simple synonym mapping for difficult words
SIMPLE_SYNONYMS = {
    "frequently": "often",
    "utilize": "use",
    "individuals": "people",
    "numerous": "many",
    "demonstrates": "shows",
    "approximately": "about",
    "objective": "clear",
    "domain": "area",
    "indicators": "signs",
    "detected": "found",
    "assess": "check",
    "monitor": "watch",
    "conditions": "situations",
    "isolation": "being alone",
    "comprehension": "understanding"
}


def simplify_text(text):
    """
    Lightweight simplifier using synonym replacement.
    Fast, stable, no heavy AI models.
    """

    if not text:
        return ""

    words = text.split()
    simplified_words = []

    for word in words:
        # Remove punctuation for matching
        clean_word = word.lower().strip(".,!?;:")

        if clean_word in SIMPLE_SYNONYMS:
            replacement = SIMPLE_SYNONYMS[clean_word]

            # Preserve capitalization style
            if word.istitle():
                replacement = replacement.title()
            elif word.isupper():
                replacement = replacement.upper()

            simplified_words.append(replacement)
        else:
            simplified_words.append(word)

    return " ".join(simplified_words)
