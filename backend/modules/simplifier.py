import spacy

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

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")


def simplify_text(text):
    """
    Lexical + structural text simplification.
    Replaces difficult words with simpler synonyms
    and removes unnecessary complexity.
    """

    doc = nlp(text)
    simplified_sentences = []

    for sent in doc.sents:
        words = []

        for token in sent:
            word = token.text

            # Replace difficult words with simpler synonyms
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

        # Clean spacing before punctuation
        new_sentence = new_sentence.replace(" ,", ",").replace(" .", ".")

        # Shorten very long sentences
        if len(new_sentence.split()) > 20:
            new_sentence = new_sentence.replace(",", ".")
        
        if not new_sentence.endswith("."):
            new_sentence += "."

        simplified_sentences.append(new_sentence)

    return " ".join(simplified_sentences)
