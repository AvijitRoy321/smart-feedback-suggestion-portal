import joblib

# ==========================
# Load AI Model
# ==========================

model = joblib.load("models/sentiment_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")


# ==========================
# Sentiment Prediction
# ==========================

def predict_sentiment(text):

    text = text.lower().strip()

    # ==========================
    # Positive Rules
    # ==========================

    positive_phrases = [
        "not bad",
        "not so bad",
        "not too bad",
        "not terrible",
        "not poor",
        "not disappointing",
        "well done",
        "keep it up",
        "good job",
        "very good",
        "excellent",
        "awesome",
        "great",
        "fantastic",
        "nice",
        "best",
        "happy",
        "satisfied",
        "good",
        "love",
        "liked",
        "amazing",
        "wonderful",
        "perfect"
    ]

    # ==========================
    # Neutral Rules
    # ==========================

    neutral_phrases = [
        "average",
        "okay",
        "ok",
        "fine",
        "normal",
        "satisfactory",
        "acceptable",
        "manageable",
        "moderate",
        "fair",
        "decent"
    ]

    # ==========================
    # Negative Rules
    # ==========================

    negative_phrases = [
        "very bad",
        "extremely bad",
        "terrible",
        "worst",
        "poor",
        "disappointed",
        "not good",
        "not satisfied",
        "not happy",
        "awful",
        "hate",
        "useless",
        "dirty",
        "slow",
        "rude",
        "boring",
        "bad",
        "horrible",
        "pathetic",
        "waste"
    ]

    # ==========================
    # Check Positive
    # ==========================

    for phrase in positive_phrases:

        if phrase in text:

            return "Positive"

    # ==========================
    # Check Neutral
    # ==========================

    for phrase in neutral_phrases:

        if phrase in text:

            return "Neutral"

    # ==========================
    # Check Negative
    # ==========================

    for phrase in negative_phrases:

        if phrase in text:

            return "Negative"

    # ==========================
    # AI Prediction
    # ==========================

    vector = vectorizer.transform([text])

    prediction = model.predict(vector)

    return prediction[0]