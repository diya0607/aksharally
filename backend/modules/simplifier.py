import spacy
import re
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini client
client = genai.Client(api_key=API_KEY) if API_KEY else None
if client:
    print("Using Gemini AI (new SDK)")

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

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


def clean_ocr_errors(text):
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


def clean_output(text):
    """
    Clean Gemini or fallback output
    """
    text = re.sub(r"\n+", "\n", text)       # remove extra newlines
    text = re.sub(r"[ ]{2,}", " ", text)    # remove extra spaces
    return text.strip()


def simplify_text(text):
    if not text.strip():
        return ""

    # STEP 1: Clean OCR errors
    text = clean_ocr_errors(text)

    # STEP 2: Gemini AI
    if client:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"""
Simplify this text for a child or dyslexic reader.
Use very simple words and short sentences.
Keep line breaks if present.

{text}
"""
            )

            if response and hasattr(response, "text") and response.text:
                return clean_output(response.text)

        except Exception as e:
            print("Gemini error:", e)

    # STEP 3: Rule-based fallback
    doc = nlp(text)
    simplified_sentences = []

    for sent in doc.sents:
        words = []

        for token in sent:
            word = token.text
            lower_word = word.lower()

            if lower_word in SIMPLE_SYNONYMS:
                replacement = SIMPLE_SYNONYMS[lower_word]

                if word[0].isupper():
                    replacement = replacement.capitalize()

                words.append(replacement)
            else:
                words.append(word)

        new_sentence = " ".join(words)

        # Break long sentences
        if len(new_sentence.split()) > 12:
            parts = new_sentence.split(",")
            new_sentence = ". ".join(parts)

        new_sentence = re.sub(r"\s+", " ", new_sentence)
        new_sentence = re.sub(r"\s+\.", ".", new_sentence)
        new_sentence = new_sentence.strip()

        if not new_sentence.endswith("."):
            new_sentence += "."

        simplified_sentences.append(new_sentence)

    # KEEP STRUCTURE (important)
    return "\n".join(simplified_sentences)