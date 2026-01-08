# ==========================================
# 🔥 ADVANCED SENTIMENT MODEL TRAINER
# TF-IDF + Logistic Regression + GridSearchCV
# ==========================================

import os
import joblib
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score


# =====================================================
# 🧹 TEXT CLEANER
# =====================================================
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def train_and_dump():
    # =====================================================
    # 📌 DATASET (ENHANCED ENGLISH SENTIMENT DATASET)
    # =====================================================
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

    # Clean text
    texts_cleaned = [clean_text(t) for t in texts]

    # =====================================================
    # ⚙️ PIPELINE + HYPERPARAMETER TUNING
    # =====================================================
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(stop_words="english")),
        ("clf", LogisticRegression(max_iter=500))
    ])

    param_grid = {
        "tfidf__ngram_range": [(1,1), (1,2)],
        "clf__C": [0.5, 1, 2, 5]
    }

    print("🔍 Running GridSearchCV…")

    grid = GridSearchCV(
        pipeline,
        param_grid,
        scoring="accuracy",
        cv=3,
        n_jobs=-1,
        verbose=1
    )

    grid.fit(texts_cleaned, labels)

    print("✅ Best Parameters:", grid.best_params_)

    # =====================================================
    # 🎯 EVALUATION
    # =====================================================
    preds = grid.predict(texts_cleaned)
    acc = accuracy_score(labels, preds)
    print(f"🎉 Training Accuracy: {acc:.2f}")

    # =====================================================
    # 💾 SAVE MODEL
    # =====================================================
    model_dir = "models"
    os.makedirs(model_dir, exist_ok=True)

    model_path = os.path.join(model_dir, "model_en.pkl")
    joblib.dump(grid.best_estimator_, model_path)

    print("📦 Saved model:", model_path)
    print("🌟 Training Completed Successfully!")


if __name__ == "__main__":
    train_and_dump()
