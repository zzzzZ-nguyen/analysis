# ==========================================
# ⚡ ADVANCED SENTIMENT MODEL TRAINER PRO MAX
# TF-IDF + Logistic Regression + GridSearchCV + Auto Dataset Loader
# ==========================================

import os
import re
import joblib
import json
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure NLTK data
nltk.download("stopwords")
nltk.download("wordnet")

# ================================
# 🎨 Terminal Colors
# ================================
OK = "\033[92m"
INFO = "\033[94m"
WARN = "\033[93m"
ERR = "\033[91m"
END = "\033[0m"


# ==========================================
# 🧹 ADVANCED TEXT CLEANER
# ==========================================
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


def clean_text(text):
    text = text.lower()

    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#\w+", "", text)

    # Remove emoji
    text = re.sub(r"[^\w\s,!?]", " ", text)

    # Remove special chars
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    # Lemmatization + stopwords
    words = [lemmatizer.lemmatize(w) for w in text.split() if w not in stop_words]
    return " ".join(words)


# ==========================================
# 📂 AUTO DATA LOADER
# ==========================================
def load_dataset():
    dataset_path = "data/sentiment_dataset.csv"

    if os.path.exists(dataset_path):
        print(f"{INFO}📂 Loading dataset from {dataset_path}{END}")
        df = pd.read_csv(dataset_path)

        if "text" not in df.columns or "label" not in df.columns:
            raise ValueError("CSV must contain 'text' and 'label' columns")

        return df["text"].tolist(), df["label"].tolist()

    # Fallback dataset
    print(f"{WARN}⚠ No external dataset found → Using built-in sample dataset.{END}")

    texts = [
        "This product is very good",
        "Excellent quality and fast delivery",
        "Amazing experience, I love it",
        "I am extremely satisfied",
        "Worth the price",

        "Bad product, very disappointed",
        "Terrible quality, waste of money",
        "Very poor experience",
        "I hate this item",
        "Worst purchase ever",

        "It is okay, not bad",
        "Average quality",
        "Not good, not bad",
        "The product is acceptable",
        "Quality is fine"
    ]

    labels = [
        "positive", "positive", "positive", "positive", "positive",
        "negative", "negative", "negative", "negative", "negative",
        "neutral", "neutral", "neutral", "neutral", "neutral"
    ]

    return texts, labels


# ==========================================
# 🚀 TRAIN & DUMP MODEL
# ==========================================
def train_and_dump():

    # Load dataset
    texts, labels = load_dataset()

    print(f"{INFO}🧹 Cleaning dataset…{END}")
    texts_cleaned = [clean_text(t) for t in texts]

    # Encode labels
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(labels)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        texts_cleaned, y, test_size=0.2, random_state=42
    )

    # Pipeline
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", LogisticRegression(max_iter=1000, solver="saga"))
    ])

    # Hyperparameters
    param_grid = {
        "tfidf__ngram_range": [(1,1), (1,2)],
        "tfidf__min_df": [1, 2, 3],
        "clf__C": [0.5, 1, 2, 5, 10],
        "clf__penalty": ["l1", "l2"],
    }

    print(f"{INFO}🔍 Running GridSearchCV…{END}")

    grid = GridSearchCV(
        pipeline,
        param_grid,
        scoring="accuracy",
        cv=3,
        n_jobs=-1,
        verbose=1
    )

    grid.fit(X_train, y_train)

    # Evaluate
    preds = grid.predict(X_test)
    acc = accuracy_score(y_test, preds)
    p, r, f1, _ = precision_recall_fscore_support(y_test, preds, average="weighted")

    print(f"{OK}🎯 Test Accuracy: {acc:.3f}{END}")
    print(f"{OK}📊 Precision: {p:.3f}, Recall: {r:.3f}, F1: {f1:.3f}{END}")
    print(f"{OK}🏆 Best Parameters: {grid.best_params_}{END}")

    # Create model directory
    os.makedirs("models", exist_ok=True)

    # Save objects
    joblib.dump(grid.best_estimator_, "models/model_en.pkl")
    joblib.dump(label_encoder, "models/label_encoder.pkl")

    print(f"{OK}📦 Model saved → models/model_en.pkl{END}")
    print(f"{OK}📦 Label encoder saved → models/label_encoder.pkl{END}")
    print(f"{INFO}🌟 Training Completed Successfully!{END}")


if __name__ == "__main__":
    train_and_dump()
