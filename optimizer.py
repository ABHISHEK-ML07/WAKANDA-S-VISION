import re

REWRITE_RULES = {
    "explain": "analyze",
    "basically": "",
    "with": "including",
    "and": ",",
    "in detail": ""
}

def smart_rewrite(prompt):
    text = prompt.lower()

    for key, val in REWRITE_RULES.items():
        text = text.replace(key, val)

    text = re.sub(r'\s+,', ',', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text.capitalize()


def optimize_prompt(prompt, importance):
    words = prompt.split()

    # remove LOW importance
    trimmed_words = [
        w for w in words
        if w in importance and importance[w]["level"] != "LOW"
    ]

    trimmed = " ".join(trimmed_words)

    if not trimmed:
        trimmed = prompt

    rewritten = smart_rewrite(trimmed)

    best = rewritten if len(rewritten) < len(prompt) else trimmed

    return {
        "original": prompt,
        "trimmed": trimmed,
        "rewritten": rewritten,
        "best_prompt": best,
        "method_used": "SMART_REWRITE",
        "original_tokens": len(words),
        "final_tokens": len(best.split()),
        "tokens_saved": len(words) - len(best.split())
    }