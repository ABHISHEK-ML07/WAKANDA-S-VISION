from sklearn.feature_extraction.text import TfidfVectorizer

# Common useless words
STOPWORDS = {"me", "is", "the", "a", "an", "in", "on", "at", "to", "for", "of", "and"}


def normalize_scores(scores_dict):
    max_score = max(scores_dict.values()) if scores_dict else 1
    return {k: v / max_score for k, v in scores_dict.items()}


def label_score(score):
    if score > 0.75:
        return "HIGH"
    elif score > 0.4:
        return "MEDIUM"
    else:
        return "LOW"


def get_token_importance(text):
    words = text.split()

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]

    tfidf_scores = {}
    for word in words:
        word_lower = word.lower()
        if word_lower in feature_names:
            idx = list(feature_names).index(word_lower)
            tfidf_scores[word] = float(scores[idx])
        else:
            tfidf_scores[word] = 0.0

    position_scores = {}
    for i, word in enumerate(words):
        position_scores[word] = 1 / (i + 1)

    length_scores = {}
    for word in words:
        length_scores[word] = len(word) / 10

    combined_scores = {}
    for word in words:
        combined_scores[word] = (
            tfidf_scores[word] * 0.6 +
            position_scores[word] * 0.2 +
            length_scores[word] * 0.2
        )

        # 🔥 NEW: Penalize stopwords
        if word.lower() in STOPWORDS:
            combined_scores[word] *= 0.3

    final_scores = normalize_scores(combined_scores)

    labeled_scores = {}
    for word, score in final_scores.items():
        labeled_scores[word] = {
            "score": round(score, 3),
            "level": label_score(score)
        }

    return labeled_scores