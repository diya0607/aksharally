import sys
import os

# Ensure we can import modules from current directory
sys.path.append(os.getcwd())

try:
    from modules.simplifier import simplify_text
except ImportError:
    print("Could not import simplify_text. Make sure you are in the 'backend' directory.")
    sys.exit(1)

test_sentences = [
    "The inherent complexities of the universe are staggering.",
    "The implementation of the algorithm was meticulous.",
    "She utilized the apparatus to demonstrate the phenomenon."
]

print("Loading models and running tests...")
for sentence in test_sentences:
    print(f"\nOriginal: {sentence}")
    try:
        simplified = simplify_text(sentence)
        print(f"Simplified: {simplified}")
    except Exception as e:
        print(f"Error: {e}")
