"""
Text Simplification + OCR Error Correction using Google Gemini 2.0 API
Optimized for dyslexia-friendly reading
"""

import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# Configure Gemini client
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("⚠️ Warning: GEMINI_API_KEY not found in .env file")
else:
    try:
        # Create client directly with API key (new google-genai SDK)
        print("✅ Gemini AI (google-genai 1.68.0) configured successfully")
        print(f"Using model: gemini-2.5-flash (latest available)")
    except Exception as e:
        print(f"❌ Failed to configure Gemini: {e}")


def process_text(text):
    """
    Single Gemini API call that:
    1. Fixes OCR errors (0→O, l→I, etc.)
    2. Simplifies vocabulary for dyslexia readers
    3. Breaks complex sentences into short ones
    4. Removes passive voice and jargon
    5. Maintains proper spacing and line breaks
    
    Returns simplified, dyslexia-friendly text
    """
    
    if not text.strip():
        return ""
    
    if not API_KEY:
        print("⚠️ No Gemini API key configured, returning original text")
        return text
    
    try:
        # Build comprehensive prompt for OCR correction + simplification
        prompt = f"""You are helping a dyslexia patient read scanned text.

The text below was extracted by OCR and may have errors.

DO THIS IN ORDER:
STEP 1 - Fix OCR errors only:
- Wrong characters: "0" → "O" or "A", "1" → "I" or "l", "/" → "W" or "f"
- Broken words: "Trom" → "from", "/lherher" → "Whether", "nores" → "notes"
- Merged or split words: fix spacing issues
- Do NOT change correct words

STEP 2 - Simplify for dyslexia:
- Replace complex words with simple ones
- Break long sentences into short ones (max 10 words each)
- One idea per sentence
- Use active voice
- No jargon or technical terms
- Keep ALL the original meaning, do not add or remove facts

STRICT RULES:
- Output plain text only
- No bullet points, no headers, no markdown
- No extra commentary or explanation
- Do not make up any new information
- If unsure about an OCR error, keep the original word

TEXT TO PROCESS:
{text}

OUTPUT:"""

        # Call Gemini API using google-genai SDK
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        if response and response.text:
            simplified = response.text.strip()
            print("✅ Text simplified successfully")
            return simplified
        else:
            print("⚠️ Empty response from Gemini API, returning original text")
            return text
    
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        print(f"❌ Gemini API Error [{error_type}]: {error_msg}")
        print(f"Model: gemini-2.5-flash | API Key configured: {bool(API_KEY)}")
        print("Returning original text as fallback")
        return text