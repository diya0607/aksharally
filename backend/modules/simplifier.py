import spacy
import re
import requests

# Replace with your NEW API key
API_URL = "https://api-inference.huggingface.co/models/t5-small"
headers = {
    "Authorization": "Bearer Yhf_pQrVcuInOSHiounJiXToJcqqRwnMpIwdMW"
}

# Strong synonym mapping (expanded)
SIMPLE_SYNONYMS = {
    "frequently": "often",
    "utilize": "use",
    "individuals": "people",
    "numerous": "many",
    "demonstrates": "shows",
    "approximately": "about",
    "objective": "goal",
    "domain": "area",
    "indicators": "signs",
    "detected": "found",
    "assess": "check",
    "monitor": "watch",
    "conditions": "situations",
    "isolation": "being alone",
    "comprehension": "understanding",
    "neighborhood": "area",
    "learned": "studied",
    "another": "each other",
    "children": "kids",
    "difficult": "hard",
    "understand": "know",
    "information": "details",
    "grandfather": "grandpa"
}

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


def clean_ocr_errors(text):
    """Fix common OCR mistakes"""
    corrections = {
        "arc": "are",
        "storics": "stories",
        "belicved": "believed",
        "ycars": "years",
        "usc": "use",
        "Acsop": "Aesop"
    }

    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)

    return text


def simplify_text(text):
    """
    Dyslexia-friendly simplification pipeline
    """

    if not text.strip():
        return ""

    # STEP 1: Clean OCR errors
    text = clean_ocr_errors(text)

    # STEP 2: Try AI (optional enhancement)
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={
                "inputs": "Simplify this text using very easy words for children:\n" + text,
                "parameters": {"max_length": 150}
            }
        )

        result = response.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]

    except Exception:
        pass  # fallback below

    # STEP 3: Rule-based simplification (MAIN LOGIC)
    doc = nlp(text)
    simplified_sentences = []

    for sent in doc.sents:
        words = []

        for token in sent:
            word = token.text
            lower_word = word.lower()

            if lower_word in SIMPLE_SYNONYMS:
                replacement = SIMPLE_SYNONYMS[lower_word]

                # Preserve capitalization
                if word[0].isupper():
                    replacement = replacement.capitalize()

                words.append(replacement)
            else:
                words.append(word)

        # Rebuild sentence
        new_sentence = " ".join(words)

        # Simplify grammar
        new_sentence = new_sentence.replace("had been", "was")
        new_sentence = new_sentence.replace("it is believed that", "")

        # Clean formatting
        new_sentence = re.sub(r"\s+", " ", new_sentence)
        new_sentence = re.sub(r"\s+\.", ".", new_sentence)
        new_sentence = new_sentence.strip()

        # Shorten long sentences (VERY IMPORTANT)
        if len(new_sentence.split()) > 12:
            new_sentence = new_sentence.replace(",", ".")

        # Ensure proper ending
        if not new_sentence.endswith("."):
            new_sentence += "."

        simplified_sentences.append(new_sentence)

    return " ".join(simplified_sentences)