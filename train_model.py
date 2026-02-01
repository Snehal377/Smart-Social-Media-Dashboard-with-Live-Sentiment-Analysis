import pandas as pd
import re
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Text cleaning function

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@\w+|#\w+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# Load reduced dataset

df = pd.read_csv("tweets_60k.csv")

df["tweet"] = df["tweet"].apply(clean_text)
df["label"] = df["sentiment"].map({"Negative": 0, "Positive": 1})

# Train-test split

X_train, X_test, y_train, y_test = train_test_split(
    df["tweet"], df["label"],
    test_size=0.2,
    random_state=42,
    stratify=df["label"]
)

# TF-IDF Vectorizer

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train Model

model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

# Evaluate

y_pred = model.predict(X_test_vec)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save Model & Vectorizer

joblib.dump(model, "sentiment_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

print("Model and vectorizer saved")
