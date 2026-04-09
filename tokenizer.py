import re

# Stopwords = LOW importance
STOPWORDS = set([
    "the", "and", "of", "in", "a", "to", "is", "for", "on", "with",
    "as", "by", "an", "be", "this", "that", "it"
])


def clean_tokens(text):
    words = re.findall(r'\b\w+\b', text)
    return words


def get_token_importance(text):
    tokens = clean_tokens(text)
    importance = {}

    for word in tokens:
        w = word.lower()

        # RULE-BASED SCORING
        if w in STOPWORDS:
            score = 0.1

        elif len(w) > 7:
            score = 0.8

        elif word[0].isupper():  # Proper nouns
            score = 0.7

        else:
            score = 0.5

        score = round(score, 3)

        # LEVEL CLASSIFICATION
        if score >= 0.75:
            level = "HIGH"
        elif score >= 0.4:
            level = "MEDIUM"
        else:
            level = "LOW"

        importance[word] = {
            "score": score,
            "level": level
        }

    return importance