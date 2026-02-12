import spacy
from transformers import pipeline
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize NLP components globally to load only once
nlp = None
simplifier_model = None

def load_models():
    """Lazy load models to ensure app starts quickly and handles missing downloads"""
    global nlp, simplifier_model
    
    if nlp is None:
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.info("Downloading 'en_core_web_sm' model...")
            from spacy.cli import download
            download("en_core_web_sm")
            nlp = spacy.load("en_core_web_sm")

    if simplifier_model is None:
        try:
            # Use distilbert for faster inference suitable for real-time
            simplifier_model = pipeline("fill-mask", model="distilbert-base-uncased")
        except Exception as e:
            logger.error(f"Error loading transformer model: {e}")
            simplifier_model = None

def simplify_text(text):
    """
    Simplifies text by replacing complex words with simpler synonyms
    while preserving sentence structure and nouns.
    """
    load_models()
    
    if not text:
        return ""
        
    doc = nlp(text)
    new_tokens = []
    
    # Iterate through tokens
    for token in doc:
        # Check if the word is "complex" and safe to replace
        # Criteria for replacement:
        # 1. Long word (length > 6) - quick proxy for complexity
        # 2. Not a Noun or Proper Noun (pos_ not in ["NOUN", "PROPN"]) - preserves subjects/objects
        # 3. Is an Adjective, Adverb, or Verb (pos_ in ["ADJ", "ADV", "VERB"])
        # 4. Not a stop word
        # 5. Not a Named Entity (e.g. Person, Org)
        
        is_complex = (len(token.text) > 6 and 
                      token.pos_ in ["ADJ", "ADV", "VERB"] and 
                      not token.is_stop and 
                      token.ent_type_ == "")
                      
        if is_complex and simplifier_model:
            try:
                # Construct masked sentence to find context-aware synonyms
                # We replace the current token with [MASK]
                start_text = doc[:token.i].text_with_ws
                end_text = doc[token.i+1:].text_with_ws
                
                # Note: distilbert-base-uncased uses [MASK]
                masked_sentence = f"{start_text}[MASK]{token.whitespace_}{end_text}"
                
                # Get predictions (top 5 by default)
                predictions = simplifier_model(masked_sentence)
                
                best_replacement = token.text
                found_better = False
                
                for pred in predictions:
                    candidate = pred['token_str'].strip().lower()
                    original = token.text.lower()
                    
                    # Filter candidates:
                    # 1. No subwords (start with ##)
                    # 2. Not the same as original
                    # 3. Must be a valid word
                    if (candidate.startswith("##") or 
                        candidate == original or 
                        not candidate.isalpha()):
                        continue
                    
                    # Logic: Shorter words are generally simpler
                    if len(candidate) < len(original):
                        best_replacement = candidate
                        found_better = True
                        break # Take the highest probability simpler word
                
                # Restore case (Title, UPPER)
                if found_better:
                    if token.text.istitle():
                        best_replacement = best_replacement.title()
                    elif token.text.isupper():
                        best_replacement = best_replacement.upper()
                        
                new_tokens.append(best_replacement + token.whitespace_)
                
            except Exception as e:
                logger.error(f"Error simplifying word '{token.text}': {e}")
                new_tokens.append(token.text_with_ws)
        else:
            # Keep original token (nouns, short words, structure, punctuation)
            new_tokens.append(token.text_with_ws)
            
    return "".join(new_tokens)
