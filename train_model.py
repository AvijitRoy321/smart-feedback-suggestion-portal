import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load Dataset
data = pd.read_csv("dataset/feedback_dataset.csv")

# Input
X = data["feedback"]

# Output
y = data["sentiment"]

# Convert text into numbers
vectorizer = TfidfVectorizer()

X_vector = vectorizer.fit_transform(X)

# Create Model
model = LogisticRegression()

# Train Model
model.fit(X_vector, y)

# Save Model
joblib.dump(model, "models/sentiment_model.pkl")

# Save Vectorizer
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("Model Trained Successfully")